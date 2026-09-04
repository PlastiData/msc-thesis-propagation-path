---
paper_id: 311
title: Actionable and interpretable fault localization for recurring failures in online service systems
authors:
  - Zeyan Li
  - Nengwen Zhao
  - Mingjie Li
  - Xianglin Lu
  - Lixin Wang
  - Dong Chang
  - Xiaohui Nie
  - Li Cao
  - Wenzhi Zhang
  - Kaixin Sui
  - Yanhua Wang
  - Xu Du
  - Guoqiang Duan
  - Dan Pei
year: 2022
venue: ESEC/SIGSOFT FSE
doi: 10.1145/3540250.3549092
arxiv_id: 2207.09021
url: "https://www.semanticscholar.org/paper/a9028987d109dc5e816470fda8e676f627fc8577"
pdf_path: data/pdfs/paper_311.pdf
read_date: 2026-05-11

category:
  - root_cause_analysis
  - service_dependency_topology
  - observability_data_analysis

method:
  family: classical_ml
  specific: Random Forest with custom feature engineering
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
  primary_contribution: An automated fault localization approach that identifies both faulty components and indicative metric groups for recurring failures while providing global and local interpretability.
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

Fault localization in online service systems faces challenges from large volumes of diverse monitoring data and complex dependencies across system components. While existing research approaches can detect faults, they fail to provide actionable and interpretable results that engineers require for effective remediation. The current industry practice relies on experienced engineers who manually diagnose recurring failures using accumulated knowledge about the system and historical failure patterns. These engineers can identify root causes by recognizing indicative metric groups on faulty components and understand how failures propagate through system dependencies. However, this manual approach is slow, labor-intensive, and sometimes inaccurate, creating a need for automation that preserves the actionability and interpretability of human expert diagnosis.

## Method summary

DejaVu operates in two phases: offline training and online inference. During offline training, the system takes historical failure data and system dependency information as input to build a localization model. The approach represents each failure instance through features that capture both metric patterns and dependency relationships. For each component in the system, DejaVu constructs features from monitoring metrics and dependency context, then trains a Random Forest classifier to predict whether that component is faulty. The model learns to associate specific metric patterns with fault occurrences across different components. During online inference, when a new failure occurs, DejaVu applies the trained models to all components, ranking them by their predicted fault probability. The system outputs both the suspected faulty components and the indicative metric groups that triggered the prediction. Interpretability is provided through two mechanisms: global interpretation using feature importance from the Random Forest model to show which metrics generally indicate faults, and local interpretation using SHAP values to explain why specific components were ranked highly for a particular failure instance.

## Ground truth and evaluation

The ground truth for evaluation comes from 601 real failures across three production online service systems and one open-source benchmark system. For each failure, the ground truth specifies the actual faulty component that caused the incident. The evaluation uses ranking metrics, specifically measuring the average rank position where the true faulty component appears in DejaVu's output list. The paper reports that DejaVu ranks ground truth components at positions between 1.66 and 5.03 on average across the different systems, requiring engineers to examine only a small number of candidates from potentially long lists. The approach achieves this localization in less than one second per failure. Comparison with baseline methods shows DejaVu outperforms alternatives by 54.52 percent in ranking accuracy. The evaluation also includes ablation studies examining the contribution of different feature types and interpretability assessments through case studies demonstrating how the global and local explanations align with engineering understanding.

## Stated limitations

The paper explicitly states that DejaVu is designed for recurring failures, meaning it requires historical failure data for training and may not handle novel failure types that have not been seen before. The approach depends on the availability and quality of historical failure records and monitoring data from the target system. The effectiveness of the dependency-based features relies on having accurate dependency information about the system, which may not always be complete or up-to-date in practice. The interpretability mechanisms, while providing insights through feature importance and SHAP values, still require some domain knowledge from engineers to translate these explanations into concrete remediation actions. The evaluation is conducted on specific production systems and one benchmark, which may limit generalizability to other types of online service systems with different architectures or monitoring setups.

## Gaps this paper opens

The paper's focus on recurring failures leaves open the question of how to handle novel or previously unseen failure types, which are critical in evolving cloud-native systems. The approach treats each component independently during classification, potentially missing complex interactions or cascading failures that involve multiple components simultaneously. While dependency information is used as features, the paper does not deeply explore temporal propagation patterns of failures through the dependency graph, which could provide additional localization signals. The interpretability provided through feature importance and SHAP values offers statistical explanations but does not generate natural language descriptions or causal reasoning chains that might be more intuitive for operators. The evaluation focuses on ranking accuracy but does not extensively examine false positive rates or the practical impact of recommended actions on mean time to resolution. The paper does not address how the model should be updated or retrained as the system evolves or as new failure patterns emerge over time.

## Relevance to the thesis topic

This paper is directly relevant to the thesis topic as it addresses root cause analysis in distributed service systems using both dependency information and temporal patterns from monitoring data. DejaVu demonstrates how dependency topology can be incorporated as features for fault localization, which aligns with the thesis's emphasis on dependency analysis. The approach's use of historical failure patterns and metric time series data connects to the temporal analysis component of the thesis framework. However, DejaVu's treatment of temporal information is primarily through feature engineering rather than explicit temporal causal modeling, representing a different approach than what the thesis might pursue. The paper's emphasis on interpretability and actionability provides important requirements that any RCA framework should satisfy. The limitation to recurring failures highlights a gap that the thesis could address by incorporating temporal causal analysis to handle novel failure scenarios. The evaluation methodology and metrics used in this paper, particularly ranking-based evaluation on real production failures, offer valuable guidance for validating the thesis framework.
