---
paper_id: 316
title: The Multi-Agent Fault Localization System Based on Monte Carlo Tree Search Approach
authors:
  - Rui Ren
year: 2025
venue: arXiv.org
doi: 10.48550/arXiv.2507.22800
arxiv_id: 2507.22800
url: "https://www.semanticscholar.org/paper/c7d58cc7b35569a6d01a95f23e81bf86e6b2b91b"
pdf_path: data/pdfs/paper_316.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - llm_based_rca
  - service_dependency_topology

method:
  family: hybrid
  specific: Monte Carlo Tree Search with LLM agents and rule-based rewards
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
  primary_contribution: A multi-agent LLM system using Monte Carlo Tree Search and knowledge base rewards for service-by-service root cause localization that reduces context window requirements and mitigates hallucinations.
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

Microservice architectures present significant challenges for root cause analysis due to their highly decoupled and flexible nature, leading to frequent incidents that require rapid identification and recovery. Existing LLM-based RCA frameworks that rely on approaches like ReAct and Chain-of-Thought suffer from two critical problems. First, LLM hallucinations combined with the propagation nature of anomalies frequently produce incorrect localization results. Second, large complex systems generate massive amounts of anomalous information that exceed the context window limitations of current LLMs, making it difficult to process all relevant data simultaneously. These limitations prevent effective root cause localization in real-world microservice environments where both accuracy and scalability are essential.

## Method summary

KnowledgeMind is a multi-agent LLM system that employs Monte Carlo Tree Search to guide the root cause localization process through service-by-service exploration. The system uses multiple LLM agents that traverse the service dependency graph in a structured manner, evaluating each service as a potential root cause candidate. A knowledge base reward mechanism provides real-time feedback during the search process, using rule-based evaluations to score different exploration paths. This reward mechanism helps guide the MCTS algorithm toward more promising service candidates while penalizing paths that lead to hallucinated or inconsistent conclusions. The service-by-service exploration strategy breaks down the analysis into smaller focused investigations rather than attempting to process all system information at once. The MCTS framework balances exploration of new service paths with exploitation of promising leads based on accumulated rewards.

## Ground truth and evaluation

The paper reports comparative evaluation against state-of-the-art LLM-based RCA methods, showing improvements in root cause localization accuracy ranging from 49.29% to 128.35%. The evaluation demonstrates that the proposed method requires only one-tenth of the context window size compared to existing approaches. The paper does not explicitly detail the source of ground truth labels, the specific benchmark datasets used, or the evaluation metrics beyond accuracy improvements. No information is provided about the number of test cases, the types of faults evaluated, or whether the evaluation used synthetic or real-world incident data. The comparison focuses on demonstrating superiority over SOTA LLM-based RCA frameworks but lacks details about the experimental setup and validation methodology.

## Stated limitations

The paper does not explicitly state limitations of the proposed approach. No discussion is provided regarding computational overhead of running Monte Carlo Tree Search with multiple LLM agents, potential latency in real-time incident response scenarios, or scalability constraints for extremely large microservice systems. The paper does not address how the rule-based reward mechanism is constructed or maintained, whether it requires domain expertise to configure, or how it generalizes across different system architectures. There is no mention of failure cases where the MCTS approach might struggle or scenarios where the service-by-service exploration strategy might miss root causes that require holistic system-level reasoning.

## Gaps this paper opens

The paper introduces Monte Carlo Tree Search for RCA but does not explain how the search space is constructed from service dependencies or how the tree structure maps to the microservice topology. The knowledge base reward mechanism is mentioned as rule-based but the specific rules, their design principles, and how they encode expert knowledge remain unspecified. The interaction between multiple LLM agents is not detailed, including how agents coordinate, share information, or resolve conflicting hypotheses during exploration. The paper claims to address context window limitations but does not describe how information from previously explored services is retained or summarized for subsequent reasoning steps. The relationship between the MCTS exploration strategy and temporal propagation patterns of failures is unexplored, leaving unclear whether the method can effectively capture time-dependent causal relationships.

## Relevance to the thesis topic

This paper is highly relevant as it directly addresses root cause analysis in cloud-native microservice systems using a novel combination of LLM-based reasoning and structured search. The service-by-service exploration approach aligns with dependency analysis by traversing service relationships, though the paper lacks explicit discussion of how service topology is modeled or utilized. The MCTS framework provides a systematic way to navigate the space of potential root causes, which could complement temporal analysis methods by providing a structured exploration strategy. The hybrid approach combining LLM capabilities with rule-based rewards demonstrates how to mitigate common LLM limitations in RCA tasks. However, the paper's lack of detail on temporal aspects and failure propagation patterns means it does not directly contribute to understanding time-based causal relationships. The work is most relevant for understanding how to structure LLM-based reasoning in complex distributed systems and how to reduce computational requirements through focused exploration strategies.
