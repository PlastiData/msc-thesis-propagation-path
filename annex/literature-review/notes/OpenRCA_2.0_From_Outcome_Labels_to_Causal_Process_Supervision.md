---
title: "OpenRCA 2.0: From Outcome Labels to Causal Process Supervision"
authors: "Aoyang Fang et al."
arxiv: "2606.27154v2"
source_pdf: "https://arxiv.org/pdf/2606.27154v2.pdf"
converted: "2026-08-02"
note: "Converted from the official arXiv PDF (clean LaTeX source). The local Downloads copy was an HTML-print PDF and was not used."
---

# **OpenRCA 2.0: From Outcome Labels to Causal Process Supervision** 

**Aoyang Fang Yifan Yang Jin’ao Shang**<sup>_∗_</sup> **Qisheng Lu Junjielung Xu** Rui Wang Songhan Zhang Yuzhong Zhang Boxi Yu<sup>_¶_</sup> Pinjia He<sup>_‡∗_</sup> The Chinese University of Hong Kong, Shenzhen aoyangfang, yifanyang6, qishenglu, junjielongxu, 224040299, 222010549, yuzhongzhang@link.cuhk.edu.cn 

> _∗_ jinao_s@stu.xjtu.edu.cn _¶_ boxi.yu@lero.ie _‡_ hepinjia@cuhk.edu.cn 

## **Abstract** 

Root cause analysis (RCA) poses a holistic test of LLM agentic capabilities, such as long-context understanding, multi-step reasoning, and tool use. However, existing datasets suffer from a fundamental gap: they label only the root cause, not the propagation path connecting it to the observed symptom, which largely simplifies the task to naive pattern matching. To support rigorous evaluation, we introduce PAVE, a step-wise labeling protocol that leverages known interventions from fault injection to reconstruct causal propagation paths. The mechanism is _forward verification_ : reasoning from cause to effect rather than inferring backward from symptoms. Applying PAVE yields OpenRCA 2.0 (500 instances), the first crosssystem RCA benchmark with step-wise causal annotations for LLM agents. Across 11 frontier LLMs, recovering the exact root-cause set succeeds in only 20.7% of cases on average. To locate where this difficulty lies, we relax the criterion and find what we call the _ungrounded diagnosis_ : agents identify at least one correct root-cause service in 76.0% of cases but ground that service in a verified causal propagation path to the observed symptom in only 61.5%. Outcome-only evaluation hides this failure mode; step-wise causal ground truth is the missing piece for trustworthy LLM-based RCA agents. 

## **1 Introduction** 

_Root cause analysis_ (RCA), pinpointing which component caused a failure in a large software system, has emerged as a demanding testbed for LLM agents [1–4]. The originating fault is rarely where symptoms first appear: modern cloud applications are split into dozens of small components communicating over the network [5], so a local fault can cascade through callers and reach distant parts of the system before any human notices. From this cascade, the agent receives heterogeneous telemetry: request traces showing how each request propagated, time-series metrics, and free-form logs. It must reason backward from this telemetry to the originating fault. 

To evaluate such reasoning, all widely used RCA benchmarks build labeled data through _fault injection_ : the procedure deliberately breaks a known component (e.g., throttling its CPU, delaying its network, crashing its process), records the resulting telemetry, and treats the broken component as the ground-truth label [6, 7, 2]. Evaluation then scores only the outcome: whether the agent identified the correct component (Figure 1). The derivation that produced this answer is not examined. 

Scoring the derivation rather than just the outcome reveals what we call the _ungrounded diagnosis_ : the agent identifies a correct root-cause service without a verified causal propagation path linking it to the observed failure. Detecting it at scale requires step-wise causal ground truth, but building it runs 

> _∗‡_ Corresponding author. 

Preprint. 







<!-- Start of picture text -->
Healthy do (Seat = NetworkDelay)<br>Window: [to, to+5min] Pave verified<br>Unhealthy Process-level Eval  (ours)<br>Path Reachability=False<br>Edge predicted=0.33<br>Ground Truth Path Seat Travel Order Gateway Correct Answer, Wrong reason<br>✗ Outcome-only  (prior work)<br>Agent Predicted Path Seat Order Gateway Root Cause = Seat  ✓<br>Hallucinated edge Score: Pass@1=1.0<br>Travel  skiped<br><!-- End of picture text -->

Figure 1: An _ungrounded diagnosis_ on the running NetworkDelay failure in Seat service. From the known intervention (top), PAVE reconstructs the verified causal path Seat _→_ Travel _→_ Order _→_ Gateway (middle). The agent names the correct root cause but produces a graph that skips Travel (bottom): outcome-only evaluation scores this as a success, whereas processlevel evaluation surfaces the missing edge. 

into the agent’s problem: from telemetry alone, an annotator would still have to reason backward from cascading effects to the originating fault, since many faults can produce similar telemetry. But fault-injection records hand the annotator one thing the agent never sees: the intervention that started the cascade [8]. This information asymmetry [9] turns the annotator’s task from inference into _forward verification_ : with the cause given, check which downstream effects actually followed. 

We turn this insight into PAVE (Path Annotation via Verified Effects), an annotation protocol that reconstructs verified causal propagation paths from fault-injection recordings. No single signal is sufficient: a structurally plausible chain may not actually have carried the failure, a statistical co-occurrence may be coincidental, and aligned timing alone does not imply a causal link. PAVE therefore admits a candidate path only when it satisfies all three conditions jointly: conformance to known propagation mechanisms (structural), statistically significant deviation from a pre-injection baseline (statistical), and upstream-to-downstream timing alignment (temporal). Admitted paths thus carry consistent structural, statistical, and temporal evidence (Section 2.3). 

Applying PAVE across 3 architecturally distinct microservice systems (TrainTicket, the OpenTelemetry Demo, and DeathStarBench Hotel Reservation) and 27 fault types yields OpenRCA 2.0, the first cross-system RCA benchmark with step-wise causal annotations: 500 evaluable instances carrying 7.5 verified causal edges on average. 

On OpenRCA 2.0, the gap between identifying a correct service and grounding it in a verifiable path is substantial across frontier LLMs. Averaged across 11 such models, agents recover the exact root-cause set in only 20.7% of cases. To locate where this difficulty lies, we relax the criterion: identifying at least one correct root-cause service rises to 76.0%, but grounding that service in a verified causal propagation path to the observed symptom is satisfied in only 61.5%, leaving roughly one in five correct identifications ungrounded. Outcome-only evaluation hides this failure mode; step-wise causal ground truth is the missing piece for trustworthy LLM-based RCA agents. 

## **2 PAVE: Path Annotation via Verified Effects** 

A microservice system runs as a directed dependency graph over services, pods, and hosts (Figure 2a), and a fault at one node propagates along two distinct channels: horizontally along RPC call chains, and vertically across shared infrastructure. The diagnosing agent sees only the telemetry these channels leave behind (traces, metrics, and logs; Figure 2b) and must reason backward to the originating fault. 

We now describe the PAVE pipeline (Figure 3). Given fault injection records and the system dependency graph, it reconstructs verified causal propagation paths in two phases that together enforce three conditions on every admitted path. _Structural Pruning_ (Section 2.2) enumerates candidate paths consistent with the topology and a propagation rule set, enforcing _mechanism conformance_ . _Causal Verification_ (Section 2.3) then checks each candidate against pre-injection telemetry, enforcing _statistical deviation_ and _timing alignment_ jointly. 

For each injection, PAVE consumes three inputs (the dependency graph _G_ , raw telemetry **O**<sup>(</sup><sup>_t_)</sup> over the injection window, and the recorded intervention _do_ ( _vroot_ )) and emits one output: a verified path 

2 





<!-- Start of picture text -->
Inject: NetworkDelay<br>Traces (call chains) 3020ms Timeout<br>Gateway Order Travel 3050ms Travel Seat<br>Gateway Order<br>MySQL<br>Healthy MySQL Seat<br>Metrics (time series)<br>Unhealthy Runs on Runs on InjectionWindow Seat.p99_latency<br>[Node-1] [Pod-A] [Pod-B] t0 t0+dt t0+2dt<br>Logs (text events)<br>[ERROR] Travel: upstream timeout from Seat (3012ms<br>Horizontal: service  →  service (RPC) > 2000ms)<br>Vertical: infra  →  service (resource contention) [WARN] Seat: connection reset by peer<br><!-- End of picture text -->

Figure 2: The RCA setting. **(a)** A microservice system forms a two-layer dependency graph. A fault injected at Seat cascades along the RPC chain (Seat _→_ Travel _→_ Order) and may also propagate vertically through shared infrastructure (e.g., co-located pods). **(b)** The agent observes only telemetry (traces, metrics, logs) and must reason backward to the originating fault; the intervention itself is hidden. 

set Π<sup>_∗_</sup> . Phase 1 builds an intermediate candidate set Π _cand_ from topology and the rule set; Phase 2 yields Π<sup>_∗_</sup> _⊆_ Π _cand_ by verifying survivors on telemetry. Each injection in OpenRCA 2.0 carries Π<sup>_∗_</sup> as its step-wise annotation. 

### **2.1 Setup: Forward Verification from a Known Intervention** 

We model a microservice system as a directed dependency graph _G_ = ( _V, E_ ) over services, pods, and hosts (Figure 2a), with edges encoding invocation or resource dependencies (channels and modalities in Appendix B.5). Fault propagation is a structural causal process over _G_ [8]: anomalies propagate along edges with finite delay (full equation in Eq. (2), Appendix D.1). An RCA agent observes only telemetry **O** _obs_ and must jointly infer the dependency structure, the root cause, and the propagation path: an inherently _backward_ abductive problem. PAVE, by contrast, has access to the intervention _do_ ( _vroot_ ) (target component, fault type, injection window [ _t_ 0 _, t_ 0+∆ _t_ ], and parameters), giving it a strictly richer information set: 



Knowing the intervention turns an ill-posed inverse problem into a well-posed _forward_ verification task: confirming that observed anomalies are consistent with the known intervention propagating through _G_ . The verified causal subgraph _G_<sup>_∗_</sup> (formed by the edges of all paths in Π<sup>_∗_</sup> ) is the processlevel ground truth (GT) against which agent reasoning is evaluated. 

### **2.2 Phase 1: Structural Pruning** 

Phase 1 produces a candidate path set Π _cand_ by enforcing topological constraints from the system dependency graph. Raw telemetry **O**<sup>(</sup><sup>_t_)</sup> is first projected onto a discrete state alphabet Σ via a nodetype-aware mapping Ψ (e.g., `HighLatency` for service nodes, `CPU_Throttled` for pods; formal definition in Appendix D.2). A propagation rule set _R_ admits only transitions between (type, state) channel pairs ( _θi_ : _si_ ) _−−−−→_ ( _θj_ : _sj_ ) backed by a known mechanism (resource contention, RPC timeout cascade, etc.). A constrained DFS over a time-expanded heterogeneous graph, whose nodes are (component, state, time) triples ( _v, s, t_ ), unrolls circular dependencies into acyclic chains, yielding Π _cand_ . The state alphabet, full rule table, and time-expansion details are in Appendix D. 

3 



<!-- Start of picture text -->
Seat<br><!-- End of picture text -->







Figure 3: **Coarse-to-Fine verification refines a cluttered observation graph into one verified causal chain.** Running TrainTicket example: the true root cause is _Seat_ , while _Route_ is a benign service that appears anomalous due to background noise. _Input._ Every observed anomaly and every potential edge are kept, so the root cause cannot be picked out. _Phase 1 (Structural Pruning)._ Edges marked _×_ are removed because the topology admits no such dependency (e.g., _Route→Seat_ ); surviving solid edges are structurally possible, but _Route_ itself is still flagged. _Phase 2 (Causal Verification)._ Each candidate is scored against a pre-injection baseline; _Route_ ’s deviation matches baseline noise and is dropped, leaving the chain _Seat→Travel→Order_ . Phase 1 asks “ _could this edge happen?_ ” (topology); Phase 2 asks “ _did this anomaly carry the signal?_ ” (baseline contrast); injections with no surviving chain are discarded, and the released artifact is the union of such chains. 

### **2.3 Phase 2: Causal Verification** 

Phase 2 produces the verified path set Π<sup>_∗_</sup> by separating genuine propagation from coincidental disturbances (e.g., periodic cron jobs) that co-occur with the injection window. For each injection, we collect normal-period telemetry on a fresh, warmed-up instance as a _Reference Baseline_ ( _Dbase_ ) immediately before injection, approximating _P_ ( _· | do_ ( _vroot_ = _∅_ )). For each node _vi_ along a candidate path _π ∈_ Π _cand_ , we apply distributional tests tailored to each metric type (Z-score for Gaussian metrics, percentile-based tests for heavy-tailed metrics; Appendix D.8). A candidate path _π_ is _verified_ only if _all_ of (i) every node along _π_ exhibits a deviation beyond its baseline screen, (ii) every consecutive edge conforms to _R_ (inherited from Phase 1), and (iii) each downstream anomaly onsets no earlier than its upstream cause hold simultaneously. 

Phase 2 admits an injection into the released artifact only when its cascade clears the joint screen end-to-end: the fault must produce an observable downstream signature (a deviation crossing the configured SLO surface), at least one rule-admitted, temporally consistent path must connect the intervention to that signature, and the pre-injection baseline must be free of drift. Cases failing any of these conditions are dropped during pipeline-level analysis. 

## **3 Experiments** 

Process-level ground truth reveals a reasoning gap in LLM-based RCA agents that outcome-only evaluation hides: across 11 frontier LLMs, correct root-cause identifications are routinely not grounded in any verified causal propagation path. 

### **3.1 Experimental Setup** 

This subsection specifies the three microservice systems we run, the fault-injection campaigns that produce the raw pool, the curation that yields OpenRCA 2.0, and the agent design under evaluation. 

**Systems and Faults.** We evaluate on 3 architecturally distinct microservice systems: _TrainTicket_ [5], _Hotel Reservation_ from DeathStarBench [10], and the _OpenTelemetry Demo_ (OTel Demo) application [11], spanning different language stacks and synchronous/asynchronous communication patterns; deployment specifications are in Appendix B. For each system we run fault-injection workloads covering 27 chaos primary kinds across application, resource, network, and pod-level faults (per-system taxonomies in Appendix C.2); for TrainTicket we build on the released dataset of Fang et al. [7] and augment it with new campaigns on the other two systems. The resulting raw pool comprises 8137 

