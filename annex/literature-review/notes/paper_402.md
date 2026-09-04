---
paper_id: 402
title: Causal discovery for time series with latent confounders
authors:
  - Christian Reiser
year: 2022
venue: arXiv
doi: ""
arxiv_id: 2209.03427
url: "http://arxiv.org/abs/2209.03427v1"
pdf_path: data/pdfs/paper_402.pdf
read_date: 2026-05-11

category:
  - temporal_causal_analysis
  - anomaly_detection
  - observability_data_analysis

method:
  family: classical_ml
  specific: LPCMCI (Latent PC-MCI algorithm)
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
  primary_contribution: Empirical evaluation of the LPCMCI algorithm for discovering causal relationships in multivariate time series data when latent confounders are present.
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

The fundamental challenge addressed is reconstructing causal relationships from observational data when controlled experiments are infeasible, unethical, or prohibitively expensive. The specific focus is on multivariate time series data where some variables remain unobserved, creating latent confounders that complicate causal inference. The work examines whether automated causal discovery methods can identify the underlying causal structure from highly autocorrelated time series when not all relevant variables are measured. This problem is particularly relevant in complex systems where the complete set of influencing factors cannot be directly observed or measured.

## Method summary

The paper evaluates the LPCMCI algorithm, which stands for Latent PC-MCI and extends previous causal discovery methods to handle unobserved confounding variables. LPCMCI aims to identify generators that are compatible with the observed multivariate time series data while accounting for the presence of hidden variables. The algorithm attempts to discover three types of dependencies: auto-dependencies where a variable depends on its own past values, contemporaneous dependencies between variables at the same time point, and lagged dependencies where one variable influences another with a time delay. The evaluation compares LPCMCI performance against a random baseline algorithm that represents having no knowledge about the causal structure.

## Ground truth and evaluation

The evaluation uses synthetic data where the true causal structure is known by construction, allowing direct comparison between discovered and actual causal relationships. The paper assesses LPCMCI performance across different types of dependencies separately: auto-dependencies, contemporaneous dependencies, and lagged dependencies. Performance is measured by comparing the algorithm's ability to correctly identify these different dependency types against both the ground truth and a random baseline. The results show that LPCMCI significantly outperforms random guessing but falls considerably short of optimal detection accuracy. The algorithm demonstrates varying success rates depending on dependency type, with best performance on auto-dependencies and poorest performance on lagged dependencies.

## Stated limitations

The paper explicitly states that LPCMCI remains far from optimal detection performance despite outperforming random baselines. The algorithm struggles most with identifying lagged dependencies, which represent time-delayed causal effects between different variables. The performance hierarchy shows clear weaknesses, with contemporaneous dependencies being moderately difficult and lagged dependencies presenting the greatest challenge. The presence of latent confounders inherently makes the causal discovery problem more difficult, and LPCMCI's limited success suggests fundamental challenges remain in handling unobserved variables in time series causal inference.

## Gaps this paper opens

The significant gap between LPCMCI performance and optimal detection indicates substantial room for improvement in causal discovery methods for time series with latent confounders. The differential performance across dependency types suggests that current approaches may need specialized techniques for handling lagged versus contemporaneous relationships. The work does not explore why lagged dependencies are particularly difficult to detect or propose solutions to address this weakness. There is no investigation into how the number or nature of latent confounders affects detection accuracy, nor examination of which characteristics of time series make causal discovery more or less feasible. The evaluation focuses solely on one algorithm without comparing against other potential approaches for handling latent confounders.

## Relevance to the thesis topic

This work is adjacent to the thesis topic on root cause analysis in cloud-native systems. Causal discovery in time series with latent confounders directly relates to understanding failure propagation patterns when not all system components or metrics are observable. Cloud systems inherently have unobserved variables due to incomplete instrumentation, third-party dependencies, and complex interactions that cannot be fully monitored. The temporal aspect of LPCMCI aligns with analyzing how failures propagate through service dependencies over time. However, the paper focuses on general causal discovery methodology rather than specific application to distributed systems or root cause analysis. The findings about difficulty detecting lagged dependencies are particularly relevant since failure propagation in cloud systems involves time-delayed cascading effects. The work provides theoretical grounding for temporal causal analysis but lacks the domain-specific considerations needed for practical root cause analysis in production systems.
