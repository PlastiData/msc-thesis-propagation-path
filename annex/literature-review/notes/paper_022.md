---
paper_id: 022
title: Spatiotemporal Traffic Prediction in Distributed Backend Systems via Graph Neural Networks
authors:
  - Zhimin Qiu
  - Feng Liu
  - Yuxiao Wang
  - Chenrui Hu
  - Ziyu Cheng
  - Di Wu
year: 2025
venue: 2025 6th International Conference on Information Science, Parallel and Distributed Systems (ISPDS)
doi: 10.1109/ISPDS67367.2025.11390994
arxiv_id: 2510.15215
url: "https://www.semanticscholar.org/paper/2a347b12586351b0a66cb5156390be068938107b"
pdf_path: data/pdfs/paper_022.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - temporal_causal_analysis
  - service_dependency_topology

method:
  family: deep_learning
  specific: graph convolutional network with gated recurrent units
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
  primary_contribution: A spatiotemporal graph neural network approach that combines graph convolution for capturing service dependencies with gated recurrent structures for modeling temporal traffic patterns in distributed backend systems.
  novelty_strength: incremental

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

Traffic prediction in distributed backend systems faces challenges in capturing complex dependencies between services and dynamic temporal patterns simultaneously. Traditional time series models treat services independently and fail to account for the intricate interaction patterns that characterize microservice architectures. The problem requires modeling both the spatial structure of service dependencies and the temporal evolution of traffic patterns. Distributed systems exhibit non-linear relationships where traffic changes in one service propagate through dependent services in ways that simple statistical models cannot capture. The goal is to predict future traffic volumes across all services in the system with sufficient accuracy to enable proactive resource management and anomaly detection.

## Method summary

The approach abstracts the distributed system as a graph where nodes represent services and edges represent interactions or dependencies between services. Node features encode current traffic volumes and resource utilization states. A graph convolutional mechanism performs multi-order propagation and aggregation of node features to capture spatial dependencies across the service topology. This allows information from neighboring services to influence each node's representation based on the strength and structure of their connections. A gated recurrent unit structure processes historical traffic sequences to model temporal dynamics and capture patterns over time. The spatiotemporal joint modeling module fuses the graph-based spatial representations with the temporal dependency information extracted by the recurrent component. A decoder network then generates predictions for future traffic values across all nodes in the system. The model is trained end-to-end using mean squared error loss to minimize prediction deviations from observed traffic values.

## Ground truth and evaluation

The ground truth consists of actual traffic measurements extracted from public distributed system logs. These logs provide historical traffic volumes and service interaction patterns that serve as training data and evaluation targets. The evaluation uses four standard regression metrics: mean squared error, root mean squared error, mean absolute error, and mean absolute percentage error. The proposed method is compared against mainstream baseline approaches across different prediction horizons to assess short-term and long-term forecasting accuracy. Experiments also examine model performance at different network depths to understand how multi-hop information propagation affects prediction quality. The evaluation demonstrates that the proposed method achieves lower error rates and more stable performance compared to baselines across various experimental configurations.

## Stated limitations

The paper does not explicitly state limitations of the proposed approach. No discussion is provided regarding computational complexity or scalability constraints when applying the method to very large distributed systems with thousands of services. The paper does not address how the model handles dynamic topology changes when services are added or removed from the system. There is no analysis of failure modes or scenarios where the graph neural network approach might underperform. The generalizability of the approach across different types of distributed systems or application domains is not discussed. The paper does not examine the interpretability of the learned representations or how operators might understand which service dependencies drive specific predictions.

## Gaps this paper opens

The focus on traffic prediction rather than anomaly detection or root cause analysis leaves open questions about how predicted traffic patterns could be used for fault diagnosis. The paper does not explore how prediction errors or deviations from expected traffic could signal emerging problems or propagating failures in the system. There is no investigation of causal relationships between services beyond correlation patterns captured by the graph structure. The temporal modeling captures sequential patterns but does not explicitly reason about cause-and-effect relationships or failure propagation delays. The integration of this predictive capability with diagnostic or remediation systems remains unexplored. The paper does not address how prediction uncertainty could be quantified or used to trigger alerts when confidence is low.

## Relevance to the thesis topic

This work is adjacent to the thesis topic as it addresses temporal analysis and service dependency modeling in distributed systems but focuses on prediction rather than root cause analysis. The graph-based representation of service dependencies aligns with the thesis requirement for topology analysis, demonstrating how graph neural networks can capture complex interaction patterns. The temporal modeling component using gated recurrent units shows one approach to handling time-series data in distributed systems, which relates to temporal analysis needs in RCA. However, the paper's goal of forecasting future traffic differs fundamentally from diagnosing past failures or identifying root causes. The spatiotemporal modeling framework could potentially be adapted for RCA by analyzing prediction residuals or anomalous deviations, but this connection is not developed. The work provides relevant background on graph-based system representation and temporal feature extraction that could inform RCA approaches, but does not directly address the causal inference or diagnostic reasoning central to root cause analysis.
