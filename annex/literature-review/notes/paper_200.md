---
paper_id: 200
title: "TraceDiag: Adaptive, Interpretable, and Efficient Root Cause Analysis on Large-Scale Microservice Systems"
authors:
  - Ruomeng Ding
  - Chaoyun Zhang
  - Lu Wang
  - Yong Xu
  - Minghua Ma
  - Xiaomin Wu
  - Meng Zhang
  - Qingjun Chen
  - Xin Gao
  - X. Y. Gao
  - Hao Fan
  - Saravan Rajmohan
  - Qingwei Lin
  - Dongmei Zhang
year: 2023
venue: arXiv (Cornell University)
doi: 10.48550/arxiv.2310.18740
arxiv_id: ""
url: "https://openalex.org/W4388092829"
pdf_path: data/pdfs/paper_200.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - temporal_causal_analysis

method:
  family: hybrid
  specific: reinforcement learning for graph pruning with causal inference
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
  primary_contribution: An adaptive reinforcement learning approach that prunes service dependency graphs before applying causal analysis to enable efficient and interpretable root cause analysis on large-scale microservice systems.
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

Root cause analysis in large-scale microservice systems faces significant challenges due to the sheer number of components involved, often numbering in the hundreds. Traditional RCA approaches struggle with scalability because analyzing the full service dependency graph becomes computationally expensive and time-consuming. The problem is exacerbated by the fact that many components in the dependency graph may be irrelevant to a specific failure incident, yet existing methods must process them all. This leads to excessive human effort in both the analysis process and the interpretation of results. The need exists for an automated approach that can intelligently reduce the search space while maintaining high accuracy in identifying root causes.

## Method summary

TraceDiag employs a two-stage approach combining reinforcement learning with causal inference. In the first stage, a reinforcement learning agent learns a pruning policy that adaptively eliminates redundant components from the service dependency graph. The agent is trained to maximize a reward function that balances the trade-off between graph reduction and preservation of relevant causal information. The pruning policy is designed to be interpretable and adaptive, meaning it can generalize to new RCA instances without retraining. In the second stage, once the graph has been pruned to a manageable size, a causal-based method is applied to the reduced graph to identify the root cause. The causal analysis leverages trace data to establish causal relationships between services. The framework operates end-to-end, taking raw trace data as input and producing root cause diagnoses as output.

## Ground truth and evaluation

The framework is evaluated using real trace data collected from the Microsoft Exchange system, which represents a production-scale microservice environment. Ground truth for root causes appears to be derived from actual incident reports and post-mortem analyses from the operational system. The evaluation compares TraceDiag against state-of-the-art RCA approaches, measuring both accuracy in identifying correct root causes and efficiency in terms of computational cost and graph size reduction. Performance metrics demonstrate that TraceDiag achieves superior results on both dimensions. The practical validation is strengthened by the fact that TraceDiag has been deployed and integrated as a critical component in the Microsoft M365 Exchange production system, where it has demonstrably improved system reliability and reduced human effort in RCA tasks.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the reliance on reinforcement learning for pruning policy implies that the approach requires sufficient training data from the target system to learn effective pruning strategies. The generalization capability of the learned policy across fundamentally different microservice architectures or failure patterns is not thoroughly discussed. The interpretability claim for the pruning policy, while stated, is not extensively validated with user studies or detailed explanations of what makes the policy interpretable in practice. The computational overhead of training the reinforcement learning agent and the data requirements for achieving good performance are not quantified in detail.

## Gaps this paper opens

The paper demonstrates the value of combining graph pruning with causal analysis but does not explore how temporal patterns in failure propagation might further inform the pruning strategy. The reinforcement learning approach focuses on structural pruning but could potentially benefit from incorporating temporal dependencies and time-series patterns observed in traces. The framework treats the pruning and causal analysis stages somewhat independently, suggesting opportunities for tighter integration where causal feedback could refine pruning decisions iteratively. The interpretability of the pruning policy is asserted but not deeply investigated, leaving open questions about how operators understand and trust the automated pruning decisions. The paper does not address how the framework handles evolving system architectures where new services are added or removed, requiring policy adaptation or retraining.

## Relevance to the thesis topic

TraceDiag is highly relevant to the thesis topic as it directly addresses root cause analysis in cloud-native microservice systems using both dependency analysis and temporal trace data. The framework explicitly tackles the service dependency topology challenge through its graph pruning approach, which is central to the thesis focus. The causal analysis component aligns with the temporal and dependency analysis aspects of the proposed framework. The use of trace data provides temporal information about service interactions and failure propagation patterns. However, TraceDiag does not emphasize temporal causal analysis as deeply as the thesis might, focusing more on structural graph reduction. The paper provides valuable insights into handling large-scale systems and demonstrates the practical importance of efficiency in RCA, which are key considerations for any framework targeting production cloud-native environments. The deployment in Microsoft Exchange validates the real-world applicability of combining adaptive graph analysis with causal reasoning.
