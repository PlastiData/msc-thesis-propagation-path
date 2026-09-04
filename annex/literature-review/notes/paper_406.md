---
paper_id: 406
title: "TSGuard: Automated User-Centric Incident Diagnosis for AI Workloads in the Cloud"
authors:
  - Yitao Yang
  - Yangtao Deng
  - Yifan Xiong
  - Baochun Li
  - Hong Xu
  - Peng Cheng
year: 2025
venue: ""
doi: ""
arxiv_id: 2506.01481
url: "https://www.semanticscholar.org/paper/71016323bab0600da2fa1dea56882292d69b43a8"
pdf_path: data/pdfs/paper_406.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - recommendation_and_remediation

method:
  family: llm
  specific: multi-agent LLM system with structured reasoning and knowledge base retrieval
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
  primary_contribution: A user-centric multi-agent system that provides immediate incident diagnosis for AI workloads by mining historical troubleshooting knowledge and mimicking expert diagnosis through structured reasoning.
  novelty_strength: moderate

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

AI workloads deployed on cloud infrastructure experience frequent failures and incidents originating from the underlying infrastructure layer. The current incident management workflow operates under a provider-centric paradigm where users must report incidents to the infrastructure provider who then performs manual troubleshooting. This manual process is slow and resource-intensive, often requiring several days to resolve a single incident due to the high volume of incidents and limited expert availability. The delays result in significant operational disruptions and productivity losses for users running AI workloads. The fundamental challenge is enabling faster incident resolution while maintaining diagnostic accuracy, particularly in scenarios where users lack direct visibility into the infrastructure layer causing the failures.

## Method summary

TSGuard implements a user-centric multi-agent system that shifts incident diagnosis capability from the provider to the user side, enabling immediate troubleshooting without waiting for provider intervention. The system operates in two phases. In the offline phase, TSGuard constructs domain-specific knowledge bases by mining historical on-call experiences and troubleshooting records to capture expert knowledge about common failure patterns and diagnostic procedures. In the online phase, when an incident occurs, TSGuard mimics human expert diagnosis through structured reasoning and iterative trial-and-error processes. The multi-agent architecture coordinates different specialized agents that work together to analyze symptoms, hypothesize potential root causes, and verify diagnoses through systematic exploration. The system leverages large language models as the reasoning engine within each agent while grounding their decisions in the mined knowledge bases to ensure domain-specific accuracy.

## Ground truth and evaluation

The evaluation uses production incident records from Microsoft Azure as the ground truth dataset. The paper reports that TSGuard improves diagnostic accuracy by 19.8% compared to state-of-the-art baselines, demonstrating superior performance in identifying correct root causes. The system also reduces average verification time by 63.4% compared to sequential execution baselines, indicating significant efficiency gains in the diagnostic process. The evaluation appears to measure both the correctness of the final diagnosis and the time required to reach that diagnosis. The use of real production incidents from a major cloud provider lends credibility to the results, though the paper does not explicitly detail the size of the evaluation dataset or the specific metrics used to define diagnostic accuracy beyond the percentage improvement figures.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the focus on AI workloads specifically suggests the approach may be tailored to this domain and might require adaptation for other workload types. The reliance on historical on-call experiences for knowledge base construction implies that the system's effectiveness depends on the availability and quality of historical troubleshooting records. The multi-agent architecture and iterative trial-and-error approach, while mimicking human experts, may introduce complexity in terms of computational overhead and potential for cascading errors across agents. The evaluation being limited to Microsoft Azure infrastructure means generalizability to other cloud providers or on-premises environments remains unclear.

## Gaps this paper opens

The paper does not address how TSGuard handles novel incidents that lack historical precedent in the knowledge base, leaving open questions about its ability to diagnose truly unprecedented failures. The relationship between incident characteristics and diagnostic accuracy is not explored, making it unclear which types of incidents benefit most from the multi-agent approach versus simpler methods. The paper does not discuss how the system maintains and updates its knowledge base as new incidents occur and new troubleshooting patterns emerge over time. The interaction between multiple concurrent incidents and potential resource contention in the multi-agent system is not examined. The paper also does not explore how TSGuard integrates with existing monitoring and observability systems or what specific telemetry data it requires to perform diagnosis, leaving the data requirements and integration complexity unclear.

## Relevance to the thesis topic

TSGuard addresses root cause analysis in cloud infrastructure supporting AI workloads, which aligns with the thesis focus on cloud-native systems. However, the paper's emphasis on user-centric incident diagnosis and LLM-based multi-agent reasoning differs from the thesis focus on temporal and dependency analysis. The system relies primarily on mining historical knowledge and structured reasoning rather than analyzing temporal patterns of failures or service dependency topologies in real-time. While TSGuard performs root cause analysis, its methodology centers on knowledge retrieval and agent-based reasoning rather than the temporal causal analysis and dependency graph construction that form the core of the thesis framework. The work is relevant as a complementary approach showing how LLMs can be applied to RCA problems, but it does not directly contribute techniques for temporal failure propagation analysis or dependency-based root cause localization that the thesis aims to develop.
