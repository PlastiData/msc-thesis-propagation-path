---
paper_id: 087
title: Autonomous AI Agents for Site Reliability Engineering
authors:
  - Selvakumar Kalyanasundaram
year: 2026
venue: International Journal of Artificial Intelligence Data Science and Machine Learning
doi: 10.63282/3050-9262.ijaidsml-v7i1p162
arxiv_id: ""
url: "https://openalex.org/W7153171236"
pdf_path: data/pdfs/paper_087.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - anomaly_detection
  - recommendation_and_remediation

method:
  family: hybrid
  specific: multi-agent system with ML anomaly detection, graph-based RCA, LLM reasoning, and reinforcement learning
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
  primary_contribution: A multi-agent AI framework that autonomously detects anomalies, diagnoses root causes using dependency graphs, and executes automated remediation in cloud-native systems.
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

Modern cloud-native infrastructures built on microservices architectures and container orchestration platforms generate massive volumes of telemetry data that overwhelm traditional Site Reliability Engineering teams. The distributed nature of these systems creates complexity in incident management where failures can propagate through multiple services in unpredictable ways. Manual approaches to anomaly detection, root cause diagnosis, and remediation cannot scale to handle the velocity and volume of operational data in dynamic scaling environments. The challenge is to maintain system reliability while reducing the burden on human operators who must currently correlate signals across logs, metrics, and traces to understand system behavior and respond to incidents.

## Method summary

The proposed framework employs a multi-agent architecture where specialized AI agents collaborate to handle different aspects of SRE operations. Machine learning models perform anomaly detection on incoming telemetry streams to identify deviations from normal system behavior. The system constructs a dynamic dependency graph representing relationships between services and components in the cloud infrastructure. Graph-based root cause analysis algorithms traverse this dependency graph to identify failure propagation paths and locate the origin of incidents. Large language models provide reasoning capabilities to interpret operational knowledge, documentation, and historical incident data to support diagnostic decisions. Reinforcement learning policies learn optimal remediation actions through interaction with the system, enabling automated execution of corrective measures. The agents process logs, metrics, and traces in an integrated pipeline that flows from detection through diagnosis to remediation.

## Ground truth and evaluation

The paper reports experimental results showing an 83% reduction in mean time to detect anomalies and an 80% reduction in mean time to resolve incidents compared with traditional SRE workflows. These metrics indicate comparison against baseline human-operated or conventional automated systems. The evaluation demonstrates improvements in operational efficiency measured through standard SRE performance indicators. The paper does not specify the dataset characteristics, the number of incidents evaluated, the specific cloud environment tested, or whether ground truth root causes were independently verified. The comparison baseline appears to be existing SRE practices rather than other automated RCA approaches.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed framework. There is no discussion of scenarios where the multi-agent system might fail or perform poorly. The paper does not address potential challenges in deploying the framework across different cloud platforms or technology stacks. No analysis is provided regarding the computational overhead of maintaining dynamic dependency graphs or running multiple AI models simultaneously. The paper does not discuss limitations related to the accuracy of the dependency graph construction, potential errors in LLM reasoning, or safety concerns around autonomous remediation actions that could potentially worsen system state.

## Gaps this paper opens

The lack of detail about the dependency graph construction methodology leaves open questions about how the system handles dynamic service topologies and discovers relationships in real-time. The integration mechanism between the different AI components including anomaly detection, graph analysis, LLM reasoning, and reinforcement learning is not thoroughly explained, creating uncertainty about coordination and information flow. The paper does not provide specifics on how the reinforcement learning agents are trained safely without causing production incidents or how their action space is constrained. The evaluation lacks comparison with other state-of-the-art RCA methods and does not report accuracy metrics for root cause identification. The framework's ability to handle novel failure modes not seen during training remains unclear, as does its performance across different types of cloud-native applications.

## Relevance to the thesis topic

This paper is directly relevant to the thesis as it addresses root cause analysis in cloud-native systems using both dependency analysis and temporal reasoning. The dynamic dependency graph construction aligns with the thesis focus on service dependency topology for understanding failure propagation. The framework's processing of temporal telemetry signals including logs, metrics, and traces connects to temporal analysis approaches for RCA. The multi-agent architecture demonstrates how different analytical techniques can be combined for comprehensive root cause diagnosis. However, the paper's emphasis on autonomous remediation and reinforcement learning extends beyond pure RCA into operational automation. The graph-based failure propagation path identification is particularly relevant to understanding how failures cascade through dependencies, which is central to the thesis framework.
