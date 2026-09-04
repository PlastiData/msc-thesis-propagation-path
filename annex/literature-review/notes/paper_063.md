---
paper_id: 063
title: "TrustGraph: A Heterogeneous GNN for Dynamic Zero-Trust Policy Enforcement in Microservices"
authors:
  - Nurmyrat Amanmadov
  - Jemshit Iskanderov
  - Tarlan Abdullayev
year: 2025
venue: International Journal of Advanced Computer Science and Applications
doi: 10.14569/ijacsa.2025.0161205
arxiv_id: ""
url: "https://openalex.org/W7117964361"
pdf_path: data/pdfs/paper_063.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - service_dependency_topology
  - root_cause_analysis

method:
  family: deep_learning
  specific: heterogeneous graph neural network with attention
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
  primary_contribution: A heterogeneous GNN framework that integrates multi-modal telemetry (logs, metrics, traces, authentication) into graph representations for dynamic Zero-Trust policy enforcement with temporal trust scoring.
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

Securing cloud microservices requires understanding how services behave, authenticate, and interact in real time, but existing methods analyze telemetry signals in isolation rather than jointly. Traditional security approaches fail to capture the complex dependencies and behavioral patterns that emerge across distributed service interactions. The challenge is to perform continuous verification and dynamic policy enforcement based on a unified view of system state that incorporates multiple telemetry modalities simultaneously. Current Zero-Trust implementations lack the ability to propagate risk information across service dependencies and adapt policies in real time based on evolving trust levels. The problem demands a framework that can detect anomalies, compute trust scores with temporal decay, and enforce access policies dynamically while maintaining low operational overhead in production microservice environments.

## Method summary

The framework represents microservices as a heterogeneous graph where nodes encode services and edges capture dependencies, with multi-modal telemetry embedded directly into the graph structure. Logs, metrics, traces, and authentication flows are processed and embedded into node and edge features rather than analyzed separately. A Graph Neural Network architecture with attention mechanisms propagates information across the service dependency graph to capture risk propagation patterns. The GNN performs joint anomaly detection and trust computation, generating dynamic trust scores for each service interaction. Trust scores incorporate temporal decay to reflect the continuous verification principle of Zero-Trust architectures. The computed trust signals feed directly into a policy enforcement engine that can deny or restrict suspicious interactions in real time. The attention mechanism allows the model to weigh different types of telemetry and service relationships according to their relevance for security decisions.

## Ground truth and evaluation

The method is evaluated on three microservice benchmarks: TrainTicket, Sock Shop, and DeathStarBench. Ground truth appears to be derived from injected anomalies or attack scenarios in these benchmark systems, though the paper does not explicitly detail the labeling process. Performance metrics include accuracy (97.2% on TrainTicket), recall (98.1%), and AUC (0.987), with consistent results across all three datasets. Latency overhead is measured at below 3.2 milliseconds, demonstrating real-time feasibility. Robustness testing evaluates performance under degraded conditions including noisy logs, delayed traces, and authentication failures, with accuracy remaining above 95.8%. Ablation studies isolate the contribution of different telemetry modalities, and SHAP analysis identifies which features most influence trust scoring decisions. The evaluation demonstrates that authentication data and the combination of multiple modalities are critical for accurate detection.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the experimental setup is confined to three specific benchmark microservice applications, which may not capture the full diversity of production cloud-native systems. The robustness tests examine specific degradation scenarios (noisy logs, delayed traces, authentication failures) but do not explore all possible failure modes or adversarial attacks. The 3.2 millisecond latency overhead, while low, is measured in controlled benchmark environments and may vary in larger-scale production deployments. The reliance on labeled anomaly data for training suggests potential challenges in generalizing to novel attack patterns not represented in the training set. The temporal decay mechanism for trust scores uses parameters that may require tuning for different operational contexts.

## Gaps this paper opens

The framework focuses on anomaly detection and policy enforcement but does not address root cause analysis or remediation of detected security issues. While the heterogeneous graph captures service dependencies and the GNN propagates risk information, the paper does not explore how to trace anomalies back to their originating causes or identify the specific failure points in the dependency chain. The temporal aspects of trust scoring use decay functions but do not model the temporal propagation of failures or security breaches through the service graph over time. The SHAP analysis identifies important features but does not provide interpretable explanations of why specific services or interactions are flagged as suspicious. The integration of authentication flows is valuable but the paper does not examine how to distinguish between legitimate behavioral changes and actual security threats. The policy enforcement mechanism operates reactively based on trust scores but does not incorporate predictive capabilities to anticipate cascading failures or security incidents.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses service dependency analysis and temporal aspects in cloud-native systems, but focuses on security rather than root cause analysis. The heterogeneous graph representation of microservices with embedded telemetry provides a relevant architectural pattern for modeling service dependencies that could be adapted for RCA purposes. The attention-based GNN mechanism for propagating information across the dependency graph offers techniques applicable to tracing failure propagation in temporal causal analysis. However, the primary goal of Zero-Trust policy enforcement differs fundamentally from identifying root causes of incidents. The temporal decay mechanism for trust scores represents a simplified approach to temporal dynamics compared to the temporal failure propagation analysis needed for RCA. The multi-modal telemetry integration demonstrates the value of combining logs, metrics, traces, and authentication data, which aligns with observability data analysis requirements for comprehensive root cause investigation. The framework's ability to operate in real time with low latency suggests architectural patterns that could support online RCA systems.
