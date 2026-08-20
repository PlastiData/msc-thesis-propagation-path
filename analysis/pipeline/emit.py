"""Emit machine_graph.json and derived human_report.json / graph.html / summaries."""

from __future__ import annotations

import html
import json
from pathlib import Path

from .fault_taxonomy import taxonomy_public


SCHEMA_VERSION = "0.3.0"

LEVEL_COLOR = {
    "observed": "#1b9e77",
    "supported": "#7570b3",
    "inferred": "#d95f02",
}

EVID_RANK = {"observed": 0, "supported": 1, "inferred": 2}
EVID_SHORT = {"observed": "obs", "supported": "sup", "inferred": "inf"}
REFUSE_SHORT = {
    "required_horizontal_relationship_unavailable": "horiz",
    "no_connected_candidate_path": "nopath",
    "algo_output_missing": "algo",
    "ambiguous_equally_supported_paths": "ambig",
    "injected_component_unavailable": "inj",
    "symptom_unavailable": "sym",
    "evidence_query_failed": "query",
    "unsupported_case_schema": "schema",
    "required_vertical_topology_unavailable": "vert",
}

AGREEMENT_KEYS = ("same", "differ", "inject_only", "rca_only", "both_refuse")
SIBLING_POLICY = {"strict": "relaxed", "relaxed": "strict"}


def path_agreement(
    fault_status: str | None,
    fault_nodes: list | None,
    rca_status: str | None,
    rca_nodes: list | None,
) -> str:
    fault_ok = fault_status == "candidate_path_constructed"
    rca_ok = rca_status == "candidate_path_constructed"
    if not fault_ok and not rca_ok:
        return "both_refuse"
    if fault_ok and not rca_ok:
        return "inject_only"
    if rca_ok and not fault_ok:
        return "rca_only"
    if list(fault_nodes or []) == list(rca_nodes or []):
        return "same"
    return "differ"


def backfill_agreement(summary: dict) -> dict:
    """Fill agreement / agreement_profile from case path fields (old summaries)."""
    cases = summary.get("cases") or []
    if not cases:
        summary["agreement_profile"] = {k: 0 for k in AGREEMENT_KEYS}
        return summary
    if all("agreement" in c for c in cases) and "agreement_profile" in summary:
        return summary
    profile = {k: 0 for k in AGREEMENT_KEYS}
    for case in cases:
        tag = path_agreement(
            case.get("status"),
            case.get("path"),
            case.get("rca_status"),
            case.get("rca_path"),
        )
        case["agreement"] = tag
        profile[tag] += 1
    summary["agreement_profile"] = profile
    return summary


def load_sibling_policy(out_dir: Path, policy: str) -> dict | None:
    other = SIBLING_POLICY.get(policy)
    if not other:
        return None
    path = out_dir.parent / other / "summary.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    n = data.get("evaluated_cases") or 0
    return {
        "policy": other,
        "path_coverage": data.get("path_coverage"),
        "rca_path_coverage": data.get("rca_path_coverage"),
        "constructed_cases": data.get("constructed_cases"),
        "rca_constructed_cases": data.get("rca_constructed_cases"),
        "evaluated_cases": n,
    }


def refuse_short(reason: str | None) -> str:
    if not reason:
        return "?"
    return REFUSE_SHORT.get(reason, reason[:8])


def weakest_evid(levels: list[str]) -> str | None:
    if not levels:
        return None
    worst = max(levels, key=lambda level: EVID_RANK.get(level, 99))
    return EVID_SHORT.get(worst)


def rca_overlap_pct(path_nodes: list[str], top_services: list[dict], k: int = 5) -> int:
    if not path_nodes:
        return 0
    top = {
        str(row["service"])
        for row in (top_services or [])[:k]
        if row.get("service")
    }
    if not top:
        return 0
    hit = sum(1 for node in path_nodes if node in top)
    return int(round(100.0 * hit / len(path_nodes)))


def build_scorecard(
    machine: dict,
    *,
    seed: str,
    judgment: dict,
    edges: list[dict] | None = None,
) -> dict:
    """Flat five-col block; identical shape for path and refuse."""
    algo = machine.get("algo_context") or {}
    injection = ((machine.get("reality") or {}).get("injection") or {})
    tax = injection.get("injected_fault") or taxonomy_public(injection.get("fault_type"))
    base = {
        "case": machine.get("case_id"),
        "sec": (machine.get("run") or {}).get("sec"),
        "seed": seed,
        "evid": None,
        "rca_pct": 0,
        "hops": None,
        "algo": algo.get("algo"),
        "rank1": algo.get("rank1"),
        "refuse": judgment.get("primary_rejection_reason"),
        "injected_fault": tax,
        "target_layer": tax.get("target_layer"),
        "fault_kind": tax.get("fault_kind"),
        "category": tax.get("category"),
        "chaos_type": tax.get("chaos_type"),
    }
    if judgment.get("status") != "candidate_path_constructed":
        return base

    edges_by_id = {e["edge_id"]: e for e in (edges or [])}
    selected = [
        edges_by_id[eid]
        for eid in (judgment.get("selected_path_edge_ids") or [])
        if eid in edges_by_id
    ]
    levels = [e.get("evidence_level") for e in selected if e.get("evidence_level")]
    nodes = judgment.get("selected_path_nodes") or []
    base["evid"] = weakest_evid(levels)
    base["hops"] = len(selected)
    base["rca_pct"] = rca_overlap_pct(nodes, algo.get("top_services") or [])
    base["refuse"] = None
    return base


def empty_rca_path(
    *,
    algo: str | None,
    algo_ac_at_1: float | None,
    seed: str | None,
    end: str | None,
    reason: str = "algo_output_missing",
    policy: str | None = None,
) -> dict:
    from .judgment import case_metrics

    judgment = {
        "status": "insufficient_evidence",
        "selected_path_edge_ids": [],
        "selected_path_nodes": [],
        "primary_rejection_reason": reason,
        "rejection_reasons": [reason],
        "limitations": [
            "No official process-level ground truth was available.",
            reason,
        ],
        "policy": policy,
    }
    return {
        "algo": algo,
        "algo_ac_at_1": algo_ac_at_1,
        "seed": seed,
        "end": end,
        "judgment": judgment,
        "case_metrics": case_metrics(judgment, {}),
    }


_SEED_LABEL = {"fault": "inject", "algo": "rca"}


def scorecard_line(sc: dict, *, show_case: bool = True) -> str:
    case = (sc.get("case") or "") if show_case else ""
    seed = _SEED_LABEL.get(sc.get("seed") or "", sc.get("seed") or "?")
    sec = sc.get("sec")
    sec_s = f"{sec:.1f}" if isinstance(sec, (int, float)) else "—"
    evid = sc.get("evid") or "—"
    hops = sc.get("hops")
    hops_s = str(hops) if hops is not None else "—"
    return (
        f"{case:<34}{seed:<7}{sec_s:>5}  {evid:<4} "
        f"{sc.get('rca_pct', 0):>4}  {hops_s:>4}"
    )


SCORECARD_HEADER = (
    f"{'case':<34}{'seed':<7}{'sec':>5}  {'evid':<4} {'rca%':>4}  {'hops':>4}"
)
SCORECARD_LEGEND = (
    "seed: inject=real injection→symptom  rca=best-algo#1→symptom  |  "
    "obs=in telemetry  sup=signals agree  inf=plausible, evidence thin"
)


def _short(name: str) -> str:
    text = name or ""
    if text.startswith("ts-"):
        text = text[3:]
    if text.endswith("-service"):
        text = text[: -len("-service")]
    return text or name


