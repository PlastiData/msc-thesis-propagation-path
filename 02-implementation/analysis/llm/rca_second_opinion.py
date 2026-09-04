#!/usr/bin/env -S uv run -s
"""Pilot: can a cheap LLM improve on the RCA-seeded root-cause guess?

RCA-seeded means the candidate path was built starting from the algorithm's own
rank1 guess (not the true injection point). Two failure modes exist there:
  - the guess itself is wrong (algo_hit_at_1 is False)
  - the guess is right but a path still couldn't be built (rca_status refused)
This shows each model the algorithm's specific seed plus the evidence, in plain
language, and asks it to confirm/replace the seed - a second-opinion/re-ranking
task, not a blind independent guess. What must never be shown is which service
was actually injected; everything else, including the algorithm's own guess, is
fair game (that's the point - see the redaction rules in build_payload()).

No parquet is read and no pipeline step is re-run: this only reads the already
-computed machine_graph.json files under an evidence_path_poc run (--sample/
--policy) and each case's real injection.json (for scoring only, never sent to
a model). The prompt is built fresh per case from that case's own
machine_graph.json (see render_prompt()) - nothing about a specific case or
dataset is hardcoded, so pointing --sample at a different dataset's
evidence_path_poc output reproduces the same pilot there unchanged.

Usage:
    uv run analysis/rca_second_opinion.py --limit 3 --dry-run   # payload+leak check only
    uv run analysis/rca_second_opinion.py --limit 3             # one real batch, all registry models
    uv run analysis/rca_second_opinion.py                       # full 18-case pilot (sample_all/strict)
    uv run analysis/rca_second_opinion.py --sample pilot_cases  # same pilot against a different run
    uv run analysis/rca_second_opinion.py --models gemini-3.7-flash,gemini-3.5-flash-lite  # subset
"""

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

ANALYSIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = ANALYSIS_DIR.parent
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

# loads ANTHROPIC_API_KEY / OPENAI_API_KEY into this process's env before any
# subprocess call - claude/codex CLIs then bill against the API key instead of
# falling back to subscription OAuth, with no per-call code change needed.
load_dotenv(ANALYSIS_DIR / ".env")

from pipeline.emit import (  # reuse the exact dashboard renderers - never reimplement
    _path_svg,
    _path_strip_html,
    _pct,
    _short,
    outcome_breakdown_rows,
)
CHARTS_DIR = ANALYSIS_DIR / "output_charts"
RAW_ROOT = REPO_ROOT / "data" / "rcabench-platform-v2" / "data" / "rcabench"

CLAUDE = shutil.which("claude")
CODEX = shutil.which("codex")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# strings that must never appear anywhere in a redacted payload - the true injected
# service must survive only as an unmarked candidate, never as a labelled answer.
BANNED_TEXT = ("ground_truth", "known_injection", "injected fault", "fault_type", "injection")



ALL_BUCKETS = ("wrong_accepted", "wrong_refused", "correct_refused")


def select_pilot(
    seed: int, n_per_bucket: int | None, sample_dir: Path, buckets: tuple[str, ...] = ALL_BUCKETS
) -> list[dict]:
    """`n_per_bucket=None` takes every case in each bucket (no sampling at all) -
    that's how you run every eligible case, not just a draw from it. `buckets`
    narrows which outcome groups are eligible in the first place - e.g.
    ("wrong_accepted", "wrong_refused") for "RCA was wrong" only, dropping
    correct_refused."""
    summary = json.loads((sample_dir / "summary.json").read_text())
    cases = summary["cases"]

    by_bucket = {
        "wrong_accepted": [c for c in cases if c["algo_hit_at_1"] is False and c["rca_status"] == "candidate_path_constructed"],
        "wrong_refused": [c for c in cases if c["algo_hit_at_1"] is False and c["rca_status"] == "insufficient_evidence"],
        "correct_refused": [c for c in cases if c["algo_hit_at_1"] is True and c["rca_status"] == "insufficient_evidence"],
    }

    rng = random.Random(seed)
    picked = []
    for bucket_name in buckets:
        bucket = by_bucket[bucket_name]
        take = len(bucket) if n_per_bucket is None else min(n_per_bucket, len(bucket))
        for c in rng.sample(bucket, take):
            picked.append({**c, "_bucket": bucket_name})
    return picked



def find_leaks(payload: dict) -> list[str]:
    blob = json.dumps(payload).lower()
    return [t for t in BANNED_TEXT if t in blob]


def strip_rankings(rankings: dict) -> dict:
    out = {}
    for name, entry in (rankings or {}).items():
        out[name] = {
            "rank1": entry.get("rank1"),
            "top_services": [s.get("service") for s in entry.get("top_services", [])],
        }
    return out


def build_payload(case_dir: Path) -> dict:
    machine = json.loads((case_dir / "machine_graph.json").read_text())

    algo = machine.get("algo_context") or {}
    algo_safe = {
        "algo": algo.get("algo"),
        "algo_ac_at_1": algo.get("algo_ac_at_1"),
        "available": algo.get("available"),
        "rank1": algo.get("rank1"),
        "predicted_chain": algo.get("predicted_chain"),
        "rankings": strip_rankings(algo.get("rankings")),
    }

    rca = machine.get("rca_path") or {}
    rca_judgment = rca.get("judgment") or {}
    rca_safe = {
        "status": rca_judgment.get("status"),
        "primary_rejection_reason": rca_judgment.get("primary_rejection_reason"),
        "rejection_reasons": rca_judgment.get("rejection_reasons"),
    }

    registry = machine.get("evidence_registry") or []
    registry_safe = [
        e for e in registry
        if e.get("evidence_id") != "injection_facts" and e.get("source_file") != "injection.json"
    ]

    payload = {
        "candidate_graph": machine.get("candidate_graph"),
        "evidence_registry": registry_safe,
        "algo_context": algo_safe,
        "rca_path": rca_safe,
        "case_metrics": machine.get("case_metrics"),
    }
    return payload



def edges_prose(candidate_graph: dict) -> str:
    lines = []
    for e in (candidate_graph or {}).get("edges", [])[:40]:
        checks = e.get("checks") or {}
        lines.append(
            f"  - {e.get('source')} -> {e.get('target')}: "
            f"statistical={checks.get('statistical')}, structural={checks.get('structural')}, "
            f"temporal={checks.get('temporal')}"
        )
    return "\n".join(lines) if lines else "  (no candidate connections found)"


def evidence_prose(registry: list) -> str:
    lines = []
    for e in registry:
        claim = e.get("claim")
        if not claim:
            continue
        hits = ((e.get("detail") or {}).get("hits")) or []
        # a claim like "shows 3 abnormal metric signal(s)" hides HOW abnormal - two
        # services can show the same signal count with very different magnitudes.
        # surface the strongest z-score/ratio so the model can actually compare them.
        mags = [abs(h.get("z", h.get("ratio", 0)) or 0) for h in hits]
        peak = f" (strongest deviation: {max(mags):.1f}x normal)" if mags else ""
        lines.append(f"  - {claim}{peak}")
    lines = lines[:30]
    return "\n".join(lines) if lines else "  (no additional evidence signals)"


