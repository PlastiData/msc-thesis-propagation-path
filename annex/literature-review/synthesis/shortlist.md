# Shortlist

## Accepted (all indicators PASS)

1. **Cross-Modal Dependency Graph Construction from Heterogeneous Telemetry** — Does a cross-modal dependency graph construction method that fuses structural information from traces, behavioral patterns from metrics, and semantic relationships from logs achieve higher accuracy in capturing runtime service dependencies compared to trace-only or static configuration-based approaches?
2. **Failure Propagation Chain Reconstruction for Root Cause Analysis in Cloud-Native Systems** — Does explicit temporal failure propagation chain reconstruction — identifying the ordered sequence of affected services and the time lags between them — produce higher Recall@5 and higher explainability ratings than static topology-based RCA on multi-service fault scenarios in the Train-Ticket and AIOps 2022 benchmarks?

## Refinable (no FAIL, at most 3 PARTIAL)

1. **Temporal Causal Discovery for Multi-Root Failures** — Does a temporal causal discovery algorithm that explicitly models propagation delays and time-lagged dependencies outperform static causal inference methods in identifying primary root causes when multiple simultaneous faults occur in microservice systems?
2. **Interpretable Failure Propagation Path Reconstruction** — Does a framework that combines temporal causal inference with dependency-aware path search and multi-modal evidence aggregation produce failure propagation explanations that operators rate as more complete, trustworthy, and actionable compared to root-cause-only methods?
3. **Adaptive Temporal Window Selection for Anomaly Correlation** — Does an adaptive temporal window selection algorithm that learns propagation delay distributions from historical incidents and system topology outperform fixed-window approaches in correlating causally-related anomalies across distributed services?
4. **Remediation Strategy Selection with Dependency-Aware Impact Analysis** — Does a remediation recommendation framework that simulates action propagation through service dependency graphs and predicts downstream impacts reduce unintended side effects and improve recovery time compared to root-cause-only remediation selection?
5. **LLM-Based Causal Reasoning Validation for RCA** — Do LLM-based RCA methods demonstrate genuine causal reasoning capabilities that generalize to novel failure patterns, or do they primarily perform pattern matching on training distribution, and under what conditions do they outperform statistical causal inference methods?