4 

Table 1: **OpenRCA 2.0 by system.** The three systems differ in size (9–44 services), language stack, and typical propagation depth, so the 500 instances cover distinct architectures rather than re-sampling one. Cluster configuration in Appendix D.4; raw pool sizes and silent-injection rates in Appendix A. 

|**Property**|**TrainTicket**|**OTel Demo**|**Hotel Res.**|**Total**|
|---|---|---|---|---|
|Services in system|44|15|9||
|Implementation|Java/REST|polyglot/gRPC+Kafka|Go/gRPC||
|Evaluable instances|320|38|142|500|
|Distinct chaos primary kinds|25|9|5|27|
|Mean longest propagation path|3.0|2.5|2.1|2.7|
|Avg. causal edges per instance|10.1|3.0|2.7|7.5|



injected runs. After filtering silent injections, we apply the PAVE pipeline (Section 2) to the survivors and curate OpenRCA 2.0 (500 instances) by stratified selection on (system, chaos family, root service) with per-stratum caps and additional structural screens (full rules in Appendix A). Table 1 reports per-system breakdowns; the Datasheet is in Appendix A. 

**Ground Truth.** Causal propagation paths are extracted automatically using the pipeline described in Section 2; their reliability is bounded by the two-annotator manual audit reported in Section 3.4. 

**Agent Design.** All evaluated agents follow a tool-augmented ReAct-style [12] architecture, adopted from the Deep Research agent [13]. To isolate LLM reasoning capability from tooling effects, all models share an identical tool suite over the released telemetry and identical prompt templates; no dependency graph is provided. Each diagnosis is returned as structured output: root-cause claims and propagation edges, each paired to a re-executable SQL query as evidence (full schema, tool definitions, and prompts in Appendix F and F.3). 

### **3.2 Benchmark Utility: Process-Level Evaluation of RCA Agents** 

This subsection grades 11 frontier LLMs against OpenRCA 2.0 along outcome and process layers and reads three patterns out of the pooled results: outcome scores understate the failure (Finding 1), process-level Edge F1 is universally lower than Node F1 (Finding 2), and no single backbone dominates (Finding 3). 

**Experimental Design.** We evaluate the RCA agent architecture above with 11 frontier LLMs as backbones spanning closed-source and open-source families across Anthropic, Google, ByteDance, Xiaomi, Zhipu, Moonshot, DeepSeek, Alibaba, Tencent, and MiniMax: Claude Opus 4.7, Gemini 3.1 Pro, Claude Sonnet 4.6, MiMo 2.5 Pro, GLM 5.1, Kimi K2.6, DeepSeek V4 Pro, Qwen3.6-Max, Hy 3.0 Preview, Seed 2.0 Pro, and MiniMax M2.7. Each model receives multi-modal telemetry (traces, metrics, logs) and must diagnose the root cause while explaining the failure propagation as a causal graph. 

**Evaluation Metrics.** We grade each diagnosis along two complementary layers (formal definitions in Appendix G). The _outcome layer_ scores the agent’s predicted root-cause set against ground truth: _Exact Match_ (EM) requires the predicted set to match ground truth exactly; _F1_ , _Precision_ , and _Recall_ are mean fractional scores over the (service, fault_kind) pair set; _AnySvc_ is the case-level rate of naming at least one correct root-cause service ignoring fault kind, the most lenient outcome score and a service-only relaxation of Recall. The _process layer_ scores the agent’s reasoning: _Path Reachability_ (PR) is satisfied when the agent both names at least one correct root-cause service _and_ draws a valid path through its predicted causal graph from that service to a ground-truth alarm node, a component observed to behave abnormally during the injection window; _Node F1_ and _Edge F1_ score the predicted causal graph _G_<sup>ˆ</sup> against _G_<sup>_∗_</sup> under exact matching; _SQL Exec_ is the share of agent-emitted evidence SQL queries that execute cleanly. PR is the most lenient process metric: it requires only one valid path from a single correct anchor, not the full graph. We reserve the term _ungrounded diagnosis_ for cases that satisfy AnySvc but not PR: a correct root-cause identification not grounded in a verified causal propagation path to the observed symptom. 

**Results.** Three patterns govern the pooled results in Table 2. First, outcome-level scores are already low (mean F1 reaches only 34 _._ 1% and EM only 20 _._ 7% across the 11 models), yet outcome alone obscures the underlying failure: agents name a correct service in 76 _._ 0% of cases (AnySvc), and 

5 

Table 2: Outcome- and process-level evaluation on OpenRCA 2.0 pooled across 3 systems ( _n_ =500, percentages). **Bold** marks the per-column maximum. Metric definitions in Section 3.2; per-system breakdown in Appendix Table 8. 

||||_Outcom_|_e_||||_Process_||
|---|---|---|---|---|---|---|---|---|---|
|Model|EM_↑_|F1_↑_|Precision_↑_|Recall_↑_|AnySvc_↑_|PR_↑_|Node F1_↑_|Edge F1_↑_|SQL Exec_↑_|
|Claude Opus 4.7|27.6|41.4|45.7|40.1|**82.6**|70.0|67.5|49.5|97.5|
|Gemini 3.1 Pro|**29.4**|**43.8**|**50.4**|**40.7**|82.0|70.4|**67.9**|36.8|**98.8**|
|Claude Sonnet 4.6|26.2|40.5|45.7|38.5|79.4|52.6|64.5|48.0|95.6|
|MiMo 2.5 Pro|22.8|35.9|40.1|34.8|77.8|59.6|64.3|44.9|92.0|
|GLM 5.1|21.6|34.0|38.3|32.4|79.0|69.6|66.9|**50.4**|93.4|
|Kimi K2.6|21.0|34.0|38.4|32.6|70.8|63.2|58.8|44.1|82.4|
|DeepSeek V4 Pro|20.4|32.0|36.9|29.7|65.6|53.0|53.5|40.1|74.9|
|Qwen3.6-Max|19.2|35.7|40.5|34.9|79.2|**71.8**|65.1|48.5|92.9|
|Hy 3.0 Preview|17.4|30.1|33.4|30.2|71.0|53.4|55.9|38.3|92.1|
|Seed 2.0 Pro|14.8|26.8|30.1|26.6|78.6|66.4|64.5|47.7|90.6|
|MiniMax M2.7|6.8|20.6|19.7|24.2|69.8|46.4|55.3|29.2|86.9|



the gap between this lenient outcome score and the most lenient process score (61 _._ 5% PR) reveals what we call the _ungrounded diagnosis_ (Finding 1). Second, within the process layer mean Edge F1 (43 _._ 4%) trails mean Node F1 (62 _._ 2%) by 18.8 pp for every model, indicating that agents identify participating services more reliably than the directed dependencies among them (Finding 2). Third, the per-column extrema are distributed across four different models with distinct recall and precision profiles, so no single backbone dominates and the appropriate ranking depends on the downstream verification cost (Finding 3). The per-system spread is wider than the cross-model spread (Hotel Reservation approaches saturation on the outcome layer for the top tier, whereas TrainTicket leaves a 30+ pp gap on the process-level metrics); we therefore keep the main table pooled to support a single comparable model ranking and report the per-system breakdown in Appendix Table 8. 

**(1) Outcome scores understate the failure: the lenient process check exposes ungrounded diagnoses.** The outcome layer pools two distinct failure modes into one number. On the lenient end, AnySvc reaches 76 _._ 0% on average, showing that agents routinely name a correct root-cause service. The strict outcome metrics, however, collapse: pair-level F1 falls to 34 _._ 1% and EM to 20 _._ 7%, with the drop from AnySvc (76 _._ 0%) to Recall (33 _._ 2%) dominated by mislabelled fault kinds on services the agent did identify. The decisive evidence that this gap is a _reasoning_ failure rather than a labelling artefact comes from the process layer: even PR, which requires only one valid path from a single correct anchor, is satisfied in only 61 _._ 5% of cases, so for 14.5 pp of cases the agent names a correct service _without_ drawing any verifiable path to the observed symptom. The per-model conditional rate PR _/_ AnySvc separates models that outcome-only grading rates as comparable: Qwen3.6-Max attains 71 _._ 8 _/_ 79 _._ 2 _≈_ 91%, whereas Sonnet 4.6 attains only 52 _._ 6 _/_ 79 _._ 4 _≈_ 66% despite comparable F1, indicating that Sonnet emits correct service labels that are not integrated into a connected propagation path. 

**(2) Edge F1 is universally lower than Node F1, and the gap is the size of the entire process-level signal.** The ordering holds for every model in the table, and the gap is substantial in absolute terms (62 _._ 2% vs. 43 _._ 4%, 18.8 pp on average). Gemini exhibits the widest split, reaching 67 _._ 9% Node F1 but only 36 _._ 8% Edge F1. Identifying the participating services approximates a classification task that pre-training prepares the model for; ordering them into a directed propagation path requires reasoning about what each abnormal signal implies for the underlying inter-service dependencies, a derivation step that outcome-only metrics do not score. This separation provides direct evidence that the agent’s _output_ (a service list) is closer to ground truth than its _derivation_ (a directed graph), and that the discrepancy is large enough to affect model selection in practice. 

### **3.3 Failure Mode Characterization** 

To probe what drives the shortfall between AnySvc and PR, we read agent trajectories across the 11 models on a stratified sample of cases tiered by joint correctness (the fraction of models clearing _F_ 1 _>_ 0 on each case). Three patterns recur across the sample, each describing how an agent commits to an incorrect or unsupported answer rather than continuing to verify, and together they account for the dominant share of ungrounded diagnoses. 

6 



<!-- Start of picture text -->
(a) Ground Truth (b) LLM Prediction<br>ts-basic-service ts-basic-service<br>ts-travel2service ts-travelservice Hallucinated<br>ts-route-plan ts-route-plan<br>service service<br>ts-travel-plan ts-travel-plan<br>service service<br>ts-ui-dashboard ts-ui-dashboard<br><!-- End of picture text -->

Figure 4: Spurious causal reasoning case. (a) Ground truth shows fault propagation through intermediate services ( `travel` , `travel2` ). (b) Claude correctly identifies root cause and symptoms but hallucinates a direct edge, missing the branching structure (Edge F1=44.4%). 

**(1) Premature commitment under under-exploration.** After identifying one plausible root cause, the agent stops investigating and emits the answer, leaving co-occurring faults or alternative attributions unexamined. This shape is most visible on hybrid injections that pair one prominent fault with one subtle one: every evaluated model converges on the prominent half (often emitting nearly identical wording across heterogeneous backbones) and uniformly misses the subtle half, depressing Recall and EM whenever the ground truth covers more than one service. 

**(2) Presence bias on observable activity.** Agents weight evidence by what they see and treat absence of observed activity as evidence of normal operation, rather than recognizing that the absence itself can be the fault signature. A killed-pod injection makes this failure mode crisp: during the incident window the affected service stops producing spans entirely, and many agents read the resulting silence as “this service has no errors, hence no fault here”, then attribute the incident to the upstream callers that surface errors precisely because their callee disappeared. The dual of Pattern (3): attentional bias toward strong positive signals and against silent ones jointly explain the bulk of the localization shortfall. 

**(3) Salience capture on the loudest signal.** Agents converge on the service whose error or latency aggregates carry the strongest abnormal-versus-normal delta, even when those signals are pure downstream amplification rather than the originating fault; this pattern accounts for the bulk of the localization failures responsible for AnySvc falling short of full coverage by roughly 24pp. The capture operates on aggregate metrics (a high-traffic hub on the load-generator path absorbs attention while the lower-traffic ground-truth service goes unnamed) and equally on text: a SEVERE log line claiming a timeout is taken at face value by most models even when the corresponding trace span returns in tens of milliseconds and contradicts the log claim. 

The case study below illustrates Pattern (1) on the path-drawing dimension specifically: an agent commits to the correct service and stops verifying, leaving the propagation chain to skip the intermediates that the verified ground truth actually traverses. 

**Case Study: An Ungrounded Diagnosis.** Figure 4 shows an injection where Claude correctly names the root cause (ts-basic-service) but justifies it with a graph that skips the services actually on the 4-hop ground-truth propagation path: a paradigmatic ungrounded diagnosis. The predicted graph hallucinates a direct edge from ts-basic-service to ts-route-plan-service, skipping the intermediate ts-travel2-service and ts-travel-service (Node Precision/Recall 100%/66.7%, Edge Precision/Recall 66.7%/33.3%, Edge F1 44.4%). Outcome-only evaluation scores this as a hit on AnySvc; process-level evaluation surfaces the missing edges and exposes the reasoning failure an on-call engineer would still hit in practice. 

### **3.4 Annotation Reliability** 

A two-annotator manual audit on _N_ =100 instances drawn uniformly at random from OpenRCA 2.0 reports 94% case-level agreement (94 _/_ 100) on the validity of _G_<sup>_∗_</sup> , with every disagreement attributable to under-coverage of weakly supported paths rather than to a spurious included edge. Two of the paper’s authors, with prior experience in distributed-system observability and the PAVE schema, independently rated each case as AGREE when every edge in _G_<sup>_∗_</sup> is plausibly causal from the telemetry 

7 

and no obvious propagation edge is missing, and DISAGREE otherwise; annotators were blind to one another’s verdicts. All six disagreements were one-directional: at least one annotator considered an additional propagation path plausible that the verification gates had rejected as weakly supported, and no case was flagged for an implausible included edge. Joint adjudication attributed every under-coverage instance to the conjunctive design’s deliberate strictness on borderline evidence; for a process-level reference, omitting weakly supported edges is preferable to admitting spurious ones, so we accept this precision-favoured trade-off. The full protocol, verification procedure, and per-disagreement notes are in Appendix E.1. 

## **4 Related Work** 

### **4.1 From Classification-Based Ranking to Generative Reasoning** 

