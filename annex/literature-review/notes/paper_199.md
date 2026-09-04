---
paper_id: 199
title: "CHASE: A Causal Hypergraph based Framework for Root Cause Analysis in Multimodal Microservice Systems"
authors:
  - Ziming Zhao
  - Wang
  - Zhenwei
  - Tiehua Zhang
  - Zhishu Shen
  - Hai Dong
  - Lei
  - Zhen
  - Xingjun Ma
  - Xu
  - Gaowei
  - Ding
  - Zhijun
  - Yun Yang
year: 2024
venue: arXiv (Cornell University)
doi: 10.48550/arxiv.2406.19711
arxiv_id: ""
url: "https://openalex.org/W4400222627"
pdf_path: data/pdfs/paper_199.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - anomaly_detection

method:
  family: deep_learning
  specific: heterogeneous graph neural network with hypergraph learning
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
  primary_contribution: A framework that integrates multimodal observability data (traces, logs, metrics) into a causal hypergraph structure for root cause localization in microservice systems.
  novelty_strength: strong

limitations_authors_state: []

quality_flags:
  self_constructed_ground_truth: false
  comparison_table_only: false
  hobby_project_scale: false
  predictable_outcome: false

relevance:
  relevance_to_topic: core
  must_cite: false
---

## Problem statement

Enterprise microservice systems exhibit complex service invocation paths and dependencies that make prompt anomaly localization challenging during service failures. Traditional root cause analysis approaches struggle to effectively integrate the multiple modalities of observability data available in these systems, including distributed traces, application logs, and system monitoring metrics. The complexity of causal relationships between different service instances and the heterogeneous nature of the data sources create difficulties for existing methods to accurately pinpoint root causes. The problem is further compounded by the dynamic nature of service dependencies and the need to understand how anomalies propagate through invocation chains in distributed architectures.

## Method summary

CHASE constructs a multimodal invocation graph that encodes traces, logs, and metrics into representative embeddings. The framework first models the system using a heterogeneous graph where different node types represent service instances, metrics, and log entries. Anomaly detection is performed on instance nodes through attentive heterogeneous message passing, which aggregates information from adjacent metric and log nodes to identify abnormal behaviors. The core innovation lies in constructing a causal hypergraph where hyperedges explicitly represent the flow of causality between service instances. This hypergraph structure captures complex many-to-many causal relationships that cannot be represented by simple pairwise edges. The framework then applies hypergraph learning techniques to perform root cause localization by reasoning over these causal structures. The attention mechanism allows the model to weight the importance of different data modalities and neighboring nodes when making root cause predictions.

## Ground truth and evaluation

The framework is evaluated on two public microservice datasets with distinct characteristics. Performance is measured using standard root cause analysis metrics including A@1 (accuracy at top-1) and Percentage@1, which measure whether the true root cause appears as the top prediction. CHASE is compared against state-of-the-art baseline methods for root cause analysis in microservice systems. The evaluation demonstrates average performance gains of 36.2% for A@1 and 29.4% for Percentage@1 compared to the best performing baseline method. The use of two datasets with different attributes provides evidence of generalizability across different microservice system configurations. However, the paper does not explicitly detail how ground truth labels were obtained for these datasets or whether they represent real production failures versus injected faults.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. The abstract and evaluation focus primarily on demonstrating performance improvements over existing methods. The reliance on public datasets, while enabling reproducibility, may not fully capture the complexity and scale of real-world enterprise microservice deployments. The computational overhead of constructing and learning from hypergraph structures is not discussed, which could be relevant for real-time root cause analysis requirements. The paper does not address how the framework handles evolving service topologies or how it performs when the causal relationships change over time due to system updates or configuration changes.

## Gaps this paper opens

The framework assumes availability of comprehensive multimodal data including traces, logs, and metrics, but does not address scenarios where certain data modalities are incomplete or unavailable due to instrumentation gaps. The construction of the causal hypergraph appears to require understanding of service dependencies, but the paper does not clarify whether this topology is manually specified or automatically discovered, and how it adapts to dynamic changes. The temporal aspects of failure propagation are not explicitly modeled beyond the causal flow representation in hyperedges. There is no discussion of how the framework handles cascading failures where multiple root causes may exist simultaneously or where the causal structure itself becomes ambiguous. The interpretability of the hypergraph-based predictions and how operators can understand the reasoning behind root cause identification remains unclear.

## Relevance to the thesis topic

CHASE is highly relevant to the thesis topic as it directly addresses root cause analysis in cloud-native microservice systems using both dependency analysis and causal reasoning. The framework's use of service invocation graphs aligns with dependency topology analysis, while the causal hypergraph structure provides an explicit mechanism for modeling how failures propagate through the system. The integration of multimodal observability data (traces, logs, metrics) demonstrates a comprehensive approach to analyzing system behavior. However, CHASE does not emphasize temporal analysis as a distinct component, instead encoding temporal relationships implicitly through the causal hypergraph structure. The framework provides a concrete example of how graph-based representations can capture complex service dependencies and causal relationships for root cause localization. The strong empirical results suggest that combining heterogeneous data sources with explicit causal modeling is a promising direction for the thesis framework.
