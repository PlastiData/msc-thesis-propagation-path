---
paper_id: 405
title: "PRAXIS: Integrating Program Analysis with Observability for Root-Cause Analysis"
authors:
  - Shengkun Cui
  - R. Krishna
  - Saurabh Jha
  - Ravi Iyer
year: 2025
venue: ""
doi: ""
arxiv_id: 2512.22113
url: "https://www.semanticscholar.org/paper/c3039b7de36a9b759dfd0850dce107c91a0b40de"
pdf_path: data/pdfs/paper_405.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - llm_based_rca

method:
  family: hybrid
  specific: LLM-driven structured graph traversal over SDG and PDG
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
  primary_contribution: An orchestrator that combines LLM-based reasoning with program analysis artifacts (service dependency graphs and program dependence graphs) to diagnose code and configuration issues in cloud incidents through structured agentic workflows.
  novelty_strength: strong

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

Production cloud incidents remain extremely costly, with unresolved incidents averaging over $2M per hour in losses. The challenge lies in diagnosing root causes that stem from code-level and configuration-level issues within complex microservice architectures. Traditional approaches struggle to bridge the gap between high-level service dependencies and low-level code dependencies, making it difficult to pinpoint the exact location and nature of faults. Existing LLM-based methods often lack structure in their reasoning process, leading to inefficient token usage and lower diagnostic accuracy. The need exists for a systematic approach that can traverse both service-level and code-level dependency structures to identify root causes efficiently and accurately.

## Method summary

PRAXIS operates as an orchestrator that manages an agentic workflow combining LLM reasoning with static program analysis artifacts. The system employs two complementary graph structures: a service dependency graph that captures microservice-level relationships and a hammock-block program dependence graph that represents code-level dependencies within each microservice. The LLM performs structured traversal over these graphs, moving from service-level analysis down to code-level investigation. The hammock-block PDG representation provides a more manageable abstraction of program dependencies compared to traditional control-flow or data-flow graphs. The orchestrator guides the LLM through a systematic diagnostic process, constraining the search space while allowing the model to leverage its reasoning capabilities. This hybrid approach combines the structural guarantees of program analysis with the flexibility of LLM-based inference.

## Ground truth and evaluation

The paper evaluates PRAXIS on a set of 30 comprehensive real-world incidents that the authors are compiling into an RCA benchmark. The evaluation compares PRAXIS against state-of-the-art ReAct baselines, measuring both RCA accuracy and token consumption. PRAXIS demonstrates up to 6.3x improvement in RCA accuracy while reducing token consumption by 5.3x compared to the baselines. The ground truth for these incidents appears to be derived from actual production cloud failures, though the paper does not explicitly detail how the correct root causes were determined or validated. The benchmark being compiled suggests an effort to create standardized evaluation criteria for root cause analysis systems. The metrics focus on both effectiveness (accuracy) and efficiency (token usage), reflecting practical deployment considerations.

## Stated limitations

The paper does not explicitly enumerate limitations in the provided abstract. However, several implicit constraints can be inferred from the methodology. The approach requires static program analysis artifacts to be available, which necessitates access to source code and the ability to construct program dependence graphs for each microservice. The focus on code and configuration issues means the system may not address other types of cloud incidents such as hardware failures, network issues, or resource exhaustion problems. The reliance on LLM reasoning introduces potential variability and the need for careful prompt engineering. The evaluation on 30 incidents, while comprehensive, represents a limited sample size for generalizing performance across diverse cloud environments and failure modes.

## Gaps this paper opens

The integration of program analysis with LLM-based reasoning opens questions about how to optimally balance static and dynamic analysis approaches. The hammock-block PDG representation suggests opportunities to explore other program abstraction techniques that might further improve efficiency or accuracy. The paper does not address how temporal aspects of incident evolution are incorporated into the analysis, leaving open questions about handling time-series observability data. The relationship between service dependency graphs and temporal failure propagation patterns remains unexplored. The benchmark being compiled raises questions about standardization and reproducibility in RCA evaluation, including how to capture sufficient context from real incidents. The approach's applicability to runtime-only issues that do not manifest in static code analysis requires further investigation.

## Relevance to the thesis topic

PRAXIS is highly relevant to the thesis topic as it directly addresses root cause analysis in cloud-native systems through dependency analysis. The service dependency graph component aligns with the thesis focus on service topology and dependency relationships. However, PRAXIS emphasizes static program-level dependencies rather than temporal analysis of failure propagation, representing a complementary but distinct approach. The thesis topic's emphasis on temporal analysis suggests examining how incidents evolve over time through dependency chains, while PRAXIS focuses on static structural relationships augmented with LLM reasoning. The integration of multiple graph types (service and program level) provides a model for multi-level dependency analysis that could inform the thesis framework. The hybrid methodology combining structured artifacts with flexible reasoning demonstrates how different analysis paradigms can be orchestrated. The benchmark development effort is particularly relevant for establishing evaluation standards that the thesis work could adopt or extend.
