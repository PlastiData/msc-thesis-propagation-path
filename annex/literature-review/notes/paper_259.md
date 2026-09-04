---
paper_id: 259
title: "From Observability to Understanding: Automated Incident Triage Using Large Language Model Reasoning Over Logs, Metrics, and Traces"
authors:
  - USA Senior Java Full Stack Developer
  - Sriram Ghanta
year: 2023
venue: International Journal of Engineering & Extended Technologies Research
doi: 10.15662/ijeetr.2023.0505009
arxiv_id: ""
url: "https://openalex.org/W7128806013"
pdf_path: data/pdfs/paper_259.pdf
read_date: 2026-05-11

category:
  - llm_based_rca
  - root_cause_analysis
  - observability_data_analysis

method:
  family: llm
  specific: LLM reasoning over multi-modal telemetry (logs, metrics, traces)
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
  primary_contribution: An automated incident triage framework that uses LLM reasoning to semantically interpret and correlate heterogeneous telemetry data across temporal and causal boundaries for root cause diagnosis.
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

Modern cloud-native microservice architectures produce massive volumes of heterogeneous telemetry data including logs, metrics, and distributed traces due to fine-grained service decomposition and elastic scaling. The velocity, high dimensionality, and predominantly unstructured nature of these signals overwhelm traditional rule-based incident triage systems and threshold-driven alerting mechanisms. Existing AIOps solutions rely primarily on statistical anomaly detection or supervised learning models trained on historical failure patterns, which are effective for known issues but struggle to generalize to unseen failure modes. These approaches face particular difficulty with rapidly evolving system topologies and context-dependent cascading faults that characterize modern production environments. The fundamental challenge is elevating telemetry analysis from low-level signal detection to high-level operational reasoning that can handle novel and complex failure scenarios.

## Method summary

The proposed framework leverages Large Language Model reasoning capabilities to perform automated incident triage over structured logs, metrics, and distributed traces. The system enables LLMs to semantically interpret multi-modal telemetry data by correlating signals across temporal and causal boundaries. The framework synthesizes coherent causal narratives that describe system failures by analyzing the relationships between different telemetry types. It ranks probable root causes and generates actionable remediation hypotheses expressed in natural language. The approach integrates LLM-based reasoning on top of existing observability pipelines, allowing organizations to preserve their proven monitoring infrastructures while adding intelligent interpretation capabilities. The framework builds upon foundational research in distributed tracing, log parsing, and machine learning-based anomaly detection to create a system that performs high-level operational reasoning rather than simple signal detection.

## Ground truth and evaluation

The paper does not provide explicit details about ground truth sources, evaluation datasets, or experimental validation. No specific metrics are reported for measuring the effectiveness of the LLM-based triage system such as accuracy in root cause identification, reduction in mean time to diagnosis, or comparison with baseline methods. The paper does not describe whether the framework was evaluated on real production incidents, synthetic failure injection scenarios, or public benchmark datasets. No information is provided about how the quality of generated causal narratives or remediation hypotheses was assessed. The absence of concrete evaluation methodology makes it difficult to assess the practical effectiveness of the proposed approach or validate the claimed benefits of reduced MTTD and improved operator situational awareness.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed framework. No discussion is provided regarding potential failure modes of LLM reasoning, such as hallucination or generation of incorrect causal explanations. The paper does not address computational costs or latency concerns associated with processing large volumes of telemetry through LLMs during active incidents. There is no mention of limitations related to the quality or completeness of input telemetry data, or how the system handles missing or corrupted signals. The paper does not discuss challenges in prompt engineering, context window limitations for processing extensive telemetry histories, or the need for domain-specific fine-tuning. No consideration is given to the interpretability or verifiability of LLM-generated diagnoses, which could be critical for operator trust and accountability in production environments.

## Gaps this paper opens

The absence of concrete evaluation creates a significant gap in understanding the practical effectiveness and reliability of LLM-based incident triage in production environments. The paper does not address how to construct appropriate prompts or structure telemetry data for optimal LLM reasoning, leaving open questions about the engineering required for real-world deployment. There is no exploration of how the framework handles the inherent non-determinism of LLM outputs or ensures consistency in root cause diagnosis across similar incidents. The paper does not investigate the relationship between service dependency topology and LLM reasoning quality, particularly for understanding cascading failures. The integration mechanism between existing observability pipelines and LLM reasoning remains underspecified, creating uncertainty about implementation complexity. The framework does not address how to validate or verify LLM-generated causal narratives against actual system behavior, which is essential for building operator confidence and preventing misdiagnosis.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in cloud-native systems using reasoning over observability data. The framework's focus on correlating signals across temporal and causal boundaries aligns with the thesis emphasis on temporal and dependency analysis. The paper demonstrates how LLM reasoning can synthesize causal narratives from multi-modal telemetry, which relates to understanding failure propagation patterns through service dependencies. However, the paper lacks the structured temporal analysis and explicit dependency topology modeling that the thesis proposes to emphasize. The LLM-based approach offers a complementary perspective to more deterministic temporal causal analysis methods, suggesting potential hybrid approaches. The paper's emphasis on handling unseen failure modes and evolving topologies highlights challenges that the thesis framework must address. The integration with existing observability pipelines provides practical context for how advanced RCA techniques can be deployed in real systems.
