---
paper_id: 194
title: Multi-Modal Foundation Models for Unified Log, Trace, and Metric Reasoning in Service Graph Diagnosis
authors:
  - Adrien Moreau
  - Katarina Jović
year: 2025
venue: American Journal of Machine Learning
doi: 10.71465/ajml3451
arxiv_id: ""
url: "https://openalex.org/W7118246032"
pdf_path: data/pdfs/paper_194.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - observability_data_analysis
  - service_dependency_topology

method:
  family: hybrid
  specific: transformer foundation model with graph neural network and contrastive learning
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
  primary_contribution: A framework that unifies reasoning across logs, traces, and metrics using multi-modal foundation models combined with graph neural networks for service graph diagnosis.
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

Modern cloud-native microservice architectures produce heterogeneous telemetry data across three primary modalities: logs, distributed traces, and performance metrics. Traditional diagnostic approaches process these data sources in isolation, which prevents the discovery of critical cross-modal correlations that are essential for comprehensive system understanding. This siloed processing limits the effectiveness of service graph diagnosis and root cause analysis because faults often manifest differently across modalities and their relationships contain diagnostic information that single-modality analysis cannot capture. The challenge lies in developing a unified framework that can reason across these diverse data types while maintaining the unique characteristics of each modality that are crucial for accurate fault localization in complex distributed systems.

## Method summary

The proposed framework integrates transformer-based foundation models with graph neural networks to enable unified reasoning across logs, traces, and metrics. The architecture captures sequential patterns within individual telemetry modalities using transformer encoders while simultaneously modeling structural dependencies across the service graph through graph neural networks. The system employs contrastive learning as a key mechanism to align representations from different telemetry sources, ensuring that related signals from different modalities are mapped to similar embedding spaces. This alignment process preserves modality-specific characteristics that remain important for diagnostic accuracy. The foundation models process the raw telemetry data to extract high-level semantic features, which are then combined with graph structural information to perform anomaly detection and root cause identification. The multi-modal nature of the approach allows the system to leverage complementary information from logs, traces, and metrics simultaneously during the diagnostic process.

## Ground truth and evaluation

The framework is evaluated on industry-standard microservice benchmarks, though the paper does not specify which particular benchmark datasets or systems were used. The evaluation compares the proposed multi-modal approach against both single-modality methods that process only one type of telemetry data and traditional multi-modal methods that combine multiple data sources. Performance is measured in terms of anomaly detection accuracy and root cause identification effectiveness. The experimental results demonstrate that the unified multi-modal foundation model approach achieves superior performance compared to baseline methods across these metrics. The paper claims the approach outperforms existing techniques but does not provide specific quantitative performance numbers or details about how ground truth labels for anomalies and root causes were obtained or validated.

## Stated limitations

The paper does not explicitly state limitations of the proposed approach. There is no discussion of computational costs associated with running large foundation models in production environments or the latency implications for real-time diagnosis. The paper does not address challenges related to training data requirements for the foundation models or how the system handles novel failure modes not seen during training. There is no mention of the interpretability of the multi-modal representations or how operators can understand the reasoning behind diagnostic conclusions. The scalability of the approach to very large service graphs with hundreds or thousands of microservices is not discussed, nor are there considerations about the overhead of collecting and processing multiple telemetry modalities simultaneously.

## Gaps this paper opens

The lack of detail about specific benchmark datasets and evaluation methodology creates uncertainty about reproducibility and generalizability of the results. The paper does not explain how the contrastive learning mechanism specifically aligns different modality representations or what training objectives are used beyond the general concept of alignment. There is insufficient information about how the graph neural network component integrates with the transformer-based foundation models or how information flows between these architectural components. The paper does not address how temporal dependencies are captured across modalities, particularly for understanding failure propagation patterns over time. The relationship between the service graph topology and the multi-modal analysis is underspecified, leaving unclear how dependency information influences the diagnostic reasoning. Questions remain about how the system handles missing or incomplete telemetry data and whether all three modalities are required for effective diagnosis.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in cloud-native systems using multiple observability data sources. The integration of service graph topology with multi-modal telemetry analysis aligns with the thesis focus on dependency analysis for RCA. The use of foundation models to reason across logs, traces, and metrics represents a modern approach to the observability data analysis component of the thesis framework. However, the paper appears to lack the explicit temporal analysis emphasis that is central to the thesis topic, particularly regarding how failures propagate through service dependencies over time. The framework could inform the thesis by demonstrating how different telemetry modalities can be unified for diagnosis, though the thesis would need to extend this with more explicit temporal causal reasoning. The graph neural network component for modeling service dependencies provides relevant architectural insights for incorporating topology into RCA frameworks, which directly supports the dependency analysis pillar of the thesis.