def build_machine_graph(
    case_id: str,
    run: dict,
    reality: dict,
    annotated: dict,
    judgment: dict,
    metrics: dict,
    algo_context: dict | None = None,
    rca_path: dict | None = None,
) -> dict:
    reality_out = {
        "injection": reality["injection"],
        "symptom": reality["symptom"],
        "services_in_abnormal_traces": reality.get("services_in_abnormal_traces") or [],
        "placement": {
            "pod_count": len((reality.get("placement") or {}).get("pod_to_service") or {}),
            "node_count": len((reality.get("placement") or {}).get("node_to_pods") or {}),
        },
        "timeline": reality.get("timeline") or [],
    }
    algo = algo_context or {"available": False}
    end = (reality.get("symptom") or {}).get("component")
    rca = rca_path or empty_rca_path(
        algo=algo.get("algo"),
        algo_ac_at_1=algo.get("algo_ac_at_1"),
        seed=algo.get("rank1"),
        end=end,
        reason=algo.get("reason") or "algo_output_missing",
        policy=run.get("policy"),
    )
    machine = {
        "schema_version": SCHEMA_VERSION,
        "case_id": case_id,
        "run": run,
        "reality": reality_out,
        "candidate_graph": {
            "nodes": [
                {"id": n}
                for n in sorted(
                    {
                        *(e["source"] for e in annotated["edges"]),
                        *(e["target"] for e in annotated["edges"]),
                        reality["injection"]["component"],
                        reality["symptom"]["component"],
                    }
                )
            ],
            "edges": annotated["edges"],
        },
        "judgment": {
            "status": judgment["status"],
            "selected_path_edge_ids": judgment.get("selected_path_edge_ids") or [],
            "selected_path_nodes": judgment.get("selected_path_nodes") or [],
            "primary_rejection_reason": judgment.get("primary_rejection_reason"),
            "rejection_reasons": judgment.get("rejection_reasons") or [],
            "limitations": judgment.get("limitations") or [],
            "policy": judgment.get("policy"),
        },
        "case_metrics": metrics,
        "evidence_registry": annotated.get("evidence_registry") or [],
        "algo_context": algo,
        "rca_path": rca,
    }
    attach_scorecards(machine)
    return machine


def reject_machine_graph(
    case_id: str,
    run: dict,
    reason: str,
    detail: str = "",
    algo_context: dict | None = None,
    reality: dict | None = None,
    rca_path: dict | None = None,
) -> dict:
    reality_out = {}
    if reality:
        reality_out = {
            "injection": reality.get("injection") or {},
            "symptom": reality.get("symptom") or {},
            "timeline": reality.get("timeline") or [],
            "services_in_abnormal_traces": reality.get("services_in_abnormal_traces") or [],
        }
    algo = algo_context or {"available": False}
    end = (reality_out.get("symptom") or {}).get("component") if reality_out else None
    rca = rca_path or empty_rca_path(
        algo=algo.get("algo"),
        algo_ac_at_1=algo.get("algo_ac_at_1"),
        seed=algo.get("rank1"),
        end=end,
        reason=algo.get("reason") or "algo_output_missing",
        policy=run.get("policy"),
    )
    machine = {
        "schema_version": SCHEMA_VERSION,
        "case_id": case_id,
        "run": run,
        "reality": reality_out,
        "candidate_graph": {"nodes": [], "edges": []},
        "judgment": {
            "status": "insufficient_evidence",
            "selected_path_edge_ids": [],
            "selected_path_nodes": [],
            "primary_rejection_reason": reason,
            "rejection_reasons": [reason],
            "limitations": [
                "No official process-level ground truth was available.",
                detail or reason,
            ],
            "policy": run.get("policy"),
        },
        "case_metrics": {
            "path_covered": 0,
            "observed_edges": 0,
            "supported_edges": 0,
            "inferred_edges": 0,
            "observed_edge_ratio": 0.0,
            "supported_edge_ratio": 0.0,
            "inferred_edge_ratio": 0.0,
            "returned_edges": 0,
        },
        "evidence_registry": [],
        "algo_context": algo,
        "rca_path": rca,
    }
    attach_scorecards(machine)
    return machine


def attach_scorecards(machine: dict) -> None:
    edges = (machine.get("candidate_graph") or {}).get("edges") or []
    machine["scorecard"] = build_scorecard(
        machine, seed="fault", judgment=machine["judgment"], edges=edges
    )
    rca = machine.get("rca_path") or {}
    rca_judgment = rca.get("judgment") or {
        "status": "insufficient_evidence",
        "primary_rejection_reason": "algo_output_missing",
        "selected_path_edge_ids": [],
        "selected_path_nodes": [],
    }
    rca["scorecard"] = build_scorecard(
        machine, seed="algo", judgment=rca_judgment, edges=edges
    )
    machine["rca_path"] = rca


def _hop_refs_brief(edge: dict) -> dict:
    hop = edge.get("hop") or {}
    return {
        "route": hop.get("route"),
        "call_count": hop.get("call_count"),
        "error_count": hop.get("error_count"),
        "trace_ids": hop.get("trace_ids") or [],
        "stat": hop.get("stat") or {},
    }


def human_report_from_machine(machine: dict) -> dict:
    if "scorecard" not in machine:
        attach_scorecards(machine)
    judgment = machine["judgment"]
    reality = machine.get("reality") or {}
    injection = reality.get("injection") or {}
    symptom = reality.get("symptom") or {}
    metrics = machine.get("case_metrics") or {}
    algo = machine.get("algo_context") or {}
    rca = machine.get("rca_path") or {}

    report = {
        "case_id": machine["case_id"],
        "status": judgment["status"],
        "scorecard": machine.get("scorecard"),
        "scorecard_algo": rca.get("scorecard"),
        "algo": {
            "algo": algo.get("algo"),
            "available": bool(algo.get("available")),
            "rank1": algo.get("rank1"),
            "rank1_hit": algo.get("rank1_hit"),
            "algo_ac_at_1": algo.get("algo_ac_at_1"),
            "predicted_chain": algo.get("predicted_chain") or [],
            "error": algo.get("error") or algo.get("reason"),
        },
    }

    if judgment["status"] != "candidate_path_constructed":
        report["reality"] = {
            "known_injection": (
                f"Injected fault (benchmark label): fault_type "
                f"{injection.get('fault_type')} "
                f"({(injection.get('injected_fault') or {}).get('chaos_type') or '?'}) "
                f"at {injection.get('component', 'unknown')}."
                if injection
                else "Injection facts unavailable."
            ),
            "observed_symptom": (
                f"{symptom.get('component')} via {symptom.get('selection_rule')}."
                if symptom
                else "Symptom unavailable."
            ),
        }
        report["evidence"] = {
            "available": [
                e.get("claim")
                for e in (machine.get("evidence_registry") or [])[:8]
                if e.get("claim")
            ]
        }
        report["judgment"] = {
            "safe_statement": "A connected candidate path could not be reconstructed.",
            "primary_rejection_reason": judgment.get("primary_rejection_reason"),
            "cannot_claim": (
                "The available dataset does not prove a unique true causal path."
            ),
            "missing_evidence": judgment.get("limitations") or [],
        }
        return report

    edges_by_id = {e["edge_id"]: e for e in machine["candidate_graph"]["edges"]}
    path = []
    for eid in judgment["selected_path_edge_ids"]:
        edge = edges_by_id[eid]
        path.append(
            {
                "hop": f"{edge['source']} -> {edge['target']}",
                "level": edge["evidence_level"],
                "checks": edge.get("checks") or {},
                "refs": _hop_refs_brief(edge),
                "missing_evidence": edge.get("missing_evidence") or [],
                "sources": sorted(
                    {
                        r.get("source_file")
                        for r in machine["evidence_registry"]
                        if r["evidence_id"] in edge.get("evidence_refs", [])
                    }
                ),
            }
        )

    def pct(x: float) -> str:
        return f"{100.0 * x:.1f}%"

    report["reality"] = {
        "known_injection": (
            f"Injected fault (benchmark label): fault_type "
            f"{injection.get('fault_type')} "
            f"({(injection.get('injected_fault') or {}).get('chaos_type') or '?'}) "
            f"injected into {injection.get('component')}."
        ),
        "observed_symptom": (
            f"{symptom.get('component')} selected by {symptom.get('selection_rule')}."
        ),
        "timeline_summary": [
            (
                f"{ev.get('timestamp')}: {ev.get('event_type')} @ {ev.get('component')}"
                + (f" — {ev.get('note')}" if ev.get("note") else "")
            )
            for ev in (reality.get("timeline") or [])
        ],
    }
    report["evidence"] = {
        "path": path,
        "composition": {
            "observed": pct(metrics.get("observed_edge_ratio") or 0.0),
            "supported": pct(metrics.get("supported_edge_ratio") or 0.0),
            "inferred": pct(metrics.get("inferred_edge_ratio") or 0.0),
        },
    }
    report["judgment"] = {
        "safe_statement": (
            "The telemetry supports this candidate relationship under the "
            f"{judgment.get('policy')} policy."
        ),
        "cannot_claim": (
            "The available dataset does not prove that this is the unique "
            "true causal path."
        ),
        "missing_evidence": [
            m
            for e in (edges_by_id[i] for i in judgment["selected_path_edge_ids"])
            for m in (e.get("missing_evidence") or [])
        ],
    }
    return report


