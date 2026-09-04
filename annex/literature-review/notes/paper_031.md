---
paper_id: 031
title: Causal Fault Localization for Cross-Border Payment Gateways Using Multi-Relational Service Dependency Graphs
authors:
  - Stefan Müller
  - Isabel Torres
year: 2026
venue: Multidisciplinary Research in Computing Information Systems
doi: 10.71465/mrcis202
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/fe963b848981a3889cb61be5966f5d2497c88f9c"
pdf_path: data/pdfs/paper_031.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - temporal_causal_analysis

method:
  family: hybrid
  specific: Multi-Relational Service Dependency Graphs with weighted PageRank and Graph Neural Networks
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
  primary_contribution: A causal fault localization framework using multi-relational service dependency graphs that distinguishes genuine causal relationships from correlations in cross-border payment gateways.
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

Cross-border payment gateways represent critical infrastructure for global e-commerce, processing trillions of dollars annually through complex distributed architectures. These systems involve multiple microservices including currency conversion systems, compliance modules, and international banking networks that create intricate causal relationships and multi-relational dependencies. Traditional fault localization approaches fail to adequately handle these complex interdependencies when service degradations occur. The primary challenge is distinguishing genuine causal relationships from spurious correlations that arise from shared payment peaks and regulatory events, which leads to high false positive rates in fault diagnosis. Existing dependency graph methods do not sufficiently capture both synchronous service calls and asynchronous message flows while incorporating temporal causality constraints.

## Method summary

The framework constructs Multi-Relational Service Dependency Graphs that capture both synchronous service calls and asynchronous message flows derived from transaction traces. The approach incorporates temporal causality constraints to model how faults propagate through the system over time. A weighted PageRank algorithm enhanced with causal inference mechanisms analyzes fault propagation patterns across heterogeneous service relationships to identify root causes. The system integrates Graph Neural Network architectures with structural causal models to distinguish correlation from genuine causal relationships. This integration allows the framework to filter spurious correlations that commonly arise in payment systems during shared load peaks or regulatory events. The causal inference component specifically addresses the challenge of false positives by reasoning about the directionality and temporal ordering of fault propagation across different types of service dependencies.

## Ground truth and evaluation

The experimental validation uses production traces from a multinational payment gateway to assess the framework's performance. The evaluation compares the MRSDG-based approach against conventional dependency graph methods using metrics including mean time to detection and false positive rates. Results demonstrate that the proposed approach achieves approximately forty-three percent reduction in mean time to detection compared to baseline methods. The false positive rate decreases by thirty-seven percent, indicating improved precision in identifying actual root causes. The evaluation specifically examines the causal inference component's ability to filter spurious correlations arising from shared payment peaks and regulatory events. The paper reports superior accuracy in localizing root causes compared to conventional methods, though specific details about ground truth labeling procedures or the size of the evaluation dataset are not provided in the abstract.

## Stated limitations

The abstract does not explicitly state limitations of the proposed approach. No discussion is provided regarding computational complexity, scalability constraints, or applicability to other types of distributed systems beyond payment gateways. The paper does not mention challenges in constructing the multi-relational dependency graphs or potential difficulties in obtaining sufficient training data for the Graph Neural Network components. There is no acknowledgment of scenarios where the causal inference mechanisms might fail or produce ambiguous results. The abstract also does not address potential limitations in handling novel fault types not seen during training or the framework's performance under extreme load conditions.

## Gaps this paper opens

The framework's specificity to cross-border payment gateways raises questions about generalizability to other cloud-native systems with different architectural patterns and failure modes. The integration of Graph Neural Networks with structural causal models suggests a need for substantial labeled training data, but the paper does not address how to bootstrap such systems in new deployment environments. The temporal causality constraints are mentioned but not detailed, leaving open questions about how temporal windows are determined and how the system handles varying propagation delays across different service types. The weighted PageRank enhancement with causal inference mechanisms is introduced but the specific weighting schemes and their sensitivity to parameter choices remain unexplored. The paper does not discuss how the framework handles dynamic topology changes common in cloud-native systems or how it adapts when new services are deployed or existing services are modified.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in distributed systems using both temporal and dependency analysis. The Multi-Relational Service Dependency Graph approach aligns with the thesis focus on service dependency topology, while the incorporation of temporal causality constraints from transaction traces directly supports temporal analysis objectives. The framework's emphasis on distinguishing genuine causal relationships from correlations addresses a core challenge in root cause analysis that the thesis must confront. The integration of Graph Neural Networks with structural causal models provides a concrete example of combining modern machine learning with causal reasoning for fault localization. The experimental validation demonstrating reduced mean time to detection and lower false positive rates offers quantitative benchmarks relevant to evaluating the thesis framework. However, the domain-specific focus on payment gateways means that adaptation and generalization work would be necessary to apply these techniques to broader cloud-native systems.
