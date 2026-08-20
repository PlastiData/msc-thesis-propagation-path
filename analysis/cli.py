#!/usr/bin/env python3
"""CLI for failure propagation paths with evidence.

Returns either a candidate path with Observed/Supported/Inferred edges and
re-executable evidence references, or insufficient_evidence with a primary reason.

  .venv/bin/python analysis/cli.py --sample analysis/samples/sample10.txt --policy strict
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = ANALYSIS_DIR.parent
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

from pipeline.algo_context import AUTO_ALGO, DEFAULT_ALGO, load_algo_context, load_dataset_perf
from pipeline.config import load_rules, select_policy
from pipeline.emit import (
    SCORECARD_HEADER,
    SCORECARD_LEGEND,
    aggregate,
    attach_scorecards,
    build_machine_graph,
    empty_rca_path,
    index_html,
    load_sibling_policy,
    refuse_short,
    reject_machine_graph,
    scorecard_line,
    summary_md,
    write_case_outputs,
)
from pipeline.evidence import annotate_paths
from pipeline.graph import build_candidate_graph, paths_between
from pipeline.judgment import case_metrics, judge
from pipeline.reality import build_reality, enrich_timeline_path_errors

DEFAULT_DATA_ROOT = REPO_ROOT / "data/rcabench-platform-v2/data/rcabench"
OUT_ROOT = REPO_ROOT / "results" / "evidence_path_poc"


def _git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "unknown"


def _sample_label(sample_path: Path) -> str:
    return sample_path.stem


def _read_sample(path: Path) -> list[str] | str:
    if not path.exists():
        return f"sample file missing: {path}"
    cases = [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not cases:
        return f"sample file empty: {path}"
    return cases


def _judgment_public(judgment: dict) -> dict:
    return {
        "status": judgment["status"],
        "selected_path_edge_ids": judgment.get("selected_path_edge_ids") or [],
        "selected_path_nodes": judgment.get("selected_path_nodes") or [],
        "primary_rejection_reason": judgment.get("primary_rejection_reason"),
        "rejection_reasons": judgment.get("rejection_reasons") or [],
        "limitations": judgment.get("limitations") or [],
        "policy": judgment.get("policy"),
    }


def _annotated_subset(annotated: dict, path_lists: list[list[str]]) -> dict:
    keys = {tuple(path) for path in path_lists}
    return {
        "edges": annotated["edges"],
        "annotated_paths": [
            path
            for path in annotated["annotated_paths"]
            if tuple(path["nodes"]) in keys
        ],
        "evidence_registry": annotated["evidence_registry"],
    }


def _union_paths(*path_groups: list[list[str]]) -> list[list[str]]:
    seen: set[tuple[str, ...]] = set()
    out: list[list[str]] = []
    for group in path_groups:
        for path in group:
            key = tuple(path)
            if key in seen:
                continue
            seen.add(key)
            out.append(path)
    return out


def _refuse_reason_bucket(reality: str, rules: dict) -> str:
    allowed = set(rules.get("rejection_reasons") or [])
    if reality in allowed:
        return reality
    if reality in {
        "unsupported_case_schema",
        "injected_component_unavailable",
        "symptom_unavailable",
    }:
        return reality
    return "other"


def _format_refuse_counts(reasons: dict[str, int]) -> str:
    if not reasons:
        return ""
    parts = [f"{refuse_short(r)} {n}" for r, n in sorted(reasons.items(), key=lambda kv: (-kv[1], kv[0]))]
    return "(" + ", ".join(parts) + ")"


def _format_evid_counts(counts: dict[str, int]) -> str:
    parts = [f"{k}={counts[k]}" for k in ("obs", "sup", "inf") if counts.get(k)]
    return " ".join(parts) if parts else "—"


def _rel(path: Path) -> Path | str:
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def _print_banner(
    *,
    sample: str,
    n: int,
    policy: str,
    algo: str,
    ac_at_1: float | None,
    out_dir: Path,
    algo_arg: str,
) -> None:
    ac_txt = f"{100 * ac_at_1:.1f}%" if isinstance(ac_at_1, (int, float)) else "—"
    source = "override" if algo_arg not in (None, "", AUTO_ALGO) else "from dataset.perf"
    print("propagation", flush=True)
    print(f"  sample={sample}  n={n}  policy={policy}", flush=True)
    print("  seeds=inject->symptom + best_algo->symptom", flush=True)
    print(f"  algo={algo}  AC@1={ac_txt}  ({source})", flush=True)
    print(f"  out={_rel(out_dir)}", flush=True)
    print(SCORECARD_LEGEND, flush=True)
    print(SCORECARD_HEADER, flush=True)


def _print_done(summary: dict, out_dir: Path) -> None:
    elapsed = summary.get("elapsed_s") or 0
    n = summary["evaluated_cases"]
    fault = summary.get("fault_counts") or {}
    algo = summary.get("algo_counts") or {}
    fault_refuse = _format_refuse_counts(fault.get("refuse_reasons") or {})
    algo_refuse = _format_refuse_counts(algo.get("refuse_reasons") or {})
    print(f"-- done {elapsed:.0f}s --", flush=True)
    print(
        f"inject  path {fault.get('constructed', 0)}/{n}   "
        f"refuse {fault.get('refused', 0)}  {fault_refuse}".rstrip(),
        flush=True,
    )
    print(
        f"rca     path {algo.get('constructed', 0)}/{n}   "
        f"refuse {algo.get('refused', 0)}  {algo_refuse}".rstrip(),
        flush=True,
    )
    print(
        "evid on kept:  inject "
        f"{_format_evid_counts(fault.get('evid_counts') or {})}  |  rca "
        f"{_format_evid_counts(algo.get('evid_counts') or {})}",
        flush=True,
    )
    strat = summary.get("injection_stratification") or {}
    by_layer = (strat.get("by_target_layer") or {}).get("inject") or {}
    if by_layer:
        parts = []
        for layer in sorted(by_layer):
            row = by_layer[layer]
            parts.append(f"{layer} {row['accept']}/{row['n']}")
        print(
            "inject by target_layer (accept/n): " + "  ".join(parts),
            flush=True,
        )
    print(f"out: {_rel(out_dir)}/", flush=True)


def _banner_algo(algo: str, dataset_perf: list[dict]) -> tuple[str, float | None]:
    if algo not in (None, "", AUTO_ALGO) and dataset_perf:
        for row in dataset_perf:
            if row.get("algorithm") == algo:
                return algo, row.get("AC@1")
        return algo, None
    if not dataset_perf:
        return algo or AUTO_ALGO, None
    top = dataset_perf[0]
    return str(top.get("algorithm") or AUTO_ALGO), top.get("AC@1")


def process_case(
    case_id: str,
    *,
    data_root: Path,
    rules: dict,
    policy: dict,
    policy_name: str,
    run_meta: dict,
    algo: str = DEFAULT_ALGO,
    dataset_perf: list[dict] | None = None,
) -> dict:
    case_dir = data_root / case_id
    run = {**run_meta, "case_id": case_id}

    reality = build_reality(case_dir, rules)
    labels: list[str] = []
    if isinstance(reality, dict):
        component = (reality.get("injection") or {}).get("component")
        if component:
            labels = [str(component)]
    algo_ctx = load_algo_context(
        case_id, algo=algo, injection_labels=labels, dataset_perf=dataset_perf
    )

    if isinstance(reality, str):
        return reject_machine_graph(
            case_id,
            run,
            _refuse_reason_bucket(reality, rules),
            detail=str(reality),
            algo_context=algo_ctx,
        )

    try:
        graph = build_candidate_graph(reality, rules)
        inj_paths = list(graph["candidate_paths"])
        end = graph["end"]
        rca_seed = algo_ctx.get("rank1") if algo_ctx.get("available") else None

        if not rca_seed:
            rca_block = empty_rca_path(
                algo=algo_ctx.get("algo"),
                algo_ac_at_1=algo_ctx.get("algo_ac_at_1"),
                seed=None,
                end=end,
                reason="algo_output_missing",
                policy=policy_name,
            )
            rca_paths: list[list[str]] = []
        else:
            rca_paths = paths_between(graph["horizontal"], rca_seed, end, rules)
            rca_block = None

        graph["candidate_paths"] = _union_paths(inj_paths, rca_paths)
        annotated = annotate_paths(case_dir, reality, graph, rules)
        edges_by_id = {e["edge_id"]: e for e in annotated["edges"]}

        inj_judgment = judge(_annotated_subset(annotated, inj_paths), policy, policy_name)
        metrics = case_metrics(inj_judgment, edges_by_id)

        if rca_block is None:
            rca_judgment = judge(
                _annotated_subset(annotated, rca_paths), policy, policy_name
            )
            rca_block = {
                "algo": algo_ctx.get("algo"),
                "algo_ac_at_1": algo_ctx.get("algo_ac_at_1"),
                "seed": rca_seed,
                "end": end,
                "judgment": _judgment_public(rca_judgment),
                "case_metrics": case_metrics(rca_judgment, edges_by_id),
            }

        path_nodes = inj_judgment.get("selected_path_nodes") or []
        if not path_nodes:
            path_nodes = (rca_block.get("judgment") or {}).get("selected_path_nodes") or []
        frames = reality.get("_frames") or {}
        reality["timeline"] = enrich_timeline_path_errors(
            reality.get("timeline") or [],
            frames.get("abnormal"),
            path_nodes,
        )

        return build_machine_graph(
            case_id,
            run,
            reality,
            annotated,
            inj_judgment,
            metrics,
            algo_context=algo_ctx,
            rca_path=rca_block,
        )
    except Exception as exc:  # noqa: BLE001 — case must not abort the batch
        return reject_machine_graph(
            case_id,
            run,
            "evidence_query_failed",
            detail=f"{type(exc).__name__}: {exc}",
            algo_context=algo_ctx,
            reality=reality if isinstance(reality, dict) else None,
        )


def _load_existing_machine(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or "scorecard" not in data:
        return None
    return data


def run(
    *,
    sample_path: Path,
    policy_name: str,
    data_root: Path,
    rules_path: Path | None = None,
    algo: str = DEFAULT_ALGO,
    resume: bool = False,
) -> dict | str:
    rules = load_rules(rules_path)
    if "error" in rules:
        return rules["error"]
    policy = select_policy(rules, policy_name)
    if isinstance(policy, str):
        return policy

    cases = _read_sample(sample_path)
    if isinstance(cases, str):
        return cases

    sample = _sample_label(sample_path)
    out_dir = OUT_ROOT / sample / policy_name
    if out_dir.exists() and not resume:
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dataset_perf = load_dataset_perf()
    banner_algo, banner_ac = _banner_algo(algo, dataset_perf)

    run_meta = {
        "code_version": _git_commit(),
        "config_hash": rules["_config_hash"],
        "sample_path": str(sample_path),
        "sample_seed": None,
        "policy": policy_name,
        "data_root": str(data_root),
        "algo": algo,
        "banner_algo": banner_algo,
        "banner_ac_at_1": banner_ac,
        "resume": resume,
    }

    already = 0
    if resume:
        already = sum(
            1 for c in cases if (out_dir / c / "machine_graph.json").is_file()
        )
    _print_banner(
        sample=sample,
        n=len(cases),
        policy=policy_name,
        algo=banner_algo,
        ac_at_1=banner_ac,
        out_dir=out_dir,
        algo_arg=algo,
    )
    if resume:
        print(
            f"resume: {already} cached, {len(cases) - already} to run",
            flush=True,
        )

    machines = []
    t0 = time.time()
    for case_id in cases:
        existing = _load_existing_machine(out_dir / case_id / "machine_graph.json")
        if resume and existing is not None:
            machines.append(existing)
            print(f"{case_id:40s} skip  (resume)", flush=True)
            continue

        t_case = time.time()
        machine = process_case(
            case_id,
            data_root=data_root,
            rules=rules,
            policy=policy,
            policy_name=policy_name,
            run_meta=run_meta,
            algo=algo,
            dataset_perf=dataset_perf,
        )
        machine["run"]["sec"] = round(time.time() - t_case, 1)
        attach_scorecards(machine)
        write_case_outputs(out_dir / case_id, machine)
        machines.append(machine)
        print(scorecard_line(machine["scorecard"], show_case=True), flush=True)
        print(
            scorecard_line(machine["rca_path"]["scorecard"], show_case=False),
            flush=True,
        )

    summary = aggregate(machines)
    summary["elapsed_s"] = round(time.time() - t0, 3)
    summary["dataset_perf"] = dataset_perf
    sibling = load_sibling_policy(out_dir, policy_name)
    if sibling:
        summary["sibling_policy"] = sibling
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text(
        summary_md(summary, sample=sample, policy=policy_name)
    )
    (out_dir / "index.html").write_text(
        index_html(summary, sample=sample, policy=policy_name)
    )
    manifest = {
        **run_meta,
        "command": sys.argv,
        "n_cases": len(cases),
        "elapsed_s": summary["elapsed_s"],
        "path_coverage": summary["path_coverage"],
        "rca_path_coverage": summary.get("rca_path_coverage"),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    _print_done(summary, out_dir)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample",
        type=Path,
        default=ANALYSIS_DIR / "samples" / "sample10.txt",
        help="case list file (default: analysis/samples/sample10.txt)",
    )
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="run one case id (repeatable); overrides --sample when set",
    )
    parser.add_argument(
        "--policy",
        choices=("strict", "relaxed"),
        default="strict",
        help="acceptance preset from evidence_rules.json",
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=DEFAULT_DATA_ROOT,
        help="case datapack root (Zenodo unpack → .../data/rcabench)",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=None,
        help="optional alternate evidence_rules.json",
    )
    parser.add_argument(
        "--algo",
        default=DEFAULT_ALGO,
        help="RCA seed algo override (default: auto = highest AC@1 with case output)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="keep existing case outputs; skip cases with machine_graph.json",
    )
    args = parser.parse_args(argv)

    if args.case:
        sample_path = ANALYSIS_DIR / "_cli_cases.txt"
        sample_path.write_text("\n".join(args.case) + "\n")
    else:
        sample_path = args.sample
        if not sample_path.is_absolute():
            candidates = [
                sample_path,
                REPO_ROOT / sample_path,
                ANALYSIS_DIR / sample_path.name,
                Path.cwd() / sample_path,
            ]
            sample_path = next((p for p in candidates if p.exists()), sample_path)

    result = run(
        sample_path=sample_path,
        policy_name=args.policy,
        data_root=args.data_root,
        rules_path=args.rules,
        algo=args.algo,
        resume=args.resume,
    )
    if isinstance(result, str):
        print(f"error: {result}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