def baselines_prose(algo_context: dict) -> str:
    lines = []
    for name, r in (algo_context.get("rankings") or {}).items():
        if name == algo_context.get("algo"):
            continue
        lines.append(f"  - {name} -> {r.get('rank1')}")
    return "\n".join(lines) if lines else "  (no other baselines available)"


def temporal_note(candidate_graph: dict) -> str:
    edges = (candidate_graph or {}).get("edges", [])
    if any(e.get("checks", {}).get("temporal") != "unknown" for e in edges):
        return (
            "NOTE: temporal ordering (onset-timestamp order between two services) is "
            "resolved for some of these edges (pass/fail) and unknown for others - use it "
            "where it's resolved, and where it's unknown, decide from statistical/structural "
            "signals and magnitudes instead. Ordering may come from Error-span onset or from "
            "a latency-anomaly fallback when no Error span exists at both endpoints."
        )
    return (
        "NOTE: temporal ordering is unknown for every edge in this case (no Error span and "
        "no usable latency-anomaly onset at both endpoints to order). Do not treat that as a "
        "gap unique to this case or wait for it; decide from the statistical/structural "
        "signals and magnitudes below instead."
    )


def render_prompt(case: dict, payload: dict) -> str:
    algo = payload["algo_context"]
    rca = payload["rca_path"]
    seed = algo.get("rank1")

    if rca.get("status") == "candidate_path_constructed":
        outcome = f"A path WAS built from that starting point to the symptom, but that does not confirm it is correct - only that the evidence between those specific points held together."
    else:
        outcome = (
            f"When we tried to build a full evidence path from that starting point to the "
            f"symptom, the attempt was REFUSED (reason: {rca.get('primary_rejection_reason')})."
        )

    return f"""You are reviewing a root-cause-analysis case for a failure in a microservice system.

An automated algorithm ({algo.get('algo')}) inspected the evidence and proposed
"{seed}" as the most likely root cause. {outcome}

Here is what the evidence shows.

Candidate connections between services, with the statistical/structural/temporal checks
each one passed or failed (computed from real metric z-scores, call-graph structure, and
onset timestamps during the incident window). {temporal_note(payload['candidate_graph'])}
{edges_prose(payload['candidate_graph'])}

Other evidence signals observed, with how far each deviated from its normal range
(this is the number that actually distinguishes otherwise-similar candidates):
{evidence_prose(payload['evidence_registry'])}

Four other independent detection algorithms also examined this same case; their
own top picks were:
{baselines_prose(algo)}

Given ONLY this evidence, decide:
1. Do you CONFIRM "{seed}" as the root cause, PROPOSE a different service instead,
   or is the evidence INSUFFICIENT to decide either way? Only use INSUFFICIENT if
   no candidate's evidence is meaningfully stronger than the others - a difference
   in deviation magnitude or in how many independent algorithms/checks agree IS a
   meaningful basis for CONFIRM or PROPOSE, even without temporal ordering.
2. Confidence: low, medium, or high.
3. Reasoning in 15 words or fewer.

Respond with ONLY a JSON object, no other text:
{{"decision": "confirm"|"propose"|"insufficient", "service": "<service name or null>",
 "confidence": "low"|"medium"|"high", "reason": "<15 words or fewer>"}}"""



def parse_answer(text: str) -> dict | None:
    match = re.search(r"\{.*\}", text, re.S)
    return json.loads(match.group(0)) if match else None


