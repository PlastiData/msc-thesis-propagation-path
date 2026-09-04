---
paper_id: 184
title: "Sage: Using Unsupervised Learning for Scalable Performance Debugging in Microservices"
authors:
  - Yu Gan
  - Mingyu Liang
  - Sundar Dev
  - David Lo
  - Christina Delimitrou
year: 2021
venue: arXiv (Cornell University)
doi: 10.48550/arxiv.2101.00267
arxiv_id: ""
url: "https://openalex.org/W3118353567"
pdf_path: data/pdfs/paper_184.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - anomaly_detection

method:
  family: classical_ml
  specific: unsupervised clustering with dependency graph analysis
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
  primary_contribution: An unsupervised machine learning system that identifies root causes of QoS violations in microservices by analyzing service dependencies and applying corrective actions without requiring labeled training data.
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

Microservice architectures introduce significant challenges for performance debugging because dependencies between services create backpressure effects and cascading quality-of-service violations. When one microservice experiences degraded performance, it can propagate through the dependency graph affecting multiple downstream services, making it difficult to identify which service is the actual root cause. Traditional monitoring approaches struggle with this complexity because they either require extensive labeled datasets for supervised learning or fail to capture the intricate relationships between services. The problem is further complicated by the dynamic nature of cloud deployments where services scale elastically and workload patterns change continuously. Manual debugging becomes impractical at scale, necessitating automated systems that can identify root causes online without human intervention or pre-labeled training examples.

## Method summary

Sage employs unsupervised machine learning to identify root causes of performance degradation in microservice applications. The system collects performance metrics from all microservices in an application and constructs a dependency graph representing the relationships between services. It uses unsupervised clustering algorithms to group similar performance patterns and identify anomalous behavior without requiring labeled training data. The approach captures how performance issues propagate through service dependencies by analyzing metrics across the entire call graph rather than examining services in isolation. When a QoS violation is detected, Sage traces the anomaly backward through the dependency graph to identify the originating service. The system then applies corrective actions such as resource reallocation or service scaling to remediate the identified root cause. The unsupervised nature of the approach allows Sage to adapt to new performance patterns and deployment configurations without retraining on labeled datasets.

## Ground truth and evaluation

The ground truth for evaluation is established through controlled fault injection experiments where the authors deliberately introduce performance degradations into specific microservices and verify whether Sage correctly identifies those services as root causes. Experiments are conducted on both dedicated local clusters and large-scale deployments on Google Compute Engine using real microservice applications. The primary evaluation metric is accuracy in root cause identification, measuring the percentage of cases where Sage correctly pinpoints the service responsible for QoS violations. The system achieves over 93% accuracy across different experimental configurations. Additional evaluation examines the effectiveness of corrective actions by measuring whether QoS is restored after Sage applies remediation. The experiments test various types of performance degradations including CPU contention, memory pressure, and network bottlenecks. The evaluation also assesses scalability by deploying on clusters of different sizes and measuring the overhead introduced by Sage's monitoring and analysis components.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the reliance on unsupervised learning means the system may struggle with novel or rare failure modes that do not cluster well with historical patterns. The accuracy of 93% while high still indicates that approximately 7% of root causes are misidentified, which could lead to incorrect remediation actions that fail to resolve or potentially worsen performance issues. The dependency graph construction assumes that service relationships can be accurately inferred from observed communication patterns, which may not capture all implicit dependencies or correctly represent complex conditional dependencies. The corrective actions are limited to resource reallocation and scaling, which may not address all types of root causes such as software bugs, configuration errors, or external dependencies. The evaluation focuses on specific types of performance degradations and may not generalize to all possible failure scenarios in production environments.

## Gaps this paper opens

The paper does not address how temporal patterns in performance degradation evolve over time or how root causes manifest differently across various time scales. While Sage captures dependencies between services, it does not explicitly model how failures propagate temporally through the system or distinguish between immediate versus delayed effects. The unsupervised clustering approach may miss subtle causal relationships that require understanding the temporal ordering of events rather than just spatial patterns across services. The system does not incorporate semantic information about what each microservice does or how business logic flows through the application, relying purely on performance metrics and communication patterns. There is no discussion of how Sage handles transient issues versus persistent problems or how it adapts when the application topology changes due to deployments or reconfigurations. The integration of multiple data modalities such as logs, traces, and metrics is not explored, leaving open questions about whether combining these sources could improve root cause accuracy beyond the 93% achieved.

## Relevance to the thesis topic

This paper is directly relevant to the thesis topic as it addresses root cause analysis in cloud-native microservice systems using dependency analysis. Sage's approach of constructing service dependency graphs and tracing performance anomalies through these relationships aligns closely with the dependency analysis component of the thesis framework. However, the paper's treatment of temporal aspects is implicit rather than explicit, focusing on spatial propagation through the dependency graph rather than temporal propagation patterns. The thesis could build upon Sage's dependency modeling by adding explicit temporal causal analysis to distinguish when failures occur and how they propagate over time. The unsupervised learning approach demonstrates the feasibility of root cause analysis without labeled data, which is valuable for practical deployment. The 93% accuracy benchmark provides a concrete target for comparison. The paper's focus on corrective actions also connects to potential remediation aspects of the thesis framework, though the thesis may focus more on diagnosis than automated remediation.