The formulation of Root Cause Analysis (RCA) has undergone a fundamental shift. Traditionally, RCA was cast as a _multi-class classification problem_ , where each candidate component is scored and ranked by its likelihood of being the root cause, using heuristic algorithms (e.g., Random Walk [14]) or supervised graph neural networks [15]. While effective for locating faults, these “black-box” approaches lack interpretability and fail to capture the sequential propagation mechanism. With the advent of Large Language Models (LLMs), recent works have pivoted towards a _generative reasoning paradigm_ [1–4], treating RCA as a causal narrative generation task. However, a critical misalignment persists: while the model architecture has evolved to handle complex reasoning, the underlying data supervision remains stagnant. Existing benchmarks [6, 7, 2] still rely on outcome-based labels that record only _which_ component is the root cause, without annotating _how_ the fault propagates, inherited from the classification era. This forces reasoning agents to optimize for the final answer directly, bypassing the logical derivation steps and encouraging the memorization of spurious correlations rather than learning robust causal dynamics. 

### **4.2 Causal Structure Learning under Intervention** 

Our work intersects with causal discovery, particularly in dynamic systems. Classical observational methods (e.g., PC algorithm [16]) struggle to recover Directed Acyclic Graphs (DAGs) in distributed systems due to unobserved confounders and high-dimensional noise [17, 18]. Pearl’s hierarchy of causation posits that interventional data ( _do_ ( _x_ )) is essential for distinguishing true causality from mere correlation [8]. While some RCA methods attempt to infer causal graphs relying solely on observational telemetry [19, 20], they lack the _identifiability_ guarantees that controlled interventions provide. PAVE distinguishes itself by adopting an _interventional_ rather than purely observational perspective during annotation. While prior benchmarks use only the identity of the injected component as the ground-truth label, PAVE leverages the full intervention specification ( _do_ ( _vroot_ )) to actively verify propagation paths. This effectively transforms the intractable structure learning problem into a tractable verification task, filtering out silent injections and confounding noise that plague purely observational datasets. 

### **4.3 Process Supervision and Verifiability** 

In the broader LLM landscape, focus is shifting from outcome-based supervision (Outcome Reward Models, ORMs) to _Process Supervision_ (Process Reward Models, PRMs) [21–23]. Research in mathematical reasoning and code generation demonstrates that providing step-by-step verification signals significantly reduces hallucinations and improves generalization [24, 25]. However, applying this to system diagnostics is hindered by the _verification gap_ : unlike math (where proofs are deterministic) or code (where unit tests exist), operational faults lack a natural “compiler” to verify reasoning steps. Current RCA benchmarks like AIOpsLab [2] or OpenRCA [1] rely on human-curated scenarios or heuristically filtered logs, which are hard to scale and lack granular process labels. PAVE addresses this verification gap for system diagnostics by synthesizing verifiable failure propagation paths rooted in system topology and causal interventions, producing the first large-scale process-level ground truth for _evaluating_ diagnostic reasoning in complex systems. The resulting step-wise annotations also open a path toward training PRMs in the reliability domain, though we leave this exploration to future work. 

8 

Table 3: Differentiation of OpenRCA 2.0 from prior RCA benchmarks. “✓” = present; “–” = absent or not reported as a fixed-size benchmark; “part.” = partial form (e.g., issue-type tag without a propagation graph). Instance counts are reported as in each source. 

|Benchmark|#Sys|#Inst.|Outcome|**Process**|SLO surface|LLM eval|
|---|---|---|---|---|---|---|
|OpenRCA 1.0 [1]|3|335|✓|–|implicit|✓|
|AIOpsLab [2]|2|48|✓|part.|implicit|✓|
|RCAEval [6]|3|735|✓|–|–|–|
|Stratus [3]|3|–|✓|–|implicit|✓|
|Fang et al. [7]|1|8137|✓|–|implicit|–|
|**OpenRCA 2.0 (ours)**|3|500|✓|✓|**explicit**|✓|



**Differentiation summary.** Table 3 compares OpenRCA 2.0 to five prior RCA benchmarks on seven axes. Two columns separate our work from prior benchmarks. _Process annotations_ record the step-wise causal edges of each cascade rather than only the root-cause identity; AIOpsLab provides a partial form (issue-type tags without a propagation graph), and the others provide none. The _SLO surface as an explicit method input_ promotes a threshold that prior work fixes implicitly into a configurable knob. 

## **5 Assumptions and Threats to Validity** 

This section delimits OpenRCA 2.0’s claims along three axes: the input conditions PAVE relies on, the residual threats internal to the pipeline, and the boundary of external transfer. 

**Input assumptions.** Four falsifiable conditions underwrite the protocol: a real controlled intervention _do_ ( _vroot_ ) rather than an inferred label, a service-layer dependency graph complete enough that genuine horizontal propagation survives structural pruning, a propagation signature in trace, metric, or log modalities, and a pre-injection baseline that approximates the no-intervention distribution closely enough for baseline-relative anomaly screening to discriminate. Where any of these fails for a target setting, the reported numbers should be read as an upper bound rather than a transferable estimate. 

**Internal threats.** Two single-gate weaknesses remain inside the pipeline: the rule set _R_ may silently prune propagation mechanisms outside its current vocabulary, and the per-node anomaly screen is calibrated toward low false negatives (calibration split in Appendix E.2) and so admits individual nodes spuriously. Neither propagates to end-to-end errors, because admission requires the conjunction of rule consistency, baseline-relative deviation, and upstream-to-downstream timing alignment (Eq. (3)), and a two-annotator audit on a uniform-random 100-case subsample reports zero false-positive edges in the audited sample (Section 3.4). 

**External transfer.** Faithful simulation of production-scale microservice deployments is neither a goal of this benchmark nor realistically achievable inside controlled testbeds, so reported numbers apply within the testbed envelope and transfer to production must be calibrated rather than assumed. A complementary scope note concerns information conditions: PAVE’s annotation step requires full telemetry, since forward verification relies on it, but the evaluation step does not. The same step-wise ground truth, established once under full data, can be reused to evaluate agents under deliberately restricted telemetry (subsampled traces, missing modalities, truncated observation windows), turning information availability into a controllable evaluation axis that we leave to future work. 

## **6 Conclusion** 

We introduced PAVE, an annotation protocol that reconstructs verified causal propagation paths from fault-injection experiments by exploiting the information asymmetry between backward RCA and forward verification from a known intervention. Its application across 3 architecturally distinct microservice systems yields OpenRCA 2.0 (500 instances), the first cross-system RCA benchmark with step-wise causal annotations and process-level metrics (Path Reachability, Node F1, Edge F1) that grade the _causal path_ rather than only the identified root cause. On this benchmark, processlevel evaluation of 11 frontier LLMs exposes the _ungrounded diagnosis_ , a failure mode invisible to outcome-only evaluation in which correct root-cause identifications are not grounded in any verified propagation path to the observed symptom. More broadly, step-wise causal ground truth raises the 

9 

standard from correct localization to correct reasoning, the bar any diagnostic agent must clear to be trusted where errors carry real consequences. 

## **References** 

- [1] Junjielong Xu, Qinan Zhang, Zhiqing Zhong, Shilin He, Chaoyun Zhang, Qingwei Lin, Dan Pei, Pinjia He, Dongmei Zhang, and Qi Zhang. Openrca: Can large language models locate the root cause of software failures? In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [2] Yinfang Chen, Manish Shetty, Gagan Somashekar, Minghua Ma, Yogesh Simmhan, Jonathan Mace, Chetan Bansal, Rujia Wang, and Saravan Rajmohan. Aiopslab: A holistic framework to evaluate ai agents for enabling autonomous clouds. In _MLSys_ , 2025. URL `https:// openreview.net/forum?id=3EXBLwGxtq` . 

- [3] Yinfang Chen, Jiaqi Pan, Jackson Clark, Yiming Su, Noah Zheutlin, Bhavya Bhavya, Rohan Arora, Yu Deng, Saurabh Jha, and Tianyin Xu. Stratus: A multi-agent system for autonomous reliability engineering of modern clouds. _arXiv preprint arXiv:2506.02009v2_ , 05 2025. URL `https://arxiv.org/abs/2506.02009v2` . 

- [4] Lingzhe Zhang, Yunpeng Zhai, Tong Jia, Chiming Duan, Siyu Yu, Jinyang Gao, Bolin Ding, Zhonghai Wu, and Ying Li. Thinkfl: Self-refining failure localization for microservice systems via reinforcement fine-tuning. _ACM Transactions on Software Engineering and Methodology_ , 2025. doi: 10.1145/3789262. URL `https://doi.org/10.1145/3789262` . 

- [5] Xiang Zhou, Xin Peng, Tao Xie, Jun Sun, Chao Ji, Wenhai Li, and Dan Ding. Fault analysis and debugging of microservice systems: Industrial survey, benchmark system, and empirical study. _IEEE Transactions on Software Engineering_ , 47(2):243–260, 2018. 

- [6] Luan Pham, Hongyu Zhang, Huong Ha, Flora Salim, and Xiuzhen Zhang. Rcaeval: A benchmark for root cause analysis of microservice systems with telemetry data. In _Companion Proceedings of the ACM on Web Conference 2025_ , pages 777–780, 2025. 

- [7] Aoyang Fang, Songhan Zhang, Yifan Yang, Haotong Wu, Junjielong Xu, Xuyang Wang, Rui Wang, Manyi Wang, Qisheng Lu, and Pinjia He. Rethinking the evaluation of microservice rca with a fault propagation-aware benchmark. _arXiv preprint arXiv:2510.04711v2_ , 10 2025. URL `https://arxiv.org/abs/2510.04711v2` . 

- [8] Judea Pearl. _Causality_ . Cambridge university press, 2009. 

- [9] Wei Liu, Siya Qi, Yali Du, and Yulan He. Self-play only evolves when self-synthetic pipeline ensures learnable information gain. _arXiv preprint arXiv:2603.02218v1_ , 02 2026. URL `https://arxiv.org/abs/2603.02218v1` . 

- [10] Deathstarbench. `https://github.com/delimitrou/DeathStarBench/tree/master` , 2024. Accessed: 2026-02-10. 

- [11] Opentelemetry demo. `https://github.com/open-telemetry/opentelemetry-demo` , 2026. Accessed: 2026-05-05. 

- [12] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In _The eleventh international conference on learning representations_ , 2022. 

- [13] Paichun Lin. Self-balancing agentic AI: Test-time diffusion and context engineering re-imagined for deep research. `https://github.com/thinkdepthai/Deep_Research` , 2025. 

- [14] Guangba Yu, Pengfei Chen, Hongyang Chen, Zijie Guan, Zicheng Huang, Linxiao Jing, Tianjun Weng, Xinmeng Sun, and Xiaoyun Li. Microrank: End-to-end latency issue localization with extended spectrum analysis in microservice environments. In _Proceedings of the Web Conference 2021_ , pages 3087–3098, 2021. 

10 

- [15] Songhan Zhang, Aoyang Fang, Yifan Yang, Ruiyi Cheng, Xiaoying Tang, and Pinjia He. Dynacausal: Dynamic causality-aware root cause analysis for distributed microservices. _arXiv preprint arXiv:2510.22613v1_ , 10 2025. URL `https://arxiv.org/abs/2510.22613v1` . 

- [16] Peter Spirtes, Clark N Glymour, and Richard Scheines. _Causation, prediction, and search_ . MIT press, 2000. 

- [17] Azam Ikram, Sarthak Chakraborty, Subrata Mitra, Shiv Saini, Saurabh Bagchi, and Murat Kocaoglu. Root cause analysis of failures in microservices through causal discovery. _Advances in Neural Information Processing Systems_ , 35:31158–31170, 2022. 

- [18] Xiao Han, Saima Absar, Lu Zhang, and Shuhan Yuan. Root cause analysis of anomalies in multivariate time series through granger causal discovery. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [19] Zeyan Li, Nengwen Zhao, Shenglin Zhang, Yongqian Sun, Pengfei Chen, Xidao Wen, Minghua Ma, and Dan Pei. Constructing large-scale real-world benchmark datasets for aiops. _arXiv preprint arXiv:2208.03938v1_ , 08 2022. URL `https://arxiv.org/abs/2208.03938v1` . 

- [20] Guangba Yu, Pengfei Chen, Yufeng Li, Hongyang Chen, Xiaoyun Li, and Zibin Zheng. Nezha: Interpretable fine-grained root causes analysis for microservices on multi-modal observability data. In _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , pages 553–565, 2023. 

- [21] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In _The Twelfth International Conference on Learning Representations_ , 2023. 

- [22] Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process- and outcome-based feedback. _arXiv preprint arXiv:2211.14275v1_ , 11 2022. URL `https://arxiv.org/abs/2211.14275v1` . 

- [23] Thomas Zeng, Shuibai Zhang, Shutong Wu, Christian Classen, Daewon Chae, Ethan Ewer, Minjae Lee, Heeju Kim, Wonjun Kang, Jackson Kunde, et al. Versaprm: Multi-domain process reward model via synthetic reasoning data. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [24] Zhangyue Yin, Qiushi Sun, Zhiyuan Zeng, Qinyuan Cheng, Xipeng Qiu, and Xuan-Jing Huang. Dynamic and generalizable process reward modeling. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 4203–4233, 2025. 

- [25] Yibo Yan, Jiamin Su, Jianxiang He, Fangteng Fu, Xu Zheng, Yuanhuiyi Lyu, Kun Wang, Shen Wang, Qingsong Wen, and Xuming Hu. A survey of mathematical reasoning in the era of multimodal large language model: Benchmark, method & challenges. In _Findings of the Association for Computational Linguistics: ACL 2025_ , pages 11798–11827, 2025. 

11 

**Appendix organization.** This appendix is organized into five parts. _Part I_ (Section A) is the datasetside documentation: Datasheet, including a reproducibility section. _Part II_ (Sections B–C) specifies the benchmark testbed. _Part III_ (Section D) expands the PAVE pipeline compressed in Section 2. _Part IV_ (Section E) reports the two-annotator audit on a random 100-case subsample and documents the calibration split used by the per-node anomaly screen. _Part V_ (Sections F–G) documents the evaluated RCA agents and the formal metric definitions. 

## **A Datasheet for Datasets** 

### **A.1 Motivation** 

