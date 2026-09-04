---
paper_id: 213
title: Automated Cause Analysis of Latency Outliers Using System-Level Dependency Graphs
authors:
  - Sneh Patel
  - Brendan Park
  - Naser Ezzati-Jivan
  - Quentin Fournier
year: 2021
venue: International Conference on Software Quality, Reliability and Security
doi: 10.1109/QRS54544.2021.00054
arxiv_id: 2207.06515
url: "https://www.semanticscholar.org/paper/c95ba48a0bcba0ec426b000263582107842646be"
pdf_path: data/pdfs/paper_213.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - service_dependency_topology
  - root_cause_analysis

method:
  family: hybrid
  specific: DBSCAN clustering with Z-score statistical analysis on dependency graphs
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
  primary_contribution: An automated method for detecting latency outliers in system traces using dependency graphs combined with density-based clustering and statistical analysis to identify root causes.
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

Performance issues in runtime systems are difficult to detect and diagnose manually. Developers traditionally rely on logging and tracing methods to identify bottlenecks, but these approaches require significant manual effort and time investment. When systems generate large volumes of traces with each trace containing numerous requests, manually analyzing dependency graphs to identify performance anomalies becomes impractical. The challenge is compounded by the need to distinguish between normal latency variations and genuine outliers that indicate underlying problems. There is a need for automated methods that can process system-level traces at scale, detect latency outliers, and pinpoint their root causes without requiring extensive manual intervention from developers.

## Method summary

The proposed method constructs dependency graphs from system-level traces to represent internal interactions between threads and system resources. Each request generates a dependency graph that captures the execution flow and resource dependencies. To automate outlier detection across large datasets of these graphs, the method employs density-based machine learning models, specifically DBSCAN clustering, combined with statistical calculations using Z-score. The dependency graphs serve as the foundation for comparison between normal and outlier traces. By analyzing the structural differences in dependency graphs between normal requests and detected outliers, the method identifies where performance issues occur in the system. The approach is designed to work in production environments where traces contain numerous requests and manual analysis would be prohibitive.

## Ground truth and evaluation

The evaluation demonstrates accuracy greater than 97 percent on outlier detection tasks. The paper claims this level of accuracy makes the method suitable for deployment on in-production servers and industry-level use cases. The evaluation focuses on the accuracy of detecting outliers rather than on validating the correctness of root cause identification. The ground truth for outlier detection appears to be established through the combination of density-based clustering results and statistical thresholds, though the paper does not explicitly describe how ground truth labels were obtained or validated. The high accuracy metric suggests the method can reliably distinguish between normal latency patterns and outlier requests in the evaluated datasets.

## Stated limitations

The paper does not explicitly state limitations of the proposed method. There is no discussion of scenarios where the dependency graph approach might fail or where the density-based clustering might produce false positives or false negatives. The paper does not address computational overhead of constructing and analyzing dependency graphs for every request in high-throughput production systems. There is no mention of how the method handles evolving system behaviors or concept drift where normal patterns change over time. The scalability limits of the approach when dealing with extremely large or complex dependency graphs are not discussed.

## Gaps this paper opens

The paper does not provide details on how root causes are actually extracted from the dependency graph comparisons beyond identifying where issues occur. The transition from detecting an outlier to providing actionable root cause information remains underspecified. There is no discussion of how the method handles multiple concurrent root causes or cascading failures where one issue triggers others. The paper does not address temporal aspects of how failures propagate through the dependency graph over time. The relationship between structural differences in dependency graphs and specific types of performance problems is not explored. There is no evaluation of whether the identified root causes are accurate or actionable from a developer perspective, only that outliers are detected with high accuracy.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in distributed systems using dependency analysis. The use of dependency graphs to represent system interactions aligns with the thesis focus on service dependency topology. The automated detection of latency outliers provides a foundation for understanding when root cause analysis is needed. However, the paper's approach to temporal analysis is limited, focusing primarily on structural graph comparison rather than temporal propagation patterns. The method provides a starting point for understanding how dependency information can be leveraged for RCA, though it lacks the temporal causal analysis component central to the thesis. The work is particularly relevant for understanding how to construct and utilize dependency graphs in cloud-native systems, which is a key component of the proposed framework.
