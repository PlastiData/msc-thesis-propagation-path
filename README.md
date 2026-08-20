# Failure propagation paths

This repository is the public code and result pack for an MSc thesis (Alexis Marin, SRH Heidelberg, 2026).

**What the method does.** In a cloud native microservice failure, it builds a candidate path from a seed service to a symptom service. Every hop is labelled Observed, Supported, or Inferred, with a pointer back to the telemetry that supports the label. If the evidence is too weak for the chosen acceptance policy, it returns refuse and names the reason (for example weak hops, or no connected route). That refusal is a valid output, not a crash.

**What you will find here**

| Path | What it is |
|---|---|
| `analysis/` | Python implementation: build the path, label edges, apply strict or relaxed policy, write HTML and JSON |
| `results/evidence_path_poc/sample_all/` | Frozen outputs for 1422 benchmark cases, under `strict/` and `relaxed/` (open `index.html`) |
| `results/evidence_path_poc/sample10/` | Small subset for a quick look |
| `docs/REPRODUCE.md` | How to install, browse results, download data, and re run a case |
| `scripts/validate.sh` | Checks that the tree is complete and tests pass |

**What is not here.** The ~13 GB RCABench telemetry pack and the ~15 GB upstream ranking outputs. Download the datapack from Zenodo ([DOI 10.5281/zenodo.17105974](https://doi.org/10.5281/zenodo.17105974), CC BY 4.0). The frozen dual seed numbers in `results/` already include both injection seed and RCA seed columns.

**Run**

```bash
git clone https://github.com/PlastiData/msc-thesis-propagation-path.git
cd msc-thesis-propagation-path
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest analysis/test_evidence_poc.py -q
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict
```

Open http://127.0.0.1:8765/ for the case queue. License: [CC BY 4.0](LICENSE).
