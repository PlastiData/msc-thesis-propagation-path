"""Algo context selection tests."""

from __future__ import annotations

from pipeline.algo_context import select_best_algo


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
