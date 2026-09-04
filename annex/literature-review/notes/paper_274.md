---
paper_id: 274
title: Automated Root Causing of Cloud Incidents using In-Context Learning with GPT-4
authors:
  - Xuchao Zhang
  - Supriyo Ghosh
  - Chetan Bansal
  - Rujia Wang
  - Ming-Jie Ma
  - Yu Kang
  - S. Rajmohan
year: 2024
venue: SIGSOFT FSE Companion
doi: 10.1145/3663529.3663846
arxiv_id: 2401.13810
url: "https://www.semanticscholar.org/paper/7030cc233f6ba06d1f9ae0079197da7860e5ba23"
pdf_path: data/pdfs/paper_274.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - observability_data_analysis

method:
  family: llm
  specific: GPT-4 with in-context learning and few-shot prompting
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
  primary_contribution: An in-context learning approach using GPT-4 for automated root cause analysis of cloud incidents that avoids fine-tuning costs while outperforming fine-tuned models.
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

Root cause analysis in cloud services requires on-call engineers to manually diagnose incidents by identifying primary issues and implementing corrective actions. This process is time-consuming and contributes to service downtime and customer impact. While recent large language models like GPT-4 show promise for AIOps tasks, their massive size creates significant challenges for fine-tuning on user data. Fine-tuning requires substantial GPU resources and continuous retraining as new incident data emerges, making it impractical for production deployment at scale. The need exists for an approach that can leverage the capabilities of large language models without incurring the high computational and maintenance costs associated with fine-tuning.

## Method summary

The approach uses GPT-4 with in-context learning to perform root cause analysis without any model fine-tuning. The method constructs prompts that include relevant examples of past incidents and their root causes as context, allowing the model to learn the task from these examples at inference time. The system takes incident data as input and generates root cause explanations by leveraging the few-shot learning capabilities of GPT-4. The in-context learning paradigm provides the model with demonstration examples within the prompt itself, enabling it to understand the structure and requirements of the RCA task without parameter updates. This approach eliminates the need for gradient-based training while still allowing the model to adapt to the specific characteristics of cloud incident data through carefully selected contextual examples.

## Ground truth and evaluation

The evaluation uses over 100,000 production incidents from Microsoft cloud services. Ground truth consists of actual root causes identified and documented by incident owners during real incident resolution processes. The study compares multiple large language models using several metrics to assess performance. Human evaluation is conducted with actual incident owners who assess the generated root causes for correctness and readability. The human evaluators compare outputs from the in-context learning approach against fine-tuned models and zero-shot baselines. Results show the in-context learning approach achieves 24.8% improvement over fine-tuned GPT-3 across all metrics and 49.7% improvement over zero-shot models. Human evaluation demonstrates 43.5% improvement in correctness and 8.7% enhancement in readability compared to fine-tuned models.

## Stated limitations

The paper does not explicitly enumerate technical limitations of the approach. The abstract focuses on presenting the positive results and improvements over baseline methods. While the paper mentions the challenges of fine-tuning large models that motivated the work, it does not discuss potential drawbacks or failure modes of the in-context learning approach itself. The scope is limited to demonstrating effectiveness on Microsoft cloud incidents, but generalization to other cloud environments or incident types is not addressed. The paper does not discuss computational costs of inference with GPT-4 compared to smaller fine-tuned models, nor does it address potential issues with prompt engineering or example selection strategies.

## Gaps this paper opens

The paper does not explain how relevant examples are selected for in-context learning, leaving open questions about retrieval strategies and similarity metrics for matching new incidents to historical examples. The relationship between incident characteristics and model performance remains unexplored, raising questions about which types of incidents benefit most from this approach. The paper does not address how the system handles novel failure modes or incidents that differ significantly from historical examples in the context. Integration with existing observability data such as metrics, logs, and traces is not discussed, leaving unclear how multi-modal incident information could enhance the approach. The temporal aspects of incident evolution and how root causes propagate through service dependencies are not considered in the evaluation or methodology.

## Relevance to the thesis topic

This paper is highly relevant as it addresses automated root cause analysis in cloud systems using modern language models. The work demonstrates that LLMs can effectively analyze incident data to identify root causes, which aligns with the thesis goal of developing an RCA framework. However, the approach treats incidents as isolated text analysis problems without explicitly modeling temporal patterns or service dependencies. The thesis framework aims to incorporate temporal causal analysis and dependency topology, which could complement this LLM-based approach by providing structured context about how failures propagate through time and across services. The in-context learning paradigm could potentially be enhanced by incorporating temporal failure patterns and dependency graphs as additional context, bridging the gap between pure text-based analysis and structured system understanding. The evaluation methodology using production incidents provides a valuable reference for assessing RCA approaches in real-world settings.
