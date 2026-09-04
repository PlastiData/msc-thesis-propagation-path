---
paper_id: 288
title: Incident Diagnosing and Reporting System Based on Retrieval Augmented Large Language Model
authors:
  - Peng Yuan
  - Lu-An Tang
  - Yanchi Liu
  - Yuji Kobayashi
  - Moto Sato
  - Haifeng Chen
year: 2025
venue: AAAI Conference on Artificial Intelligence
doi: 10.1609/aaai.v39i28.35379
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/120996efb7374dae87a14483ef9d186e75c117d2"
pdf_path: data/pdfs/paper_288.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - observability_data_analysis

method:
  family: llm
  specific: Retrieval Augmented Generation (RAG) with Large Language Model
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
  primary_contribution: A retrieval-augmented LLM system that automatically diagnoses IoT incidents and generates reports by retrieving relevant system documentation and analyzing sensor anomalies.
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

IoT systems generate abnormal sensor records that require analysis and incident reporting for maintenance purposes. Traditionally this analysis is performed manually by domain experts, making it a labor-intensive process. The challenge of applying LLMs to automate this task stems from two fundamental issues. First, LLMs lack the specific background knowledge about deployed IoT systems, including their architecture, component relationships, and operational characteristics. Second, IoT incidents are complex events that involve multiple sensors and components with intricate relationships, requiring the model to understand these dependencies for accurate diagnosis. Without addressing these gaps, LLMs cannot effectively perform root cause analysis or generate meaningful incident reports for IoT maintenance.

## Method summary

RAIDR combines retrieval augmented generation with large language models to automate incident diagnosis and reporting. The system first processes incident features from abnormal sensor records. It then retrieves relevant system documentation based on these features, which provides the necessary background knowledge about the IoT deployment. The retrieved documents are used to augment the LLM's context, enabling it to understand the specific system architecture and sensor relationships. The LLM then analyzes the anomalies by considering both the incident data and the retrieved documentation. Through this augmented understanding, the system identifies root causes of the incidents and automatically generates comprehensive incident reports. The retrieval mechanism addresses the knowledge gap while the LLM's reasoning capabilities handle the complexity of multi-sensor incidents.

## Ground truth and evaluation

The paper does not provide detailed information about ground truth sources or evaluation methodology. The abstract mentions that the system streamlines decision making for system maintenance and troubleshooting, suggesting practical deployment considerations. However, specific details about how the system's diagnoses were validated, what datasets were used for evaluation, or how the generated incident reports were assessed for accuracy are not included in the provided abstract. The evaluation approach, including whether expert-labeled incidents were used as ground truth or how the quality of root cause identification was measured, remains unspecified in the available material.

## Stated limitations

The abstract does not explicitly state limitations of the RAIDR system. No discussion is provided regarding potential failure modes, scalability constraints, or scenarios where the retrieval augmented approach might struggle. The paper does not acknowledge challenges in retrieval quality, potential hallucination issues with LLMs, or limitations in handling novel incident types not covered by existing documentation. There is no mention of computational costs, latency requirements for real-time incident response, or the system's dependence on documentation quality and completeness.

## Gaps this paper opens

The lack of detailed evaluation methodology creates uncertainty about the system's actual performance in production IoT environments. The paper does not address how the system handles incidents that span multiple subsystems or how it prioritizes among multiple potential root causes. The retrieval mechanism's effectiveness when documentation is incomplete, outdated, or contradictory remains unexplored. How the system manages temporal aspects of incidents, such as failure propagation sequences or time-dependent sensor relationships, is not discussed. The integration between retrieved documentation and real-time sensor data analysis needs further investigation. Questions remain about how the system adapts to evolving IoT deployments and whether it can learn from past incident resolutions.

## Relevance to the thesis topic

RAIDR addresses root cause analysis in distributed systems using LLM-based approaches, making it adjacent to the thesis focus on cloud-native systems. While the paper targets IoT rather than cloud-native environments, both domains share challenges of analyzing complex multi-component failures. The retrieval augmented approach offers insights into incorporating system knowledge for RCA, which is relevant for understanding cloud service dependencies. However, the paper does not emphasize temporal analysis or explicit dependency modeling, which are central to the thesis framework. The IoT context differs from cloud-native systems in terms of failure patterns, observability data types, and operational characteristics. The LLM-based methodology represents an alternative approach to the thesis's temporal and dependency analysis framework, useful for comparison but not directly applicable to the proposed framework's core mechanisms.
