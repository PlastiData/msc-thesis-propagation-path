---
paper_id: 168
title: Automatic Failure Attribution and Critical Step Prediction Method for Multi-Agent Systems Based on Causal Inference
authors:
  - Guoqing Ma
  - Zhu Jia
  - Hanghui Guo
  - Weijie Shi
  - Jiawei Shen
  - Jingjiang Liu
  - Yidan Liang
year: 2025
venue: ArXiv.org
doi: 10.48550/arxiv.2509.08682
arxiv_id: ""
url: "https://openalex.org/W4417070626"
pdf_path: data/pdfs/paper_168.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - temporal_causal_analysis
  - recommendation_and_remediation

method:
  family: hybrid
  specific: causal inference with Shapley values and CDC-MAS causal discovery
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
  primary_contribution: A multi-granularity causal inference framework for failure attribution in multi-agent systems that combines performance causal inversion with Shapley values for agent-level blame and a novel causal discovery algorithm for identifying critical failure steps.
  novelty_strength: strong

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

Multi-agent systems face severe challenges in failure attribution that prevent their practical deployment. Current diagnostic approaches rely on statistical correlations rather than causal relationships, leading to fundamentally inadequate performance. On benchmark datasets like Who&When, state-of-the-art methods achieve less than 15% accuracy when attempting to locate the root-cause step of a failure. The core difficulty stems from the complex interactions between multiple agents executing tasks through sequences of steps, where failures can propagate through the system in non-obvious ways. Existing methods cannot distinguish between symptoms and actual causes, making it nearly impossible to identify which specific agent action or step is responsible for system failures.

## Method summary

The framework introduces multi-granularity causal inference operating at both agent and step levels. At the agent level, the method applies a performance causal inversion principle that reverses the data flow observed in execution logs to correctly model performance dependencies. This inverted causal model is combined with Shapley values from cooperative game theory to quantify each agent's contribution to failures and assign blame accurately. At the step level, the framework employs CDC-MAS, a novel causal discovery algorithm designed to handle the non-stationary nature of multi-agent interaction data. CDC-MAS identifies critical failure steps by constructing causal graphs that capture temporal dependencies between actions. The attribution results from both granularities feed into an automated optimization loop that generates targeted suggestions for fixing identified issues. These suggestions are validated through counterfactual simulations that predict whether proposed changes would prevent the observed failures.

## Ground truth and evaluation

The framework is evaluated on two benchmarks: Who&When and TRAIL. The Who&When benchmark provides scenarios where ground truth root-cause steps are labeled, allowing direct measurement of step-level attribution accuracy. The TRAIL benchmark evaluates the practical impact of generated optimizations on overall task success rates. Evaluation metrics include step-level accuracy for identifying the correct root-cause step and task success rate improvements after applying automated optimizations. The method achieves 36.2% step-level accuracy on failure attribution, representing more than a doubling of the previous state-of-the-art 15% baseline. The generated optimizations boost overall task success rates by an average of 22.4% across the benchmarks. Counterfactual simulations validate the efficacy of proposed fixes by showing whether they would have prevented observed failures.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the evaluation reveals implicit constraints. The 36.2% step-level accuracy, while significantly better than prior work, indicates that nearly two-thirds of failure attributions remain incorrect. The framework's reliance on execution logs means it can only analyze failures that have already occurred and been logged, limiting its applicability to novel failure modes. The causal discovery component must handle non-stationary interaction data, suggesting potential brittleness when agent behaviors change dramatically over time. The counterfactual simulation approach for validating optimizations requires a simulation environment, which may not perfectly reflect production system behavior.

## Gaps this paper opens

The framework's focus on multi-agent systems leaves open questions about applicability to other distributed system architectures like microservices. The causal discovery algorithm CDC-MAS is tailored to multi-agent interaction patterns, and its effectiveness on general cloud-native service dependencies remains unexplored. The paper does not address how the method scales with system size, particularly when dealing with hundreds or thousands of interacting components rather than multiple agents. The reliance on Shapley values for blame assignment assumes cooperative game theory principles apply, but cloud systems may exhibit different failure propagation dynamics. The counterfactual simulation validation approach requires accurate system models, raising questions about how to obtain such models for complex production environments. The method's ability to handle concurrent failures or cascading failures across multiple components is not explicitly addressed.

## Relevance to the thesis topic

This work is adjacent to the thesis topic because it addresses root cause analysis through causal inference and temporal analysis, though in a different system context. The multi-granularity approach to causal analysis offers insights applicable to cloud-native systems, where failures must be attributed across both service-level and request-level granularities. The performance causal inversion principle demonstrates how reversing observed data flows can reveal true causal dependencies, a technique potentially adaptable to analyzing service call traces and dependency graphs in microservices. The CDC-MAS algorithm's handling of non-stationary interaction data addresses challenges also present in cloud systems where service behaviors change with deployments and load patterns. The automated optimization loop with counterfactual validation provides a model for how root cause analysis results can drive remediation in cloud environments. However, the framework's design for discrete agent actions and steps differs from the continuous metrics and distributed traces typical in cloud observability, requiring substantial adaptation for the thesis context.
