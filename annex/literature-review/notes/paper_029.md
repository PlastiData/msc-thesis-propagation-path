---
paper_id: 029
title: Wait Analysis of Distributed Systems Using Kernel Tracing
authors:
  - Francis Giraldeau
  - M. Dagenais
year: 2016
venue: IEEE Transactions on Parallel and Distributed Systems
doi: 10.1109/TPDS.2015.2488629
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/3234ea18fea0c173e5a8d91147dde7a82ff945e6"
pdf_path: data/pdfs/paper_029.pdf
read_date: 2026-05-11

category:
  - observability_data_analysis
  - distributed_system_monitoring
  - temporal_failure_propagation

method:
  family: rule_based
  specific: kernel tracing with critical path analysis
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
  primary_contribution: A method to identify wait periods and their causes in distributed systems by correlating kernel-level events across multiple machines using critical path analysis.
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

Understanding performance bottlenecks in distributed systems requires identifying where time is spent and what causes delays across multiple machines. Traditional profiling tools focus on CPU usage but fail to capture waiting periods where threads are blocked or idle. These wait periods are critical for understanding performance degradation in distributed systems where processes frequently wait for network communication, synchronization primitives, or remote service responses. Existing approaches either lack the granularity to identify specific wait causes or cannot correlate events across machine boundaries. The challenge is to trace low-level system events across distributed nodes and reconstruct causal relationships that explain why processes wait and which remote operations are responsible for these delays.

## Method summary

The method uses kernel-level tracing to capture system events such as system calls, context switches, and network packet transmissions across all nodes in a distributed system. The LTTng tracer collects timestamped events with nanosecond precision from the Linux kernel. The approach builds execution graphs for each thread showing active periods and wait states. Critical path analysis identifies the sequence of operations that determine overall execution time. When a thread waits, the method examines kernel events to classify the wait type, such as waiting on network I/O, disk operations, or synchronization primitives. For distributed waits, the system correlates network send and receive events across machines using packet matching to establish causal links. The analysis reconstructs which remote operations caused local waits by following these cross-machine dependencies. The result is a detailed breakdown of where time is spent and which components or machines are responsible for delays.

## Ground truth and evaluation

The evaluation uses synthetic benchmarks and real distributed applications where the expected behavior and bottlenecks are known by design. The authors test their approach on client-server applications with deliberate delays inserted at specific points to verify that the analysis correctly identifies these artificial bottlenecks. They examine distributed database operations and parallel computing workloads where the critical path can be manually verified. The accuracy is assessed by comparing the identified wait causes against the known sources of delay in controlled experiments. Performance overhead of the tracing infrastructure is measured to ensure the observation does not significantly perturb the system behavior. The evaluation demonstrates that the method can pinpoint specific system calls and remote operations responsible for waits with low overhead, though the paper does not use independent fault injection or compare against alternative root cause analysis methods.

## Stated limitations

The paper acknowledges that kernel tracing generates large volumes of data that require significant storage and post-processing time. The overhead of tracing, while low, can still affect timing-sensitive applications and may perturb the very behavior being observed. Correlating events across machines requires synchronized clocks, and clock drift can introduce inaccuracies in causal analysis. The method requires access to kernel-level instrumentation which may not be available in all deployment environments, particularly in cloud settings where users lack kernel access. The analysis is limited to wait periods visible at the kernel level and cannot directly observe application-level semantic information such as business logic delays or higher-level protocol interactions. The approach also requires domain knowledge to interpret the low-level kernel events in terms of application behavior.

## Gaps this paper opens

The method focuses on performance analysis rather than failure diagnosis, leaving open how kernel tracing could be adapted for root cause analysis of errors and anomalies in distributed systems. The approach does not address how to automate the interpretation of wait patterns or how to distinguish normal operational delays from pathological conditions indicating faults. There is no discussion of how the technique scales to large-scale cloud-native systems with hundreds or thousands of services where manual analysis becomes infeasible. The paper does not explore integration with higher-level observability data such as application logs or metrics that could provide semantic context for kernel events. The relationship between low-level wait analysis and service-level objectives or user-perceived performance remains unexplored. Finally, the work does not consider how machine learning or automated reasoning could be applied to the traced data to identify recurring patterns or predict performance issues.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic because it addresses temporal analysis and dependency tracking in distributed systems, though focused on performance rather than failure root cause analysis. The kernel tracing approach provides fine-grained temporal data about system behavior and establishes causal dependencies across service boundaries through network event correlation. These capabilities are relevant for understanding failure propagation in cloud-native systems where timing relationships and cross-service dependencies are critical. However, the method operates at the kernel level rather than the application or service level typical in cloud-native environments, and it does not address anomaly detection or fault diagnosis. The critical path analysis technique could potentially be adapted to trace failure propagation paths in a root cause analysis framework. The work demonstrates the value of low-level temporal data for understanding distributed system behavior, though the thesis would need to bridge the gap between kernel events and service-level failures in containerized cloud environments.
