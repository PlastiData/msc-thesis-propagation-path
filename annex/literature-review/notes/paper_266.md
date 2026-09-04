---
paper_id: 266
title: "From Observability Data to Diagnosis: An Evolving Multi-agent System for Incident Management in Cloud Systems"
authors:
  - Yu Luo
  - Jiamin Jiang
  - Jingfei Feng
  - Lei Tao
  - Qingliang Zhang
  - Xidao Wen
  - Yongqian Sun
  - Shenglin Zhang
  - Jie Huang
  - N. Qi
  - Dan Pei
year: 2025
venue: arXiv.org
doi: 10.48550/arXiv.2510.24145
arxiv_id: 2510.24145
url: "https://www.semanticscholar.org/paper/a36cb33a369506b95372e31c6b3f9c3d42bf9791"
pdf_path: data/pdfs/paper_266.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - observability_data_analysis

method:
  family: llm
  specific: multi-agent LLM collaboration with self-evolution
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
  primary_contribution: A multi-agent LLM system that converts heterogeneous observability data into structured text and uses agent collaboration with dual self-evolution for incident diagnosis.
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

Incident management in large-scale cloud systems requires on-call engineers to manually examine vast amounts of heterogeneous observability data including metrics, logs, and traces. This manual process is labor-intensive and prone to errors given the scale and complexity of modern cloud infrastructures. Existing automated incident management approaches face three key challenges that limit their practical adoption. First, they struggle to generalize across different systems and deployment contexts. Second, they provide limited interpretability in their diagnostic reasoning, making it difficult for engineers to trust and validate their outputs. Third, they incur high deployment costs, particularly when requiring extensive training data or system-specific customization.

## Method summary

OpsAgent employs a multi-agent architecture built on large language models to perform incident diagnosis. The system begins with a training-free data processor that converts heterogeneous observability data from metrics, logs, and traces into structured textual descriptions suitable for LLM consumption. The core diagnostic engine uses a multi-agent collaboration framework where different agents specialize in analyzing different aspects of the incident and coordinate their findings through structured interactions. This agent-based approach makes the diagnostic reasoning process transparent and auditable by exposing the intermediate steps and rationale. OpsAgent incorporates a dual self-evolution mechanism consisting of internal model updates through fine-tuning on accumulated cases and external experience accumulation through a memory system that stores successful diagnostic patterns. This evolution mechanism allows the system to continuously improve its capabilities over time without requiring manual retraining or reconfiguration.

## Ground truth and evaluation

The system is evaluated on the OPENRCA benchmark, which provides standardized incident scenarios for root cause analysis. The evaluation demonstrates state-of-the-art performance compared to existing automated incident management approaches. The experiments assess four key dimensions: generalizability across different system types, interpretability of diagnostic outputs, cost-efficiency in terms of deployment and operational expenses, and the effectiveness of the self-evolution mechanism over time. The benchmark evaluation shows that OpsAgent achieves superior performance while maintaining practical deployment characteristics. The dual evolution mechanism is validated by demonstrating improved diagnostic accuracy as the system accumulates experience from resolved incidents.

## Stated limitations

The paper does not explicitly enumerate specific limitations of the OpsAgent approach. However, the reliance on large language models implies inherent constraints related to LLM capabilities, including potential hallucination issues, context window limitations for processing very large observability datasets, and dependency on the quality of the underlying language model. The training-free data processor, while reducing deployment costs, may face challenges in handling novel or unexpected data formats that differ significantly from those encountered during system design. The effectiveness of the self-evolution mechanism depends on the quality and diversity of incidents encountered during operation, which may vary across different deployment environments.

## Gaps this paper opens

The paper does not provide detailed analysis of failure modes where the multi-agent system produces incorrect diagnoses or how conflicting agent conclusions are resolved. The relationship between the structured textual representation and the fidelity of the original observability data remains underexplored, particularly regarding information loss during the conversion process. The paper does not discuss how the system handles temporal dependencies and causal relationships in incident propagation across distributed services. The dual evolution mechanism's convergence properties and potential for accumulating incorrect diagnostic patterns over time are not thoroughly examined. The scalability of the multi-agent collaboration framework to very large cloud systems with thousands of services and complex dependency graphs requires further investigation.

## Relevance to the thesis topic

OpsAgent directly addresses root cause analysis in cloud-native systems using observability data, making it highly relevant to the thesis topic. The system processes the three primary types of observability data that the thesis framework would need to analyze: metrics, logs, and traces. However, OpsAgent takes an LLM-based approach rather than focusing on explicit temporal and dependency analysis as the thesis proposes. The multi-agent collaboration provides interpretability but through natural language reasoning rather than through explicit causal graphs or dependency models. The training-free data processor demonstrates one approach to handling heterogeneous observability data, though it converts everything to text rather than preserving temporal sequences or dependency structures. The self-evolution mechanism offers insights into how a root cause analysis system can improve over time, which could inform the thesis framework's design for continuous learning. The work highlights the importance of interpretability and auditability in root cause analysis, principles that should guide the thesis framework's design even if using different technical approaches.
