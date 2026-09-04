---
paper_id: 246
title: "GALA: Can Graph-Augmented Large Language Model Agentic Workflows Elevate Root Cause Analysis?"
authors:
  - Tian
  - Yifang
  - Yaming Liu
  - Chong
  - Zichun
  - Huang
  - Zihang
  - Hans‐Arno Jacobsen
year: 2025
venue: ArXiv.org
doi: 10.48550/arxiv.2508.12472
arxiv_id: ""
url: "https://openalex.org/W4414487891"
pdf_path: data/pdfs/paper_246.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - service_dependency_topology

method:
  family: hybrid
  specific: LLM agentic workflow with statistical causal inference and service dependency graphs
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
  primary_contribution: A multi-modal RCA framework combining statistical causal inference with LLM-driven iterative reasoning to provide both root cause identification and actionable remediation guidance.
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

Root cause analysis in microservice systems presents significant challenges for on-call engineers who must rapidly diagnose failures across heterogeneous telemetry data including metrics, logs, and traces. Traditional RCA approaches typically focus on analyzing single data modalities in isolation, which limits their diagnostic capability in complex distributed systems. Even when multiple modalities are considered, existing methods often produce only ranked lists of suspect services without providing actionable diagnostic insights or remediation guidance that engineers need for practical incident resolution. The gap between automated failure detection and practical resolution remains substantial, as engineers require not just identification of problematic components but also interpretable explanations and concrete steps for remediation. This challenge is compounded by the complexity of modern cloud-native architectures where failures can propagate through intricate service dependencies in non-obvious ways.

## Method summary

GALA implements a multi-modal framework that integrates statistical causal inference with large language model driven iterative reasoning for root cause analysis. The system constructs service dependency graphs from system topology information and combines this structural knowledge with multi-modal telemetry data including metrics, logs, and traces. Statistical causal inference techniques are applied to identify potential causal relationships between service failures and anomalies in the observability data. The framework employs an LLM-based agentic workflow that performs iterative reasoning over the causal graph and telemetry signals to progressively refine the diagnosis. The LLM agent navigates through the service dependency topology while incorporating evidence from different data modalities to identify root causes. Beyond identifying the root cause service, GALA generates human-interpretable diagnostic explanations and actionable remediation guidance by leveraging the LLM's reasoning capabilities over the integrated multi-modal evidence and structural dependency information.

## Ground truth and evaluation

The evaluation uses an open-source benchmark for microservice RCA that provides ground truth labels for root cause services in failure scenarios. GALA achieves accuracy improvements of up to 42.22 percent over state-of-the-art baseline methods on this benchmark dataset. The paper introduces a novel human-guided LLM evaluation score to assess the quality of diagnostic outputs beyond simple root cause identification accuracy. This evaluation metric measures the causal soundness and actionability of the generated diagnostic explanations and remediation guidance. The human-guided LLM evaluation demonstrates that GALA produces significantly more causally sound and actionable outputs compared to existing methods. The evaluation includes comprehensive experiments across multiple failure scenarios in the benchmark as well as a detailed case study illustrating the practical application of the framework. The case study demonstrates how GALA bridges automated diagnosis with practical incident resolution by providing interpretable explanations alongside accurate root cause identification.

## Stated limitations

The paper does not explicitly enumerate specific limitations of the GALA framework in a dedicated section. However, the reliance on LLM-based reasoning introduces inherent challenges related to the stochastic nature of large language model outputs and potential hallucination issues. The framework's dependency on service topology graphs means its effectiveness is contingent on the accuracy and completeness of the dependency information available in the system. The evaluation is conducted on a single open-source benchmark, which may not capture the full diversity of failure modes and system architectures encountered in production environments. The human-guided LLM evaluation score, while novel, introduces subjectivity in assessing diagnostic quality and may not fully capture all dimensions of practical utility for on-call engineers.

## Gaps this paper opens

The introduction of human-guided LLM evaluation scores for assessing RCA quality opens questions about standardizing evaluation methodologies for LLM-based diagnostic systems beyond simple accuracy metrics. The paper demonstrates the potential of agentic LLM workflows for RCA but does not fully explore the computational costs and latency implications for real-time incident response scenarios. The integration of statistical causal inference with LLM reasoning raises questions about how to optimally balance data-driven causal discovery with LLM-based interpretation and when each approach should take precedence. The framework's ability to generate remediation guidance suggests potential for automated or semi-automated remediation, but the paper does not explore the reliability and safety considerations of acting on LLM-generated recommendations. The multi-modal integration approach leaves open questions about handling conflicting signals across different telemetry types and how to weight evidence from different modalities during the diagnostic process.

## Relevance to the thesis topic

GALA is directly relevant to the thesis topic as it addresses root cause analysis in cloud-native microservice systems through explicit integration of temporal analysis and service dependency topology. The framework's use of service dependency graphs aligns with the thesis focus on dependency analysis, while its processing of time-series metrics and temporal patterns in logs and traces addresses the temporal analysis dimension. The combination of statistical causal inference with LLM-based reasoning provides a concrete example of how temporal causal relationships can be identified and interpreted in distributed systems. The multi-modal approach demonstrates how different types of observability data can be integrated for comprehensive RCA, which is essential for the thesis framework. GALA's emphasis on generating actionable diagnostic outputs and remediation guidance extends beyond simple root cause identification to address the practical needs of incident resolution. The evaluation methodology and benchmark usage provide valuable references for assessing RCA frameworks in the thesis work. The agentic workflow design offers insights into how iterative reasoning over dependency graphs and temporal data can progressively refine diagnostic conclusions.
