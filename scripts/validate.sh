#!/usr/bin/env bash
# End-to-end sanity for a fresh clone. Exit non-zero on any failure.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PIP_CONFIG_FILE="${PIP_CONFIG_FILE:-/dev/null}"

echo "== structure =="
test -f README.md
test -f LICENSE
test -f analysis/cli.py
test -d analysis/pipeline
test -f analysis/pipeline/evidence_rules.json
test -f analysis/pipeline/fault_types.py
test -f analysis/ground_truth.py
test -f rankings/meta/rcabench/dataset.perf.parquet
test -d rankings/data/rcabench
test -f results/evidence_path_poc/sample_all/strict/summary.json
test -f results/evidence_path_poc/sample_all/relaxed/summary.json
test -f results/evidence_path_poc/sample_all/strict/index.html
! test -d data
! test -d output
if command -v rg >/dev/null; then
  if rg -n 'from chain_poc|import chain_poc' analysis; then
    echo "chain_poc import leaked"; exit 1
  fi
  if rg -l '/home/alexis|/Users/' results --glob '*.html' | head -1 | grep -q .; then
    echo "absolute home paths in HTML"; exit 1
  fi
fi

echo "== venv + tests =="
if [[ ! -x .venv/bin/python ]]; then
  if command -v uv >/dev/null; then
    uv venv .venv
    uv pip install --python .venv/bin/python -e ".[dev]"
  else
    python3 -m venv .venv
    .venv/bin/pip install -U pip
    .venv/bin/pip install -e ".[dev]"
  fi
fi
.venv/bin/python -m pytest tests/ -q

echo "== import entrypoint =="
PYTHONPATH=analysis .venv/bin/python -c "import cli as e; print('OUT_ROOT', e.OUT_ROOT)"

echo "== inject run if data present =="
DATA_ROOT="${DATA_ROOT:-$ROOT/data/rcabench-platform-v2/data/rcabench}"
CASE="${CASE:-ts0-ts-order-service-stress-64c8cv}"
if [[ -d "$DATA_ROOT/$CASE" ]]; then
  .venv/bin/python analysis/cli.py --case "$CASE" --policy strict --data-root "$DATA_ROOT"
  test -f "results/evidence_path_poc/_cli_cases/strict/$CASE/machine_graph.json"
  echo "inject-seed run OK"
else
  echo "SKIP inject-seed (no datapack at $DATA_ROOT/$CASE)"
fi

echo "== ALL CHECKS PASSED =="
