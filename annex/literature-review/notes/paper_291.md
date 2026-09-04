---
paper_id: 291
title: "SDVDiag: A Modular Platform for the Diagnosis of Connected Vehicle Functions"
authors:
  - Matthias Weiss
  - Falk Dettinger
  - Michael Weyrich
year: 2025
venue: 2025 IEEE International Automated Vehicle Validation Conference (IAVVC)
doi: 10.1109/IAVVC61942.2025.11219581
arxiv_id: 2507.19403
url: "https://www.semanticscholar.org/paper/0813c51b5970e36b3f34f89d13a03750a3fd9c2f"
pdf_path: data/pdfs/paper_291.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - anomaly_detection

method:
  family: hybrid
  specific: graph traversal with anomaly augmentation
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
  primary_contribution: An extensible platform for automated diagnosis of connected vehicle functions that dynamically maintains a dependency graph and performs root cause analysis by traversing this graph augmented with detected anomalies.
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

Connected and software-defined vehicles operate through complex cloud and edge architectures with intricate dependencies between services and functions. These systems must meet high reliability and availability requirements to support passenger comfort and autonomous driving capabilities. When failures occur in such environments, manual diagnosis becomes unfeasible due to the complexity of navigating the mesh of dependencies across distributed components. The delay introduced by manual troubleshooting significantly impacts system availability and user experience. The challenge lies in automating the diagnosis process to quickly identify root causes of failures in this distributed vehicle computing environment while accounting for the dynamic nature of service dependencies and system metrics.

## Method summary

SDVDiag implements a modular pipeline architecture that covers the complete diagnosis workflow from data collection to root cause identification. The platform continuously detects and updates dependencies between vehicle functions, maintaining a dynamic graph representation of the system topology. System metrics are monitored in parallel to detect anomalies in real-time. When an incident occurs requiring investigation, the platform captures a snapshot of the current dependency graph and augments it with relevant anomalies detected around the time of the incident. The root cause analysis is then performed by traversing this augmented graph to identify the most likely causes of the observed failure. The platform supports self-adaptive behavior through runtime module exchange, allowing the diagnosis pipeline to be reconfigured dynamically. This modular design enables extensibility and adaptation to different vehicle architectures and diagnosis requirements.

## Ground truth and evaluation

The platform is evaluated by deploying it within a 5G test fleet environment designed for connected vehicle functions. The evaluation methodology involves injecting faults into the system and measuring whether SDVDiag can reliably detect these injected failures. The results demonstrate that the platform successfully identifies the injected faults, confirming its ability to detect problems in a realistic connected vehicle environment. The paper reports that faults can be detected reliably, though specific quantitative metrics such as detection rates, false positive rates, or precision and recall values are not detailed in the abstract. The ground truth for evaluation consists of the known injected faults, allowing for verification that the diagnosis platform correctly identifies problems when they occur in the test environment.

## Stated limitations

The paper does not explicitly state limitations in the provided abstract. The evaluation is conducted in a test fleet environment rather than a full production deployment, which may limit the generalizability of the results to real-world operational conditions. The abstract does not discuss scalability constraints, computational overhead, or the types of faults that the system may struggle to diagnose. There is no mention of false positive or false negative rates, which would indicate the accuracy boundaries of the approach. The reliance on graph traversal for root cause ranking may face challenges in highly complex systems with numerous interconnected dependencies, though this is not explicitly acknowledged.

## Gaps this paper opens

The paper does not provide details on how temporal relationships between anomalies and failures are modeled beyond taking snapshots at incident time. The specific algorithms used for graph traversal and ranking of root causes are not described, leaving open questions about how the platform prioritizes among multiple potential causes. The approach to dependency detection and graph construction is mentioned but not elaborated, creating uncertainty about how accurately the system captures dynamic dependencies in practice. The paper does not address how the platform handles cascading failures or distinguishes between root causes and downstream effects in the dependency graph. The integration of anomaly detection with graph-based analysis is described at a high level, but the mechanisms for determining which anomalies are relevant to a given incident remain unclear. The self-adaptive capabilities through runtime module exchange are mentioned but not demonstrated in the evaluation.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in distributed systems using both dependency analysis and anomaly detection. The dynamic dependency graph maintained by SDVDiag aligns with the thesis focus on service dependency topology for understanding failure propagation. The platform's approach of augmenting dependency graphs with detected anomalies demonstrates a practical integration of temporal anomaly information with structural dependency knowledge. The connected vehicle domain represents a specific instantiation of cloud-native principles with edge computing components, making it a relevant application area for understanding RCA challenges. The modular pipeline architecture and the graph traversal method for identifying root causes provide concrete examples of how dependency and temporal analysis can be combined in practice. However, the paper's focus on vehicle-specific functions and 5G infrastructure may limit direct applicability of certain domain-specific aspects to general cloud-native systems.
