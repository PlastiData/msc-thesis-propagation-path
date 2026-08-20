"""Injection taxonomy (OpenRCA 2.0 Tables 5–6) for scorecards and HTML."""

from __future__ import annotations

from typing import Any

from .fault_types import (
    FAULT_TYPE_NAMES,
    TAXONOMY_FIELDS,
    all_taxonomy_fault_types,
    injection_taxonomy,
)

__all__ = [
    "FAULT_TYPE_NAMES",
    "TAXONOMY_FIELDS",
    "all_taxonomy_fault_types",
    "injection_taxonomy",
    "taxonomy_public",
]


def taxonomy_public(fault_type: Any) -> dict[str, Any]:
    """Fields safe to embed in machine_graph / scorecard / HTML."""
    row = injection_taxonomy(fault_type)
    return {
        "fault_type": row.get("fault_type"),
        "mapped": bool(row.get("mapped")),
        "category": row.get("category"),
        "chaos_type": row.get("chaos_type"),
        "target_layer": row.get("target_layer"),
        "expected_propagation_channel": row.get("expected_propagation_channel"),
        "fault_kind": row.get("fault_kind"),
        "obs_channel_expected": row.get("obs_channel_expected"),
    }
