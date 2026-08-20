"""Rules and policy loading tests."""

from __future__ import annotations

from pipeline.config import load_rules, select_policy


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
