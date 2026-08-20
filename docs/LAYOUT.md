# Layout

```text
analysis/                 # runnable evidence POC
  evidence_path_poc.py    # CLI entry
  evidence/               # Reality → Evidence → Judgment
  test_evidence_poc.py
  sample_*.txt
results/evidence_path_poc/
  sample_all/{strict,relaxed}/   # n=1422 frozen HTML+JSON
  sample10/                      # small browse set
docs/REPRODUCE.md
```

Upstream Fang et al. platform `src/` is **not** vendored here. Download `rcabench-platform-feat-fse26.zip` from the same Zenodo record if you need `./main.py eval`.
