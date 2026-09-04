---
paper_id: 401
title: Evaluating scalability and performance in microservices-based web systems through observability
authors:
  - Thao Ho
year: 2026
venue: Trepo - Institutional Repository of Tampere University
doi: ""
arxiv_id: ""
url: "https://openalex.org/W7139697155"
pdf_path: data/pdfs/paper_401.pdf
read_date: 2026-05-11

category:
  - observability_data_analysis
  - distributed_system_monitoring
  - benchmark_and_evaluation

method:
  family: other
  specific: systematic literature review with tool evaluation framework
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
  primary_contribution: A systematic evaluation framework for assessing observability and load testing tools in microservices architectures, identifying integration benefits and research gaps.
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

Microservices architectures have become widely adopted for web systems due to their flexibility and scalability advantages over monolithic designs. However, this architectural shift introduces significant complexity in monitoring and maintaining system performance. The increasing interdependencies between services create challenges in ensuring system resilience and understanding performance characteristics. Traditional monitoring approaches prove insufficient for capturing the distributed nature of microservices interactions. Organizations need robust observability strategies that can handle the complexity of service-to-service communication, provide visibility into request flows across multiple services, and enable proactive performance evaluation. The thesis addresses the question of how integrating observability and load testing tools can enhance the ability to assess and maintain scalability and performance in microservices-based applications.

## Method summary

The thesis employs a systematic literature review methodology to evaluate research on microservices monitoring, tracing, visualization, and load testing. Four specific open-source tools are selected for detailed analysis based on their industry prevalence and complementary functionalities: Prometheus for real-time metrics collection, Grafana for visualization, Jaeger for distributed tracing, and k6 for load testing. The evaluation framework applies multiple criteria including integration ease, metrics collection capabilities, scalability support, visualization usability, operational overhead, and licensing flexibility. The analysis examines how these tools can be combined into a cohesive observability pipeline rather than used in isolation. The methodology focuses on understanding the practical benefits of tool integration and identifying gaps in current observability practices for microservices environments.

## Ground truth and evaluation

The thesis does not employ empirical ground truth in the traditional sense of experimental validation. Instead, the evaluation relies on a systematic review of existing research literature and documented tool capabilities. The assessment framework uses qualitative criteria to evaluate each tool's characteristics and their integration potential. The findings are based on analyzing published research, tool documentation, and reported industry practices rather than conducting original experiments with controlled failure injection or performance benchmarks. The evaluation of tool effectiveness is derived from synthesizing existing evidence about their deployment in microservices environments and their documented capabilities for addressing observability challenges.

## Stated limitations

The thesis explicitly acknowledges that no single tool provides a comprehensive observability solution for microservices architectures. The research identifies several gaps in current observability practices. Enhanced automation in observability workflows remains insufficient in existing tools. Tighter integration between observability systems and orchestration platforms like Kubernetes is needed but not fully realized. The application of machine learning techniques for predictive scaling and anomaly detection represents an underdeveloped area. The thesis recognizes that while the selected tools offer complementary functionalities, achieving a truly cohesive observability pipeline requires additional integration effort and customization beyond out-of-the-box capabilities.

## Gaps this paper opens

The thesis identifies several critical research directions that remain underexplored. The need for enhanced automation in observability workflows suggests opportunities for developing intelligent systems that can automatically configure monitoring, adjust collection parameters, and respond to detected issues. The gap in integration between observability and orchestration platforms points to research opportunities in creating feedback loops where monitoring insights directly influence scaling and deployment decisions. The identified need for machine learning-based predictive scaling and anomaly detection opens avenues for research into automated root cause analysis and proactive failure prevention. The thesis also implicitly highlights the challenge of creating unified observability solutions that reduce the operational complexity of managing multiple specialized tools while maintaining their individual strengths.

## Relevance to the thesis topic

This work is adjacent to the thesis topic on root cause analysis in cloud-native systems using temporal and dependency analysis. The thesis provides important context on observability infrastructure that enables root cause analysis but does not directly address causal reasoning or automated diagnosis. The evaluation of Jaeger for distributed tracing is relevant as tracing data captures service dependencies and temporal relationships between requests. The discussion of metrics collection through Prometheus relates to the observability data sources needed for temporal analysis. However, the thesis focuses on tool evaluation and integration rather than developing methods for analyzing temporal patterns or dependency relationships to identify root causes. The identified gaps around machine learning for anomaly detection and the need for tighter integration between monitoring and orchestration align with challenges in building automated root cause analysis systems. The work establishes the observability foundation upon which root cause analysis techniques must operate.
