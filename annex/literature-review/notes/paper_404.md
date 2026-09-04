---
paper_id: 404
title: "STLGT: A Scalable Trace-Based Linear Graph Transformer for Tail Latency Prediction in Microservices"
authors:
  - Yongliang Ding
  - Qigong Bi
  - Peng Pu
year: 2026
venue: ""
doi: ""
arxiv_id: 2604.26422
url: "https://www.semanticscholar.org/paper/bd62ad90427d4803397394f2a2eb337114971e71"
pdf_path: data/pdfs/paper_404.pdf
read_date: 2026-05-11

category:
  - temporal_causal_analysis
  - distributed_system_monitoring
  - observability_data_analysis

method:
  family: deep_learning
  specific: linear graph transformer with decoupled temporal module
  inputs: []

ground_truth:
  source: ""
  external: false
  case_count: 0
  reproducible: false

evaluation:
  metrics: []
  baseline_compared: false
  has_uncertainty_quantification: false

claims:
  primary_contribution: A scalable graph transformer architecture that models trace spans as graphs to predict multi-step p95 tail latency with linear inference complexity.
  novelty_strength: moderate

limitations_authors_state: []

quality_flags:
  self_constructed_ground_truth: false
  comparison_table_only: false
  hobby_project_scale: false
  predictable_outcome: false

relevance:
  relevance_to_topic: adjacent
  must_cite: false
---

## Problem statement

Microservice systems require accurate prediction of end-to-end tail latency to enable proactive service level objective management. The challenge lies in modeling how latency propagates across service dependencies while accounting for non-stationary and bursty workload patterns. Existing approaches struggle to balance prediction accuracy with computational efficiency, particularly as the number of spans in distributed traces grows. The problem becomes more acute when systems need to forecast multiple steps ahead to support proactive interventions. Traditional methods either fail to capture long-range dependencies between services or incur prohibitive computational costs that prevent real-time deployment at scale.

## Method summary

STLGT operates as a per-API predictor that represents distributed traces as span graphs where nodes correspond to service spans and edges capture dependency relationships. The architecture consists of two main components working in tandem. The structure-aware linear graph transformer processes the span graph topology to propagate cross-service dependency information with computational complexity linear in the number of spans rather than quadratic as in standard transformers. This component uses a linearized attention mechanism specifically designed for graph-structured data. The second component is a decoupled temporal module that captures workload dynamics and temporal patterns independently from the structural propagation. This separation allows the model to handle non-stationary and bursty traffic patterns while maintaining efficiency. The system produces multi-step forecasts of p95 tail latency for each API endpoint by combining structural dependency information with temporal workload characteristics.

## Ground truth and evaluation

The evaluation uses three datasets including a personalized education microservice application, DeathStarBench benchmark suite, and production traces from Alibaba. The ground truth for tail latency prediction appears to be derived from actual observed p95 latency values in these systems, though the paper does not explicitly detail the labeling process. Performance is measured primarily using mean absolute percentage error comparing predicted versus actual p95 latencies across multiple forecast horizons. The baseline comparison focuses on PERT-GNN, showing STLGT achieves 8.5 percent lower MAPE on average. Inference efficiency is evaluated by measuring CPU inference time, demonstrating up to 12x speedup at span graph size of 32 nodes. Ablation studies examine the contribution of individual components by systematically removing the linear graph transformer or temporal module and measuring degradation in prediction accuracy, particularly under bursty traffic conditions.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. The evaluation scope is confined to three specific datasets which may not represent the full diversity of microservice architectures and workload patterns encountered in production environments. The maximum span graph size tested is 32 nodes after preprocessing Alibaba traces, leaving questions about scalability to even larger distributed systems with more complex call graphs. The focus on p95 tail latency as the sole prediction target means other important performance metrics are not addressed. The per-API prediction approach may not capture system-wide effects or interactions between multiple API endpoints experiencing simultaneous load.

## Gaps this paper opens

The work does not address how predicted tail latencies could be used for automated root cause analysis when SLO violations are forecasted. While the model identifies which services contribute to predicted latency through the graph structure, it does not provide mechanisms to trace back from predictions to underlying causes such as resource contention, cascading failures, or specific anomalous behaviors. The temporal module captures workload dynamics but does not explicitly model or identify the root causes of bursty traffic patterns. The relationship between predicted latency degradation and specific system faults or configuration issues remains unexplored. There is no discussion of how the learned dependency propagation patterns could inform fault localization or help operators understand why certain service paths exhibit elevated latency. The model operates as a black-box predictor without interpretability mechanisms that would connect predictions to actionable diagnostic insights.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic as it addresses temporal analysis and dependency modeling in cloud-native systems but focuses on prediction rather than root cause analysis. The span graph representation captures service dependency topology which is relevant for understanding how failures and performance issues propagate through microservice architectures. The temporal module's handling of workload dynamics relates to temporal analysis aspects of the thesis framework. However, the work stops at forecasting tail latency rather than diagnosing why latency violations occur or identifying root causes. The linear graph transformer's ability to propagate information across service dependencies could potentially be adapted for causal analysis by tracing how anomalies flow through the system. The per-API prediction approach and the separation of structural versus temporal factors provide architectural insights that could inform how a root cause analysis framework decomposes the problem space. The evaluation on production traces demonstrates practical applicability in real cloud-native environments similar to the thesis target domain.
