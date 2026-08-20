# Evidence path POC runbook

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python analysis/evidence_path_poc.py --sample analysis/sample10.txt --policy strict
.venv/bin/python analysis/evidence_path_poc.py --case ts0-ts-order-service-stress-64c8cv --policy strict
.venv/bin/python -m pytest analysis/test_evidence_poc.py -q
```

Frozen full-pack outputs: `results/evidence_path_poc/sample_all/{strict,relaxed}/`

```bash
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict
```

Datapack + dual-seed notes: `docs/REPRODUCE.md`. Provenance vs PAVE: `analysis/docs/PAVE_MAPPING.md`.