OpenRCA 2.0 is designed for _process-level_ evaluation of LLM-based RCA agents. The goal is to assess not only whether an agent identifies the correct root cause, but also whether it can justify that diagnosis with a faithful step-wise causal propagation path. Existing RCA benchmarks typically supervise only the final outcome label, which hides the _ungrounded diagnosis_ failure mode studied in this paper. No dedicated external funding was used specifically to compile the released benchmark artifact beyond the broader research effort supporting this study. 

### **A.2 Composition** 

Each instance contains three components: (i) multimodal pre- and post-injection telemetry, including distributed traces, metric time series, and structured logs in parquet format; (ii) a structured groundtruth label specifying the originating system, the injected component, and the fault type; and (iii) a step-wise causal propagation graph over services, pods, and spans (Section 2). OpenRCA 2.0 contains 500 evaluable instances drawn from 3 architecturally distinct microservice systems and covering 27 chaos primary kinds; per-system breakdowns are reported in Table 1. Curation uses two-pass stratified selection on (system, chaos family, root service) with per-stratum caps, sorted by (longest path, edge count, services), and retains only instances that pass end-to-end causal-path verification while excluding cyclic service graphs, trivial propagation depth ( _≤_ 1), and frontend/loadgen entry points. The result is a curated, self-contained evaluation set whose sampling objective is balanced coverage rather than statistical representativeness of production incidents. 

The current release does not define train/development/test splits. Retained instances are distributed as complete telemetry packs rather than field-pruned records, so field-level missingness or redaction is not a concern within the released trace, metric, or log data. Because the benchmark consists of synthetic operational telemetry generated under controlled load, it contains no PII or human-subject data; people-related subpopulation, identity, and sensitive-attribute considerations are therefore not applicable. 

### **A.3 Collection Process** 

Faults are injected on three microservice systems: TrainTicket [5], the OpenTelemetry Demo application [11], and Hotel Reservation from DeathStarBench [10]. These interventions are run with Chaos Mesh on a shared 7-node Kubernetes cluster; per-system topology and deployment details are given in Section B, and the cluster configuration in Section D.4. For each intervention, a fresh system instance is deployed and warmed up, a pre-injection baseline window is recorded, the fault is applied over [ _t_ 0 _, t_ 0+∆ _t_ ], and post-injection telemetry is then collected. Step-wise causal labels are produced automatically by the PAVE pipeline (Sections 2.2, 2.3) and are further checked by the forward verification protocol described later in this appendix. 

Reliability of this procedure was assessed by a two-annotator audit on a uniform random 100-case subsample, with 94% case-level agreement (Section 3.4; full protocol in Appendix E). The annotators were two of the paper’s authors; no crowdworkers or paid external annotators were used. Because the benchmark is built from synthetic system telemetry rather than data about natural persons, consent, participant notification, and formal human-subject review considerations do not apply. 

### **A.4 Preprocessing, Cleaning, Labeling** 

Telemetry is exported through OpenTelemetry into standardized parquet schemas, with one file per modality per period. The released benchmark contains only injections that pass the joint screen 

12 

described in Section 2.3 (observable SLO impact, a rule-admitted propagation path, and a clean pre-injection baseline); cases failing any condition are dropped during pipeline-level analysis. The released package bundles the evaluation telemetry together with the derived labels and propagation graphs, so the released artifact is the processed benchmark itself rather than an undocumented intermediate product. 

Cleaning is performed primarily at the instance level by filtering out runs whose pre-injection baseline is itself anomalous, rather than by manually editing fields inside retained telemetry records. The software responsible for preprocessing, filtering, and label construction is the released PAVE pipeline described in Section D. Pipeline reliability rests on the conjunctive verification design analyzed in Section D.8 and is corroborated by the two-annotator audit reported in Section 3.4 (Appendix E.1). 

### **A.5 Uses** 

Intended uses include (i) process-level evaluation of LLM-based RCA agents and (ii) training process reward models in the reliability domain, where the step-wise edges provide natural supervision targets. At the time of submission, the benchmark is used only in this study as the primary evaluation suite for process-level RCA assessment. 

The benchmark is not intended for production-readiness certification of any specific RCA agent, for cross-architecture generalization claims to service-mesh, serverless, or fully event-driven systems beyond the three included testbeds, or for claims about faults that leave no telemetry signature. It should also not be used as a training corpus for the _evaluated_ RCA agents themselves, as doing so would create direct test-set leakage. 

### **A.6 Distribution and License** 

An anonymized preview of the benchmark accompanies the supplementary submission, and the anonymized full benchmark package is provided in the submission materials. Upon acceptance, the full benchmark artifact and the PAVE pipeline will be released publicly with archival metadata and integrity checksums. The released benchmark is a derived artifact constructed from a curated subset of the upstream fault-injection runs together with the additional annotations and causal-process labels introduced in this work. The dataset is released under **CC-BY-SA 4.0** , and the pipeline code under **Apache 2.0** . To the best of our knowledge, no export-control or comparable regulatory restrictions apply to the released artifact. 

### **A.7 Maintenance** 

To preserve anonymity in the submission version, direct maintainer contact details are omitted here and will be restored upon acceptance. Corrections, additional fault types, and cross-system extensions will be managed through versioned releases, and older public versions will remain archived for reproducibility. After public release, questions and fixes can be tracked through the GitHub issue tracker and pull requests. External contributions will be reviewed for schema compatibility, reproducibility, and annotation consistency before inclusion in an official release. 

### **A.8 Reproducibility** 

The complete PAVE pipeline source is released alongside the dataset, with explicit random seeds for every stochastic component (DFS tie-breaking, baseline-window selection, fault-injection scheduling) so the numbers in this paper are regeneratable; pipeline hyperparameters and detector thresholds are tabulated in Sections D.5 and D.8, and cluster configuration is in Section D.4. A single-entry-point `reproduce.sh` accompanies the anonymized submission artifact and regenerates the Section 3.2 numbers on a downloadable instance subset; full-dataset re-evaluation requires API quota for the 11 models documented in Section F.5. No pre-trained models are released as part of the benchmark. 

## **B Benchmark Systems and Topology** 

This section details the microservice systems used in our benchmark, including their architecture, scale, and the service dependency topology that defines the structural prior _G_ for causal path extraction. 

13 

### **B.1 Systems Overview** 

The benchmark spans 3 open-source microservice testbeds chosen to cover distinct propagation regimes: TrainTicket [5] for deep, layered Java/REST call chains; the OpenTelemetry Demo application [11] for polyglot gRPC services with asynchronous Kafka legs; and Hotel Reservation from DeathStarBench [10] for shallow, wide Go/gRPC services with shared in-memory caches. Together they cover three communication styles (synchronous REST, synchronous gRPC, and asynchronous queueing) and four data-store classes (relational, document, key-value cache, and message log), so the recovered ground-truth paths reflect propagation patterns that no single system would expose on its own. The subsections below summarize the topology of each system; deployment manifests, image tags, and commit hashes are released alongside the dataset. 

### **B.2 TrainTicket Service Dependency Topology** 

TrainTicket’s 44 microservices follow a layered architecture centered on REST-style service-toservice calls, with RabbitMQ used for asynchronous messaging and a shared MySQL instance supporting many backend services. At a coarse level, requests flow from user-facing entry services through gateway and orchestration layers into domain services and then into shared infrastructure, creating long dependency chains and frequent opportunities for multi-hop propagation. 

The system exhibits several properties that make RCA challenging: 

- **Deep call chains** : Booking operations traverse up to 6 service layers (Entry _→_ Gateway _→_ Orchestration _→_ Domain _→_ Foundation _→_ Infrastructure). 

- **High fan-in** : Foundation services ( `Station` , `Route` , `Train` ) are shared by many upstream callers, creating complex dependency patterns where a single failure can manifest in multiple symptom locations. 

- **Shared infrastructure** : 23 services connect to a shared MySQL 5.7 instance, introducing vertical propagation paths from database-level faults to application-level errors. 

- **Circular dependencies** : Some services exhibit mutual dependencies (e.g., `Travel` _↔_ `Seat` ) that require temporal unrolling for causal analysis. 

### **B.3 OpenTelemetry Demo Service Dependency Topology** 

The OpenTelemetry Demo is a polyglot e-commerce reference application comprising 15 application services implemented across Go, Python, Java, .NET, Ruby, and JavaScript. The deployed stack also includes supporting components such as Kafka, Postgres, valkey/Redis, and observability infrastructure, which are not counted as application services. Inter-service communication uses gRPC for synchronous request paths (e.g., `cart` _→_ `checkout` _→_ `payment` ) and Kafka for asynchronous fanout (e.g., `checkout` _→_ `accounting` / `fraud-detection` ); state is held in Postgres, valkey/Redis, and the Kafka log itself. 

Properties relevant for fault propagation: 

- **Polyglot error semantics** : each language stack surfaces failures differently (Java stack traces, Go panics, Python tracebacks, .NET exceptions), exercising the rule set across heterogeneous log formats. 

- **Synchronous + asynchronous mix** : faults injected upstream of the Kafka boundary propagate as queue back-pressure rather than RPC timeouts, producing a propagation signature absent from the REST-only TrainTicket. 

- **Shared infrastructure** : Postgres and valkey are accessed by multiple services; an injected database fault produces correlated anomalies across otherwise unrelated request paths. 

### **B.4 Hotel Reservation Service Dependency Topology** 

Hotel Reservation, drawn from DeathStarBench [10], consists of 9 Go services that communicate via gRPC and rely on MongoDB and Memcached. 

Properties relevant for fault propagation: 

- **Shallow but wide call chains** : the maximum service-to-service depth is 3 hops ( `frontend` _→_ `search` _→_ `profile` / `geo` / `rate` ), with high fan-out at the search service. 

14 

Table 4: Ground truth label schema. Each fault injection instance is annotated with a structured label across multiple granularity levels. Cardinalities are system-dependent; example values are drawn from TrainTicket for concreteness. 

|Field|Description|Cardinality|Example Value|
|---|---|---|---|
|`service`|Target microservice|system-dependent|`ts-order-service`|
|`pod`|Target Kubernetes Pod|system-dependent|`ts-order-service-7b8f4-xk9z2`|
|`container`|Target container within Pod|system-dependent|`ts-order-service`|
|`function`|Target function or handler (code-level faults)|system-dependent|`com.order.service.impl.create`|
|`span`|Target trace span (HTTP faults)|system-dependent|`POST /api/v1/orderservice/order`|
|`metric`|Anomalous golden signal|system-dependent|`http.server.request.duration`|



- **In-memory cache layer** : Memcached sits between every read-heavy service and its MongoDB backing store; cache faults degrade many downstream services in parallel. 

- **Terse error surface** : Go services return gRPC status codes directly rather than wrapping errors in stack traces, so log signals are sparser and trace-side evidence carries a comparatively larger share of the verification load. 

### **B.5 Propagation Channels and Telemetry Modalities** 

The dependency graph _G_ supports two propagation channels that the verification pipeline must distinguish. _Horizontal propagation_ follows RPC call chains: a slow `Order` service causes its upstream callers to time out, producing cascading latency spikes along the call graph. _Vertical propagation_ crosses abstraction layers: CPU throttling on a Kubernetes node degrades all co-located services simultaneously, even those with no mutual RPC dependency. A single injection can trigger both channels, creating multi-hop paths that mix horizontal and vertical edges. 

These channels leave distinct signatures in the three telemetry modalities, which Phase 2 verification (Section 2.3) exploits. _Traces_ record per-request call trees with span-level latencies and status codes; horizontal propagation manifests as anomalous parent _→_ child span timing that reveals the cascade direction. _Metrics_ are per-service and per-host time series (CPU usage, p99 latency, error rate); vertical propagation appears as correlated anomalies among co-located services sharing a throttled resource. _Logs_ are semi-structured text events (e.g., `[ERROR] upstream timeout` ) that supply causal context absent from numerical signals alone. 

## **C Root Cause Taxonomy** 

This section formalizes the ground truth label schema and provides the complete fault type catalog. 

### **C.1 Ground Truth Schema** 

Each fault injection instance is annotated with a structured ground truth label that specifies the root cause at multiple granularity levels. Table 4 shows the schema fields; cardinalities vary by system, and TrainTicket values are shown as concrete examples. 

The multi-level annotation enables evaluation at different abstraction levels. Service-level evaluation ( _|V|_ = 44) is the most commonly reported granularity in prior work. Finer-grained levels (function, span) provide more precise localization but increase label space complexity substantially. 

### **C.2 Complete Fault Type Catalog** 

Table 5 presents the fault types implemented in our chaos engineering framework, organized by Chaos Mesh CRD category. Each fault type is classified by: 

- **Target layer** : Whether the fault targets infrastructure resources (Pod, network, CPU/memory) or application logic (HTTP endpoints, JVM methods, database queries). 

- **Applicable ground truth levels** : Which fields of the ground truth schema are relevant. Infrastructure faults are labeled at the `service` / `pod` level, while application faults include `function` or `span` annotations. 

15 

Table 5: Fault type taxonomy across 7 Chaos Mesh CRD categories. “Applicable Levels” lists the ground-truth fields relevant to each fault type. 

