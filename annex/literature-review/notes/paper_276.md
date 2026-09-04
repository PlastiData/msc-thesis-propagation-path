---
paper_id: 276
title: "Automated Detection of Network Card Bottlenecks in Apache Pulsar: An Enhanced Framework with Dynamic Thresholds and Root Cause Analysis"
authors:
  - Muhamed Ramees Cheriya Mukkolakkal
year: 2025
venue: International Journal of Scientific Research and Modern Technology
doi: 10.38124/ijsrmt.v4i1.1158
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/ac0062eec699e6d2a654e34f78503492388bddd0"
pdf_path: data/pdfs/paper_276.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - root_cause_analysis
  - observability_data_analysis

method:
  family: rule_based
  specific: dynamic threshold computation with configuration mismatch detection
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
  primary_contribution: A centralized monitoring framework for Apache Pulsar that pre-computes hardware-specific thresholds and performs automated root cause analysis for network card bottlenecks.
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

Apache Pulsar message queuing systems depend on robust hardware infrastructure monitoring to maintain performance levels required for production workloads. Traditional monitoring approaches rely on static threshold-based alerting that fails to accommodate variations in hardware capabilities, diverse workload characteristics, and transient performance issues. This limitation results in high false positive rates that burden operations teams and delayed incident response when actual performance degradation occurs. The existing monitoring architectures place the burden of analysis within alert rules themselves, creating complexity in operations and reducing the accuracy of detection. Network card bottlenecks specifically represent a critical failure mode in distributed messaging systems where throughput degradation can cascade across the entire cluster, yet detecting these bottlenecks requires understanding both hardware specifications and runtime behavior patterns.

## Method summary

The framework introduces a centralized analysis service that shifts intelligence away from distributed alert rules into a dedicated component responsible for threshold computation and root cause analysis. The service pre-computes optimal thresholds by analyzing hardware specifications for each node, including network interface card capabilities and system configurations. It continuously monitors network utilization metrics and compares observed performance against these dynamically computed thresholds rather than static values. When anomalies are detected, the system performs configuration mismatch detection by comparing actual hardware configurations against expected specifications for the deployment. The root cause analysis component examines multiple signals including network throughput, packet loss, interface errors, and system resource utilization to determine whether bottlenecks stem from hardware limitations, misconfigurations, or workload patterns. The framework emits actionable metrics and generates specific remediation recommendations based on the identified root cause, such as hardware upgrades, configuration adjustments, or workload rebalancing.

## Ground truth and evaluation

The framework was validated across production Apache Pulsar environments though the paper does not specify the exact number or scale of deployments tested. Evaluation metrics include detection accuracy of 96.3 percent, false positive rate of 1.4 percent, and a 61 percent reduction in mean time to resolution compared to baseline static threshold approaches. The ground truth for detection accuracy appears to be established through manual validation of alerts against actual performance incidents, though the specific labeling process is not detailed. The false positive rate was measured by tracking alerts that did not correspond to genuine performance degradation requiring intervention. Mean time to resolution was computed by measuring the duration from initial alert to problem remediation, comparing the enhanced framework against the previous static threshold system. The paper reports that the system automatically generates specific remediation recommendations, but does not provide quantitative evaluation of recommendation quality or accuracy.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed framework. No discussion is provided regarding scenarios where dynamic threshold computation might fail or produce suboptimal results. The scope is limited to network card bottlenecks in Apache Pulsar specifically, without addressing whether the approach generalizes to other hardware components or distributed systems. The evaluation does not report on computational overhead introduced by the centralized analysis service or potential scalability constraints as cluster size increases. There is no analysis of failure modes where the framework might miss genuine bottlenecks or incorrectly attribute root causes. The paper does not discuss limitations in the root cause analysis component's ability to distinguish between correlated causes or handle complex multi-factor performance degradation scenarios.

## Gaps this paper opens

The framework focuses exclusively on network card bottlenecks without addressing how similar dynamic threshold and root cause analysis approaches could extend to other infrastructure components like CPU, memory, or storage subsystems. The centralized architecture raises questions about fault tolerance and what happens when the analysis service itself becomes unavailable or experiences performance issues. The root cause analysis appears rule-based without learning from historical incident patterns, suggesting opportunities for incorporating machine learning to improve diagnosis accuracy over time. The evaluation provides aggregate metrics but does not examine performance across different workload types, cluster configurations, or failure scenarios, leaving uncertainty about robustness. The remediation recommendations are generated but not evaluated for correctness or completeness, creating a gap in understanding whether operators can reliably act on the system's guidance. The approach does not address temporal dependencies or cascading failures where network bottlenecks in one component trigger performance issues elsewhere in the distributed system.

## Relevance to the thesis topic

This paper addresses root cause analysis in a cloud-native distributed system, specifically Apache Pulsar, making it adjacent to the thesis topic. The framework performs root cause analysis by examining configuration mismatches and correlating multiple performance signals to identify the source of network bottlenecks. However, the approach lacks temporal analysis of how failures propagate through the system over time or dependency analysis of how components interact within the service topology. The method is rule-based rather than leveraging temporal patterns or service dependencies that would be central to a comprehensive root cause analysis framework. The centralized analysis architecture provides a useful architectural pattern for how RCA logic can be organized separately from monitoring infrastructure. The dynamic threshold computation addresses one aspect of adapting to system characteristics, though it does not incorporate historical temporal patterns or dependency relationships. The paper demonstrates practical value in production environments but represents a narrower scope than the thesis topic's emphasis on temporal and dependency-based analysis across cloud-native systems generally.
