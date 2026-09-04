---
paper_id: 340
title: "Service mesh circuit breaker: From panic button to performance management tool"
authors:
  - Mohammad Reza Saleh Sedghpour
  - C. Klein
  - Johan Tordsson
year: 2021
venue: HAOC@EuroSys
doi: 10.1145/3447851.3458740
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/421ed0698ce96bc75e3f41258713bd7f294959b9"
pdf_path: data/pdfs/paper_340.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - recommendation_and_remediation

method:
  family: classical_ml
  specific: adaptive controller
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
  primary_contribution: An adaptive circuit breaking mechanism using a controller that dynamically adjusts circuit breaker thresholds to maintain tail response time below a given threshold while maximizing service throughput in service mesh environments.
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

Site Reliability Engineers face a fundamental tension between responding quickly to alerts to restore non-functional systems and avoiding alert fatigue from disruptive short response times. Circuit breaking in service meshes is a mechanism designed to handle overload by rejecting incoming requests to protect latency, but this comes at the expense of availability. The core problem is that static circuit breaker configurations struggle to determine when to trigger circuit breaking in highly dynamic microservice environments. This difficulty often results in scenarios where neither latency nor availability objectives are achieved. The challenge is to develop a circuit breaking mechanism that can adapt to dynamic conditions and maintain performance guarantees while maximizing service throughput.

## Method summary

The paper proposes an adaptive circuit breaking mechanism implemented through an adaptive controller that dynamically adjusts circuit breaker parameters based on observed system behavior. Unlike static circuit breakers that use fixed thresholds, this controller continuously monitors tail response time and adjusts the circuit breaking threshold to keep response times below a specified target while maximizing the number of successfully answered requests. The controller is implemented within the Istio service mesh framework running on Kubernetes. The adaptive mechanism responds to changing load conditions and system dynamics by modulating when circuit breaking is triggered, balancing the trade-off between protecting latency and maintaining availability. The implementation leverages the existing circuit breaking capabilities in Istio but adds a control layer that adjusts parameters based on real-time performance metrics.

## Ground truth and evaluation

The evaluation uses a testbed based on Istio and Kubernetes where the adaptive controller is experimentally compared against static circuit breaker configurations across multiple overload scenarios. The ground truth is established through direct measurement of system metrics including tail response time, availability (successfully answered requests), percentage of circuit broken requests, and percentage of requests timing out. The experiments measure whether the system maintains tail response time below a given threshold and tracks the trade-offs between availability and circuit breaking rates. The evaluation includes cold start scenarios and measures performance over time to assess how well the controller adapts to changing conditions. Multiple static circuit breaker configurations are tested to establish baseline performance for comparison with the adaptive approach.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the results indicate that even with the adaptive controller, the system maintains tail response time below the threshold only 98 percent of the time on average when including cold starts, suggesting some scenarios where the controller cannot meet objectives. The availability achieved is 70 percent with 29 percent of requests being circuit broken, indicating that a significant portion of requests are still rejected. The evaluation is conducted in a testbed environment which may not capture all complexities of production systems. The paper does not discuss how the controller behaves under different types of failures beyond overload scenarios or how it performs with different microservice architectures and communication patterns.

## Gaps this paper opens

The paper focuses exclusively on performance management through circuit breaking but does not address root cause identification of why overload or performance degradation occurs in the first place. While the adaptive controller responds to symptoms by adjusting circuit breaker thresholds, it does not provide insights into what upstream services or dependencies are causing the overload conditions. The relationship between circuit breaking decisions and the underlying service dependency topology is not explored, leaving open questions about how failures propagate through the system and whether circuit breaking at certain points is more effective than others. The temporal patterns of when circuit breaking is triggered and how these patterns relate to cascading failures or dependency chains are not analyzed. The paper does not investigate whether the adaptive mechanism could be enhanced by incorporating knowledge of service dependencies or temporal failure propagation patterns to make more informed decisions about where and when to apply circuit breaking.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic as it addresses performance management and failure mitigation in cloud-native systems but does not focus on root cause analysis. The adaptive circuit breaking mechanism is a remediation technique that responds to observed performance degradation rather than identifying why degradation occurs. For a thesis on root cause analysis using temporal and dependency analysis, this work highlights the need for understanding what causes overload conditions that trigger circuit breaking. The paper demonstrates that reactive mechanisms alone, even when adaptive, still result in significant request rejection and occasional threshold violations. This suggests that combining such remediation mechanisms with root cause analysis could enable more proactive management. The temporal aspects of when circuit breaking occurs and the dependency relationships between services that might contribute to overload are relevant but unexplored dimensions that connect to the thesis focus on temporal and dependency analysis for root cause identification.
