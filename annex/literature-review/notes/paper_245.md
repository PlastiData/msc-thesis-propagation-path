---
paper_id: 245
title: AI/ML Powered Intelligent Root Cause Analysis and Automated Remediation for Multi System Data Integrity Issues
authors:
  - Vineeth Kumar Reddy Mittamidi
year: 2025
venue: International Journal of AI BigData Computational and Management Studies
doi: 10.63282/3050-9416.ijaibdcms-v6i4p115
arxiv_id: ""
url: "https://openalex.org/W7117569635"
pdf_path: data/pdfs/paper_245.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - recommendation_and_remediation
  - observability_data_analysis

method:
  family: hybrid
  specific: graph-based dependency localization with LLM-assisted evidence synthesis and graduated autonomy remediation
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
  primary_contribution: A unified architecture combining contract-based quality checks, provenance reasoning, dependency-aware localization, and graduated autonomy remediation for multi-system data integrity incidents in enterprise data platforms.
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

Data integrity incidents in enterprise environments emerge from complex interactions across operational databases, event streams, microservices, batch ETL workflows, data warehouses and analytics products. These incidents rarely originate from a single component but instead result from interacting failure modes including schema drift, late or duplicated events, inconsistent reference data, partial writes, replay defects and misaligned transformation logic. Such failures propagate across system boundaries and can silently corrupt business reporting, customer experiences and compliance artifacts. Current observability solutions provide improved visibility into distributed systems but diagnosis and recovery remain heavily dependent on human expertise and manual correlation across heterogeneous telemetry including logs, traces, metrics and change histories. The challenge is to automate root cause analysis and remediation for these multi-system data integrity issues while maintaining auditability and safety of corrective actions.

## Method summary

The proposed architecture integrates multiple components for detection, localization and remediation. Contract-based data quality checks are grounded in established data quality dimensions and pipeline quality taxonomies derived from developer evidence. The system employs provenance and lineage reasoning to trace data flows and support debugging across system boundaries. Dependency-aware localization adapts techniques from microservice RCA to identify failure propagation paths in data pipelines. Incident knowledge retrieval leverages patterns mined from real cloud incident investigations to inform diagnosis. The remediation framework applies graduated autonomy with policy gating inspired by agentic AIOps architectures. Large language models are used only for evidence synthesis and remediation plan drafting under strict guardrails to ensure safety. The system constructs a graph-based representation of data dependencies and uses this topology along with temporal analysis to localize root causes. The remediation catalog contains pre-validated corrective actions that can be automatically applied based on incident classification and policy constraints.

## Ground truth and evaluation

The paper describes evaluation metrics for detection, localization and recovery but does not specify concrete ground truth sources or experimental datasets. The proposed metrics include mean time to detection and mean time to recovery as primary measures of system effectiveness. The architecture is designed to improve auditability of both diagnosis and corrective actions in enterprise data platforms. The evaluation framework appears to focus on operational metrics that demonstrate reduced incident resolution time and improved safety of automated remediation. The paper references taxonomies and root causes mined from developer evidence and real cloud incident investigations but does not detail how these were collected or validated. No specific benchmark datasets or controlled experiments are described for validating the RCA accuracy or remediation effectiveness.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed approach. The architecture description emphasizes strict guardrails around LLM usage, suggesting awareness of risks in applying generative models to critical remediation tasks. The graduated autonomy framework with policy gating indicates recognition that full automation may not be appropriate for all incident types or organizational contexts. The reliance on contract-based quality checks implies that the system requires upfront specification of expected data properties and may not detect novel or unanticipated failure modes. The dependency on provenance and lineage information suggests the approach requires comprehensive instrumentation of data flows which may not exist in all enterprise environments. The paper does not discuss computational costs, scalability limits, false positive rates or scenarios where automated remediation might introduce additional risks.

## Gaps this paper opens

The paper does not provide implementation details for the graph-based RCA method or specify how temporal analysis is integrated with dependency reasoning. The incident taxonomy is mentioned but not fully described, leaving unclear how incidents are classified and mapped to remediation strategies. The graduated autonomy framework and policy gating mechanisms are referenced but not detailed, creating uncertainty about how automation decisions are made and what safety constraints are enforced. The role of LLMs in evidence synthesis and plan drafting is constrained by guardrails but the nature of these guardrails and their effectiveness is not evaluated. The paper does not address how the system handles evolving data ecosystems where dependencies and contracts change over time. The relationship between different components such as contract checking, provenance reasoning and dependency localization is described architecturally but their integration and relative contributions to RCA accuracy are not quantified. No comparison with existing RCA approaches or ablation studies are presented.

## Relevance to the thesis topic

This paper is directly relevant to the thesis topic as it addresses root cause analysis in distributed systems using both temporal and dependency analysis. The graph-based dependency-aware localization aligns with the thesis focus on service dependency topology while the temporal aspects of failure propagation across data pipelines relate to temporal causal analysis. The multi-system data integrity context extends beyond traditional cloud-native microservices to include data platforms but the fundamental challenges of dependency tracking and temporal reasoning are shared. The combination of provenance reasoning and dependency graphs provides a concrete example of how topology and temporal information can be integrated for RCA. The graduated autonomy remediation framework demonstrates how RCA outputs can drive automated corrective actions. The emphasis on auditability and safety constraints is relevant for practical deployment of RCA systems. The hybrid approach combining multiple techniques including contract checking, lineage tracing and incident knowledge retrieval illustrates the complexity of real-world RCA systems beyond pure algorithmic solutions.
