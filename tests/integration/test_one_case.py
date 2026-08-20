"""Integration smoke: one case when datapack is present."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.config import load_rules, select_policy


@pytest.mark.parametrize("policy_name", ["strict", "relaxed"])
def test_smoke_one_case_if_data_present(policy_name: str) -> None:
    data_root = Path(__file__).resolve().parents[2] / "data/rcabench-platform-v2/data/rcabench"
    case_id = "ts4-ts-basic-service-request-delay-rxfqg2"
    if not (data_root / case_id).exists():
        pytest.skip("benchmark data not present")
    import cli as poc

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
