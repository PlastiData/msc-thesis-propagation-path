"""Injection taxonomy lookup tests."""

from __future__ import annotations

from pipeline.fault_taxonomy import (
    FAULT_TYPE_NAMES,
    all_taxonomy_fault_types,
    injection_taxonomy,
    taxonomy_public,
)


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
