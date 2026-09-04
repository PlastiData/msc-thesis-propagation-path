---
paper_id: 238
title: "ErrorPrism: Reconstructing Error Propagation Paths in Cloud Service Systems"
authors:
  - Junsong Pu
  - Yichen Li
  - Zhuangbin Chen
  - Jinyang Liu
  - Zhihan Jiang
  - Jianjun Chen
  - Rui Shi
  - Zibin Zheng
  - Tieying Zhang
year: 2025
venue: International Conference on Automated Software Engineering
doi: 10.1109/ASE63991.2025.00292
arxiv_id: 2509.26463
url: "https://www.semanticscholar.org/paper/9ed46463e0245a467000b3267b79223e1bc86428"
pdf_path: data/pdfs/paper_238.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - llm_based_rca

method:
  family: hybrid
  specific: static analysis with LLM-guided backward search
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
  primary_contribution: A hybrid approach combining static code analysis with LLM-based iterative backward search to reconstruct multi-hop error propagation paths from log messages in microservice systems.
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

Modern cloud service systems built on microservice architectures face significant reliability management challenges due to cascading failures. When errors occur, developers commonly employ error wrapping practices that add contextual information at each layer of the function call stack, creating error chains that trace failures from their technical origins to their business-level impacts. While this practice enriches error information, it creates a substantial traceability problem when operators need to reconstruct the complete error propagation path from a final log message back to its root cause. Existing approaches fail to effectively address this reconstruction problem, leaving operators without automated tools to trace errors through multiple service hops and function calls. The challenge is compounded by the complexity of production microservice systems where errors can propagate through numerous services and layers before manifesting in observable logs.

## Method summary

ErrorPrism employs a two-stage hybrid approach to reconstruct error propagation paths. In the first stage, the system performs static analysis on service code repositories to construct a function call graph that captures the structural relationships between functions across the microservice system. This stage also maps log strings to candidate functions that could have generated them, effectively pruning the search space for subsequent analysis. The static analysis creates a foundation by identifying potential paths through the codebase based on code structure alone. In the second stage, ErrorPrism deploys an LLM agent that performs iterative backward search starting from the logged error message. The LLM agent uses the pre-computed function call graph and candidate function mappings to guide its search, reasoning about which functions in the call chain are most likely to have participated in the error propagation. This iterative process continues backward through the call stack until the agent identifies the root cause function where the error originated.

## Ground truth and evaluation

The evaluation uses 102 real-world errors collected from 67 production microservices deployed at ByteDance. These errors represent actual failures that occurred in production systems, providing authentic test cases for the reconstruction task. The ground truth for each error consists of the complete, verified error propagation path from the root cause function to the final logged message. ErrorPrism achieves 97.0% accuracy in correctly reconstructing these paths, demonstrating substantial improvement over baseline approaches. The evaluation compares ErrorPrism against pure static analysis methods and standalone LLM-based approaches, showing that the hybrid combination outperforms either technique used independently. The production setting at ByteDance provides realistic complexity including diverse programming patterns, multiple service interactions, and varied error-wrapping practices.

## Stated limitations

The paper does not explicitly enumerate limitations of the ErrorPrism approach. However, the method's reliance on static analysis implies potential challenges with dynamically generated code or reflection-based patterns that cannot be captured in the static call graph. The LLM component introduces non-determinism and potential variability in results depending on model capabilities and prompt engineering. The evaluation focuses on a single organization's microservice ecosystem at ByteDance, which may not fully represent the diversity of error-handling patterns across different development cultures and technology stacks. The 97.0% accuracy, while high, indicates that approximately 3% of cases remain unsolved, suggesting scenarios where the current approach fails.

## Gaps this paper opens

The work reveals the need for better understanding of how error propagation patterns vary across different programming languages and frameworks beyond those used at ByteDance. The hybrid approach suggests opportunities for exploring other combinations of static and dynamic analysis techniques that might improve accuracy further or reduce computational costs. The reliance on LLM agents raises questions about interpretability and explainability of the reconstruction process, particularly for the 3% of cases where ErrorPrism fails. There is no discussion of how the approach handles concurrent or asynchronous error propagation, which are common in cloud-native systems. The paper does not address temporal aspects of error propagation, such as timing delays between error occurrence and manifestation, which could be crucial for understanding cascading failures. Finally, the work focuses on reconstruction after errors occur but does not explore predictive capabilities for anticipating error propagation before failures manifest.

## Relevance to the thesis topic

ErrorPrism directly addresses root cause analysis in cloud-native microservice systems, making it highly relevant to the thesis topic. The paper's focus on reconstructing error propagation paths aligns with the thesis emphasis on understanding failure propagation through system dependencies. The hybrid approach combining static dependency analysis with iterative reasoning demonstrates how service dependency topology can be leveraged for RCA, which parallels the thesis framework's dependency analysis component. However, ErrorPrism differs from the thesis focus in its treatment of temporal aspects. The paper primarily addresses structural propagation through code call chains rather than temporal propagation through time-series observability data. The static call graph captures spatial dependencies but not temporal ordering or timing relationships between failures. ErrorPrism's focus on code-level error chains complements but does not directly overlap with temporal causal analysis of metrics and traces. The LLM-based component provides insights into how large language models can enhance RCA processes, relevant to the thesis exploration of modern techniques. The production evaluation at scale demonstrates practical applicability, which is valuable for understanding real-world RCA requirements in cloud-native environments.
