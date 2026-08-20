"""Evidence queries, registry, and Observed/Supported/Inferred classification."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pandas as pd

from trace_graph import call_pair_stats

MAX_STAT_HITS = 3


def _hash_payload(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _metric_family(metric: str, checks: dict) -> str:
    lower = metric.lower()
    for kind, key in (
        ("latency", "latency_metric_substrings"),
        ("count", "count_metric_substrings"),
        ("gauge", "gauge_metric_substrings"),
    ):
        for needle in checks.get(key) or []:
            if needle.lower() in lower:
                return kind
    return "gauge"


def _round_num(value: float | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 4)


def service_abnormal(
    case_dir,
    service: str,
    rules: dict,
    registry: list[dict],
    *,
    metric_frames: tuple[pd.DataFrame, pd.DataFrame] | None = None,
) -> tuple[str, list[str], dict]:
    """Return (pass|fail|unknown, evidence_ids, summary) for endpoint abnormality."""
    checks = (rules.get("checks") or {}).get("statistical") or {}
    if metric_frames is None:
        path = case_dir / "abnormal_metrics.parquet"
        normal_path = case_dir / "normal_metrics.parquet"
        if not path.exists() or not normal_path.exists():
            return "unknown", [], {}
        cols = ["metric", "value", "service_name"]
        abnormal = pd.read_parquet(path, columns=cols)
        normal = pd.read_parquet(normal_path, columns=cols)
    else:
        abnormal, normal = metric_frames

    a = abnormal[abnormal["service_name"] == service]
    n = normal[normal["service_name"] == service]
    if a.empty or n.empty:
        return _trace_error_check(case_dir, service, registry)

    hits: list[dict] = []
    n_compared = 0
    for metric, grp_n in n.groupby("metric"):
        family = _metric_family(str(metric), checks)
        vals_n = grp_n["value"].dropna()
        vals_a = a[a["metric"] == metric]["value"].dropna()
        if vals_n.empty or vals_a.empty:
            continue
        n_compared += 1
        eps = float(checks.get("epsilon") or 1e-6)
        mean_n = float(vals_n.mean())
        std_n = float(vals_n.std() or 0.0)
        mean_a = float(vals_a.mean())
        hit: dict | None = None
        if family == "latency":
            mult = float(checks.get("latency_multiplier") or 3.0)
            if mean_n > 0 and mean_a >= mult * mean_n:
                hit = {
                    "metric": str(metric),
                    "family": family,
                    "normal_mean": _round_num(mean_n),
                    "abnormal_mean": _round_num(mean_a),
                    "ratio": _round_num(mean_a / mean_n),
                }
        elif family == "count":
            p = float(checks.get("count_percentile") or 99.0)
            base = float(vals_n.quantile(p / 100.0))
            mult = float(checks.get("count_multiplier_vs_p99") or 2.0)
            if mean_a > max(base, mult * max(base, eps)):
                hit = {
                    "metric": str(metric),
                    "family": family,
                    "normal_mean": _round_num(mean_n),
                    "abnormal_mean": _round_num(mean_a),
                    "p99": _round_num(base),
                }
        else:
            z = (mean_a - mean_n) / max(std_n, eps)
            if abs(z) >= float(checks.get("gauge_zscore_threshold") or 3.0):
                hit = {
                    "metric": str(metric),
                    "family": family,
                    "normal_mean": _round_num(mean_n),
                    "abnormal_mean": _round_num(mean_a),
                    "z": _round_num(z),
                }
        if hit:
            hits.append(hit)

    hits = hits[:MAX_STAT_HITS]
    summary = {"n_compared": n_compared, "hits": hits, "source": "metrics"}
    eid = f"stat_{service}"
    registry.append(
        {
            "evidence_id": eid,
            "source_file": "abnormal_metrics.parquet",
            "query": (
                f"compare normal vs abnormal metrics for service_name={service!r}"
            ),
            "row_count": n_compared,
            "result_hash": _hash_payload(
                {"service": service, "hits": [h["metric"] for h in hits]}
            ),
            "claim": (
                f"{service} shows {len(hits)} abnormal metric signal(s)"
                if hits
                else f"{service} has no metric deviation under configured thresholds"
            ),
            "detail": summary,
        }
    )
    if hits:
        return "pass", [eid], summary
    if n_compared:
        return "fail", [eid], summary
    return _trace_error_check(case_dir, service, registry)


def _trace_error_check(case_dir, service: str, registry: list[dict]) -> tuple[str, list[str], dict]:
    path = case_dir / "abnormal_traces.parquet"
    if not path.exists():
        return "unknown", [], {}
    df = pd.read_parquet(
        path, columns=["service_name", "attr.status_code", "duration"]
    )
    scoped = df[df["service_name"] == service]
    if scoped.empty:
        eid = f"trace_absent_{service}"
        summary = {"source": "traces", "errors": 0, "spans": 0}
        registry.append(
            {
                "evidence_id": eid,
                "source_file": "abnormal_traces.parquet",
                "query": f"spans where service_name={service!r}",
                "row_count": 0,
                "result_hash": _hash_payload({"service": service, "rows": 0}),
                "claim": f"{service} emits no abnormal-window spans",
                "detail": summary,
            }
        )
        return "unknown", [eid], summary
    errors = scoped[scoped["attr.status_code"] == "Error"]
    eid = f"trace_err_{service}"
    summary = {
        "source": "traces",
        "errors": int(len(errors)),
        "spans": int(len(scoped)),
    }
    registry.append(
        {
            "evidence_id": eid,
            "source_file": "abnormal_traces.parquet",
            "query": (
                f"count Error spans for service_name={service!r}"
            ),
            "row_count": int(len(errors)),
            "result_hash": _hash_payload(
                {"service": service, "errors": int(len(errors)), "n": int(len(scoped))}
            ),
            "claim": (
                f"{service} has {len(errors)} Error spans of {len(scoped)}"
            ),
            "detail": summary,
        }
    )
    if len(errors) > 0:
        return "pass", [eid], summary
    return "fail", [eid], summary


def structural_check(
    edge_meta: dict,
    src: str,
    dst: str,
    registry: list[dict],
    *,
    hop_struct: dict | None = None,
) -> tuple[str, list[str]]:
    eid = f"struct_{src}__{dst}"
    in_abn = bool(edge_meta.get("in_abnormal"))
    in_norm = bool(edge_meta.get("in_normal"))
    detail = hop_struct or {}
    registry.append(
        {
            "evidence_id": eid,
            "source_file": "abnormal_traces.parquet",
            "query": (
                f"parent-child service edge call={edge_meta.get('call_direction')} "
                f"propagation=({src}->{dst})"
            ),
            "row_count": int(detail.get("call_count") or (int(in_abn) + int(in_norm))),
            "result_hash": _hash_payload(
                {
                    "src": src,
                    "dst": dst,
                    "in_abnormal": in_abn,
                    "in_normal": in_norm,
                    "call_count": detail.get("call_count"),
                }
            ),
            "claim": (
                "Direct abnormal-window parent-child relationship"
                if in_abn
                else (
                    "Dependency present only in normal window"
                    if in_norm
                    else "No parent-child relationship in traces"
                )
            ),
            "detail": detail,
        }
    )
    if in_abn:
        return "pass", [eid]
    if in_norm:
        return "fail", [eid]
    return "fail", [eid]


def temporal_check(
    src: str,
    dst: str,
    reality: dict,
    registry: list[dict],
) -> tuple[str, list[str]]:
    """Onset ordering often unavailable at this resolution → unknown."""
    eid = f"temp_{src}__{dst}"
    registry.append(
        {
            "evidence_id": eid,
            "source_file": "abnormal_traces.parquet",
            "query": f"onset order between {src} and {dst}",
            "row_count": 0,
            "result_hash": _hash_payload({"src": src, "dst": dst, "status": "unknown"}),
            "claim": (
                "Temporal ordering left unknown; timing alone cannot prove causality"
            ),
        }
    )
    return "unknown", [eid]


def classify_edge(checks: dict[str, str], rules: dict, *, both_incident: bool) -> tuple[str, list[str]]:
    missing: list[str] = []
    observed = (rules.get("classification") or {}).get("observed") or {}
    if (
        checks.get("structural") == observed.get("structural", "pass")
        and checks.get("statistical") == observed.get("statistical", "pass")
        and both_incident
        and checks.get("temporal") in (observed.get("temporal_may_be") or ["pass", "unknown"])
    ):
        return "observed", missing

    supported = (rules.get("classification") or {}).get("supported") or {}
    pass_count = sum(1 for v in checks.values() if v == "pass")
    if pass_count >= int(supported.get("min_pass_checks", 2)):
        if checks.get("structural") in (supported.get("structural_may_be") or ["pass", "fail"]):
            return "supported", missing

    if checks.get("structural") != "pass":
        missing.append("direct_abnormal_parent_child_relationship")
    if checks.get("statistical") != "pass":
        missing.append("statistical_deviation_at_both_endpoints")
    if checks.get("temporal") == "unknown":
        missing.append("usable_temporal_onset_ordering")
    if not both_incident:
        missing.append("incident_evidence_at_both_endpoints")
    return "inferred", missing


def _hop_from_call(
    call_dir: dict | None,
    pair_stats: dict[tuple[str, str], dict],
) -> dict:
    if not call_dir:
        return {}
    caller = call_dir.get("source")
    callee = call_dir.get("target")
    if not caller or not callee:
        return {}
    return dict(pair_stats.get((str(caller), str(callee))) or {})


def _endpoint_stat_brief(verdict: str, summary: dict) -> dict:
    brief = {"verdict": verdict, "source": summary.get("source")}
    hits = summary.get("hits") or []
    if hits:
        brief["hits"] = hits
        return brief
    if summary.get("source") == "traces":
        brief["errors"] = summary.get("errors")
        brief["spans"] = summary.get("spans")
    elif summary.get("n_compared") is not None:
        brief["n_compared"] = summary.get("n_compared")
        brief["hits"] = []
    return brief


def annotate_paths(
    case_dir,
    reality: dict,
    graph: dict,
    rules: dict,
) -> dict:
    registry: list[dict] = [
        {
            "evidence_id": "injection_facts",
            "source_file": "injection.json",
            "query": "read injection component/fault/window",
            "row_count": 1,
            "result_hash": _hash_payload(reality["injection"]),
            "claim": f"Injection at {reality['injection']['component']}",
        },
        {
            "evidence_id": "symptom_selection",
            "source_file": "conclusion.parquet",
            "query": "select symptom by frozen policy",
            "row_count": 1,
            "result_hash": _hash_payload(reality["symptom"]),
            "claim": f"Symptom at {reality['symptom']['component']}",
        },
    ]

    incident_cache: dict[str, tuple[str, list[str], dict]] = {}
    edge_records: dict[tuple[str, str], dict] = {}
    all_edge_metas = {**graph["horizontal"], **graph["vertical"]}

    metric_frames = None
    m_abn = case_dir / "abnormal_metrics.parquet"
    m_nrm = case_dir / "normal_metrics.parquet"
    if m_abn.exists() and m_nrm.exists():
        cols = ["metric", "value", "service_name"]
        metric_frames = (
            pd.read_parquet(m_abn, columns=cols),
            pd.read_parquet(m_nrm, columns=cols),
        )

    frames = reality.get("_frames") or {}
    abn_frame = frames.get("abnormal")
    if abn_frame is None:
        abn_frame = pd.DataFrame()
    pair_stats = call_pair_stats(abn_frame)

    def ensure_edge(src: str, dst: str) -> dict:
        key = (src, dst)
        if key in edge_records:
            return edge_records[key]
        meta = all_edge_metas.get(key)
        if meta is None:
            meta = {
                "channel": "horizontal",
                "call_direction": {"source": dst, "target": src},
                "candidate_propagation_direction": {"source": src, "target": dst},
                "direction_reason": "synthetic bridge; no span evidence",
                "in_abnormal": False,
                "in_normal": False,
            }
        hop_struct = _hop_from_call(meta.get("call_direction"), pair_stats)
        struct, srefs = structural_check(
            meta, src, dst, registry, hop_struct=hop_struct
        )
        for node in (src, dst):
            if node not in incident_cache:
                incident_cache[node] = service_abnormal(
                    case_dir, node, rules, registry, metric_frames=metric_frames
                )
        src_stat, src_refs, src_sum = incident_cache[src]
        dst_stat, dst_refs, dst_sum = incident_cache[dst]
        if src_stat == "pass" and dst_stat == "pass":
            statistical = "pass"
        elif src_stat == "unknown" or dst_stat == "unknown":
            statistical = "unknown"
        else:
            statistical = "fail"
        temporal, trefs = temporal_check(src, dst, reality, registry)
        checks = {
            "structural": struct,
            "statistical": statistical,
            "temporal": temporal,
        }
        both = src_stat == "pass" and dst_stat == "pass"
        level, missing = classify_edge(checks, rules, both_incident=both)
        edge_id = f"e_{src}__{dst}"
        route = (hop_struct.get("span_names") or [None])[0]
        edge_records[key] = {
            "edge_id": edge_id,
            "source": src,
            "target": dst,
            "channel": meta["channel"],
            "call_direction": meta["call_direction"],
            "candidate_propagation_direction": meta["candidate_propagation_direction"],
            "direction_reason": meta["direction_reason"],
            "evidence_level": level,
            "evidence_refs": sorted(set(srefs + src_refs + dst_refs + trefs)),
            "checks": checks,
            "missing_evidence": missing,
            "hop": {
                "route": route,
                "span_names": hop_struct.get("span_names") or [],
                "call_count": hop_struct.get("call_count"),
                "error_count": hop_struct.get("error_count"),
                "trace_ids": hop_struct.get("trace_ids") or [],
                "in_abnormal": bool(meta.get("in_abnormal")),
                "in_normal": bool(meta.get("in_normal")),
                "stat": {
                    "source": _endpoint_stat_brief(src_stat, src_sum),
                    "target": _endpoint_stat_brief(dst_stat, dst_sum),
                },
            },
        }
        return edge_records[key]

    annotated_paths = []
    for path in graph["candidate_paths"]:
        path_edges = []
        for a, b in zip(path, path[1:]):
            path_edges.append(ensure_edge(a, b))
        annotated_paths.append({"nodes": path, "edges": path_edges})

    # Vertical placement edges: structural presence only (not on path search).
    for (src, dst), meta in graph["vertical"].items():
        if (src, dst) in edge_records:
            continue
        struct, srefs = structural_check(meta, src, dst, registry)
        level = "observed" if struct == "pass" else "inferred"
        missing = [] if level == "observed" else ["incident_evidence_at_infra_endpoints"]
        edge_records[(src, dst)] = {
            "edge_id": f"e_{src}__{dst}",
            "source": src,
            "target": dst,
            "channel": "vertical",
            "call_direction": meta["call_direction"],
            "candidate_propagation_direction": meta["candidate_propagation_direction"],
            "direction_reason": meta["direction_reason"],
            "evidence_level": level,
            "evidence_refs": srefs,
            "checks": {
                "structural": struct,
                "statistical": "unknown",
                "temporal": "unknown",
            },
            "missing_evidence": missing,
            "hop": {
                "route": None,
                "span_names": [],
                "call_count": None,
                "error_count": None,
                "trace_ids": [],
                "in_abnormal": bool(meta.get("in_abnormal")),
                "in_normal": bool(meta.get("in_normal")),
                "stat": {},
            },
        }

    return {
        "edges": list(edge_records.values()),
        "annotated_paths": annotated_paths,
        "evidence_registry": registry,
    }
