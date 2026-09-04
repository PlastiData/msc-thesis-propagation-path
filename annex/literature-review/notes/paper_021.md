---
paper_id: 021
title: Distributed Temporal Graph Learning with Provenance for APT Detection in Supply Chains
authors:
  - Zhuoran Tan
  - Christos Anagnostopoulos
  - Jeremy Singer
year: 2025
venue: International Conference on Distributed Computing Systems Workshops
doi: 10.1109/ICDCSW63273.2025.00071
arxiv_id: 2504.02313
url: "https://www.semanticscholar.org/paper/25ab1b755b08a83e17992e03fd4058d156908e20"
pdf_path: data/pdfs/paper_021.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - temporal_causal_analysis
  - distributed_system_monitoring

method:
  family: deep_learning
  specific: temporal graph neural network
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
  primary_contribution: A temporal graph learning approach that integrates multi-source runtime data into dynamic provenance graphs for real-time APT detection in supply chains.
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

Supply chains in modern ICT systems have become increasingly complex with growing inter-dependencies across digital assets, software, and hardware components. This complexity creates numerous attack vectors that advanced persistent threats exploit, particularly through supply chain vulnerabilities that provide inherent stealth advantages to attackers. Existing defense mechanisms focus predominantly on prevention through blockchain-based integrity assurance or detection via static source code analysis in open-source software. These approaches fail in scenarios where source code is unavailable and cannot provide runtime detection and defense capabilities. The research addresses the gap in real-time detection of APT behavior during system operation when traditional static analysis methods are insufficient.

## Method summary

The approach integrates multi-source data to construct comprehensive dynamic provenance graphs that capture system behavior and dependencies over time. These provenance graphs represent entities such as processes, files, and network connections along with their temporal interactions and relationships. Temporal graph learning techniques are applied to these dynamic graphs to identify patterns indicative of APT behavior in real time. The method operates during runtime rather than relying solely on pre-deployment static analysis, enabling detection of attacks as they unfold. The distributed nature of the approach allows it to handle the scale and complexity of modern supply chain environments where components are geographically dispersed and interconnected.

## Ground truth and evaluation

The paper identifies a significant gap in available datasets, noting that neither industry nor academia provides tailored datasets for supply chain APT detection. To address this limitation, the authors propose simulating a custom dataset by replaying real-world supply chain exploits while collecting multi-source monitoring data. This simulation-based approach aims to generate labeled data that captures the temporal dynamics and provenance information necessary for training and evaluating the temporal graph learning models. The evaluation methodology relies on recreating known attack scenarios rather than using production system data or existing benchmark datasets. The specific metrics and validation procedures for assessing detection performance are not detailed in the abstract.

## Stated limitations

The paper explicitly acknowledges the absence of suitable datasets in both industry and academic contexts for evaluating APT detection in supply chains. This limitation necessitates the creation of synthetic datasets through simulation and replay of known exploits. The reliance on simulated data rather than real-world production traces introduces questions about how well the approach generalizes to novel attack patterns not represented in the replay scenarios. The paper does not discuss computational overhead or scalability constraints associated with maintaining and analyzing dynamic provenance graphs in large-scale distributed supply chain environments. Performance characteristics such as detection latency and false positive rates are not addressed in the available content.

## Gaps this paper opens

The work highlights the fundamental challenge of obtaining realistic training and evaluation data for supply chain security research, suggesting that data scarcity remains a critical barrier to advancing detection capabilities. The focus on temporal graph learning for provenance analysis raises questions about how to effectively capture and represent complex multi-hop attack chains that span multiple supply chain tiers and time scales. The paper does not address how to distinguish between legitimate complex workflows and malicious APT behavior in supply chains where both may exhibit similar temporal patterns. Integration challenges between different monitoring sources and the completeness of provenance capture in heterogeneous supply chain environments remain unexplored. The approach does not discuss how to handle concept drift as attack techniques evolve or how to update models without complete retraining.

## Relevance to the thesis topic

This work is adjacent to the thesis topic as it addresses temporal analysis and dependency relationships in distributed systems, though in a security context rather than root cause analysis for operational failures. The construction of dynamic provenance graphs parallels the dependency topology analysis needed for RCA, as both require tracking causal relationships between system components over time. The temporal graph learning techniques could potentially be adapted for analyzing failure propagation patterns in cloud-native systems. However, the focus on APT detection differs fundamentally from diagnosing performance issues or service failures. The multi-source data integration approach and handling of temporal dependencies provide relevant methodological insights, but the security-oriented threat detection objectives diverge from operational troubleshooting goals central to the thesis.