|Category|Fault Type|Parameters|Target Layer|Applicable Levels|Propagation Channel|
|---|---|---|---|---|---|
|PodChaos|PodKill<br>PodFailure<br>ContainerKill|Kill signal (SIGKILL)<br>Unavailability duration<br>Target container|Infrastructure<br>Infrastructure<br>Infrastructure|service, pod<br>service, pod<br>service, pod, container|Vertical<br>Vertical<br>Vertical|
|StressChaos|CPUStress<br>MemoryStress|Core count, load %<br>Memory size (MB)|Infrastructure<br>Infrastructure|service, pod<br>service, pod|Vertical<br>Vertical|
||HTTPRequestAbort<br>HTTPResponseAbort<br>HTTPRequestDelay|Abort code, target path<br>Abort code, target path<br>Delay (ms), target path|Application<br>Application<br>Application|service, span<br>service, span<br>service, span|Horizontal<br>Horizontal<br>Horizontal|
||HTTPResponseDelay|Delay (ms), target path|Application|service, span|Horizontal|
|HTTPChaos|HTTPResponseReplaceBody<br>HTTPResponsePatchBody<br>HTTPRequestReplacePath<br>HTTPRequestReplaceMethod<br>HTTPResponseReplaceCode|Body type {empty, random}<br>Patch content<br>New path<br>Method {GET, POST, ...}<br>Status code|Application<br>Application<br>Application<br>Application<br>Application|service, span<br>service, span<br>service, span<br>service, span<br>service, span|Horizontal<br>Horizontal<br>Horizontal<br>Horizontal<br>Horizontal|
|DNSChaos|DNSError<br>DNSRandom|Target hostname<br>Target hostname|Infrastructure<br>Infrastructure|service, pod<br>service, pod|Vertical<br>Vertical|
||NetworkDelay<br>NetworkLoss|Delay (ms), jitter<br>Loss rate (%)|Infrastructure<br>Infrastructure|service, pod<br>service, pod|Vertical + Horizontal<br>Vertical + Horizontal|
|NetworkChaos|NetworkDuplicate<br>NetworkCorrupt<br>NetworkBandwidth<br>NetworkPartition|Duplicate rate (%)<br>Corrupt rate (%)<br>Rate (bps)<br>Partition direction|Infrastructure<br>Infrastructure<br>Infrastructure<br>Infrastructure|service, pod<br>service, pod<br>service, pod<br>service, pod|Vertical + Horizontal<br>Vertical + Horizontal<br>Vertical + Horizontal<br>Vertical + Horizontal|
|TimeChaos|TimeSkew|Offset (ms)|Infrastructure|service, pod|Vertical|
||JVMLatency<br>JVMReturn<br>JVMException|Delay (ms), target class.method<br>Return value, type {String, Int}<br>Exception class, target method|Application<br>Application<br>Application|service, function<br>service, function<br>service, function|Horizontal<br>Horizontal<br>Horizontal|
|JVMChaos|JVMGarbageCollector<br>JVMCPUStress<br>JVMMemoryStress<br>JVMMySQLLatency<br>|—<br>CPU count<br>Type {heap, stack}, size<br>Delay (ms), target method<br>|Application<br>Application<br>Application<br>Application<br>|service, pod<br>service, pod<br>service, pod<br>service, function<br>|Vertical<br>Vertical<br>Vertical<br>Horizontal<br>|
||JVMMySQLException|Exception, target method|Application|service, function|Horizontal|



Table 6: Mapping from raw `chaos_type` (Table 5) to the observable fault-kind labels used at evaluation time. Rows listing multiple source identifiers are many-to-one collapses where the listed mechanisms produce indistinguishable telemetry signatures; the remaining rows map one-to-one. 

|Fault kind|Source`chaos_type`(s)|Primary observation channel|
|---|---|---|
|_Pod / container lifecycle_<br>`pod_failure`|`PodKill`,`ContainerKill`|trace emission gap, brief, recovers in window|
|`pod_unavailable`|`PodFailure`|trace emission gap, sustained to window end|
|_L3/L4 network (direction recorded i_|_n GT)_||
|`network_delay`|`NetworkDelay`|`container.network.*`, trace latency tail|
|`network_loss`|`NetworkLoss`|`container.network.*`, trace retry pattern|
|`network_partition`|`NetworkPartition`|`container.network.*`, timeout share approaches one|
|`network_corrupt`|`NetworkCorrupt`|`container.network.*`, TCP retransmit signal<br>|
|`network_duplicate`|`NetworkDuplicate`|`container.network.*`, duplicate-ack pattern|
|`network_bandwidth_limit`|`NetworkBandwidth`|`container.network.*`, throughput drop|
|_HTTP application layer_|||
|`http_aborted`|`HTTPRequestAbort`,`HTTPResponseAbort`|HTTP span status, request-failure rate|
|`http_slow`|`HTTPRequestDelay`,`HTTPResponseDelay`|HTTP span duration distribution|
|`http_payload_modified`|`HTTPResponseReplaceBody`,`HTTPResponsePatchBody`,`HTTPRequestReplacePath`,`HTTPRequestReplaceMethod`|response body / path / method differs from baseline|
|`http_response_status_modifi`|`ed`<br>`HTTPResponseReplaceCode`|HTTP span status-code distribution|
|_Resource exhaustion_|||
|`cpu_stress`|`CPUStress`|`container.cpu.*`saturated|
|`mem_stress`|`MemoryStress`|`container.memory.*`saturated<br>|
|`jvm_thread_cpu_stress`|`JVMCPUStress`|`jvm.cpu.*`elevated, container CPU normal|
|`jvm_heap_stress`|`JVMMemoryStress`|`jvm.memory.used`climbs to limit|
|`jvm_gc_pressure`|`JVMGarbageCollector`|`jvm.gc.duration`histogram spikes|
|_Code-level JVM_|||
|`jvm_method_exception`|`JVMException`|log exception class on a specifc method|
|`jvm_jdbc_exception`|`JVMMySQLException`|exception on a JDBC client call|
|`jvm_method_latency`|`JVMLatency`|elevated span duration on a method|
|`jvm_jdbc_latency`|`JVMMySQLLatency`|elevated span duration on a JDBC call|
|`jvm_method_mutated`|`JVMReturn`,`JVMRuntimeMutator`|method returns a value differing from baseline|
|_DNS / clock_|||
|`dns_resolution_failed`|`DNSError`,`DNSChaos`|DNS error log entries on the affected service|
|`dns_resolution_wrong`|`DNSRandom`|resolution succeeds but returns wrong target<br>|
|`clock_skew`|`TimeSkew`,`TimeChaos`|cross-service timestamp drift in correlated logs|



- **Propagation channel** : Whether the fault propagates horizontally (between logical entities via RPC) or vertically (from infrastructure to logical layers via resource contention), or both. 

### **C.3 Observable Fault-Kind Vocabulary for Evaluation** 

The chaos-mesh API names in Table 5 describe _how_ a fault is injected, not what an agent observes from telemetry; in many cases distinct injection mechanisms produce indistinguishable signatures in the parquet data (for example `HTTPRequestAbort` and `HTTPResponseAbort` both surface as request failures from the client side, and `PodKill` and `ContainerKill` both manifest as a brief gap in the affected service’s trace emission). An agent therefore cannot recover the raw chaos-mesh API name from the released telemetry alone. We define an observable fault-kind vocabulary by relabeling 

16 

each chaos mechanism according to the feature signature it produces in metrics, traces, and logs, and judge an agent correct when its predicted label matches this observable label rather than the underlying API name. Table 6 lists the mapping from raw `chaos_type` to observable label together with the primary signal carrying each label; the same projection is applied at ground-truth extraction and at agent-prediction matching so both sides of the comparison share one vocabulary. 

## **D PAVE Pipeline and Experimental Details** 

This appendix details (i) the pipeline internals compressed in Section 2 for space (Sections D.1–D.3, plus the rule set, hyperparameters, and detector thresholds in Sections D.6, D.5, D.8), and (ii) the operational and calibration details supporting reproduction (Sections D.4–D.8). 

### **D.1 Structural Causal Model** 

Fault propagation over _G_ [8] is realized at each node as 



where **S**<sup>(</sup> _P a_<sup>_<t_</sup> (<sup>)</sup> _vi_ )<sup>are the recent states of</sup><sup>_vi_’s causal parents and</sup><sup>_U_</sup> _i_<sup>(</sup><sup>_t_)</sup> is an exogenous shock. The agent’s observation **O** _obs ⊂_ **O** _true_ is a strict subset of system state (instrumentation gaps, sampling), which is the source of the information asymmetry in inequality (1). 

### **D.2 Phase 1: Discrete State Abstraction** Ψ 

We project high-dimensional raw telemetry **O**<sup>(</sup><sup>_t_)</sup> _∈_ R<sup>_d_</sup> onto a discrete state alphabet Σ via a nodetype-aware mapping Ψ( _Oi, θ_ ( _vi_ )) _→ si ∈_ Σ, where _θ_ ( _vi_ ) is the type of node _vi_ (matching the type tag _θi_ used in the Phase 1 rule transitions of Section 2.2). For _logical nodes_ (services, spans), states capture performance violations such as `HighLatency` and `HighErrorRate` ; for _infrastructure nodes_ (pods, containers, hosts), states reflect resource exhaustion such as `CPU_Throttled` and `MemoryPressure` . This abstraction filters high-frequency noise ( _Ui_ ), retaining only semantically meaningful events as inputs to the rule-filtering and DFS stages. 

### **D.3 Phase 1: Time-Expanded Heterogeneous Graph and Constrained DFS** 

To enumerate candidate paths Π _cand_ , we construct a Time-Expanded Heterogeneous Graph whose nodes are tuples ( _v, s, t_ ): a system node _v ∈V_ with state _s ∈_ Σ activated at time _t_ . Edges connect tuples whose state transitions are admitted by the propagation rule set _R_ (Section D.6) and whose times are causally ordered. A constrained Depth-First Search starting from the injection point unrolls circular dependencies (common in microservice meshes) into acyclic chains, with the configured maximum path length and per-node revisit budget (Section D.5). The resulting paths are topologically valid sequences of state transitions; statistical and temporal verification (Section 2.3) then admits or rejects them. 

### **D.4 Cluster Configuration** 

Our testbed runs on Kubernetes v1.29 with the following specifications: 

- **Cluster** : 1 control-plane node ( `master1` , 48 vCPU, 64GB RAM) and 6 worker nodes running Debian 12 with containerd 1.7.5; `worker1` – `worker3` each provide 32 vCPU and 64GB RAM, while `worker4` – `worker6` each provide 128 vCPU and 128GB RAM 

- **Systems hosted** : TrainTicket (44 Java/Spring services), OpenTelemetry Demo (15 polyglot services), and Hotel Reservation (9 Go services), each deployed in separate Kubernetes namespaces on the shared cluster 

- **Service-count convention** : Reported per-system service counts are application `Deployments` obtained via `kubectl get deploy` on the running benchmark, excluding load generators, the OpenTelemetry collector, datastores, message brokers, and the TrainTicket UI dashboard 

- **Deployment versions** : Exact system commit hashes and image tags for the three deployments are pinned in the archived manifests released with the benchmark 

17 

Table 7: Complete propagation rule set _R_ . _Src_ / _Dst_ denote source and destination entity types; _Path_ shows intermediate hops for multi-hop rules. 

|ID|Category|Src Kind : States|Path|Dst Kind : States|Mechanism|
|---|---|---|---|---|---|
|_Vertica_|_l: Container_|_→Span_||||
|C-01<br>C-02|vertical<br>vertical|container : {cpu, mem}<br>container : {restart}|pod_→_svc_→_<br>pod_→_svc_→_|span : {lat, p99, timeout, missing, err}<br>span : {missing, err, timeout}|Resource contention<br>Process termination|
|_Vertica_|_l: Pod →Sp_|_an_||||
|P-01|vertical|pod : {cpu, mem}|svc_→_|span : {lat, p99, timeout}|Resource contention|
|_First-h_|_op: Service _|_→Span_||||
|S-01|frst-hop|service : {any}|—|span : {lat, p99, timeout}|Latency inheritance|
|S-02|frst-hop|service : {err, unavail}|—|span : {err, timeout, reset, missing, log_err}|Error inheritance|
|_Horizo_|_ntal: Span →_|_Span (RPC cascade)_||||
|H-01|horizontal|span : {lat, p99}|—|span : {lat, p99, timeout}|Callee slowdown|
|H-02|horizontal|span : {err, timeout}|—|span : {err, timeout}|Error propagation|
|H-03|horizontal|span : {missing}|—|span : {err, timeout, missing}|Missing callee|
|H-04|horizontal|span : {err, missing}|healthy span_→_|span : {err, missing}|Controller bypass|
|H-05|horizontal|span : {err, timeout}|—|span : {timeout}|Retry-induced wait|
|H-06|horizontal|span : {inj_affected}|—|span : {err, lat, p99, timeout, missing}|Infra fault relay|
|H-07|horizontal|span : {healthy}|healthy span_→_|span : {err, lat, p99, missing}|JVM injection bypass|
|_Cross-c_|_hannel: Spa_|_n →Pod →Span_||||
|X-01|cross|span : {lat, p99}|svc_→_pod_→_svc_→_|<br>span : {lat, p99, timeout}|JVM stress via shared pod|



- **Traffic load** : Synthetic user sessions are generated by per-system load generators after a warmup period, with sustained request streams used to establish pre-injection baselines and expose post-injection propagation 

- **Monitoring stack** : OpenTelemetry-based collection with per-system telemetry export to standardized parquet artifacts, together with cluster-level collectors and Prometheus-based metric scraping 

- **Fault injection** : Chaos Mesh with programmatic CRD generation for application, resource, network, and pod-level interventions 

- **Stateful backends** : Across the three systems, the benchmark exercises MySQL, PostgreSQL, MongoDB, Memcached/valkey, RabbitMQ, and Kafka-backed propagation paths 

### **D.5 PAVE Hyperparameters** 

Key parameters for the PAVE annotation pipeline: 

- **State Detection Window** ∆: 3 s for span/service-level metrics; 5 s for pod, container, and machine-level metrics 

- **State Activation** : Dual detection combines fixed utilization thresholds ( _>_ 80% CPU/memory) with Z-score baseline comparison ( _Z >_ 3 _σ_ for critical anomalies), plus adaptive multiplier thresholds for latency metrics based on coefficient of variation (CV) 

- **Maximum Path Length** : 5 hops (default), with diamond-shaped revisits allowed (max 2 visits per node) 

- **Rule Confidence** : Default 0.8 per propagation rule, with per-rule overrides 

### **D.6 Propagation Rule Set** 

Table 7 lists the complete rule set _R_ used in Phase 1 (Section 2.2). Rules are constructed by enumerating all (source entity type _×_ source state _×_ edge type _×_ destination entity type) combinations in the system dependency graph, then retaining only those for which a known physical or logical mechanism exists. We group rules into four categories by injection granularity. 

**Vertical rules** (container _→_ span, pod _→_ span) encode resource contention: a throttled container or pod degrades all spans of its co-located service through the Kubernetes scheduling hierarchy (Container _⊂_ Pod _⊂_ Node). **First-hop rules** (service _→_ span) bridge the aggregation layer, since services are logical groupings without directly observable states. **Horizontal rules** (span _→_ span) capture RPC call-chain cascades, the dominant propagation channel, accounting for over 80% of observed edges. **Cross-channel rules** (span _→_ pod _→_ span) model JVM stress scenarios where resource contention on a shared pod affects sibling services. 

