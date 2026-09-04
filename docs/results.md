# Results (frozen on this stick)

Numbers copied from 01-results/propagation-paths/*/summary.json at pack time.

- **n = 1422** evaluable cases (Fang paper table often cites 1430).
- **Path coverage (strict, injection seed):** 73.7% (1048/1422).
- **Path coverage (strict, RCA seed):** 72.2% (1027/1422).
- **Relaxed sensitivity:** injection 88.7%, RCA 82.9% — not a second headline metric.
- **Agreement (strict):** same 15.5% (221), differ 48.0% (682). Descriptive only when both seeds built a path.
- **Suffix overlap:** see 02-implementation/analysis/tools/suffix_overlap.py against strict summary.

## How to read the dashboard

Open 01-results/propagation-paths/strict/index.html (not the case folders). Explorer lists ~1422 case folders first; the dashboard file sits below them.

Per case: machine_graph.json (machine-readable), human_report.json, graph.html.
