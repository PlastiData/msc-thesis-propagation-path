---
paper_id: 165
title: Causal Inference-Based Root Cause Analysis for Online Service Systems with Intervention Recognition
authors:
  - Mingjie Li
  - Zeyan Li
  - Kanglin Yin
  - Xiaohui Nie
  - Wenchi Zhang
  - Kaixin Sui
  - Dan Pei
year: 2022
venue: Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining
doi: 10.1145/3534678.3539041
arxiv_id: ""
url: "https://openalex.org/W4290927880"
pdf_path: data/pdfs/paper_165.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - temporal_causal_analysis
  - service_dependency_topology

method:
  family: hybrid
  specific: Causal Bayesian Network with intervention recognition
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
  primary_contribution: Formulates root cause analysis as an intervention recognition problem in causal inference and proposes CIRCA, which identifies root causes by detecting distribution changes conditioned on parent nodes in a Causal Bayesian Network constructed from system architecture knowledge.
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

Online service systems generate vast amounts of monitoring data from various metrics and components. When failures occur, operators must quickly identify the root cause indicators from this large set of monitoring variables to enable timely mitigation. The challenge is that many metrics may show anomalous behavior during a failure, but only a small subset represent the actual root causes. Traditional approaches struggle to distinguish between symptoms and true root causes, leading to inefficient diagnosis processes. The problem requires not just detecting that something is wrong, but pinpointing which specific monitoring variables correspond to the underlying fault that triggered the cascading effects observed across the system.

## Method summary

CIRCA formulates root cause analysis as an intervention recognition problem within a causal inference framework. The method constructs a Causal Bayesian Network among monitoring metrics using knowledge of the system architecture and a set of causal assumptions about how components interact. The core theoretical insight is that a monitoring variable qualifies as a root cause indicator if its probability distribution conditioned on its parent nodes in the CBN changes during the fault period. The method operates in an unsupervised manner, avoiding the need for labeled training data. CIRCA evaluates each metric by comparing its conditional probability distribution before and during the fault, using the causal graph structure to properly account for dependencies. Metrics showing significant conditional distribution shifts are ranked as candidate root causes, with the assumption that true root causes will exhibit such shifts while downstream effects will not when properly conditioned on their causal parents.

## Ground truth and evaluation

The paper evaluates CIRCA using both simulation studies and real-world datasets from online service systems. For the real-world evaluation, ground truth root causes are obtained from post-incident analysis by human operators who investigated actual failures. The evaluation metrics focus on recall at different ranking positions, particularly top-1 and top-5 recall, measuring how often the true root cause appears in the top-ranked recommendations. The simulation study validates the theoretical properties of the approach under controlled conditions where the true causal structure and intervention points are known. The real-world dataset contains multiple failure cases from production systems, allowing comparison against baseline methods including statistical approaches and other causal inference techniques. The ground truth represents expert judgment after thorough investigation rather than automated labeling.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the approach inherently depends on the accuracy of the system architecture knowledge used to construct the initial causal graph. The method makes several causal assumptions about the relationships between monitoring metrics that may not hold perfectly in all scenarios. The construction of the Causal Bayesian Network requires domain knowledge about component dependencies, which may be incomplete or outdated in rapidly evolving systems. The evaluation is conducted on a specific set of online service systems, and generalization to other domains or system architectures is not thoroughly discussed. The computational complexity of evaluating conditional probability distributions for all metrics during real-time fault diagnosis is not analyzed in detail.

## Gaps this paper opens

The reliance on pre-existing system architecture knowledge creates a gap for scenarios where such documentation is incomplete, incorrect, or unavailable. The method does not address how to automatically discover or validate the causal relationships assumed in the graph construction phase. There is no mechanism for handling temporal dynamics beyond comparing distributions before and during faults, leaving open questions about how to incorporate time-series patterns or propagation delays. The approach does not explicitly model transient effects or consider that root causes may manifest differently across multiple temporal scales. The paper does not explore how to integrate heterogeneous observability data types beyond metrics, such as logs or traces, which might provide additional causal evidence. The handling of multiple simultaneous root causes or cascading failures is not thoroughly examined.

## Relevance to the thesis topic

This paper is highly relevant as it directly addresses root cause analysis in distributed systems using causal inference principles. The formulation of RCA as intervention recognition provides a theoretical foundation that aligns with the thesis goal of using temporal and dependency analysis. CIRCA's use of Causal Bayesian Networks to model service dependencies directly relates to the dependency analysis component of the thesis framework. The method's focus on conditional probability distribution changes offers insights into how temporal patterns can be analyzed within a causal structure. However, the thesis aims to incorporate more explicit temporal propagation analysis and potentially leverage modern observability data beyond metrics. CIRCA's requirement for system architecture knowledge highlights the importance of dependency topology in the thesis framework, while its limitations in handling temporal dynamics motivate the need for enhanced temporal analysis methods. The strong empirical results demonstrate the value of causal reasoning for RCA in cloud-native environments.
