"""Trace call-pair and timeline honesty tests."""

from __future__ import annotations

import pandas as pd

from pipeline.reality import build_timeline, enrich_timeline_path_errors
from trace_graph import call_pair_stats


def test_call_pair_stats_and_timeline_honesty() -> None:
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
