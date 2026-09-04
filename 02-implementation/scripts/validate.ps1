# USB-aware validation for 02-implementation/ (Windows PowerShell).
$ErrorActionPreference = "Stop"
$Impl = Split-Path -Parent $PSScriptRoot
$Usb = Split-Path -Parent $Impl
Set-Location $Impl

function Fail($msg) { Write-Error "FAIL: $msg"; exit 1 }
function Ok($msg) { Write-Host "OK: $msg" }

Write-Host "== structure =="
if (-not (Test-Path "analysis/cli.py")) { Fail "analysis/cli.py missing" }
if (-not (Test-Path "analysis/pipeline")) { Fail "analysis/pipeline missing" }
if (Test-Path ".env") { Fail ".env must not ship on USB" }
if (-not (Test-Path "$Usb\thesis.pdf") -and -not (Test-Path "$Usb\README.md")) {
    Fail "thesis.pdf or README.md missing at pack root"
}
$strictSummary = "$Usb\01-results\propagation-paths\strict\summary.json"
if (-not (Test-Path $strictSummary)) { Fail "strict summary.json missing" }
if (-not (Test-Path "$Usb\01-results\llm-second-opinion\relaxed\pilot_results.json")) {
    Fail "pilot_results.json missing"
}

$n = python -c "import json; print(json.load(open(r'$strictSummary'))['evaluated_cases'])"
if ($n -ne "1422") { Fail "strict summary evaluated_cases=$n expected 1422" }
Ok "structure ($n cases)"

Write-Host "== venv + unit tests =="
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    & .\.venv\Scripts\pip install -U pip -q
    & .\.venv\Scripts\pip install -e ".[dev]" -q
}
& .\.venv\Scripts\python -m pytest tests/ -q
Ok "pytest"

Write-Host "== frozen LLM pilot =="
python -c @"
import json
from pathlib import Path
rows = json.loads(Path(r'$Usb\01-results\llm-second-opinion\relaxed\pilot_results.json').read_text())
assert len(rows) == 4080, len(rows)
models = {r['model'] for r in rows}
assert len(models) == 6, models
errs = [r for r in rows if r.get('error')]
assert not errs, f'{len(errs)} errors in pilot'
print('rows', len(rows), 'models', len(models))
"@
Ok "LLM pilot 4080 rows, 6 models, 0 errors"

Write-Host "== one-case live rebuild =="
$dataRoot = if ($env:DATA_ROOT) { $env:DATA_ROOT } else { "$Usb\04-data\telemetry\rcabench-platform-v2\data\rcabench" }
$liveCase = if ($env:LIVE_CASE) { $env:LIVE_CASE } else { "ts0-ts-order-service-stress-64c8cv" }
if (Test-Path "$dataRoot\$liveCase") {
    $out = "$Impl\results\_validation\live"
    if (Test-Path $out) { Remove-Item -Recurse -Force $out }
    & .\.venv\Scripts\python analysis/cli.py `
        --case $liveCase `
        --policy strict `
        --data-root $dataRoot `
        --out-root $out
    if (-not (Test-Path "$out\_cli_cases\strict\$liveCase\machine_graph.json")) { Fail "live rebuild output missing" }
    Ok "live rebuild $liveCase"
} else {
    Write-Host "SKIP live rebuild (no datapack at $dataRoot\$liveCase)"
}

Write-Host "== ALL CHECKS PASSED =="
