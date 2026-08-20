"""Edge labels and judgment policy tests."""

from __future__ import annotations

from conftest import ratios_sum_to_one
from pipeline.config import load_rules
from pipeline.evidence import classify_edge
from pipeline.judgment import case_metrics, judge


def test_classify_observed_supported_inferred() -> None:
    rules = load_rules()
    level, missing = classify_edge(
        {"structural": "pass", "statistical": "pass", "temporal": "unknown"},
        rules,
        both_incident=True,
    )
    assert level == "observed"
    assert missing == []

    level, missing = classify_edge(
        {"structural": "fail", "statistical": "pass", "temporal": "pass"},
        rules,
        both_incident=True,
    )
    assert level == "supported"

    level, missing = classify_edge(
        {"structural": "fail", "statistical": "fail", "temporal": "unknown"},
        rules,
        both_incident=False,
    )
    assert level == "inferred"
    assert "usable_temporal_onset_ordering" in missing
    assert "unknown" != "pass"


def test_unknown_temporal_never_promoted() -> None:
    rules = load_rules()
    checks = {"structural": "pass", "statistical": "pass", "temporal": "unknown"}
    level, _ = classify_edge(checks, rules, both_incident=True)
    assert level == "observed"
    assert checks["temporal"] == "unknown"


def test_case_metrics_ratios() -> None:
    judgment = {
        "status": "candidate_path_constructed",
        "selected_path_edge_ids": ["e1", "e2"],
    }
    edges = {
        "e1": {"evidence_level": "observed"},
        "e2": {"evidence_level": "inferred"},
    }
    metrics = case_metrics(judgment, edges)
    assert metrics["returned_edges"] == 2
    assert ratios_sum_to_one(
        metrics["observed_edge_ratio"],
        metrics["supported_edge_ratio"],
        metrics["inferred_edge_ratio"],
    )


def test_judge_prefers_fewest_inferred() -> None:
    policy = {
        "max_inferred_edges": 2,
        "min_observed_or_supported_fraction": 0.0,
        "allow_ambiguous_paths": False,
    }
    annotated = {
        "annotated_paths": [
            {
                "nodes": ["a", "b", "c"],
                "edges": [
                    {"edge_id": "e1", "evidence_level": "inferred"},
                    {"edge_id": "e2", "evidence_level": "observed"},
                ],
            },
            {
                "nodes": ["a", "c"],
                "edges": [
                    {"edge_id": "e3", "evidence_level": "observed"},
                ],
            },
        ]
    }
    result = judge(annotated, policy, "relaxed")
    assert result["status"] == "candidate_path_constructed"
    assert result["selected_path_edge_ids"] == ["e3"]
