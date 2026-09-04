---
paper_id: 221
title: Diagnosis of Service Failures by Trace Analysis with Partial Knowledge
authors:
  - Wolfgang E Mayer
  - G. Friedrich
  - M. Stumptner
year: 2010
venue: International Conference on Service Oriented Computing
doi: 10.1007/978-3-642-17358-5_23
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/29159af248e5873e4a3c25ee261ab5092d171318"
pdf_path: data/pdfs/paper_221.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - observability_data_analysis

method:
  family: rule_based
  specific: model-based diagnosis with partial dependency knowledge
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
  primary_contribution: A model-based diagnosis approach that identifies faulty service components from execution traces even when complete system knowledge is unavailable.
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

Service-oriented architectures present significant challenges for fault diagnosis because complete system models are often unavailable or impractical to maintain. Services are composed dynamically and may involve third-party components whose internal behavior is unknown to system operators. When failures occur, execution traces capture the observable interactions between services, but diagnosing the root cause requires reasoning about which components are responsible for observed failures. The problem is complicated by the fact that a single observable failure symptom may have multiple possible explanations, and the diagnostic system must work with incomplete knowledge about service dependencies and behaviors. Traditional debugging approaches that assume complete system knowledge are inadequate for these distributed, loosely-coupled environments.

## Method summary

The approach applies model-based diagnosis theory to service execution traces by representing the system as a set of components with known input-output relationships where available. The method constructs a diagnostic model from execution traces that capture service invocations, message exchanges, and observed outcomes. When failures are detected, the diagnosis algorithm identifies minimal sets of components whose abnormal behavior would explain all observed symptoms. The technique handles partial knowledge by making conservative assumptions about unknown components and dependencies. It uses consistency-based reasoning to determine which components must be faulty to account for discrepancies between expected and observed behavior. The diagnosis process generates candidate explanations ranked by parsimony, preferring explanations that involve fewer faulty components. The framework explicitly models the uncertainty introduced by incomplete system knowledge and distinguishes between definite diagnoses and possible diagnoses that depend on unknown system properties.

## Ground truth and evaluation

The paper evaluates the approach using synthetic service composition scenarios where failures are artificially injected into specific components. The ground truth consists of the known faulty components that were deliberately made to malfunction in the test scenarios. Evaluation metrics focus on the accuracy of identifying the actual faulty component within the set of diagnostic candidates produced by the algorithm. The experiments examine how diagnostic accuracy degrades as the completeness of system knowledge decreases. Performance is measured in terms of the size of the candidate set and whether the true faulty component appears in the diagnosis. The evaluation demonstrates that even with partial knowledge, the approach can significantly narrow down the set of possible root causes compared to having no diagnostic reasoning. The test cases involve varying degrees of missing information about service dependencies and component behaviors to assess robustness under different knowledge conditions.

## Stated limitations

The paper acknowledges that diagnostic accuracy necessarily decreases when system knowledge is incomplete, resulting in larger sets of candidate diagnoses that are less specific. The approach requires that execution traces capture sufficient information about service interactions, which may not always be available in practice. The method assumes that trace data is reliable and correctly reflects actual system behavior, but does not address scenarios where traces themselves may be incomplete or corrupted. The computational complexity of generating all minimal diagnoses can become prohibitive for large-scale systems with many components and complex interaction patterns. The framework does not incorporate probabilistic reasoning or historical failure data that could help rank candidate diagnoses beyond simple cardinality-based preferences. The evaluation uses relatively small synthetic examples rather than large-scale real-world service systems, leaving questions about practical scalability.

## Gaps this paper opens

The work does not address how to automatically acquire or learn the partial system models from operational data rather than requiring manual specification. There is no mechanism for incorporating temporal patterns or failure propagation dynamics that could help distinguish between primary faults and cascading secondary effects. The approach treats all trace observations equally without considering that some symptoms may be more diagnostic than others based on their position in the execution flow. The paper does not explore how to integrate multiple traces from different execution instances to improve diagnostic accuracy or how to handle intermittent failures that may not manifest consistently. The relationship between the granularity of component modeling and diagnostic precision remains unexplored. There is no discussion of how the diagnostic results could be used to drive automated remediation or how operators should interact with sets of candidate diagnoses in practice.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in distributed service systems using trace analysis. The focus on handling partial knowledge about system dependencies aligns with the practical challenges of analyzing cloud-native systems where complete topology information may be unavailable or constantly changing. The model-based diagnostic approach provides a formal foundation for reasoning about fault propagation through service dependencies, which complements the thesis emphasis on dependency analysis. However, the paper's rule-based method contrasts with modern approaches that might leverage temporal patterns or machine learning from observability data. The work establishes important concepts about how to reason under uncertainty in distributed system diagnosis, but lacks the temporal causal analysis and automated learning capabilities that the thesis aims to develop. The trace-based analysis methodology is directly applicable, though the thesis would need to extend beyond the consistency-based reasoning to incorporate time-series patterns and automated topology discovery.
