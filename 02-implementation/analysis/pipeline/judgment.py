"""Judgment: accept a candidate path under a policy, or refuse with one reason."""

from __future__ import annotations


def _path_key(path_rec: dict) -> tuple:
    edges = path_rec["edges"]
    inferred = sum(1 for e in edges if e["evidence_level"] == "inferred")
    observed = sum(1 for e in edges if e["evidence_level"] == "observed")
    length = len(edges)
    lexical = "->".join(path_rec["nodes"])
    return (inferred, -observed, length, lexical)


def _passes_policy(path_rec: dict, policy: dict) -> bool:
    edges = path_rec["edges"]
    if not edges:
        return False
    inferred = sum(1 for e in edges if e["evidence_level"] == "inferred")
    observed = sum(1 for e in edges if e["evidence_level"] == "observed")
    supported = sum(1 for e in edges if e["evidence_level"] == "supported")
    fraction = (observed + supported) / len(edges)
    if inferred > int(policy.get("max_inferred_edges", 0)):
        return False
    if fraction < float(policy.get("min_observed_or_supported_fraction", 1.0)):
        return False
    return True


def judge(annotated: dict, policy: dict, policy_name: str) -> dict:
    paths = annotated.get("annotated_paths") or []
    if not paths:
        return {
            "status": "insufficient_evidence",
            "selected_path_edge_ids": [],
            "selected_path_nodes": [],
            "primary_rejection_reason": "no_connected_candidate_path",
            "rejection_reasons": ["no_connected_candidate_path"],
            "limitations": [
                "No official process-level ground truth was available.",
                "No connected horizontal candidate path from injection to symptom.",
            ],
            "policy": policy_name,
            "rejected_candidates": [],
        }

    eligible = [p for p in paths if _passes_policy(p, policy)]
    if not eligible:
        # Prefer a more specific horizontal reason when paths exist but fail policy.
        return {
            "status": "insufficient_evidence",
            "selected_path_edge_ids": [],
            "selected_path_nodes": [],
            "primary_rejection_reason": "required_horizontal_relationship_unavailable",
            "rejection_reasons": ["required_horizontal_relationship_unavailable"],
            "limitations": [
                "No official process-level ground truth was available.",
                f"Paths existed but none met acceptance policy {policy_name!r}.",
            ],
            "policy": policy_name,
            "rejected_candidates": [
                {"nodes": p["nodes"], "key": list(_path_key(p))} for p in paths[:20]
            ],
        }

    eligible.sort(key=_path_key)
    best = eligible[0]
    if len(eligible) > 1 and _path_key(eligible[0]) == _path_key(eligible[1]):
        if not policy.get("allow_ambiguous_paths", False):
            return {
                "status": "insufficient_evidence",
                "selected_path_edge_ids": [],
                "selected_path_nodes": [],
                "primary_rejection_reason": "ambiguous_equally_supported_paths",
                "rejection_reasons": ["ambiguous_equally_supported_paths"],
                "limitations": [
                    "No official process-level ground truth was available.",
                    "Two or more paths tied on the frozen selection order.",
                ],
                "policy": policy_name,
                "rejected_candidates": [
                    {"nodes": p["nodes"], "key": list(_path_key(p))}
                    for p in eligible[:10]
                ],
            }

    edge_ids = [e["edge_id"] for e in best["edges"]]
    levels = [e["evidence_level"] for e in best["edges"]]
    return {
        "status": "candidate_path_constructed",
        "selected_path_edge_ids": edge_ids,
        "selected_path_nodes": best["nodes"],
        "primary_rejection_reason": None,
        "rejection_reasons": [],
        "limitations": [
            "No official process-level ground truth was available.",
            "Evidence levels describe availability, not causal correctness.",
            f"Acceptance policy: {policy_name}.",
            f"Path evidence composition: {levels}.",
        ],
        "policy": policy_name,
        "rejected_candidates": [
            {"nodes": p["nodes"], "key": list(_path_key(p))}
            for p in paths
            if p is not best
        ][:20],
    }


def case_metrics(judgment: dict, edges_by_id: dict[str, dict]) -> dict:
    if judgment["status"] != "candidate_path_constructed":
        return {
            "path_covered": 0,
            "observed_edges": 0,
            "supported_edges": 0,
            "inferred_edges": 0,
            "observed_edge_ratio": 0.0,
            "supported_edge_ratio": 0.0,
            "inferred_edge_ratio": 0.0,
            "returned_edges": 0,
        }
    selected = [edges_by_id[eid] for eid in judgment["selected_path_edge_ids"]]
    obs = sum(1 for e in selected if e["evidence_level"] == "observed")
    sup = sum(1 for e in selected if e["evidence_level"] == "supported")
    inf = sum(1 for e in selected if e["evidence_level"] == "inferred")
    n = len(selected) or 1
    return {
        "path_covered": 1,
        "observed_edges": obs,
        "supported_edges": sup,
        "inferred_edges": inf,
        "observed_edge_ratio": obs / n,
        "supported_edge_ratio": sup / n,
        "inferred_edge_ratio": inf / n,
        "returned_edges": len(selected),
    }
