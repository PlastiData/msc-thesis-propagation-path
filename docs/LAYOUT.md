# Layout

```text
analysis/                    # runnable method
  evidence_path_poc.py       # CLI entry (filename kept for continuity)
  evidence/                  # Reality → Evidence → Judgment
  test_evidence_poc.py
  sample_*.txt
results/evidence_path_poc/
  sample_all/{strict,relaxed}/   # n=1422 frozen HTML and JSON
  sample10/                      # small browse set
docs/REPRODUCE.md
```

The Fang et al. platform `src/` is not vendored here. Download `rcabench-platform-feat-fse26.zip` from the same Zenodo record if you need `./main.py eval`.
