---
paper_id: 333
title: Machine Learning-Based Network Status Detection and Fault Localization
authors:
  - Ayşe Rumeysa Mohammed
  - S. Mohammed
  - David Côté
  - S. Shirmohammadi
year: 2021
venue: IEEE Transactions on Instrumentation and Measurement
doi: 10.1109/TIM.2021.3094223
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/9e0195a29ecdc0d27fa59ae407758d8d6f2f0079"
pdf_path: data/pdfs/paper_333.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - root_cause_analysis
  - observability_data_analysis

method:
  family: classical_ml
  specific: gradient boosting and extreme gradient boosting decision trees
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
  primary_contribution: A machine learning method using decision trees and gradient boosting variants to classify network status into three categories (normal, congestion, fault) and localize faults, achieving 99% accuracy on emulated network data.
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

Network operators face significant challenges in detecting and localizing faults because these tasks remain largely manual processes in contemporary networks. Existing approaches can at best distinguish between faulty and non-faulty network states, providing limited granularity for understanding network problems. The lack of automated methods for network status detection and fault localization creates operational inefficiencies and delays in problem resolution. There is a need for more sophisticated classification that can distinguish between different types of network degradation, such as congestion versus actual faults, to enable more targeted remediation actions.

## Method summary

The proposed approach employs three classical machine learning algorithms: decision trees, gradient boosting, and extreme gradient boosting. These algorithms process network telemetry data to classify network status into three distinct categories: normal operation, congestion, and network fault. The method extends beyond binary classification by providing this three-way distinction, allowing operators to differentiate between performance degradation due to congestion versus actual infrastructure failures. After detecting the network status, the system performs fault localization to identify the specific location of problems within the network. The gradient boosting variants are ensemble methods that combine multiple weak learners to create a stronger predictive model, making them suitable for handling the complexity of network telemetry data.

## Ground truth and evaluation

The ground truth for this work was obtained through an emulated network environment where the researchers could control and label network conditions. The emulation setup allowed them to generate labeled datasets with known normal states, congestion scenarios, and fault conditions. The evaluation focused on classification accuracy, with the proposed methods achieving up to 99% accuracy in distinguishing between the three network states. The controlled emulation environment provided clear ground truth labels since the researchers explicitly introduced congestion and faults at known times and locations. However, the paper does not provide extensive details about the specific metrics used for evaluating fault localization accuracy or the complexity of the emulated network topology.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed approach. The reliance on emulated network data rather than real production network traces represents an implicit limitation, as emulated environments may not capture the full complexity and variability of operational networks. The paper does not discuss how the method would scale to large-scale networks or how it would handle previously unseen fault types. There is no discussion of the computational overhead required for real-time classification or the latency between fault occurrence and detection. The generalizability of models trained on emulated data to real-world production environments remains unaddressed.

## Gaps this paper opens

The work leaves several questions unanswered regarding practical deployment in production environments. The transition from emulated to real-world network data requires investigation, particularly regarding whether models trained on synthetic data can generalize to operational networks with their inherent noise and complexity. The paper does not address temporal aspects of fault propagation or how faults evolve over time in distributed systems. There is no consideration of service dependencies or how faults in one network component might cascade to affect other services. The method treats network status classification as an isolated problem without considering the broader context of cloud-native systems where network issues interact with application-layer problems. The interpretability of the machine learning models and how operators would use the classification results for remediation remains unexplored.

## Relevance to the thesis topic

This work is adjacent to the thesis topic as it addresses fault detection and localization in networks using machine learning, but it focuses on traditional network infrastructure rather than cloud-native systems. The three-way classification approach (normal, congestion, fault) provides more granularity than binary classification, which aligns with the thesis goal of understanding different types of system degradation. However, the paper does not incorporate temporal analysis of how faults propagate over time or dependency analysis between services, which are central to the thesis framework. The use of classical machine learning methods rather than temporal causal analysis or dependency-aware approaches represents a different methodological direction. The work could inform the thesis by demonstrating the value of multi-class status classification, but the lack of service-level context and temporal propagation analysis limits its direct applicability to cloud-native root cause analysis.