def _path_svg(
    nodes: list[str],
    edges: list[dict],
    *,
    aria: str = "candidate propagation path",
    endpoint_labels: tuple[str, str] = ("seed", "symptom"),
) -> str:
    if not nodes:
        return "<p class='muted'>No candidate path selected.</p>"
    width = max(720, 160 * len(nodes))
    height = 120
    y = 55
    gap = width / max(len(nodes), 1)
    coords = [(i * gap + gap / 2, y) for i in range(len(nodes))]
    edge_by_pair = {(e["source"], e["target"]): e for e in edges}
    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" '
        f'role="img" aria-label="{html.escape(aria)}">'
    ]
    for i in range(len(nodes) - 1):
        edge = edge_by_pair.get((nodes[i], nodes[i + 1]), {})
        level = edge.get("evidence_level", "observed")
        color = LEVEL_COLOR.get(level, "#666")
        dash = ' stroke-dasharray="7 5"' if level == "inferred" else ""
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        parts.append(
            f'<line x1="{x1 + 42}" y1="{y1}" x2="{x2 - 42}" y2="{y2}" '
            f'stroke="{color}" stroke-width="3"{dash} />'
        )
        mid = (x1 + x2) / 2
        parts.append(
            f'<text x="{mid}" y="{y1 - 18}" text-anchor="middle" '
            f'font-size="12" fill="{color}">{html.escape(level)}</text>'
        )
    for i, node in enumerate(nodes):
        x, yy = coords[i]
        if i == 0:
            role = endpoint_labels[0]
        elif i == len(nodes) - 1:
            role = endpoint_labels[1]
        else:
            role = "hop"
        fill = "#111" if role != "hop" else "#fff"
        text = "#fff" if role != "hop" else "#111"
        parts.append(
            f'<rect x="{x - 40}" y="{yy - 18}" width="80" height="36" rx="8" '
            f'fill="{fill}" stroke="#111" stroke-width="1.5" />'
            f'<text x="{x}" y="{yy + 5}" text-anchor="middle" font-size="12" '
            f'fill="{text}">{html.escape(_short(node))}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _algo_panel_html(algo: dict) -> str:
    rankings = algo.get("rankings") or {}
    if not algo.get("available") and not rankings:
        reason = algo.get("reason") or algo.get("error") or "unavailable"
        return (
            "<section><h2>Upstream RCA rankings</h2>"
            f"<p class='muted'>No algorithm output under "
            f"<code>output/.../data/rcabench/&lt;case&gt;/</code> "
            f"({html.escape(str(reason))})</p></section>"
        )

    hit = algo.get("rank1_hit")
    hit_txt = "hit" if hit else "miss" if hit is False else "unknown"
    chain = " → ".join(_short(s) for s in (algo.get("predicted_chain") or [])) or "—"
    true_rank = algo.get("true_label_best_rank")
    true_rank_txt = str(true_rank) if true_rank is not None else "—"

    compare_rows = []
    for name, row in rankings.items():
        compare_rows.append(
            "<tr>"
            f"<td>{html.escape(name)}</td>"
            f"<td>{html.escape(_short(str(row.get('rank1') or '—')))}</td>"
            f"<td>{'✓' if row.get('hit_at_1') else '·'}</td>"
            f"<td>{'✓' if row.get('hit_at_5') else '·'}</td>"
            f"<td>{row.get('true_label_best_rank') if row.get('true_label_best_rank') is not None else '—'}</td>"
            "</tr>"
        )

    top_rows = "".join(
        "<tr>"
        f"<td>{row.get('rank')}</td>"
        f"<td>{html.escape(_short(str(row.get('service'))))}</td>"
        f"<td>{'✓' if row.get('hit') else '·'}</td>"
        "</tr>"
        for row in (algo.get("top_services") or [])
    )
    err = ""
    if algo.get("error"):
        err = f"<p class='warn'>Walk note: {html.escape(str(algo['error']))}</p>"
    return f"""
<section>
<h2>Upstream RCA rankings (from output parquet)</h2>
<p>Primary walk seed: <strong>{html.escape(str(algo.get('algo')))}</strong>
 → <code>{html.escape(_short(str(algo.get('rank1') or '—')))}</code> ({hit_txt}).
 Injection label best rank under primary: <strong>{html.escape(true_rank_txt)}</strong>.</p>
<p><strong>Walk chain:</strong> {html.escape(chain)}</p>
{err}
<div class="grid">
<div class="card">
<h3>All algorithms on this case</h3>
<table><thead><tr><th>Algo</th><th>Rank-1</th><th>Hit@1</th><th>Hit@5</th><th>True rank</th></tr></thead>
<tbody>{''.join(compare_rows) or '<tr><td colspan="5">none</td></tr>'}</tbody></table>
</div>
<div class="card">
<h3>{html.escape(str(algo.get('algo')))} top services</h3>
<table><thead><tr><th>Rank</th><th>Service</th><th>Hit</th></tr></thead>
<tbody>{top_rows or '<tr><td colspan="3">empty</td></tr>'}</tbody></table>
</div>
</div>
<p class="muted">Rankings come from <code>output/rcabench-platform-v2/data/rcabench/&lt;case&gt;/&lt;algo&gt;/output.parquet</code>.
Evidence path labels are independent of these scores.</p>
</section>
"""


def _selected_path_view(judgment: dict, edges: list[dict]) -> tuple[list[str], list[dict]]:
    selected_ids = set(judgment.get("selected_path_edge_ids") or [])
    selected = [e for e in edges if e["edge_id"] in selected_ids]
    nodes = judgment.get("selected_path_nodes") or []
    if nodes or not selected:
        return nodes, selected
    return [selected[0]["source"], *[e["target"] for e in selected]], selected


def _route_short(route: str | None) -> str:
    if not route:
        return "—"
    text = str(route)
    for proto in ("http://", "https://"):
        if proto in text:
            after = text.split(proto, 1)[1]
            slash = after.find("/")
            if slash >= 0:
                return after[slash:][:72] or text[:72]
    return text[:72]


def _fmt_stat_hit(hit: dict) -> str:
    metric = hit.get("metric") or "?"
    short = metric if len(metric) <= 40 else metric[:37] + "…"
    if hit.get("z") is not None:
        return f"{short} z={hit['z']} (abn {hit.get('abnormal_mean')} / nrm {hit.get('normal_mean')})"
    if hit.get("ratio") is not None:
        return f"{short} ×{hit['ratio']} (abn {hit.get('abnormal_mean')} / nrm {hit.get('normal_mean')})"
    if hit.get("p99") is not None:
        return f"{short} abn {hit.get('abnormal_mean')} vs p99 {hit.get('p99')}"
    return f"{short} abn {hit.get('abnormal_mean')} / nrm {hit.get('normal_mean')}"


def _stat_cell(edge: dict) -> str:
    checks = edge.get("checks") or {}
    verdict = str(checks.get("statistical") or "—")
    hop = edge.get("hop") or {}
    stat = hop.get("stat") or {}
    lines = [f"<div><strong>{html.escape(verdict)}</strong></div>"]
    for role, key in (("from", "source"), ("to", "target")):
        ep = stat.get(key) or {}
        if not ep:
            continue
        bits = [f"{role}: {ep.get('verdict') or '—'}"]
        hits = ep.get("hits") or []
        if hits:
            bits.append(_fmt_stat_hit(hits[0]))
            if len(hits) > 1:
                bits.append(f"+{len(hits) - 1} more")
        elif ep.get("source") == "traces":
            bits.append(f"err {ep.get('errors')}/{ep.get('spans')} spans")
        elif ep.get("n_compared") is not None:
            bits.append(f"{ep.get('n_compared')} metrics compared, 0 hits")
        lines.append(
            f"<div class='muted tiny'>{html.escape(' · '.join(str(b) for b in bits))}</div>"
        )
    return "".join(lines)


def _hop_table_rows(selected: list[dict]) -> str:
    rows = []
    for edge in selected:
        checks = edge.get("checks") or {}
        hop = edge.get("hop") or {}
        color = LEVEL_COLOR.get(edge.get("evidence_level"), "#666")
        route = _route_short(hop.get("route"))
        calls = hop.get("call_count")
        errors = hop.get("error_count")
        if calls is None:
            heat = "—"
        else:
            heat = f"{calls}"
            if errors:
                heat += f" / {errors} err"
        traces = hop.get("trace_ids") or []
        if traces:
            trace_html = "<br>".join(
                f"<code class='tid'>{html.escape(t[:16])}…</code>"
                if len(t) > 16
                else f"<code class='tid'>{html.escape(t)}</code>"
                for t in traces[:3]
            )
        else:
            trace_html = "<span class='muted'>—</span>"
        struct = str(checks.get("structural") or "—")
        win = []
        if hop.get("in_abnormal"):
            win.append("abn")
        if hop.get("in_normal"):
            win.append("nrm")
        struct_extra = f" ({'+'.join(win)})" if win else ""
        rows.append(
            "<tr>"
            f"<td>{html.escape(_short(edge['source']))}</td>"
            f"<td>{html.escape(_short(edge['target']))}</td>"
            f"<td><code>{html.escape(route)}</code></td>"
            f"<td style='color:{color};font-weight:600'>"
            f"{html.escape(edge.get('evidence_level',''))}</td>"
            f"<td>{html.escape(struct)}{html.escape(struct_extra)}</td>"
            f"<td>{html.escape(heat)}</td>"
            f"<td>{trace_html}</td>"
            f"<td>{_stat_cell(edge)}</td>"
            "</tr>"
        )
    return "".join(rows)


def _path_brief(judgment: dict, edges: list[dict]) -> str:
    if judgment.get("status") != "candidate_path_constructed":
        return refuse_short(judgment.get("primary_rejection_reason"))
    _, selected = _selected_path_view(judgment, edges)
    levels = [e.get("evidence_level") for e in selected if e.get("evidence_level")]
    counts = {"observed": 0, "supported": 0, "inferred": 0}
    for level in levels:
        if level in counts:
            counts[level] += 1
    return f"obs={counts['observed']} sup={counts['supported']} inf={counts['inferred']}"


def _case_injected_fault(machine: dict) -> dict:
    injection = ((machine.get("reality") or {}).get("injection") or {})
    tax = injection.get("injected_fault")
    if isinstance(tax, dict) and tax.get("fault_kind"):
        return tax
    return taxonomy_public(injection.get("fault_type"))


def _strat_bucket() -> dict[str, int]:
    return {"n": 0, "accept": 0, "refuse": 0}


def _bump_strat(table: dict[str, dict[str, int]], key: str, accepted: bool) -> None:
    label = key or "unknown"
    row = table.setdefault(label, _strat_bucket())
    row["n"] += 1
    if accepted:
        row["accept"] += 1
        return
    row["refuse"] += 1


def stratify_by_injection(
    machines: list[dict],
    *,
    group_key: str,
) -> dict[str, dict[str, dict[str, int]]]:
    """Accept/refuse counts by injection taxonomy field, per seed.

    group_key: target_layer | fault_kind | category
    """
    inject: dict[str, dict[str, int]] = {}
    rca: dict[str, dict[str, int]] = {}
    for m in machines:
        tax = _case_injected_fault(m)
        key = str(tax.get(group_key) or "unknown")
        fault_ok = m["judgment"]["status"] == "candidate_path_constructed"
        rca_ok = (m.get("rca_path") or {}).get("judgment", {}).get(
            "status"
        ) == "candidate_path_constructed"
        _bump_strat(inject, key, fault_ok)
        _bump_strat(rca, key, rca_ok)
    return {"inject": inject, "rca": rca}


def build_injection_stratification(machines: list[dict]) -> dict:
    return {
        "by_target_layer": stratify_by_injection(machines, group_key="target_layer"),
        "by_fault_kind": stratify_by_injection(machines, group_key="fault_kind"),
        "by_category": stratify_by_injection(machines, group_key="category"),
        "note": (
            "Stratified by injected fault (benchmark label) via OpenRCA 2.0 "
            "Tables 5–6 taxonomy lookup — not detected error type, not Table 7 "
            "rule firing."
        ),
    }


QUEUE_SORT_RANK = {
    "differ": 0,
    "inject_only": 1,
    "rca_only": 1,
    "both_refuse": 1,
    "same": 2,
}
QUEUE_FILTER = {
    "all": AGREEMENT_KEYS,
    "differ": ("differ",),
    "refuse": ("inject_only", "rca_only", "both_refuse"),
    "same": ("same",),
}


def _queue_sort_key(case: dict) -> tuple:
    tag = case.get("agreement") or "both_refuse"
    return (QUEUE_SORT_RANK.get(tag, 9), case.get("case_id") or "")


def _path_strip_html(
    nodes: list | None,
    edges: list | None = None,
    *,
    refused: bool = False,
    refuse_reason: str | None = None,
) -> str:
    if refused or not nodes:
        reason = refuse_short(refuse_reason) if refuse_reason else "—"
        return (
            f"<span class='strip refuse'>refuse — "
            f"{html.escape(reason)}</span>"
        )
    edge_by_pair = {}
    for edge in edges or []:
        edge_by_pair[(edge.get("source"), edge.get("target"))] = edge
    parts = ["<span class='strip'>"]
    for i, node in enumerate(nodes):
        if i:
            edge = edge_by_pair.get((nodes[i - 1], node), {})
            level = edge.get("evidence_level") or "observed"
            color = LEVEL_COLOR.get(level, "#666")
            dash = " dashed" if level == "inferred" else ""
            parts.append(
                f"<span class='tick{dash}' style='border-color:{color}' "
                f"title='{html.escape(level)}'></span>"
            )
        parts.append(f"<span class='hop'>{html.escape(_short(str(node)))}</span>")
    parts.append("</span>")
    return "".join(parts)


def _verdict_label(judgment: dict, *, policy: str | None = None) -> str:
    pol = policy or judgment.get("policy") or "?"
    if judgment.get("status") == "candidate_path_constructed":
        return f"ACCEPT ({pol})"
    reason = refuse_short(judgment.get("primary_rejection_reason"))
    return f"REFUSE — {reason}"


def _injected_fault_banner_html(injection: dict) -> str:
    tax = injection.get("injected_fault") or taxonomy_public(injection.get("fault_type"))
    ft = tax.get("fault_type", injection.get("fault_type", "?"))
    chaos = tax.get("chaos_type") or "?"
    kind = tax.get("fault_kind") or "?"
    layer = tax.get("target_layer") or "?"
    cat = tax.get("category") or "?"
    channel = tax.get("expected_propagation_channel") or "?"
    return (
        "<div class='tiny'>"
        "<strong>Injected fault (benchmark label)</strong>: "
        f"fault_type={html.escape(str(ft))} → "
        f"<code>{html.escape(str(chaos))}</code> "
        f"({html.escape(str(cat))}, {html.escape(str(layer))}, "
        f"kind=<code>{html.escape(str(kind))}</code>, "
        f"channel={html.escape(str(channel))})"
        "</div>"
    )


def graph_html_from_machine(machine: dict) -> str:
    judgment = machine["judgment"]
    reality = machine.get("reality") or {}
    injection = reality.get("injection") or {}
    symptom = reality.get("symptom") or {}
    edges = machine.get("candidate_graph", {}).get("edges") or []
    nodes, selected = _selected_path_view(judgment, edges)
    status = judgment.get("status")
    ok = status == "candidate_path_constructed"
    banner_color = "#1b9e77" if ok else "#c44"

    rca = machine.get("rca_path") or {}
    rca_judgment = rca.get("judgment") or {}
    rca_nodes, rca_selected = _selected_path_view(rca_judgment, edges)
    rca_ok = rca_judgment.get("status") == "candidate_path_constructed"
    rca_algo = rca.get("algo") or (machine.get("algo_context") or {}).get("algo") or "—"
    rca_ac = rca.get("algo_ac_at_1")
    rca_ac_txt = f"{100 * rca_ac:.1f}%" if isinstance(rca_ac, (int, float)) else "—"
    agree = path_agreement(status, nodes, rca_judgment.get("status"), rca_nodes)

    policy = judgment.get("policy") or (machine.get("run") or {}).get("policy")
    inject_verdict = _verdict_label(judgment, policy=policy)
    rca_verdict = _verdict_label(rca_judgment, policy=policy)

    inject_strip = _path_strip_html(
        nodes, selected, refused=not ok, refuse_reason=judgment.get("primary_rejection_reason")
    )
    rca_strip = _path_strip_html(
        rca_nodes,
        rca_selected,
        refused=not rca_ok,
        refuse_reason=rca_judgment.get("primary_rejection_reason"),
    )

    if agree == "same" and ok:
        dual_block = (
            "<div class='path-row'>"
            "<div class='lab'>Both seeds</div>"
            f"{inject_strip}"
            "<span class='tag same'>same</span>"
            "</div>"
        )
    else:
        dual_block = (
            "<div class='path-row'>"
            "<div class='lab'>Inject</div>"
            f"{inject_strip}"
            "</div>"
            "<div class='path-row'>"
            "<div class='lab'>RCA</div>"
            f"{rca_strip}"
            "</div>"
        )

    path_svg = ""
    if ok:
        path_svg = (
            "<details class='maps'><summary>Fault-seeded SVG map</summary>"
            + _path_svg(
                nodes,
                selected,
                aria="fault-seeded candidate path",
                endpoint_labels=("fault", "symptom"),
            )
            + "</details>"
        )
    rca_svg = ""
    if rca_ok:
        rca_svg = (
            "<details class='maps'><summary>RCA-seeded SVG map</summary>"
            + _path_svg(
                rca_nodes,
                rca_selected,
                aria="RCA-seeded candidate path",
                endpoint_labels=("rank1", "symptom"),
            )
            + "</details>"
        )

    hop_rows = _hop_table_rows(selected)
    if not hop_rows and rca_ok:
        hop_rows = _hop_table_rows(rca_selected)
        hop_caption = "Edge evidence (RCA-selected)"
    else:
        hop_caption = "Edge evidence (fault-selected)" if hop_rows else "Edge evidence"

    timeline = reality.get("timeline") or []
    tl_items = "".join(
        "<li>"
        f"<span class='t'>{html.escape(str(ev.get('timestamp') or '—'))}</span> "
        f"<strong>{html.escape(str(ev.get('event_type')))}</strong> @ "
        f"<code>{html.escape(_short(str(ev.get('component'))))}</code>"
        + (
            f"<div class='muted tiny'>{html.escape(str(ev.get('note')))}</div>"
            if ev.get("note")
            else ""
        )
        + "</li>"
        for ev in timeline
    ) or "<li class='muted'>No timeline events recorded.</li>"

    inj_window = ""
    start = injection.get("start_time")
    end = injection.get("end_time")
    if start or end:
        inj_window = (
            f"Injection window <code>{html.escape(str(start or '—'))}</code>"
            f" → <code>{html.escape(str(end or '—'))}</code><br>"
        )

    symptom_route = ""
    if symptom.get("span_name"):
        symptom_route = (
            f"Symptom route <code>{html.escape(_route_short(symptom.get('span_name')))}</code><br>"
        )

    claims = [
        e.get("claim")
        for e in (machine.get("evidence_registry") or [])[:10]
        if e.get("claim")
    ]
    claim_items = "".join(f"<li>{html.escape(c)}</li>" for c in claims) or (
        "<li class='muted'>No evidence claims.</li>"
    )

    reject_block = ""
    if not ok:
        reject_block = (
            "<section><h2>Why no fault-seeded path</h2>"
            f"<p><strong>{html.escape(str(judgment.get('primary_rejection_reason')))}</strong></p>"
            "<ul>"
            + "".join(
                f"<li>{html.escape(str(x))}</li>"
                for x in (judgment.get("limitations") or [])
            )
            + "</ul></section>"
        )

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{html.escape(machine['case_id'])}</title>
<style>
:root {{ --bg:#faf9f7; --ink:#1a1a1a; --muted:#666; --line:#ddd; }}
body{{font-family:ui-sans-serif,system-ui,sans-serif;margin:0;background:var(--bg);color:var(--ink)}}
main{{max-width:1100px;margin:0 auto;padding:1.5rem}}
h1{{font-size:1.35rem;margin:0 0 .5rem}}
h2{{font-size:1.05rem;margin:1.5rem 0 .6rem;border-bottom:1px solid var(--line);padding-bottom:.3rem}}
h3{{font-size:.95rem;margin:.2rem 0 .5rem}}
.banner{{padding:.9rem 1rem;background:#fff;border-left:5px solid {banner_color};margin:1rem 0;box-shadow:0 1px 0 var(--line)}}
.verdicts{{display:flex;flex-wrap:wrap;gap:.75rem 1.5rem;margin:.4rem 0 .6rem;font-family:ui-monospace,monospace;font-size:.92rem}}
.verdicts .v{{font-weight:700}}
.agree{{display:inline-block;font-size:.8rem;padding:.15rem .45rem;border:1px solid var(--line);background:#fff}}
.path-compare{{background:#fff;border:1px solid var(--line);padding:1rem;margin:1rem 0}}
.path-row{{display:flex;align-items:center;gap:.75rem;margin:.55rem 0;flex-wrap:wrap}}
.path-row .lab{{min-width:4.5rem;font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
.strip{{display:inline-flex;align-items:center;flex-wrap:wrap;gap:.25rem}}
.strip .hop{{background:#111;color:#fff;padding:.2rem .45rem;font-size:.82rem;border-radius:4px}}
.strip .tick{{display:inline-block;width:18px;height:0;border-top:3px solid #1b9e77;margin:0 .1rem}}
.strip .tick.dashed{{border-top-style:dashed;border-color:#d95f02}}
.strip.refuse{{color:#a45;font-family:ui-monospace,monospace;font-size:.88rem}}
.tag.same{{font-size:.75rem;color:var(--muted);border:1px solid var(--line);padding:.1rem .35rem}}
.maps{{margin:.5rem 0}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:#fff;padding:1rem;border:1px solid var(--line)}}
table{{border-collapse:collapse;width:100%;font-size:.88rem;background:#fff}}
th,td{{border:1px solid var(--line);padding:.4rem;text-align:left;vertical-align:top}}
.muted{{color:var(--muted)}} .warn{{color:#a45}} .tiny{{font-size:.78rem;line-height:1.35;margin-top:.15rem}}
.legend span{{display:inline-block;margin-right:1rem}}
.legend i{{display:inline-block;width:12px;height:12px;margin-right:.3rem;vertical-align:middle}}
ul.timeline{{list-style:none;padding:0;margin:0}}
ul.timeline li{{padding:.35rem 0;border-bottom:1px solid var(--line)}}
ul.timeline .t{{color:var(--muted);font-size:.85rem;display:block}}
code{{font-size:.9em}} code.tid{{font-size:.78em}}
a{{color:#0b5}}
</style></head><body><main>
<p><a href="../index.html">← sample index</a></p>
<h1>{html.escape(machine['case_id'])}</h1>
<div class="banner" id="verdict">
<div class="verdicts">
<span>Inject <span class="v">{html.escape(inject_verdict)}</span></span>
<span>RCA <span class="v">{html.escape(rca_verdict)}</span></span>
<span class="agree">{html.escape(agree)}</span>
</div>
Injection <code>{html.escape(_short(str(injection.get('component') or '—')))}</code>
 → symptom <code>{html.escape(_short(str(symptom.get('component') or '—')))}</code><br>
{_injected_fault_banner_html(injection)}
{inj_window}{symptom_route}
RCA seed algo <code>{html.escape(str(rca_algo))}</code> (AC@1 {html.escape(rca_ac_txt)})
 → <code>{html.escape(_short(str(rca.get('seed') or '—')))}</code><br>
<em>Evidence levels describe availability, not causal correctness.</em>
</div>
<div class="legend">
<span><i style="background:{LEVEL_COLOR['observed']}"></i>observed</span>
<span><i style="background:{LEVEL_COLOR['supported']}"></i>supported</span>
<span><i style="background:{LEVEL_COLOR['inferred']}"></i>inferred (dashed)</span>
</div>
<section id="dual-path">
<h2>Dual-path compare</h2>
<div class="path-compare">{dual_block}</div>
{path_svg}
{rca_svg}
</section>
{reject_block}
<section id="evidence">
<h2>{html.escape(hop_caption)}</h2>
<p class="muted tiny">Struct/Stat are verdicts. Route, calls/errors, trace ids, and metric numbers are re-queryable refs from abnormal-window telemetry. Per-hop onset time is not available on this dataset.</p>
<table>
<thead><tr><th>From</th><th>To</th><th>Route</th><th>Level</th><th>Struct</th><th>Calls</th><th>Traces</th><th>Stat</th></tr></thead>
<tbody>
{hop_rows if hop_rows else '<tr><td colspan="8">No selected edges</td></tr>'}
</tbody></table>
</section>
{_algo_panel_html(machine.get('algo_context') or {})}
<div class="grid">
<div class="card">
<h2>Timeline anchors</h2>
<p class="muted tiny">Sparse anchors only (injection window, first error, symptom / path errors) — not a full incident Gantt.</p>
<ul class="timeline">{tl_items}</ul>
</div>
<div class="card">
<h2>What was detected</h2>
<ul>{claim_items}</ul>
</div>
</div>
</main></body></html>
"""


def write_case_outputs(out_dir: Path, machine: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "machine_graph.json").write_text(
        json.dumps(machine, indent=2, sort_keys=True) + "\n"
    )
    human = human_report_from_machine(machine)
    (out_dir / "human_report.json").write_text(
        json.dumps(human, indent=2, sort_keys=True) + "\n"
    )
    (out_dir / "graph.html").write_text(graph_html_from_machine(machine))


def _seed_counts(machines: list[dict], *, rca: bool) -> dict:
    constructed = 0
    refuse_reasons: dict[str, int] = {}
    evid_counts = {"obs": 0, "sup": 0, "inf": 0}
    for m in machines:
        if "scorecard" not in m:
            attach_scorecards(m)
        sc = (m.get("rca_path") or {}).get("scorecard") if rca else m.get("scorecard")
        sc = sc or {}
        if sc.get("evid"):
            constructed += 1
            evid_counts[sc["evid"]] = evid_counts.get(sc["evid"], 0) + 1
            continue
        reason = sc.get("refuse") or "other"
        refuse_reasons[reason] = refuse_reasons.get(reason, 0) + 1
    return {
        "constructed": constructed,
        "refused": len(machines) - constructed,
        "refuse_reasons": refuse_reasons,
        "evid_counts": evid_counts,
    }


def aggregate(machines: list[dict]) -> dict:
    n = len(machines)
    constructed = [m for m in machines if m["judgment"]["status"] == "candidate_path_constructed"]
    obs = sum(m["case_metrics"]["observed_edges"] for m in constructed)
    sup = sum(m["case_metrics"]["supported_edges"] for m in constructed)
    inf = sum(m["case_metrics"]["inferred_edges"] for m in constructed)
    returned = obs + sup + inf
    rejected = [m for m in machines if m["judgment"]["status"] != "candidate_path_constructed"]
    reasons: dict[str, int] = {}
    for m in rejected:
        reason = m["judgment"].get("primary_rejection_reason") or "other"
        reasons[reason] = reasons.get(reason, 0) + 1

    rca_built = [
        m
        for m in machines
        if (m.get("rca_path") or {}).get("judgment", {}).get("status")
        == "candidate_path_constructed"
    ]
    rca_obs = sum((m.get("rca_path") or {}).get("case_metrics", {}).get("observed_edges", 0) for m in rca_built)
    rca_sup = sum((m.get("rca_path") or {}).get("case_metrics", {}).get("supported_edges", 0) for m in rca_built)
    rca_inf = sum((m.get("rca_path") or {}).get("case_metrics", {}).get("inferred_edges", 0) for m in rca_built)
    rca_returned = rca_obs + rca_sup + rca_inf

    def ratio(num: int, den: int) -> float:
        if den == 0:
            return 0.0
        return num / den

    fault_counts = _seed_counts(machines, rca=False)
    algo_counts = _seed_counts(machines, rca=True)
    agreement_profile = {k: 0 for k in AGREEMENT_KEYS}

    cases = []
    for m in machines:
        if "scorecard" not in m:
            attach_scorecards(m)
        rca = m.get("rca_path") or {}
        rca_j = rca.get("judgment") or {}
        edges = (m.get("candidate_graph") or {}).get("edges") or []
        fault_nodes = m["judgment"].get("selected_path_nodes") or []
        rca_nodes = rca_j.get("selected_path_nodes") or []
        agree = path_agreement(
            m["judgment"]["status"], fault_nodes, rca_j.get("status"), rca_nodes
        )
        agreement_profile[agree] += 1
        tax = _case_injected_fault(m)
        cases.append(
            {
                "case_id": m["case_id"],
                "status": m["judgment"]["status"],
                "reason": m["judgment"].get("primary_rejection_reason"),
                "path": fault_nodes,
                "path_brief": _path_brief(m["judgment"], edges),
                "metrics": m["case_metrics"],
                "injection": ((m.get("reality") or {}).get("injection") or {}).get(
                    "component"
                ),
                "injected_fault": tax,
                "symptom": ((m.get("reality") or {}).get("symptom") or {}).get(
                    "component"
                ),
                "timeline": (m.get("reality") or {}).get("timeline") or [],
                "algo_rank1": (m.get("algo_context") or {}).get("rank1"),
                "algo_chain": (m.get("algo_context") or {}).get("predicted_chain") or [],
                "algo_hit_at_1": (m.get("algo_context") or {}).get("hit_at_1"),
                "algo_true_rank": (m.get("algo_context") or {}).get(
                    "true_label_best_rank"
                ),
                "algo_name": (m.get("algo_context") or {}).get("algo"),
                "algo_ac_at_1": (m.get("algo_context") or {}).get("algo_ac_at_1"),
                "rankings": (m.get("algo_context") or {}).get("rankings") or {},
                "scorecard": m.get("scorecard"),
                "scorecard_algo": rca.get("scorecard"),
                "rca_status": rca_j.get("status"),
                "rca_reason": rca_j.get("primary_rejection_reason"),
                "rca_path": rca_nodes,
                "rca_path_brief": _path_brief(rca_j, edges),
                "rca_algo": rca.get("algo"),
                "rca_seed": rca.get("seed"),
                "agreement": agree,
            }
        )

    return {
        "evaluated_cases": n,
        "constructed_cases": len(constructed),
        "rejected_cases": len(rejected),
        "path_coverage": ratio(len(constructed), n),
        "returned_edges": returned,
        "observed_edges": obs,
        "supported_edges": sup,
        "inferred_edges": inf,
        "observed_edge_ratio": ratio(obs, returned),
        "supported_edge_ratio": ratio(sup, returned),
        "inferred_edge_ratio": ratio(inf, returned),
        "rca_constructed_cases": len(rca_built),
        "rca_path_coverage": ratio(len(rca_built), n),
        "rca_observed_edges": rca_obs,
        "rca_supported_edges": rca_sup,
        "rca_inferred_edges": rca_inf,
        "rca_observed_edge_ratio": ratio(rca_obs, rca_returned),
        "rca_supported_edge_ratio": ratio(rca_sup, rca_returned),
        "rca_inferred_edge_ratio": ratio(rca_inf, rca_returned),
        "fault_counts": fault_counts,
        "algo_counts": algo_counts,
        "agreement_profile": agreement_profile,
        "injection_stratification": build_injection_stratification(machines),
        "rejection_profile": {
            reason: {
                "count": count,
                "rate": ratio(count, len(rejected)),
            }
            for reason, count in sorted(reasons.items())
        },
        "cases": cases,
    }


def summary_md(summary: dict, *, sample: str, policy: str) -> str:
    rca_cov = summary.get("rca_path_coverage") or 0.0
    lines = [
        f"# Evidence path — {sample} / {policy}",
        "",
        "| Measurement | Formula | Count | Result |",
        "|---|---|---:|---:|",
        (
            f"| Path Coverage (fault→symptom) | constructed / evaluated | "
            f"{summary['constructed_cases']} / {summary['evaluated_cases']} | "
            f"{100*summary['path_coverage']:.1f}% |"
        ),
        (
            f"| RCA Path Coverage (rank1→symptom) | rca constructed / evaluated | "
            f"{summary.get('rca_constructed_cases', 0)} / {summary['evaluated_cases']} | "
            f"{100*rca_cov:.1f}% |"
        ),
        (
            f"| Observed Edge Ratio | observed / returned edges | "
            f"{summary['observed_edges']} / {summary['returned_edges']} | "
            f"{100*summary['observed_edge_ratio']:.1f}% |"
        ),
        (
            f"| Supported Edge Ratio | supported / returned edges | "
            f"{summary['supported_edges']} / {summary['returned_edges']} | "
            f"{100*summary['supported_edge_ratio']:.1f}% |"
        ),
        (
            f"| Inferred Edge Ratio | inferred / returned edges | "
            f"{summary['inferred_edges']} / {summary['returned_edges']} | "
            f"{100*summary['inferred_edge_ratio']:.1f}% |"
        ),
        "",
        "## Rejection profile (fault seed)",
        "",
        "| Reason | Count | Rate among rejected |",
        "|---|---:|---:|",
    ]
    profile = summary.get("rejection_profile") or {}
    if not profile:
        lines.append("| (none) | 0 | 0.0% |")
    for reason, row in profile.items():
        lines.append(
            f"| {reason} | {row['count']} | {100*row['rate']:.1f}% |"
        )
    lines.append("")
    lines.append("Evidence levels describe availability, not causal correctness.")
    lines.append("")
    return "\n".join(lines)


def _pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def _refuse_count_rows(counts: dict) -> str:
    reasons = (counts or {}).get("refuse_reasons") or {}
    if not reasons:
        return "<tr><td colspan='2'>no refusals</td></tr>"
    return "".join(
        f"<tr><td>{html.escape(refuse_short(r))}</td><td>{n}</td></tr>"
        for r, n in sorted(reasons.items(), key=lambda kv: -kv[1])
    )


def _strat_dual_table(seed_tables: dict, *, title: str) -> str:
    inject = (seed_tables or {}).get("inject") or {}
    rca = (seed_tables or {}).get("rca") or {}
    keys = sorted(set(inject) | set(rca))
    if not keys:
        return f"<p class='muted'>No {html.escape(title)} rows.</p>"
    rows = []
    for key in keys:
        i = inject.get(key) or _strat_bucket()
        r = rca.get(key) or _strat_bucket()
        rows.append(
            "<tr>"
            f"<td>{html.escape(key)}</td>"
            f"<td>{i['accept']}</td><td>{i['refuse']}</td><td>{i['n']}</td>"
            f"<td>{r['accept']}</td><td>{r['refuse']}</td><td>{r['n']}</td>"
            "</tr>"
        )
    body = "".join(rows)
    return f"""
<table>
<thead><tr>
<th>{html.escape(title)}</th>
<th>Inject accept</th><th>Inject refuse</th><th>Inject n</th>
<th>RCA accept</th><th>RCA refuse</th><th>RCA n</th>
</tr></thead>
<tbody>{body}</tbody>
</table>
"""


def _injection_stratification_html(summary: dict) -> str:
    strat = summary.get("injection_stratification") or {}
    note = strat.get("note") or (
        "Stratified by injected fault (benchmark label) via OpenRCA 2.0 "
        "Tables 5–6 taxonomy lookup."
    )
    return f"""
<section>
<h2>Accept / refuse by injection taxonomy</h2>
<p class="muted">{html.escape(note)}</p>
<h3>By target layer (infra vs app)</h3>
{_strat_dual_table(strat.get("by_target_layer") or {{}}, title="target_layer")}
<h3>By fault kind (Table 6)</h3>
{_strat_dual_table(strat.get("by_fault_kind") or {{}}, title="fault_kind")}
<details>
<summary>By Chaos Mesh category (Table 5)</summary>
{_strat_dual_table(strat.get("by_category") or {{}}, title="category")}
</details>
</section>
"""


def _rqa_coverage_table(summary: dict, *, sample: str, policy: str) -> str:
    n = summary["evaluated_cases"]
    rows = [
        "<tr>"
        f"<td>{html.escape(policy)} (this run)</td>"
        f"<td>{summary['constructed_cases']}/{n}</td>"
        f"<td>{_pct(summary['path_coverage'])}</td>"
        f"<td>{summary.get('rca_constructed_cases', 0)}/{n}</td>"
        f"<td>{_pct(summary.get('rca_path_coverage') or 0.0)}</td>"
        "</tr>"
    ]
    sibling = summary.get("sibling_policy")
    if sibling:
        sn = sibling.get("evaluated_cases") or n
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(sibling.get('policy')))}</td>"
            f"<td>{sibling.get('constructed_cases', 0)}/{sn}</td>"
            f"<td>{_pct(sibling.get('path_coverage') or 0.0)}</td>"
            f"<td>{sibling.get('rca_constructed_cases', 0)}/{sn}</td>"
            f"<td>{_pct(sibling.get('rca_path_coverage') or 0.0)}</td>"
            "</tr>"
        )
        note = ""
    else:
        other = SIBLING_POLICY.get(policy, "sibling")
        note = (
            f"<p class='muted'>Sibling policy <code>{html.escape(other)}</code> "
            f"summary absent under <code>../{html.escape(other)}/</code> for "
            f"{html.escape(sample)}.</p>"
        )
    body = "".join(rows)
    return f"""
<table>
<thead><tr><th>Policy</th><th>Inject constructed</th><th>Inject cov</th>
<th>RCA constructed</th><th>RCA cov</th></tr></thead>
<tbody>{body}</tbody>
</table>
{note}
"""


def _queue_case_row(case: dict) -> str:
    cid = case["case_id"]
    agree = case.get("agreement") or "—"
    inject_ok = case.get("status") == "candidate_path_constructed"
    rca_ok = case.get("rca_status") == "candidate_path_constructed"
    inject_v = "path" if inject_ok else f"refuse — {refuse_short(case.get('reason'))}"
    rca_v = "path" if rca_ok else f"refuse — {refuse_short(case.get('rca_reason'))}"
    inject_strip = _path_strip_html(
        case.get("path"),
        refused=not inject_ok,
        refuse_reason=case.get("reason"),
    )
    rca_strip = _path_strip_html(
        case.get("rca_path"),
        refused=not rca_ok,
        refuse_reason=case.get("rca_reason"),
    )
    filter_keys = " ".join(
        key for key, tags in QUEUE_FILTER.items() if key != "all" and agree in tags
    )
    return (
        f"<article class='qrow' data-agree='{html.escape(agree)}' "
        f"data-filter='{html.escape(filter_keys)}'>"
        f"<div class='qhead'>"
        f"<a class='cid' href='{html.escape(cid)}/graph.html'>"
        f"{html.escape(cid)}</a>"
        f"<span class='agree'>{html.escape(agree)}</span>"
        f"</div>"
        f"<div class='qseed'><span class='lab'>Inject</span>"
        f"<span class='ver'>{html.escape(inject_v)}</span>{inject_strip}</div>"
        f"<div class='qseed'><span class='lab'>RCA</span>"
        f"<span class='ver'>{html.escape(rca_v)}</span>{rca_strip}</div>"
        f"</article>"
    )


def index_html(summary: dict, *, sample: str, policy: str) -> str:
    backfill_agreement(summary)
    profile = summary.get("agreement_profile") or {k: 0 for k in AGREEMENT_KEYS}
    cases = sorted(summary.get("cases") or [], key=_queue_sort_key)
    queue_rows = "".join(_queue_case_row(c) for c in cases) or (
        "<p class='muted'>No cases.</p>"
    )

    agree_tiles = "".join(
        f"<div class='tile'><div class='n'>{profile.get(k, 0)}</div>"
        f"<div class='l'>{html.escape(k)}</div></div>"
        for k in AGREEMENT_KEYS
    )
    fault_refuse = _refuse_count_rows(summary.get("fault_counts") or {})
    algo_refuse = _refuse_count_rows(summary.get("algo_counts") or {})

    perf_note = ""
    perf = summary.get("dataset_perf") or []
    if perf:
        top = perf[0]
        perf_note = (
            f"Seed ordering footnote: dataset AC@1 leader "
            f"<code>{html.escape(str(top.get('algorithm')))}</code> "
            f"({_pct(top.get('AC@1') or 0.0)}); full table in "
            f"<code>dataset.perf.parquet</code>."
        )

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Evidence dashboard — {html.escape(sample)}/{html.escape(policy)}</title>
<style>
:root {{ --bg:#f7f5f2; --ink:#1a1a1a; --muted:#666; --line:#ddd; --card:#fff; }}
body{{font-family:ui-sans-serif,system-ui,sans-serif;margin:0;background:var(--bg);color:var(--ink)}}
main{{max-width:1100px;margin:0 auto;padding:1.5rem}}
h1{{font-size:1.45rem;margin:0 0 .4rem}}
h2{{font-size:1.05rem;margin:1.2rem 0 .6rem;border-bottom:1px solid var(--line);padding-bottom:.3rem}}
.lead{{line-height:1.45;max-width:70ch}}
.filters{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}
.filters button{{background:var(--card);border:1px solid var(--line);padding:.35rem .7rem;cursor:pointer;font:inherit}}
.filters button.active{{border-color:#111;font-weight:600}}
.queue{{display:flex;flex-direction:column;gap:.75rem}}
.qrow{{background:var(--card);border:1px solid var(--line);padding:.85rem 1rem}}
.qrow.hidden{{display:none}}
.qhead{{display:flex;align-items:center;gap:.75rem;margin-bottom:.55rem;flex-wrap:wrap}}
.qhead .cid{{font-weight:600;color:#0b5;text-decoration:none}}
.agree{{font-size:.78rem;font-family:ui-monospace,monospace;border:1px solid var(--line);padding:.1rem .4rem}}
.qseed{{display:flex;align-items:center;gap:.55rem;margin:.35rem 0;flex-wrap:wrap}}
.qseed .lab{{min-width:3.2rem;font-size:.75rem;color:var(--muted);text-transform:uppercase}}
.qseed .ver{{font-size:.82rem;font-family:ui-monospace,monospace;min-width:5.5rem}}
.strip{{display:inline-flex;align-items:center;flex-wrap:wrap;gap:.2rem}}
.strip .hop{{background:#111;color:#fff;padding:.15rem .4rem;font-size:.78rem;border-radius:4px}}
.strip .tick{{display:inline-block;width:14px;height:0;border-top:3px solid #1b9e77}}
.strip .tick.dashed{{border-top-style:dashed;border-color:#d95f02}}
.strip.refuse{{color:#a45;font-family:ui-monospace,monospace;font-size:.82rem}}
.tiles{{display:grid;grid-template-columns:repeat(5,1fr);gap:.75rem;margin:1rem 0}}
.tile{{background:var(--card);border:1px solid var(--line);padding:1rem}}
.tile .n{{font-size:1.5rem;font-weight:700}}
.tile .l{{color:var(--muted);font-size:.85rem}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
@media(max-width:900px){{.tiles{{grid-template-columns:1fr 1fr}}.grid{{grid-template-columns:1fr}}}}
.card{{background:var(--card);border:1px solid var(--line);padding:1rem}}
table{{border-collapse:collapse;width:100%;font-size:.86rem;background:var(--card)}}
th,td{{border:1px solid var(--line);padding:.35rem .4rem;text-align:left;vertical-align:top}}
.muted{{color:var(--muted)}}
code{{font-size:.88em}}
details.eval{{margin:2rem 0 1rem;background:var(--card);border:1px solid var(--line);padding:.75rem 1rem}}
details.eval>summary{{cursor:pointer;font-weight:600}}
</style></head><body><main>
<h1>Investigation console — {html.escape(sample)} / {html.escape(policy)}</h1>
<p class="lead">Return a candidate propagation path with Observed / Supported /
Inferred labels and re-executable refs, or refuse with a named gap.
Paths are candidates under this policy, not causal ground truth.</p>

<nav class="filters" aria-label="Queue filter">
<button type="button" data-filter="all" class="active">all</button>
<button type="button" data-filter="differ">differ</button>
<button type="button" data-filter="refuse">refuse</button>
<button type="button" data-filter="same">same</button>
</nav>

<section id="queue">
<h2>Investigation queue</h2>
<p class="muted">Sorted: differ → one-sided refuse → same.</p>
<div class="queue">{queue_rows}</div>
</section>

<details class="eval">
<summary>Evaluation metrics (RQ-A / RQ-B / RQ-C)</summary>
<section>
<h2>RQ-A — coverage and policy</h2>
{_rqa_coverage_table(summary, sample=sample, policy=policy)}
<p class="muted">{perf_note}</p>
</section>
{_injection_stratification_html(summary)}
<section>
<h2>RQ-C — refuse both seeds</h2>
<div class="grid">
<div class="card">
<h3>Inject seed refusals</h3>
<table><thead><tr><th>Reason</th><th>n</th></tr></thead>
<tbody>{fault_refuse}</tbody></table>
</div>
<div class="card">
<h3>RCA seed refusals</h3>
<table><thead><tr><th>Reason</th><th>n</th></tr></thead>
<tbody>{algo_refuse}</tbody></table>
</div>
</div>
</section>
<section>
<h2>Agreement — inject vs RCA node lists</h2>
<p class="muted">Exact <code>selected_path_nodes</code> equality when both constructed.</p>
<div class="tiles">{agree_tiles}</div>
</section>
<section>
<h2>RQ-B — evidence composition (honesty)</h2>
<p>Fault-returned edges: Observed {_pct(summary['observed_edge_ratio'])},
Supported {_pct(summary['supported_edge_ratio'])},
Inferred {_pct(summary['inferred_edge_ratio'])}
({summary['observed_edges']}/{summary['supported_edges']}/{summary['inferred_edges']}
 of {summary['returned_edges']}).</p>
<p class="muted">Supported is empty when classifiers never emit it; temporal is often
<code>unknown</code>. Edge mix is availability, not a success metric.</p>
</section>
</details>
<script>
(function () {{
  var buttons = document.querySelectorAll('.filters button');
  var rows = document.querySelectorAll('.qrow');
  buttons.forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var key = btn.getAttribute('data-filter');
      buttons.forEach(function (b) {{ b.classList.toggle('active', b === btn); }});
      rows.forEach(function (row) {{
        var show = key === 'all' || (row.getAttribute('data-filter') || '').split(' ').indexOf(key) >= 0;
        row.classList.toggle('hidden', !show);
      }});
    }});
  }});
}})();
</script>
</main></body></html>
"""
