# Data on this stick

| Location | Contents |
|---|---|
| 04-data/telemetry/rcabench-platform-v2/ | ~13 GB case telemetry (Fang et al., Zenodo DOI 10.5281/zenodo.17105974) |
| 04-data/rankings/ | RCA algorithm outputs used as seeds (output.parquet per case) |
| 01-results/ | Frozen HTML/JSON dashboards — enough to read results without a run |

No sdg.pkl graph pickles (14+ GB intermediate upstream artifacts; not needed here).

Rebuild one case: point --data-root at telemetry and symlink or copy rankings into 02-implementation/rankings/.
