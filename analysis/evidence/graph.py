"""Candidate graph: horizontal span edges, vertical placement, bounded paths."""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from trace_graph import build_call_graph


def horizontal_edges(
    abnormal: pd.DataFrame, normal: pd.DataFrame
) -> tuple[dict[tuple[str, str], dict], set[tuple[str, str]]]:
    """Propagation direction is callee→caller (effect travels upstream)."""
    abnormal_calls = build_call_graph(abnormal)
    normal_calls = build_call_graph(normal)
    edges: dict[tuple[str, str], dict] = {}
    for caller, callee in abnormal_calls:
        prop = (callee, caller)
        edges[prop] = {
            "channel": "horizontal",
            "call_direction": {"source": caller, "target": callee},
            "candidate_propagation_direction": {"source": callee, "target": caller},
            "direction_reason": "RPC effect propagates from callee to caller",
            "in_abnormal": True,
            "in_normal": (caller, callee) in normal_calls,
        }
    for caller, callee in normal_calls:
        prop = (callee, caller)
        if prop in edges:
            continue
        edges[prop] = {
            "channel": "horizontal",
            "call_direction": {"source": caller, "target": callee},
            "candidate_propagation_direction": {"source": callee, "target": caller},
            "direction_reason": "RPC effect direction from normal-window dependency only",
            "in_abnormal": False,
            "in_normal": True,
        }
    return edges, abnormal_calls


def vertical_edges(placement: dict) -> dict[tuple[str, str], dict]:
    edges: dict[tuple[str, str], dict] = {}
    for pod, service in (placement.get("pod_to_service") or {}).items():
        key = (pod, service)
        edges[key] = {
            "channel": "vertical",
            "call_direction": {"source": pod, "target": service},
            "candidate_propagation_direction": {"source": pod, "target": service},
            "direction_reason": "pod placement attribute maps to service",
            "in_abnormal": True,
            "in_normal": False,
        }
    for node, pods in (placement.get("node_to_pods") or {}).items():
        for pod in pods:
            key = (node, pod)
            edges[key] = {
                "channel": "vertical",
                "call_direction": {"source": node, "target": pod},
                "candidate_propagation_direction": {"source": node, "target": pod},
                "direction_reason": "node hosts pod (metrics attr)",
                "in_abnormal": True,
                "in_normal": False,
            }
    for pod, containers in (placement.get("pod_to_containers") or {}).items():
        for container in containers:
            key = (pod, container)
            edges[key] = {
                "channel": "vertical",
                "call_direction": {"source": pod, "target": container},
                "candidate_propagation_direction": {"source": pod, "target": container},
                "direction_reason": "pod contains container (metrics attr)",
                "in_abnormal": True,
                "in_normal": False,
            }
    return edges


def _adjacency(edges: dict[tuple[str, str], dict]) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        adj[src].append(dst)
    for src in adj:
        adj[src] = sorted(set(adj[src]))
    return adj


def enumerate_paths(
    edges: dict[tuple[str, str], dict],
    start: str,
    end: str,
    *,
    max_hops: int,
    max_visits: int,
) -> list[list[str]]:
    if start == end:
        return [[start]]
    adj = _adjacency(edges)
    found: list[list[str]] = []

    def dfs(path: list[str], visits: dict[str, int]) -> None:
        if len(path) - 1 > max_hops:
            return
        node = path[-1]
        if node == end and len(path) > 1:
            found.append(list(path))
            return
        if len(path) - 1 == max_hops:
            return
        for nxt in adj.get(node, ()):
            if visits.get(nxt, 0) >= max_visits:
                continue
            visits[nxt] = visits.get(nxt, 0) + 1
            path.append(nxt)
            dfs(path, visits)
            path.pop()
            visits[nxt] -= 1

    dfs([start], {start: 1})
    found.sort(key=lambda p: (len(p), p))
    return found


def build_edge_tables(reality: dict) -> tuple[dict, dict]:
    frames = reality["_frames"]
    h_edges, _ = horizontal_edges(frames["abnormal"], frames["normal"])
    v_edges = vertical_edges(reality.get("placement") or {})
    return h_edges, v_edges


def paths_between(
    h_edges: dict[tuple[str, str], dict],
    start: str,
    end: str,
    rules: dict,
) -> list[list[str]]:
    path_cfg = rules.get("path_search") or {}
    return enumerate_paths(
        h_edges,
        start,
        end,
        max_hops=int(path_cfg.get("max_hops", 5)),
        max_visits=int(path_cfg.get("max_visits_per_component", 2)),
    )


def build_candidate_graph(
    reality: dict,
    rules: dict,
    *,
    start: str | None = None,
    end: str | None = None,
) -> dict:
    """Horizontal path search + vertical placement edges (same tables for any seed)."""
    h_edges, v_edges = build_edge_tables(reality)
    start = start or reality["injection"]["component"]
    end = end or reality["symptom"]["component"]
    paths = paths_between(h_edges, start, end, rules)
    nodes = sorted(
        {n for e in h_edges for n in e}
        | {n for e in v_edges for n in e}
        | {start, end}
    )
    return {
        "nodes": [{"id": n, "entity_type": "service"} for n in nodes],
        "horizontal": h_edges,
        "vertical": v_edges,
        "candidate_paths": paths,
        "start": start,
        "end": end,
    }
