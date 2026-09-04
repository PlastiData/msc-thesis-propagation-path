---
paper_id: 025
title: "DynaCausal: Dynamic Causality-Aware Root Cause Analysis for Distributed Microservices"
authors:
  - Songhan Zhang
  - Aoyang Fang
  - Yifan Yang
  - Ruiyi Cheng
  - Xiaoying Tang
  - Pinjia He
year: 2025
venue: arXiv.org
doi: 10.48550/arXiv.2510.22613
arxiv_id: 2510.22613
url: "https://www.semanticscholar.org/paper/563a55a4915ea0970772855c6c57c40dd699aa63"
pdf_path: data/pdfs/paper_025.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - temporal_causal_analysis
  - service_dependency_topology

method:
  family: deep_learning
  specific: interaction-aware representation learning with dynamic contrastive mechanism and causal-prioritized ranking
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
  primary_contribution: A dynamic causality-aware framework that unifies multi-modal signals through interaction-aware representation learning and uses dynamic contrastive mechanisms with causal-prioritized ranking to improve root cause localization in microservices.
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

Existing root cause analysis methods for cloud-native microservices struggle with three fundamental challenges despite incorporating multi-modal data from logs, traces, and metrics. First, they inadequately model cascading fault propagation patterns that occur when failures spread through service dependencies in distributed systems. Second, these methods are vulnerable to noise interference and concept drift, where normal service behavior patterns shift over time, making it difficult to distinguish genuine anomalies from benign variations. Third, current approaches over-rely on service deviation intensity as the primary signal for root cause identification, which can obscure the true causal origin of failures because downstream services often exhibit more severe symptoms than the actual root cause. These limitations become particularly acute in dynamic microservice environments where service relationships and dependencies evolve rapidly.

## Method summary

DynaCausal introduces a framework that unifies multi-modal dynamic signals to capture time-varying spatio-temporal dependencies in microservice systems. The approach employs interaction-aware representation learning to model how services influence each other over time, explicitly accounting for the dynamic nature of service relationships and fault propagation patterns. To address noise and concept drift, DynaCausal incorporates a dynamic contrastive mechanism that learns to disentangle true fault indicators from contextual noise by contrasting faulty states against normal operational patterns while adapting to shifting baselines. The framework replaces traditional deviation-intensity-based ranking with a causal-prioritized pairwise ranking objective that explicitly optimizes for causal attribution rather than symptom severity. This ranking mechanism learns to identify services that are causally responsible for failures rather than those merely exhibiting strong anomalous signals as downstream effects.

## Ground truth and evaluation

The paper evaluates DynaCausal on public benchmarks for microservice root cause analysis, though the specific benchmark datasets are not detailed in the abstract. Ground truth for evaluation appears to be established through known fault injection scenarios where the actual root cause service is predetermined. The primary evaluation metric is AC@1, which measures whether the true root cause appears as the top-ranked prediction. DynaCausal achieves an average AC@1 of 0.63 across evaluated scenarios, representing absolute improvements ranging from 0.25 to 0.46 over state-of-the-art baseline methods. The evaluation demonstrates both quantitative accuracy improvements and qualitative interpretability of the diagnoses produced. The consistent performance gains across different scenarios suggest robustness to varying fault types and system configurations in the benchmark environments.

## Stated limitations

The abstract does not explicitly enumerate limitations of the DynaCausal approach. The paper focuses on presenting the method's capabilities and empirical successes rather than discussing boundary conditions or failure modes. No discussion is provided regarding computational complexity, scalability constraints, or scenarios where the approach might underperform. The abstract does not address potential limitations in handling specific types of faults, requirements for training data volume or quality, or challenges in deployment to production environments. The lack of stated limitations in the abstract suggests these considerations may be addressed in the full paper or remain as implicit areas for future investigation.

## Gaps this paper opens

The strong performance improvements suggest that dynamic causality modeling is a promising direction, yet several questions remain unexplored. The paper does not clarify how the framework handles completely novel fault patterns that differ significantly from training data, raising questions about generalization beyond observed failure modes. The interaction between the dynamic contrastive mechanism and the causal-prioritized ranking objective is not detailed, leaving open questions about how these components balance competing signals and whether they might conflict in certain scenarios. The framework's reliance on multi-modal data integration raises questions about performance degradation when certain data modalities are incomplete, delayed, or unavailable, which commonly occurs in production systems. Additionally, the interpretability claims suggest the method provides explanations for its diagnoses, but the nature and granularity of these explanations remain unspecified, creating uncertainty about how operators would use these insights in practice.

## Relevance to the thesis topic

DynaCausal directly addresses the core thesis topic by combining temporal analysis with dependency modeling for root cause analysis in cloud-native systems. The framework's interaction-aware representation learning explicitly captures service dependencies and their evolution over time, aligning with the thesis emphasis on dependency topology. The dynamic contrastive mechanism and causal-prioritized ranking represent sophisticated approaches to temporal causal analysis, distinguishing causal relationships from mere correlations or downstream effects. The method's focus on cascading fault propagation patterns directly relates to understanding how failures propagate through dependency graphs over time. DynaCausal's multi-modal signal fusion and emphasis on time-varying dependencies provide concrete techniques relevant to the thesis framework. The empirical validation on microservice benchmarks and significant performance improvements demonstrate practical viability of combining temporal and dependency analysis for root cause localization, offering both methodological insights and validation approaches applicable to the thesis work.
