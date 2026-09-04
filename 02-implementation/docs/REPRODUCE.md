# Reproduce

## What ships here vs Zenodo

| Artifact | Where |
|---|---|
| Thesis code and tests | this repo `analysis/`, `tests/` |
| Frozen dual seed results (n=1422) | `results/evidence_path_poc/sample_all/{strict,relaxed}/` |
| Upstream RCA rankings (44 MB) | this repo `rankings/` (per case `output.parquet` plus `meta/rcabench/dataset.perf.parquet`) |
| Telemetry datapack (~13.4 GB) | [Zenodo 10.5281/zenodo.17105974](https://doi.org/10.5281/zenodo.17105974) → `rcabench-absolute_anomaly.tar.gz` |

The heavy intermediate artefacts of the upstream algorithms (the `sdg.pkl` graph pickles, about 14.6 GB) are not needed. Only the ranking tables are read, and those ship here.

Unpack the Zenodo datapack so cases live at:

```text
data/rcabench-platform-v2/data/rcabench/<case-id>/{injection.json,conclusion.parquet,abnormal_traces.parquet,normal_traces.parquet}
```

That is the layout expected by `--data-root`.

## Install

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest tests/ -q
```

## Browse frozen results (no data required)

```bash
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict
# open http://127.0.0.1:8765/
```

Each case folder has `machine_graph.json`, `human_report.json`, `graph.html`. Rollups: `summary.json`, `index.html`.

## Re run with an injection seed (needs Zenodo data)

```bash
.venv/bin/python analysis/cli.py \
  --case ts0-ts-order-service-stress-64c8cv \
  --policy strict \
  --data-root data/rcabench-platform-v2/data/rcabench
```

Sample list:

```bash
.venv/bin/python analysis/cli.py \
  --sample analysis/samples/sample10.txt \
  --policy strict \
  --data-root data/rcabench-platform-v2/data/rcabench
```

Both seeds run. The injection seed comes from `injection.json`; the RCA seed is rank 1 of the best upstream algorithm, read from `rankings/`. A full local platform run under `output/rcabench-platform-v2/` is preferred when present. With neither, the RCA column reports `algo_output_missing` and the injection seed path still runs.

## Attribution

Fang et al. RCABench datapack and platform, CC BY 4.0: https://doi.org/10.5281/zenodo.17105974  
Thesis evidence model and acceptance policy: Alexis Marin, SRH Heidelberg, 2026.
