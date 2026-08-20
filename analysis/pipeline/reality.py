"""Reality layer: injection facts, symptom policy, timeline, placement attrs."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from ground_truth import injected_targets

from .fault_taxonomy import taxonomy_public

REQUIRED_FILES = (
    "injection.json",
    "conclusion.parquet",
    "abnormal_traces.parquet",
    "normal_traces.parquet",
)

HOST_RE = re.compile(r"https?://([^:/]+)")


def _has_issue(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in ("", "{}")
    if isinstance(value, dict):
        return len(value) > 0
    try:
        return len(value) > 0
    except TypeError:
        return bool(value)


def validate_case_dir(case_dir: Path) -> str | None:
    if not case_dir.is_dir():
        return "unsupported_case_schema"
    for name in REQUIRED_FILES:
        if not (case_dir / name).exists():
            return "unsupported_case_schema"
    return None


def read_injection(case_dir: Path) -> dict | str:
    path = case_dir / "injection.json"
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return f"injection read failed: {exc}"
    targets = injected_targets(payload)
    if not targets:
        return "injected_component_unavailable"
    start = payload.get("start_time")
    end = payload.get("end_time")
    return {
        "component": targets[0],
        "all_targets": targets,
        "fault_type": payload.get("fault_type"),
        "injection_name": payload.get("injection_name") or case_dir.name,
        "start_time": start,
        "end_time": end,
        "raw": payload,
    }


def _host_from_span_name(span_name: str) -> str | None:
    match = HOST_RE.search(span_name)
    if not match:
        return None
    return match.group(1)


def _rank_key(row: pd.Series) -> tuple:
    normal_succ = float(row.get("NormalSuccRate") or 0.0)
    abnormal_succ = float(row.get("AbnormalSuccRate") or 0.0)
    succ_drop = normal_succ - abnormal_succ
    normal_dur = float(row.get("NormalAvgDuration") or 0.0)
    abnormal_dur = float(row.get("AbnormalAvgDuration") or 0.0)
    if normal_dur > 0:
        duration_ratio = abnormal_dur / normal_dur
    else:
        duration_ratio = abnormal_dur
    return (-succ_drop, -duration_ratio, str(row.get("SpanName") or ""))


def select_symptom(case_dir: Path, rules: dict) -> dict | None:
    policy = rules.get("symptom_policy") or {}
    exclude = {s.lower() for s in policy.get("exclude_services") or []}
    conclusion = pd.read_parquet(case_dir / "conclusion.parquet")
    if conclusion.empty or "SpanName" not in conclusion.columns:
        return None

    stages = []
    primary = policy.get("primary") or {}
    fallback = policy.get("fallback") or {}
    if primary:
        stages.append(("primary", primary))
    if fallback:
        stages.append(("fallback", fallback))

    for stage_name, stage in stages:
        rows = conclusion
        if stage.get("require_issues"):
            rows = conclusion[conclusion["Issues"].apply(_has_issue)]
        if rows.empty:
            continue
        ordered = sorted((row for _, row in rows.iterrows()), key=_rank_key)
        for row in ordered:
            host = _host_from_span_name(str(row["SpanName"]))
            if not host or host.lower() in exclude:
                continue
            return {
                "component": host,
                "span_name": str(row["SpanName"]),
                "source": "conclusion.parquet",
                "selection_rule": f"{policy.get('id', 'policy')}:{stage_name}",
                "succ_drop": float(row.get("NormalSuccRate") or 0)
                - float(row.get("AbnormalSuccRate") or 0),
            }
    return None


def load_traces(case_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    cols = [
        "time",
        "trace_id",
        "span_id",
        "parent_span_id",
        "span_name",
        "attr.span_kind",
        "service_name",
        "duration",
        "attr.status_code",
        "attr.k8s.pod.name",
        "attr.k8s.service.name",
        "attr.k8s.namespace.name",
    ]
    abnormal = pd.read_parquet(case_dir / "abnormal_traces.parquet")
    normal = pd.read_parquet(case_dir / "normal_traces.parquet")
    keep_a = [c for c in cols if c in abnormal.columns]
    keep_n = [c for c in cols if c in normal.columns]
    return abnormal[keep_a], normal[keep_n]


def placement_facts(abnormal_traces: pd.DataFrame, case_dir: Path) -> dict:
    """Vertical placement only from attributes actually present."""
    pod_to_service: dict[str, str] = {}
    if "attr.k8s.pod.name" in abnormal_traces.columns:
        for pod, svc in zip(
            abnormal_traces["attr.k8s.pod.name"],
            abnormal_traces["service_name"],
        ):
            if pd.isna(pod) or not pod:
                continue
            pod_to_service.setdefault(str(pod), str(svc))

    node_to_pod: dict[str, set[str]] = {}
    pod_to_container: dict[str, set[str]] = {}
    metrics_path = case_dir / "abnormal_metrics.parquet"
    if metrics_path.exists():
        mcols = [
            "attr.k8s.node.name",
            "attr.k8s.pod.name",
            "attr.k8s.container.name",
        ]
        metrics = pd.read_parquet(metrics_path, columns=mcols)
        for _, row in metrics.dropna(subset=["attr.k8s.pod.name"]).iterrows():
            pod = str(row["attr.k8s.pod.name"])
            node = row.get("attr.k8s.node.name")
            container = row.get("attr.k8s.container.name")
            if node and not pd.isna(node):
                node_to_pod.setdefault(str(node), set()).add(pod)
            if container and not pd.isna(container):
                pod_to_container.setdefault(pod, set()).add(str(container))

    return {
        "pod_to_service": pod_to_service,
        "node_to_pods": {k: sorted(v) for k, v in node_to_pod.items()},
        "pod_to_containers": {k: sorted(v) for k, v in pod_to_container.items()},
    }


def _ts_sort_key(timestamp: str | None) -> tuple:
    text = str(timestamp or "")
    if not text:
        return (1, "")
    try:
        return (0, str(pd.Timestamp(text)))
    except (ValueError, TypeError):
        return (0, text)


def _first_error_row(abnormal_traces: pd.DataFrame, service: str | None = None):
    if abnormal_traces.empty or "time" not in abnormal_traces.columns:
        return None
    scoped = abnormal_traces
    if service is not None:
        scoped = abnormal_traces[abnormal_traces["service_name"] == service]
    if "attr.status_code" in scoped.columns:
        err = scoped[scoped["attr.status_code"] == "Error"]
        if not err.empty:
            return err.sort_values("time").iloc[0]
    if scoped.empty:
        return None
    return scoped.sort_values("time").iloc[0]


def build_timeline(
    injection: dict,
    symptom: dict,
    abnormal_traces: pd.DataFrame,
) -> list[dict]:
    """Sparse case anchors only — not a full incident timeline."""
    events: list[dict] = []
    if injection.get("start_time"):
        events.append(
            {
                "timestamp": str(injection["start_time"]),
                "component": injection["component"],
                "entity_type": "service",
                "event_type": "injection_start",
                "source": "injection.json",
                "evidence_ref": "injection_facts",
                "note": "fault injection window start",
            }
        )
    if injection.get("end_time"):
        events.append(
            {
                "timestamp": str(injection["end_time"]),
                "component": injection["component"],
                "entity_type": "service",
                "event_type": "injection_end",
                "source": "injection.json",
                "evidence_ref": "injection_facts",
                "note": "fault injection window end",
            }
        )

    first = _first_error_row(abnormal_traces)
    if first is not None and first.get("attr.status_code") == "Error":
        events.append(
            {
                "timestamp": str(first["time"]),
                "component": str(first["service_name"]),
                "entity_type": "service",
                "event_type": "first_error_span",
                "source": "abnormal_traces.parquet",
                "evidence_ref": "timeline_first_error",
                "note": "earliest Error span in abnormal window (any service)",
            }
        )

    # conclusion.parquet has no selection clock; use first Error (else first span)
    # on the symptom service in the abnormal window when present.
    symptom_row = _first_error_row(abnormal_traces, symptom["component"])
    if symptom_row is not None:
        is_error = (
            "attr.status_code" in symptom_row.index
            and symptom_row.get("attr.status_code") == "Error"
        )
        events.append(
            {
                "timestamp": str(symptom_row["time"]),
                "component": symptom["component"],
                "entity_type": "service",
                "event_type": "selected_symptom",
                "source": "abnormal_traces.parquet",
                "evidence_ref": "symptom_selection",
                "note": (
                    "first Error span on symptom service"
                    if is_error
                    else "first span on symptom service (no Error); policy pick has no clock"
                ),
                "span_name": (
                    str(symptom_row["span_name"])
                    if "span_name" in symptom_row.index
                    else symptom.get("span_name")
                ),
            }
        )
    else:
        events.append(
            {
                "timestamp": "",
                "component": symptom["component"],
                "entity_type": "service",
                "event_type": "selected_symptom",
                "source": symptom["source"],
                "evidence_ref": "symptom_selection",
                "note": (
                    "policy-selected symptom; no span clock "
                    f"({symptom.get('span_name') or 'no span_name'})"
                ),
            }
        )

    events.sort(key=lambda e: _ts_sort_key(e.get("timestamp")))
    return events


def enrich_timeline_path_errors(
    timeline: list[dict],
    abnormal_traces: pd.DataFrame | None,
    path_nodes: list[str] | None,
) -> list[dict]:
    """Add first Error per accepted-path service when cheaply available."""
    if not path_nodes or abnormal_traces is None or abnormal_traces.empty:
        return timeline
    if "attr.status_code" not in abnormal_traces.columns:
        return timeline

    existing = {
        (ev.get("event_type"), ev.get("component"))
        for ev in timeline
    }
    extra: list[dict] = []
    for node in path_nodes:
        key = ("path_first_error", node)
        if key in existing or ("first_error_span", node) in existing:
            continue
        row = _first_error_row(abnormal_traces, node)
        if row is None or row.get("attr.status_code") != "Error":
            continue
        extra.append(
            {
                "timestamp": str(row["time"]),
                "component": node,
                "entity_type": "service",
                "event_type": "path_first_error",
                "source": "abnormal_traces.parquet",
                "evidence_ref": "timeline_path_first_error",
                "note": "first Error span on accepted-path service",
            }
        )
    if not extra:
        return timeline
    merged = list(timeline) + extra
    merged.sort(key=lambda e: _ts_sort_key(e.get("timestamp")))
    return merged


def build_reality(case_dir: Path, rules: dict) -> dict | str:
    schema_err = validate_case_dir(case_dir)
    if schema_err:
        return schema_err

    injection = read_injection(case_dir)
    if isinstance(injection, str):
        return injection

    symptom = select_symptom(case_dir, rules)
    if not symptom:
        return "symptom_unavailable"

    abnormal, normal = load_traces(case_dir)
    placement = placement_facts(abnormal, case_dir)
    services = sorted(set(abnormal["service_name"].dropna().astype(str)))
    timeline = build_timeline(injection, symptom, abnormal)
    tax = taxonomy_public(injection["fault_type"])
    return {
        "injection": {
            "component": injection["component"],
            "fault_type": injection["fault_type"],
            "start_time": injection["start_time"],
            "end_time": injection["end_time"],
            "injection_name": injection["injection_name"],
            "injected_fault": tax,
        },
        "symptom": {
            "component": symptom["component"],
            "span_name": symptom["span_name"],
            "source": symptom["source"],
            "selection_rule": symptom["selection_rule"],
        },
        "services_in_abnormal_traces": services,
        "placement": placement,
        "timeline": timeline,
        "_frames": {"abnormal": abnormal, "normal": normal},
    }
