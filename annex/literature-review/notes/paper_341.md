---
paper_id: 341
title: Deep Learning-Based Fault Localization in Video Networks Using Only Client-Side QoE
authors:
  - Hossein Ebrahimi Dinaki
  - S. Shirmohammadi
  - Emil Janulewicz
  - David Côté
year: 2020
venue: IEEE Transactions on Artificial Intelligence
doi: 10.1109/TAI.2020.3041816
arxiv_id: ""
url: "https://www.semanticscholar.org/paper/028f63f1475eaa1c6d6448445336bf8de472e41f"
pdf_path: data/pdfs/paper_341.pdf
read_date: 2026-05-11

category:
  - anomaly_detection
  - root_cause_analysis
  - observability_data_analysis

method:
  family: deep_learning
  specific: MLP and LSTM networks
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
  primary_contribution: A deep learning approach to localize network faults in video streaming systems using only client-side QoE metrics without requiring access to intermediate network infrastructure.
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

Video service providers face significant challenges in maintaining customer Quality of Experience because network faults can occur anywhere along the end-to-end delivery path. The fundamental difficulty is that this path spans multiple autonomous systems owned by different entities including the video streaming provider, internet service providers, and local network operators. When customers experience poor video quality, they typically blame the video service provider even though the root cause may lie in network segments that the provider cannot access or monitor. The provider needs a method to localize faults across this distributed infrastructure without having direct visibility into ISP or client networks. Traditional approaches require instrumentation and access to all network segments, which is impractical in the multi-stakeholder video delivery ecosystem.

## Method summary

The authors develop a supervised deep learning approach using two neural network architectures: multi-layer perceptron and long-short-term memory networks. The system takes as input only client-side QoE metrics measured during video streaming sessions. These metrics capture the quality degradation experienced by end users without requiring any information from intermediate network hops. The MLP architecture processes these QoE features to classify the fault location, while the LSTM variant leverages temporal patterns in the QoE time series data. Both models are trained on labeled data collected from a controlled testbed where faults are deliberately injected at known locations. The trained models learn to map patterns in QoE degradation to specific fault locations in either the ISP network or the client network. The approach enables fault localization by recognizing characteristic QoE signatures associated with faults in different network segments.

## Ground truth and evaluation

Ground truth is established through a controlled experimental testbed that simulates a realistic video streaming environment. The testbed consists of a video server, a simplified ISP network segment, and a client network, with the ability to inject actual network faults at specific locations. Faults are deliberately introduced in both ISP and client network segments while QoE metrics are recorded at the client side. The authors evaluate their approach by measuring classification accuracy for fault localization across different scenarios. The MLP and LSTM models achieve accuracy rates between 93% and 97% depending on the specific configuration and fault scenario. The evaluation demonstrates that the models can successfully distinguish between faults occurring in the ISP network versus the client network using only the observable QoE degradation patterns. Multiple videos are streamed during data collection to ensure diversity in the training and test datasets.

## Stated limitations

The paper does not explicitly enumerate limitations in a dedicated section. However, the approach inherently assumes that different fault locations produce distinguishable patterns in client-side QoE metrics. The testbed uses a simplified ISP network rather than a full production environment, which may not capture all complexities of real-world networks. The fault localization is limited to coarse-grained classification between ISP and client network segments rather than pinpointing specific devices or links. The method requires sufficient labeled training data with known fault locations, which necessitates either a controlled testbed or extensive historical incident data with verified root causes. The accuracy range of 93-97% indicates some misclassification cases that are not deeply analyzed.

## Gaps this paper opens

The paper demonstrates fault localization at the network segment level but does not address finer-grained localization to specific components or services within those segments. The approach focuses on binary or multi-class classification of fault location but does not provide explanations for why certain QoE patterns indicate specific fault locations, limiting interpretability for operators. The temporal dynamics of fault propagation are not explicitly modeled beyond using LSTM for sequence processing. The paper does not address how the system would handle novel fault types not seen during training or how it would adapt to evolving network conditions. There is no discussion of how multiple simultaneous faults in different locations would be detected and localized. The relationship between fault severity and QoE degradation patterns is not characterized, nor is there analysis of how different types of faults within the same location might be distinguished.

## Relevance to the thesis topic

This paper is adjacent to the thesis topic as it addresses fault localization in distributed systems using observable metrics, though in the video streaming domain rather than cloud-native systems. The approach of inferring root causes from end-to-end observable effects without direct access to intermediate components parallels challenges in cloud-native environments where service owners may not have visibility into underlying infrastructure. However, the paper does not explicitly model service dependencies or use dependency graphs, which are central to the thesis framework. The temporal analysis is limited to LSTM-based sequence modeling rather than explicit causal temporal analysis of failure propagation. The coarse-grained localization between network segments differs from the fine-grained service-level root cause analysis needed in cloud-native systems. The deep learning approach could inform aspects of the thesis framework, particularly regarding how observable metrics can be used to infer hidden fault locations, but the lack of dependency modeling and the domain-specific focus on video QoE limit direct applicability to cloud-native root cause analysis.
