---
paper_id: 059
title: APPROACHES AND TOOLS FOR AUTOMATION OF MICROSERVICE ARCHITECTURE TESTING
authors:
  - Iryna Daineko
year: 2026
venue: Наука і техніка сьогодні
doi: 10.52058/2786-6025-2025-13(54)-1613-1626
arxiv_id: ""
url: "https://openalex.org/W7124723752"
pdf_path: data/pdfs/paper_059.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - benchmark_and_evaluation
  - observability_data_analysis

method:
  family: hybrid
  specific: multi-layered automated testing framework combining API testing, contract testing, and integration testing
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
  primary_contribution: A comprehensive automated testing framework for microservice architectures that combines API testing, consumer-driven contract testing, and multi-layered integration testing to enhance stability and reliability in FinTech systems.
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

The transition from monolithic systems to microservice architectures in FinTech platforms introduces significant testing challenges that traditional approaches cannot adequately address. The reliability of microservice-based applications depends not only on individual service correctness but also on the stability of network interactions, asynchronous communication patterns, and evolving API contracts. These distributed characteristics create high levels of architectural uncertainty where failures can propagate across service boundaries in unpredictable ways. Traditional testing methodologies prove insufficient because they do not account for the complex inter-service dependencies and dynamic nature of independently deployable services. The problem is further compounded by the need to maintain continuous delivery pipelines while ensuring system stability and security in highly dynamic environments.

## Method summary

The research proposes a comprehensive automated testing framework that integrates three distinct testing layers specifically designed for microservice ecosystems. The framework combines API testing to verify individual service endpoints, consumer-driven contract testing to prevent breaking changes between service providers and consumers, and multi-layered integration testing to reveal emergent behaviors in distributed environments. The methodology includes systematic review of scientific publications to establish theoretical foundations, comparative analysis of leading automation tools to identify best practices, and construction of UML-based models to illustrate inter-service communication patterns. The framework is designed for tight integration into CI/CD pipelines to enable continuous validation throughout the development lifecycle. The approach emphasizes the coordination of these testing layers to address both individual service correctness and system-wide behavioral properties.

## Ground truth and evaluation

The evaluation methodology employs multiple quantitative metrics to assess testing effectiveness in real-world microservice deployments. The study measures execution time to evaluate testing efficiency, defect detection rates to quantify the ability to identify issues before production, failure propagation patterns to understand how errors cascade through service dependencies, and system stability indicators to assess overall reliability. The experimental evaluation applies these metrics to FinTech systems built on microservice principles, comparing outcomes before and after implementing the proposed testing framework. The results demonstrate substantial reductions in integration failures and accelerated regression testing cycles. The findings confirm that contract testing effectively prevents breaking changes in independently deployable services while integration testing remains essential for detecting emergent distributed system behaviors that cannot be identified through isolated service testing alone.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed approach. The focus remains on demonstrating the benefits of the comprehensive testing framework without discussing scenarios where the methodology might face challenges. There is no discussion of computational overhead introduced by multi-layered testing or potential bottlenecks in CI/CD pipeline execution times. The paper does not address scalability concerns when the number of microservices grows significantly or when service dependency graphs become highly complex. Cost considerations for implementing and maintaining the automated testing infrastructure are not examined. The generalizability of findings beyond FinTech domains remains unexplored, as does the applicability to microservice architectures with different communication patterns or technology stacks.

## Gaps this paper opens

The research reveals several areas requiring further investigation in microservice testing automation. The paper does not address how to automatically identify which services require integration testing versus those adequately covered by contract testing alone, leaving service selection strategies undefined. The relationship between test coverage metrics and actual failure prevention in production environments remains unexplored. There is no discussion of how to handle non-deterministic behaviors common in distributed systems or how to test temporal dependencies and timing-sensitive interactions between services. The framework does not incorporate mechanisms for root cause analysis when tests fail, leaving diagnosis of complex inter-service failures as manual work. The paper does not examine how observability data from production systems could inform test case generation or prioritization. Methods for automatically detecting when service contracts have evolved in ways that require test updates are not provided.

## Relevance to the thesis topic

This paper addresses testing automation in microservice architectures but does not directly tackle root cause analysis during operational failures. The work is adjacent to the thesis topic because it focuses on preventing failures through comprehensive testing rather than diagnosing failures after they occur in production. The emphasis on failure propagation patterns provides relevant context for understanding how issues cascade through service dependencies, which relates to temporal failure propagation analysis. The discussion of inter-service communication patterns and dependency modeling through UML diagrams connects to service dependency topology analysis. However, the paper does not employ temporal analysis techniques to trace causality chains or use observability data for post-incident diagnosis. The framework operates primarily in pre-production testing phases rather than runtime monitoring and analysis. While the work contributes to understanding microservice reliability and inter-service dependencies, it does not directly advance methods for identifying root causes of failures in cloud-native production environments using temporal and dependency analysis.
