#!/usr/bin/env bash
# USB-aware validation for 02-implementation/. Run from USB root or 02-implementation/.
set -euo pipefail

IMPL="$(cd "$(dirname "$0")/.." && pwd)"
USB="$(cd "$IMPL/.." && pwd)"
cd "$IMPL"
export PIP_CONFIG_FILE="${PIP_CONFIG_FILE:-/dev/null}"

fail() { echo "FAIL: $*" >&2; exit 1; }
ok() { echo "OK: $*"; }

echo "== structure =="
test -f analysis/cli.py || fail "analysis/cli.py missing"
test -d analysis/pipeline || fail "analysis/pipeline missing"
test -f analysis/pipeline/evidence_rules.json || fail "evidence_rules.json missing"
test ! -f .env || fail ".env must not ship on USB"
# thesis.pdf is USB-only; public GitHub ships README instead
if [[ ! -f "$USB/thesis.pdf" && ! -f "$USB/README.md" ]]; then
  fail "thesis.pdf or README.md missing at pack root"
fi
test -f "$USB/01-results/propagation-paths/strict/summary.json" || fail "strict summary.json missing"
test -f "$USB/01-results/propagation-paths/relaxed/summary.json" || fail "relaxed summary.json missing"
test -f "$USB/01-results/propagation-paths/strict/index.html" || fail "strict index.html missing"
test -f "$USB/01-results/llm-second-opinion/relaxed/pilot_results.json" || fail "pilot_results.json missing"

N=$(python3 -c "import json; print(json.load(open('$USB/01-results/propagation-paths/strict/summary.json'))['evaluated_cases'])")
[[ "$N" == "1422" ]] || fail "strict summary evaluated_cases=$N expected 1422"
ok "structure ($N cases)"

if command -v rg >/dev/null; then
  if rg -n 'from chain_poc|import chain_poc' analysis 2>/dev/null; then
    fail "chain_poc import leaked"
  fi
  if rg -l '/home/alexis|/Users/' "$USB/01-results" --glob '*.html' 2>/dev/null | head -1 | grep -q .; then
    fail "absolute home paths in frozen HTML"
  fi
fi

echo "== venv + unit tests =="
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -U pip -q
  .venv/bin/pip install -e ".[dev]" -q
fi
.venv/bin/python -m pytest tests/ -q
ok "pytest"

echo "== frozen LLM pilot =="
python3 <<PY
import json
from pathlib import Path
rows = json.loads(Path("$USB/01-results/llm-second-opinion/relaxed/pilot_results.json").read_text())
assert len(rows) == 4080, len(rows)
models = {r["model"] for r in rows}
assert len(models) == 6, models
errs = [r for r in rows if r.get("error")]
assert not errs, f"{len(errs)} errors in pilot"
print("rows", len(rows), "models", len(models))
PY
ok "LLM pilot 4080 rows, 6 models, 0 errors"

echo "== golden case keys =="
test -f tests/fixtures/golden_case.json || fail "golden_case.json missing"
GOLDEN_CASE="${GOLDEN_CASE:-ts4-ts-basic-service-request-delay-rxfqg2}"
FIXTURE_DIR="tests/fixtures/$GOLDEN_CASE"
if [[ -d "$FIXTURE_DIR" ]]; then
  RANKINGS="$USB/04-data/rankings"
  if [[ ! -d "$RANKINGS/data/rcabench" ]]; then
    [[ -L rankings ]] || ln -sf ../04-data/rankings rankings 2>/dev/null || true
  fi
  OUT="$IMPL/results/_validation/golden"
  rm -rf "$OUT"
  .venv/bin/python analysis/cli.py \
    --case "$GOLDEN_CASE" \
    --policy strict \
    --data-root "$IMPL/tests/fixtures" \
    --out-root "$OUT" || fail "golden fixture rebuild failed"
  .venv/bin/python <<PY
import json
from pathlib import Path
golden = json.loads(Path("tests/fixtures/golden_case.json").read_text())
out = json.loads(Path("$OUT/_cli_cases/strict/$GOLDEN_CASE/machine_graph.json").read_text())
for key in ("judgment", "case_metrics"):
    if golden.get(key) != out.get(key):
        raise SystemExit(f"golden mismatch on {key}")
print("judgment keys match")
PY
  ok "golden case $GOLDEN_CASE"
else
  echo "SKIP golden fixture rebuild (no $FIXTURE_DIR)"
fi

echo "== one-case live rebuild =="
DATA_ROOT="${DATA_ROOT:-$USB/04-data/telemetry/rcabench-platform-v2/data/rcabench}"
LIVE_CASE="${LIVE_CASE:-ts0-ts-order-service-stress-64c8cv}"
if [[ -d "$DATA_ROOT/$LIVE_CASE" ]]; then
  [[ -L rankings ]] || ln -sf ../04-data/rankings rankings 2>/dev/null || true
  OUT="$IMPL/results/_validation/live"
  rm -rf "$OUT"
  .venv/bin/python analysis/cli.py \
    --case "$LIVE_CASE" \
    --policy strict \
    --data-root "$DATA_ROOT" \
    --out-root "$OUT"
  test -f "$OUT/_cli_cases/strict/$LIVE_CASE/machine_graph.json" || fail "live rebuild output missing"
  ok "live rebuild $LIVE_CASE"
else
  echo "SKIP live rebuild (no datapack at $DATA_ROOT/$LIVE_CASE)"
fi

echo "== ALL CHECKS PASSED =="
