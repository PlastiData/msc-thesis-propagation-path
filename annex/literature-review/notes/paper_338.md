---
paper_id: 338
title: Generic and Robust Root Cause Localization for Multi-Dimensional Data in Online Service Systems
authors:
  - Zeyan Li
  - Junjie Chen
  - Yihao Chen
  - Chengyang Luo
  - Yiwei Zhao
  - Yongqian Sun
  - Kaixin Sui
  - Xiping Wang
  - Dapeng Liu
  - Xing Jin
  - Qi Wang
  - Dan Pei
year: 2023
venue: Journal of Systems and Software
doi: 10.2139/ssrn.4100992
arxiv_id: 2305.03331
url: "https://www.semanticscholar.org/paper/c58d3fd5a69ca5ee58376772a4ffc1855a2180c8"
pdf_path: data/pdfs/paper_338.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - anomaly_detection
  - observability_data_analysis

method:
  family: hybrid
  specific: probabilistic clustering with heuristic search based on generalized ripple effect
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
  primary_contribution: A generic root cause localization approach for multi-dimensional data that identifies abnormal attribute combinations using generalized ripple effect property, probabilistic clustering, and heuristic search, including the first method to determine external root causes.
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

When faults occur in online service systems, operators need to identify which specific combinations of attributes in multi-dimensional monitoring data are responsible for observed anomalies. Multi-dimensional data consists of measures aggregated across various attribute combinations, such as different regions, device types, or network providers. When a fault happens, only certain attribute combinations exhibit abnormal measure values, and these combinations provide critical clues to the underlying root causes. Existing approaches struggle with the complexity of multi-dimensional data where the number of possible attribute combinations grows exponentially with the number of dimensions. Additionally, no prior work addresses the problem of determining whether root causes are external to the monitored system, which is essential for effective fault diagnosis and remediation.

## Method summary

PSqueeze introduces the concept of generalized ripple effect, which formalizes the observation that root cause attribute combinations create ripple patterns in aggregated data across different dimensions. The method operates in three main stages. First, it applies a probabilistic clustering technique that groups attribute combinations based on their likelihood of being affected by the same root cause, using the generalized ripple effect property to guide clustering decisions. Second, it employs a heuristic search algorithm to efficiently explore the exponentially large space of possible attribute combinations and identify the most likely root causes within each cluster. Third, PSqueeze incorporates a novel mechanism to determine whether identified root causes are external to the system by analyzing patterns in how anomalies propagate across different attribute dimensions. The approach is designed to be generic across different types of multi-dimensional data and robust to noise and incomplete observations.

## Ground truth and evaluation

The evaluation uses two real-world datasets containing 5400 injected faults across production online service systems. Ground truth for root cause attribute combinations is established through the fault injection process, where operators know precisely which attribute combinations were affected by each injected fault. The paper measures performance using F1-score, which balances precision and recall in identifying the correct root cause attribute combinations. PSqueeze achieves an F1-score improvement of 32.89% over baseline methods, with localization times consistently around 10 seconds across all test cases. For the external root cause determination task, PSqueeze achieves an F1-score of 0.90. The baselines compared include existing multi-dimensional root cause localization methods. Case studies in several production systems provide qualitative validation that PSqueeze assists operators in real-world fault diagnosis scenarios.

## Stated limitations

The paper does not explicitly enumerate technical limitations of the PSqueeze approach. The evaluation relies on fault injection rather than naturally occurring production incidents, which may not fully capture the complexity and diversity of real-world failure scenarios. The generalizability across different types of online service systems beyond those tested is not thoroughly discussed. The paper does not address computational scalability limits for extremely high-dimensional data or discuss failure modes where the generalized ripple effect assumption might not hold. There is no analysis of how the method performs when multiple simultaneous root causes exist or when root causes interact in complex ways.

## Gaps this paper opens

The work focuses exclusively on multi-dimensional aggregated metrics and does not consider how temporal patterns in these metrics might provide additional signals for root cause localization. The relationship between identified attribute combinations and the underlying service dependency topology remains unexplored, leaving unclear how root causes in multi-dimensional data map to specific microservices or components in cloud-native architectures. The method does not incorporate log data, traces, or other observability signals that could complement multi-dimensional metric analysis. The external root cause determination mechanism, while novel, lacks integration with broader system knowledge about dependencies and failure propagation paths. The evaluation does not examine how PSqueeze could be combined with causal inference techniques to move beyond correlation-based localization to true causal root cause identification.

## Relevance to the thesis topic

PSqueeze addresses a fundamental aspect of root cause analysis in cloud-native systems by localizing faults within multi-dimensional monitoring data, which is directly relevant to the thesis goal of developing a comprehensive RCA framework. The method's focus on attribute combinations provides a complementary perspective to service-level dependency analysis, as abnormal attribute combinations often correspond to specific service instances or deployment configurations. However, PSqueeze operates primarily on aggregated metrics without explicit temporal or dependency modeling, which are central to the thesis framework. The approach could serve as a component for initial fault localization that feeds into subsequent temporal causal analysis and dependency-aware reasoning. The external root cause determination capability is particularly relevant as it addresses the boundary between internal system issues and external factors, which is important for scoping RCA efforts in distributed systems.
