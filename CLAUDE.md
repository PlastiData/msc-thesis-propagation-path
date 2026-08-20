# Failure propagation paths with evidence

Public code and result pack for an MSc thesis (Alexis Marin, SRH Heidelberg, 2026). Given a seed service and a symptom, the pipeline builds a candidate propagation path. Every edge is labelled Observed, Supported, or Inferred with a re executable evidence reference. If the acceptance policy is not met, the output is refuse with a named reason. Refuse is a valid result.

## Folder map

| Path | Role |
|---|---|
| `analysis/cli.py` | CLI entry (`process_case`, `run`, `main`) |
| `analysis/pipeline/` | Core stages (see read order below) |
| `analysis/ground_truth.py`, `analysis/trace_graph.py` | Adapters used by the pipeline |
| `analysis/samples/` | Case id lists (`sample10`, `sample100`, `sample_all`) |
| `rankings/` | Upstream RCA rankings; source of the RCA seed. `output/` overrides it when present |
| `tests/` | Unit under `tests/unit/`, smoke under `tests/integration/` |
| `results/evidence_path_poc/` | Frozen HTML/JSON (path name kept stable) |
| `docs/` | Layout and reproduce notes |

`analysis/evidence_path_poc.py` is a thin shim that re exports `cli`. Prefer `cli.py`.

## Pipeline read order

1. `pipeline/reality.py` — load case, injection, symptom, traces, timeline  
2. `pipeline/graph.py` — candidate routes between seed and symptom  
3. `pipeline/evidence.py` — structural / statistical / temporal checks; classify edges  
4. `pipeline/judgment.py` — apply strict or relaxed policy; accept or refuse  
5. `pipeline/emit.py` — machine graph, human report, scorecard, HTML  

Supporting: `config.py` + `evidence_rules.json`, `fault_taxonomy.py` / `fault_types.py`, `algo_context.py`.

## Commands

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/python analysis/cli.py --case ts0-ts-order-service-stress-64c8cv --policy strict
python3 -m http.server 8765 -d results/evidence_path_poc/sample_all/strict
bash scripts/validate.sh
```

Datapack layout and Zenodo download: `docs/REPRODUCE.md`.

## Hard rules

- Never claim a "true causal path", "verified causal graph", "causal accuracy", or an exact PAVE reproduction. There is no process level ground truth.
- Do not commit `data/` or `output/`.
- Do not reintroduce `chain_poc`.
- Keep the on disk results path `results/evidence_path_poc/` stable (browsers and papers link there).
- `insufficient_evidence` / refuse is valid output, not a failure of the tool.