The rule set is intentionally over-inclusive: rules with zero empirical usage (e.g., service error _→_ span) are retained for completeness, and Phase 2’s statistical verification (Section 2.3) filters false positives. 

18 

Rules lacking any empirical support after 500+ injection experiments were removed in version 2.0 (e.g., circuit-breaker bypass, pod-level disk/network faults), as noted in the version history. 

### **D.7 Scalability and Computational Cost** 

All experiments were conducted on a virtual machine with 32 CPU cores and 64GB RAM. The path extraction process for a single fault injection scenario, covering a 15-minute telemetry window ( _∼_ 1GB of metrics and traces), completes in an average of 3.5 minutes. Computational complexity scales with the number of active anomalous entities rather than total system components, demonstrating practical scalability. 

### **D.8 Anomaly Detection Thresholds** 

The per-node anomaly screen in Phase 2 (Section 2.3) uses three detector families, each matched to the distributional characteristics of the underlying metric. 

**Z-score detector** (for approximately Gaussian metrics such as CPU and memory utilization). A metric value _x_ is flagged if its Z-score _z_ = ( _x − µbase_ ) _/_ max( _σbase, ϵ_ ) exceeds a threshold, where _µbase_ and _σbase_ are the baseline mean and standard deviation and _ϵ_ = 10<sup>_−_6</sup> prevents division by zero. We use three severity levels: _critical_ ( _z >_ 3 _._ 0), _warning_ ( _z >_ 2 _._ 0), and _moderate_ ( _z >_ 1 _._ 5). 

**Percentile detector** (for heavy-tailed metrics such as error counts). Instead of parametric assumptions, anomalies are flagged relative to empirical baseline percentiles: _critical_ if the value exceeds the baseline P99.9 or 2 _×_ P99; _warning_ if it exceeds P99 or 1 _._ 5 _×_ P99; _moderate_ if it exceeds P90 or 1 _._ 2 _×_ P99. 

**Adaptive latency detector** (for request latency, which spans orders of magnitude across services). The threshold multiplier is _τ_ = ( _τcv_ - _base_ + _τcv_ - _range ·_ (1 _− e_<sup>_−cv/α_</sup> )) _·_ ( _lref /lbase_ )<sup>_β_</sup> , where _cv_ is the baseline coefficient of variation, _lbase_ the baseline mean latency, and _lref_ a reference latency. This formulation encodes the principle that low-baseline services (e.g., 1 ms mean) tolerate large relative spikes with minimal user impact, while high-baseline services (e.g., 5 s mean) require tighter thresholds. 

**Design rationale.** All three detectors are intentionally permissive at the per-node level: they aim to avoid false negatives (missing a genuinely affected node) at the cost of admitting some false positives (flagging coincidental deviations). False positives are subsequently eliminated by the conjunctive verification criterion: a candidate path is accepted only when every node passes the anomaly screen, every edge conforms to the propagation rule set _R_ , and downstream anomalies follow upstream causes in time. This layered design decouples the sensitivity of individual detectors from the overall precision of the ground truth. 

**Why conjunction filtering is effective.** A candidate path _π_ of length _k_ is verified only if three independent conditions hold simultaneously at every hop: (i) statistical anomaly, (ii) structural rule conformance, and (iii) temporal ordering. Let _ps_ , _pr_ , and _pt_ denote the per-hop false-positive rates of each condition in isolation. Under an independence assumption, the probability that a spurious (non-causal) path of length _k_ accidentally satisfies all three conditions at every hop is bounded by: 

_P_ (false path accepted) _≤_ ( _ps · pr · pt_ )<sup>_k_</sup> (3) 

Even with individually permissive thresholds (e.g., _ps_ =0 _._ 2, _pr_ =0 _._ 3, _pt_ =0 _._ 5), the per-hop joint false-positive rate is 0 _._ 2 _×_ 0 _._ 3 _×_ 0 _._ 5 = 0 _._ 03, and for a typical path of length _k_ =3 this yields 0 _._ 03<sup>3</sup> _≈_ 2 _._ 7 _×_ 10<sup>_−_5</sup> . This exponential decay in _k_ means that longer propagation paths, which are harder to verify, are also the most resistant to spurious acceptance. The independence assumption is approximate: in practice the three conditions share some information (e.g., structural constraints partially determine temporal ordering). Nevertheless, the exponential scaling ensures robust filtering even when the conditions are moderately correlated. 

## **E Audit Protocol and Calibration** 

This appendix details the two-annotator audit conducted on a random 100-case subsample of OpenRCA 2.0 (Section 3.4) and the calibration split used by the per-node anomaly screen. Soundness of the verified causal subgraph _G_<sup>_∗_</sup> rests on the conjunctive verification design analyzed in Section D.8: 

19 

_do_ ( _vroot_ ) pins the root direction, and an admitted path must clear three independently sourced gates simultaneously. The audit reported here is the empirical complement to that design argument. 

### **E.1 Annotator Audit on a Random Subsample** 

**Goal.** Bound the reliability of _G_<sup>_∗_</sup> by measuring agreement between the verified causal subgraphs produced by PAVE and the propagation paths that domain-experienced annotators consider plausible from the same telemetry. 

**Sampling.** A simple random sample of _N_ =100 instances was drawn without replacement from the 500 evaluable instances of OpenRCA 2.0. Sampling was uniform rather than stratum-balanced, so the audit’s verdict reflects the dataset’s natural mix of (system, fault family) pairs; post-hoc, the sample covered all 3 systems and every chaos primary kind retained in the benchmark. 

**Annotators.** Two of the paper’s authors served as annotators. Both have research experience in distributed-system observability and operational fault analysis, and are familiar with the PAVE pipeline output schema. The annotators worked independently from disjoint copies of each case’s telemetry and were blind to one another’s verdicts until the adjudication step. 

**Materials per case.** For each instance, an annotator received: (i) the multimodal telemetry over both pre- and post-injection windows (distributed traces, metric series, structured logs, all in their original parquet schema); (ii) the injected-fault metadata, comprising _vroot_ , fault type, and the injection window [ _t_ 0 _, t_ 0+∆ _t_ ]; and (iii) the pipeline-produced cascade _G_<sup>_∗_</sup> rendered as a labelled directed graph over services, pods, and spans. The pipeline output was shown so the annotator could assess it directly; the underlying telemetry was provided so the assessment was grounded in the raw evidence rather than the pipeline’s own intermediate features. 

**Annotation rubric.** Each annotator recorded a single binary verdict per case: AGREE when every edge in _G_<sup>_∗_</sup> is plausibly causal given the telemetry _and_ no obvious propagation edge is missing; DISAGREE otherwise. When an annotator marked DISAGREE, they were instructed to flag the specific edge or path that was either implausible (an included edge with no telemetry support) or missing (a propagation step visible in the telemetry but absent from _G_<sup>_∗_</sup> ). 

**Verification procedure.** The binary verdict is grounded in a fixed three-stage inspection of each case, applied uniformly across the sample. The annotator first reviews the injected-fault metadata to anchor expectation: which component received the intervention _do_ ( _vroot_ ), which fault primitive was applied, and the injection window [ _t_ 0 _, t_ 0+∆ _t_ ]. The annotator then proceeds through three stages. 

_Stage 1: anomaly verification (per node)._ For each node in _G_<sup>_∗_</sup> that carries a non-healthy state annotation, the annotator opens the underlying telemetry slice for that node over the abnormal window (span series for span nodes, metric and log streams for service and pod nodes) and verifies that the annotated abnormality is visible in the raw evidence. A node whose label cannot be located in the raw signal is flagged as a detector false positive. 

_Stage 2: hop-level causality verification (per edge)._ For each edge _u → v_ in _G_<sup>_∗_</sup> , the annotator assesses three properties: (i) _temporal precedence_ , where _u_ ’s onset of abnormality precedes _v_ ’s within plausible propagation latency; (ii) _structural plausibility_ , where the architectural relationship between _u_ and _v_ (caller–callee, container-of-pod, span-within-service, or other declared edge kind) admits the proposed propagation mechanism for the injected fault primitive; and (iii) _causal versus coincidental_ , where the change in _v_ is consistent with a downstream consequence of the abnormality at _u_ (correlated latency, error-rate, or saturation pattern) rather than an unrelated fluctuation that happens to fall within the same time window. An edge that fails any of (i)–(iii) is flagged as implausible. 

_Stage 3: coverage check._ The annotator scans the telemetry for nodes that exhibit clear abnormality during the injection window but are absent from _G_<sup>_∗_</sup> . For each such omission the annotator asks whether the missing node lies on a plausible propagation hop from _vroot_ to a labelled alarm in _G_<sup>_∗_</sup> ; if it does, the missing path is flagged. 

A case receives AGREE only when stages 1–3 produce no flags; any flag triggers DISAGREE, and the flagged node, edge, or missing path is recorded for adjudication. 

**Adjudication.** After both annotators completed the sample, every case on which the two verdicts diverged was reviewed jointly. The two annotators discussed the flagged edges, returned to the underlying telemetry where needed, and reached consensus on the source of each disagreement. This 

20 

adjudication produced a per-disagreement note used in the analysis below; it did not modify the released _G_<sup>_∗_</sup> for those cases, since the audit is a measurement of the pipeline’s output, not a relabelling pass. 

**Result.** Inter-annotator agreement on the case-level verdict was 94 _/_ 100 = 94%. The six disagreements were entirely one-directional: in each case, at least one annotator considered an additional propagation path plausible that _G_<sup>_∗_</sup> did not include. No case was flagged in the opposite direction, that is, no annotator considered any edge already in _G_<sup>_∗_</sup> implausible, so within the audited sample the released cascades contain no detected false-positive edges. 

**Disagreement analysis.** Joint review attributed every under-coverage instance to the conjunctive verification design’s deliberate strictness on borderline evidence: the gates had rejected paths whose statistical-deviation, rule-conformance, or temporal-alignment signal sat near the admission threshold. The flagged paths were not spurious (annotators considered them plausible) but they were weakly supported, and in each instance the path corresponded to a service receiving low traffic during the abnormal window, where the per-node anomaly screen could not cleanly separate the propagated effect from baseline jitter. This direction of error is consistent with the protocol’s stated property: _G_<sup>_∗_</sup> is constructed as a high-precision over-approximation of the underlying causal structure, prioritizing precision (no spurious edges admitted) over recall (some weakly supported edges may be missed). For OpenRCA 2.0’s intended use as a process-level reference for evaluating LLM agents’ propagationpath reasoning, admitting a false edge into the reference would directly mis-credit or mis-penalize an agent’s diagnosis; omitting a weakly supported edge does not. The audit therefore confirms the design’s labelling discipline: in the audited sample the released cascades are sound (no implausible included edges) at the cost of conservative coverage, which we accept as the appropriate trade-off for the benchmark’s intended use. 

### **E.2 Baseline Cal-Eval Split** 

For each instance, the pre-injection baseline window _Dbase_ is split into two halves: the first calibrates per-node thresholds (Z-score parameters, percentile cutoffs, adaptive-latency multipliers; see Section D.8), the second evaluates them. Calibrating and evaluating on the same window inflates the per-node admission rate because the screen would fit the noise it then tests against; the split prevents this overfit. Default calibration set size is half the baseline window length ( _∼_ 7 _._ 5 minutes). 

## **F LLM-Based RCA Agent Details** 

This section details the evaluation framework, agent architecture, and prompt design for the LLMbased RCA agents evaluated in our benchmark. 

### **F.1 Agent Evaluation Framework** 

Each LLM agent receives a datapack containing multimodal telemetry (traces, metrics, logs in parquet format) and produces a structured CausalGraph: a directed graph with annotated root causes, affected nodes, and causal edges. Evaluation operates at two levels: outcome-level (root cause accuracy) and process-level (causal edge and node fidelity against ground truth). This dual evaluation design enables the stratified Edge F1 analysis presented in Section 3.2. 

### **F.2 Agent Architecture** 

All agents follow a tool-augmented LLM architecture adapted from the Deep Research agent [13], operating in a ReAct-style [12] investigation loop with three nodes: 

1. `llm_call` (Decision Node): The LLM analyzes the current investigation state, consisting of the incident description, prior tool observations, and its own reflections, and either issues additional tool calls or terminates the loop. 

2. `tool_node` (Execution Node): Dispatches all tool calls from the LLM response, executes them asynchronously, and returns observations as `ToolMessage` objects. Errors are caught and returned as observations (the loop does not crash on tool failures). 

3. `compress_rca_findings` (Synthesis Node): Invoked when the LLM stops issuing tool calls. A separate LLM call synthesizes all accumulated evidence into a structured CausalGraph JSON. 

21 

The control flow follows: 

tool_calls? `START` _→_ `llm_call` _−−−−−→_ `tool_node` _→_ `llm_call` _→· · · →_ `compress` _→_ `END` 

**Tool suite.** The agent has access to four tools: 

- `list_tables_in_directory` : Discovers available parquet files and their metadata (row/column counts). 

- `get_schema` : Inspects the column names, types, and row count of a parquet file before querying. 

- `query_parquet_files` : Executes SQL queries over parquet files (supports SELECT, WHERE, JOIN, aggregations). 

- `think_tool` : A reflection tool that records the agent’s internal reasoning. The prompt instructs the agent to call this tool after each query to summarize findings and plan the next investigation step. 

The prompt recommends a tool-call budget of _∼_ 50 calls per case and enforces a hard cap of 100 at the runtime layer; the LangGraph recursion limit is set well above this so the cap is the binding constraint. All models share the same tool definitions and identical API retry logic (exponential backoff with max 5 retries). 

### **F.3 Output Schemas: Ground Truth and Agent Answer** 

Evaluation uses two distinct schemas: the released ground-truth graph in each case directory, and the structured JSON the agent emits. The ground-truth schema preserves per-node states and onset timestamps for process-level metrics; the agent schema is a smaller, verifiable contract built from `(service, fault_kind)` root-cause claims, propagation edges, and SQL evidence. 

