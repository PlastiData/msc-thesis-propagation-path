# Pipeline runbook

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python analysis/cli.py --sample analysis/samples/sample10.txt --policy strict
.venv/bin/python analysis/cli.py --case ts0-ts-order-service-stress-64c8cv --policy strict
.venv/bin/python -m pytest tests/ -q
```

Stages live under `analysis/pipeline/`: reality → graph → evidence → judgment → emit. Rules: `pipeline/evidence_rules.json`. CLI: `analysis/cli.py`.

Frozen full pack outputs: `results/evidence_path_poc/sample_all/{strict,relaxed}/`

```bash
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict
```

Datapack and dual seed notes: `docs/REPRODUCE.md`. Provenance vs PAVE: `analysis/docs/PAVE_MAPPING.md`.
