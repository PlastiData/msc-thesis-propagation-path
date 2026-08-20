"""Tests for the evidence-backed propagation POC."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ANALYSIS_DIR = Path(__file__).resolve().parent
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

from evidence.algo_context import select_best_algo
from evidence.config import load_rules, select_policy
from evidence.emit import (
    SCORECARD_HEADER,
    aggregate,
    build_scorecard,
    graph_html_from_machine,
    human_report_from_machine,
    index_html,
    path_agreement,
    reject_machine_graph,
    scorecard_line,
)
from evidence.evidence import classify_edge
from evidence.fault_taxonomy import (
    FAULT_TYPE_NAMES,
    all_taxonomy_fault_types,
    injection_taxonomy,
    taxonomy_public,
)
from evidence.judgment import case_metrics, judge


def ratios_sum_to_one(obs: float, sup: float, inf: float, tol: float = 1e-9) -> bool:
    return abs((obs + sup + inf) - 1.0) <= tol


def test_injection_taxonomy_lookup_completeness() -> None:
    """All named ints + sample10 fault_types map to Tables 5–6 fields."""
    sample10_types = {22, 28, 7, 11, 8}
    for ft in set(FAULT_TYPE_NAMES) | sample10_types | set(all_taxonomy_fault_types()):
        row = injection_taxonomy(ft)
        assert row["mapped"] is True, f"unmapped fault_type {ft}"
        assert row["category"]
        assert row["chaos_type"]
        assert row["target_layer"] in ("infrastructure", "application")
        assert row["fault_kind"]
        assert row["expected_propagation_channel"]
        pub = taxonomy_public(ft)
        assert pub["mapped"] is True
        assert pub["fault_kind"] == row["fault_kind"]

    unknown = injection_taxonomy(999)
    assert unknown["mapped"] is False
    assert unknown["fault_kind"].startswith("unknown_")


def test_rules_load_and_policies() -> None:
    rules = load_rules()
    assert "error" not in rules
    assert rules["_config_hash"]
    strict = select_policy(rules, "strict")
    relaxed = select_policy(rules, "relaxed")
    assert isinstance(strict, dict)
    assert isinstance(relaxed, dict)
    assert strict["max_inferred_edges"] == 0
    assert relaxed["max_inferred_edges"] >= 1


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


def test_reject_stays_in_denominator() -> None:
    machines = [
        reject_machine_graph("a", {"policy": "strict"}, "symptom_unavailable"),
        reject_machine_graph("b", {"policy": "strict"}, "no_connected_candidate_path"),
    ]
    summary = aggregate(machines)
    assert summary["evaluated_cases"] == 2
    assert summary["constructed_cases"] == 0
    assert summary["path_coverage"] == 0.0
    assert summary["rejection_profile"]["symptom_unavailable"]["count"] == 1


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


def test_human_derived_only_from_machine() -> None:
    machine = reject_machine_graph("c1", {"policy": "strict"}, "other", detail="x")
    human = human_report_from_machine(machine)
    assert human["case_id"] == "c1"
    assert human["status"] == "insufficient_evidence"
    assert human["judgment"]["primary_rejection_reason"] == "other"
    assert "algo" in human
    assert human["scorecard"]["seed"] == "fault"
    assert human["scorecard"]["evid"] is None
    assert human["scorecard"]["rca_pct"] == 0
    assert human["scorecard"]["hops"] is None
    assert human["scorecard"]["refuse"] == "other"
    assert human["scorecard_algo"]["seed"] == "algo"


def test_select_best_algo_by_ac_at_1() -> None:
    rankings = {
        "nsigma": {"available": True, "rank1": "svc-n"},
        "traceback-A8": {"available": True, "rank1": "svc-a8"},
        "baro": {"available": True, "rank1": "svc-b"},
    }
    perf = [
        {"algorithm": "traceback-A8", "AC@1": 0.625},
        {"algorithm": "traceback-A7", "AC@1": 0.55},
        {"algorithm": "nsigma", "AC@1": 0.4},
        {"algorithm": "baro", "AC@1": 0.3},
    ]
    best = select_best_algo(rankings, perf)
    assert best["algo"] == "traceback-A8"
    assert best["rank1"] == "svc-a8"
    assert best["ac_at_1"] == 0.625
    assert best["selection"] == "best_ac_at_1"

    only_nsigma = {"nsigma": rankings["nsigma"]}
    best2 = select_best_algo(only_nsigma, perf)
    assert best2["algo"] == "nsigma"

    forced = select_best_algo(rankings, perf, override="baro")
    assert forced["algo"] == "baro"
    assert forced["selection"] == "override"

    missing = select_best_algo({}, perf)
    assert missing["available"] is False
    assert missing["reason"] == "algo_output_missing"


def test_scorecard_matches_console_keys() -> None:
    machine = {
        "case_id": "c-score",
        "run": {"sec": 7.2},
        "algo_context": {
            "algo": "traceback-A8",
            "rank1": "ts-route-plan-service",
            "top_services": [
                {"rank": 1, "service": "ts-a"},
                {"rank": 2, "service": "ts-b"},
            ],
        },
    }
    judgment = {
        "status": "candidate_path_constructed",
        "selected_path_edge_ids": ["e1", "e2"],
        "selected_path_nodes": ["ts-a", "ts-b", "ts-c"],
        "primary_rejection_reason": None,
    }
    edges = [
        {"edge_id": "e1", "evidence_level": "observed"},
        {"edge_id": "e2", "evidence_level": "inferred"},
    ]
    sc = build_scorecard(machine, seed="fault", judgment=judgment, edges=edges)
    assert set(sc) >= {"case", "sec", "evid", "rca_pct", "hops", "seed", "algo", "rank1", "refuse"}
    assert sc["evid"] == "inf"
    assert sc["hops"] == 2
    assert sc["rca_pct"] == 67
    assert sc["refuse"] is None
    line = scorecard_line(sc)
    assert "c-score" in line
    assert "inject" in line
    assert "inf" in line
    line_algo = scorecard_line({**sc, "seed": "algo", "case": ""}, show_case=False)
    assert "rca" in line_algo
    for col in ("case", "seed", "sec", "evid", "rca%", "hops"):
        assert col in SCORECARD_HEADER


def test_case_page_renders_path_map() -> None:
    machine = {
        "case_id": "demo",
        "reality": {
            "injection": {
                "component": "ts-a-service",
                "fault_type": 1,
                "start_time": "t0",
                "end_time": "t1",
            },
            "symptom": {
                "component": "ts-b-service",
                "selection_rule": "x",
                "span_name": "HTTP GET http://ts-b-service:8080/api/v1/demo",
            },
            "timeline": [
                {
                    "timestamp": "t0",
                    "event_type": "injection_start",
                    "component": "ts-a-service",
                    "note": "fault injection window start",
                }
            ],
        },
        "candidate_graph": {
            "edges": [
                {
                    "edge_id": "e1",
                    "source": "ts-a-service",
                    "target": "ts-b-service",
                    "evidence_level": "observed",
                    "checks": {
                        "structural": "pass",
                        "statistical": "pass",
                        "temporal": "unknown",
                    },
                    "missing_evidence": [],
                    "evidence_refs": [],
                    "hop": {
                        "route": "POST /api/v1/demo",
                        "span_names": ["POST /api/v1/demo"],
                        "call_count": 12,
                        "error_count": 2,
                        "trace_ids": ["abc123def4567890"],
                        "in_abnormal": True,
                        "in_normal": True,
                        "stat": {
                            "source": {
                                "verdict": "pass",
                                "source": "metrics",
                                "hits": [
                                    {
                                        "metric": "jvm_memory_used",
                                        "family": "gauge",
                                        "z": 4.2,
                                        "abnormal_mean": 1.0,
                                        "normal_mean": 0.1,
                                    }
                                ],
                            },
                            "target": {
                                "verdict": "pass",
                                "source": "metrics",
                                "hits": [],
                            },
                        },
                    },
                }
            ]
        },
        "judgment": {
            "status": "candidate_path_constructed",
            "selected_path_edge_ids": ["e1"],
            "selected_path_nodes": ["ts-a-service", "ts-b-service"],
            "policy": "strict",
            "primary_rejection_reason": None,
            "limitations": [],
        },
        "case_metrics": {},
        "evidence_registry": [{"claim": "direct parent-child spans"}],
        "algo_context": {
            "available": True,
            "algo": "traceback-A8",
            "rank1": "ts-a-service",
            "rank1_hit": True,
            "predicted_chain": ["ts-a-service", "ts-b-service"],
            "top_services": [{"rank": 1, "service": "ts-a-service", "hit": True}],
            "error": None,
        },
        "rca_path": {
            "algo": "traceback-A8",
            "algo_ac_at_1": 0.625,
            "seed": "ts-a-service",
            "end": "ts-b-service",
            "judgment": {
                "status": "candidate_path_constructed",
                "selected_path_edge_ids": ["e1"],
                "selected_path_nodes": ["ts-a-service", "ts-b-service"],
                "primary_rejection_reason": None,
                "policy": "strict",
            },
            "case_metrics": {},
        },
    }
    page = graph_html_from_machine(machine)
    assert 'id="verdict"' in page
    assert "ACCEPT (strict)" in page
    assert 'id="dual-path"' in page
    assert "Dual-path compare" in page
    assert "Both seeds" in page
    assert 'id="evidence"' in page
    assert "Upstream RCA rankings" in page
    assert "Walk chain" in page
    assert page.find("Dual-path compare") < page.find("Upstream RCA rankings")
    assert page.find('id="evidence"') < page.find("Upstream RCA rankings")
    assert ">Why<" not in page
    assert "<th>Time</th>" not in page
    assert "<th>Route</th>" in page
    assert "<th>Calls</th>" in page
    assert "<th>Traces</th>" in page
    assert "POST /api/v1/demo" in page
    assert "12 / 2 err" in page
    assert "abc123def4567890"[:16] in page
    assert "z=4.2" in page
    assert "Injection window" in page
    assert "Timeline anchors" in page
    assert "not a full incident Gantt" in page
    assert "fault injection window start" in page


def test_call_pair_stats_and_timeline_honesty() -> None:
    import pandas as pd
    from evidence.reality import build_timeline, enrich_timeline_path_errors
    from trace_graph import call_pair_stats

    traces = pd.DataFrame(
        [
            {
                "time": "2025-01-01T00:00:01Z",
                "trace_id": "t1",
                "span_id": "s1",
                "parent_span_id": "",
                "span_name": "GET /root",
                "service_name": "caller",
                "attr.status_code": "Unset",
            },
            {
                "time": "2025-01-01T00:00:02Z",
                "trace_id": "t1",
                "span_id": "s2",
                "parent_span_id": "s1",
                "span_name": "POST /api/v1/x",
                "service_name": "callee",
                "attr.status_code": "Error",
            },
            {
                "time": "2025-01-01T00:00:03Z",
                "trace_id": "t2",
                "span_id": "s3",
                "parent_span_id": "s1",
                "span_name": "POST /api/v1/x",
                "service_name": "callee",
                "attr.status_code": "Unset",
            },
        ]
    )
    # parent s1 only exists once; second child still resolves via id2svc for s1
    stats = call_pair_stats(traces)
    assert ("caller", "callee") in stats
    assert stats[("caller", "callee")]["call_count"] == 2
    assert stats[("caller", "callee")]["error_count"] == 1
    assert "POST /api/v1/x" in stats[("caller", "callee")]["span_names"]
    assert "t1" in stats[("caller", "callee")]["trace_ids"]

    injection = {
        "component": "callee",
        "start_time": "2025-01-01T00:00:00Z",
        "end_time": "2025-01-01T00:10:00Z",
    }
    symptom = {
        "component": "caller",
        "span_name": "GET /root",
        "source": "conclusion.parquet",
    }
    timeline = build_timeline(injection, symptom, traces)
    types = [e["event_type"] for e in timeline]
    assert "injection_start" in types
    assert "injection_end" in types
    assert "first_error_span" in types
    assert "selected_symptom" in types
    assert types.index("injection_start") < types.index("injection_end")
    symptom_ev = next(e for e in timeline if e["event_type"] == "selected_symptom")
    assert symptom_ev["timestamp"] != injection["end_time"]
    assert "note" in symptom_ev

    enriched = enrich_timeline_path_errors(timeline, traces, ["caller", "callee"])
    assert any(e["event_type"] == "path_first_error" for e in enriched) or any(
        e["event_type"] == "first_error_span" and e["component"] == "callee"
        for e in enriched
    )

def test_path_agreement_classes() -> None:
    ok = "candidate_path_constructed"
    refuse = "insufficient_evidence"
    assert path_agreement(ok, ["a", "b"], ok, ["a", "b"]) == "same"
    assert path_agreement(ok, ["a", "b"], ok, ["a", "c"]) == "differ"
    assert path_agreement(ok, ["a"], refuse, []) == "inject_only"
    assert path_agreement(refuse, [], ok, ["a"]) == "rca_only"
    assert path_agreement(refuse, [], refuse, []) == "both_refuse"


def test_aggregate_agreement_and_index_rq() -> None:
    ok = "candidate_path_constructed"
    refuse = "insufficient_evidence"

    def machine(cid, fault_nodes, rca_nodes, *, fault_ok=True, rca_ok=True):
        edges = []
        fault_ids = []
        for i in range(max(0, len(fault_nodes) - 1)):
            eid = f"{cid}-f{i}"
            fault_ids.append(eid)
            edges.append(
                {
                    "edge_id": eid,
                    "source": fault_nodes[i],
                    "target": fault_nodes[i + 1],
                    "evidence_level": "observed",
                }
            )
        rca_ids = []
        for i in range(max(0, len(rca_nodes) - 1)):
            eid = f"{cid}-r{i}"
            if eid not in {e["edge_id"] for e in edges}:
                edges.append(
                    {
                        "edge_id": eid,
                        "source": rca_nodes[i],
                        "target": rca_nodes[i + 1],
                        "evidence_level": "observed",
                    }
                )
            rca_ids.append(eid)
        return {
            "case_id": cid,
            "run": {"policy": "strict", "sec": 1.0},
            "reality": {
                "injection": {
                    "component": (fault_nodes or ["x"])[0],
                    "fault_type": 7,
                    "injected_fault": taxonomy_public(7),
                },
                "symptom": {"component": (fault_nodes or rca_nodes or ["y"])[-1]},
                "timeline": [],
            },
            "candidate_graph": {"edges": edges},
            "judgment": {
                "status": ok if fault_ok else refuse,
                "selected_path_edge_ids": fault_ids if fault_ok else [],
                "selected_path_nodes": fault_nodes if fault_ok else [],
                "primary_rejection_reason": None if fault_ok else "no_connected_candidate_path",
                "policy": "strict",
            },
            "case_metrics": {
                "observed_edges": len(fault_ids) if fault_ok else 0,
                "supported_edges": 0,
                "inferred_edges": 0,
                "observed_edge_ratio": 1.0 if fault_ok and fault_ids else 0.0,
                "supported_edge_ratio": 0.0,
                "inferred_edge_ratio": 0.0,
                "returned_edges": len(fault_ids) if fault_ok else 0,
                "path_covered": 1 if fault_ok else 0,
            },
            "algo_context": {"algo": "nsigma", "rank1": (rca_nodes or ["z"])[0]},
            "rca_path": {
                "algo": "nsigma",
                "seed": (rca_nodes or [None])[0],
                "judgment": {
                    "status": ok if rca_ok else refuse,
                    "selected_path_edge_ids": rca_ids if rca_ok else [],
                    "selected_path_nodes": rca_nodes if rca_ok else [],
                    "primary_rejection_reason": None if rca_ok else "algo_output_missing",
                    "policy": "strict",
                },
                "case_metrics": {
                    "observed_edges": len(rca_ids) if rca_ok else 0,
                    "supported_edges": 0,
                    "inferred_edges": 0,
                },
            },
        }

    machines = [
        machine("same1", ["a", "b"], ["a", "b"]),
        machine("diff1", ["a", "b"], ["a", "c"]),
        machine("inj1", ["a", "b"], [], rca_ok=False),
        machine("rca1", [], ["a", "b"], fault_ok=False),
        machine("none1", [], [], fault_ok=False, rca_ok=False),
    ]
    summary = aggregate(machines)
    assert summary["agreement_profile"] == {
        "same": 1,
        "differ": 1,
        "inject_only": 1,
        "rca_only": 1,
        "both_refuse": 1,
    }
    by_id = {c["case_id"]: c["agreement"] for c in summary["cases"]}
    assert by_id["same1"] == "same"
    assert by_id["diff1"] == "differ"

    page = index_html(summary, sample="sample10", policy="strict")
    assert "Investigation queue" in page
    assert "<details" in page
    assert "Evaluation metrics" in page
    assert page.find("Investigation queue") < page.find("RQ-A")
    assert "RQ-A" in page
    assert "RQ-C" in page
    assert "Agreement" in page
    assert "RQ-B" in page
    assert "data-filter" in page
    assert "Sibling policy" in page or "relaxed" in page
    assert "Accept / refuse by injection taxonomy" in page
    assert "OpenRCA 2.0" in page
    assert "target_layer" in page
    assert "fault_kind" in page

    strat = summary["injection_stratification"]
    assert "by_target_layer" in strat
    assert "by_fault_kind" in strat
    layer = strat["by_target_layer"]["inject"]
    assert "application" in layer
    assert layer["application"]["n"] == 5
    assert "Tables 5" in strat["note"] or "Table 5" in strat["note"]

    # Queue sort: differ before same
    assert page.find("diff1") < page.find("same1")

    summary["sibling_policy"] = {
        "policy": "relaxed",
        "path_coverage": 0.8,
        "rca_path_coverage": 0.5,
        "constructed_cases": 8,
        "rca_constructed_cases": 5,
        "evaluated_cases": 10,
    }
    page2 = index_html(summary, sample="sample10", policy="strict")
    assert "relaxed" in page2
    assert "8/10" in page2


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


@pytest.mark.parametrize("policy_name", ["strict", "relaxed"])
def test_smoke_one_case_if_data_present(policy_name: str) -> None:
    data_root = ANALYSIS_DIR.parent / "data/rcabench-platform-v2/data/rcabench"
    case_id = "ts4-ts-basic-service-request-delay-rxfqg2"
    if not (data_root / case_id).exists():
        pytest.skip("benchmark data not present")
    import evidence_path_poc as poc

    rules = load_rules()
    policy = select_policy(rules, policy_name)
    assert isinstance(policy, dict)
    machine = poc.process_case(
        case_id,
        data_root=data_root,
        rules=rules,
        policy=policy,
        policy_name=policy_name,
        run_meta={"policy": policy_name, "config_hash": rules["_config_hash"]},
    )
    assert machine["schema_version"]
    assert machine["judgment"]["status"] in {
        "candidate_path_constructed",
        "insufficient_evidence",
    }
    assert machine["judgment"]["primary_rejection_reason"] in {
        None,
        *rules["rejection_reasons"],
    }
    assert "rca_path" in machine
    assert machine["rca_path"]["judgment"]["status"] in {
        "candidate_path_constructed",
        "insufficient_evidence",
    }
    assert machine["rca_path"]["judgment"]["primary_rejection_reason"] in {
        None,
        *rules["rejection_reasons"],
    }
    assert "scorecard" in machine
    assert machine["rca_path"].get("scorecard", {}).get("seed") == "algo"

    machine2 = poc.process_case(
        case_id,
        data_root=data_root,
        rules=rules,
        policy=policy,
        policy_name=policy_name,
        run_meta={"policy": policy_name, "config_hash": rules["_config_hash"]},
    )
    assert machine["judgment"] == machine2["judgment"]
    assert machine["case_metrics"] == machine2["case_metrics"]
    assert machine["rca_path"]["judgment"] == machine2["rca_path"]["judgment"]
    dumped = json.dumps(machine["candidate_graph"], sort_keys=True)
    dumped2 = json.dumps(machine2["candidate_graph"], sort_keys=True)
    assert dumped == dumped2
