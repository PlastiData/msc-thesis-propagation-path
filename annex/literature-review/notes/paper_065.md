---
paper_id: 065
title: Failure Isolation And Blast Radius Control In Large-Scale Distributed Systems
authors:
  - Sathwik Rao Sirikonda
  - Shashidhar Bhat
  - Rishabh Jain
  - Vikas Katoch
year: 2026
venue: International Journal of Advances in Signal and Image Sciences
doi: 10.29284/mkwrh621
arxiv_id: ""
url: "https://openalex.org/W7154241946"
pdf_path: data/pdfs/paper_065.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - root_cause_analysis
  - benchmark_and_evaluation

method:
  family: rule_based
  specific: operational pattern analysis with containment mechanisms
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
  primary_contribution: A measurement-based framework for failure isolation and blast radius control using operational instruments and empirical analysis of 30-50 public incidents from 2016-2025.
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

Large-scale distributed systems built on microservices, Kubernetes, service meshes, and multi-region platforms introduce complex dependency graphs that create numerous pathways for failure propagation. As these systems scale, failures that originate in isolated components can cascade across service boundaries, hosts, zones, regions, and organizational boundaries, affecting large numbers of users and services. The study identifies specific mechanisms that drive cascading failures including retry storms, shared control plane demands, noisy-neighbor resource contention, and configuration errors that transform localized issues into fleet-wide outages. Real-world incidents demonstrate the severity of this problem, with the Cloudflare incident of June 21, 2022 affecting 19 data centers and the AWS us-east-1 outage of December 7, 2021 lasting over 8 hours. The fundamental challenge is understanding how to contain failures within defined boundaries and limit the blast radius of incidents across temporal, geographic, and service dimensions.

## Method summary

The research develops a measurement-based framework that integrates multiple operational instruments for controlling failure propagation. The framework incorporates established containment patterns including bulkheads for resource isolation, circuit breakers for preventing cascading calls, rate limiting for controlling request flow, control plane separation to protect critical infrastructure, and zonal and cell-based architectural designs for geographic isolation. Progressive delivery and rollback mechanisms are included to limit the impact of problematic changes. The methodology analyzes 30-50 documented public incidents spanning from 2016 to 2025, extracting patterns and outcomes across different containment strategies. The framework establishes metrics based on mean time to detect (MTTD), mean time to recover (MTTR), service level objective (SLO) burn rates, and blast-radius indices that quantify the scope of impact across users, services, and geographic areas over time. Statistical comparison of containment outcomes across different architectural layers provides empirical guidance for designing resilient systems.

## Ground truth and evaluation

The ground truth for this study consists of 30-50 publicly documented incidents from major cloud providers and distributed systems operators between 2016 and 2025. Specific incidents referenced include the Cloudflare event affecting 19 data centers on June 21, 2022, and the AWS us-east-1 outage exceeding 8 hours on December 7, 2021. The evaluation framework uses community-derived metrics including MTTD and MTTR to assess detection and recovery capabilities. SLO burn rates measure the rate at which service quality degrades during incidents. Blast-radius indices quantify the scope of impact across multiple dimensions including affected users, impacted services, and geographic spread over time. The study performs statistical comparisons of containment outcomes across different architectural layers to identify which patterns and mechanisms most effectively limit failure propagation. The empirical analysis reveals that instability due to changes accounts for the majority of outages in the studied incident corpus.

## Stated limitations

The paper acknowledges that future research directions point to several current limitations in the field. There is a need for more uniform reporting standards for incidents, as the current analysis relies on publicly available postmortems that vary significantly in detail and structure. The framework presented is primarily retrospective and measurement-based rather than predictive, indicating a gap in the ability to anticipate and prevent failures before they occur. The study notes that predictive containment mechanisms require further development. The research also highlights challenges in safely automating containment and recovery in serverless and self-healing systems, suggesting that current operational instruments may not fully address the unique characteristics of these emerging architectures. The statistical comparisons are limited by the availability and quality of public incident reports, which may not represent the full spectrum of failure modes in production systems.

## Gaps this paper opens

The emphasis on uniform incident reporting reveals a significant gap in standardized observability and documentation practices across the industry. The call for predictive containment mechanisms indicates that current approaches are reactive rather than proactive, opening opportunities for research in anomaly detection and early warning systems that can anticipate cascading failures. The challenge of safe automation in serverless and self-healing systems suggests that existing containment patterns may not translate directly to these architectures, requiring new techniques tailored to ephemeral and dynamically scaling infrastructure. The measurement framework based on blast-radius indices and SLO burn rates provides a foundation but does not address how to automatically detect the boundaries of failure propagation in real-time. The statistical analysis of containment outcomes across layers suggests a need for more sophisticated causal models that can explain why certain mechanisms succeed or fail in specific contexts. The focus on operational instruments rather than automated root cause analysis leaves open questions about how to systematically identify the origin points of cascading failures.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic on root cause analysis in cloud-native systems using temporal and dependency analysis. While the paper focuses on failure isolation and blast radius control rather than identifying root causes, it provides critical context for understanding how failures propagate through distributed systems. The emphasis on dependency graphs and failure propagation pathways directly relates to the dependency analysis component of the thesis. The temporal dimension of blast radius measurement, tracking impact over time, aligns with the temporal analysis aspect of the proposed framework. The documented mechanisms of cascading failures including retry storms, shared control plane demands, and noisy-neighbor contention represent specific failure patterns that a root cause analysis system must understand. The measurement framework using MTTD, MTTR, and SLO burn rates provides relevant metrics that could inform the evaluation of root cause analysis effectiveness. However, the paper does not address the core challenge of automatically identifying causal relationships or root causes, instead focusing on containment strategies once failures occur. The empirical analysis of public incidents could serve as valuable case studies for validating root cause analysis approaches in the thesis work.