**Ground-truth representation (released artifact).** Each case directory ships a `causal_graph.json` file in the `CausalGraph` schema below. This is the per-case process-level label produced by the PAVE pipeline (Section 2). Every node carries a controlled-vocabulary state and an onset timestamp, so the process-level metrics in Section G can be computed directly from this representation. 



<!-- Start of picture text -->
SCHEMA Ground-truth CausalGraph JSON<br>{<br>"nodes": [<br>{"component": "ts-order-service",<br>"state": ["HIGH_ERROR_RATE"],<br>"timestamp": 1718234567000000000},<br>{"component": "ts-travel-service",<br>"state": ["TIMEOUT"],<br>"timestamp": 1718234569000000000},<br>{"component": "ts-station-service",<br>"state": ["UNAVAILABLE"],<br>"timestamp": 1718234565000000000}<br>],<br>"edges": [<br>{"source": "ts-station-service",<br>"target": "ts-travel-service"},<br>{"source": "ts-travel-service",<br>"target": "ts-order-service"}<br>],<br>"root_causes": [<br>{"component": "ts-station-service",<br>"state": ["UNAVAILABLE"],<br>"timestamp": 1718234565000000000}<br>],<br>"alarm_nodes": [<br>{"component": "span|loadgenerator::POST /api/order"}<br>]<br>}<br><!-- End of picture text -->

The four top-level fields are: 

22 

- `nodes` : all involved components, each tagged with abnormal state(s) and an onset timestamp. 

- `edges` : directed causal arcs; an edge ( `source` _,_ `target` ) means the failure of `source` caused the failure of `target` . 

- `root_causes` : the subset of `nodes` that initiated the cascade. 

- `alarm_nodes` : the downstream nodes observed to behave abnormally during the injection window, used as targets for path-reachability scoring. 

In the example, `ts-station-service` became `UNAVAILABLE` at _t_ 0, propagating to `ts-travel-service` ( `TIMEOUT` ) and then `ts-order-service` ( `HIGH_ERROR_RATE` ), yielding a three-hop path. 

**Agent answer schema.** The agent emits a strict-JSON `AgentRCAOutput` with two flat lists. `root_causes` contains entries of the form ( `service` , `fault_kind` , `evidence[]` ), where `fault_kind` is drawn from a controlled enum and `evidence` is non-empty. `propagation` contains directed ( `from` , `to` ) edges, each also with non-empty `evidence` . The schema is uniform across single-fault and hybrid cases; the agent fills `root_causes` with as many entries as the evidence supports. 



<!-- Start of picture text -->
SCHEMA Agent answer ( AgentRCAOutput )<br>{<br>"root_causes": [<br>{"service": "ts-station-service",<br>"fault_kind": "pod_unavailable",<br>"evidence": [<br>{"kind": "metric",<br>"sql": "SELECT time, value FROM abnormal_metrics WHERE service_name = ’<br>ts-station-service’ AND metric LIKE ’pod_phase’ ORDER BY time",<br>"claim": "ts-station-service pod is in NotReady throughout the window"}<br>]}<br>],<br>"propagation": [<br>{"from": "ts-station-service", "to": "ts-travel-service",<br>"evidence": [<br>{"kind": "trace",<br>"sql": "SELECT span_name, attr.status_code, COUNT(*) FROM<br>abnormal_traces WHERE service_name = ’ts-travel-service’ AND span_name LIKE<br>’%station%’ GROUP BY 1,2",<br>"claim": "ts-travel-service calls into ts-station-service return TIMEOUT<br>"}<br>]}<br>]<br>}<br><!-- End of picture text -->

Each `Evidence` item declares (i) its modality ( `kind` _∈_ { `metric` , `trace` , `log` }), (ii) the actual DuckDB `sql` it claims is supported by the case parquets, and (iii) a _≤_ 20-word `claim` stating what the rows demonstrate. The contract requires every `root_cause` and every `propagation` edge to carry at least one evidence item, and the SQL must be re-executable by the judge against the case directory. Service names are normalized at match time (lowercase, hyphens and underscores stripped) to absorb naming-style drift. 

Both schemas feed the evaluation pipeline: the `(service, fault_kind)` multiset and the propagation edge set are extracted from the agent answer, while their counterparts plus the alarm-node set are read off the ground-truth graph. Section G defines the per-axis comparisons. 

### **F.4 Prompt Design** 

The agent runs a two-phase prompt. The _investigation phase_ ( `RCA_ANALYSIS_SP/UP` ) lets the model freely query the case parquets via tool calls and fixes the goal and playbook without prescribing the output JSON. The _synthesis phase_ ( `COMPRESS_FINDINGS_SP/UP` ) converts the accumulated tool messages into one strict-JSON `AgentRCAOutput` (Section F.3) using a canonical contract block spliced in from the SDK at format time. 

23 

### **F.4.1 Investigation Phase** 

#### **SYSTEM: RCA_ANALYSIS_SP** 



<!-- Start of picture text -->
You are a Root Cause Analysis (RCA) expert investigating a microservices<br>incident.<br>For context, today’s date is {date}.<br>## Goal<br>Identify the root cause(s) of the SLO violation from the telemetry. There may<br>be more than one. Let the data tell you how many faults there are and where they<br>sit.<br>Your job in this phase is INVESTIGATION ONLY. A separate synthesis step will<br>turn your findings into the final structured output. Do not try to emit JSON or<br>final answers here.<br>## Available data<br>Parquets in this case directory:<br>• abnormal_metrics.parquet, abnormal_traces.parquet, abnormal_logs.parquet<br>• abnormal_metrics_histogram.parquet, abnormal_metrics_sum.parquet<br>• normal_metrics.parquet, normal_traces.parquet, normal_logs.parquet<br>Common columns:<br>• metrics: time, metric, value, service_name, attr.k8s.pod.name,<br>attr.k8s.namespace.name<br>• metrics_sum: same shape; carries jvm.cpu.*, jvm.memory.*, jvm.thread.count,<br>jvm.gc.*, container.cpu.*, container.memory.*<br>• metrics_histogram: time, metric, service_name, count, sum, min, max,<br>attr.jvm.gc.action, attr.jvm.gc.name<br>• traces: time, trace_id, span_id, parent_span_id, span_name,<br>service_name, duration, attr.status_code, attr.http.request.method,<br>attr.http.response.status_code<br>• logs: time, trace_id, span_id, level, service_name, message<br>## Tools<br>1. query_parquet_files: DuckDB SQL on parquets in this case dir.<br>2. list_tables_in_directory: list parquets.<br>3. get_schema: column types of a parquet.<br>4. think_tool: REQUIRED after each query; summarize, plan next step.<br>## Hard limits<br>• Tool-call budget: aim for ∼ 50 calls; extend if the evidence genuinely<br>warrants it. Hard cap is 100, at which point the runtime forces a stop.<br>• Spend the budget efficiently: list_tables_in_directory once, get_schema on the<br>files you actually plan to query, then spend the rest on query_parquet_files.<br>## Investigation playbook<br>1. list_tables_in_directory to confirm the parquet files.<br>2. get_schema on the relevant ones (start with abnormal_traces).<br>3. Diff abnormal vs normal: error rates, latency, status codes, log levels.<br>4. Trace the call chain (parent_span_id → span_id) to find the earliest service<br>whose own work, not its dependency’s, went wrong.<br>5. Decide every root cause and every propagation edge. More than one root<br>cause is possible; note each separately when evidence supports it.<br><!-- End of picture text -->

#### **USER: RCA_ANALYSIS_UP** 

```
{incident_description}
```

24 

### **F.4.2 Synthesis Phase** 

#### **SYSTEM: COMPRESS_FINDINGS_SP** 

```
YouareanRCAsynthesizer.Today’sdateis{date}.
Yourjob:converttheinvestigationmessagesaboveintoasingleSTRICTJSON
objectmatchingtheRCAschema.OutputJSONonly,withnomarkdown,commentary,
orprose.
```

```
{agent_contract}(splicedcanonicalblock;see“AgentContract”below.)
##Filteringinvestigationmessages
```

- `Include: query results showing anomalies, errors, or elevated latency.` 

- `Exclude: think_tool outputs (the agent’s own reasoning notes).` 

#### **USER: COMPRESS_FINDINGS_UP** 

```
##Incident
```

```
{incident_description}
```

```
SynthesizetheinvestigationmessagesaboveintoONEJSONobjectasspecified
inthesystemprompt.Noprefix,nosuffix,nomarkdownfences,noexplanation.
Beginoutputnow.
```

### **F.4.3 Agent Contract (spliced into synthesis)** 

The synthesis prompt does not hand-maintain the output schema or the fault-kind enumeration. Both are pulled at agent-startup from the SDK, so the contract version follows the SDK version automatically. The block below is the canonical text spliced in via `{agent_contract}` ; it states the JSON shape of `AgentRCAOutput` (Section F.3), enumerates the `fault_kind` vocabulary, and lists the field, SQL, and hard rules. 

#### **SPLICED: agent_contract** 

```
##Outputschema(STRICTJSON,nomarkdown/commentary)
```

```
JSONshapeofAgentRCAOutputasinSectionF.3:root_causes[]of{service,
fault_kind,evidence[]},andpropagation[]of{from,to,evidence[]},where
everyevidenceis{kind,sql,claim}.
```

```
##fault_kindenum(pickexactlyoneperroot_cause)
```

```
pod_failure,pod_unavailable,network_delay,network_loss,network_partition,
network_corrupt,network_duplicate,network_bandwidth_limit,http_aborted,
http_slow,http_payload_modified,http_response_status_modified,cpu_stress,
jvm_thread_cpu_stress,mem_stress,jvm_heap_stress,jvm_gc_pressure,
jvm_method_exception,jvm_jdbc_exception,jvm_method_latency,jvm_jdbc_latency,
jvm_method_mutated,dns_resolution_failed,dns_resolution_wrong,clock_skew
```

```
##Fieldrules
```

- `Service names must match strings present in the data; do not invent.` 

- `One entry per distinct root cause; do NOT collapse multiple distinct faults` 

- `into a single root_cause.` 

```
##SQLrules
```

- `DuckDB on this case dir’s parquets.` 

- `SELECT only; one statement per sql field. No DDL/DML/ATTACH/etc.` 

- `Reference parquets via read_parquet(’<file>.parquet’) with bare filenames, OR` 

- `directly FROM abnormal_traces (each *.parquet is mounted as a same-named view).` 

- `Each evidence.sql MUST be the actual SQL, not a description.` 

- `Each evidence.claim is the` _≤_ `20-word natural-language assertion the SQL rows` 

- `back.` 

#### `## Hard rules` 

- `EVERY root_cause carries` _≥_ `1 evidence (real runnable SQL).` 

25 

_•_ `EVERY propagation edge carries` _≥_ `1 evidence. Do not emit edges you cannot back with a concrete trace or metric query.` 

### **F.4.4 Key Design Choices** 

- **Investigation/synthesis separation.** The investigation prompt withholds the JSON schema so the model spends tokens on collecting evidence rather than packing partial answers. The synthesis prompt then receives the canonical contract block alongside the full tool history, eliminating schema drift between agent answer and judge. 

- **Controlled fault-kind vocabulary.** The `fault_kind` enum is observable-effect-based: two chaos primitives whose telemetry is indistinguishable share a kind, and two whose signals are distinguishable get separate kinds. This lets the matcher score classification ( _fault_kind_accuracy_ ) deterministically without an LLM-as-judge. 

- **Mandatory SQL evidence.** Every claim, including both root causes and propagation edges, must cite at least one DuckDB-runnable SQL. The judge re-executes each SQL on the case directory; un-runnable evidence ( _sql_executable_rate_ ) and rows that do not back the claim ( _evidence_support_rate_ , Section G) each surface as a scoreable axis. 

- **No topology leakage.** The agent is _not_ given the service dependency graph; service relations must be inferred from trace data, testing investigative ability rather than pattern matching over a known graph. 

- **Paired normal/abnormal telemetry.** Both pre- and post-injection parquets ship in the case directory, so the agent can run differential queries (error rates, latency tails, log volumes) on identical schemas. 

### **F.5 Model Configurations** 

We evaluate Claude Opus 4.7, Claude Sonnet 4.6, Gemini 3.1 Pro, MiMo 2.5 Pro, GLM 5.1, Kimi K2.6, DeepSeek V4 Pro, Qwen3.6-Max, Hy 3.0 Preview, Seed 2.0 Pro, and MiniMax M2.7 in the main results, plus GPT-5.4 and GPT-5.5 reported separately in Appendix H.3. 

All models use identical system prompts, tool definitions, and temperature (0.7) for reproducibility. GPT-5.4 and GPT-5.5 have limited benchmark coverage and are reported separately in Appendix H.3. 

## **G Evaluation Protocol and Metric Definitions** 

We organize our evaluation metrics into two layers: _outcome_ (set classification of the predicted root-cause set against ground truth) and _process_ (causal reasoning quality on the predicted graph plus evidence executability), complemented by _dataset difficulty_ signals that characterize each instance. 

**Claim-to-Metric Mapping.** Each headline claim in Section 3.2 is anchored to a specific metric defined below: 

- _Outcome scores understate the failure; the lenient process check exposes ungrounded diagnoses_ (Finding 1): measured by the share of cases satisfying AnySvc but not PR, and by the conditional rate PR _/_ AnySvc in Table 2. 

- _Edge F1 lags Node F1 universally_ (Finding 2): measured by the per-row Node F1 vs. Edge F1 columns. 

- _No single best model_ (Finding 3): measured by the distribution of per-column extrema (bolded in Table 2) across distinct models. 

- _Per-system difficulty is uneven_ (Appendix Section H.1): measured by the spread of EM and PR across the TrainTicket / OTel Demo / Hotel Reservation rows of Appendix Table 8. 

### **G.1 Outcome-Level Metrics** 

The outcome-level metrics grade only the agent’s predicted root-cause set against the ground-truth root-cause set, ignoring the predicted causal graph. Let _R_<sup>ˆ</sup> _q_ denote the set of (service, fault_kind) pairs the agent emits as root causes for case _q_ , _Rq_<sup>_∗_the corresponding ground-truth set, and</sup><sup>_Q_the set</sup> of all evaluation queries. Service names are normalized as in Section G.2 before comparison; for network-class faults, both endpoints of the netem rule are accepted because the rule is observable on either side. 

