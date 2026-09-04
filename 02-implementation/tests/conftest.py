"""Pytest path setup: analysis/ on sys.path for pipeline and adapters."""

from __future__ import annotations

import sys
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))


def ratios_sum_to_one(obs: float, sup: float, inf: float, tol: float = 1e-9) -> bool:
    return abs((obs + sup + inf) - 1.0) <= tol
