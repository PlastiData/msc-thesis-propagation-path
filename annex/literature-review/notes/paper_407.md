---
paper_id: 407
title: "E2E-REME: Towards End-to-End Microservices Auto-Remediation via Experience-Simulation Reinforcement Fine-Tuning"
authors:
  - Lingzhe Zhang
  - Yunpeng Zhai
  - Tong Jia
  - Minghua He
  - Chiming Duan
  - Zhaoyang Liu
  - Bolin Ding
  - Ying Li
year: 2026
venue: ""
doi: ""
arxiv_id: 2604.11094
url: "https://www.semanticscholar.org/paper/59d7860583287a005ac18d8b68c12fff0759e694"
pdf_path: data/pdfs/paper_407.pdf
read_date: 2026-05-11

category:
  - recommendation_and_remediation
  - llm_based_rca
  - benchmark_and_evaluation

method:
  family: llm
  specific: reinforcement fine-tuning on smaller LLM with experience simulation
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
  primary_contribution: An end-to-end auto-remediation system that generates executable Ansible playbooks directly from diagnosis reports using a reinforcement fine-tuned LLM, along with a benchmark for automated evaluation.
  novelty_strength: strong

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

Contemporary microservice systems exhibit increasing scale and complexity, resulting in frequent and costly failures that require rapid remediation. Existing LLM-based auto-remediation approaches face significant limitations in their operational effectiveness. These approaches primarily function as translation systems that convert textual instructions into executable Ansible playbooks, relying heavily on expert-crafted prompts to guide the generation process. They lack integration of runtime knowledge and system state information that could inform remediation decisions. The dependence on large-scale general-purpose language models creates barriers to both accuracy and efficiency in production environments. Current methods do not provide end-to-end automation from fault diagnosis to system restoration, requiring human intervention at multiple stages of the remediation pipeline.

## Method summary

E2E-REME introduces an end-to-end microservice remediation approach that directly generates executable Ansible playbooks from diagnosis reports without intermediate human intervention. The system employs experience-simulation reinforcement fine-tuning to train a specialized language model for remediation tasks. Rather than relying on general-purpose LLMs with expert-crafted prompts, the method fine-tunes a model specifically for the remediation domain using reinforcement learning signals derived from simulated execution experiences. The training process incorporates feedback from actual playbook execution outcomes in controlled environments, allowing the model to learn effective remediation strategies through trial and error. This approach enables the model to internalize runtime knowledge and system-specific patterns that guide playbook generation. The system operates autonomously from receiving a diagnosis report through generating the playbook and executing it to restore the faulty microservice system.

## Ground truth and evaluation

The paper introduces MicroRemed, a comprehensive benchmark designed to enable rigorous evaluation of auto-remediation systems. This benchmark automates the complete remediation pipeline including microservice deployment, failure injection, playbook execution, and post-repair verification. The automated nature of MicroRemed allows for systematic testing across multiple failure scenarios without manual intervention. Experiments are conducted on both public microservice platforms and industrial systems to validate the approach across different deployment contexts. The evaluation compares E2E-REME against nine representative LLMs, measuring both accuracy of generated playbooks and efficiency of the remediation process. The benchmark provides standardized metrics for assessing whether generated playbooks successfully restore system functionality after injected failures. Post-repair verification mechanisms confirm that the microservice system returns to correct operational state following playbook execution.

## Stated limitations

The paper does not explicitly enumerate limitations of the proposed approach in a dedicated section. However, the problem statement implicitly acknowledges that the system operates within the context of microservice architectures and requires diagnosis reports as input, suggesting dependency on upstream diagnostic capabilities. The reliance on Ansible as the execution framework constrains the types of remediation actions that can be performed to those expressible in Ansible playbook syntax. The reinforcement fine-tuning approach requires access to simulation environments where playbooks can be safely executed and their outcomes observed, which may limit applicability in environments where such simulation infrastructure is unavailable or expensive to maintain.

## Gaps this paper opens

The paper focuses exclusively on the remediation phase assuming diagnosis reports are already available, leaving open questions about integration with upstream root cause analysis systems. The experience-simulation reinforcement fine-tuning methodology requires further investigation regarding how much simulation data is needed for effective training and how well models generalize to novel failure types not encountered during training. The relationship between diagnosis report quality and remediation success remains unexplored, particularly regarding what level of diagnostic detail is necessary for accurate playbook generation. The paper does not address how the system handles cases where multiple remediation strategies might be valid or how it prioritizes among competing repair actions. Questions remain about the system's behavior when facing cascading failures or situations where initial remediation attempts fail and iterative refinement is necessary.

## Relevance to the thesis topic

This paper addresses the remediation phase that follows root cause analysis rather than the RCA process itself, making it adjacent to the thesis focus on temporal and dependency-based root cause analysis in cloud-native systems. The work demonstrates how diagnosis outputs can be automatically translated into corrective actions, providing context for what downstream systems expect from RCA components. The benchmark methodology in MicroRemed offers insights into automated evaluation approaches that could be adapted for assessing RCA accuracy by measuring whether identified root causes lead to successful remediation. The emphasis on microservice architectures and the integration of runtime knowledge aligns with cloud-native system characteristics central to the thesis. While E2E-REME does not perform temporal or dependency analysis for fault localization, it operates on systems where such analysis would be prerequisite, suggesting potential integration points between RCA frameworks and auto-remediation systems.
