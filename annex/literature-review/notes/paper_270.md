---
paper_id: 270
title: "StepFly: Agentic Troubleshooting Guide Automation for Incident Diagnosis"
authors:
  - Jiayi Mao
  - Liqun Li
  - Yan Gao
  - Zegang Peng
  - Shilin He
  - Chaoyun Zhang
  - Sijing Qin
  - Samia Khalid
  - Qingwei Lin
  - Saravan Rajmohan
  - S. Lanka
  - Dongmei Zhang
year: 2025
venue: ""
doi: 10.1145/3808143
arxiv_id: 2510.10074
url: "https://www.semanticscholar.org/paper/e0e24f291783b63e12cbbf4907464a1b3be492b9"
pdf_path: data/pdfs/paper_270.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - recommendation_and_remediation
  - llm_based_rca

method:
  family: llm
  specific: GPT-4 with agentic workflow and DAG-based execution scheduling
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
  primary_contribution: An end-to-end agentic framework that automates troubleshooting guide execution through structured DAG extraction, query preparation plugins, and parallel execution scheduling.
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

Large-scale IT systems rely on troubleshooting guides (TSGs) for effective incident management, but manual execution of these guides by site reliability engineers is both time-consuming and prone to errors. Existing LLM-based solutions for automating incident management fail to address several critical challenges specific to TSG execution. These challenges include managing quality issues in TSGs such as ambiguous instructions and missing context, interpreting complex control flow structures with conditional branches and loops, handling data-intensive queries that require accessing multiple data sources, and exploiting opportunities for parallel execution of independent diagnostic steps. The paper identifies that TSGs in production environments often contain unstructured natural language descriptions that are difficult for automated systems to parse and execute reliably.

## Method summary

StepFly employs a three-stage workflow to automate TSG execution. The first stage provides TSG Mentor, a tool that assists SREs in improving TSG quality by identifying and addressing issues like ambiguous instructions and missing information. The second stage performs offline preprocessing where LLMs extract structured execution directed acyclic graphs (DAGs) from unstructured TSG documents and create Query Preparation Plugins (QPPs) that handle data-intensive queries by preparing necessary context and parameters. The third stage executes TSGs online using a DAG-guided scheduler-executor framework that interprets the extracted control flow, maintains a memory system to track execution state, and schedules independent steps for parallel execution. The framework uses GPT-4 as the underlying LLM and integrates specialized components to handle the unique challenges of TSG automation, including conditional logic, iterative steps, and complex data retrieval operations.

## Ground truth and evaluation

The evaluation uses a collection of 92 real-world TSGs from production systems and associated incident data. The paper measures success rate as the primary metric, where StepFly achieves approximately 94% success rate on GPT-4.1. Comparative evaluation against baseline approaches demonstrates that StepFly outperforms alternatives while consuming less time and fewer tokens. For TSGs that contain parallelizable steps, the framework achieves execution time reductions ranging from 32.9% to 70.4%. The empirical study analyzes characteristics of real-world TSGs to identify common patterns and challenges, which informed the design of the framework. The evaluation focuses on both correctness of execution and efficiency metrics including total execution time and computational resource consumption.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the approach inherently depends on the quality of the underlying LLM, specifically GPT-4, for both the offline preprocessing stage and online execution. The framework requires TSGs to be amenable to DAG representation, which may not capture all possible control flow patterns in arbitrary troubleshooting procedures. The success rate of 94%, while high, indicates that some TSGs still fail to execute correctly, though the specific failure modes are not detailed. The preprocessing stage requires offline computation to extract DAGs and create QPPs, which represents an upfront cost before TSGs can be automated.

## Gaps this paper opens

The paper does not address how StepFly integrates with broader root cause analysis workflows beyond TSG execution, leaving open questions about how automated TSG results feed into causal reasoning and diagnosis. The framework focuses on executing existing TSGs but does not explore how to automatically generate or update TSGs based on new incident patterns or system changes. The relationship between TSG execution and the underlying service dependency topology is not explicitly modeled, which could limit effectiveness when troubleshooting issues that span multiple services. The paper does not investigate how temporal patterns in observability data could inform TSG execution or help prioritize diagnostic steps. The evaluation does not examine how StepFly performs when TSGs contain outdated information or when system behavior deviates from TSG assumptions.

## Relevance to the thesis topic

StepFly addresses incident diagnosis through automated execution of troubleshooting procedures, which is adjacent to root cause analysis but focuses on a different aspect of the problem. While the thesis topic emphasizes temporal and dependency analysis for identifying root causes, StepFly concentrates on automating the execution of predefined diagnostic workflows. The framework could complement temporal causal analysis by providing a structured way to execute diagnostic queries and gather evidence, but it does not perform causal reasoning itself. The DAG representation of TSGs captures procedural dependencies between diagnostic steps but not the causal dependencies between system components that are central to the thesis topic. The parallel execution capability demonstrates awareness of step independence but does not leverage temporal failure propagation patterns. StepFly represents an orthogonal approach to incident management that could potentially be integrated with temporal and dependency-based root cause analysis to create a more comprehensive diagnostic system.
