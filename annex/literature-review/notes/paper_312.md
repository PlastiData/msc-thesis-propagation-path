---
paper_id: 312
title: Model-based Reinforcement Learning for Service Mesh Fault Resiliency in a Web Application-level
authors:
  - Fanfei Meng
  - L. Jagadeesan
  - M. Thottan
year: 2021
venue: Applied and Computational Engineering
doi: 10.54254/2755-2721/43/20230817
arxiv_id: 2110.13621
url: "https://www.semanticscholar.org/paper/2908fd01898243c90a84714db927ba0abfc73e16"
pdf_path: data/pdfs/paper_312.pdf
read_date: 2026-05-11

category:
  - recommendation_and_remediation
  - distributed_system_monitoring
  - benchmark_and_evaluation

method:
  family: deep_learning
  specific: model-based reinforcement learning with communicative multi-agent extension
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
  primary_contribution: A model-based reinforcement learning approach to identify worst-case combinations of service mesh configuration attributes and load settings that challenge application-level fault resiliency.
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

Microservice architectures deployed with service mesh technologies like Istio provide fault resiliency through configurable attributes that govern self-adaptive behaviors in response to failures. These attributes include timeout values, retry policies, circuit breaker thresholds, and other parameters that control how services respond to faults without requiring changes to application code. The challenge is that the space of possible attribute configurations combined with varying load conditions is extremely large, making it impractical to exhaustively test all combinations using traditional software testing approaches. The relationships among these attributes and their interaction with load patterns can produce unexpected emergent behaviors that significantly degrade application performance and fault resilience. Organizations need a systematic way to discover the worst-case configurations before full production deployment, as these problematic combinations may only manifest under specific failure and load conditions that are difficult to anticipate manually.

## Method summary

The authors propose a model-based reinforcement learning framework that treats the discovery of problematic configurations as an optimization problem. The system models the service mesh environment as a Markov Decision Process where actions correspond to selecting specific combinations of service mesh attributes and load parameters. The agent learns a model of the environment dynamics and uses this model to plan actions that maximize a reward signal designed to identify configurations leading to poor fault resilience. The approach employs model-based methods rather than model-free alternatives to improve sample efficiency, which is important given the cost of running fault injection experiments. The framework is extended to support communicative multi-agent reinforcement learning, where multiple agents can share information about their observations and learned policies. This multi-agent approach allows different agents to explore different regions of the configuration space while benefiting from shared knowledge. The system performs fault injection experiments on a deployed application, observes the resulting performance metrics, and iteratively refines its understanding of which configuration combinations produce the most severe degradation in application-level fault resilience.

## Ground truth and evaluation

The evaluation uses a case study involving a simple request-response service deployed with the Istio service mesh on a Kubernetes cluster. The ground truth for fault resilience is defined through application-level performance metrics observed during controlled fault injection experiments. These metrics include response times, error rates, and throughput under various failure scenarios such as network delays and service unavailability. The authors compare their model-based reinforcement learning approach against a baseline that selects configuration parameters randomly or according to predefined heuristics. Performance is measured by how quickly and effectively each method identifies configuration combinations that result in the worst fault resilience outcomes. The evaluation demonstrates that the model-based approach discovers problematic configurations more efficiently than the baseline. Additionally, the communicative multi-agent variant shows improved performance over both single-agent and non-communicative multi-agent approaches, finding worse-case scenarios with fewer experimental trials. The metrics focus on the learning efficiency and the severity of fault resilience degradation discovered rather than on diagnosing root causes of specific failures.

## Stated limitations

The paper acknowledges that the evaluation is limited to a simple request-response service architecture, which may not capture the complexity of real-world microservice applications with many interdependent services. The authors note that scaling the approach to larger systems with hundreds of microservices and more complex interaction patterns remains an open challenge. The computational cost of model learning and the number of fault injection experiments required for convergence are not thoroughly analyzed, leaving questions about practical deployment timelines. The paper does not address how the learned policies generalize across different application workloads or how the approach handles dynamic changes in application topology that occur during continuous deployment cycles. There is limited discussion of how the choice of reward function affects the types of problematic configurations discovered and whether important failure modes might be missed if the reward signal is not carefully designed. The integration with existing continuous integration and deployment pipelines is not explored.

## Gaps this paper opens

The work focuses on discovering problematic configurations but does not address how to diagnose why specific attribute combinations lead to poor fault resilience or how to recommend corrective actions. There is no mechanism for explaining the causal relationships between configuration choices and observed failures, which would be valuable for operators trying to understand and fix resilience issues. The approach treats configuration discovery as a black-box optimization problem without building interpretable models of service dependencies or failure propagation paths. The temporal aspects of how failures cascade through microservices over time are not explicitly modeled, even though such temporal patterns are crucial for understanding root causes. The paper does not consider how observability data such as traces, logs, and metrics could be incorporated to provide richer state representations for the reinforcement learning agent. The relationship between service mesh configurations and underlying infrastructure failures is not explored, leaving a gap in understanding how low-level faults manifest as application-level resilience problems. The lack of integration with root cause analysis techniques means discovered problems must still be manually investigated.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses fault resilience in cloud-native systems but focuses on configuration testing rather than root cause analysis. The work demonstrates the importance of understanding how service mesh configurations affect fault behavior, which is relevant context for root cause analysis frameworks that must account for such configurations when diagnosing failures. However, the paper does not perform temporal analysis of failure propagation or build service dependency models for causal reasoning, which are core to the thesis. The reinforcement learning approach could potentially inform how to generate diverse failure scenarios for testing root cause analysis systems, but the paper itself does not contribute methods for identifying root causes. The emphasis on application-level fault resilience testing complements root cause analysis by identifying problematic configurations that RCA systems would need to diagnose. The lack of temporal causal analysis and dependency topology modeling means the techniques cannot directly support root cause identification, though the problem domain of service mesh resilience overlaps with the operational challenges that motivate root cause analysis research.