26 

### **AnySvc (any service hit, kind-agnostic).** 



AnySvc is satisfied when at least one predicted root-cause service appears in the ground truth, irrespective of the predicted fault kind. 

**Precision, Recall, F1 on (service, fault_kind) pairs.** For each case _q_ , the per-case precision and recall on the pair set are 



where intersection uses HIT-and-equivalence semantics (a predicted pair counts as matched if there is a ground-truth pair with the same normalized service and an equivalent fault_kind in the equivalence vocabulary of Section C.3). We report the mean of P _q_ , R _q_ , and F1 _q_ over _Q_ . Recall captures fractional coverage of the ground-truth pairs and is therefore a strictly finer measurement than AnySvc, which only checks whether at least one service is named. 

### **Exact Match (EM).** 



EM requires the predicted root-cause set to coincide with the ground truth as sets, penalizing both missing and spurious entries. 

### **G.2 Process-Level Metrics** 

These metrics evaluate the quality of the agent’s causal reasoning by comparing the predicted CausalGraph against the verified causal subgraph _G_<sup>_∗_</sup> . We decompose the evaluation into _primary_ metrics (service-level, deterministic matching) and _secondary_ metrics (component-level, with LLMassisted semantic matching for name normalization). 

**Loadgen filtering.** Edges incident on the synthetic load-generator endpoint are removed from both _E_<sup>ˆ</sup> _q_ and _Eq_<sup>_∗_before any graph-shape metric (Edge F1, Node F1, Path Reachability) is computed.Loadgen</sup> is an evaluation-time client and not part of the system under test, so neither admitting nor omitting loadgen-touching edges should be scored. 

### **G.2.1 Primary Metrics (Service-Level)** 

All primary metrics operate on service-level representations. Service names are normalized (lowercased, `ts-` prefix stripped, hyphens removed) before comparison. 

**Edge F1.** Let _E_<sup>ˆ</sup> and _E_<sup>_∗_</sup> be the service-level edge sets of the predicted and ground-truth causal graphs, respectively: 



Edge F1 is the harmonic mean. 

**Node F1.** Let _V_<sup>ˆ</sup> and _V_<sup>_∗_</sup> be the service-level node sets: 



Node F1 measures whether the agent correctly identified the set of affected services. 

**Boundary case.** When both the predicted and ground-truth sets are empty for a metric (e.g., both graphs have zero edges), we assign a perfect score of 1.0, since the agent correctly predicted the absence of that element. 

27 

### **G.2.2 SQL Exec** 

The agent answer schema (Section F.3) ties every claim to at least one piece of SQL evidence. Every `evidence.sql` in the agent answer is re-executed on a fresh in-memory DuckDB connection with each `*.parquet` of the case directory mounted as a same-named view. The result is one of three statuses: `OK` (executed, _≥_ 1 row), `EMPTY` (executed, 0 rows), or `SQL_ERROR` (parse or runtime failure). Per case, 



where _E_ ev _,q_ is the union of all evidence items in _q_ ’s root_causes and propagation edges. This axis is mechanical; whether the rows actually back the claim is not scored here. 

### **G.2.3 Diagnostic Reasoning Axes** 

**Path Reachability (PR).** Path reachability measures the fraction of all instances where the agent both names a correct root-cause service _and_ constructs at least one valid directed path from that service to a ground-truth alarm node in its predicted graph: 



where _Rq_<sup>_∗_and</sup><sup>_A∗_</sup> _q_<sup>are the ground-truth root cause and alarm-node sets for instance</sup><sup>_q_, and AnySvc</sup> _q_<sup>= 1</sup> when at least one of the agent’s predicted root-cause services lies in _Rq_<sup>_∗_(kind-agnostic).Anchoring</sup> on AnySvc rather than on a kind-correct hit lets PR vary independently from the fault-kind-tagged Recall: PR isolates whether the agent constructed a faithful chain, while Recall captures whether it also labelled the fault kind correctly. Cases where the agent named no correct service receive PR = 0 by definition, since no service-correct anchor exists for the path. PR is therefore strictly upper-bounded by AnySvc, and the share of AnySvc cases failing PR quantifies how often a correctly localized service lacks even a single actionable propagation path. 

**HIT-anchored variant.** For backward comparison we also report a HIT-anchored variant of PR (Appendix Table 9), which restricts the anchor to root-cause claims that match both service _and_ fault kind. The HIT-anchored variant is strictly upper-bounded by Recall and is what the SDK stores by default; the AnySvc-anchored variant in the main table is computed locally from the same trajectories. 

## **H Auxiliary Evaluation Tables** 

### **H.1 Per-system breakdown** 

Table 8 expands the pooled main-paper table (Table 2) into per-system rows for TrainTicket, OTel Demo, and Hotel Reservation. The pooled **All** row of each model matches the corresponding row in the main table. 

The per-system spread is wide enough to dominate the cross-model spread on the easier metrics. On Hotel Reservation (142 cases, 9 services, mean longest path 2.1 hops) Opus reaches 99.3% AnySvc and 54.9% EM, while on TrainTicket (320 cases, 44 services, mean longest path 3.0 hops) the same model drops to 75.3% AnySvc and 15.6% EM; OpenTelemetry Demo (38 cases, 15 services, 2.5 hops) sits between, at 81.6% AnySvc and 26.3% EM. Both service count and chain depth track the difficulty ordering in the same direction. Finding (2) in Section 3.2 suggests path depth is the load-bearing factor: Edge F1 trails Node F1 by _∼_ 19 pp pooled, and the deficit compounds along longer paths. Pooled scores across systems with disparate chain depth are therefore sensitive to system-mix manipulation; the per-system rows below are the direct read for any narrow-regime comparison. 

### **H.2 HIT-anchored Path Reachability** 

Table 9 reports PR under the stricter HIT anchor (the SDK default): the agent must match both service _and_ fault kind on the anchoring root-cause claim before the path is checked. The HIT-anchored variant is what the per-case `result.json` stores; the main-table PR (Table 2) relaxes the anchor to AnySvc so PR varies independently from fault-kind labelling. 

28 

Table 8: Per-system breakdown of Table 2 (TrainTicket, OTel Demo, Hotel Reservation; pooled aggregate in the **All** row; percentages). 

|||||_Outcom_|_e_||||_Process_||
|---|---|---|---|---|---|---|---|---|---|---|
|Model|System|EM_↑_|F1_↑_|Precision_↑_|Recall_↑_|AnySvc_↑_|PR_↑_|Node F1_↑_|Edge F1_↑_|SQL Exec_↑_|
||TrainTicket|15.6|22.3|23.4|22.7|75.3|55.9|58.9|36.3|98.7|
|Cld O 47|OTel Demo|26.3|50.5|51.8|52.6|81.6|81.6|77.4|66.5|98.7|
|aue pus .|Hotel Res.|54.9|81.9|94.4|76.1|99.3|98.6|84.2|74.7|94.4|
||**All**|**27.6**|**41.4**|**45.7**|**40.1**|**82.6**|**70.0**|**67.5**|**49.5**|**97.5**|
||TrainTicket|18.1|25.2|28.0|24.1|75.0|57.8|59.8|27.1|98.7|
|Gii 31 P|OTel Demo|36.8|57.5|67.1|52.6|81.6|76.3|77.3|31.9|99.0|
|emn . ro|Hotel Res.|52.8|82.2|96.5|75.0|97.9|97.2|83.8|60.0|98.9|
||**All**|**29.4**|**43.8**|**50.4**|**40.7**|**82.0**|**70.4**|**67.9**|**36.8**|**98.8**|
||TrainTicket|15.0|20.8|21.9|20.9|70.3|30.0|55.1|34.1|96.8|
|Cld St 46|OTel Demo|34.2|57.6|61.4|57.9|89.5|81.6|72.5|62.1|96.6|
|aue onne .|Hotel Res.|49.3|80.2|95.1|72.9|97.2|95.8|83.7|75.4|92.8|
||**All**|**26.2**|**40.5**|**45.7**|**38.5**|**79.4**|**52.6**|**64.5**|**48.0**|**95.6**|
||TrainTicket|11.2|16.8|17.0|18.0|68.8|42.2|56.0|32.1|93.5|
|MiM 25 P|OTel Demo|31.6|47.5|50.0|47.4|86.8|76.3|71.7|56.0|94.4|
|o . ro|Hotel Res.|46.5|75.8|89.4|69.4|95.8|94.4|81.0|70.5|88.1|
||**All**|**22.8**|**35.9**|**40.1**|**34.8**|**77.8**|**59.6**|**64.3**|**44.9**|**92.0**|
||TrainTicket|9.4|14.7|15.5|15.0|70.9|56.9|59.8|38.6|93.9|
|GLM 51|OTel Demo|21.1|39.6|42.1|39.5|84.2|78.9|77.1|68.7|94.3|
|.|Hotel Res.|49.3|75.9|88.7|69.7|95.8|95.8|80.3|71.9|92.2|
||**All**|**21.6**|**34.0**|**38.3**|**32.4**|**79.0**|**69.6**|**66.9**|**50.4**|**93.4**|
||TrainTicket|10.6|15.3|15.7|15.9|61.6|50.0|49.3|30.8|78.8|
||OTel Demo|18.4|41.9|43.9|44.7|68.4|65.8|61.0|51.5|72.9|
|Kimi K2.6|Hotel Res.|45.1|73.9|88.0|66.9|92.3|92.3|79.6|72.1|93.0|
||**All**|**21.0**|**34.0**|**38.4**|**32.6**|**70.8**|**63.2**|**58.8**|**44.1**|**82.4**|
||TrainTicket|10.9|14.1|15.0|13.9|54.1|35.6|42.1|25.8|70.1|
|DSk V4 P|OTel Demo|23.7|39.4|42.5|38.2|65.8|57.9|58.0|46.5|68.7|
|eepee  ro|Hotel Res.|40.8|70.3|84.9|63.0|91.5|90.8|78.1|70.5|87.4|
||**All**|**20.4**|**32.0**|**36.9**|**29.7**|**65.6**|**53.0**|**53.5**|**40.1**|**74.9**|
||TrainTicket|9.4|17.2|17.3|19.1|70.6|60.3|56.1|36.7|93.8|
|Qwen36-Max|OTel Demo|21.1|47.4|55.3|44.7|86.8|76.3|77.1|67.5|89.4|
|.|Hotel Res.|40.8|74.4|88.8|68.0|96.5|96.5|82.0|69.8|92.0|
||**All**|**19.2**|**35.7**|**40.5**|**34.9**|**79.2**|**71.8**|**65.1**|**48.5**|**92.9**|
||TrainTicket|6.2|11.7|11.0|14.4|60.6|34.7|43.2|22.9|89.5|
||OTel Demo|21.1|37.7|42.1|36.8|63.2|57.9|69.9|50.3|98.0|
|Hy 3.0 Preview|||||||||||
||Hotel Res.|41.5|69.4|81.5|64.1|96.5|94.4|80.6|69.8|96.6|
||**All**|**17.4**|**30.1**|**33.4**|**30.2**|**71.0**|**53.4**|**55.9**|**38.3**|**92.1**|
||TrainTicket|8.8|14.3|14.1|16.1|72.5|53.8|57.3|35.7|89.8|
|Sd 20 P|OTel Demo|10.5|24.2|26.6|25.0|73.7|71.1|72.9|63.3|87.2|
|ee . ro|Hotel Res.|29.6|55.9|67.1|50.7|93.7|93.7|78.7|70.5|93.3|
||**All**|**14.8**|**26.8**|**30.1**|**26.6**|**78.6**|**66.4**|**64.5**|**47.7**|**90.6**|
||TrainTicket|1.9|8.3|7.1|11.4|64.7|33.1|46.9|21.2|86.6|
|MiniMax M27|OTel Demo<br>|2.6<br>|15.4<br>|14.5<br>|18.4<br>|52.6<br>|39.5<br>|62.2<br>|43.6<br>|88.3<br>|
|.|Hotel Res.|19.0|49.7|49.5|54.6|85.9|78.2|72.5|43.4|87.3|
||<br>**All**|**6.8**|**20.6**|**19.7**|**24.2**|**69.8**|**46.4**|**55.3**|**29.2**|**86.9**|



### **H.3 Limited-coverage models** 

GPT-5.4 and GPT-5.5 hit API budget limits before completing the full benchmark, so their sample sizes are smaller than the main-table models. We include their partial results below for reference only; they should not be compared directly to Table 2. 

29 

Table 9: HIT-anchored Path Reachability (PR<sup>HIT</sup> ) per (model, system). Strictly upper-bounded by Recall. Cf. Table 2 for the AnySvc-anchored PR used in the main table. 

|Model|TrainTicket|OTel Demo|Hotel Res.|**All**|
|---|---|---|---|---|
|Claude Opus 4.7|22.2|60.5|94.4|**45.6**|
|Gemini 3.1 Pro|24.4|60.5|97.2|**47.8**|
|Claude Sonnet 4.6|16.9|57.9|94.4|**42.0**|
|MiMo 2.5 Pro|16.6|44.7|90.8|**39.8**|
|GLM 5.1|16.2|44.7|89.4|**39.2**|
|Kimi K2.6|15.3|39.5|88.7|**38.0**|
|DeepSeek V4 Pro|13.4|39.5|85.2|**35.8**|
|Qwen3.6-Max|20.6|60.5|91.5|**43.8**|
|Hy 3.0 Preview|12.2|39.5|83.8|**34.6**|
|Seed 2.0 Pro|16.2|34.2|70.4|**33.0**|
|MiniMax M2.7|7.8|15.8|70.4|**26.2**|



Table 10: GPT models with partial coverage due to budget limits (pooled across systems; for reference only). 

|Model|n|EM_↑_|F1_↑_|AnySvc_↑_|PR_↑_|Node F1_↑_|Edge F1_↑_|
|---|---|---|---|---|---|---|---|
|GPT-5.4|114|18.4|22.5|85.1|58.8|68.1|45.8|
|GPT-5.5|32|15.6|19.8|90.6|87.5|70.9|53.3|



30 

