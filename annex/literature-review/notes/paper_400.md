---
paper_id: 400
title: "Rebooting Microreboot: Architectural Support for Safe, Parallel Recovery in Microservice Systems"
authors:
  - Laurent Bindschaedler
year: 2026
venue: arXiv
doi: ""
arxiv_id: 2604.09963
url: "http://arxiv.org/abs/2604.09963v1"
pdf_path: data/pdfs/paper_400.pdf
read_date: 2026-05-11

category:
  - recommendation_and_remediation
  - service_dependency_topology
  - root_cause_analysis

method:
  family: hybrid
  specific: three-agent architecture with typed ISA and microkernel validation
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
  primary_contribution: A safe microreboot system that uses typed remediation plans, explicit side-effect semantics, and recovery boundary inference from distributed traces to enable parallel service recovery without disrupting dependent services.
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

Microreboot as originally conceived enables fast recovery by restarting only failing components rather than entire systems. However, in modern microservice architectures with dense service dependencies, naive component restarts create cascading disruptions because rebooting one service can break many callers that depend on it. The problem is compounded by autonomous remediation agents that execute raw infrastructure commands without safety guarantees, potentially causing additional harm through unsafe actuation decisions. Existing microreboot approaches lack mechanisms to determine which services can be safely restarted together and in what order, and they provide no protection against unsafe remediation actions proposed by untrusted agents. The core challenge is making microreboot practical and safe in densely interconnected microservice systems where dependencies create complex failure propagation patterns.

## Method summary

The system implements a three-agent architecture that separates diagnosis, planning, and verification responsibilities, treating all agents as explicitly untrusted. The planning agent proposes remediation actions using a seven-action instruction set architecture with explicit side-effect semantics, where each action type has formally defined preconditions and postconditions. A small microkernel validates each proposed remediation plan and executes it transactionally, ensuring that unsafe operations are rejected regardless of agent behavior. To determine where restarts are safe, the system infers recovery boundaries online from distributed traces by analyzing service dependency patterns. This inference computes minimal restart groups that identify which services must be restarted together and derives ordering constraints to prevent cascading failures. The typed actuation model ensures that remediation plans specify explicit semantics rather than raw infrastructure commands, allowing the microkernel to reason about safety properties before execution. The architecture prioritizes safety over speed, accepting increased time-to-recovery in exchange for guaranteed harm prevention.

## Ground truth and evaluation

The system is evaluated using industrial distributed traces from Alibaba and Meta, as well as DeathStarBench with fault injection to simulate failure scenarios. Recovery-group inference performance is measured showing P99 latency of 21 milliseconds for computing restart boundaries from trace data. Safety is evaluated through simulation experiments measuring agent-caused harm, where typed actuation reduces harmful actions by 95 percent compared to untyped approaches. Online deployment testing achieves 0 percent harm, meaning no unsafe remediation actions were executed in production scenarios. The evaluation explicitly acknowledges that LLM inference overhead increases time-to-recovery for services with fast auto-restart capabilities, demonstrating the tradeoff between safety guarantees and recovery speed. The ground truth for recovery boundaries comes from the dependency structure extracted from distributed traces, while harm metrics are computed by comparing remediation outcomes against known safe states.

## Stated limitations

The paper explicitly states that the primary value proposition is safety rather than speed, acknowledging that LLM inference overhead increases time-to-recovery for services that have fast auto-restart mechanisms. This represents a fundamental tradeoff where safety guarantees come at the cost of recovery latency. The system requires distributed traces to infer recovery boundaries, which means it depends on comprehensive observability infrastructure being in place. The three-agent architecture and microkernel validation add computational overhead compared to direct remediation execution. The evaluation uses simulation for some safety metrics rather than exhaustive real-world testing across all possible failure modes. The typed ISA is limited to seven actions, which may not cover all possible remediation strategies that operators might want to employ in complex production environments.

## Gaps this paper opens

The paper does not address how the system handles incomplete or incorrect distributed traces, which could lead to incorrect recovery boundary inference and unsafe restart decisions. The relationship between the diagnosis agent's root cause analysis and the planning agent's remediation strategy selection remains underspecified, leaving open questions about how diagnostic confidence affects plan generation. The work does not explore how the system adapts when service dependencies change dynamically during runtime, potentially invalidating previously computed recovery boundaries. There is no discussion of how the verification agent validates plans when ground truth about safe states is uncertain or when multiple conflicting safety constraints exist. The paper does not examine how the system handles scenarios where the minimal restart group is too large to restart safely or where ordering constraints create circular dependencies. The integration of LLM-based agents with the formal verification microkernel raises questions about how to handle non-deterministic agent behavior while maintaining safety guarantees.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses remediation and recovery rather than root cause analysis directly, though it assumes diagnosis has already occurred. The recovery boundary inference from distributed traces is relevant to understanding service dependencies, which is a core component of the thesis framework for dependency analysis. The paper's approach to extracting dependency structures from traces and computing minimal restart groups provides techniques applicable to understanding how failures propagate through service dependencies. However, the primary focus on safe actuation and remediation planning differs from the thesis emphasis on temporal and causal analysis for identifying root causes. The work demonstrates how dependency topology extracted from observability data can inform recovery decisions, which complements but does not directly address the thesis goal of using temporal patterns to trace failures back to their origins. The explicit modeling of service dependencies and their role in failure propagation is valuable context for understanding how root causes manifest across distributed systems.
