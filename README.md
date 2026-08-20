# Evidence-backed failure propagation paths

MSc thesis code: reconstruct a candidate service-to-service failure path with every hop labelled **Observed / Supported / Inferred**, or **refuse** with a named reason when evidence is insufficient. Built on the [Fang et al. RCABench](https://doi.org/10.5281/zenodo.17105974) datapack (CC BY 4.0).

**In this repo:** `analysis/` (runnable POC), frozen `results/` for n=1422 (strict + relaxed), docs. **Not in this repo:** the 13 GB telemetry datapack (download from Zenodo) and ~15 GB upstream RCA algo outputs.

```bash
git clone https://github.com/PlastiData/msc-thesis-propagation-path.git
cd msc-thesis-propagation-path
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest analysis/test_evidence_poc.py -q
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict   # browse index.html
```

Data + re-run: see [docs/REPRODUCE.md](docs/REPRODUCE.md). License: [CC BY 4.0](LICENSE).
