---
paper_id: 133
title: "Composite Indexing for Service Recovery: An AI-Unified Alerting Framework for Enterprise Messaging Platforms"
authors:
  - Bala Maheshbabu Kolluri
year: 2025
venue: European Modern Studies Journal
doi: 10.59573/emsj.9(5).2025.100
arxiv_id: ""
url: "https://openalex.org/W7104177584"
pdf_path: data/pdfs/paper_133.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - observability_data_analysis
  - recommendation_and_remediation

method:
  family: hybrid
  specific: composite health indexing with ML-based correlation and anomaly detection
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
  primary_contribution: A framework that aggregates multi-layered telemetry into weighted health indices combined with ML-based anomaly detection to enable context-aware incident detection and automated remediation in enterprise messaging platforms.
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

Traditional monitoring approaches for enterprise messaging platforms suffer from fundamental limitations in detecting and recovering from service degradation. Alert fatigue occurs when monitoring systems generate excessive false positives from isolated metric threshold violations without understanding broader system context. Enterprise messaging platforms operate across multiple layers including infrastructure, application logic, and user experience, making it difficult to correlate signals and identify root causes when incidents occur. Existing monitoring solutions lack the ability to aggregate telemetry across these dimensions into meaningful health indicators that reflect actual service quality. The strict delivery guarantees and compliance requirements of mission-critical messaging platforms demand more sophisticated approaches to observability and automated recovery that can maintain reliability while reducing operational burden on site reliability engineers.

## Method summary

The composite indexing framework aggregates telemetry from infrastructure, application, and user experience layers into weighted health indices that represent overall system state. Signal collection gathers metrics, logs, and traces from multiple sources which undergo normalization to enable cross-layer comparison and aggregation. Machine learning models perform correlation analysis to identify relationships between different telemetry signals and detect anomalies that indicate service degradation. The system computes composite health scores by applying weights to individual metrics based on their importance to service quality. Context-aware alerting uses these health indices rather than individual metric thresholds to trigger incidents, reducing false positives. Graduated recovery procedures implement automated remediation actions based on the severity and type of detected anomalies, creating a closed-loop system. The framework integrates AI components throughout the pipeline to enhance correlation detection, anomaly identification, and recovery decision-making.

## Ground truth and evaluation

The framework underwent empirical evaluation in production environments of enterprise messaging platforms. Performance metrics included alert precision measuring the reduction in false positive alerts compared to traditional threshold-based monitoring. Detection speed assessed how quickly the system identified service degradation events. Recovery time measured the duration from incident detection to service restoration through automated remediation. Operational burden quantified the reduction in manual intervention required from site reliability engineers. The evaluation demonstrated substantial improvements across all metrics, though specific numerical results are not detailed in the abstract. The production deployment context suggests ground truth was derived from actual service incidents and their outcomes, with comparison against baseline monitoring systems previously in use.

## Stated limitations

The abstract does not explicitly state limitations of the proposed framework. No discussion appears regarding computational overhead of the composite indexing calculations or machine learning model training requirements. The scalability constraints of aggregating multi-layered telemetry across large distributed systems are not addressed. There is no mention of challenges in determining appropriate weights for health index computation or how these weights might need adjustment across different deployment contexts. The conditions under which automated remediation might fail or cause additional problems are not discussed. The generalizability of the approach beyond enterprise messaging platforms to other types of distributed systems remains unspecified.

## Gaps this paper opens

The framework raises questions about how to systematically determine optimal weights for different telemetry signals when computing composite health indices across diverse system architectures. The relationship between composite health scores and actual root causes of incidents requires further investigation, particularly whether aggregated indices obscure causal relationships needed for diagnosis. The paper does not address how temporal patterns in health indices could reveal failure propagation paths through service dependencies. Integration with topology-aware analysis that understands service dependency graphs remains unexplored. The role of temporal causal analysis in distinguishing correlation from causation within the ML-based correlation component needs clarification. How the framework handles cascading failures where multiple composite indices degrade simultaneously is unclear. The approach to incorporating domain knowledge about messaging platform semantics into the AI components requires elaboration.

## Relevance to the thesis topic

This work addresses observability and automated remediation in distributed systems, which are adjacent concerns to root cause analysis in cloud-native environments. The composite indexing approach aggregates multi-layered telemetry similar to how RCA frameworks must synthesize diverse observability data, though it focuses on health scoring rather than causal diagnosis. The ML-based correlation component touches on identifying relationships between signals, which relates to understanding dependencies, but does not explicitly model service topology or temporal causal chains. The framework's emphasis on automated recovery suggests it assumes root causes are implicitly identified through anomaly patterns, whereas the thesis focuses on explicit causal analysis. The graduated recovery procedures could benefit from temporal failure propagation analysis to understand how incidents evolve. The production evaluation methodology and focus on reducing operational burden align with practical RCA goals. However, the paper's primary contribution is proactive monitoring and remediation rather than post-incident root cause diagnosis, making it complementary but not central to temporal and dependency-based RCA frameworks.
