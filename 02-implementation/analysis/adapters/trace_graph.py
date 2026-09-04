"""Shared call-graph helpers. Moved out of chain_poc so ground_truth can import them."""

from __future__ import annotations

import re

import pandas as pd

GENERIC_VERB_SPANS = {"GET", "POST", "PUT", "DELETE", "PATCH"}
SQL_PATTERN = re.compile(r"^\s*(SELECT|INSERT|UPDATE|DELETE)\b", re.IGNORECASE)
RELAXED_DURATION_MULTIPLIER = 3.0


def build_call_graph(df: pd.DataFrame) -> set:
    id2svc = dict(zip(df.span_id, df.service_name))
    edges = set()
    for parent, svc in zip(df.parent_span_id, df.service_name):
        parent_svc = id2svc.get(parent)
        if parent_svc is None or parent_svc == svc:
            continue
        edges.add((parent_svc, svc))
    return edges


def call_pair_stats(
    df: pd.DataFrame, *, max_traces: int = 3, max_routes: int = 2
) -> dict[tuple[str, str], dict]:
    """Per (caller, callee) counts, errors, sample trace_ids, top span names."""
    need = {"span_id", "parent_span_id", "service_name"}
    if df.empty or not need.issubset(df.columns):
        return {}

    parents = df[["span_id", "service_name"]].rename(
        columns={"span_id": "parent_span_id", "service_name": "caller"}
    )
    cols = ["parent_span_id", "service_name"]
    for optional in ("span_name", "attr.status_code", "trace_id"):
        if optional in df.columns:
            cols.append(optional)
    merged = df[cols].merge(parents, on="parent_span_id", how="inner")
    cross = merged[merged["caller"] != merged["service_name"]]
    if cross.empty:
        return {}

    out: dict[tuple[str, str], dict] = {}
    grouped = cross.groupby(["caller", "service_name"], sort=False)
    for (caller, callee), grp in grouped:
        routes: list[str] = []
        if "span_name" in grp.columns:
            ranked = grp["span_name"].dropna().astype(str).value_counts()
            routes = [str(n) for n in ranked.index[:max_routes]]
        errors = 0
        if "attr.status_code" in grp.columns:
            errors = int((grp["attr.status_code"] == "Error").sum())
        traces: list[str] = []
        if "trace_id" in grp.columns:
            traces = [str(t) for t in grp["trace_id"].dropna().astype(str).unique()[:max_traces]]
        out[(str(caller), str(callee))] = {
            "call_count": int(len(grp)),
            "error_count": errors,
            "trace_ids": traces,
            "span_names": routes,
        }
    return out


def connected_component(scope: pd.DataFrame, seed_span_ids: set) -> pd.DataFrame:
    """Keep only the parent/child tree(s) of the seed spans. trace_id alone is too loose."""
    span_ids = scope["span_id"].tolist()
    parent_ids = scope["parent_span_id"].tolist()
    id2parent = dict(zip(span_ids, parent_ids))
    children: dict = {}
    for sid, pid in zip(span_ids, parent_ids):
        if not pid:
            continue
        children.setdefault(pid, set()).add(sid)

    component: set = set()
    frontier = set(seed_span_ids)
    while frontier:
        sid = frontier.pop()
        if sid in component:
            continue
        component.add(sid)
        pid = id2parent.get(sid)
        if pid and pid not in component:
            frontier.add(pid)
        for child in children.get(sid, ()):
            if child not in component:
                frontier.add(child)
    return scope[scope["span_id"].isin(component)]


def try_sql_bridge(incident: pd.DataFrame, relaxed: bool = False) -> dict | None:
    sql_spans = incident[incident["span_name"].str.match(SQL_PATTERN, na=False)]
    mode = "sql-bridge"
    if sql_spans.empty and not relaxed:
        return None
    if sql_spans.empty:
        sql_spans = incident[incident.get("attr.span_kind") == "Client"]
        mode = "client-span-bridge-relaxed"
    if sql_spans.empty:
        return None

    id2svc = dict(zip(incident.span_id, incident.service_name))
    sql_spans = sql_spans.copy()
    sql_spans["caller_svc"] = sql_spans["parent_span_id"].map(id2svc)
    sql_spans = sql_spans.dropna(subset=["caller_svc"])
    if sql_spans.empty:
        return None

    first = sql_spans.sort_values("time").iloc[0]
    kind = "SQL-shaped" if mode == "sql-bridge" else "Client-kind"
    return {
        "mode": mode,
        "bridge_caller": first["caller_svc"],
        "onset_time": first["time"],
        "origin_span_id": first["span_id"],
        "evidence": (
            f"{kind} span {first['span_name']!r} issued by {first['caller_svc']} "
            f"(status={first.get('attr.status_code')})"
        ),
    }


def _anomalous_leaf_mask(
    candset: pd.DataFrame, normal_traces: pd.DataFrame
) -> pd.Series:
    baseline = normal_traces.groupby(["service_name", "span_name"])["duration"].mean()

    def is_anomalous_leaf(row) -> bool:
        if row.get("attr.status_code") == "Error":
            return True
        base = baseline.get((row["service_name"], row["span_name"]))
        if base is None or base <= 0:
            return False
        return row["duration"] >= RELAXED_DURATION_MULTIPLIER * base

    return candset.apply(is_anomalous_leaf, axis=1)


def try_dangling_leaf_bridge(
    candidate: str,
    incident: pd.DataFrame,
    normal_traces: pd.DataFrame,
    relaxed: bool = False,
) -> dict | None:
    normal_edges = build_call_graph(normal_traces)
    normal_callers: dict = {}
    for caller, callee in normal_edges:
        normal_callers.setdefault(callee, set()).add(caller)
    callers_of_candidate = normal_callers.get(candidate, set())
    if not callers_of_candidate:
        return None

    ids_as_parent = set(incident["parent_span_id"].dropna())
    leaf_mask = ~incident["span_id"].isin(ids_as_parent)
    caller_mask = incident["service_name"].isin(callers_of_candidate)

    if not relaxed:
        verb_mask = incident["span_name"].isin(GENERIC_VERB_SPANS)
        err_mask = incident["attr.status_code"] == "Error"
        dangling = incident[leaf_mask & verb_mask & err_mask & caller_mask]
        mode = "dangling-leaf-bridge"
    else:
        candset = incident[leaf_mask & caller_mask]
        if candset.empty:
            return None
        dangling = candset[_anomalous_leaf_mask(candset, normal_traces)]
        mode = "dangling-leaf-bridge-relaxed"

    if dangling.empty:
        return None

    first = dangling.sort_values("time").iloc[0]
    reason = (
        "Error status"
        if first.get("attr.status_code") == "Error"
        else f">= {RELAXED_DURATION_MULTIPLIER:.0f}x normal mean duration"
    )
    return {
        "mode": mode,
        "bridge_caller": first["service_name"],
        "onset_time": first["time"],
        "origin_span_id": first["span_id"],
        "evidence": (
            f"Dangling {first['span_name']} leaf on {first['service_name']} ({reason}), "
            f"normal caller of {candidate}"
        ),
    }


def is_untraced_globally(candidate: str, *trace_frames: pd.DataFrame) -> bool:
    return not any((df["service_name"] == candidate).any() for df in trace_frames)
