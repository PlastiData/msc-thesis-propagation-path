"""Emit, scorecard, and aggregate HTML tests."""

from __future__ import annotations

from pipeline.emit import (
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
from pipeline.fault_taxonomy import taxonomy_public


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

