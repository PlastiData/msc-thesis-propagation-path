---
paper_id: 390
title: "Microservices Anti Patterns: A Taxonomy"
authors:
  - Davide Taibi
  - Valentina Lenarduzzi
  - Claus Pahl
year: 2019
venue: arXiv
doi: ""
arxiv_id: 1908.04101
url: "http://arxiv.org/abs/1908.04101v3"
pdf_path: data/pdfs/paper_390.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - observability_data_analysis
  - other

method:
  family: other
  specific: qualitative practitioner interviews and taxonomy construction
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
  primary_contribution: A taxonomy of 20 microservices anti-patterns derived from practitioner interviews, categorized into organizational and technical dimensions.
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

Organizations are migrating from monolithic architectures to microservices without sufficient experience or established best practices. Practitioners and consultants are learning through trial and error, often relying on books and blog posts rather than systematic guidance. This lack of structured knowledge leads to repeated mistakes across different organizations as they attempt microservices adoption. The paper addresses the need for a systematic catalog of common problems that arise during microservices development and migration, enabling practitioners to avoid known pitfalls and researchers to understand the practical challenges in microservices architectures.

## Method summary

The authors conducted interviews with practitioners over a three-year period to collect experiences and challenges encountered in microservices development. They synthesized these experiences into a taxonomy organizing 20 anti-patterns across two main dimensions. The organizational dimension includes team-oriented anti-patterns related to how teams are structured and interact, and technology-tool-oriented anti-patterns concerning tool and technology choices. The technical dimension encompasses internal anti-patterns related to service design and implementation, and communication anti-patterns addressing inter-service interactions. Each anti-pattern in the catalog describes a problematic practice or pattern that practitioners commonly encounter but should avoid.

## Ground truth and evaluation

The ground truth for this work derives from practitioner interviews conducted over three years, representing real-world experiences from companies implementing microservices. The validation approach is primarily qualitative, based on the consistency of problems reported across multiple practitioners and organizations. The paper does not present quantitative metrics or controlled experiments to measure the harmfulness of identified anti-patterns. Instead, it relies on the collective experience of interviewed practitioners to establish which patterns are problematic and warrant inclusion in the taxonomy. The authors acknowledge that further validation of the anti-patterns' harmfulness is needed and position this as future work for researchers.

## Stated limitations

The paper explicitly states that the anti-patterns identified require further validation by researchers to confirm their harmfulness in practice. The taxonomy is based on practitioner experiences rather than systematic empirical studies with controlled conditions. The authors note that the catalog represents a snapshot of knowledge accumulated over three years of interviews but does not claim completeness or exhaustiveness. The work is positioned as a starting point for both practitioners and researchers rather than a definitive or fully validated catalog. The reliance on practitioner self-reporting means the anti-patterns reflect perceived problems rather than objectively measured impacts on system quality or operational metrics.

## Gaps this paper opens

The paper identifies anti-patterns but does not provide quantitative evidence of their impact on system reliability, performance, or operational costs. There is no connection made between these anti-patterns and observable symptoms in monitoring data, logs, or metrics that could be used for automated detection. The work does not address how these anti-patterns manifest in runtime behavior or how they might be detected through analysis of observability data. The relationship between anti-patterns and specific failure modes or root causes of incidents remains unexplored. The taxonomy lacks guidance on how to systematically detect these patterns in existing systems or how to measure their prevalence across different organizations and domains.

## Relevance to the thesis topic

This paper provides foundational context for understanding common architectural and operational problems in microservices systems that can lead to failures requiring root cause analysis. The anti-patterns identified, particularly those related to service communication and internal service design, represent potential root causes of system failures that an RCA framework would need to diagnose. Understanding these patterns helps frame what kinds of architectural issues might manifest as temporal anomalies or dependency-related failures in cloud-native systems. However, the paper does not address the detection or diagnosis of these issues through observability data, temporal analysis, or dependency graphs. The work is complementary to an RCA framework by identifying what problems exist, but it does not provide methods for detecting when these problems cause incidents or how to trace failures back to these architectural anti-patterns using runtime data.
