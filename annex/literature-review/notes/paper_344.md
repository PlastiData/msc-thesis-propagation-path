---
paper_id: 344
title: The case for an internet primitive for fault localization
authors:
  - W. Sussman
  - Emily Marx
  - Venkat Arun
  - Akshay Narayan
  - Mohammad Alizadeh
  - Harinarayanan Balakrishnan
  - Aurojit Panda
  - S. Shenker
year: 2022
venue: ACM Workshop on Hot Topics in Networks
doi: 10.1145/3563766.3564105
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/bbedf183d8c16b64f618a32d11bccdc0ae7d18d0"
pdf_path: data/pdfs/paper_344.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - distributed_system_monitoring
  - observability_data_analysis

method:
  family: other
  specific: cross-layer standardized information interface primitive
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
  primary_contribution: Proposes a standardized Internet-level primitive for fault localization that enables cross-layer, cross-domain, and cross-application visibility through a simple information interface.
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

Modern distributed applications span multiple layers and organizational boundaries including microservices, cloud infrastructure, edge services, network functions, and physical network components. When user-visible faults occur, the first critical step is localizing the fault to determine where it originated. Current approaches fail because no single entity has complete visibility across all these layers and domains. Application operators lack access to network-level information, while network operators cannot see into application-layer behavior. This fragmentation of visibility makes rapid fault localization extremely difficult. The problem is exacerbated by the fact that different organizations control different parts of the infrastructure stack, creating information silos that prevent effective diagnosis. The authors argue that fault localization should be treated as a fundamental Internet primitive rather than an ad-hoc per-application or per-organization solution.

## Method summary

The paper proposes designing a standardized fault localization primitive that would operate across layers, domains, and applications. The primitive would provide a simple and standardized information interface that different entities could use to expose relevant diagnostic information. The approach envisions each component in the stack exposing localization-relevant information through this common interface, enabling queries that traverse organizational and technical boundaries. The primitive would allow operators to quickly narrow down fault locations by querying across the entire application delivery path. The authors suggest this should be built into Internet infrastructure itself rather than relying on proprietary or application-specific solutions. The paper does not provide detailed implementation specifics but rather makes the case for why such a primitive is necessary and feasible. The standardized interface would enable automated tools and human operators to perform systematic fault localization without requiring deep knowledge of every component in the delivery chain.

## Ground truth and evaluation

The paper does not present an implemented system or evaluation with ground truth data. This is a position paper that makes the case for developing such a primitive rather than demonstrating a working solution. The authors do not provide experimental validation, benchmark datasets, or comparison with existing fault localization approaches. No metrics are reported for localization accuracy, time to diagnosis, or system overhead. The paper relies on argumentation and examples of current limitations to motivate the need for the proposed primitive. The lack of evaluation reflects the paper's nature as a vision statement intended to spark discussion and future research rather than a complete technical solution. The authors acknowledge this is a proposal for what should be built rather than a description of what has been built.

## Stated limitations

The paper explicitly acknowledges it is presenting a vision and case for the primitive rather than a complete solution. The authors recognize that defining the exact information interface and standardizing it across diverse stakeholders would be challenging. They note that getting buy-in from multiple organizations and layers of the Internet infrastructure would require significant coordination effort. The paper does not address specific technical challenges such as privacy concerns when exposing diagnostic information across organizational boundaries, potential security implications of standardized fault information interfaces, or the computational overhead of maintaining and querying such information. The authors also do not discuss how to handle cases where organizations may be unwilling to expose internal diagnostic information to external parties. The feasibility of achieving widespread adoption of such a standard across the heterogeneous Internet ecosystem remains an open question that the paper does not fully address.

## Gaps this paper opens

The paper identifies the need for cross-layer and cross-domain fault localization but does not specify what information should be exposed through the standardized interface. The exact design of the primitive including its API, data formats, and query mechanisms remains undefined. How to balance the need for diagnostic visibility with privacy and security concerns is not explored. The paper does not address how such a primitive would integrate with existing observability tools and monitoring systems. Questions about incentive structures for organizations to adopt and maintain such a primitive are left open. The relationship between this proposed primitive and existing distributed tracing systems, logging infrastructure, and metrics collection frameworks is not clarified. How the primitive would handle the dynamic nature of cloud-native systems where components are constantly being created, destroyed, and reconfigured is not discussed. The paper also does not explore how machine learning or automated reasoning could leverage such a primitive for more sophisticated root cause analysis.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic as it addresses fault localization in distributed systems but takes a fundamentally different approach. While the thesis focuses on temporal and dependency analysis for root cause analysis within cloud-native systems, this paper proposes infrastructure-level standardization across organizational boundaries. The paper's emphasis on cross-domain visibility complements the thesis work by highlighting limitations of single-organization observability approaches. The proposed primitive could potentially provide input data for temporal and dependency analysis methods if it were implemented. However, the paper does not engage with specific analytical techniques for root cause analysis such as temporal pattern recognition or dependency graph construction. The vision of standardized fault information interfaces could inform how observability data should be structured and exposed in cloud-native systems. The cross-layer perspective reinforces the importance of considering multiple levels of the system stack when performing root cause analysis, which aligns with comprehensive dependency analysis approaches in the thesis topic.
