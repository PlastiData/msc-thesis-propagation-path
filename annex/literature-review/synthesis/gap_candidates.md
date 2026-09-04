# Gap candidates

### Gap candidate 1. Temporal Causal Discovery for Multi-Root Failures

Statement. Existing RCA methods assume single root causes or do not model temporal propagation delays when multiple simultaneous faults cascade through service dependencies, leaving unclear how to distinguish primary from secondary failures in time-ordered event sequences.

Evidence.
- paper_25: Dynamic causality-aware framework shows strong results but does not clarify how it handles completely novel fault patterns or multiple concurrent root causes
- paper_165: CIRCA formulates RCA as intervention recognition but does not model temporal dynamics beyond comparing distributions, leaving open questions about propagation delays
- paper_190: Multi-layer causal graphs mentioned but temporal dimension of causality not thoroughly developed, unclear how time-lagged dependencies are handled
- paper_200: Reinforcement learning for graph pruning does not explore how temporal patterns in failure propagation might inform pruning strategy

Research question. Does a temporal causal discovery algorithm that explicitly models propagation delays and time-lagged dependencies outperform static causal inference methods in identifying primary root causes when multiple simultaneous faults occur in microservice systems?

External validation source. Train-Ticket benchmark with injected multi-fault scenarios (estimated 50+ distinct multi-root failure cases) and AIOps Challenge datasets with documented cascading failure timestamps

Methodology fit. The framework can use distributed tracing timestamps and metric time-series to establish temporal ordering independently of causal labels, then validate discovered causal graphs against known fault injection sequences where ground truth propagation is documented externally.

Hobby project test. Implementing temporal causal discovery algorithms that handle non-stationary time-series, variable propagation delays, and confounding factors across distributed services requires substantial algorithmic development, large-scale trace data processing infrastructure, and rigorous statistical validation beyond weekend scope.

### Gap candidate 2. Cross-Modal Dependency Graph Construction from Heterogeneous Telemetry

Statement. Current service dependency discovery methods rely primarily on traces or static configuration, but do not systematically integrate logs, metrics, and traces to construct dependency graphs that capture both structural and behavioral relationships, leaving gaps in dynamic topology inference.

Evidence.
- paper_31: Multi-relational service dependency graphs distinguish causal relationships but do not address how graphs are constructed or maintained in dynamic environments
- paper_193: LLM-based knowledge graph construction from telemetry but relationship between LLM-constructed graph and traditional static models unexplored, validation mechanisms unclear
- paper_199: Causal hypergraph structure integrates multimodal data but does not clarify whether topology is manually specified or automatically discovered
- paper_121: Topology-aware RCA does not address how to automatically construct and maintain end-to-end service topology in dynamic cloud environments
- paper_: 

Research question. Does a cross-modal dependency graph construction method that fuses structural information from traces, behavioral patterns from metrics, and semantic relationships from logs achieve higher accuracy in capturing runtime service dependencies compared to trace-only or static configuration-based approaches?

External validation source. Sock-Shop and Online-Boutique microservice benchmarks with documented ground-truth service dependencies (20-30 services each), plus chaos engineering experiments where dependency changes are externally controlled and timestamped

Methodology fit. Ground truth dependencies can be established through instrumented service mesh configurations and deployment manifests, independent of the telemetry-based discovery process, allowing objective validation of inferred versus actual call graphs and data flow relationships.

Hobby project test. Building a system that parses heterogeneous telemetry formats, aligns temporal windows across modalities, implements graph fusion algorithms, handles dynamic topology updates, and validates against multiple benchmark systems requires significant engineering effort and distributed systems expertise.

### Gap candidate 3. Interpretable Failure Propagation Path Reconstruction

Statement. While many RCA methods identify root causes, they do not reconstruct complete, human-interpretable failure propagation paths showing how anomalies cascade through service dependencies with supporting evidence from multiple telemetry sources, limiting operator trust and actionability.

Evidence.
- paper_171: Hybrid RCA framework reconstructs fault propagation trajectories but lacks detailed algorithmic specifications and does not compare with existing methods quantitatively
- paper_238: ErrorPrism reconstructs multi-hop error propagation paths but does not discuss interpretability or explainability of the reconstruction process, particularly for 3% failure cases
- paper_246: Multi-modal RCA with LLM reasoning provides remediation guidance but integration of statistical causal inference with LLM interpretation not fully explored
- paper_86: Automated benchmark reveals dramatic performance gap but does not analyze which propagation patterns prove most challenging or why certain model architectures fail

