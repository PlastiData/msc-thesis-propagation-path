---
paper_id: 016
title: "STL-GO: Spatio-Temporal Logic with Graph Operators for Distributed Systems with Multiple Network Topologies"
authors:
  - Yiqi Zhao
  - Xinyi Yu
  - Bardh Hoxha
  - Georgios Fainekos
  - J. Deshmukh
  - Lars Lindemann
year: 2025
venue: ACM Transactions on Embedded Computing Systems
doi: 10.1145/3760258
arxiv_id: 2507.15147
url: "https://www.semanticscholar.org/paper/247e27968a81a399d7255213fcdbe4f304c25385"
pdf_path: data/pdfs/paper_016.pdf
read_date: 2026-05-11

category:
  - distributed_system_monitoring
  - observability_data_analysis

method:
  family: formal_methods
  specific: spatio-temporal logic with graph operators
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
  primary_contribution: A formal logic framework STL-GO that extends signal temporal logic with graph operators to specify and monitor requirements in multi-agent systems with multiple network topologies using only local information.
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

Multi-agent systems consist of autonomous agents that communicate and coordinate to achieve complex missions across applications like robotics, smart cities, and internet-of-things deployments. Monitoring and verifying requirements in such systems presents significant challenges because specifications must capture diverse sensing and communication modalities, dependencies between agent tasks, and spatial or virtual distances between agents. Existing specification languages for multi-agent systems lack the expressiveness to reason about the number of neighboring agents satisfying properties of interest while considering multiple types of interaction graphs simultaneously. Furthermore, centralized monitoring approaches do not scale to large distributed systems where agents need to determine specification satisfaction using only locally available information. The problem is to develop a formal specification language that can express rich requirements over multiple network topologies and enable distributed monitoring where individual agents can verify properties without global knowledge.

## Method summary

STL-GO extends signal temporal logic by introducing graph operators that enable reasoning about agent interactions modeled through multiple directed graphs. Each graph represents a different interaction modality such as sensing, communication, or task dependencies. The logic includes two primary graph operators: one that counts incoming edges and another that counts outgoing edges from an agent that satisfy a given property. These operators allow specifications to express requirements like an agent needing at least two neighbors with specific capabilities or ensuring that all downstream agents in a task dependency graph satisfy safety conditions. The framework supports nested temporal and spatial operators, enabling complex specifications that combine timing constraints with topological reasoning. The authors develop distributed monitoring algorithms where each agent evaluates the specification using only information from its local neighborhood in the interaction graphs. The monitoring procedure computes robustness values that indicate how strongly a specification is satisfied or violated, providing quantitative feedback beyond binary satisfaction. The distributed monitors are proven to be sound and complete for the class of STL-GO specifications.

## Ground truth and evaluation

The paper evaluates STL-GO through two case studies rather than using labeled ground truth datasets. The first case study involves a bike-sharing system where agents represent bikes and docking stations with interaction graphs modeling physical proximity and operational dependencies. Specifications capture requirements about bike availability, station capacity, and coordination between stations. The second case study examines a multi-drone system where drones must coordinate for area coverage and collision avoidance. The interaction graphs represent sensing ranges and communication links between drones. For both case studies, the authors demonstrate that their distributed monitors correctly evaluate STL-GO specifications using simulated traces of agent behaviors. The evaluation focuses on showing that the logic can express meaningful requirements that cannot be captured by existing formalisms and that the distributed monitoring approach scales with the number of agents. The paper includes expressivity comparisons against related spatial and temporal logics, proving that STL-GO can express properties that are inexpressible in these other frameworks. However, the evaluation does not include real-world deployment data or comparison against baseline monitoring approaches in terms of detection accuracy or latency.

## Stated limitations

The paper acknowledges that STL-GO monitoring requires agents to have access to information from their local neighborhoods in the interaction graphs, which assumes that communication infrastructure supports this information exchange. The distributed monitoring approach has computational complexity that depends on the nesting depth of graph operators and the size of local neighborhoods. The authors note that their current framework assumes the interaction graphs are known and fixed over time, though they suggest extensions to handle dynamic topologies as future work. The case studies use simulated data rather than real-world deployments, which limits validation of the approach under realistic conditions with noisy measurements and communication failures. The paper does not provide detailed analysis of how the monitoring approach degrades when communication links fail or when agents have incomplete information about their neighborhoods. Additionally, the framework focuses on monitoring and specification rather than on diagnosis or root cause analysis when violations are detected.

## Gaps this paper opens

The paper introduces a formal specification language but does not address how to diagnose the root causes when STL-GO specifications are violated in distributed systems. While the monitoring approach can detect that a requirement is not satisfied and provide robustness metrics, it does not explain which agents or interactions are responsible for the violation or how failures propagate through the interaction graphs. The framework assumes interaction graphs are given but does not provide methods for automatically inferring these graphs from observational data in real systems. There is no discussion of how to integrate STL-GO monitoring with existing observability platforms or how to translate violations into actionable remediation steps. The paper does not explore how temporal patterns in specification violations could reveal underlying system issues or how dependency relationships in the interaction graphs affect failure propagation. The case studies demonstrate monitoring capabilities but do not examine scenarios where multiple interacting failures occur or where causal relationships between agent behaviors need to be understood. The framework would benefit from extensions that use the graph structure and temporal violation patterns to perform automated root cause analysis.

## Relevance to the thesis topic

STL-GO provides a formal framework for reasoning about distributed systems with explicit network topologies, which is directly relevant to understanding service dependencies in cloud-native systems. The multiple interaction graphs in STL-GO correspond conceptually to different dependency relationships in microservices architectures, such as service call graphs, data flow dependencies, and deployment topologies. The distributed monitoring approach demonstrates how to evaluate system properties using only local information, which aligns with the scalability requirements of cloud-native root cause analysis. However, STL-GO focuses on specification and monitoring rather than on diagnosing root causes when violations occur. The graph operators and robustness metrics could potentially be adapted to identify which services or dependencies contribute most to requirement violations, providing a foundation for dependency-aware root cause analysis. The temporal aspects of STL-GO specifications relate to the temporal propagation of failures in distributed systems, though the paper does not explore causal relationships between events. The formal semantics and distributed evaluation algorithms offer rigorous foundations that could complement data-driven approaches to root cause analysis. Overall, this work is adjacent to the thesis topic because it addresses distributed system monitoring with explicit dependency modeling but does not tackle the root cause analysis problem directly.
