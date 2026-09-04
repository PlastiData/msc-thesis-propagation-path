---
paper_id: 391
title: "DMSA: A Decentralized Microservice Architecture for Edge Networks"
authors:
  - Yuang Chen
  - Chengdi Lu
  - Yongsheng Huang
  - Chang Wu
  - Fengqian Guo
  - Hancheng Lu
  - Chang Wen Chen
year: 2025
venue: arXiv
doi: ""
arxiv_id: 2501.00883
url: "http://arxiv.org/abs/2501.00883v1"
pdf_path: data/pdfs/paper_391.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - service_dependency_topology
  - recommendation_and_remediation

method:
  family: rule_based
  specific: decentralized scheduling with multi-level weighted load balancing
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
  primary_contribution: A decentralized microservice architecture that delegates control plane scheduling functions to edge nodes with customized discovery, monitoring, and scheduling modules optimized for edge network constraints.
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

Traditional centralized microservice architectures face fundamental challenges when deployed in edge networks due to dispersed node locations, complex topologies, and intricate dynamic microservice dependencies. The centralized control plane creates bottlenecks and single points of failure that are incompatible with the distributed nature of edge computing environments. Existing microservice architectures struggle to maintain accurate awareness of instance deployments across geographically distributed edge nodes while simultaneously keeping monitoring overhead low. The dynamic nature of microservice dependencies in edge networks, combined with varying network conditions and link failures, requires scheduling mechanisms that can adapt quickly without relying on centralized coordination. Current solutions cannot adequately balance the competing requirements of low latency, high reliability, and efficient resource utilization in edge deployments where network conditions fluctuate frequently.

## Method summary

DMSA delegates scheduling functions from a centralized control plane to individual edge nodes, enabling decentralized decision-making for microservice management. The architecture redesigns three core modules specifically for edge networks: microservice discovery, monitoring, and scheduling. The discovery module maintains precise awareness of microservice instance deployments across distributed edge nodes without centralized coordination. The monitoring module reduces overhead and measurement errors through localized data collection and processing at edge nodes. The scheduling module implements a customized scheme using multi-port listening and zero-copy forwarding to achieve high data forwarding efficiency. A dynamic weighted multi-level load balancing algorithm adjusts scheduling decisions based on three factors: reliability, priority, and response delay. This algorithm operates locally at each edge node, making scheduling decisions based on real-time observations of network conditions and service performance. The multi-port listening mechanism allows services to accept connections on multiple network interfaces simultaneously, while zero-copy forwarding minimizes data copying overhead during request routing.

## Ground truth and evaluation

The evaluation uses a physical verification platform implementing DMSA in real edge network environments. Performance metrics include service response delay and execution success rate measured under various network conditions including link failures and network fluctuations. The baseline comparisons involve state-of-the-art scheduling schemes and traditional centralized approaches, though specific names of comparison systems are not detailed. Ground truth for scheduling effectiveness comes from actual service execution outcomes on the physical platform, measuring whether requests complete successfully and how long they take. The evaluation methodology focuses on empirical performance under stress conditions rather than synthetic workloads or simulations. Network failures and fluctuations are introduced to test the resilience of the decentralized architecture compared to centralized alternatives. Success rates and response times serve as the primary indicators of whether the decentralized approach effectively handles the challenges of edge network deployments.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed DMSA approach. The focus remains on demonstrating performance improvements over existing centralized architectures without discussing scenarios where decentralization might introduce challenges. No analysis is provided regarding the overhead of maintaining consistency across decentralized scheduling decisions or potential conflicts when multiple edge nodes make independent scheduling choices. The scalability limits of the decentralized approach as the number of edge nodes grows are not addressed. There is no discussion of how the system handles network partitions that might isolate edge nodes from each other or create inconsistent views of the overall system state. The paper does not examine trade-offs between decentralization benefits and potential coordination costs or the complexity of debugging and managing a fully decentralized system.

## Gaps this paper opens

The absence of root cause analysis capabilities in DMSA creates opportunities for integrating failure diagnosis into decentralized edge architectures. While DMSA monitors service performance and adapts scheduling, it does not explain why failures occur or identify underlying causes of performance degradation. The decentralized monitoring data collected at edge nodes could serve as valuable input for distributed root cause analysis, but mechanisms for correlating observations across nodes to identify causal relationships are not developed. The dynamic scheduling decisions based on reliability, priority, and delay metrics suggest that temporal patterns in these metrics could reveal failure propagation paths, yet no causal analysis framework is proposed. The multi-level load balancing algorithm reacts to observed conditions but lacks diagnostic capabilities to determine whether poor performance stems from application bugs, resource exhaustion, network issues, or cascading failures. Understanding how failures propagate through microservice dependencies in a decentralized edge environment remains an open problem that DMSA's architecture could support but does not address.

## Relevance to the thesis topic

DMSA relates to the thesis topic by addressing microservice dependency management and monitoring in distributed systems, though it focuses on scheduling rather than root cause analysis. The decentralized monitoring infrastructure provides observability data at edge nodes that could feed into temporal and dependency analysis for RCA. The architecture's awareness of microservice dependencies and instance deployments represents foundational information needed for constructing service dependency topologies in cloud-native systems. However, DMSA does not perform causal analysis or attempt to identify root causes of failures. The dynamic scheduling based on reliability and response delay metrics demonstrates reactive adaptation to problems but lacks the diagnostic depth required for RCA. The temporal aspects of DMSA's load balancing decisions could inform understanding of how failures propagate over time through microservice chains, though this analysis is not performed. The edge network context differs from typical cloud-native deployments, but the challenges of distributed monitoring and dependency tracking are relevant. DMSA could be viewed as providing infrastructure that an RCA framework would build upon, offering monitoring data and topology information while leaving causal analysis unaddressed.
