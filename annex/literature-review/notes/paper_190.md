---
paper_id: 190
title: "Multi-Layer Causal Graphs for Distributed System Performance: Modeling Cross-Service Dependencies in Microarchitectures"
authors:
  - Sichen Liu
year: 2025
venue: Computer Science Bulletin
doi: 10.71465/csb161
arxiv_id: ""
url: "https://openalex.org/W7118780173"
pdf_path: data/pdfs/paper_190.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - temporal_causal_analysis

method:
  family: hybrid
  specific: multi-layer causal graph construction with causal inference
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
  primary_contribution: A hierarchical framework that constructs multi-layer causal graphs across infrastructure, metric, and invocation layers to model cross-service dependencies and enable root cause localization in microservice architectures.
  novelty_strength: moderate

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

Modern microservice architectures introduce significant complexity in performance management and fault diagnosis due to their distributed nature and dynamic service interactions. Traditional single-layer dependency analysis methods fail to capture the multi-faceted relationships that exist across different abstraction levels in these systems. The challenge lies in simultaneously modeling inter-service dependencies that span across services and intra-service dependencies within individual service components while accounting for infrastructure-level factors that influence performance. Existing approaches typically focus on one layer of abstraction, missing critical causal relationships that propagate across layers and lead to cascading failures or performance degradation. The dynamic nature of microservice deployments, where services scale and reconfigure frequently, further complicates the task of maintaining accurate dependency models for effective root cause analysis.

## Method summary

The framework constructs multi-layer causal graphs that operate across three distinct abstraction layers: infrastructure, metric, and invocation. The infrastructure layer captures hardware and platform-level dependencies such as compute resources, network topology, and storage systems. The metric layer models relationships between performance indicators including latency, throughput, error rates, and resource utilization metrics. The invocation layer represents service call patterns and request flow dependencies derived from distributed tracing data. The methodology integrates causal inference techniques to establish directional relationships between nodes within and across these layers, distinguishing correlation from causation. The framework analyzes service invocation patterns to understand request propagation, examines performance metrics to identify anomalous behaviors, and incorporates infrastructure telemetry to account for resource-level constraints. The resulting multi-layer graph structure enables the system to trace anomaly propagation paths by following causal edges across layers, identifying where performance issues originate and how they cascade through dependent services. The approach maintains dynamic models that adapt as the microservice topology evolves through service additions, removals, or reconfigurations.

## Ground truth and evaluation

The experimental evaluation uses benchmark microservice applications as testbeds, though the paper does not specify which particular benchmark suites were employed. Ground truth for root cause localization appears to be established through known fault injection scenarios or labeled anomaly cases within these benchmark applications. The evaluation measures precision and recall metrics for root cause identification, comparing the multi-layer approach against traditional single-layer methods. Results demonstrate an average precision improvement of 23% and recall enhancement of 18% over baseline approaches. The framework's scalability is assessed by measuring performance consistency as system complexity increases with additional services and dependencies. The evaluation methodology appears to test the system's ability to correctly identify the true root cause among candidate services or components when anomalies are introduced. However, the paper does not provide detailed information about the specific benchmark applications used, the number of services tested, the types of faults injected, or the exact procedures for establishing ground truth labels.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed approach. No discussion is provided regarding computational overhead associated with maintaining multi-layer causal graphs in large-scale deployments. The scalability claims mention consistent performance as complexity increases, but specific bounds or breaking points are not identified. There is no acknowledgment of potential challenges in causal inference accuracy when dealing with noisy telemetry data or incomplete observability. The paper does not address how the framework handles transient dependencies or ephemeral services common in modern cloud-native environments. Limitations regarding the types of anomalies the system can effectively diagnose or scenarios where multi-layer modeling may not provide advantages over simpler approaches are not discussed. The generalizability of the 23% precision and 18% recall improvements across different application domains or deployment environments remains unexamined.

## Gaps this paper opens

The paper does not provide sufficient detail about the causal inference algorithms employed, leaving unclear how causality is distinguished from correlation in practice and what assumptions underlie the causal discovery process. The specific mechanisms for integrating information across the three layers and resolving conflicts when different layers suggest contradictory causal relationships remain unexplained. The temporal dimension of causality is mentioned through anomaly propagation paths but not thoroughly developed, raising questions about how time-lagged dependencies and temporal ordering constraints are incorporated into the graph structure. The paper lacks discussion of how the framework handles uncertainty in causal relationships or probabilistic dependencies. The adaptation mechanism for dynamic topology changes is described at a high level without implementation details. The relationship between the multi-layer graph representation and existing service mesh or observability platform data models is not explored. Finally, the paper does not address how domain knowledge or operator expertise could be incorporated into the causal graph construction process or how the system explains its root cause conclusions to human operators.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in distributed systems through dependency modeling and causal analysis. The multi-layer causal graph approach aligns closely with the thesis emphasis on both temporal and dependency analysis by explicitly modeling service dependencies across multiple abstraction layers and tracing anomaly propagation paths. The framework's hierarchical structure that separates infrastructure, metric, and invocation layers provides a concrete example of how dependency topology can be organized and analyzed for root cause localization. The integration of causal inference techniques demonstrates one approach to establishing directional relationships that go beyond simple correlation, which is essential for accurate root cause identification. The paper's focus on microservice architectures directly corresponds to cloud-native systems, the thesis's target domain. However, the paper's treatment of temporal aspects appears less developed than dependency modeling, suggesting the thesis could strengthen temporal analysis components. The experimental validation on benchmark applications and the reported improvements in precision and recall provide useful reference points for evaluating the thesis framework's effectiveness against existing approaches.
