---
paper_id: 360
title: "Debugging Streaming Applications In Kubernetes: Tools, Patterns, And Case Studies"
authors:
  - Swapna Marru
year: 2025
venue: Journal of International Crisis and Risk Communication Research
doi: 10.63278/jicrcr.vi.3332
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/64ace8ac82530b7da202ad0c9bcd0175d7f608d3"
pdf_path: data/pdfs/paper_360.pdf
read_date: 2026-05-11

category:
  - observability_data_analysis
  - distributed_system_monitoring
  - other

method:
  family: other
  specific: ephemeral containers and EFK stack logging
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
  primary_contribution: A comprehensive framework for debugging streaming applications in Kubernetes using non-disruptive techniques including ephemeral containers and centralized logging.
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

Streaming applications deployed in Kubernetes environments face unique debugging challenges that differ fundamentally from traditional stateless microservices. These challenges stem from three primary characteristics: in-memory state persistence, strict event-time semantics, and continuous uptime requirements. The containerized infrastructure introduces additional complexity through its ephemeral nature and the distributed architecture of streaming systems. Traditional debugging approaches that require service interruption or pod restarts are incompatible with streaming applications where data loss or state corruption can have cascading effects. The combination of container visibility limitations, pod connectivity issues, and configuration drift creates a clinical environment where conventional debugging tools prove inadequate for maintaining operational continuity while diagnosing production issues.

## Method summary

The paper presents a comprehensive debugging framework centered on non-disruptive techniques for Kubernetes-based streaming applications. The approach utilizes ephemeral containers that enable direct access to running container environments without requiring image modifications or pod restarts, preserving the state and continuity of streaming workloads. The kubectl debug command serves as a primary tool for live diagnostics without service interruption. For observability, the framework employs the EFK stack comprising Fluentd for log aggregation, Elasticsearch for storage and indexing, and Kibana for visualization to provide end-to-end observability across distributed streaming pipelines. The methodology emphasizes log processing pipelines with metadata enrichment to handle high-volume streaming workloads. The framework addresses specific Kubernetes debugging challenges through specialized tooling and standardized processes that maintain system availability while providing deep operational insights into running applications.

## Ground truth and evaluation

The paper evaluates the proposed debugging framework through practical case studies across three domains: financial services, IoT analytics, and media streaming platforms. These real-world deployments demonstrate the effectiveness of the integrated debugging approach in resolving complex operational problems including memory leaks, thread contention issues, and resource management bugs. The evaluation focuses on practical metrics such as development speed improvements and production stability gains achieved through streamlined debugging operations. The case studies serve as empirical validation showing that the non-disruptive debugging techniques enable real-time issue resolution while maintaining operational continuity in mission-critical systems. However, the paper does not provide quantitative metrics or controlled experimental comparisons against baseline debugging approaches, relying instead on qualitative assessments of effectiveness in production environments.

## Stated limitations

The paper does not explicitly enumerate its limitations in a dedicated section. The abstract and content focus primarily on presenting the debugging framework and demonstrating its applicability through case studies. The lack of quantitative evaluation metrics or controlled experiments represents an implicit limitation in the rigor of the validation approach. The paper does not discuss scenarios where the proposed techniques might fail or prove insufficient, nor does it address potential overhead introduced by the debugging infrastructure itself on streaming application performance. There is no discussion of scalability limits for the EFK stack when handling extremely high-volume streaming workloads or the resource costs associated with maintaining ephemeral containers for debugging purposes.

## Gaps this paper opens

The paper identifies but does not fully address several critical gaps in debugging streaming applications. While it presents tools and patterns for diagnosis, it lacks automated root cause analysis capabilities that could correlate debugging observations with underlying system faults. The framework does not integrate temporal analysis of failures or dependency tracking across distributed streaming components, which are essential for understanding cascading failures in complex topologies. There is no discussion of how debugging insights could feed into automated remediation or self-healing mechanisms. The paper does not explore how machine learning or LLM-based approaches could enhance the debugging process by automatically analyzing logs and system metrics to identify root causes. The relationship between debugging observations and the underlying service dependency graph remains unexplored, limiting the ability to understand how failures propagate through streaming pipelines.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic as it addresses observability and debugging in cloud-native systems but does not focus on root cause analysis using temporal and dependency analysis. The debugging framework provides foundational observability capabilities through centralized logging and live diagnostics that could serve as data sources for a root cause analysis system. The emphasis on streaming applications with strict event-time semantics and state persistence aligns with scenarios where temporal analysis would be particularly valuable for understanding failure propagation. However, the paper treats debugging as a manual diagnostic process rather than an automated analytical framework. The EFK stack and observability infrastructure described could provide the raw data needed for temporal causal analysis, but the paper does not develop methods for automatically inferring causality or analyzing service dependencies. The case studies in complex production environments demonstrate the types of problems that a comprehensive RCA framework would need to address, including memory leaks and resource contention that manifest over time.
