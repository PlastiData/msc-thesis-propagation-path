---
paper_id: 064
title: Quantifying Chaos Engineering Effectiveness In Event-Driven Microservices
authors:
  - Mahitha Adapa
  - Naveen Reddy Singi Reddy
year: 2025
venue: Journal of International Crisis and Risk Communication Research
doi: 10.63278/jicrcr.vi.3334
arxiv_id: ""
url: "https://openalex.org/W4415269255"
pdf_path: data/pdfs/paper_064.pdf
read_date: 2026-05-11

category:
  - benchmark_and_evaluation
  - observability_data_analysis
  - distributed_system_monitoring

method:
  family: other
  specific: controlled chaos experimentation with comparative analysis
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
  primary_contribution: Empirical demonstration that event-driven microservices exhibit distinct failure propagation patterns and observability challenges compared to REST-based systems, requiring adapted chaos engineering approaches.
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

Traditional chaos engineering techniques were developed primarily for synchronous request-response systems and may not adequately capture the failure behaviors inherent in event-driven architectures. Event-driven microservices exhibit different failure propagation patterns due to asynchronous communication through message queues and event buses. The paper identifies a critical observability gap where resilience mechanisms in event-driven systems can mask underlying structural problems, creating what the authors term a "failure masking effect." This masking prevents operators from detecting issues that would be immediately visible in synchronous REST-based architectures. The core problem is determining whether existing chaos engineering practices and tools provide sufficient coverage and effectiveness when applied to event-driven systems, and if not, what adaptations are necessary.

## Method summary

The authors conducted controlled chaos experiments on containerized e-commerce microservices implemented in both event-driven and REST-based architectural patterns. They systematically evaluated major chaos engineering tools under varying failure conditions to compare their effectiveness across the two architectural styles. The experimental approach involved injecting different failure modes into the systems and measuring observability outcomes. The study focused on comparing metrics relevant to each architecture, specifically examining queue-based metrics for event-driven systems versus response time metrics for REST-based systems. Through this comparative analysis, the researchers identified distinct patterns of effectiveness for chaos engineering tools depending on the underlying communication pattern. The methodology emphasized empirical observation of how failures propagate differently in asynchronous versus synchronous systems and how these differences impact the ability to detect and diagnose problems.

## Ground truth and evaluation

The ground truth in this study derives from the controlled injection of known failures into the experimental microservices systems. The authors injected specific failure modes and observed the resulting system behaviors across both architectural patterns. Evaluation centered on comparing observability outcomes between event-driven and REST-based implementations when subjected to identical failure scenarios. The effectiveness of chaos engineering tools was assessed based on their ability to reveal structural problems and failure propagation patterns in each architecture. The paper does not specify precise quantitative metrics for measuring chaos engineering effectiveness but indicates that the evaluation involved analyzing how well different approaches exposed hidden issues. The comparative nature of the study allowed the researchers to establish that event-driven systems require longer experiment durations and different metric priorities to achieve coverage equivalent to what traditional chaos testing provides for synchronous systems.

## Stated limitations

The paper does not explicitly enumerate its limitations in a dedicated section. However, the scope is implicitly limited to containerized e-commerce microservices, which may not generalize to all event-driven system types or domains. The study focuses on comparing two specific architectural patterns and may not capture the full spectrum of hybrid or mixed-mode communication patterns found in production systems. The evaluation of chaos engineering tools appears to be conducted in controlled experimental settings rather than production environments, which may not reflect the complexity and scale challenges of real-world deployments. The paper does not discuss whether the identified failure masking effects vary with different resilience mechanism implementations or message queue technologies. Additionally, the empirical guidelines provided are derived from specific experimental conditions and may require validation across broader system configurations and workload patterns.

## Gaps this paper opens

The identification of failure masking effects in event-driven systems raises questions about how to design observability instrumentation that can penetrate resilience mechanisms to expose underlying structural issues. The paper reveals that different architectural patterns require different chaos testing strategies but does not provide automated methods for determining optimal experiment duration or metric selection for arbitrary event-driven systems. The finding that event-driven systems fail according to non-uniform patterns suggests a need for pattern-specific testing frameworks that can adapt to different failure propagation characteristics. The work does not address how to automatically detect whether a system exhibits event-driven failure patterns versus synchronous patterns, leaving open the question of automated chaos strategy selection. Furthermore, the paper does not explore how temporal dependencies in event-driven systems affect the timing and sequencing of chaos experiments, nor does it provide methods for constructing dependency models that account for asynchronous communication delays and queue dynamics.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses observability and failure behavior in distributed systems but does not directly tackle root cause analysis or dependency modeling. The identification of failure masking effects is relevant to understanding why root cause analysis might fail in event-driven architectures, as masked failures would not appear in typical observability data used for causal inference. The emphasis on queue-based metrics versus response times informs what temporal signals should be analyzed when performing root cause analysis in event-driven systems. The finding that event-driven systems require longer observation periods relates to the temporal analysis component of the thesis, suggesting that causal analysis windows must be extended to capture asynchronous failure propagation. However, the paper focuses on chaos engineering effectiveness rather than developing root cause analysis methods, making it more relevant for understanding system behavior characteristics than for directly informing RCA framework design. The insights about non-uniform failure patterns could inform how dependency graphs should be constructed differently for event-driven versus synchronous architectures.
