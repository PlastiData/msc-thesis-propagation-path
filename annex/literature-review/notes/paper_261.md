---
paper_id: 261
title: Agentic Generative AI Framework for Predictive Fault Detection in Self-Healing Cloud Environments
authors:
  - Ripusoodan Sharma
year: 2026
venue: International Journal for Research in Applied Science and Engineering Technology
doi: 10.22214/ijraset.2026.78761
arxiv_id: ""
url: "https://openalex.org/W7142450926"
pdf_path: data/pdfs/paper_261.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - recommendation_and_remediation

method:
  family: llm
  specific: LLM with Retrieval-Augmented Generation (RAG) and Chain-of-Thought reasoning
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
  primary_contribution: An autonomous self-healing framework that combines LLMs with RAG for context-aware fault detection and automated remediation in cloud environments.
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

Traditional AIOps approaches for fault detection and recovery in cloud-native systems rely on static rules and data-driven models that lack adaptability in dynamic and large-scale environments. The increasing complexity of cloud-native architectures creates challenges for effective fault detection and recovery, requiring systems that can reason contextually and adapt to evolving operational conditions. Existing methods struggle with minimal human intervention requirements and often fail to incorporate historical incident knowledge effectively. The need exists for intelligent systems that can continuously monitor, reason about telemetry data, identify root causes autonomously, and perform automated recovery actions while maintaining high reliability and efficiency.

## Method summary

The ARCH framework implements a layered architecture consisting of perception, cognition, knowledge, and action components. The perception layer continuously monitors telemetry data from cloud-native systems. The cognition layer employs Large Language Models with Chain-of-Thought reasoning strategies to analyze telemetry data and perform intelligent reasoning about system states. The knowledge layer integrates Retrieval-Augmented Generation to enhance contextual awareness by incorporating historical incident knowledge and patterns into the reasoning process. The action layer executes autonomous remediation decisions based on the cognitive analysis. The framework leverages agentic reasoning strategies that enable action-oriented decision-making, allowing the system to identify root causes and execute recovery procedures with minimal human intervention. Predictive fault detection capabilities utilize historical telemetry patterns to anticipate potential failures before they manifest.

## Ground truth and evaluation

The framework evaluation uses Mean Time to Repair (MTTR), Autonomous Success Rate (ASR), and system efficiency as key performance metrics. The paper reports experimental results comparing the ARCH framework against baseline approaches, though the specific nature of these baseline methods is not detailed. The evaluation demonstrates an 82% reduction in MTTR and an 89.5% autonomous success rate. The paper does not explicitly describe the dataset used for evaluation, the source of ground truth labels for root causes, or how the autonomous success rate was validated. The experimental setup details regarding the cloud environment configuration, the types of faults injected or observed, and the methodology for establishing ground truth for root cause identification are not provided in the abstract.

## Stated limitations

The abstract does not explicitly state limitations of the proposed ARCH framework. No discussion is provided regarding computational overhead of LLM-based reasoning, potential latency issues in real-time fault detection scenarios, or limitations in handling specific types of failures. The paper does not address challenges related to LLM hallucination risks in critical remediation decisions or the framework's performance boundaries. There is no mention of scalability constraints, the types of cloud environments tested, or limitations in the diversity of fault scenarios evaluated. The reliability of autonomous remediation actions and potential risks of incorrect automated interventions are not discussed.

## Gaps this paper opens

The paper does not provide sufficient detail on how ground truth for root cause analysis was established or validated, creating uncertainty about evaluation rigor. The relationship between the RAG component and specific root cause identification accuracy remains unclear, particularly regarding how historical knowledge retrieval contributes to causal reasoning. The framework's handling of temporal dependencies and failure propagation patterns across distributed services is not addressed. The paper does not explain how the system distinguishes between correlation and causation when analyzing telemetry data or how it handles cascading failures. The integration of service dependency topology information into the reasoning process is not described. The predictive fault detection mechanism lacks detail on how temporal patterns are learned and how prediction accuracy is measured across different failure types.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it addresses root cause analysis in cloud-native systems using an LLM-based approach. The framework's focus on autonomous fault detection and remediation directly relates to the thesis goal of developing RCA methodologies. However, the paper's emphasis differs from the thesis focus on temporal and dependency analysis. While the ARCH framework mentions utilizing historical telemetry patterns for predictive detection, it does not explicitly detail temporal causal analysis mechanisms or how service dependency topology is modeled and leveraged. The RAG component provides historical context but the paper does not describe explicit temporal failure propagation analysis. The framework represents an alternative approach to RCA that prioritizes LLM-based reasoning over structured temporal and dependency modeling, offering a comparison point for understanding different architectural choices in cloud-native RCA systems.
