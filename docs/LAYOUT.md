# Layout

```text
analysis/
  cli.py                 # CLI entry
  evidence_path_poc.py   # thin shim → cli (name kept for continuity)
  pipeline/              # reality → graph → evidence → judgment → emit
    evidence_rules.json
    fault_types.py
  ground_truth.py        # adapter
  trace_graph.py         # adapter
  samples/               # sample10.txt, sample100.txt, sample_all.txt
  docs/                  # PIPELINE.md, PAVE_MAPPING.md
rankings/                # upstream RCA rankings (44 MB), source of the RCA seed
  data/rcabench/<case>/<algo>/output.parquet
  meta/rcabench/dataset.perf.parquet
tests/
  conftest.py
  unit/
  integration/
results/evidence_path_poc/
  sample_all/{strict,relaxed}/   # n=1422 frozen HTML and JSON
  sample10/
docs/REPRODUCE.md
docs/LAYOUT.md
docs/figures/             # path example, channels, direction, pipeline, seed vs path
scripts/validate.sh
CLAUDE.md
```

Method diagrams under `docs/figures/` are linked from the root README so visitors see the chain, the horizontal/vertical edge model, and how ranking (AC@k) differs from Path Coverage.
