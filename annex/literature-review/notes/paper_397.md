---
paper_id: 397
title: Robust Multimodal Failure Detection for Microservice Systems
authors:
  - Chenyu Zhao
  - Minghua Ma
  - Zhenyu Zhong
  - Shenglin Zhang
  - Zhiyuan Tan
  - Xiao Xiong
  - LuLu Yu
  - Jiayi Feng
  - Yongqian Sun
  - Yuzhi Zhang
  - Dan Pei
  - Qingwei Lin
  - Dongmei Zhang
year: 2023
venue: arXiv
doi: ""
arxiv_id: 2305.18985
url: "http://arxiv.org/abs/2305.18985v1"
pdf_path: data/pdfs/paper_397.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - observability_data_analysis
  - distributed_system_monitoring

method:
  family: deep_learning
  specific: Graph Transformer Network with GAT-GRU fusion
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
  primary_contribution: An unsupervised multimodal failure detection approach that fuses metrics, logs, and traces using graph neural networks to detect instance failures in microservice systems.
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

Microservice systems face critical challenges in proactive failure detection because instance failures can propagate throughout the system and cause widespread performance degradation. Existing approaches typically rely on single-modal data sources such as metrics, logs, or traces in isolation. These single-modal methods suffer from high false alarm rates and miss a substantial number of actual failures because they fail to capture the correlations that exist across different data modalities. The dynamic nature of microservice systems further complicates detection as the characteristics and relationships of multimodal data continuously change during system operation. There is a need for an approach that can effectively integrate heterogeneous multimodal observability data while adapting to the temporal dynamics of microservice environments.

## Method summary

AnoFusion employs a multi-stage deep learning architecture to fuse metrics, logs, and traces for unsupervised failure detection. The approach first uses a Graph Transformer Network to learn correlations among heterogeneous multimodal data by treating different data types as nodes in a graph structure. This allows the model to capture cross-modal relationships that would be missed by single-modal approaches. To handle the temporal dynamics of microservice systems, AnoFusion integrates a Graph Attention Network with Gated Recurrent Units. The GAT component learns spatial relationships among instances and services while the GRU component captures temporal patterns in the multimodal data streams. The combined architecture enables the system to adapt to changing patterns in the multimodal data over time. The method operates in an unsupervised manner, detecting anomalies without requiring labeled failure examples during training.

## Ground truth and evaluation

The paper evaluates AnoFusion on two datasets from real microservice systems. Ground truth for failure detection is established through labeled instances of actual system failures. The evaluation uses standard classification metrics including precision, recall, and F1-score to measure detection performance. AnoFusion achieves F1-scores of 0.857 and 0.922 on the two datasets respectively. The paper compares AnoFusion against state-of-the-art failure detection approaches to demonstrate performance improvements. The evaluation methodology focuses on the ability to correctly identify instance failures while minimizing false alarms. The paper demonstrates that the multimodal fusion approach outperforms single-modal baselines, validating the importance of cross-modal correlation learning for failure detection.

## Stated limitations

The paper does not explicitly enumerate limitations of the AnoFusion approach in a dedicated section. The abstract and methodology focus primarily on the contributions and performance achievements. Implicit limitations can be inferred from the problem formulation, such as the requirement for collecting and aligning multimodal data from different sources which may introduce operational complexity. The unsupervised nature of the approach means it may require careful tuning of anomaly thresholds to balance precision and recall in different deployment contexts. The computational overhead of running Graph Transformer Networks and GAT-GRU models in real-time production environments is not discussed in detail.

## Gaps this paper opens

The paper focuses exclusively on failure detection without addressing root cause analysis or the propagation paths of detected failures. While AnoFusion can identify that an instance has failed, it does not explain why the failure occurred or trace the causal chain of events leading to the failure. The temporal analysis is limited to pattern recognition rather than explicit causal reasoning about how failures propagate through service dependencies over time. The graph structures used for multimodal fusion do not appear to explicitly model service dependency topology or call graphs that would enable understanding of failure propagation. There is no discussion of how detected failures relate to specific root causes or how the multimodal signals could be decomposed to identify the originating fault. The approach also does not address remediation or provide actionable insights beyond binary failure classification.

## Relevance to the thesis topic

AnoFusion addresses the detection phase that precedes root cause analysis but does not perform causal analysis itself. The multimodal data fusion approach is relevant because effective RCA requires integrating signals from metrics, logs, and traces to understand system behavior. The use of graph neural networks to model relationships among instances provides a foundation that could be extended to model service dependencies explicitly for causal analysis. However, the paper's focus on anomaly detection rather than causality means it provides limited direct contribution to temporal and dependency-based RCA frameworks. The temporal modeling with GRU captures time-series patterns but does not perform the temporal causal reasoning needed to trace failure propagation paths. The work demonstrates the value of multimodal analysis in cloud-native systems but would need significant extension to support root cause identification through temporal and dependency analysis.
