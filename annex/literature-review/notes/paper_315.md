---
paper_id: 315
title: A Decentralized Microservice Scheduling Approach Using Service Mesh in Cloud-Edge Systems
authors:
  - Yangyang Wen
  - Paul Townend
  - Per-Olov Östberg
  - Abel Souza
  - Clément Courageux-Sudan
year: 2025
venue: Fall Joint Computer Conference
doi: 10.1109/JCC67032.2025.00012
arxiv_id: 2510.11189
url: "https://www.semanticscholar.org/paper/eabf410d98d9ac285d1ce3ad57545bebcab36b8d"
pdf_path: data/pdfs/paper_315.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - service_dependency_topology
  - other

method:
  family: other
  specific: decentralized sidecar-based scheduling
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
  primary_contribution: An architectural approach that embeds autonomous scheduling logic into service mesh sidecar proxies to enable decentralized microservice scheduling across cloud-edge systems without centralized control.
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

Traditional centralized scheduling mechanisms face significant challenges when microservice-based systems scale across the cloud-edge continuum. These centralized approaches encounter increasing latency as the system grows, suffer from coordination overhead when managing large numbers of distributed services, and exhibit vulnerability to single points of failure. The cloud-edge environment exacerbates these issues because services are distributed across heterogeneous infrastructure with varying network characteristics and resource availability. Existing scheduling solutions rely on centralized controllers that must maintain global state and make decisions for all services, creating bottlenecks that limit scalability and responsiveness in large-scale deployments.

## Method summary

The proposed approach embeds lightweight autonomous scheduling logic directly into service mesh sidecar proxies, transforming them into decentralized in-situ schedulers. Each sidecar proxy makes scheduling decisions locally based on its immediate context and available information, eliminating the need for centralized control. The architecture leverages the existing service mesh infrastructure, which already provides programmable distributed traffic management capabilities across microservices. By distributing scheduling intelligence to the sidecars, the system enables local decision-making at each service instance without requiring coordination with a central authority. The design takes advantage of the maturity of service mesh technologies to implement this decentralized scheduling layer as an extension of existing traffic management functions.

## Ground truth and evaluation

The evaluation focuses on demonstrating scalability potential rather than validating scheduling correctness or optimality. Initial results measure response time and latency under varying request rates to show how the decentralized approach scales compared to centralized alternatives. The experiments assess system performance characteristics as load increases, examining whether the distributed scheduling architecture maintains acceptable latency profiles. The paper presents preliminary evidence supporting the scalability claims but does not provide comprehensive comparisons against specific baseline scheduling algorithms or detailed metrics on scheduling quality. The evaluation is positioned as exploratory, demonstrating the feasibility of the architectural direction rather than establishing definitive performance superiority.

## Stated limitations

The paper explicitly positions itself as presenting an architectural direction rather than a finalized scheduling algorithm. The authors acknowledge that they are providing preliminary evidence of scalability potential rather than a complete solution. The work does not deliver a fully developed scheduling algorithm with proven optimality guarantees or comprehensive evaluation across diverse workload scenarios. The initial results are presented as supporting evidence for the architectural approach rather than definitive validation. The paper does not address how the decentralized schedulers handle complex coordination scenarios that may require global knowledge or how they ensure consistency across distributed scheduling decisions.

## Gaps this paper opens

The paper leaves open fundamental questions about how decentralized schedulers coordinate when scheduling decisions require global knowledge or cross-service dependencies. It does not address how the system handles failure scenarios where local scheduling decisions may conflict or lead to suboptimal global outcomes. The mechanism for maintaining consistency across distributed scheduling decisions remains unspecified. Questions about how the approach integrates with existing orchestration platforms and whether it can coexist with centralized scheduling for certain workload types are not explored. The paper does not provide guidance on what scheduling policies are appropriate for implementation in sidecars or how to tune the autonomous scheduling logic for different application requirements. The relationship between this scheduling approach and service dependency analysis for root cause determination is not examined.

## Relevance to the thesis topic

This work relates to the thesis topic through its focus on distributed system architecture and service mesh infrastructure, which are foundational elements of cloud-native systems where root cause analysis must operate. Understanding how scheduling decisions are made in a decentralized manner provides context for how failures might propagate through service dependencies in modern cloud-native environments. The service mesh sidecar architecture described here represents the observability and control plane infrastructure that root cause analysis systems must interact with to gather dependency information and temporal execution data. However, the paper does not address failure detection, anomaly identification, or causal analysis of system problems. The decentralized nature of the scheduling approach could complicate root cause analysis by distributing decision-making logic that might contribute to failures, making it harder to trace causality through centralized logs. The work is adjacent rather than core because it focuses on system architecture and scheduling rather than the diagnostic and analytical capabilities needed for root cause analysis.
