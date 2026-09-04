---
paper_id: 281
title: "Approaching overload: diagnosis and response to anomalies in complex and automated systems"
authors:
  - Marisa R. Grayson
year: 2020
venue: "Proceedings: 8th REA Symposium on Resilience Engineering: Scaling up and Speeding up Linnaeus Univerity, Kalmar, Sweden, 24th-27th June 2019"
doi: 10.15626/rea8.13
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/5e63ab1ed3243a6f606706a79bf567a187b6c080"
pdf_path: data/pdfs/paper_281.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - observability_data_analysis
  - distributed_system_monitoring

method:
  family: other
  specific: Above the Line / Below the Line Framework (ABL) from Cognitive Systems Engineering
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
  primary_contribution: Application of Cognitive Systems Engineering framework to analyze how Site Reliability Engineers diagnose and respond to anomalies in complex web production systems through case study analysis.
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

Web production software systems operate at unprecedented scale and require extensive automation for development and maintenance. These systems are designed to adapt dynamically to changing loads to prevent network overload, but as they scale and grow in complexity, it becomes increasingly difficult to observe, model, and track their functioning and malfunctioning behaviors. Anomalies inevitably emerge in these complex systems, creating challenges for incident responders and Site Reliability Engineers who must recognize and understand unusual behaviors while planning and executing interventions to mitigate or resolve service outages. The fundamental problem is understanding the interplay between human and machine agents when disruptions occur, particularly how cognitive work above the line of representation relates to the cascade of disturbances occurring below that line in the actual system infrastructure.

## Method summary

The study employs the Above the Line / Below the Line Framework from Cognitive Systems Engineering and Resilience Engineering to analyze four real incident cases from web production systems. The ABL framework distinguishes between events and states below the line of representation, which include the actual system components, network behaviors, and infrastructure elements, and the cognitive work above the line, which encompasses what incident responders can observe through computer interfaces and monitoring tools. The analysis examines how Site Reliability Engineers perceive, interpret, and respond to anomalies by linking the cascade of disturbances in the underlying system with the cognitive processes of diagnosis and intervention. This qualitative case study approach reviews incidents post mortem to identify patterns in how complications arise during incident management and to understand the gap between what is happening in the system and what responders can observe and comprehend through available tooling.

## Ground truth and evaluation

The ground truth for this study consists of four real incident cases from web production software systems. The evaluation is qualitative and based on post mortem analysis of these actual incidents, examining the documented sequence of events, responder actions, and system behaviors. The framework does not employ quantitative metrics or controlled experiments but instead focuses on identifying patterns across the cases that reveal complications in incident management. The assessment considers how well the ABL framework illuminates the relationship between system-level disturbances and human cognitive work during incident response. The study validates its findings through the identification of both specific patterns within individual cases and general patterns that emerge across multiple incidents, demonstrating recurring challenges that Site Reliability Engineers face when diagnosing and responding to anomalies in complex automated systems.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the nature of the case study approach implies certain constraints. The analysis is based on only four incident cases, which may limit the generalizability of the identified patterns to the broader landscape of web production systems. The retrospective post mortem analysis relies on available documentation and records of incidents, which may not capture all aspects of the real-time cognitive work and decision-making processes that occurred during the actual incidents. The qualitative nature of the ABL framework analysis means that findings are interpretive rather than quantitatively measurable, making it difficult to establish objective criteria for success or failure in incident response.

## Gaps this paper opens

The paper identifies the need for better tooling to support Site Reliability Engineers in bridging the gap between system-level disturbances and observable representations. While the ABL framework successfully analyzes past incidents, it does not provide concrete technical solutions or automated methods for improving real-time anomaly detection and diagnosis. The study reveals patterns of complications but does not develop predictive models or automated systems that could anticipate or prevent similar incidents in the future. There is an open question about how to translate the cognitive systems engineering insights into practical improvements in monitoring infrastructure, alerting systems, and diagnostic tools. The paper also highlights but does not resolve the challenge of representing increasingly complex system behaviors in ways that support effective human reasoning and decision-making during high-pressure incident response situations.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses root cause analysis and anomaly diagnosis in complex distributed systems from a human factors perspective rather than a technical automation perspective. While the thesis focuses on automated temporal and dependency analysis for root cause identification in cloud-native systems, this paper examines the cognitive challenges that human operators face when interpreting system anomalies and planning interventions. The insights about the gap between system-level disturbances and observable representations are relevant for understanding what information automated RCA systems need to surface to support effective human decision-making. The emphasis on how cascading failures propagate below the line of representation connects to temporal failure propagation concepts in the thesis. However, the paper does not develop automated analysis techniques, machine learning models, or dependency graph methods that would directly contribute to the technical framework proposed in the thesis. The work is valuable for understanding the operational context and human needs that automated RCA systems must address.
