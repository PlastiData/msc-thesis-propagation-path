---
paper_id: 121
title: Efficient Fault Localization in a Cloud Stack Using End-to-End Application Service Topology
authors:
  - Dhanya R Mathews
  - Mudit Verma
  - Pooja Aggarwal
  - J. Lakshmi
year: 2025
venue: ArXiv.org
doi: 10.48550/arxiv.2509.05511
arxiv_id: ""
url: "https://openalex.org/W4414763660"
pdf_path: data/pdfs/paper_121.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - observability_data_analysis

method:
  family: hybrid
  specific: topology-aware causal analysis with metric selection
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
  primary_contribution: A topology-aware root cause detection method that selects informative metrics across the cloud stack and incorporates end-to-end service topology to improve fault localization accuracy and efficiency.
  novelty_strength: moderate

limitations_authors_state: []

quality_flags:
  self_constructed_ground_truth: false
  comparison_table_only: false
  hobby_project_scale: false
  predictable_outcome: false

relevance:
  relevance_to_topic: core
  must_cite: false
---

## Problem statement

Cloud application services built on microservice architectures generate massive amounts of observability data across distributed components spanning the entire cloud stack. This volume of data makes it challenging to react to anomalies and restore service quality in real time. The problem is compounded by the need to identify which observability metrics are most informative for root cause analysis from among the many available metrics across infrastructure, platform, and application layers. Existing root cause detection approaches do not adequately leverage the end-to-end application service topology to guide metric selection and fault localization. Without considering how components relate to each other through the service topology, root cause analysis becomes inefficient and less accurate, particularly as the number of service components increases with microservice adoption.

## Method summary

The approach consists of two main components. First, a metric selection method uses the application service topology to identify the most informative metrics across the cloud stack. This selection process considers the relationships between components in the end-to-end service delivery path to filter the observability data. Second, the paper proposes Topology-Aware Root Cause Detection (TA-RCD), which enhances existing causal analysis methods by incorporating the service topology directly into the root cause localization process. TA-RCD builds upon a state-of-the-art RCD algorithm but adds topology awareness to improve both accuracy and efficiency. The method operates across multiple layers of the cloud stack, including application, platform, and infrastructure components, ensuring that the analysis considers dependencies throughout the entire service delivery chain. The topology information guides the causal analysis to focus on components and metrics that are most relevant given the structural relationships in the distributed system.

## Ground truth and evaluation

The evaluation uses failure injection studies where faults are deliberately introduced into a cloud application service. The ground truth consists of the known root causes of these injected failures. The paper evaluates performance using Top-3 and Top-5 recall metrics, which measure whether the true root cause appears in the top three or top five ranked results produced by the algorithm. The proposed TA-RCD method is compared against a state-of-the-art RCD algorithm as the baseline. The evaluation demonstrates that TA-RCD performs at least 2X better on average than the baseline in terms of Top-3 and Top-5 recall. The failure injection approach allows for controlled experiments where the actual root cause is known with certainty, enabling quantitative assessment of localization accuracy. The experiments appear to cover multiple types of performance anomalies across different components of the cloud stack.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the reliance on failure injection studies for evaluation implies that the method's performance on real-world production failures with more complex failure modes remains to be validated. The paper focuses on performance anomalies specifically, which suggests that other types of failures may not be addressed by the approach. The requirement to construct and maintain an accurate end-to-end application service topology represents an operational overhead that is not discussed in detail. The scalability of the topology-aware analysis to very large-scale microservice deployments with hundreds or thousands of services is not explicitly evaluated. The paper does not discuss how the method handles dynamic topology changes that occur frequently in cloud-native environments.

## Gaps this paper opens

The paper does not address how to automatically construct and maintain the end-to-end service topology in dynamic cloud environments where services are frequently deployed, updated, and scaled. The temporal aspects of failure propagation through the topology are not explicitly modeled, leaving open questions about how failures cascade over time through dependent services. The method's applicability to different types of anomalies beyond performance issues remains unexplored. There is no discussion of how the approach handles transient failures or intermittent issues that may not have clear causal relationships. The integration of multiple types of observability data beyond metrics, such as logs and traces, is not addressed. The paper does not explore how machine learning could be used to automatically learn which metrics are most informative for different types of failures rather than relying on topology-based selection alone.

## Relevance to the thesis topic

This paper is highly relevant to the thesis topic as it directly addresses root cause analysis in cloud-native systems using dependency analysis through service topology. The emphasis on end-to-end application service topology aligns with the thesis focus on dependency analysis for understanding how components relate and how failures propagate. The metric selection approach based on topology provides insights into identifying relevant observability data for RCA. The topology-aware enhancement of causal analysis methods demonstrates how dependency information can improve root cause localization accuracy and efficiency. However, the paper's limited treatment of temporal aspects represents a gap relative to the thesis emphasis on temporal analysis. The work provides a foundation for understanding how topology can guide RCA but does not fully integrate temporal propagation patterns. The focus on microservice architectures and distributed cloud systems directly matches the cloud-native context of the thesis. The quantitative evaluation methodology and comparison with baseline methods offers useful benchmarking approaches for the thesis work.
