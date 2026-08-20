# PAVE mapping (provenance record)

PAVE-informed reconstruction only. This table records what OpenRCA 2.0 / PAVE
(arXiv 2606.27154v2) specifies, what the Fang et al. TrainTicket datapacks expose,
what this POC implements, and every deliberate deviation. It is **not** a claim of
exact PAVE reproduction. There is no released process-level ground truth here.

Sources: local paper notes
`litreview/notes/OpenRCA_2.0_From_Outcome_Labels_to_Causal_Process_Supervision.md`.

| PAVE element | Available in Fang data | POC implementation | Deviation or missing detail |
|---|---|---|---|
| §2 forward verification from known intervention | `injection.json` (fault type, window, display_config injection_point, ground_truth labels) | Reality layer reads injection facts via `ground_truth.injected_targets` + fault_type / start / end | Prefer `target_service` / `server_address`; may disagree with injection_name for network partition (e.g. mysql→service). Not PAVE's unpublished intervention parser |
| §2.2 Structural pruning over dependency graph G | No prebuilt `edges`/`nodes` files; parent-child spans + k8s attrs | Horizontal edges from abnormal (and normal) span parent/child; vertical from pod/service/node/container attrs present in telemetry | Span-to-service collapse is our deterministic `service_name` rule (PAVE's unpublished). No full cluster topology invented. No time-expanded DFS with state alphabet Σ |
| §2.2 / Table 7 propagation rule set R (H-01…H-07, vertical, first-hop, cross-channel) | Trace status/duration; metrics CPU/mem; logs | Horizontal RPC cascade only for path search (callee→caller effect). Vertical placement edges when attrs exist. Rules live in `evidence_rules.json` | Full Table 7 state machine not reproduced; rule confidence 0.8 and per-rule overrides unpublished → omitted |
| Tables 5–6 fault taxonomy (Chaos category, target layer, fault_kind) | `injection.json` `fault_type` int (= `FAULT_TYPES` index) | Static lookup in `investigation/lib/fault_types.py`; embedded on reality/scorecard; index accept/refuse stratified by layer and kind | Stratification uses **injection taxonomy**, not Table 7 rule firing and not a detected error type |
| §2.3 joint screen: structural ∧ statistical ∧ temporal | Normal + abnormal metrics/traces/logs; conclusion.parquet | Per-edge checks `pass`/`fail`/`unknown`; classification Observed/Supported/Inferred from check table; acceptance presets strict/relaxed | PAVE drops failing cases from the released artifact; we **keep** rejected cases and report Rejection Profile. Labels are evidence strength, not verified causality |
| Appendix D.5 hyperparameters (∆ windows, Z>3σ, max 5 hops, revisit ≤2) | Same telemetry windows (~4 min normal / abnormal) | Max hops 5, revisit ≤2 in path search; Z-score / percentile / latency multiplier in rules JSON | Adaptive latency τ(cv,…) formula unpublished in usable constants → fixed latency multiplier. State detection windows 3s/5s not used (case already windowed) |
| Appendix D.8 detectors (Z-score, percentile, adaptive latency) | Gauge metrics, counters, HTTP/JVM latency | Z-score for gauge-like; percentile for count-like; fixed multiplier for latency; each may return `unknown` | Adaptive formula not copied. `unknown` never promoted to `pass` (respects temporal-gate falsification) |
| Appendix E.1 two-annotator audit (94/100) | N/A locally | Manual audit of evidence references on 3 sample10 cases (post-run) | Audit checks extraction correctness, not causal truth; no PAVE annotator protocol |
| Appendix F.3 CausalGraph / AgentRCAOutput schemas | No `causal_graph.json` in Fang cases | `machine_graph.json` with reality / candidate_graph / judgment / evidence_registry; human_report derived | Different schema: evidence_level + judgment status instead of verified CausalGraph. No LLM agent SQL answers |
| Validity threats (unpublished constants, no GT graphs, TrainTicket-only here) | Local TrainTicket split only | Documented here and in run manifest `config_hash` | Cannot claim Table-2 comparability; Path Coverage ≠ Path Reachability |

## Hand inventory — `ts4-ts-basic-service-request-delay-rxfqg2`

Checked against live datapack + `output_charts/telemetry_inventory/sample100/summary.md`.

| Artifact | Present | Columns / fields confirmed for rules |
|---|---|---|
| `injection.json` | yes | `fault_type` (7=request_delay), `start_time`, `end_time`, `ground_truth.{service,pod,container}`, `display_config.injection_point.{app_name,server_address,route,method}` → injected target **`ts-station-service`** |
| `conclusion.parquet` | yes | `SpanName`, `Issues`, `AbnormalAvgDuration`, `NormalAvgDuration`, `AbnormalSuccRate`, `NormalSuccRate`, P90/P95/P99 — symptom policy input |
| `abnormal_traces.parquet` / `normal_traces.parquet` | yes | `time`, `trace_id`, `span_id`, `parent_span_id`, `span_name`, `attr.span_kind`, `service_name`, `duration`, `attr.status_code`, `attr.k8s.pod.name`, `attr.k8s.service.name`, `attr.k8s.namespace.name`, HTTP method/status |
| `abnormal_metrics.parquet` (+ sum/histogram, normal twins) | yes | `time`, `metric`, `value`, `service_name`, `attr.k8s.node.name`, `attr.k8s.pod.name`, `attr.k8s.container.name`, deployment/replicaset/statefulset, Hubble src/dst |
| `abnormal_logs.parquet` / `normal_logs.parquet` | yes | `time`, `level`, `service_name`, `message`, k8s pod/service/namespace, optional trace/span ids |
| `env.json` | yes | environment metadata (not required by frozen rules) |
| Separate edges/nodes parquet | **no** | Derive call edges from span parent/child; vertical from k8s attrs only |

Flagged conclusion endpoints on this case (Issues non-empty): preserve, travel2 trips/left, travelPlan/minStation — all on `ts-ui-dashboard` hosts. Trace k8s attrs include **pod + service**, not node/container on spans; node/container appear on **metrics**.
