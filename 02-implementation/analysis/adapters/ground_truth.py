"""Injection target helpers used by the evidence Reality layer."""

from __future__ import annotations

import json
from collections.abc import Mapping


def _parse_display_config(injection: Mapping) -> dict:
    raw_config = injection.get("display_config") or {}
    if not isinstance(raw_config, str):
        return raw_config if isinstance(raw_config, dict) else {}
    try:
        parsed = json.loads(raw_config)
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return parsed


def injected_targets(injection: Mapping) -> list[str]:
    """Prefer target_service / server_address; label set is unordered fallback."""
    point = _parse_display_config(injection).get("injection_point") or {}
    target = point.get("target_service") or point.get("server_address")
    if target:
        return [str(target)]
    services = injection.get("ground_truth", {}).get("service") or []
    if not services:
        return []
    return [str(service) for service in services]