def call_claude(model: str, prompt: str) -> dict:
    try:
        proc = subprocess.run(
            [CLAUDE, "-p", "--model", model, "--strict-mcp-config", "--output-format", "json"],
            input=prompt, capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {"error": "claude CLI timed out after 120s", "input_tokens": 0, "output_tokens": 0}
    except OSError as exc:
        return {"error": f"claude CLI failed to start: {exc}", "input_tokens": 0, "output_tokens": 0}
    try:
        events = json.loads(proc.stdout)
        final = next(e for e in reversed(events) if e.get("type") == "result")
        usage = final["usage"]
        in_tok = usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
        out_tok = usage.get("output_tokens", 0)
        answer = parse_answer(final["result"]) or {"error": f"unparseable: {final['result'][:200]}"}
    except Exception:
        return {"error": (proc.stdout or proc.stderr)[:200], "input_tokens": 0, "output_tokens": 0}
    answer["input_tokens"] = in_tok
    answer["output_tokens"] = out_tok
    return answer


def call_codex(model: str, prompt: str) -> dict:
    try:
        proc = subprocess.run(
            [CODEX, "exec", "-m", model, "--skip-git-repo-check", "--json", "-"],
            input=prompt, capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {"error": "codex CLI timed out after 120s", "input_tokens": 0, "output_tokens": 0}
    except OSError as exc:
        return {"error": f"codex CLI failed to start: {exc}", "input_tokens": 0, "output_tokens": 0}
    usage = {}
    last_msg = None
    for line in proc.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "item.completed" and ev.get("item", {}).get("type") == "agent_message":
            last_msg = ev["item"].get("text")
        if ev.get("type") == "turn.completed":
            usage = ev.get("usage") or {}
    if not last_msg:
        return {"error": (proc.stdout or proc.stderr)[-200:], "input_tokens": 0, "output_tokens": 0}
    answer = parse_answer(last_msg)
    if answer is None:
        return {"error": f"unparseable: {last_msg[:200]}", "input_tokens": 0, "output_tokens": 0}
    answer["input_tokens"] = usage.get("input_tokens", 0) + usage.get("cached_input_tokens", 0)
    answer["output_tokens"] = usage.get("output_tokens", 0)
    return answer


# Gemini's shared capacity returns 503 ("model is currently experiencing high demand")
# and occasionally 429 (rate limit) under normal load - Google's own guidance is to
# retry with backoff, not treat it as a permanent failure. Every other error status
# still fails immediately, same as call_claude/call_codex.
GEMINI_RETRYABLE_STATUS = {429, 503}
GEMINI_MAX_RETRIES = 4
GEMINI_RETRY_BACKOFF_SECONDS = 2.0


def call_gemini(model: str, prompt: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not set", "input_tokens": 0, "output_tokens": 0}
    url = GEMINI_URL.format(model=model)
    resp = None
    for attempt in range(GEMINI_MAX_RETRIES + 1):
        try:
            resp = requests.post(
                url, params={"key": api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=120,
            )
        except requests.Timeout:
            return {"error": "gemini API timed out after 120s", "input_tokens": 0, "output_tokens": 0}
        except requests.RequestException as exc:
            return {"error": f"gemini API request failed: {exc}", "input_tokens": 0, "output_tokens": 0}
        if resp.status_code not in GEMINI_RETRYABLE_STATUS or attempt == GEMINI_MAX_RETRIES:
            break
        time.sleep(GEMINI_RETRY_BACKOFF_SECONDS * (2 ** attempt))
    if resp.status_code in GEMINI_RETRYABLE_STATUS:
        return {"error": f"gemini API still {resp.status_code} after {GEMINI_MAX_RETRIES} retries: "
                          f"{resp.text[:150]}", "input_tokens": 0, "output_tokens": 0}
    try:
        body = resp.json()
        text = body["candidates"][0]["content"]["parts"][0]["text"]
        usage = body.get("usageMetadata") or {}
        in_tok = usage.get("promptTokenCount", 0)
        out_tok = usage.get("candidatesTokenCount", 0)
        answer = parse_answer(text) or {"error": f"unparseable: {text[:200]}"}
    except Exception:
        return {"error": resp.text[:200], "input_tokens": 0, "output_tokens": 0}
    answer["input_tokens"] = in_tok
    answer["output_tokens"] = out_tok
    return answer


# caller functions must all be defined above this point - the registry is the
# single place a fourth vendor gets added: one entry here, one new call_<vendor>().
#
# published list-price $/1M tokens (in, out) - real cost is $0 for Claude/Codex
# (subscription / ChatGPT Plus quota); Gemini bills against a real metered API
# key, so its list_cost_usd in the output IS real money, not a cosmetic figure.
# gemini-3.7-flash / gemini-3.5-flash-lite are PINNED dated model ids, not the
# "-latest" rolling aliases - Google's own docs describe "-latest" as "hot-
# swapped with every new release" with no way to query which dated model it
# currently points to (confirmed via models.get, 2026-09-01: no baseModelId
# is returned). A pinned id can't silently change mid-run or between reruns
# weeks apart, which matters for a reproducible thesis result; gemini-pro-
# latest/-pro was dropped from this pair on cost grounds (flagship tier, not
# needed for a review/re-rank task). Prices below are from Google's Gemini 3
# pricing table as read 2026-09-01 (Global, Standard tier, <=200K input
# tokens) - re-check before citing if pinning to a newer model later.
MODEL_REGISTRY = {
    "claude-haiku-4-5-20251001": {"caller": call_claude, "price": (1.00, 5.00), "billing": "subscription"},
    "claude-sonnet-5": {"caller": call_claude, "price": (2.00, 10.00), "billing": "subscription"},
    "gpt-5.6-luna": {"caller": call_codex, "price": (0.20, 1.20), "billing": "subscription"},
    "gpt-5.6-terra": {"caller": call_codex, "price": (2.00, 12.00), "billing": "subscription"},
    "gemini-3.7-flash": {"caller": call_gemini, "price": (0.75, 3.75), "billing": "metered_api_key"},
    "gemini-3.5-flash-lite": {"caller": call_gemini, "price": (0.30, 2.50), "billing": "metered_api_key"},
}


def parse_models(raw: str) -> list[str]:
    """Comma-separated model ids -> validated list against MODEL_REGISTRY.
    Guard clause on any unknown id, listing the valid ones, rather than an
    if-chain per model."""
    models = [m.strip() for m in raw.split(",") if m.strip()]
    unknown = [m for m in models if m not in MODEL_REGISTRY]
    if unknown:
        valid = ", ".join(sorted(MODEL_REGISTRY))
        raise ValueError(f"unknown model id(s) {unknown}; valid ids are: {valid}")
    return models


def ask(model: str, case: dict, prompt: str) -> dict:
    caller = MODEL_REGISTRY[model]["caller"]
    started_at = datetime.now(timezone.utc)
    t0 = time.time()
    answer = caller(model, prompt)
    duration_s = round(time.time() - t0, 1)
    in_tok = answer.pop("input_tokens", 0)
    out_tok = answer.pop("output_tokens", 0)
    pin, pout = MODEL_REGISTRY[model]["price"]
    cost = in_tok / 1e6 * pin + out_tok / 1e6 * pout
    return {"case_id": case["case_id"], "bucket": case["_bucket"], "model": model,
            "algo_rank1": case["algo_rank1"], "prompt": prompt, "answer": answer,
            "started_at": started_at.strftime("%Y-%m-%dT%H:%M:%SZ"), "duration_s": duration_s,
            "input_tokens": in_tok, "output_tokens": out_tok, "list_cost_usd": round(cost, 4)}



def ground_truth(case_id: str) -> set[str]:
    payload = json.loads((RAW_ROOT / case_id / "injection.json").read_text())
    return set(payload.get("ground_truth", {}).get("service") or [])


def score(result: dict, truth: set[str]) -> bool | None:
    answer = result["answer"]
    if "error" in answer:
        return None
    decision = answer.get("decision")
    if decision == "propose":
        return answer.get("service") in truth
    if decision == "confirm":
        return result["algo_rank1"] in truth
    return None  # insufficient


# Path maps - AI's proposed path and the real solution, drawn with the same
# dark-box SVG as the main dashboard. No parquet re-read: the AI's proposed
# service is always a node already present in this case's candidate_graph
# (checked empirically), so a plain BFS over the already-computed edges finds
# the path, if any exists in the evidence explored so far.

def bfs_shortest_path(edges: list[dict], start: str, end: str, max_hops: int = 6) -> list[str] | None:
    if start == end:
        return [start]
    adjacency: dict[str, list[str]] = {}
    for e in edges:
        adjacency.setdefault(e["source"], []).append(e["target"])
    seen = {start}
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        if len(path) - 1 >= max_hops:
            continue
        for nxt in adjacency.get(path[-1], []):
            if nxt in seen:
                continue
            extended = path + [nxt]
            if nxt == end:
                return extended
            seen.add(nxt)
            queue.append(extended)
    return None


def real_solution_map(machine: dict) -> tuple[str, str]:
    """The actual injected-component-to-symptom path, already computed and
    sitting in machine_graph.json's top-level judgment - never sent to a model."""
    judgment = machine.get("judgment") or {}
    nodes = judgment.get("selected_path_nodes") or []
    if not nodes:
        reason = judgment.get("primary_rejection_reason") or "no accepted path"
        return "", f"Real solution path unavailable (refused: {reason})."
    edges = (machine.get("candidate_graph") or {}).get("edges", [])
    svg = _path_svg(nodes, edges, aria="real solution path", endpoint_labels=("root cause", "symptom"))
    return svg, f"Real solution: {' -> '.join(nodes)}"


def ai_proposed_nodes(machine: dict, answer: dict) -> list[str] | None:
    """Node list implied by one model's answer - confirm reuses the algorithm's own
    accepted RCA path, propose walks the candidate graph from the proposed service to
    the symptom. None when there is nothing to draw (refused/insufficient/unconnected)."""
    decision = answer.get("decision")
    if decision == "confirm":
        rca_judgment = (machine.get("rca_path") or {}).get("judgment") or {}
        return rca_judgment.get("selected_path_nodes") or None
    if decision == "propose":
        edges = (machine.get("candidate_graph") or {}).get("edges", [])
        symptom = ((machine.get("reality") or {}).get("symptom") or {}).get("component")
        start = answer.get("service")
        if not start or not symptom:
            return None
        return bfs_shortest_path(edges, start, symptom)
    return None


def ai_proposed_map(machine: dict, answer: dict, algo_rank1: str) -> tuple[str, str]:
    edges = (machine.get("candidate_graph") or {}).get("edges", [])
    decision = answer.get("decision")
    nodes = ai_proposed_nodes(machine, answer)

    if decision == "confirm":
        if not nodes:
            return "", f"Confirmed {algo_rank1}, but the algorithm's own path to symptom was refused; nothing to draw."
        return (
            _path_svg(nodes, edges, aria="AI-confirmed path", endpoint_labels=("AI pick", "symptom")),
            f"AI path (confirmed): {' -> '.join(nodes)}",
        )
    if decision == "propose":
        if nodes is None:
            start = answer.get("service") or "?"
            return "", f"No connected path found from {start} to symptom in the evidence explored so far."
        return (
            _path_svg(nodes, edges, aria="AI-proposed path", endpoint_labels=("AI pick", "symptom")),
            f"AI path (proposed): {' -> '.join(nodes)}",
        )
    return "", "Model returned insufficient/no proposal; no path to draw."


# Standardized summary card - one per (case, model) call, same shape everywhere

NEXT_STEP = {
    "confirm": "Proceed with {seed} as root cause; no further action needed.",
    "propose": "Re-run path construction seeded from {service} to check whether a path becomes acceptable.",
    "insufficient": "Escalate for manual review; no candidate's evidence is decisively stronger than the rest.",
}


def _card_title(answer: dict, seed: str) -> str:
    decision = answer.get("decision")
    if decision == "confirm":
        return f"CONFIRM {seed}"
    if decision == "propose":
        return f"PROPOSE {answer.get('service')} (over algorithm's {seed})"
    if decision == "insufficient":
        return "INSUFFICIENT EVIDENCE"
    return "UNPARSEABLE RESPONSE"


def _card_limitations(candidate_graph: dict) -> str | None:
    edges = (candidate_graph or {}).get("edges", [])
    temporal_resolved = any(e.get("checks", {}).get("temporal") != "unknown" for e in edges)
    if not temporal_resolved:
        return "No temporal ordering available for this case; decision rests on statistical/structural signals only."
    return None


def build_summary_card(result: dict, index: int, candidate_graph: dict) -> dict:
    """Structured card fields - rendered as markdown for summary.md and as real
    HTML elements (not literal '**' text) for the case pages, from one source."""
    answer = result["answer"]
    seed = result["algo_rank1"]
    status = "error" if "error" in answer else "ok"
    decision = answer.get("decision", "error")

    card = {
        "heading": f"{result.get('started_at', '?')} — {result['case_id']} — pipeline #{index}",
        "status": status,
        "tokens": result.get("input_tokens", 0) + result.get("output_tokens", 0),
        "duration_s": result.get("duration_s", "?"),
        "model": result["model"],
        "pipeline": f"{result['case_id']}/{result['bucket']}",
    }
    if status == "error":
        card["fields"] = [
            ("Title", "MODEL CALL FAILED"),
            ("Summary", f"{result['model']} did not return a usable answer."),
            ("Evidence", "n/a"),
            ("Suggested next step", "Retry the call; if it keeps failing, treat as insufficient evidence."),
            ("Limitations", answer.get("error", "unknown error")[:200]),
        ]
        return card

    next_step = NEXT_STEP.get(decision, "Retry with a clearer prompt; response did not match the expected decisions.")
    next_step = next_step.format(seed=seed, service=answer.get("service"))
    card["fields"] = [
        ("Title", _card_title(answer, seed)),
        ("Summary", f"{result['model']} chose {decision} "
                    f"(confidence: {answer.get('confidence', 'n/a')}) — {answer.get('reason', 'no reason given')}"),
        ("Evidence", f"Algorithm seed was {seed}; {answer.get('reason', 'no reason given')}"),
        ("Suggested next step", next_step),
    ]
    limitations = _card_limitations(candidate_graph)
    if limitations:
        card["fields"].append(("Limitations", limitations))
    return card


def card_to_markdown(card: dict) -> str:
    lines = [f"## {card['heading']}"]
    lines += [f"**{label}:** {text}" for label, text in card["fields"]]
    lines.append("---")
    lines.append(
        f"Run stats: status={card['status']}, tokens={card['tokens']}, duration={card['duration_s']}s, "
        f"model={card['model']}, pipeline={card['pipeline']}"
    )
    return "\n".join(lines)


def card_to_html(card: dict) -> str:
    rows = "".join(f"<dt>{esc(label)}</dt><dd>{esc(text)}</dd>" for label, text in card["fields"])
    return f"""<div class="run-card">
<div class="tiny muted">{esc(card['heading'])}</div>
<dl>{rows}</dl>
<div class="tiny muted">Run stats: status={esc(card['status'])}, tokens={card['tokens']}, duration={card['duration_s']}s,
model={esc(card['model'])}, pipeline={esc(card['pipeline'])}</div>
</div>"""


# HTML report - one page per case, prompt + every model's answer side by side

# same palette as evidence/emit.py's case pages, so this reads as one dashboard
DASHBOARD_CSS = """
:root { --bg:#faf9f7; --ink:#1a1a1a; --muted:#666; --line:#ddd; }
body{font-family:ui-sans-serif,system-ui,sans-serif;margin:0;background:var(--bg);color:var(--ink)}
main{max-width:1100px;margin:0 auto;padding:1.5rem}
h1{font-size:1.35rem;margin:0 0 .5rem}
h2{font-size:1.05rem;margin:1.5rem 0 .6rem;border-bottom:1px solid var(--line);padding-bottom:.3rem}
.banner{padding:.9rem 1rem;background:#fff;border-left:5px solid #888;margin:1rem 0;box-shadow:0 1px 0 var(--line)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
.card{background:#fff;padding:1rem;border:1px solid var(--line);border-left:5px solid var(--muted)}
.card.hit{border-left-color:#1b9e77} .card.miss{border-left-color:#d95f02} .card.insuff{border-left-color:#999}
.card h3{margin:0 0 .4rem;font-size:.95rem;display:flex;justify-content:space-between}
.badge{font-size:.75rem;font-family:ui-monospace,monospace;border:1px solid var(--line);padding:.1rem .4rem}
table{border-collapse:collapse;width:100%;font-size:.88rem;background:#fff}
th,td{border:1px solid var(--line);padding:.4rem;text-align:left;vertical-align:top}
.muted{color:var(--muted)} a{color:#0b5}
pre{white-space:pre-wrap;background:#fff;border:1px solid var(--line);padding:1rem;font-size:.82rem;line-height:1.4}
.run-card{background:#fbfbfa;border:1px solid var(--line);padding:.7rem .9rem;margin:.4rem 0}
.run-card dl{margin:.3rem 0} .run-card dt{font-weight:600;font-size:.82rem;margin-top:.4rem}
.run-card dd{margin:.1rem 0 0;font-size:.85rem;line-height:1.4}
.verdict-flow{display:flex;align-items:center;gap:.4rem;font-family:ui-monospace,monospace;font-size:.8rem}
.verdict-flow .arrow{color:var(--muted)}
table.breakdown{margin:.75rem 0 1.25rem}
table.breakdown tr.subtotal{font-weight:600;background:#f2f0ec}
table.breakdown tr.spacer td{border:none;padding:.2rem 0}
"""


def esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def match_badge(hit: bool | None, *, prefix: str) -> str:
    text = f"{prefix}: match" if hit is True else f"{prefix}: no match" if hit is False else f"{prefix}: insufficient"
    if hit is True:
        return f'<span class="badge" style="color:#0a7d2c">{esc(text)}</span>'
    if hit is False:
        return f'<span class="badge" style="color:#b3261e">{esc(text)}</span>'
    return f'<span class="badge muted">{esc(text)}</span>'


def _card_class(hit: bool | None) -> str:
    if hit is True:
        return "hit"
    if hit is False:
        return "miss"
    return "insuff"


AI_SECTION_START = "<!-- rca_second_opinion_section:start -->"
AI_SECTION_END = "<!-- rca_second_opinion_section:end -->"
AI_SECTION_CSS_MARKER = "/* rca_second_opinion_css */"

# extra rules not already defined in the dashboard page's own <style> block
# (.card/.grid/.banner/.muted/table are already there - see evidence/emit.py)
AI_SECTION_CSS = f"""{AI_SECTION_CSS_MARKER}
.card.hit{{border-left:5px solid #1b9e77}} .card.miss{{border-left:5px solid #d95f02}} .card.insuff{{border-left:5px solid #999}}
.badge{{font-size:.75rem;font-family:ui-monospace,monospace;border:1px solid var(--line);padding:.1rem .4rem}}
.run-card{{background:#fbfbfa;border:1px solid var(--line);padding:.7rem .9rem;margin:.4rem 0}}
.run-card dl{{margin:.3rem 0}} .run-card dt{{font-weight:600;font-size:.82rem;margin-top:.4rem}}
.run-card dd{{margin:.1rem 0 0;font-size:.85rem;line-height:1.4}}
.verdict-flow{{display:flex;align-items:center;gap:.4rem;font-family:ui-monospace,monospace;font-size:.8rem}}
.verdict-flow .arrow{{color:var(--muted)}}
.ai-tiny{{font-size:.78rem;margin:.3rem 0}} .ai-subhead{{font-size:.85rem;margin:.7rem 0 .3rem;color:var(--muted)}}
"""


def ai_section_fragment(case_id: str, truth: set[str], rows: list[dict], machine: dict, index_start: int) -> str:
    prompt = rows[0]["prompt"]
    candidate_graph = machine.get("candidate_graph") or {}
    real_svg, real_caption = real_solution_map(machine)

    cards = []
    for i, r in enumerate(rows):
        card_html = card_to_html(build_summary_card(r, index_start + i, candidate_graph))
        ai_svg, ai_caption = ai_proposed_map(machine, r["answer"], r["algo_rank1"])
        ai_panel = (
            f'<div class="ai-tiny muted">{esc(ai_caption)}</div>{ai_svg}' if ai_svg
            else f'<div class="ai-tiny muted">{esc(ai_caption)}</div>'
        )
        real_panel = ""
        if r["hit"] is True:
            real_panel = (
                f'<div class="ai-subhead">Real solution (this model matched it)</div>'
                f'<div class="ai-tiny muted">{esc(real_caption)}</div>{real_svg}'
            )
        verdict_flow = (
            f'<div class="verdict-flow">{match_badge(r["before_hit"], prefix="before")}'
            f'<span class="arrow">&rarr;</span>{match_badge(r["hit"], prefix="after")}'
            f'<span class="muted">${r["list_cost_usd"]:.3f}</span></div>'
        )
        cards.append(f"""
        <div class="card {_card_class(r['hit'])}">
          <h3>{esc(r['model'])}</h3>
          {verdict_flow}
          {card_html}
          <div class="ai-subhead">AI path</div>
          {ai_panel}
          {real_panel}
        </div>""")

    return f"""{AI_SECTION_START}
<h2>AI second opinions</h2>
<div class="banner">
real ground truth <code>{esc(sorted(truth))}</code>
&nbsp; algorithm's seed <code>{esc(rows[0]['algo_rank1'])}</code>
<br><em>Standardized cards below follow the run-report template; each is one model's independent pass over the same evidence.</em>
</div>
<div class="grid">{''.join(cards)}</div>
<details><summary>Prompt sent (identical across all models in this run)</summary><pre>{esc(prompt)}</pre></details>
{AI_SECTION_END}"""


def model_stats_table(results: list[dict], models: list[str]) -> list[tuple]:
    """One row per model: before, after, in_tok, out_tok, list_cost - no bucket split."""
    rows = []
    for model in models:
        rs = [r for r in results if r["model"] == model]
        if not rs:
            continue
        before = sum(r["before_hit"] for r in rs)
        after = sum(1 for r in rs if r["hit"] is True)
        rows.append((
            model, before, after, len(rs),
            sum(r["input_tokens"] for r in rs),
            sum(r["output_tokens"] for r in rs),
            sum(r["list_cost_usd"] for r in rs),
        ))
    return rows


NO_RUN_REASON = {
    ("RCA CORRECT", "Path correct / built"): "No AI needed: already correct",
    ("UNAVAILABLE", "Algorithm unavailable"): "No AI run: no algorithm output to review",
}


def model_breakdown_table(all_cases: list[dict], pilot: list[dict], results: list[dict], models: list[str]) -> str:
    """Table 2 for the Investigation console: same row structure as evidence.emit's
    Table 1 (outcome_breakdown_rows), model columns instead of algorithm columns. A
    cell reads 'corrected/sampled' against the pilot's own small draw from that row,
    not the full row population - '-' means the pilot never touched that row at all,
    which is not the same as 0 corrected."""
    total = len(all_cases)
    if not total:
        return "<p class='muted'>no cases</p>"

    pilot_ids = {c["case_id"] for c in pilot}

    def model_cells(subset: list[dict], placeholder: str) -> str:
        ids = [c["case_id"] for c in subset if c["case_id"] in pilot_ids]
        if not ids:
            return f"<td colspan='{len(models)}' class='muted'>{esc(placeholder)}</td>"
        cells = []
        for model in models:
            corrected = sum(
                1 for r in results
                if r["model"] == model and r["case_id"] in ids and r["hit"] is True
            )
            cells.append(f"<td>{_pct(corrected / len(ids))}</td>")
        return "".join(cells)

    header_models = "".join(f"<th>{esc(m)}</th>" for m in models)
    body = []
    for verdict, path_verdict, subset in outcome_breakdown_rows(all_cases):
        if verdict == "SPACER":
            body.append(f"<tr class='spacer'><td colspan='{3 + len(models)}'></td></tr>")
            continue
        placeholder = NO_RUN_REASON.get((verdict, path_verdict), "not sampled by this pilot run")
        if verdict.startswith("SUBTOTAL") or verdict == "TOTAL":
            cells = model_cells(subset, placeholder) if verdict != "TOTAL" else "<td></td>" * len(models)
            body.append(
                f"<tr class='subtotal'><td colspan='2'>{esc(verdict)}</td>"
                f"<td>{_pct(len(subset) / total)}</td>{cells}</tr>"
            )
            continue
        body.append(
            f"<tr><td>{esc(verdict)}</td><td>{esc(path_verdict)}</td>"
            f"<td>{_pct(len(subset) / total)}</td>{model_cells(subset, placeholder)}</tr>"
        )

    coverage_note = (
        f"a small deliberate over-sample of {len(pilot)} of the {total} cases, not the full population"
        if len(pilot) < total
        else f"every one of the {total} cases in this sample"
    )
    return f"""<table class='breakdown'>
<thead><tr><th>RCA Verdict</th><th>Path Verdict</th><th>% of Total</th>{header_models}</tr></thead>
<tbody>{''.join(body)}</tbody>
</table>
<p class="muted">Model columns read "corrected / sampled" against this pilot's own draw from that row:
{coverage_note}. A row with no sample shows "—".</p>"""


def ai_badge(corrected: int, n: int) -> str:
    color = "#0a7d2c" if corrected else "#666"
    return f'<span class="badge" style="color:{color}">AI {corrected}/{n} corrected</span>'


def _majority_ai_strip(machine: dict, rows: list[dict]) -> tuple[str, str]:
    """Third queue row's box-chain: the node list most models proposed, plus a plain-
    text note on any minority or tied proposals. Never picks a winner arbitrarily -
    a tie names every tied path instead."""
    edges = (machine.get("candidate_graph") or {}).get("edges", [])
    tally: dict[tuple[str, ...], int] = {}
    for r in rows:
        nodes = ai_proposed_nodes(machine, r["answer"])
        if nodes:
            tally[tuple(nodes)] = tally.get(tuple(nodes), 0) + 1

    if not tally:
        return "<span class='strip refuse'>refuse — no model proposed a connected path</span>", ""

    best = max(tally.values())
    winners = [nodes for nodes, count in tally.items() if count == best]
    majority = list(winners[0])
    strip = _path_strip_html(majority, edges)

    def short_path(nodes: tuple[str, ...]) -> str:
        return " - ".join(_short(n) for n in nodes)

    if len(winners) > 1:
        tied = "; ".join(short_path(nodes) for nodes in winners[1:])
        note = f"<div class='ai-tiny muted'>tied {best}x each, also: {esc(tied)}</div>"
        return strip, note

    others = [(nodes, count) for nodes, count in tally.items() if list(nodes) != majority]
    if not others:
        return strip, ""
    others_text = "; ".join(
        f"{count}x proposed: {short_path(nodes)}"
        for nodes, count in sorted(others, key=lambda kv: -kv[1])
    )
    return strip, f"<div class='ai-tiny muted'>{esc(others_text)}</div>"


AI_OVERVIEW_START = "<!-- ai_overview:start -->"
AI_OVERVIEW_END = "<!-- ai_overview:end -->"
AI_OVERVIEW_CSS_MARKER = "/* ai_overview_css */"
AI_OVERVIEW_CSS = f"""{AI_OVERVIEW_CSS_MARKER}
.badge{{font-size:.75rem;font-family:ui-monospace,monospace;border:1px solid var(--line);padding:.1rem .4rem;margin-left:.4rem}}
.ai-tiny{{font-size:.78rem;margin:.2rem 0 0}}
"""


def embed_dashboard_overview(
    index_path: Path,
    all_cases: list[dict],
    pilot: list[dict],
    results: list[dict],
    machine_cache: dict[str, dict],
    models: list[str],
) -> None:
    """Idempotent overlay on the Investigation console's own index.html (built by
    evidence.emit.index_html): Table 2 right after Table 1, plus a third 'AI' row
    and a corrected-count badge on every case card the pilot actually touched.
    Reruns replace their own markers in place rather than duplicating content."""
    if not index_path.exists():
        return
    html_text = index_path.read_text()

    if AI_OVERVIEW_CSS_MARKER not in html_text and "</style>" in html_text:
        html_text = html_text.replace("</style>", AI_OVERVIEW_CSS + "</style>", 1)

    stats_rows = "".join(
        f"<tr><td>{esc(m)}</td><td>{_pct(b / n)}</td><td>{_pct(a / n)}</td>"
        f"<td>{it:,}</td><td>{ot:,}</td><td>${c:.3f}</td></tr>"
        for m, b, a, n, it, ot, c in model_stats_table(results, models)
    )
    stats_table = f"""<h3>Model results: evaluating models to correctly identify the root cause</h3>
<p class="muted">This table shows <strong>before</strong>: how many cases have the wrong root cause
(not the real injected one) using only the algorithm's own guess. <strong>After</strong>: once each
LLM reviews the same evidence, the result: how many now land on the correct root cause. Then the
number of input tokens used, output tokens used, and price in dollars.</p>
<table class='breakdown'><thead><tr><th>model</th><th>before</th><th>after</th>
<th>in_tok</th><th>out_tok</th><th>list cost</th></tr></thead>
<tbody>{stats_rows}</tbody></table>"""
    breakdown_heading = (
        "<h3>Cases where the RCA predicted wrong: how much AI corrected it</h3>"
        '<p class="muted">For the cases where the algorithm\'s named root cause (RCA) was wrong, how '
        "often each model, reviewing independently, named the correct RCA instead.</p>"
    )
    overview_block = (
        f"{AI_OVERVIEW_START}\n{stats_table}\n{breakdown_heading}\n"
        f"{model_breakdown_table(all_cases, pilot, results, models)}\n{AI_OVERVIEW_END}"
    )
    if AI_OVERVIEW_START in html_text and AI_OVERVIEW_END in html_text:
        before, _, rest = html_text.partition(AI_OVERVIEW_START)
        _, _, after = rest.partition(AI_OVERVIEW_END)
        html_text = before + overview_block + after
    elif "<table class='breakdown'>" in html_text:
        marker = "<table class='breakdown'>"
        close_idx = html_text.index("</table>", html_text.index(marker)) + len("</table>")
        html_text = html_text[:close_idx] + "\n" + overview_block + html_text[close_idx:]
    else:
        return

    by_case: dict[str, list[dict]] = {}
    for r in results:
        by_case.setdefault(r["case_id"], []).append(r)

    for case_id, rows in by_case.items():
        machine = machine_cache.get(case_id)
        if machine is None:
            continue
        corrected = sum(1 for r in rows if r["hit"] is True)
        strip, minority_note = _majority_ai_strip(machine, rows)
        block = (
            f"<!-- ai_row:start:{case_id} -->"
            f"{ai_badge(corrected, len(rows))}"
            f"<div class='qseed'><span class='lab'>AI</span>"
            f"<span class='ver'>{corrected}/{len(rows)} correct</span>{strip}</div>"
            f"{minority_note}"
            f"<!-- ai_row:end:{case_id} -->"
        )
        start_marker = f"<!-- ai_row:start:{case_id} -->"
        end_marker = f"<!-- ai_row:end:{case_id} -->"
        if start_marker in html_text and end_marker in html_text:
            before, _, rest = html_text.partition(start_marker)
            _, _, after = rest.partition(end_marker)
            html_text = before + block + after
            continue
        href_marker = f"href='{case_id}/graph.html'"
        href_idx = html_text.find(href_marker)
        if href_idx == -1:
            continue
        article_end = html_text.index("</article>", href_idx)
        html_text = html_text[:article_end] + block + html_text[article_end:]

    index_path.write_text(html_text)


def embed_ai_section(dashboard_case_html: Path, fragment: str) -> None:
    """Insert the AI-second-opinions section directly into the dashboard's own
    case page - no redirect to a separate file. Idempotent and re-runnable: if
    the section is already there (from a previous pilot run), its content is
    replaced in place rather than duplicated. Only touches a page that already
    exists; a full dashboard regenerate will wipe this and it must be re-embedded."""
    if not dashboard_case_html.exists():
        return
    html = dashboard_case_html.read_text()

    if AI_SECTION_CSS_MARKER not in html and "</style>" in html:
        html = html.replace("</style>", AI_SECTION_CSS + "</style>", 1)

    if AI_SECTION_START in html and AI_SECTION_END in html:
        before = html.split(AI_SECTION_START)[0]
        after = html.split(AI_SECTION_END)[1]
        html = before + fragment + after
    elif "</main>" in html:
        html = html.replace("</main>", fragment + "</main>", 1)
    else:
        return
    dashboard_case_html.write_text(html)


def write_html_report(
    results: list[dict], truth_cache: dict, machine_cache: dict, out_dir: Path,
    models: list[str], sample_name: str, policy: str, pilot: list[dict], all_cases: list[dict],
) -> None:
    by_case: dict[str, list[dict]] = {}
    for r in results:
        by_case.setdefault(r["case_id"], []).append(r)

    dashboard_dir = DEFAULT_SAMPLE_DIR / policy
    index_rows = []
    summary_md_parts = []
    idx = 1
    for case_id, rows in by_case.items():
        truth = truth_cache[case_id]
        machine = machine_cache[case_id]
        dashboard_page = dashboard_dir / case_id / "graph.html"
        fragment = ai_section_fragment(case_id, truth, rows, machine, idx)
        embed_ai_section(dashboard_page, fragment)
        for i, r in enumerate(rows):
            summary_md_parts.append(card_to_markdown(build_summary_card(r, idx + i, machine.get("candidate_graph") or {})))
        idx += len(rows)
        hits = sum(1 for r in rows if r["hit"] is True)
        dashboard_href = f"../../evidence_path_poc/{sample_name}/{policy}/{case_id}/graph.html"
        index_rows.append(
            f'<tr><td><a href="{esc(dashboard_href)}">{esc(case_id)}</a></td><td>{hits}/{len(rows)}</td></tr>'
        )

    (out_dir / "summary.md").write_text("\n\n".join(summary_md_parts) + "\n")

    stats_rows = "".join(
        f"<tr><td>{esc(m)}</td><td>{_pct(b / n)}</td><td>{_pct(a / n)}</td>"
        f"<td>{it:,}</td><td>{ot:,}</td><td>${c:.3f}</td></tr>"
        for m, b, a, n, it, ot, c in model_stats_table(results, models)
    )

    overview = model_breakdown_table(all_cases, pilot, results, models)

    index = f"""<!doctype html><html><head><meta charset="utf-8"><title>RCA second-opinion pilot</title>
<style>{DASHBOARD_CSS}</style>
</head><body><main>
<h1>RCA second-opinion pilot</h1>
{overview}
<h2>Model results</h2>
<table><tr><th>model</th><th>before</th><th>after</th><th>in_tok</th><th>out_tok</th><th>list cost</th></tr>
{stats_rows}
</table>
<h2>Cases</h2>
<p class="muted">Each row opens the case's own dashboard page, which now has an "AI second opinions" section embedded
directly in it. Plain-text cards: <a href="summary.md">summary.md</a>.</p>
<table><tr><th>case</th><th>hits</th></tr>
{''.join(index_rows)}
</table>
</main></body></html>"""
    (out_dir / "index.html").write_text(index)



def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument(
        "--n-per-bucket", default="6",
        help="cases to sample per bucket, or \"all\" to take every eligible case with no sampling",
    )
    ap.add_argument(
        "--sample", default="sample_all",
        help="evidence_path_poc run to pull cases from (analysis/output_charts/evidence_path_poc/<sample>/<policy>) "
             "- point this at any other dataset's run for the same pilot to reproduce there",
    )
    ap.add_argument("--sample-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--policy", default="relaxed", choices=("strict", "relaxed"))
    ap.add_argument(
        "--buckets", default=",".join(ALL_BUCKETS),
        help="comma-separated outcome groups to draw from - default is all three; "
             "use wrong_accepted,wrong_refused for \"RCA was wrong\" only, dropping correct_refused",
    )
    ap.add_argument(
        "--models", default=",".join(MODEL_REGISTRY),
        help="comma-separated model ids to run, any subset of MODEL_REGISTRY "
             f"(default all: {', '.join(MODEL_REGISTRY)})",
    )
    ap.add_argument(
        "--max-errors", type=int, default=8,
        help="cancel remaining not-yet-started jobs once this many calls error out in a row "
             "(a subscription hitting its rate limit shows up as repeated errors, not a crash - "
             "this is the guard against that turning into a long silent failure)",
    )
    ap.add_argument("--limit", type=int, default=None, help="only process the first N (case,model) pairs (debug)")
    ap.add_argument("--dry-run", action="store_true", help="build payloads + leak-scan only, no model calls")
    ap.add_argument(
        "--fresh", action="store_true",
        help="ignore any existing pilot_results.json and rerun every (case,model) pair from scratch",
    )
    args = ap.parse_args()

    try:
        models = parse_models(args.models)
    except ValueError as exc:
        ap.error(str(exc))
    buckets = tuple(b.strip() for b in args.buckets.split(",") if b.strip())
    n_per_bucket = None if args.n_per_bucket.strip().lower() == "all" else int(args.n_per_bucket)

    if args.sample_dir:
        sample_dir = args.sample_dir
        out_dir = args.out_dir or (REPO_ROOT / "results/_validation/llm")
    else:
        sample_dir = DEFAULT_SAMPLE_DIR / args.policy
        out_dir = args.out_dir or (DEFAULT_OUT_DIR / args.policy)
    all_cases = json.loads((sample_dir / "summary.json").read_text())["cases"]
    pilot = select_pilot(args.seed, n_per_bucket, sample_dir, buckets)
    print(f"pilot: {len(pilot)} cases from {sample_dir}", flush=True)
    print(f"writing results to {out_dir}", flush=True)
    print("prompt is rebuilt fresh per case from machine_graph.json (see render_prompt()); nothing is hardcoded per-case", flush=True)

    checkpoint_path = out_dir / "pilot_results.json"
    results: list[dict] = []
    if checkpoint_path.exists() and not args.fresh:
        results = json.loads(checkpoint_path.read_text())
        print(f"resume: loaded {len(results)} existing results from {checkpoint_path}", flush=True)
    # only a clean (case_id, model) hit counts as done - an error row gets retried,
    # since "the call failed" isn't a result worth keeping frozen across a resume.
    done_pairs = {(r["case_id"], r["model"]) for r in results if "error" not in r["answer"]}

    jobs = []
    # every case_id in results needs its machine_graph.json for write_html_report()
    # below, including ones fully resumed from a larger prior run whose pilot
    # selection (--n-per-bucket) doesn't cover this run's smaller one
    machine_cache: dict[str, dict] = {
        cid: json.loads((sample_dir / cid / "machine_graph.json").read_text())
        for cid in {r["case_id"] for r in results}
        if (sample_dir / cid / "machine_graph.json").exists()
    }
    skipped_done = 0
    for case in pilot:
        case_dir = sample_dir / case["case_id"]
        payload = build_payload(case_dir)
        leaks = find_leaks(payload)
        if leaks:
            print(f"  REFUSED (leak {leaks}): {case['case_id']}", flush=True)
            continue
        machine_cache[case["case_id"]] = json.loads((case_dir / "machine_graph.json").read_text())
        prompt = render_prompt(case, payload)
        for model in models:
            if (case["case_id"], model) in done_pairs:
                skipped_done += 1
                continue
            jobs.append((model, case, prompt))

    print(f"jobs built: {len(jobs)} (case x model pairs), {skipped_done} already done, 0 leaks blocked", flush=True)
    if args.limit:
        jobs = jobs[: args.limit]

    if args.dry_run:
        print("dry-run: no model calls made")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_every = 10

    def write_checkpoint() -> None:
        # write-then-rename so a crash mid-write never corrupts the last good checkpoint
        tmp = checkpoint_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(results, indent=2))
        tmp.replace(checkpoint_path)

    t0 = time.time()
    error_streak = 0
    cancelled = 0
    total_jobs = len(jobs)
    done_at_start = len(results)
    # every case_id in results needs its ground truth for write_html_report() below,
    # including ones fully resumed from checkpoint with zero new jobs this run
    truth_cache: dict[str, set[str]] = {r["case_id"]: ground_truth(r["case_id"]) for r in results}
    try:
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = {pool.submit(ask, model, case, prompt) for model, case, prompt in jobs}
            for fut in as_completed(futures):
                if fut.cancelled():
                    cancelled += 1
                    continue
                try:
                    r = fut.result()
                except Exception as exc:  # a model call must never take the whole run down
                    r = {
                        "case_id": "unknown", "bucket": "unknown", "model": "unknown",
                        "algo_rank1": None, "prompt": "", "answer": {"error": f"job crashed: {exc}"},
                        "started_at": "", "duration_s": 0.0, "input_tokens": 0, "output_tokens": 0,
                        "list_cost_usd": 0.0,
                    }
                cid = r["case_id"]
                if cid not in truth_cache:
                    truth_cache[cid] = ground_truth(cid) if cid != "unknown" else set()
                r["hit"] = score(r, truth_cache[cid])
                r["before_hit"] = r["algo_rank1"] in truth_cache[cid] if r["algo_rank1"] else False
                # a retried (case_id, model) pair must replace its stale entry, not sit
                # beside it - otherwise every retry after a resume double-counts that pair
                results[:] = [x for x in results if (x["case_id"], x["model"]) != (cid, r["model"])]
                results.append(r)
                if len(results) % checkpoint_every == 0:
                    write_checkpoint()

                error_streak = error_streak + 1 if "error" in r["answer"] else 0
                done_this_run = len(results) - done_at_start
                elapsed = time.time() - t0
                rate = done_this_run / elapsed if elapsed > 0 else 0
                eta_s = (total_jobs - done_this_run - cancelled) / rate if rate > 0 else 0
                if "error" in r["answer"]:
                    status = f"ERROR {r['answer']['error'][:50]}"
                else:
                    verdict = "HIT" if r["hit"] is True else "miss" if r["hit"] is False else "n/a"
                    status = f"{r['answer'].get('decision', '?'):<12s} verdict={verdict}"
                print(
                    f"[{time.strftime('%H:%M:%S')}] {done_this_run:>5d}/{total_jobs} "
                    f"{r['model']:<26s} {cid[:42]:<42s} {status:<32s} "
                    f"{r['duration_s']:>5.1f}s ${r['list_cost_usd']:.4f} "
                    f"(elapsed {elapsed:>5.0f}s eta {eta_s:>5.0f}s)",
                    flush=True,
                )

                if error_streak < args.max_errors:
                    continue
                pending = [f for f in futures if not f.done()]
                for f in pending:
                    f.cancel()
                if pending:
                    print(
                        f"  {error_streak} calls in a row errored (looks like a rate limit or "
                        f"exhausted subscription quota): cancelling {len(pending)} not-yet-started jobs",
                        flush=True,
                    )
    finally:
        if results:
            write_checkpoint()
            print(f"checkpoint: {len(results)} results saved to {checkpoint_path}", flush=True)
    print(f"done in {time.time()-t0:.0f}s ({len(results)} completed, {cancelled} cancelled)", flush=True)
    write_html_report(results, truth_cache, machine_cache, out_dir, models, args.sample, args.policy, pilot, all_cases)

    # the shared investigation console (unlike this run's own out_dir report) must
    # always show every model that has ever produced results here, not just the
    # ones selected via --models on this particular invocation - otherwise running
    # a subset of models overwrites the overview and makes the other models' real,
    # already-paid-for results disappear from view (the data itself is untouched).
    dashboard_index = sample_dir / "index.html"
    models_in_results = {r["model"] for r in results}
    overview_models = [m for m in MODEL_REGISTRY if m in models_in_results]
    embed_dashboard_overview(dashboard_index, all_cases, pilot, results, machine_cache, overview_models)

    print(f"\n{'model':28s} {'before':>8s} {'after':>8s} {'in_tok':>10s} {'out_tok':>9s} {'list_cost$':>11s}")
    for model, before, after, n, in_tok, out_tok, cost in model_stats_table(results, models):
        print(f"{model:28s} {before:>3d}/{n:<4d} {after:>3d}/{n:<4d} {in_tok:>10,d} {out_tok:>9,d} {cost:>10.3f}$")
    total_cost = sum(r["list_cost_usd"] for r in results)
    metered_models = [m for m in models if MODEL_REGISTRY[m]["billing"] == "metered_api_key"]
    cost_note = (
        "list-price equivalent only, real cost is $0 (subscription/Plus quota)"
        if not metered_models
        else f"real cost is $0 only for the subscription-billed models above; "
             f"{', '.join(metered_models)} bill a real metered API key at the published "
             f"per-token rate in MODEL_REGISTRY - re-verify that rate if the rolling "
             f"'-latest' alias has since repointed to a different model"
    )
    print(f"{'TOTAL':28s} {'':>8s} {'':>8s} {'':>10s} {'':>9s} {total_cost:>10.3f}$  ({cost_note})")

    errors = [r for r in results if "error" in r["answer"]]
    if errors:
        print(f"\n{len(errors)} errors:")
        for r in errors[:10]:
            print(f"  {r['model']:20s} {r['case_id']:46s} {r['answer']['error'][:80]}")

    print(f"\nwrote {out_dir / 'pilot_results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
