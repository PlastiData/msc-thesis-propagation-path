# Reproduce one case

Telemetry is not in this repository. After downloading the Zenodo datapack:

```bash
cd 02-implementation
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
ln -sfn ../04-data/rankings rankings
.venv/bin/python analysis/cli.py \
  --case ts0-ts-order-service-stress-64c8cv \
  --policy strict \
  --data-root /path/to/rcabench-platform-v2/data/rcabench \
  --out-root results/_validation
```

Browse frozen results without a run: open `01-results/propagation-paths/strict/index.html`.
