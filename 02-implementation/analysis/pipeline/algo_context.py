"""Upstream RCA rankings as investigation metadata (not the pipeline core).

The RCA seed is rank 1 of the best upstream algorithm for a case. Rankings ship in
`rankings/`; a full local platform run under `output/` is used instead when present.
Without either, the injection seed path still runs and the RCA column reports
algo_output_missing.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

AUTO_ALGO = "auto"
DEFAULT_ALGO = AUTO_ALGO
KNOWN_ALGOS = ("traceback-A8", "traceback-A7", "nsigma", "baro", "random")
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RANKINGS_ROOTS = (
    REPO_ROOT / "output/rcabench-platform-v2",
    REPO_ROOT / "rankings",
)
DATASETS = {
    "rcabench": {"data_root": REPO_ROOT / "data/rcabench-platform-v2/data/rcabench"},
}


def _rankings_root() -> Path:
    found = next((root for root in RANKINGS_ROOTS if root.is_dir()), None)
    return found or RANKINGS_ROOTS[0]


def resolve_paths(dataset: str) -> tuple[Path, Path]:
    paths = DATASETS.get(dataset)
    if paths is None:
        supported = ", ".join(sorted(DATASETS))
        raise ValueError(f"unknown dataset {dataset!r}; supported: {supported}")
    return paths["data_root"], _rankings_root() / "data" / dataset


def _service_frame(output_parquet: Path) -> pd.DataFrame:
    if not output_parquet.exists():
        return pd.DataFrame()
    frame = pd.read_parquet(output_parquet)
    if "level" in frame.columns:
        frame = frame[frame["level"] == "service"]
    if frame.empty or "rank" not in frame.columns:
        return pd.DataFrame()
    return frame.sort_values("rank")


def _ranking_metrics(frame: pd.DataFrame, labels: list[str]) -> dict:
    if frame.empty:
        return {
            "available": False,
            "rank1": None,
            "rank1_hit": None,
            "hit_at_1": None,
            "hit_at_3": None,
            "hit_at_5": None,
            "true_label_best_rank": None,
            "top_services": [],
            "runtime_seconds": None,
        }
    top = []
    for _, row in frame.head(8).iterrows():
        top.append(
            {
                "rank": int(row["rank"]),
                "service": str(row["name"]),
                "hit": bool(row["hit"]) if "hit" in row and pd.notna(row["hit"]) else None,
            }
        )
    rank1 = top[0]["service"] if top else None
    rank1_hit = top[0].get("hit") if top else None
    label_set = {str(x) for x in labels if x}
    best_rank = None
    if label_set:
        hits = frame[frame["name"].astype(str).isin(label_set)]
        if not hits.empty:
            best_rank = int(hits["rank"].min())
    runtime = None
    if "runtime.seconds" in frame.columns and pd.notna(frame.iloc[0]["runtime.seconds"]):
        runtime = float(frame.iloc[0]["runtime.seconds"])
    return {
        "available": True,
        "rank1": rank1,
        "rank1_hit": rank1_hit,
        "hit_at_1": bool(best_rank == 1) if best_rank is not None else bool(rank1_hit),
        "hit_at_3": bool(best_rank is not None and best_rank <= 3),
        "hit_at_5": bool(best_rank is not None and best_rank <= 5),
        "true_label_best_rank": best_rank,
        "top_services": top,
        "runtime_seconds": runtime,
    }


def dataset_perf_path(dataset: str = "rcabench") -> Path:
    return _rankings_root() / "meta" / dataset / "dataset.perf.parquet"


def load_dataset_perf(path: Path | None = None) -> list[dict]:
    path = path or dataset_perf_path()
    if not path.exists():
        return []
    frame = pd.read_parquet(path)
    rows = []
    for _, row in frame.iterrows():
        rows.append(
            {
                "algorithm": str(row.get("algorithm", "")),
                "total": int(row["total"]) if pd.notna(row.get("total")) else None,
                "AC@1": float(row["AC@1"]) if pd.notna(row.get("AC@1")) else None,
                "AC@3": float(row["AC@3"]) if pd.notna(row.get("AC@3")) else None,
                "AC@5": float(row["AC@5"]) if pd.notna(row.get("AC@5")) else None,
                "MRR": float(row["MRR"]) if pd.notna(row.get("MRR")) else None,
            }
        )
    rows.sort(key=lambda r: (-1 if r["AC@1"] is None else -r["AC@1"]))
    return rows


def _ac_at_1(dataset_perf: list[dict], algo: str | None) -> float | None:
    if not algo:
        return None
    for row in dataset_perf:
        if row.get("algorithm") == algo:
            return row.get("AC@1")
    return None


def select_best_algo(
    rankings: dict[str, dict],
    dataset_perf: list[dict],
    override: str | None = None,
) -> dict:
    """Highest AC@1 among algos with case output; override wins when available."""
    forced = override not in (None, "", AUTO_ALGO)
    if forced:
        row = rankings.get(override) or {}
        if row.get("available"):
            return {
                "algo": override,
                "ac_at_1": _ac_at_1(dataset_perf, override),
                "rank1": row.get("rank1"),
                "available": True,
                "reason": None,
                "selection": "override",
            }
        return {
            "algo": override,
            "ac_at_1": _ac_at_1(dataset_perf, override),
            "rank1": None,
            "available": False,
            "reason": "algo_output_missing",
            "selection": "override",
        }

    for perf in dataset_perf:
        name = perf.get("algorithm") or ""
        row = rankings.get(name) or {}
        if not row.get("available"):
            continue
        return {
            "algo": name,
            "ac_at_1": perf.get("AC@1"),
            "rank1": row.get("rank1"),
            "available": True,
            "reason": None,
            "selection": "best_ac_at_1",
        }

    for name in KNOWN_ALGOS:
        row = rankings.get(name) or {}
        if not row.get("available"):
            continue
        return {
            "algo": name,
            "ac_at_1": _ac_at_1(dataset_perf, name),
            "rank1": row.get("rank1"),
            "available": True,
            "reason": None,
            "selection": "fallback_known",
        }

    return {
        "algo": None,
        "ac_at_1": None,
        "rank1": None,
        "available": False,
        "reason": "algo_output_missing",
        "selection": "none",
    }


def load_algo_context(
    case_id: str,
    *,
    algo: str = DEFAULT_ALGO,
    dataset: str = "rcabench",
    injection_labels: list[str] | None = None,
    dataset_perf: list[dict] | None = None,
) -> dict:
    """Load rankings; primary + walk seed = best AC@1 (or --algo override)."""
    _, output_root = resolve_paths(dataset)
    case_out = output_root / case_id
    labels = list(injection_labels or [])
    perf = dataset_perf if dataset_perf is not None else load_dataset_perf()

    rankings: dict[str, dict] = {}
    for name in KNOWN_ALGOS:
        parquet = case_out / name / "output.parquet"
        if not parquet.exists():
            continue
        rankings[name] = {
            "algo": name,
            **_ranking_metrics(_service_frame(parquet), labels),
        }

    selection = select_best_algo(rankings, perf, override=algo)
    primary_algo = selection.get("algo")
    if not selection.get("available") or not primary_algo:
        return {
            "available": False,
            "algo": primary_algo or algo,
            "algo_ac_at_1": selection.get("ac_at_1"),
            "algo_selection": selection.get("selection"),
            "reason": selection.get("reason") or "algo_output_missing",
            "top_services": [],
            "rank1": None,
            "rank1_hit": None,
            "predicted_chain": [],
            "rankings": rankings,
            "error": None,
            "ground_truth_labels": labels,
        }

    primary = rankings[primary_algo]
    return {
        "available": True,
        "algo": primary_algo,
        "algo_ac_at_1": selection.get("ac_at_1"),
        "algo_selection": selection.get("selection"),
        "reason": None,
        "top_services": primary.get("top_services") or [],
        "rank1": primary.get("rank1"),
        "rank1_hit": primary.get("rank1_hit"),
        "hit_at_1": primary.get("hit_at_1"),
        "hit_at_3": primary.get("hit_at_3"),
        "hit_at_5": primary.get("hit_at_5"),
        "true_label_best_rank": primary.get("true_label_best_rank"),
        "predicted_chain": [],
        "rankings": rankings,
        "error": None,
        "ground_truth_labels": labels,
    }
