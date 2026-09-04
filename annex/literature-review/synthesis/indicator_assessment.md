# Indicator assessment

## 1. Temporal Causal Discovery for Multi-Root Failures

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PARTIAL | Four papers touch on temporal/multi-root aspects but none fully address time-lagged propagation delays in multi-root scenarios, suggesting sparse but not empty coverage. |
| 2. Literature volume | PASS | 120 papers in corpus with 4 directly relevant papers cited provides sufficient foundation for literature review and positioning. |
| 3. Scientific value | PASS | Outcome is genuinely uncertain as temporal methods could fail to outperform static methods if propagation delays are too variable or confounded by network jitter. |
| 4. External validation | PASS | Train-Ticket benchmark and AIOps Challenge datasets are named external sources with documented fault injection sequences providing reproducible ground truth for 50+ cases. |
| 5. Falsifiability and reproducibility | PASS | Research question follows 'does X outperform Y under Z' form with clear success criteria comparing temporal versus static causal inference methods on multi-fault scenarios. |
| 6. Methodology fit | PASS | Distributed tracing timestamps and fault injection sequences provide independent ground truth separate from the causal discovery algorithm being evaluated. |
| 7. Hobby project test | PASS | Requires implementing non-trivial temporal causal discovery algorithms, processing large-scale distributed traces, and statistical validation infrastructure beyond weekend scope. |

**Overall**: refine

## 2. Cross-Modal Dependency Graph Construction from Heterogeneous Telemetry

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PASS | 120 papers searched with only 4 papers touching related aspects (multi-relational graphs, LLM construction, causal hypergraphs, topology-aware RCA) but none systematically addressing cross-modal fusion for dependency discovery. |
| 2. Literature volume | PASS | Corpus of 120 papers exceeds threshold and 4 directly relevant papers indicate sparse but existing literature on dependency graph construction in cloud-native RCA. |
| 3. Scientific value | PASS | Outcome is genuinely uncertain as cross-modal fusion could introduce noise/conflicts that degrade accuracy versus simpler trace-only methods, making negative results scientifically valuable. |
| 4. External validation | PASS | Sock-Shop and Online-Boutique are named, well-documented microservice benchmarks with 20-30 services each providing reproducible ground-truth dependencies, plus controlled chaos experiments. |
| 5. Falsifiability and reproducibility | PASS | Research question follows 'does X outperform Y under Z' form with clear success criteria (accuracy of inferred dependencies against ground truth) and comparative baselines specified. |
| 6. Methodology fit | PASS | Ground truth from service mesh configs and deployment manifests is independent of telemetry-based inference, avoiding circularity and enabling objective validation of discovered dependencies. |
| 7. Hobby project test | PASS | Requires parsing heterogeneous telemetry, temporal alignment, graph fusion algorithms, dynamic updates, and multi-benchmark validation—substantial distributed systems engineering beyond weekend scope. |

**Overall**: accept

## 3. Interpretable Failure Propagation Path Reconstruction

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PARTIAL | Four papers touch on propagation path reconstruction (171, 238) and interpretability (246, 86), suggesting the cell has 2-4 related works rather than being empty. |
| 2. Literature volume | PASS | Corpus contains 120 papers with 4 directly relevant to propagation path reconstruction and interpretability, exceeding minimum thresholds. |
| 3. Scientific value | PASS | Outcome is genuinely uncertain as paper 238 shows 3% failure cases and paper 86 reveals dramatic performance gaps, making negative results plausible. |
| 4. External validation | PASS | RCAEval benchmark is named with 100+ scenarios, and human evaluation with 20+ SREs provides specific external validation sources with reproducible cases. |
| 5. Falsifiability and reproducibility | PASS | Research question follows 'does X outperform Y' form with clear success criteria (operator ratings on completeness, trustworthiness, actionability) enabling falsification. |
| 6. Methodology fit | PASS | Ground truth from fault injection experiments is independent of reconstruction algorithm, and human evaluation provides external validation beyond self-assessment. |
| 7. Hobby project test | PASS | Multi-hop graph algorithms, heterogeneous telemetry aggregation, human evaluation protocols, SRE recruitment, and rigorous user studies require substantial sustained research effort. |

**Overall**: refine

