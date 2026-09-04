---
paper_id: 197
title: "From distributed tracing to proactive SLO management: a mini-review of trace-driven performance prediction for cloud-native microservices"
authors:
  - Miaopeng Yu
  - Haonan Liu
  - Jinran Du
  - Kequan Lin
  - Tao Dai
  - Yanzhe Fu
  - Chunyan Yang
year: 2026
venue: Frontiers in Computer Science
doi: 10.3389/fcomp.2026.1783945
arxiv_id: ""
url: "https://openalex.org/W7130384521"
pdf_path: data/pdfs/paper_197.pdf
read_date: 2026-05-11

category:
  - observability_data_analysis
  - temporal_causal_analysis
  - distributed_system_monitoring

method:
  family: other
  specific: survey of trace-driven prediction methods
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
  primary_contribution: A systematic review of trace-driven proactive SLO management techniques that predict performance violations before requests complete.
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

Cloud-native microservices architectures introduce complex and dynamic service dependencies that make performance management challenging. Resource contention, queue buildup, and downstream slowdowns propagate through call chains, amplifying end-to-end tail latency metrics such as p95 and p99 percentiles. These propagation effects increase the risk of Service Level Objective violations. Traditional approaches focus on post-hoc anomaly detection and root-cause analysis after problems have already impacted users. Industrial operations increasingly require proactive capabilities that can predict performance risks before requests complete, enabling preventive actions rather than reactive responses. The challenge lies in leveraging distributed tracing data to forecast SLO violations, predict tail-quantile latencies, issue early warnings from partial trace prefixes, and generate actionable signals for mitigation strategies.

## Method summary

This review synthesizes multiple modeling approaches for trace-driven proactive SLO management. Feature-based baselines extract statistical and structural features from trace data for classical machine learning models. Sequence models treat traces as temporal sequences of span events to capture execution patterns over time. Graph neural networks leverage the service dependency topology and call graph structure embedded in traces. Sequence-graph fusion approaches combine temporal dynamics with topological relationships to capture both execution order and service dependencies. Multimodal and causal extensions incorporate additional data sources beyond traces and attempt to model causal relationships between service behaviors. The review examines how these methods address practical deployment challenges including class imbalance in SLO violation datasets, sampling-induced missing spans in production traces, and topology drift as service architectures evolve.

## Ground truth and evaluation

The review discusses evaluation protocols for multiple prediction tasks. For SLO violation prediction, ground truth comes from comparing actual request latencies against predefined SLO thresholds, typically formulated as binary classification problems. Tail-quantile prediction tasks use observed latency distributions to establish ground truth for percentile forecasts. Prefix early warning evaluation measures how early models can detect potential violations from partial traces while maintaining precision constraints to avoid excessive false alarms. Actionable intermediate outputs are evaluated through bottleneck candidate ranking tasks where ground truth identifies which services contribute most to latency, and what-if estimation scenarios that assess counterfactual predictions. The review notes that evaluation must consider trade-offs between prediction accuracy, earliness of detection, and practical constraints like false positive rates that affect operational feasibility.

## Stated limitations

The review identifies several practical challenges that limit current approaches. Class imbalance poses significant difficulties because SLO violations are typically rare events in production systems, making it hard to train accurate predictors without specialized sampling or rebalancing techniques. Sampling-induced missing spans occur when production tracing systems sample only a fraction of requests to reduce overhead, resulting in incomplete trace data that degrades model performance. Topology drift happens as service architectures evolve through deployments and updates, causing models trained on historical data to become stale. The review also notes that many proposed methods lack thorough evaluation on deployment readiness, trustworthiness, and interpretability requirements necessary for industrial adoption.

## Gaps this paper opens

The review reveals several research gaps in trace-driven proactive SLO management. While various modeling approaches exist, there is limited understanding of which architectural choices work best under different operational constraints and system characteristics. The integration of causal reasoning with trace analysis remains underdeveloped, particularly for generating reliable what-if predictions and actionable mitigation recommendations. Handling dynamic topology changes and maintaining model accuracy over time requires more robust solutions than currently available. The review also highlights insufficient work on explainability and trustworthiness, which are critical for operators to understand and act on model predictions. Finally, there is a gap in standardized benchmarks and evaluation protocols that would enable fair comparison across different approaches and facilitate reproducible research.

## Relevance to the thesis topic

This review is adjacent to the thesis topic on root cause analysis in cloud-native systems using temporal and dependency analysis. The paper focuses on proactive prediction rather than post-hoc root cause analysis, but the underlying data structures and analytical approaches overlap significantly. Both domains rely on distributed tracing data that captures temporal execution patterns and service dependencies. The sequence-graph fusion methods discussed in the review directly align with the thesis emphasis on combining temporal and dependency analysis. The review's discussion of bottleneck candidate ranking and what-if estimation touches on aspects of root cause identification, though from a predictive rather than diagnostic perspective. Understanding proactive prediction methods provides context for how temporal and dependency patterns manifest before failures occur, which can inform root cause analysis frameworks. The practical challenges identified, particularly topology drift and missing spans, are equally relevant to root cause analysis systems operating on production trace data.
