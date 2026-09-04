---
paper_id: 119
title: "End-to-End Visibility in Cloud Deployments: Building Real-Time Program Health Systems"
authors:
  - Soumya Remella
year: 2025
venue: International Journal of AI BigData Computational and Management Studies
doi: 10.63282/3050-9416.ijaibdcms-v6i4p117
arxiv_id: ""
url: "https://openalex.org/W7118497068"
pdf_path: data/pdfs/paper_119.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - observability_data_analysis
  - distributed_system_monitoring

method:
  family: hybrid
  specific: multi-layer telemetry fusion with ML-based anomaly detection and health scoring
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
  primary_contribution: A unified real-time framework that integrates logs, metrics, traces, and events into a single health model to improve anomaly detection and cross-service correlation in cloud-native systems.
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

Cloud-native applications generate heterogeneous telemetry signals including logs, metrics, traces, and events across distributed services, containers, and serverless functions. Existing observability tools collect these signals effectively but process them in isolation, requiring engineers to manually correlate symptoms during incidents. This fragmentation creates delays in anomaly detection, obscures root-cause analysis, and prevents real-time understanding of overall program health. The core challenge is that signal-specific monitoring approaches fail to provide a unified view of system behavior, leading to slower incident response and increased operational burden on engineering teams.

## Method summary

The Real-Time Program Health Framework operates as a multi-layer model that unifies telemetry processing. The framework ingests logs, metrics, traces, and events from distributed cloud-native services and applies real-time stream processing to these heterogeneous signals. Machine learning models perform anomaly detection on the unified telemetry stream, identifying deviations from normal behavior patterns. The system then computes health scores that aggregate anomaly signals into an interpretable view of overall system state. This multi-layer architecture enables cross-service correlation by processing telemetry signals together rather than in isolated pipelines, allowing the framework to detect anomalies that span multiple services and present them through a single unified interface.

## Ground truth and evaluation

The framework is evaluated in a hybrid cloud environment running microservice workloads on Kubernetes. Synthetic faults are injected under controlled conditions to generate known anomalies. Performance is compared against established observability stacks that combine metrics, logging, and tracing tools as baseline systems. The evaluation measures anomaly detection latency, false-positive alert rates, and cross-service anomaly correlation accuracy. Resource overhead is assessed by monitoring CPU and memory consumption per node. The synthetic fault injection approach provides ground truth for anomaly timing and location, enabling measurement of detection latency and correlation correctness. The controlled experimental setup allows direct comparison between the unified RTPH approach and traditional signal-specific monitoring methods.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed framework. The evaluation relies on synthetic fault injection in a controlled environment, which may not capture the full complexity of production failure scenarios. The specific types of faults injected and the diversity of microservice workloads tested are not detailed, leaving uncertainty about generalizability. The machine learning models used for anomaly detection are not described in detail, making it unclear how they handle concept drift or require retraining. The framework's performance under extreme load conditions or with very large-scale deployments remains uncharacterized. No discussion is provided about the operational complexity of deploying and maintaining the multi-layer architecture in production environments.

## Gaps this paper opens

The framework focuses on anomaly detection and health scoring but does not address root cause localization or causal analysis of detected anomalies. While cross-service correlation is measured, the paper does not explain how temporal dependencies or failure propagation patterns are modeled or leveraged. The relationship between detected anomalies and their underlying causes remains unexplored, leaving a gap in translating health scores into actionable diagnostic information. The framework does not incorporate service dependency topology or call graphs, which could enhance correlation accuracy. There is no mechanism described for explaining why specific health scores were assigned or which telemetry signals contributed most to anomaly detection. The evaluation does not assess whether the unified view actually reduces mean time to resolution in realistic incident scenarios.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses observability and anomaly detection in cloud-native systems but does not focus on root cause analysis. The framework's cross-service correlation capability relates to understanding dependencies, but it does not explicitly model service topology or temporal causal relationships. The unified telemetry processing approach could serve as a foundation for root cause analysis by providing integrated signals, but the paper stops at anomaly detection and health scoring. The temporal aspects of the framework involve real-time stream processing for detection latency reduction rather than analyzing temporal propagation of failures across services. While the work demonstrates value in integrating heterogeneous observability signals, it does not address the causal reasoning or dependency-aware analysis central to the thesis topic. The evaluation methodology using synthetic faults in Kubernetes environments provides relevant context for understanding cloud-native failure scenarios.
