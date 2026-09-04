# Failure propagation paths with evidence

Public code and result pack for an MSc thesis (Alexis Marin, SRH Berlin, 2026).

Folder layout matches the committee USB handover (without the written thesis PDF and without the 13 GB telemetry pack).

## Read first

1. **`01-results/propagation-paths/strict/index.html`** — main dashboard (n=1422)
2. **`docs/`** — folder map, pipeline, labels, headline numbers
3. **`02-implementation/`** — curated code, tests, `scripts/validate.sh`

| Path | What it is |
|---|---|
| `01-results/` | Frozen dashboards + LLM second-opinion pilot |
| `02-implementation/` | Thesis pipeline (CLI, tests) |
| `03-methodology/` | Method figures |
| `04-data/rankings/` | RCA seeds only — **no** case telemetry |
| `05-upstream-benchmark/` | Fang et al. evaluation platform (unmodified subset) |
| `annex/` | Literature notes + investigation HTML |
| `docs/` | Plain-English pack notes |

**Not here:** thesis Markdown/PDF/DOCX (private monorepo); ~13 GB RCABench telemetry ([Zenodo](https://doi.org/10.5281/zenodo.17105974)).

## View results (no install)

```bash
python3 -m http.server 8765 -d 01-results/propagation-paths/strict
# open http://127.0.0.1:8765/
```

Relaxed twin: `01-results/propagation-paths/relaxed/`. LLM pilot: `01-results/llm-second-opinion/relaxed/`.

## Validate (optional)

```bash
cd 02-implementation
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
# if venv fails on some filesystems, copy this folder to a native Linux path first
bash scripts/validate.sh
```

`validate.sh` expects this repository layout (sibling `01-results/`, `04-data/`).

## Method in one line

Build a candidate service path from a seed (injection or RCA rank-1) to a symptom; label every hop Observed / Supported / Inferred with re-executable evidence, or return `insufficient_evidence` with a named gap. Dual-seed agreement is descriptive — not causal accuracy.
