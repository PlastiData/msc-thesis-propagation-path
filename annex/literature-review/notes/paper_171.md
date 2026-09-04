---
paper_id: 171
title: Root Cause Analysis for Cloud-Native Applications
authors:
  - Zurkowski Bartosz
  - Krzysztof Zieliński
year: 2024
venue: IEEE Transactions on Cloud Computing
doi: 10.1109/tcc.2024.3358823
arxiv_id: ""
url: "https://openalex.org/W4391305513"
pdf_path: data/pdfs/paper_171.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - temporal_causal_analysis

method:
  family: hybrid
  specific: multi-aspect symptom correlation combining structural, semantic, and temporal analysis
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
  primary_contribution: A hybrid RCA framework that combines structural, semantic, and temporal symptom correlation methods to identify root causes and reconstruct complete fault propagation trajectories in cloud-native applications.
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

Traditional root cause analysis techniques are insufficient for modern cloud-native applications due to their inherent complexity and dynamic nature. Cloud environments exhibit multiple interacting layers including infrastructure, platform services, and application components, making it difficult to trace failures back to their origins. System administrators face challenges in daily incident response routines because conventional approaches fail to capture the multifaceted relationships between symptoms that manifest across different system layers. The problem is further complicated by the need to not only identify the root cause but also reconstruct the complete fault trajectory showing how failures propagate from the initial cause to the observed effects. Existing RCA methods typically focus on single aspects of symptom relationships, such as temporal correlations or structural dependencies, but fail to integrate multiple perspectives necessary for accurate diagnosis in complex cloud systems.

## Method summary

The proposed solution approximates causal symptom dependencies by synergizing multiple correlation methods that evaluate symptoms across three distinct dimensions: structural, semantic, and temporal aspects. The structural analysis examines the architectural relationships between system components using system structure mining techniques. The semantic analysis evaluates the meaning and context of symptoms to identify related failure patterns. The temporal analysis assesses the timing and sequence of symptom occurrences to infer causality. These three correlation methods are integrated into a unified symptom correlation framework that produces a more comprehensive understanding of failure relationships than single-method approaches. The framework constructs RCA model structures that support inference processes for identifying root causes. The root cause identification process uses these integrated correlations to trace failures backward from observed effects through intermediate propagation steps to the originating fault. Statistical methods are combined with behavioral mining to enhance the accuracy of causal inference and enable reconstruction of complete fault trajectories across multiple cloud layers.

## Ground truth and evaluation

The functional evaluation was conducted on a live microservice-based system deployed in a real cloud environment. The paper demonstrates the effectiveness of the approach in identifying root causes of complex failures that span multiple cloud layers including infrastructure, platform, and application tiers. The evaluation focuses on demonstrating that the system can successfully pinpoint failure root causes and recreate complete fault trajectories in realistic scenarios. However, the paper does not provide detailed quantitative metrics such as precision, recall, or accuracy rates for root cause identification. The ground truth for evaluation appears to be derived from known failure scenarios in the live system where the actual root causes could be verified through system knowledge or manual investigation. The evaluation emphasizes functional capability rather than comparative performance against baseline methods or competing approaches.

## Stated limitations

The paper does not explicitly enumerate specific limitations of the proposed approach in a dedicated section. The abstract and methodology suggest that the approach is designed specifically for cloud-native applications, which may imply limited applicability to other system types. The reliance on multiple correlation methods across structural, semantic, and temporal dimensions suggests potential challenges in scenarios where one or more of these aspects cannot be adequately captured or analyzed. The integration of multiple methods may introduce complexity in tuning and configuration for different cloud environments. The evaluation on a single live microservice system, while demonstrating functional capability, does not address scalability concerns or performance under varying system sizes and failure complexities.

## Gaps this paper opens

The paper does not provide detailed algorithmic specifications or pseudocode for the symptom correlation framework, leaving implementation details unclear for reproduction. The specific mechanisms for weighting or prioritizing different correlation aspects (structural, semantic, temporal) when they provide conflicting signals remain unexplored. The paper lacks quantitative comparison with existing RCA methods, making it difficult to assess relative performance improvements. There is no discussion of how the approach handles dynamic topology changes common in cloud-native systems where services scale or migrate. The semantic analysis component is mentioned but not thoroughly explained, leaving questions about how semantic relationships are extracted and represented. The computational overhead and real-time performance characteristics of running multiple correlation analyses simultaneously are not addressed. The generalizability across different types of cloud-native architectures beyond microservices remains unexamined.

## Relevance to the thesis topic

This paper is directly relevant to the thesis topic as it addresses root cause analysis in cloud-native systems through explicit integration of temporal and dependency analysis. The structural correlation component aligns with dependency analysis by examining architectural relationships between components. The temporal correlation component directly addresses temporal aspects of failure propagation and symptom sequencing. The paper's emphasis on reconstructing complete fault trajectories from root cause to effect demonstrates temporal failure propagation analysis, which is central to the thesis framework. The multi-aspect correlation approach provides a concrete example of how temporal and dependency information can be combined for RCA, offering methodological insights for the thesis framework. The focus on cloud-native microservice architectures matches the thesis domain. However, the paper's lack of detailed algorithmic descriptions and quantitative evaluation metrics highlights areas where the thesis framework could provide more rigorous contributions in terms of formal temporal models and comprehensive benchmark evaluation.
