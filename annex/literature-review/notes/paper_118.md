---
paper_id: 118
title: "Silent Failures in Stateless Systems: Rethinking Anomaly Detection for Serverless Computing"
authors:
  - Chanh Nguyen
  - Erik Elmroth
  - Monowar Bhuyan
year: 2025
venue: ""
doi: 10.1109/sose67019.2025.00006
arxiv_id: ""
url: "https://openalex.org/W4413679958"
pdf_path: data/pdfs/paper_118.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - distributed_system_monitoring
  - other

method:
  family: other
  specific: vision paper with no specific method proposed
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
  primary_contribution: A comprehensive vision paper identifying unique challenges and research directions for anomaly detection in serverless computing environments.
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

Serverless computing introduces fundamental challenges for anomaly detection due to its stateless, ephemeral, and event-driven nature. Traditional anomaly detection methods designed for stateful, long-running services fail to account for the transient execution model where functions are instantiated on-demand, execute briefly, and terminate immediately. The absence of persistent state makes it difficult to establish baseline behavior patterns that conventional detection systems rely upon. The dynamic scaling and isolated execution of serverless functions create inconsistent monitoring granularity, as observability data may be sparse or incomplete across distributed function invocations. Correlating behaviors across multiple functions becomes problematic when each execution is independent and lacks shared context. These characteristics enable both traditional threats like Denial-of-Service attacks and serverless-specific threats such as Denial-of-Wallet attacks and cold start amplification, which exploit the pay-per-use billing model and function initialization overhead respectively.

## Method summary

This paper does not propose a specific detection method but rather presents a vision and research agenda for future anomaly detection frameworks in serverless environments. The authors systematically analyze the architectural differences between serverless and traditional cloud systems that render existing approaches inadequate. They identify key requirements for next-generation detection frameworks including context-aware analysis that accounts for function-specific execution patterns, multi-source data fusion that integrates logs, metrics, and traces across distributed functions, real-time processing capabilities to match the rapid execution cycles, lightweight implementations that minimize overhead in resource-constrained environments, privacy-preserving mechanisms to protect sensitive data in multi-tenant settings, and edge-cloud adaptive designs that can operate across the continuum from edge devices to centralized cloud infrastructure. The paper articulates design principles rather than concrete algorithms, emphasizing the need for fundamentally new approaches tailored to serverless characteristics.

## Ground truth and evaluation

The paper does not present empirical evaluation or ground truth datasets as it is a vision paper rather than an experimental study. No specific anomaly detection methods are implemented or tested. The authors do not describe existing benchmark datasets for serverless anomaly detection nor propose new evaluation methodologies. The focus remains on conceptual analysis of the problem space and identification of research gaps rather than validation of specific techniques. The paper discusses various threat scenarios including DoS, DoW, and cold start amplification as examples of anomalies that need detection, but these are presented as motivating examples rather than evaluated attack instances. The absence of evaluation frameworks and standardized benchmarks for serverless anomaly detection is implicitly acknowledged as part of the research challenges that need to be addressed by the community.

## Stated limitations

The paper explicitly positions itself as a vision paper and first comprehensive exploration of anomaly detection challenges in serverless computing, acknowledging that it does not provide concrete solutions or implementations. The authors recognize that serverless computing itself is still evolving, with varying implementations across cloud providers that may exhibit different characteristics and monitoring capabilities. The limited observability inherent to serverless platforms constrains what data can be collected for analysis, and the paper notes this as a fundamental challenge rather than a limitation of their work specifically. The transient nature of serverless functions means that traditional profiling and baseline establishment techniques may not apply, but the paper does not propose specific alternatives. The multi-tenancy and distributed nature of serverless deployments raise privacy concerns that complicate data collection and sharing for detection purposes, though concrete privacy-preserving mechanisms are left for future work.

## Gaps this paper opens

The paper identifies numerous open research questions that require investigation. Establishing meaningful baselines for normal behavior in stateless, ephemeral functions remains unsolved, as does the challenge of correlating anomalous patterns across distributed function invocations without persistent state. The paper highlights the need for lightweight detection mechanisms that can operate within the strict resource and latency constraints of serverless environments while maintaining accuracy. Real-time processing requirements conflict with the computational demands of sophisticated anomaly detection algorithms, creating a fundamental tension that needs resolution. The integration of heterogeneous data sources including logs, metrics, traces, and billing information across multiple functions and cloud services lacks established frameworks. Privacy-preserving techniques for multi-tenant serverless environments require development to enable detection without exposing sensitive application data. The paper also opens questions about edge-cloud adaptive detection that can operate across different deployment models and handle the unique characteristics of edge serverless computing.

## Relevance to the thesis topic

This paper addresses anomaly detection in a specific cloud-native architecture but does not directly tackle root cause analysis, temporal causal relationships, or service dependency topology which are central to the thesis topic. While anomaly detection is a prerequisite for root cause analysis, the paper focuses on identifying that anomalies have occurred rather than tracing them to underlying causes or analyzing failure propagation patterns. The serverless context introduces relevant challenges for cloud-native systems generally, particularly around statelessness, ephemeral execution, and limited observability that may apply to containerized microservices as well. However, the paper does not address dependency analysis between functions or temporal propagation of failures through function call chains, which would be more directly relevant to root cause analysis frameworks. The emphasis on multi-source data fusion and correlation across distributed components has conceptual overlap with dependency-aware RCA, but the paper does not develop these connections. The research agenda could inform observability requirements for RCA systems but does not contribute methods for causal inference or dependency discovery.
