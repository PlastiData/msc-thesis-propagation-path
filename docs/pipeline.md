# Pipeline (what the code does)

1. **Seed.** Start from the injected service (known fault) or RCA rank-1 (algorithm guess).
2. **Reality.** Read case telemetry: injection.json, traces, metrics, logs, placement.
3. **Graph.** Build candidate horizontal hops between services. Pod/node links are context only.
4. **Evidence.** Label each hop with structural, statistical, and temporal checks. Every pointer is re-executable (file + query).
5. **Judgment.** Strict policy keeps only paths where every hop is Observed (no Inferred). Relaxed allows up to two Inferred hops. Otherwise return insufficient_evidence and name what is missing.

Entry point: 02-implementation/analysis/cli.py. Tests: 02-implementation/tests/.
Dual seed (injection vs RCA) is the headline experiment — not a second reconstruction algorithm.
