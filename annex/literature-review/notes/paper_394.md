---
paper_id: 394
title: Evaluating the Risk of Changes in a Microservices Architecture
authors:
  - Matteo Collina
  - Luca Maraschi
  - Tommaso Pirini 1. Platformatic Inc
year: 2023
venue: arXiv
doi: ""
arxiv_id: 2309.06238
url: "http://arxiv.org/abs/2309.06238v1"
pdf_path: data/pdfs/paper_394.pdf
read_date: 2026-05-11

category:
  - service_dependency_topology
  - root_cause_analysis
  - recommendation_and_remediation

method:
  family: rule_based
  specific: dependency graph traversal with risk scoring
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
  primary_contribution: An algorithm that computes risk scores for microservice changes by propagating impact through service dependency graphs.
  novelty_strength: incremental

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

Microservices architectures enable independent deployment of services, which provides flexibility for making changes but introduces complexity in understanding the system-wide impact of those changes. When a single service is modified, the change can potentially cascade through dependencies and cause failures in other services or even bring down the entire system. Development teams lack systematic methods to assess the risk associated with deploying changes to individual microservices. The challenge is to quantify how risky a particular change is before deployment, considering the service's position in the dependency graph and its relationships with other services. Without such risk assessment, teams either deploy changes blindly or adopt overly conservative practices that slow down development velocity.

## Method summary

The proposed algorithm computes risk scores for microservice changes by analyzing the service dependency graph. The approach starts by constructing a directed graph where nodes represent microservices and edges represent dependencies between services. When a change is proposed for a specific service, the algorithm traverses the dependency graph to identify all services that could be affected by the change. The risk calculation considers both direct dependencies and transitive dependencies, propagating risk scores through the graph. Services that have many downstream dependents receive higher risk scores because their failure would impact more parts of the system. The algorithm also accounts for the criticality of dependent services, where changes to services that support critical business functions are assigned higher risk values. The resulting risk score provides a quantitative measure that development teams can use to make informed decisions about deployment timing and testing requirements.

## Ground truth and evaluation

The paper does not present empirical evaluation with ground truth data. There is no description of validation against real-world incidents or comparison with actual failure rates following deployments. The authors do not report on applying the algorithm to production microservices systems or measuring its predictive accuracy. No datasets are mentioned for testing the risk scoring approach. The paper does not include case studies showing how the computed risk scores correlate with observed system failures or incidents. Without experimental validation, it remains unclear whether the proposed risk scores accurately reflect actual deployment risks or whether they would help teams make better deployment decisions. The absence of evaluation metrics such as precision, recall, or correlation with real incidents limits the ability to assess the practical utility of the approach.

## Stated limitations

The paper does not explicitly discuss limitations of the proposed approach. There is no acknowledgment of scenarios where the algorithm might fail or produce misleading risk scores. The authors do not address challenges such as incomplete dependency information, dynamic dependencies that change at runtime, or the difficulty of assigning appropriate criticality weights to services. The paper does not discuss computational complexity for large-scale systems with thousands of services. There is no mention of how the algorithm handles circular dependencies or how it accounts for the nature of changes, such as whether a change is a minor bug fix or a major architectural modification. The lack of stated limitations makes it difficult to understand the boundary conditions and applicability constraints of the proposed method.

## Gaps this paper opens

The paper identifies the need for risk assessment in microservices deployments but leaves several gaps unaddressed. The algorithm requires manual specification of service criticality and dependency relationships, but does not explain how to obtain or maintain this information automatically from observability data or service meshes. The approach treats all changes uniformly without considering the semantic nature of the change, such as whether it modifies critical code paths or merely updates configuration. There is no integration with runtime monitoring or historical incident data that could refine risk estimates based on past failures. The paper does not address how risk scores should translate into concrete deployment decisions or what thresholds should trigger additional testing or staged rollouts. The relationship between static dependency analysis and actual runtime failure propagation remains unexplored, creating uncertainty about whether graph-based risk scores capture real operational risks.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses risk assessment in microservices through dependency analysis, which relates to understanding how failures propagate through service dependencies. However, the paper focuses on pre-deployment risk evaluation rather than post-incident root cause analysis. The dependency graph traversal approach could inform the thesis work by providing insights into how service relationships influence failure propagation patterns. The concept of quantifying impact through dependency structures is relevant to temporal failure propagation analysis, though this paper uses static analysis rather than temporal observability data. The work highlights the importance of service topology in understanding system-wide effects, which aligns with the thesis emphasis on dependency analysis. However, the paper does not incorporate temporal analysis, observability metrics, or actual incident data, which are central to the thesis approach for root cause analysis in cloud-native systems.