Research question. Does a framework that combines temporal causal inference with dependency-aware path search and multi-modal evidence aggregation produce failure propagation explanations that operators rate as more complete, trustworthy, and actionable compared to root-cause-only methods?

External validation source. RCAEval benchmark with hierarchical ground-truth labels (estimated 100+ complex propagation scenarios) and human operator evaluation study with 20+ SREs rating explanation quality on standardized incidents from production postmortems

Methodology fit. Ground truth propagation paths are established through fault injection experiments with instrumented cascading failures, independent of the reconstruction algorithm, while human evaluation provides external validation of interpretability and actionability beyond accuracy metrics.

Hobby project test. Developing algorithms for multi-hop path search in dynamic graphs, implementing evidence aggregation across heterogeneous telemetry, designing human evaluation protocols, recruiting and training SRE participants, and conducting rigorous user studies requires substantial research infrastructure and time.

### Gap candidate 4. Adaptive Temporal Window Selection for Anomaly Correlation

Statement. Existing temporal analysis methods use fixed or heuristic time windows for correlating anomalies across services, but do not adaptively determine optimal windows based on system characteristics and failure types, leading to missed correlations or spurious associations.

Evidence.
- paper_11: Dynamic time warping for temporal alignment improves prediction but does not explain causal relationships or identify responsible components, temporal windows not discussed
- paper_31: Temporal causality constraints mentioned but not detailed, leaving open questions about how temporal windows are determined and varying propagation delays handled
- paper_119: Multi-layer telemetry fusion framework does not explain how temporal dependencies or failure propagation patterns are modeled
- paper_225: Correlation analysis does not address how temporal delays between root causes and observable symptoms are handled

Research question. Does an adaptive temporal window selection algorithm that learns propagation delay distributions from historical incidents and system topology outperform fixed-window approaches in correlating causally-related anomalies across distributed services?

External validation source. AIOps Challenge datasets with documented incident timelines (estimated 200+ incidents with known propagation delays) and controlled chaos experiments in Kubernetes clusters where failure injection timing is externally recorded

Methodology fit. Ground truth temporal relationships are established through fault injection timestamps and postmortem analysis independent of the window selection algorithm, allowing objective measurement of correlation accuracy and false positive rates across different delay patterns.

Hobby project test. Implementing machine learning models for delay distribution estimation, developing adaptive windowing algorithms that handle non-stationary propagation patterns, processing large-scale time-series data, and conducting extensive parameter sensitivity analysis requires significant computational resources and algorithmic sophistication.

### Gap candidate 5. Remediation Strategy Selection with Dependency-Aware Impact Analysis

Statement. Current remediation recommendation systems suggest fixes based on root cause identification but do not perform dependency-aware impact analysis to predict how remediation actions propagate through the system, risking unintended consequences or incomplete recovery.

Evidence.
- paper_87: Multi-agent AI framework executes automated remediation but does not provide specifics on how reinforcement learning agents are trained safely or how action space is constrained
- paper_245: Graduated autonomy remediation mentioned but not detailed, unclear how automation decisions are made and what safety constraints are enforced
- paper_252: Compliance-bound autonomous AIOps focuses on remediation execution but provides limited insight into diagnostic reasoning that precedes remediation decisions
- paper_270: StepFly automates troubleshooting guide execution but does not explore how automated results feed into causal reasoning or how actions affect dependent services

Research question. Does a remediation recommendation framework that simulates action propagation through service dependency graphs and predicts downstream impacts reduce unintended side effects and improve recovery time compared to root-cause-only remediation selection?

External validation source. Production incident postmortems from open-source projects (estimated 50+ cases with documented remediation attempts and outcomes) and controlled remediation experiments in staging environments where impact can be measured independently

Methodology fit. Ground truth remediation outcomes are established through actual production incident resolutions and controlled experiments where system state is monitored independently, allowing validation of predicted versus actual impacts without circular reasoning.

