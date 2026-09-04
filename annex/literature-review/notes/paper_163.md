---
paper_id: 163
title: Designing Scalable AI Systems for Continuous Monitoring, Fault Detection, and Operational Intelligence
authors:
  - ANANYA PILLAI
  - VIKRAM DESHMUKHX
  - HARSHA BHATX
  - SNEHA RAJPUTX
  - Tejaswini S. Rao
year: 2026
venue: International Journal of Multidisciplinary Sciences and Technology
doi: 10.64137/31079911/ijmst-v2i1p105
arxiv_id: ""
url: "https://openalex.org/W7153010524"
pdf_path: data/pdfs/paper_163.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - anomaly_detection
  - service_dependency_topology

method:
  family: hybrid
  specific: layered reference architecture combining telemetry normalization, learning-based anomaly detection, and graph-based dependency reasoning
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
  primary_contribution: A research framework and reference architecture that unifies continuous monitoring, fault detection, and operational intelligence into a closed-loop system for distributed environments.
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

Modern digital platforms operate across heterogeneous clouds, microservices, data pipelines, AI-enabled applications, and cyber-physical workflows with expectations of continuous operation. Conventional monitoring approaches are insufficient because they report isolated symptoms rather than generating system-level understanding of operational state. The problem is that telemetry collection, anomaly detection, and operational decision-making are treated as disconnected toolchains rather than as components of a unified architectural problem. This fragmentation prevents systems from moving beyond reactive alerting toward evidence-based adaptation and intelligent operational response. The challenge is to design scalable AI systems that can integrate multiple observability signals, reason about dependencies, and support closed-loop operational intelligence across diverse domains including cloud-native software, healthcare, financial systems, and manufacturing.

## Method summary

The paper proposes a layered reference architecture that integrates five core capabilities into a unified framework. The first layer handles telemetry collection from heterogeneous sources across distributed systems. The second layer performs semantic data normalization to create consistent representations of observability data. The third layer applies learning-based anomaly detection to identify deviations from expected system behavior. The fourth layer uses graph-based dependency reasoning to understand relationships between system components and propagate fault information. The fifth layer implements policy-aware decision intelligence to enable evidence-based adaptation rather than simple alerting. The framework synthesizes advances from multiple research areas including observability engineering, log intelligence, software defect prediction, automated testing, and vulnerability detection. The architecture is designed to be cross-domain and applicable to software-intensive and distributed environments ranging from cloud-native systems to operational technology in healthcare, finance, and manufacturing.

## Ground truth and evaluation

The paper explicitly does not present fabricated benchmark outcomes or empirical validation results. Instead, it contributes a research-grade design blueprint, a model taxonomy, and an evaluation agenda for future empirical work. The authors position this as an architecture-centered research framework rather than a validated system with experimental results. The paper proposes that future work should validate the framework through empirical studies across the multiple domains it targets. No specific ground truth datasets, labeled fault scenarios, or quantitative evaluation metrics are provided. The contribution is conceptual and architectural rather than experimental, offering a blueprint for how such systems should be designed and what components they should integrate. The evaluation agenda is left as future work to be conducted by researchers implementing systems based on this reference architecture.

## Stated limitations

The paper does not explicitly enumerate technical limitations of the proposed framework. The authors acknowledge that the work is a research-grade design blueprint rather than a validated implementation, implicitly recognizing that empirical validation remains to be done. The framework is presented as intentionally cross-domain, which suggests a trade-off between generality and domain-specific optimization that is not explicitly discussed. The paper does not address computational complexity, scalability bounds, or performance characteristics of the proposed layered architecture. There is no discussion of how the graph-based dependency reasoning scales with system size or how the learning-based anomaly detection handles concept drift in production environments. The integration challenges between the five layers and the operational overhead of maintaining semantic normalization across heterogeneous telemetry sources are not examined. The paper also does not discuss limitations in terms of required training data, cold-start problems, or the accuracy-interpretability trade-offs inherent in the learning-based components.

## Gaps this paper opens

The paper opens significant gaps by proposing a comprehensive architecture without empirical validation or concrete implementation details. The learning-based anomaly detection component lacks specification of which machine learning techniques are most appropriate for different types of telemetry data or operational contexts. The graph-based dependency reasoning is mentioned as a capability but the paper does not address how dependency graphs are constructed, maintained, or updated in dynamic cloud-native environments where services are constantly deployed and scaled. The semantic data normalization layer is presented as essential but the paper provides no methodology for achieving normalization across fundamentally different telemetry types such as metrics, logs, traces, and events. The policy-aware decision intelligence component is described at a high level without addressing how policies are specified, how conflicts between policies are resolved, or how the system learns appropriate actions over time. The closed-loop capability is claimed but the feedback mechanisms and adaptation strategies are not detailed. The cross-domain applicability is asserted but domain-specific requirements and customization points are not identified.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic on root cause analysis in cloud-native systems using temporal and dependency analysis. The proposed framework includes graph-based dependency reasoning as one of its five core layers, which directly relates to the dependency analysis component of the thesis. However, the paper does not specifically focus on root cause analysis as a distinct problem but rather embeds it within a broader operational intelligence framework. The temporal dimension is implicit in the continuous monitoring and learning-based anomaly detection but is not explicitly addressed as temporal causal analysis or temporal failure propagation. The paper's emphasis on moving from reactive alerting to evidence-based adaptation aligns with the thesis goal of systematic root cause identification, but the architectural perspective is more general than the specific RCA focus. The cross-domain nature of the framework may be too broad compared to the thesis focus on cloud-native systems specifically. The lack of empirical validation and concrete methods limits its direct applicability as a reference for implementing temporal and dependency analysis techniques for RCA.
