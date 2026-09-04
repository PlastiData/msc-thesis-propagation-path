---
paper_id: 174
title: "Causality-enhanced system reliability and safety analysis: An overview"
authors:
  - Shuwen Zheng
  - Kai Pan
  - Yunxia Chen
  - Jie Liu
  - Enrico Zio
year: 2025
venue: Reliability Engineering & System Safety
doi: 10.1016/j.ress.2025.112109
arxiv_id: ""
url: "https://openalex.org/W7115704270"
pdf_path: data/pdfs/paper_174.pdf
read_date: 2026-05-11

category:
  - temporal_causal_analysis
  - root_cause_analysis
  - benchmark_and_evaluation

method:
  family: other
  specific: survey and taxonomy of causality methods in reliability engineering
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
  primary_contribution: A comprehensive survey and taxonomy of causality-based methods for system reliability and safety analysis across multiple application domains.
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

Traditional reliability and safety analysis methods often struggle to identify true causal relationships underlying system failures, relying instead on correlational or statistical associations that may not reflect actual cause-and-effect mechanisms. This limitation becomes particularly problematic in complex engineered systems where multiple interacting components and failure modes create intricate dependency structures. The field lacks a unified framework for understanding how different causality-based approaches can be applied to reliability engineering problems. Existing methods range from classical fault tree analysis to modern machine learning techniques, but their relationships, strengths, and appropriate application contexts remain unclear. The challenge is compounded by the diversity of system types, from mechanical systems to cyber-physical infrastructures, each requiring different analytical approaches while sharing common needs for causal understanding.

## Method summary

This paper provides a systematic survey and taxonomy of causality-enhanced methods in reliability and safety analysis rather than proposing a single new method. The authors organize existing approaches into several categories including graphical causal models such as Bayesian networks and fault trees, causal inference methods from observational data, and physics-informed causal modeling. The survey covers classical reliability engineering techniques like failure mode and effects analysis, fault tree analysis, and event tree analysis, examining how these inherently encode causal assumptions. It also discusses modern data-driven approaches including Granger causality, transfer entropy, and convergent cross-mapping for identifying causal relationships from time series data. The taxonomy distinguishes between knowledge-driven methods that rely on domain expertise and data-driven methods that extract causal structures from observations. The paper further examines how causality principles enhance specific reliability tasks including fault diagnosis, remaining useful life prediction, and risk assessment across various domains such as manufacturing systems, power grids, and transportation networks.

## Ground truth and evaluation

This survey paper does not present original empirical evaluations or ground truth datasets. Instead, it synthesizes evaluation approaches reported across the reviewed literature. The paper discusses how different causality methods are validated in their respective application domains, noting that evaluation strategies vary significantly by method type and application context. Knowledge-driven approaches like fault trees are typically validated through expert review and comparison with historical failure data. Data-driven causal discovery methods are evaluated using synthetic datasets with known causal structures, cross-validation on real system data, or comparison against domain expert knowledge. The survey highlights that many causality-based reliability methods are assessed through case studies on specific industrial systems, measuring performance through metrics like diagnostic accuracy, prediction error for remaining useful life, or risk assessment precision. The paper notes a general lack of standardized benchmarks for comparing causality methods in reliability engineering, with evaluation often being application-specific and difficult to generalize across domains.

## Stated limitations

The paper acknowledges several limitations in the current state of causality-enhanced reliability analysis. Many existing methods face challenges in scaling to large complex systems with numerous interacting components and failure modes. Data-driven causal discovery approaches require substantial amounts of high-quality observational data, which may not be available for rare failure events or newly deployed systems. The integration of domain knowledge with data-driven methods remains an open challenge, as purely knowledge-driven approaches may miss emergent causal relationships while purely data-driven methods may identify spurious correlations. The paper notes that most causality methods assume stationarity or slowly-varying system dynamics, which may not hold for systems undergoing significant operational changes or degradation. Computational complexity presents practical barriers for real-time applications, particularly for methods requiring extensive simulation or optimization. The survey also highlights that validation and verification of causal models remains difficult, especially for systems where controlled experiments are infeasible or unethical.

## Gaps this paper opens

The survey identifies several important research gaps in causality-enhanced reliability analysis. There is a need for unified frameworks that can systematically combine knowledge-driven and data-driven approaches to leverage both domain expertise and observational evidence. Methods for handling non-stationary systems and time-varying causal relationships require further development, particularly for systems experiencing degradation or operational regime changes. The paper points to insufficient research on causal analysis in cyber-physical systems and cloud-native architectures where software and hardware failures interact in complex ways. Standardized benchmarks and evaluation protocols for comparing different causality methods across reliability engineering applications are largely absent. The integration of uncertainty quantification with causal analysis needs deeper investigation, as reliability decisions require understanding both causal relationships and confidence in those relationships. Finally, the survey highlights limited work on real-time causal inference for online fault diagnosis and predictive maintenance, where computational efficiency and rapid adaptation to new evidence are critical.

## Relevance to the thesis topic

This survey paper is adjacent to the thesis topic on root cause analysis in cloud-native systems using temporal and dependency analysis. While the paper covers causality-based methods broadly across reliability engineering domains, many of the fundamental concepts directly apply to cloud-native RCA. The discussion of temporal causal analysis methods, including Granger causality and transfer entropy, provides theoretical foundations relevant to analyzing time-series observability data in distributed systems. The taxonomy of causal discovery approaches offers a framework for positioning cloud-native RCA methods within the broader landscape of causality-based diagnosis. However, the paper focuses primarily on traditional engineered systems like manufacturing equipment, power grids, and mechanical systems rather than software-intensive distributed architectures. The challenges identified around scaling causal analysis to complex systems with many interacting components parallel the challenges in cloud-native environments with numerous microservices. The gap identified regarding cyber-physical systems and the integration of software-hardware failure modes suggests that cloud-native RCA represents an underexplored application domain for causality-enhanced reliability analysis, strengthening the motivation for thesis work in this area.