Hobby project test. Building simulation models of service dependencies, implementing impact propagation algorithms, integrating with remediation execution frameworks, conducting controlled experiments across multiple failure scenarios, and analyzing complex multi-service recovery patterns requires extensive distributed systems engineering and experimental infrastructure.

### Gap candidate 6. LLM-Based Causal Reasoning Validation for RCA

Statement. Recent LLM-based RCA methods show promising results but lack rigorous validation of whether LLMs perform genuine causal reasoning versus pattern matching, and do not establish when LLM-based approaches outperform statistical causal inference methods.

Evidence.
- paper_246: Multi-modal RCA combines statistical causal inference with LLM reasoning but does not fully explore when each approach should dominate or how to optimally balance them
- paper_259: LLM reasoning over multi-modal telemetry lacks concrete evaluation of practical effectiveness and reliability in production environments
- paper_266: Multi-agent LLM system does not discuss how system handles temporal dependencies and causal relationships in incident propagation
- paper_274: In-context learning with GPT-4 does not explain how relevant examples are selected or which incident types benefit most from this approach

Research question. Do LLM-based RCA methods demonstrate genuine causal reasoning capabilities that generalize to novel failure patterns, or do they primarily perform pattern matching on training distribution, and under what conditions do they outperform statistical causal inference methods?

External validation source. Controlled experiments with synthetic causal graphs where ground truth causal relationships are known (estimated 100+ graph structures), plus out-of-distribution test cases from production incidents not represented in training data, validated against established causal discovery algorithms

Methodology fit. Ground truth causal relationships are established through synthetic graph generation and controlled experiments independent of LLM predictions, while out-of-distribution testing and comparison with statistical methods provides external validation of generalization versus memorization.

Hobby project test. Designing rigorous causal reasoning experiments, generating diverse synthetic causal scenarios, implementing multiple baseline causal inference methods, conducting extensive prompt engineering and hyperparameter tuning, analyzing failure modes across distribution shifts, and performing statistical significance testing requires substantial machine learning and causal inference expertise.

### Gap candidate 7. Failure Propagation Chain Reconstruction for Root Cause Analysis in Cloud-Native Systems

Statement. This work studies how failures evolve over time between dependent services and evaluates whether temporal propagation analysis improves explainability and root cause understanding in distributed cloud-native systems.

Evidence.
- paper_171: Reconstructs fault propagation trajectories using structural, semantic, and temporal symptom correlation but does not formally define propagation chain quality metrics or evaluate chain completeness against ground truth.
- paper_190: Builds multi-layer causal graphs across infrastructure, metric, and invocation layers but does not explicitly model the time-ordered sequence of failure propagation steps between dependent services.
- paper_200: Applies reinforcement learning to prune service dependency graphs for RCA but treats the graph statically and does not study how failure propagation evolves along the graph over time.
- paper_165: Frames RCA as intervention recognition in a Causal Bayesian Network but models root cause as a static distribution shift rather than a temporal chain of propagating faults across services.
- paper_168: Multi-granularity causal inference with Shapley attribution but focuses on blame assignment at a single time point and does not reconstruct the ordered sequence through which a failure reaches downstream services.

Research question. Does explicit temporal failure propagation chain reconstruction — identifying the ordered sequence of affected services and the time lags between them — produce higher Recall@5 and higher explainability ratings than static topology-based RCA on multi-service fault scenarios in the Train-Ticket and AIOps 2022 benchmarks?

External validation source. Train-Ticket benchmark (64 services, 212 metrics, documented cascading fault injection scenarios) and AIOps 2022 dataset (100+ multi-service incidents with timestamped ground truth propagation sequences), both publicly available with independent ground truth.

Methodology fit. The approach applies time-windowed Granger causality and dependency-graph traversal over distributed traces. Ground truth propagation sequences come from the independently published Train-Ticket and AIOps 2022 benchmarks — the researcher did not construct the fault scenarios, so evaluation is not circular. Ablation studies comparing temporal versus static graph traversal directly test the specific contribution of temporal ordering.

Hobby project test. Requires implementing a temporal graph traversal engine integrated with OpenTelemetry trace ingestion, validating chain reconstruction against two independent multi-service benchmarks each with distinct fault types, and running controlled ablations — this cannot be done in a weekend.

