---
paper_id: 102
title: Survey on AI-Based Reliability and Anomaly Detection in Microservices
authors:
  - Muzeeb Mohammad
year: 2026
venue: International Journal of Computer Applications
doi: 10.5120/ijca2026926263
arxiv_id: ""
url: "https://openalex.org/W7124954587"
pdf_path: data/pdfs/paper_102.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - root_cause_analysis
  - observability_data_analysis

method:
  family: other
  specific: survey and taxonomy of AI-based approaches
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
  primary_contribution: A comprehensive taxonomy and survey of AI-driven anomaly detection and reliability techniques for microservices across observability signals, modeling approaches, and deployment layers.
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

Microservice architectures have become the dominant paradigm for building scalable and agile applications, but their inherent complexity creates substantial reliability challenges. Traditional monitoring approaches are insufficient for handling the dynamic and distributed nature of microservices, where failures can cascade across service boundaries and manifest in unpredictable ways. The distributed topology, ephemeral service instances, and high volume of observability data make manual fault detection and diagnosis impractical. This motivates the need for AI-driven techniques that can automatically detect anomalies, predict failures, and support root cause analysis in real-time. The paper addresses the broader challenge of understanding how different AI approaches can be applied to improve reliability in microservice ecosystems.

## Method summary

This survey proposes a three-dimensional taxonomy for organizing AI-based anomaly detection approaches in microservices. The first dimension categorizes systems by the observability signals they consume, including metrics, logs, and traces. The second dimension classifies the modeling techniques employed, ranging from statistical methods and classical machine learning through deep learning architectures, graph-based methods that leverage service dependency structures, and emerging large language model approaches. The third dimension considers the deployment layer where detection operates, distinguishing between centralized cloud clusters, distributed edge environments, and service mesh implementations. The survey systematically reviews representative systems and frameworks across these dimensions, comparing their architectural choices, data requirements, and operational characteristics.

## Ground truth and evaluation

The survey identifies the scarcity of real-world labeled anomalies as a fundamental challenge across the field. Most systems are evaluated using synthetic fault injection or limited datasets from specific production environments, making cross-system comparison difficult. The paper discusses various evaluation metrics used in different studies, including precision, recall, F1-scores for classification tasks, and time-to-detection for operational performance. The entropy gap in anomaly scoring is highlighted as a persistent issue, where distinguishing true anomalies from normal operational variance remains challenging. The survey notes that many approaches lack standardized benchmarks, and ground truth establishment often relies on incident reports, manual labeling by operators, or controlled experiments that may not reflect real production complexity.

## Stated limitations

The survey explicitly identifies several limitations in current AI-based reliability approaches for microservices. The scarcity of real-world labeled anomaly datasets limits both training effectiveness and comparative evaluation across different methods. Interpretability and explainability remain significant challenges, particularly for deep learning approaches, which is critical for operator trust and effective root cause analysis. Compute constraints in distributed and edge environments restrict the deployment of sophisticated models that might work well in centralized cloud settings. The entropy gap problem means that many systems struggle to distinguish meaningful anomalies from normal operational noise. The survey also notes that multimodal data fusion across metrics, logs, and traces remains an open challenge, with most systems focusing on single data modalities.

## Gaps this paper opens

The survey identifies several open research directions that emerge from its comprehensive review. Multimodal data fusion techniques that effectively combine metrics, logs, and traces remain underdeveloped, despite the potential for improved detection accuracy. Federated and edge-based detection approaches are needed to handle privacy constraints and latency requirements in distributed deployments. Human-in-the-loop root cause analysis represents an important frontier, where AI systems need to better support operator decision-making rather than attempting fully autonomous diagnosis. The integration of large language models for log analysis and incident summarization is nascent and requires further investigation. Standardized benchmarks and evaluation frameworks are needed to enable rigorous comparison across different approaches. The survey also points to the need for techniques that can adapt to evolving microservice topologies and changing operational patterns without extensive retraining.

## Relevance to the thesis topic

This survey is highly relevant to the thesis topic as it provides comprehensive coverage of AI-based anomaly detection approaches that form the foundation for root cause analysis in cloud-native systems. The taxonomy of observability signals directly addresses the types of temporal data that dependency and causal analysis must process. The discussion of graph-based methods connects to service dependency topology analysis, which is central to the thesis framework. The identification of challenges around interpretability and human-in-the-loop analysis aligns with the need for explainable root cause identification. The survey's emphasis on multimodal data fusion across metrics, logs, and traces supports the thesis goal of integrating temporal patterns with dependency structures. The open problems identified, particularly around standardized evaluation and real-world datasets, inform the benchmarking and validation requirements for the proposed framework.