## 4. Adaptive Temporal Window Selection for Anomaly Correlation

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PARTIAL | Only 4 papers cited as evidence from 120-paper corpus; insufficient search depth to confirm gap is not addressed elsewhere in the literature. |
| 2. Literature volume | PASS | 120 papers in corpus exceeds minimum threshold and topic area (cloud-native RCA) has sufficient research activity for meaningful contribution. |
| 3. Scientific value | PASS | Outcome is genuinely uncertain as adaptive windows could underperform fixed windows in high-noise environments or with insufficient training data, making negative results scientifically valuable. |
| 4. External validation | PASS | AIOps Challenge datasets are named external sources with 200+ documented incidents, and controlled chaos experiments provide independent ground truth through externally recorded injection timestamps. |
| 5. Falsifiability and reproducibility | PASS | Research question follows 'does X outperform Y under Z' structure with measurable success criteria (correlation accuracy, false positive rates) enabling clear pass/fail determination. |
| 6. Methodology fit | PASS | Ground truth from fault injection timestamps and postmortem analysis is independent of the window selection algorithm being evaluated, avoiding circularity. |
| 7. Hobby project test | PASS | Requires multiple substantial technical components including ML models for delay distribution, adaptive algorithms for non-stationary patterns, large-scale time-series processing, and extensive parameter analysis. |

**Overall**: refine

## 5. Remediation Strategy Selection with Dependency-Aware Impact Analysis

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PARTIAL | Four papers touch on remediation automation but none explicitly address dependency-aware impact prediction, suggesting a sparse rather than empty cell in the literature matrix. |
| 2. Literature volume | PASS | Corpus contains 120 papers with 4 directly relevant to remediation strategies, meeting the minimum threshold for adequate literature coverage. |
| 3. Scientific value | PASS | Outcome is genuinely uncertain as dependency-aware impact prediction could either reduce side effects or introduce computational overhead that delays recovery, with plausible negative results. |
| 4. External validation | PARTIAL | Production postmortems from open-source projects are named as validation source with estimated 50+ cases, but specificity is limited to 'open-source projects' without naming concrete repositories or datasets. |
| 5. Falsifiability and reproducibility | PASS | Research question follows 'does X outperform Y' structure with measurable success criteria (reduced side effects, improved recovery time) that can definitively succeed or fail. |
| 6. Methodology fit | PASS | Ground truth is established through actual production outcomes and controlled experiments with independent system state monitoring, avoiding circular validation. |
| 7. Hobby project test | PASS | Requires building dependency simulation models, impact propagation algorithms, integration with execution frameworks, multi-scenario experiments, and complex distributed systems infrastructure beyond weekend-scale effort. |

**Overall**: refine

## 6. LLM-Based Causal Reasoning Validation for RCA

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PARTIAL | Four papers identified explore LLM-based RCA but none rigorously validate causal reasoning versus pattern matching, suggesting sparse but not empty coverage. |
| 2. Literature volume | PASS | Corpus contains 120 papers with 4 directly relevant to LLM-based RCA validation, meeting minimum thresholds for both total and relevant literature. |
| 3. Scientific value | PASS | Outcome is genuinely uncertain as LLMs could plausibly fail at causal reasoning and underperform statistical methods, avoiding predictable results. |
| 4. External validation | PASS | Synthetic causal graphs with known ground truth (100+ structures) and established causal discovery algorithms provide specific, reproducible external validation sources. |
| 5. Falsifiability and reproducibility | PASS | Research question follows 'does X outperform Y under Z' form with clear success criteria comparing LLM performance against statistical baselines on controlled experiments. |
| 6. Methodology fit | PASS | Ground truth from synthetic graphs and statistical causal inference baselines are independent of LLM predictions, avoiding circular validation. |
| 7. Hobby project test | PASS | Requires multiple technical components including synthetic graph generation, baseline implementations, prompt engineering, distribution shift analysis, and statistical testing beyond weekend scope. |

**Overall**: refine

## 7. Failure Propagation Chain Reconstruction for Root Cause Analysis in Cloud-Native Systems

| Indicator | Verdict | Justification |
| --- | --- | --- |
| 1. Demonstrated gap | PASS | Five papers examined, none explicitly reconstruct time-ordered failure propagation chains with temporal lag analysis between dependent services. |
| 2. Literature volume | PASS | Corpus contains 120 papers with five directly relevant works addressing causal analysis and propagation in cloud-native RCA. |
| 3. Scientific value | PASS | Outcome is uncertain—temporal ordering could add noise or latency without improving accuracy, making negative results scientifically plausible. |
| 4. External validation | PASS | Train-Ticket benchmark specifies 64 services with documented fault scenarios and AIOps 2022 provides 100+ incidents with timestamped ground truth propagation sequences. |
| 5. Falsifiability and reproducibility | PASS | Research question specifies measurable Recall@5 comparison between temporal chain reconstruction and static topology-based RCA on named benchmarks with clear success criteria. |
| 6. Methodology fit | PASS | Ground truth propagation sequences come from independent published benchmarks not constructed by the researcher, eliminating circularity in evaluation. |
| 7. Hobby project test | PASS | Requires temporal graph engine implementation, OpenTelemetry integration, validation across two distinct multi-service benchmarks, and controlled ablation studies—substantial sustained effort. |

**Overall**: accept

