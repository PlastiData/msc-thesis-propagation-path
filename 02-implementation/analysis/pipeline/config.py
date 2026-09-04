"""Load and hash evidence_rules.json."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

RULES_PATH = Path(__file__).with_name("evidence_rules.json")


def load_rules(path: Path | None = None) -> dict:
    rules_path = path or RULES_PATH
    if not rules_path.exists():
        return {"error": f"rules missing: {rules_path}"}
    raw = rules_path.read_bytes()
    try:
        rules = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        return {"error": f"rules invalid JSON: {exc}"}
    if not isinstance(rules, dict):
        return {"error": "rules root must be an object"}
    presets = rules.get("acceptance_presets") or {}
    if not isinstance(presets, dict) or not presets:
        return {"error": "acceptance_presets missing"}
    rules["_path"] = str(rules_path)
    rules["_config_hash"] = hashlib.sha256(raw).hexdigest()
    return rules


def select_policy(rules: dict, policy_name: str) -> dict | str:
    presets = rules.get("acceptance_presets") or {}
    policy = presets.get(policy_name)
    if policy is None:
        return f"unknown policy {policy_name!r}; choose from {sorted(presets)}"
    return dict(policy)
