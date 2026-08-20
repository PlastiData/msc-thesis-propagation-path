# Reproduce

## What ships here vs Zenodo

| Artifact | Where |
|---|---|
| Thesis code and tests | this repo `analysis/` |
| Frozen dual seed results (n=1422) | `results/evidence_path_poc/sample_all/{strict,relaxed}/` |
| Telemetry datapack (~13.4 GB) | [Zenodo 10.5281/zenodo.17105974](https://doi.org/10.5281/zenodo.17105974) → `rcabench-absolute_anomaly.tar.gz` |
| Upstream RCA ranking outputs | not shipped; dual seed numbers are frozen in `results/`; injection seed re runs need data only |

Unpack the Zenodo datapack so cases live at:

```text
data/rcabench-platform-v2/data/rcabench/<case-id>/{injection.json,conclusion.parquet,abnormal_traces.parquet,normal_traces.parquet}
```

That is the layout expected by `--data-root`.

## Install

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest analysis/test_evidence_poc.py -q
```

## Browse frozen results (no data required)

```bash
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict
# open http://127.0.0.1:8765/
```

Each case folder has `machine_graph.json`, `human_report.json`, `graph.html`. Rollups: `summary.json`, `index.html`.

## Re run with an injection seed (needs Zenodo data)

```bash
.venv/bin/python analysis/evidence_path_poc.py \
  --case ts0-ts-order-service-stress-64c8cv \
  --policy strict \
  --data-root data/rcabench-platform-v2/data/rcabench
```

Without local algo `output/` trees, the RCA column reports `algo_output_missing`; the injection seed path still runs. Full dual seed recompute needs those outputs (USB or local archive), not this GitHub tree.

## Attribution

Fang et al. RCABench datapack and platform, CC BY 4.0: https://doi.org/10.5281/zenodo.17105974  
Thesis evidence model and acceptance policy: Alexis Marin, SRH Heidelberg, 2026.
