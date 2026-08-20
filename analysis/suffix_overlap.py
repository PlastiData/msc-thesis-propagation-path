"""Suffix-overlap check on differ-bucket cases from the evidence_path_poc run.

For every case where inject-seed and RCA-seed paths differ (agreement=="differ"),
checks whether the shorter path is an exact trailing subsequence (suffix) of the
longer one. A hit means both seeds converge onto the same downstream trajectory,
one seed simply enters it later. Reads the strict sample_all summary.json; no
recomputation of paths, no new run.
"""

import json
import sys
from collections import Counter
from pathlib import Path

SUMMARY = Path(
    "results/evidence_path_poc/sample_all/strict/summary.json"
)


def is_suffix(short: list[str], long: list[str]) -> bool:
    if not short or not long:
        return False
    if len(short) > len(long):
        return False
    return long[len(long) - len(short):] == short


def classify(case: dict) -> str:
    path = case.get("path") or []
    rca_path = case.get("rca_path") or []
    if not path or not rca_path:
        return "neither"
    if is_suffix(rca_path, path):
        return "rca_suffix_of_inject"
    if is_suffix(path, rca_path):
        return "inject_suffix_of_rca"
    return "neither"


def main() -> None:
    if not SUMMARY.exists():
        print(f"missing {SUMMARY}, run from analysis/", file=sys.stderr)
        sys.exit(1)

    cases = json.loads(SUMMARY.read_text())["cases"]
    differ = [c for c in cases if c.get("agreement") == "differ"]

    buckets = Counter(classify(c) for c in differ)
    hop_offsets = Counter(
        len(c["path"]) - len(c["rca_path"])
        for c in differ
        if classify(c) == "rca_suffix_of_inject"
    )
    examples = [
        c["case_id"]
        for c in differ
        if classify(c) == "rca_suffix_of_inject"
    ][:5]

    n = len(differ)
    print(f"differ cases: n={n}")
    for tag, count in buckets.most_common():
        print(f"  {tag}: {count} ({100 * count / n:.1f}%)")
    print(f"hop-offset distribution (inject_len - rca_len): {dict(hop_offsets)}")
    print(f"example case_ids (rca_suffix_of_inject): {examples}")


if __name__ == "__main__":
    main()
