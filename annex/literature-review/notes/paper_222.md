---
paper_id: 222
title: "Evaluating Asynchronous Semantics in Trace-Discovered Resilience Models: A Case Study on the OpenTelemetry Demo"
authors:
  - Anatoly A. Krasnovsky
year: 2025
venue: arXiv.org
doi: 10.1007/978-3-032-23304-2_24
arxiv_id: 2512.12314
url: "https://www.semanticscholar.org/paper/4ce2fad4774e2cfcc06253a65424917c1eadad08"
pdf_path: data/pdfs/paper_222.pdf
read_date: 2026-05-11

category:
  - service_dependency_topology
  - benchmark_and_evaluation
  - distributed_system_monitoring

method:
  family: hybrid
  specific: trace-derived dependency graph with Monte Carlo simulation
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
  primary_contribution: An empirical evaluation showing that asynchronous semantics for message queue dependencies have negligible impact on immediate HTTP availability predictions in trace-discovered resilience models.
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

Distributed tracing and chaos engineering have become standard practices for microservices, yet resilience models that predict system behavior under failures remain largely manual and specific to individual deployments. Existing approaches to modeling service dependencies and predicting availability under failure scenarios require significant manual effort and do not leverage the observability data already collected through distributed tracing. The question of whether asynchronous communication patterns, such as message queues, need explicit modeling in resilience predictions remains unresolved. Without automated methods to discover dependencies from traces and validate predictions against actual chaos experiments, practitioners lack confidence in whether simplified connectivity models are sufficient or whether more complex asynchronous semantics are necessary for accurate availability predictions.

## Method summary

The approach derives a service dependency graph directly from raw OpenTelemetry traces collected from the system. Each edge in the graph represents a dependency between services, with edges labeled by their communication type such as HTTP or Kafka. The model attaches endpoint-specific success predicates to determine when a particular endpoint is available based on the availability of its dependencies. Monte Carlo simulation is then used to estimate endpoint availability under fail-stop service failures by randomly sampling which services fail according to a specified failure fraction. The key innovation is the introduction of asynchronous semantics that treats Kafka message queue edges as non-blocking for immediate HTTP success, meaning that a service can successfully respond to an HTTP request even if its downstream Kafka dependency is unavailable. The entire workflow is automated through GitHub Actions, which discovers the dependency graph from traces, runs availability simulations, and executes chaos experiments that randomly terminate microservices in a Docker Compose deployment of the OpenTelemetry Demo application.

## Ground truth and evaluation

Ground truth is obtained through actual chaos experiments executed on the OpenTelemetry Demo application running in Docker Compose. The chaos experiments randomly kill microservices according to specified failure fractions and measure the actual availability of HTTP endpoints by sending requests and observing success rates. The evaluation compares predicted availability from the Monte Carlo simulations against measured availability from the chaos experiments across different failure fractions. The model successfully reproduces the overall availability degradation curve observed in the real system. The specific contribution of asynchronous semantics is evaluated by comparing simulation results with and without the asynchronous treatment of Kafka edges. Quantitative results show that asynchronous semantics change predicted availabilities by at most approximately 0.001 percentage points across the studied failure scenarios, demonstrating negligible practical impact for immediate HTTP availability predictions in this case study.

## Stated limitations

The paper explicitly acknowledges that the null result regarding asynchronous semantics is specific to immediate HTTP availability in the studied case. The finding that asynchronous semantics have negligible impact may not generalize to other resilience metrics or system architectures. The case study is limited to a single application, the OpenTelemetry Demo, which may not represent the diversity of microservice architectures encountered in production environments. The fail-stop failure model used in the simulations and chaos experiments represents only one type of failure mode, and does not capture partial failures, performance degradation, or Byzantine failures. The evaluation focuses on availability as the primary metric and does not consider other resilience properties such as latency, throughput, or data consistency that might be more sensitive to asynchronous communication patterns.

## Gaps this paper opens

The null result regarding asynchronous semantics raises questions about what conditions would make explicit modeling of asynchronous dependencies necessary for resilience predictions. The paper does not explore whether different types of asynchronous patterns beyond Kafka message queues would show similar negligible impact. The evaluation is limited to immediate availability and does not investigate whether asynchronous semantics matter for eventual consistency, data loss, or long-term system behavior after failures. The trace-discovered model relies on observed dependencies in traces, which may miss rarely-exercised paths or failure-mode-specific dependencies that only appear under degraded conditions. The paper does not address how the model would handle dynamic topology changes, service scaling, or evolving dependency patterns over time. The automated workflow demonstrates feasibility on a demo application but leaves open questions about scalability to large production systems with hundreds of services and complex dependency structures.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses service dependency topology discovery from traces, which is a foundational component for root cause analysis in cloud-native systems. The trace-derived dependency graph provides the structural information needed for understanding failure propagation paths, though the paper focuses on availability prediction rather than root cause identification. The temporal aspect is present implicitly through the trace analysis that captures request-response patterns, but the paper does not perform explicit temporal causal analysis to identify root causes of observed failures. The Monte Carlo simulation approach demonstrates how dependency models can be validated against ground truth from chaos experiments, which is relevant for evaluating root cause analysis frameworks. However, the paper's primary focus on resilience modeling and availability prediction rather than diagnosing the causes of specific incidents means it provides supporting methodology rather than directly addressing root cause analysis. The automated trace-to-graph pipeline and the validation methodology against chaos experiments offer practical techniques that could be adapted for building and validating dependency models used in root cause analysis systems.
