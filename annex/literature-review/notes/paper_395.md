---
paper_id: 395
title: Feedback-based, Automated Failure Testing of Microservice-based Applications
authors:
  - Chengxu Cui
  - Guoquan Wu
  - Wei Chen
  - Jiaxing Zhu
  - Jun Wei
year: 2019
venue: arXiv
doi: ""
arxiv_id: 1908.06466
url: "http://arxiv.org/abs/1908.06466v2"
pdf_path: data/pdfs/paper_395.pdf
read_date: 2026-05-11

category:
  - benchmark_and_evaluation
  - distributed_system_monitoring
  - anomaly_detection

method:
  family: hybrid
  specific: feedback-based failure injection with coverage-guided search
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
  primary_contribution: An automated failure testing technique that uses feedback from previous test executions to guide the selection of failure injection points in microservice applications.
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

Microservice architectures require robust fault-handling capabilities because services are developed independently and failures can propagate through complex service dependencies. Traditional failure testing approaches for microservices are either manual or use random failure injection, which is inefficient at discovering defects in fault-handling logic. The problem is that the space of possible failure scenarios grows exponentially with the number of services and their interactions, making exhaustive testing impractical. Existing approaches lack systematic guidance on which failures to inject and when to inject them to maximize the discovery of fault-handling defects. The challenge is to develop an automated testing method that can efficiently explore the failure scenario space and quickly expose defects in how microservices handle failures.

## Method summary

IntelliFT employs a feedback-based approach that iteratively selects failure injection points based on information gathered from previous test executions. The technique maintains a coverage metric that tracks which fault-handling code paths have been exercised during testing. In each iteration, the system selects a service and a failure type to inject, executes the test, and observes the resulting behavior including which fault-handling paths are triggered. The feedback mechanism uses this execution information to guide subsequent failure injection decisions, prioritizing scenarios that are likely to exercise previously unexplored fault-handling code. The approach combines static analysis to identify potential failure injection points with dynamic execution monitoring to track coverage. The system automates the entire testing cycle including failure injection, execution monitoring, and result analysis, eliminating the need for manual test case design.

## Ground truth and evaluation

The paper evaluates IntelliFT on a medium-size microservice benchmark system but does not specify which benchmark or its exact characteristics. The ground truth consists of known defects in fault-handling logic that the technique should discover. The evaluation measures effectiveness by the number of defects exposed and the efficiency in terms of how quickly these defects are found compared to baseline approaches. The paper reports that the initial experimental results show the proposed approach is effective, though specific metrics and comparison baselines are not detailed in the abstract. The evaluation appears to focus on demonstrating that feedback-guided failure injection can discover fault-handling defects more efficiently than alternative approaches, though the exact experimental setup and quantitative results are not fully described.

## Stated limitations

The paper characterizes the results as initial and experimental, suggesting the evaluation is preliminary. The testing is conducted on a single medium-size benchmark system, which limits the generalizability of the findings to other microservice applications with different architectures or scales. The abstract does not discuss limitations related to the types of failures that can be injected, the overhead of the monitoring infrastructure, or potential false positives in defect detection. There is no mention of how the approach handles non-deterministic behavior in microservices or how it scales to large-scale production systems. The feedback mechanism's effectiveness may depend on the quality of the coverage metric and the ability to accurately identify fault-handling code paths, but these potential limitations are not explicitly addressed.

## Gaps this paper opens

The paper introduces a feedback-based testing approach but does not address how to diagnose the root cause of failures once defects are discovered. While the technique can expose fault-handling defects, it does not provide mechanisms for understanding why failures occur or how they propagate through service dependencies. The approach focuses on testing individual services but may not fully capture complex failure propagation patterns across multiple services in realistic scenarios. There is a gap in understanding how temporal aspects of failure injection affect the discovery of defects, such as the timing of failures relative to request processing or the duration of injected failures. The paper does not discuss how to prioritize discovered defects based on their severity or impact on system reliability. Additionally, there is no exploration of how the testing results could inform the design of monitoring or diagnosis systems for production environments.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses failure scenarios in microservice systems but focuses on testing rather than root cause analysis. The feedback-based failure injection technique could complement root cause analysis by systematically generating realistic failure scenarios that RCA systems need to diagnose. Understanding how failures are injected and propagate during testing provides insights into the types of failure patterns that occur in production and need to be analyzed. The paper's focus on service dependencies and fault-handling logic relates to the dependency analysis component of the thesis framework. However, the paper does not address temporal analysis of failure propagation or the diagnosis of root causes once failures are detected. The benchmark system and defect discovery methodology could potentially be adapted to evaluate root cause analysis techniques by providing controlled failure scenarios with known ground truth causes.
