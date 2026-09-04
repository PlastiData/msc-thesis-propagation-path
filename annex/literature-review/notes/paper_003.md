---
paper_id: 003
title: Evidence-Based Analysis of Cyber Attacks to Security Monitored Distributed Energy Resources
authors:
  - Davide Cerotti
  - Daniele Codetta‐Raiteri
  - Giovanna Dondossola
  - Lavinia Egidi
  - G. Franceschinis
  - Luigi Portinale
  - Roberta Terruggia
year: 2020
venue: Applied Sciences
doi: 10.3390/app10144725
arxiv_id: ""
url: "https://openalex.org/W3041076789"
pdf_path: data/pdfs/paper_003.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - temporal_causal_analysis
  - observability_data_analysis

method:
  family: classical_ml
  specific: dynamic Bayesian networks
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
  primary_contribution: A dynamic Bayesian network approach for cybersecurity analysis of distributed energy resources that captures causal and temporal dependencies between security events in both IT and operational technology environments.
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

The paper addresses cybersecurity analysis challenges in distributed energy resources that employ network-based controllers. These systems integrate both information technology and operational technology environments, creating complex attack surfaces where cyber threats can propagate across different layers of the infrastructure. The authors identify a need for analytical methods that can capture both causal relationships and temporal dependencies when assessing security threats in these critical energy infrastructures. Traditional security monitoring approaches lack the capability to perform time-driven predictive and diagnostic analyses that account for how attacks evolve over time and propagate through system dependencies. The problem is further complicated by the need to integrate evidence from multiple sources including security monitoring systems and operational data from the energy plants themselves.

## Method summary

The approach employs dynamic Bayesian networks to model the cybersecurity posture of distributed energy plants with network-based controllers. The system model incorporates real-world context information from both the information technology layer and the operational technology layer of the energy infrastructure. Dynamic Bayesian networks are chosen specifically for their ability to represent temporal evolution of system states and causal dependencies between security events. The model supports both predictive analysis, where future security states can be forecasted based on current evidence, and diagnostic analysis, where the root causes of observed security incidents can be inferred by reasoning backwards through the causal structure. The methodology integrates security evidence collected from monitoring platforms deployed across the digital energy infrastructure. The Bayesian framework allows for probabilistic reasoning under uncertainty, which is essential given the incomplete and noisy nature of security monitoring data in operational environments.

## Ground truth and evaluation

The paper does not provide explicit details about ground truth data sources or comprehensive empirical evaluation metrics. The approach is demonstrated using real-world context information from distributed energy plants, suggesting that actual operational data was used to populate and validate the models. However, the paper does not describe a systematic evaluation against labeled datasets of known attacks or comparison with baseline methods. The validation appears to focus on demonstrating the feasibility and utility of the approach through case studies rather than quantitative performance metrics. The authors emphasize the value of security evidence for analysis but do not specify how the accuracy of predictions or diagnoses was measured. The evaluation methodology centers on showing that the dynamic Bayesian network can effectively represent and reason about the temporal and causal aspects of security threats in the specific domain of distributed energy resources.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed approach. There is no discussion of computational complexity constraints when scaling the dynamic Bayesian network models to larger distributed energy infrastructures. The authors do not address challenges related to obtaining sufficient training data for learning the probabilistic parameters of the Bayesian networks. No mention is made of potential difficulties in maintaining and updating the models as the infrastructure evolves or as new types of attacks emerge. The paper lacks discussion of false positive or false negative rates that might arise from the probabilistic inference process. There is no acknowledgment of limitations in the temporal resolution of the analysis or constraints on how far into the future predictions can reliably extend. The scope of applicability beyond distributed energy resources to other critical infrastructure domains is not discussed.

## Gaps this paper opens

The work raises questions about how to systematically construct dynamic Bayesian network models for complex distributed systems without requiring extensive domain expertise in both cybersecurity and probabilistic modeling. The paper does not address how to automatically learn the causal structure and temporal dependencies from observational data rather than relying on manual model construction. There is an open question about integrating this approach with modern cloud-native architectures where services are more dynamic and ephemeral compared to traditional energy infrastructure. The methodology does not specify how to handle the scale and velocity of monitoring data in large distributed systems where thousands of events occur per second. The paper leaves unexplored how to combine this probabilistic reasoning approach with other root cause analysis techniques such as trace analysis or dependency graph mining. There is no discussion of how to validate that the causal relationships encoded in the Bayesian network accurately reflect the actual attack propagation patterns in the system.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic as it addresses temporal and causal analysis for security monitoring in distributed systems, though not specifically cloud-native environments. The use of dynamic Bayesian networks to capture temporal dependencies between security events aligns with the thesis emphasis on temporal analysis for root cause determination. The approach of integrating evidence from multiple monitoring sources parallels the observability data analysis required in cloud-native systems. However, the domain focus on distributed energy resources with relatively static network-based controllers differs significantly from the dynamic, microservices-based architecture of cloud-native systems. The causal modeling aspect is relevant to understanding how failures and attacks propagate through system dependencies, which is central to root cause analysis. The methodology provides insights into how temporal evolution can be incorporated into diagnostic reasoning, though the specific technique of Bayesian networks may be less suitable for the high-velocity, high-cardinality data typical of cloud environments. The paper demonstrates the value of combining temporal and dependency information for security analysis, which is a key principle applicable to the thesis work.
