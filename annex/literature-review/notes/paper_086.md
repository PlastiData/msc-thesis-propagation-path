---
paper_id: 086
title: Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark
authors:
  - Fang
  - Aoyang
  - Songhan Zhang
  - Yifan Yang
  - Hao Wu
  - Jingxian Xu
  - Xuyang Wang
  - Rui Wang
  - Manyi Wang
  - Q. W. Lu
  - Pei-Lun He
year: 2025
venue: arXiv (Cornell University)
doi: 10.48550/arxiv.2510.04711
arxiv_id: ""
url: "https://openalex.org/W4414972195"
pdf_path: data/pdfs/paper_086.pdf
read_date: 2026-05-11

category:
  - benchmark_and_evaluation
  - root_cause_analysis
  - distributed_system_monitoring

method:
  family: other
  specific: automated benchmark generation framework with fault injection and propagation validation
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
  primary_contribution: An automated framework for generating realistic microservice RCA benchmarks with complex fault propagation scenarios and hierarchical ground-truth labels validated against user-facing SLIs.
  novelty_strength: strong

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

Existing benchmarks for evaluating root cause analysis methods in microservice systems are oversimplified and fail to reflect real-world operational complexity. The authors demonstrate through preliminary experiments that simple rule-based methods can match or exceed state-of-the-art deep learning and machine learning models on four widely used public benchmarks, suggesting these benchmarks do not adequately challenge RCA methods. The oversimplification manifests in several dimensions including unrealistic fault injection strategies, overly simple call graph structures, and telemetry signal patterns that do not capture the complexity of actual production failures. This inadequacy leads to overestimation of model performance in academic settings while providing little guidance for practitioners deploying RCA solutions in real cloud-native environments. The lack of validated failure cases with measurable impact on user-facing service level indicators further disconnects benchmark evaluation from operational reality.

## Method summary

The authors develop an automated framework for generating comprehensive RCA benchmarks that address the limitations of existing datasets. The framework performs systematic fault injection across 25 fault types spanning 6 categories including resource exhaustion, network issues, application errors, configuration problems, dependency failures, and cascading failures. Each injected fault undergoes validation to ensure it produces a discernible impact on user-facing service level indicators, filtering out faults that do not manifest as observable failures. The framework captures complex fault propagation patterns by monitoring how failures cascade through service dependencies under dynamic workloads. Ground truth labels are provided at multiple hierarchical levels, mapping from affected services down to specific code-level root causes. The resulting dataset contains 1,430 validated failure cases derived from 9,152 total fault injections, ensuring each case represents a realistic operational scenario. The framework also captures rich telemetry data including metrics, traces, and logs to support evaluation of diverse RCA approaches.

## Ground truth and evaluation

Ground truth in this benchmark consists of hierarchical labels that identify root causes at multiple levels of granularity, from service-level identification down to specific code locations or configuration parameters responsible for failures. Each failure case is validated by confirming measurable degradation in user-facing service level indicators, ensuring the injected faults produce operationally relevant failures rather than silent or inconsequential errors. The authors re-evaluate 11 state-of-the-art RCA models on the new benchmark, measuring Top@1, Top@3, and Top@5 accuracy metrics. Results show dramatic performance degradation compared to existing benchmarks, with average Top@1 accuracy of 0.21 and the best model achieving only 0.37. Execution times also increase substantially from seconds to hours, revealing scalability challenges. The evaluation demonstrates that models performing well on simple benchmarks struggle with realistic fault propagation scenarios, validating the need for more challenging evaluation datasets. The hierarchical ground truth enables assessment of partial credit scenarios where models identify intermediate causes in propagation chains.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed benchmark framework. However, the methodology implicitly constrains the benchmark to fault types that can be systematically injected and validated through automated means. The requirement for measurable SLI impact may exclude certain classes of subtle or latent failures that accumulate over time. The framework generates failures in controlled testbed environments rather than capturing organic production failures, which may not fully represent the unpredictability and complexity of real-world incidents. The validation process filters out a substantial portion of injected faults, with only 1,430 cases validated from 9,152 injections, suggesting the framework may miss certain failure modes that are difficult to trigger or observe through automated means. The hierarchical ground truth relies on knowledge of the injection mechanism, which may not perfectly align with how human operators would diagnose and categorize root causes in practice.

## Gaps this paper opens

The dramatic performance gap revealed between existing benchmarks and the proposed benchmark raises questions about what specific characteristics make RCA problems genuinely difficult for automated methods. While the paper identifies fault propagation complexity as a key factor, it does not deeply analyze which propagation patterns prove most challenging or why certain model architectures fail on specific failure types. The hierarchical ground truth structure enables new research directions in partial credit evaluation and multi-level diagnosis, but the paper does not explore how models might be designed to exploit this hierarchical structure. The substantial increase in execution time from seconds to hours suggests scalability remains an open challenge, but the paper does not investigate algorithmic approaches specifically designed for computational efficiency in complex scenarios. The validation requirement for SLI impact creates opportunities to study the relationship between technical root causes and business impact, but this connection is not explored. The gap between the 9,152 injections and 1,430 validated cases suggests room for improved fault injection strategies that more reliably produce observable failures.

## Relevance to the thesis topic

This paper is directly relevant to the thesis topic as it addresses fundamental challenges in evaluating root cause analysis methods for cloud-native systems. The emphasis on fault propagation patterns aligns precisely with the thesis focus on temporal failure propagation and dependency analysis. The hierarchical ground truth structure that maps failures through service dependencies provides a concrete framework for validating temporal and dependency-aware RCA approaches. The benchmark's inclusion of dynamic workloads and complex propagation scenarios creates an evaluation environment that specifically tests the capabilities the thesis aims to develop. The finding that existing methods achieve only 0.21 average Top@1 accuracy establishes a clear performance baseline and demonstrates the need for improved approaches incorporating temporal and dependency information. The validation requirement for SLI impact ensures the benchmark focuses on operationally significant failures, which aligns with practical RCA objectives. The paper's systematic analysis of benchmark limitations provides methodological guidance for designing evaluation frameworks that properly assess temporal causal analysis and dependency topology methods.
