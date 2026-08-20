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
tests/
  conftest.py
  unit/
  integration/
results/evidence_path_poc/
  sample_all/{strict,relaxed}/   # n=1422 frozen HTML and JSON
  sample10/
docs/REPRODUCE.md
docs/LAYOUT.md
scripts/validate.sh
CLAUDE.md
```

The Fang et al. platform `src/` is not vendored here. Download `rcabench-platform-feat-fse26.zip` from the same Zenodo record if you need `./main.py eval`.
