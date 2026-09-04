---
paper_id: 038
title: "Enhancing Resilience and Scalability in Travel Booking Systems: A Microservices Approach to Fault Tolerance, Load Balancing, and Service Discovery"
authors:
  - Biman Barua
  - M. Shamim Kaiser
year: 2024
venue: arXiv (Cornell University)
doi: 10.48550/arxiv.2410.19701
arxiv_id: ""
url: "https://openalex.org/W4404312241"
pdf_path: data/pdfs/paper_038.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - service_dependency_topology
  - recommendation_and_remediation

method:
  family: rule_based
  specific: Circuit Breaker Pattern with Round-Robin load balancing
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
  primary_contribution: Demonstrates implementation of microservices architecture with circuit breaker pattern and load balancing for airline booking systems, achieving 60% reduction in failure propagation and 99.95% uptime.
  novelty_strength: incremental

limitations_authors_state: []

quality_flags:
  self_constructed_ground_truth: false
  comparison_table_only: false
  hobby_project_scale: false
  predictable_outcome: false

relevance:
  relevance_to_topic: peripheral
  must_cite: false
---

## Problem statement

Traditional airline reservation systems are built on monolithic architectures that are rigid and centralized, making them vulnerable to bottlenecks and single points of failure. These systems cannot adequately meet the dynamic requirements of modern airlines that need to handle variable loads and maintain high availability. When external dependencies such as flight APIs or payment systems fail in monolithic systems, the failures cascade through the entire application, causing widespread service disruption. The lack of independent scalability means that resource constraints in one component affect the entire system, limiting the ability to handle concurrent users during peak demand periods.

## Method summary

The paper implements a microservices architecture for airline booking systems using several key techniques for fault tolerance and scalability. The Circuit Breaker Pattern is employed to prevent failure propagation when consuming external resources like flight APIs and payment systems, allowing the system to fail gracefully and maintain partial functionality during external service outages. Round-Robin load balancing distributes user requests evenly across multiple service instances to prevent overloading individual components. The architecture includes health checks and real-time monitoring to detect failures early and enable proactive intervention before users are affected. Traffic rerouting capabilities automatically redirect requests away from failing services to healthy instances. Each microservice can be deployed and scaled independently, allowing targeted resource allocation based on specific service demands.

## Ground truth and evaluation

The evaluation compares the microservices implementation against traditional monolithic architectures using operational metrics from a deployed airline booking system. Performance improvements are measured through percentage reductions in failure propagation, downtime, and increases in concurrent user capacity and system uptime. The paper reports a 60% reduction in failure propagation to dependent systems, 99.95% uptime achievement, 35% performance improvement from load balancing, 40% increase in system scalability, 50% decrease in downtime, and 30% increase in concurrent user support compared to monolithic baselines. No details are provided about the duration of testing, the scale of deployment, specific workload characteristics, or how these metrics were precisely measured and validated.

## Stated limitations

The paper does not explicitly state limitations of the proposed approach. There is no discussion of challenges encountered during implementation, scenarios where the microservices architecture might underperform, or trade-offs introduced by the design choices. The complexity overhead of managing distributed microservices, potential latency increases from inter-service communication, or difficulties in debugging distributed failures are not addressed. No consideration is given to the operational costs of maintaining multiple services, the learning curve for development teams, or situations where the circuit breaker pattern might mask underlying problems rather than solving them.

## Gaps this paper opens

The paper lacks detailed analysis of how failures propagate through the microservices dependency graph and what mechanisms could identify root causes when cascading failures do occur. While the circuit breaker prevents failure propagation, there is no discussion of how operators diagnose which external service initially failed or how to trace the impact through dependent services. The temporal aspects of failure propagation are not examined, leaving unclear how quickly failures spread before circuit breakers activate and whether there are patterns in failure sequences that could enable predictive intervention. The paper does not address how to distinguish between legitimate service degradation requiring circuit breaking and transient issues that might resolve quickly. There is no exploration of how monitoring data from health checks could be analyzed to understand causal relationships between service failures.

## Relevance to the thesis topic

This paper has peripheral relevance to the thesis topic as it addresses fault tolerance in distributed systems but does not engage with root cause analysis methodologies. The circuit breaker pattern and load balancing are preventive mechanisms that limit failure impact rather than diagnostic tools for understanding why failures occur. While the microservices architecture creates the service dependency topology that is central to the thesis framework, the paper does not analyze or visualize these dependencies for diagnostic purposes. The health checks and monitoring mentioned could provide observability data useful for root cause analysis, but the paper focuses solely on using this data for reactive failover rather than causal investigation. The work demonstrates the type of cloud-native system that would benefit from the temporal and dependency analysis framework proposed in the thesis, but contributes no methods for performing such analysis.
