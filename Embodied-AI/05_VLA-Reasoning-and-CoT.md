---
title: "VLA Reasoning & Chain-of-Thought — Deep Dive"
tags:
  - VLA
  - reasoning
  - chain-of-thought
  - planning
  - robotics
  - manipulation
aliases:
  - "VLA Reasoning"
  - "VLA CoT"
  - "Reasoning-Augmented VLA"
---

# VLA Reasoning & Chain-of-Thought — Deep Dive

> [!abstract] Overview
> Pure imitation collapses on long-horizon, novel, or counterfactual tasks. Reasoning-augmented VLAs add explicit deliberation — visual chain-of-thought, latent reasoning, test-time search, or reasoning-traced training — to recover robustness. The design question is not *whether* to reason, but *where in the pipeline* to insert reasoning: at input prompting, in latent space, at the output head, or via external search. This note maps the four architectural slots, the trade-offs (latency vs accuracy vs interpretability), and the 2026 frontier where latent reasoning matches explicit CoT at answer-only latency.

## Evolution Graph

```text
1. LLM Planning   (language as the planner)
· grounded planning
╔═══════════════╗
║ SayCan (2022) ║─┐
╚═══════════════╝ │
                  │    +closed-loop feedback
                  │    ╔════════════════════════╗
                  ├───►║ Inner-Monologue (2022) ║──┐
                  │    ╚════════════════════════╝  │
                  │    +executable code            │
                  │    ╔═════════════════════════╗ │
                  └───►║ Code-as-Policies (2022) ║─┤
                       ╚═════════════════════════╝ │
                                         +constraint recovery
                                         ┌─────────▼────────┐
                                         │ DoReMi (2023)    │
                                         └──────────────────┘

2. Action Hierarchies   (language between plan and motor)
· intermediate action language
╔═════════════╗
║ RT-H (2024) ║─┐
╚═════════════╝ │
                │    +dexterous stages
                │    ┌───────────────┐
                ├───►│ DexVLA (2025) │
                │    └───────────────┘
                │    +visual subgoals      +action reasoning      +affordance chain
                │    ╔════════════════╗    ┌─────────────────┐    ┌───────────────────┐
                └───►║ CoT-VLA (2025) ║───►│ MolmoAct (2025) │───►│ Afford-VLA (2026) │
                     ╚════════════════╝    └─────────────────┘    └───────────────────┘

3. Visual Chain-of-Thought   (reason in pixels, not tokens)
· visual reasoning traces
                          +latent plan           +diffusion reasoning    +test-time thinking
┌────────────────────┐    ╔═════════════════╗    ┌──────────────────┐    ┌────────────────────┐
│ EmbodiedVSR (2025) │───►║ ThinkAct (2025) ║───►│ dVLA (2025)      │───►│ ThinkingVLA (2026) │
└────────────────────┘    ╚═════════════════╝    └──────────────────┘    └────────────────────┘

4. Latent Reasoning   (drop the token bottleneck)
· implicit reasoning
┌───────────────┐
│ OccVLA (2025) │─┐
└───────────────┘ │
                  │    +latent tokens     +collaborative
                  │    ┌─────────────┐    ┌────────────────┐
                  ├───►│ VITA (2025) │───►│ ColaVLA (2025) │
                  │    └─────────────┘    └────────────────┘
                  │    +latent space       +unified
                  │    ┌──────────────┐    ┌──────────────┐
                  └───►│ LaST0 (2026) │───►│ OneVL (2026) │
                       └──────────────┘    └──────────────┘

5. Grasp Reasoning   (chain-of-thought at contact)
· reasoned grasping
                   +cluttered scenes        +affordance               +explicit CoT
╔═════════════╗    ┌───────────────────┐    ┌────────────────────┐    ┌─────────────────┐
║ CoPa (2024) ║───►│ ThinkGrasp (2024) │───►│ AffordGrasp (2025) │───►│ GraspCoT (2025) │
╚═════════════╝    └───────────────────┘    └────────────────────┘    └─────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

Five lanes, distinguished by where the reasoning lives. LLM planning is the one converging thread: [[2204.01691|SayCan]] forked into closed-loop feedback ([[2207.05608|Inner-Monologue]]) and executable code ([[2209.07753|Code-as-Policies]]), and [[2307.00329|DoReMi]] merged both back. The rest move reasoning progressively out of language — into intermediate action tokens ([[2403.01823|RT-H]]), into pixels ([[2503.11089|EmbodiedVSR]], [[2507.16815|ThinkAct]]), and finally into latent space where it costs no tokens at all ([[2509.05578|OccVLA]], [[2604.18486|OneVL]]). Grasp reasoning is the one lane that applies chain-of-thought at the point of contact.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2022 | [[2204.01691\|SayCan]] | LLM Planning | An LLM scores candidate skills' semantic relevance while a learned affordance function scores physical feasibility |
| 2022 | [[2207.05608\|Inner-Monologue]] | LLM Planning | The foundational closed-loop embodied-reasoning method feeding textual environment feedback |
| 2022 | [[2209.07753\|Code-as-Policies]] | LLM Planning | A method where code-writing LLMs synthesize executable Python programs as robot policies |
| 2023 | [[2307.00329\|DoReMi]] | LLM Planning | An LLM plans the next skill *and* generates explicit constraints |
| 2024 | [[2403.01823\|RT-H]] | Action Hierarchy | An action-hierarchy VLA (PaLI-X 55B) using a two-phase query to first predict a language motion ("move arm left") |
| 2024 | [[2403.08248\|CoPa]] | Grasp Reasoning | A VLM manipulation framework decomposing 6-DoF control into Task-Oriented Grasping and Task-Aware Motion Planning |
| 2024 | [[2407.11298\|ThinkGrasp]] | Grasp Reasoning | An iterative closed-loop system using GPT-4o strategic reasoning to pick target or obstructing objects in heavy clutter |
| 2025 | [[2502.05855\|DexVLA]] | Action Hierarchy | A VLA pairing a 2B VLM with a billion-parameter diffusion action expert under three-stage embodied curriculum learning |
| 2025 | [[2503.00778\|AffordGrasp]] | Grasp Reasoning | A training-free framework doing in-context affordance reasoning with a VLM |
| 2025 | [[2503.11089\|EmbodiedVSR]] | Visual CoT | A framework feeding dynamically-updated scene graphs into a physics-constrained chain-of-thought for per-step geometric |
| 2025 | [[2503.16013\|GraspCoT]] | Grasp Reasoning | A 6-DoF grasping multimodal LLM running a hierarchical Chain-of-Thought |
| 2025 | [[2503.22020\|CoT-VLA]] | Action Hierarchy | A **7B** VILA-U unified multimodal VLA that predicts a future-frame token as a visual subgoal *first* |
| 2025 | [[2507.16815\|ThinkAct]] | Visual CoT | A dual-system framework for reinforced visual latent planning where a slow-thinking MLLM |
| 2025 | [[2508.07917\|MolmoAct]] | Action Hierarchy | An Action Reasoning Model whose three-stage autoregressive pipeline emits depth-aware perception tokens |
| 2025 | [[2509.05578\|OccVLA]] | Latent Reasoning | A driving VLA whose Vision-Language-Occupancy backbone treats dense 3D occupancy prediction as an *implicit* reasoning step |
| 2025 | [[2509.25681\|dVLA]] | Visual CoT | A unified discrete diffusion VLA converting vision/language/actions to discrete tokens under one objective |
| 2025 | [[2511.19859\|VITA]] | Latent Reasoning | An implicit visual CoT model: future-frame prediction is internalized as an *inductive bias* over a shared discrete latent |
| 2025 | [[2512.22939\|ColaVLA]] | Latent Reasoning | A driving VLA whose Cognitive Latent Reasoner relocates VLM CoT from text into decision-oriented meta-action embeddings |
| 2026 | [[2601.05248\|LaST0]] | Latent Reasoning | A dual-system Mixture-of-Transformers VLA whose Latent Spatio-Temporal CoT compresses 2D-visual / 3D-geometric / |
| 2026 | [[2604.18486\|OneVL]] | Latent Reasoning | A VLM with language + visual latent tokens supervised by dual auxiliary decoders (training-time only) |
| 2026 | [[2605.24203\|Afford-VLA]] | Action Hierarchy | A VLA internalizing task-conditioned affordance as an action-aligned planning interface: learnable query tokens |
| 2026 | [[2606.17937\|ThinkingVLA]] | Visual CoT | A unified-autoregressive VLA that interleaves forward textual CoT, predicted future images |

---

## Part A — Framework

*The four reasoning insertion slots — the taxonomy that organizes everything below.*

### 1. The Four Reasoning Insertion Slots

Every VLA pipeline has four candidate slots where reasoning can be inserted, and the slot choice — not the reasoning content — determines whether reasoning becomes a latency burden or a free accuracy win. The four slots sit on orthogonal axes: ==input prompting== reasons *before* the model runs, ==latent reasoning== reasons *inside* the model's hidden state, ==output head== reasoning emits reasoning *alongside* actions, and ==external search== reasons *around* the policy via test-time rollouts. Each absorbs a different cost — inference latency, opacity, generation expense, or search overhead — so the design question is which constraint binds your deployment.

#### 1.1 Input Prompting

The cheapest slot: ask the VLM to reason about the task in natural language *before* generating actions. The reasoning is generated by the same backbone that produces the actions, in the same forward pass.

- **[[2607.06990|Closed-Loop Multi-Robot Manipulation Framework]]** — A hierarchical multi-agent system pairing a ==Planning Agent== (dependency-aware decomposition) with per-robot ==Manipulation== and ==Verification Agents== (VLM-grounded primitives, hierarchical error recovery); **85%** Block-Stacking completion (baselines 35-75%), **63%** avg SR under disturbances (7-20%).
- **[[2607.06724|EvoPlan]]** — A neuro-symbolic framework mining a global ==Signal Temporal Logic== safety constraint from one-class demos via counterfactual negatives, then an ==LLM-driven evolutionary PDDL planner== repairs plans with runtime STL monitoring; **98.5%** SR on ALFWorld Text, **77%** fewer red-light infractions.
- **[[2607.06501|HUME]]** — A neuro-symbolic planner treating missing world knowledge as ==object-centric hypotheses==, adding explicit ==verification actions== so a classical planner + LLM/VLM actively validate assumptions; **0.93** SR / **0.86** SPL real-world mobile manipulation, beating LLM-only planners.
- **[[2607.04162|ACE]]** — A zero-shot ==closed-loop workflow reasoning== agent decoupling task decomposition from a ==mask-mediated vision-action interface== driving a task-agnostic ==Diffusion Policy==; **50-70%** SR on logically complex tasks (baselines **0%**), **90%** grasp SR from mask-only input.
- **[[2606.30613|SPARK (Anchored Robotic Keypoints)]]** — A training-free ==neurosymbolic== manipulator pairing multi-camera ==SAM3== perception with Gemini ==Behavior Tree== planning and ==Adaptive Perception Self-Consistency==, using tiered recovery instead of LLM re-planning; **43.7%** avg SR on LIBERO-PRO (2x CAP-AGENT0), **68%** cross-embodiment SR across 3 real robot families.
- **[[2606.27251|OmniAct]]** — A hierarchical asynchronous omnimodal agent separating ==planning==, state tracking, and physical verification, with a ==Multimodal Semantic Planner== unifying cyber tools + physical control in one skill-routing space and a ==Closed-Loop Execution Engine== using visual preemption for anomaly-triggered replanning; **50.0%** L3 manipulation, **54.2%** navigation E2E.
- **[[2606.25404|HEART]]** — A ==token-aware multi-LLM== task-planner coordinating five role-specialized expert reasoners (Capability, Environment, Path, Feasibility, Constraint) via a central allocator across Decompose→Allocate→Reason→Synthesize, with semantic scoring + failure penalties; **72-76%** Plan SR, **~99%** Subtask SR at ~**30%** fewer tokens, lifting LLM-CoT/DELTA planners.
- **[[2606.13049|Y-BotFrame]]** — A hierarchical modular framework decoupling an ==LLM cognitive planner== from execution, translating instructions into action sequences by invoking modules from a =='Tool Factory'== (speech, autonomous navigation with online mapping, embodied QA) with contextual consistency over history; integrates speech + RGB + LiDAR perception on a quadruped assistant.
- **[[2604.10929|Ro-SLM]]** — An onboard ==small-language-model== task-planner trained via LLM-synthesized instruction/code data then ==SFT (LoRA) + GRPO== with an LLM binary code-correctness reward, transferring LLM planning to a deployable SLM; lifts Llama-3.1-8B to **97.7%** basic / **70.0%** advanced UAV SR (untuned ~5-10%), **75%** zero-shot on an unseen ground vehicle.
- **[[2507.16713|Pragmatist-Robot-Plan-Tasks]]** — A closed-loop VLM task-planner (PRAGMABOT) learning from real-world interaction via ==short-term memory== self-reflection on within-episode failures and ==long-term memory== of summarized successes retrieved by ==RAG==; **84%** avg SR (vs 35% without STM), **79.5%** single-trial via LTM, with emergent tool use and obstruction handling.
- **[[2504.12755|Trajectory-Adaptation-Large-Language]]** — A training-free framework using ==pretrained LLMs== to adapt robot trajectories from language, generating a human-readable High-Level Plan + executable ==Python code== for waypoint/velocity edits via an iterative user-feedback loop; handles compound/numerical commands across manipulator/aerial/ground robots from 1–2 examples.
- **[[2503.06866|Graphormer-Guided]]** — A safety-aware LLM planner building a ==spatio-semantic safety graph== (LLM-annotated interactions + spatial proximity) that a pretrained ==Graphormer== screens for high-risk edges, triggering LLM re-planning on detected hazards; **91.39%** hazard-detection recall filtering ~70% false positives, **100%** safety-notice rate across AI2-THOR household tasks.
- **[[2503.15707|Safety-Aware-Task-Planning]]** — A multi-LLM robotic task-planner (SAFER) decoupling a ==Task Planning LLM== from a ==Safety Planning LLM== auditing plans against 15 risk criteria via ==LLM-as-a-Judge==, with ==Control Barrier Functions== for real-time safety; **−77.5%** Average Safety Violations (DeepSeek-r1) on COHERENT at minimal latency, deployed on real multi-robot hardware.
- **[[2503.10480|World-Modeling-Makes-Better]]** — An embodied task-planner (OpenMOSS) giving a **7B** LVLM world-modeling via ==Dual Preference Optimization (D²PO)== jointly optimizing ==state prediction== + ==action selection==, with ==tree search== auto-collecting preference pairs (no human annotation); beats **GPT-4o** SR on the new VoTa-Bench with more path-efficient actions.
- **[[2503.00729|CLEA]]** — A closed-loop embodied agent decoupling LLM-based task planning into ==four specialized LLMs== with distinct roles, adding real-time execution criticism + an environmental memory for long-horizon contextual awareness in dynamic environments; **+67.3%** SR and **+52.8%** task-completion over baselines, validated on multiple real robots in a kitchen.
- **[[2405.14314|Efficient-LLM-Grounding-Embodied]]** — A closed-loop LLM-grounding framework (ReAd) replacing heuristic feedback with learned ==multi-agent advantage functions== (joint + local) that filter negative-advantage actions, extending advantage-weighted regression to LLM planning; beats baselines on DV-RoCoBench / Overcooked at fewer env steps + queries, **100%** under resets.
- **[[2212.04088|LLM-Planner]]** — A few-shot grounded LLM planner using ==GPT-3 in-context planning== with a ==kNN example retriever== + logit biases over visible objects, plus ==dynamic grounded re-planning== that updates subgoals mid-execution from observations; competitive ALFRED SR using **<0.5%** of training data, **+1.83%** unseen SR from re-planning, **7** vs 22 LLM calls/task.
- **[[2504.00775|Visual-Environment-Interactive-Planning-Embodied]]** — A sequential ==Observation-Planning-Action== framework threading hierarchical scene graphs + parsed-question semantics through multi-turn visual feedback for embodied complex-QA; **65.4%** LLM-Match (ReAct **61.8%**), **+9.4pp** multi-step on the new ECQA — closed-loop replanning beats one-shot LLM plans.
- **[[2503.21564|Cooking-Task-Planning-LLM]]** — A hybrid planner where a multimodal LLM uses ==Chain-of-Thought== + few-shot to infer object states/actions from cooking videos, validated by a ==Functional Object-Oriented Network (FOON)== driving iterative re-planning; full task graphs for **4/5** recipes (LLM-only **1/5**), inferring an omitted Cut for execution — CoT verified by a graph.
- **[[2503.06892|SafePlan]]** — A safety-layered planner pairing ==formal logic with CoT==: a ==Prompt Sanity-Check CoT Reasoner== (Societal/Organizational/Individual layers) filters unsafe commands and an ==Invariant CoT Reasoner== verifies pre/post-conditions before execution; **88.4%** prompt-safety accuracy, **0%** AI2-THOR crash rate (baselines up to **100%**) — CoT verified by formal logic.
- **[[2503.02698|FlowPlan]]** — A zero-shot ==multi-stage LLM workflow== (Task-Info Retrieval → Language-Level Reasoning → Symbolic Planning → ==Logical Evaluation==) with context-aligned target localization for instruction following; ~**2×** ALFRED TSR/GC over prior zero-shot, **100%** real-world planning precision over 50 trials — flow-engineered self-correcting planner.
- **[[2503.01378|CognitiveDrone]]** — A UAV ==VLA (OpenVLA-adapted)== whose CognitiveDrone-R1 variant adds a ==Qwen2.5-VL reasoning module== decomposing complex instructions before flight, plus the CognitiveDroneBench suite; **77.2%** avg SR (vs **59.6%** no-reasoning, **31.3%** RaceVLA), **+31%** Human-Recognition / **+21%** Symbol-Understanding — reasoning module lifts a VLA.
- **[[2502.21257|RoboBrain]]** — A unified ==MLLM (LLaVA + Qwen2.5-7B)== that reasons from abstract instruction to concrete control via ==A-LoRA / T-LoRA== heads for planning, affordance, and trajectory, trained on the new ==ShareRobot== dataset; **55.05** BLEU-4 RoboVQA planning (**+18.75** over 2nd), **27.1%** AGD20K affordance AP — high-level planning brain.
- **[[2311.17842|VILA]]** — A robotic planning framework using ==GPT-4V as a unified VLM== to reason over visual observations *before* acting in a ==closed-loop== prompt-execute cycle, grounding commonsense and multimodal goals without external affordance models; **80%** real-world commonsense tasks (vs SayCan **13%**), **90%** Stack-Blocks under noise — the canonical input-prompting slot.
- **[[2307.02485|Building-Cooperative-Embodied-Agents]]** — ==CoELA==, a cognitive-inspired modular ==LLM agent== (Perception / Memory / Communication / Planning / Execution) for decentralized multi-agent cooperation under costly NL messaging; up to **+39%** efficiency on TDW-MAT, emergent selective communication, human-trust **6.3 vs 4.7** — LLM reasoning for embodied teams.
- **[[2307.00329|DoReMi]]** — An ==LLM== plans the next skill *and* generates explicit ==constraints==, continuously checked by a ==VLM== as binary Yes/No queries every **0.2s** to trigger immediate abort-and-replan on violation, unlike SayCan/Inner-Monologue's delayed step-completion feedback; **90%**/**80%** real-world SR on perturbed 'Prepare-food'/'Stack' tasks.
- **[[2504.20459|SAS-Prompt]]** — An LLM-as-numerical-optimizer using a ==Summarize-Analyze-Synthesize== prompt loop that reads robot execution traces in natural language to synthesize improved control parameters, treating textual parameter-outcome analysis as an interpretable gradient; **39.4%** top-1 / **83.7%** top-10 retrieval, transfers left→right table-tennis hits — reasoning-as-optimizer.
- **[[2501.02486|LLMPC]]** — A framework casting ==LLMs as approximate optimizers== inside ==Model Predictive Control==: prompt the LLM to sample K plans, simulate each via a state-transition model, score against an explicit objective, execute the best, then replan; trip-planning SR **14.5% → 44.6%**, meeting-planning **67%** — multi-plan sampling closes the LLM-vs-exact-optimization gap.
- **[[2410.02742|GLIMO]]** — A framework grounding LLM planners by fine-tuning on embodied experiences from ==imperfect world models==, with an ==automated LLM agent data generator== and ==two-stage LoRA== tuning against forgetting; **2.04×** Agent World task completion, beating GPT-4 by **51.7%** — imperfect simulators suffice to ground embodied reasoning.
- **[[2409.10106|Industry 6.0]]** — A fully-autonomous production pipeline where a ==generative-AI orchestrator== (LangChain) reasons from natural language to ==SDF mechanism code==, then an ==LLM-based supervisor== assigns subtasks to a heterogeneous robot + drone swarm via predefined APIs; **4.44×** faster than human experts end-to-end, **47×** speedup in blueprinting alone.
- **[[2303.11381|MM-REACT]]** — A foundational multimodal reasoning-and-action framework prompting ChatGPT in a ==thought-action-observation loop== that picks which vision expert to call, textualizes its output, and refines iteratively for multi-hop / spatial / video reasoning; **comparable to PaLM-E** with no joint training — the ReAct-style expert-orchestration ancestor of embodied LLM planners.
- **[[2209.07753|Code-as-Policies]]** — A method where code-writing LLMs synthesize executable ==Python programs== as robot policies, parameterizing low-level APIs with few-shot prompts and ==hierarchical code generation== for spatial-geometric reasoning; **96%** object / **100%** position selection (CoT **68%/48%**) — code-as-policy beats NL CoT for embodied control.
- **[[2207.05608|Inner-Monologue]]** — The foundational closed-loop embodied-reasoning method feeding ==textual environment feedback== (success/failure, object recognition, task progress) into an LLM planner's prompt for real-time re-planning, no fine-tuning; 3-block stacking **20% → 100%** with success feedback, **75%** under adversarial disturbance (SayCan **0%**).
- **[[2204.01691|SayCan]]** — An ==LLM== scores candidate skills' semantic relevance while a learned ==affordance function== scores physical feasibility, multiplying the two to pick the next step; **84%** planning / **74%** execution SR across **101** real kitchen tasks, scaling with LLM size (**PaLM 540B** > FLAN) — the foundational "Say×Can" split.
- **Architecture** — Zero new parameters; works with any pretrained VLM as a drop-in prompting strategy.
- **Cost trade-off** — Reasoning is a token-level afterthought; no guarantee it grounds the action distribution. Adds the full reasoning length to inference latency.
- **Canonical example** — RT-2-style "let me think step by step" prompting before action generation.

#### 1.2 Latent Reasoning

Reason inside the model's hidden state without emitting text. Either pre-allocate latent tokens for reasoning ([[2604.22709|Abstract-CoT]]) or supervise the latent space with auxiliary decoders ([[2604.18486|OneVL]]).

- **[[2604.18486|OneVL]]** — A VLM with language + visual latent tokens supervised by ==dual auxiliary decoders== (training-time only), processed in one ==prefill== pass; fast (no extra autoregressive steps), preserves ==answer-only latency==, yet *outperforms* explicit CoT — **88.84 PDM-score** on NAVSIM (**+2.64 pts** over 8B baselines). The 2026 frontier result.
- **[[2604.22709|Abstract-CoT]]** — A method replacing verbal CoT with ==discrete abstract tokens== from a ==reserved vocabulary== under two-stage post-training (==policy-iteration warm-up + warm-started GRPO==) and an ==attention-mask information bottleneck==; up to **12×** fewer reasoning tokens at comparable/superior MATH/AlpacaEval/HotpotQA across Qwen3 and Granite.
- **Cost trade-off** — Opaque — debugging requires auxiliary decoders or probing.

#### 1.3 Output Head Reasoning

Generate reasoning *as part of the output* alongside actions: visual subgoal frames ([[2503.22020|CoT-VLA]]), reasoning traces ([[2508.07917|MolmoAct]]), multimodal CoT tokens ([[2509.25681|dVLA]]).

- **[[2605.24203|Afford-VLA]]** — A VLA internalizing task-conditioned ==affordance== as an action-aligned planning interface: ==learnable query tokens== + a ==query-patch grounding decoder== produce affordance masks conditioning the action head via ==straight-through gradient== pooling; **97.4%** avg LIBERO SR, **78.1%** zero-shot LIBERO-Plus, **80%**/**70%** real-world Cup-to-Plate/Fork-in-Bowl.
- **[[2503.22020|CoT-VLA]]** — A **7B** ==VILA-U== unified multimodal VLA that predicts a future-frame token as a ==visual subgoal== *first*, then conditions actions on it, trained jointly on robot demos and action-less EPIC-KITCHENS video; **+17%** real-world and **+6%** simulation over SOTA VLAs — the subgoal *is* the plan, not a description of it.
- **[[2508.07917|MolmoAct]]** — An Action Reasoning Model whose ==three-stage autoregressive pipeline== emits ==depth-aware perception tokens==, ==visual reasoning traces==, then byte-level BPE-tokenized actions; **86.6%** LIBERO, **72.1%** SimplerEnv variant-aggregation (**+7.8pp** over RT-2-X), and visual-trace steering reaches **75%** SR (**+33pp** over natural-language steering).
- **[[2502.05855|DexVLA]]** — A VLA pairing a 2B VLM with a billion-parameter ==diffusion action expert== under ==three-stage embodied curriculum learning==, emitting internal ==sub-step reasoning== as intermediate language so the VLM is an implicit planner with no external module; **0.92** shirt-folding (baselines ~0), **0.90** novel-embodiment <100 demos — language sub-steps as output-head CoT.
- **[[2403.01823|RT-H]]** — An action-hierarchy VLA (PaLI-X 55B) using a two-phase query to first predict a ==language motion== ("move arm left") then condition the action on it, with motions auto-extracted from proprioception; **+15%** avg SR over RT-2, **20%** lower action MSE, language-motion human corrections lifting SR **40% → 63%** — the language-intermediate-as-CoT exemplar.
- **Cost trade-off** — Reasoning is grounded and interpretable, but generation cost scales with visual complexity (full subgoal frames are expensive).

#### 1.4 External Search

Treat the VLA as a policy *prior* and search at test time using a world model. MCTS rolls out candidate actions, scores via the world model, picks the best.

- **[[2509.22643|VLA-Reasoner]]** — A search wrapper around any pretrained VLA with ==online MCTS== over a learned ==world model==, ==Kernel Density Estimation== for action candidates + a ==vision-based value network== for dense state scoring; **+19pp** absolute on OpenVLA real-world (**22% → 41%**) and **+10pp** on π0-FAST.
- **[[2605.13119|VLAs-as-Tools]]** — A framework reframing VLAs as ==bounded callable executors== under a high-level ==VLM agent== via a ==bidirectional tool-family interface== plus ==Tool-Aligned Post-Training (TAPT)== with ==tool-family residual parameterization==; VLM calls per task drop **109.5 → 1.988** while lifting RoboTwin SR **+35.5pp** and invocation fidelity **+34.6pp** on OpenVLA-OFT.
- **Cost trade-off** — Maximally robust; can recover from a poorly-trained policy. **3-5×** slower; requires a usable world model.

#### 1.5 Affordance & Grasp Reasoning for Manipulation

A task-specialized form of the input-prompting slot: a VLM/LLM reasons explicitly about objects, affordances, occlusion, and physical properties *before* emitting a grasp, turning language-guided grasping in clutter into a deliberation problem rather than a detection one. Reasoning here selects *which* object/part to act on and *why*, not just *where* the gripper closes.

- **[[2503.16013|GraspCoT]]** — A 6-DoF grasping ==multimodal LLM== running a hierarchical ==Chain-of-Thought== (target ID → physical-property inference via unsupervised reasoning tokens → grasp selection) over 3D point clouds + flexible instructions, with the IntentGrasp benchmark; **0.5587** CR@0.2 (**+0.2683** over SOTA), ablating CoT drops CR **25.4%** — physical-property CoT for grasping.
- **[[2503.13082|FreeGrasp]]** — A zero-shot pipeline where ==GPT-4o== reasons over ==mark-based visual prompting== to pick the next object to grasp in clutter, via Molmo, LangSAM, and GraspNet, plus the FreeGraspData benchmark; up to **80%** easy-ambiguous SR (**10-20%** medium, **0-10%** hard) vs ThinkGrasp's near-total failure on medium/hard — reasons next-object selection under occlusion.
- **[[2503.12609|VISO-Grasp]]** — A framework unifying ==VLM spatial reasoning== (occlusion reasoning + target-aware decluttering via AMOV3D), velocity-field Next-Best-View planning, and uncertainty-guided multi-view grasp fusion for 6-DoF grasping of invisible targets; **87.5%** Average Final Success Rate at **3.10** attempts (static views **52.5-60.0%**) — reasoning-driven active view planning.
- **[[2503.00778|AffordGrasp]]** — A training-free framework doing ==in-context affordance reasoning== with a VLM, grounding object part-level affordances for open-vocabulary task-oriented grasping in clutter with an interpretable reasoning trace; **85%** single-object and **77%** cluttered-scene success, zero-shot to novel objects — affordance reasoning bridges task understanding and grasp.
- **[[2502.20041|3D-AffordanceLLM]]** — A method reframing 3D affordance detection as ==Instruction Reasoning Affordance Segmentation==, fusing a frozen ==LLM== with an affordance decoder via a `[SEG]` token for open-vocabulary masks, pre-trained on referring part segmentation; **30.43%** zero-shot mIoU (**+8%**), **36.33%** mAP50 on unseen pairs — instruction-reasoning over 3D affordances.
- **[[2407.11298|ThinkGrasp]]** — An iterative closed-loop system using ==GPT-4o== strategic reasoning to pick target or obstructing objects in heavy clutter, with a k×k grid for grasp-region suggestion and LangSAM/VLPart masking, progressively uncovering occluded objects; **0.980** general / **0.789** heavy-clutter sim success (VLG **0.753**/**0.511**) — strategic reasoning for part grasping.
- **[[2403.08248|CoPa]]** — A VLM manipulation framework decomposing 6-DoF control into ==Task-Oriented Grasping== and ==Task-Aware Motion Planning==, using ==GPT-4V== + ==Set-of-Marks== visual prompting to generate fine-grained spatial constraints between object parts, solved via constrained optimization; **63%** success across 10 real-world tasks (beats VoxPoser) with minimal prompt engineering.

#### 1.6 Memory & Cognitive-Map-Augmented Reasoning

A variant of the input-prompting slot where reasoning runs over an *externalized, persistent state* — a cognitive map, spatial knowledge graph, or multi-memory store — instead of the raw observation alone. The map/memory is the reasoning substrate: the LLM/VLM queries and updates it across long horizons, so deliberation accumulates rather than restarting each step.

- **[[2607.14252|MEMORA]]** — An ==Embodied Action Memory (EAM)== system built from egocentric video via four ==typed memory stores== (Environment, Entity, Activity, Inferred Knowledge) with online ==Memory Editor== revision and ==offline consolidation==; **+20.5pp** memory-assessment accuracy, **+16.6%** OOD generalization planning, **~18×** fewer entity records vs append-only logs.
- **[[2606.29786|OP3DSG]]** — Builds a unified open-vocab 3D scene graph (objects + interactive parts + spatial/functional relations + affordances) via ==knowledge-guided part detection== and ==geometry-anchored, CoT-inspired multi-agent LLM reasoning==; **+31.2pp** part-node R@3 on UniGraph3D, deployed on a Stretch3 robot for QA/planning/navigation.
- **[[2601.13132|GaussExplorer]]** — An embodied exploration + reasoning framework over ==semantic 3D Gaussian Splatting== (open-set CLIP per Gaussian), where an LLM extracts query 'evidence categories' to search-and-cluster objects and a VLM ==novel-view judge== evaluates perturbed camera poses; **57.8** LLM-Match EM-EQA (3D-Mem **54.6**), **12.87** 3D mIoU referring segmentation.
- **[[2508.01415|RoboMemory]]** — A ==brain-inspired multi-memory== agentic framework with a Perception-Memory-Retrieval-Planning-Execution loop and Planner-Critic module, unifying four parallel stores (Temporal, Spatial ==Knowledge Graph==, Semantic, Episodic) over a LoRA-finetuned VLA; **70.5%** avg EmbodiedBench SR (Claude-3.5-Sonnet **69.5%**), real-world repeat-task SR **26.67% → 46.67%**.
- **[[2506.17629|CLiViS]]** — A ==training-free== embodied-visual-reasoning framework orchestrating LLM↔VLM synergy: the LLM emits focused sub-instructions, the VLM perceives target video segments, and both update a =='Cognitive Map'== (Scene Navigation + Object Relation Graphs) + Evidence Memory; **55.4%** OpenEQA, **69.4%** EgoSchema (**48.4%** avg), beating Socratic models **+20.2%**.
- **[[2505.13948|Memory-Centric-EQA]]** — A ==memory-centric== Embodied-QA framework (MemoryEQA) centralizing a memory store to guide planner, stopping, and answering modules, via a ==viewpoint-contrastive== update rule, entropy-based adaptive retrieval, and a query-complexity dynamic-k mechanism, plus the MT-HM3D benchmark; **43.11%** SR (**+9.9pp**) with fewer exploration steps, SOTA on OpenEQA.

**Reasoning Slot — Decision Matrix**

| Need | Recommendation |
|---|---|
| Prototyping or language-heavy tasks | ==Input Prompting== (zero new params) |
| Real-time deployment (answer-only latency) | ==Latent Reasoning== ([[2604.18486\|OneVL]] / [[2604.22709\|Abstract-CoT]]) |
| Multi-stage manipulation needing interpretability | ==Output Head== ([[2503.22020\|CoT-VLA]] / [[2508.07917\|MolmoAct]]) |
| Safety-critical / novel tasks (acceptable latency) | ==External Search== ([[2509.22643\|VLA-Reasoner]] / [[2605.13119\|VLAs-as-Tools]]) |

^dm-1

> [!star] Key Papers
> - [[2604.18486|OneVL]] — Latent slot, beats explicit CoT at answer-only latency; **88.84 PDM-score** on NAVSIM; the 2026 latent-reasoning frontier
> - [[2503.22020|CoT-VLA]] — Output-head slot, visual subgoals as CoT steps; **+17%** real-world and **+6%** simulation
> - [[2509.22643|VLA-Reasoner]] — External-search slot, online MCTS with world model; the canonical search-augmented VLA
> - [[2605.13119|VLAs-as-Tools]] — Hierarchical external-search slot; VLM calls per task drop **109.5 → 1.988** via TAPT

^key-papers-1

> [!success] Where to Reason
> Every VLA pipeline has four candidate slots for inserting reasoning. Picking the wrong slot makes reasoning a latency burden; picking the right one is a free accuracy win. The 2026 default — latent + auxiliary decoder supervision — extracts CoT-quality reasoning at answer-only latency, but legacy deployments may still favor output-head visual CoT when interpretability dominates.

> [!tip] The Slot Determines the Cost Curve, Not Just the Capability
> The four slots are not interchangeable accuracy boosts — they sit at different points on the latency-interpretability-trainability surface, and the *binding constraint* decides the slot. Input prompting costs zero parameters but cannot reason about what the VLM never verbalizes; latent reasoning is the only slot that buys CoT-quality inference at *answer-only* latency (§3); output-head visual CoT is the only slot a human can audit step-by-step (§2); external search is the only slot that can recover from a *novel* failure at test time but pays a per-rollout tax (§4). The recurring mistake is bolting reasoning onto the output head for real-time control — where its latency is fatal — when latent reasoning would have delivered the same accuracy invisibly. Cross-reference [[07_Latent-World-Models#4. Latent Reasoning for Embodied AI]] for the latent-substrate mechanics these slots are built on.

^insight-1

---

## Part B — Reasoning Methods

*Visual CoT, latent reasoning, test-time search, reasoning-traced training.*

### 2. Visual Chain-of-Thought

The first wave of VLA reasoning ported language CoT to *visual* subgoals — instead of "thinking in words," the model first predicts a future image (the subgoal) then generates actions conditioned on that image. The fundamental design choice is whether subgoals are ==stage-based== (discrete future-frame snapshots at goal states — "first the cup is grasped, then it's at the kettle lip") or ==continuous== (interactive spatial guidance threaded through every step). Stage-based subgoals are interpretable and cheap; continuous guidance enables human-in-the-loop correction at the cost of synchronization complexity.

#### 2.1 Stage-Based Visual Subgoal Generation

Predict discrete future-frame snapshots at goal states; condition actions on the predicted subgoal. The standard "subgoal-then-act" loop.

- **[[2607.08024|APIVOT]]** — A VLM-based TAMP planner adaptively interleaving language with ==visual thoughts== (K=16 latent tokens encoding imagined future observations, cosine-aligned to real image features) via three-stage SFT, choosing modality per subgoal; **0.419** avg SR (**+8.1pp** over best VLM baseline), **91%** of 'Always-Image' SR at **-39%** token usage.
- **[[2606.31329|3D HAMSTER]]** — A hierarchical VLA whose ==depth-augmented VLM planner== (Qwen3-VL-8B) emits metric ==3D end-effector trajectories== (u,v,d) feeding a ==trajectory-conditioned 3D low-level policy (3DFA)==, fixing the 2D-to-3D "graffiti effect"; **66.2%** DroidSpatial-Bench (RoboBrain-2.5-8B **58.1%**), **44.8%** avg Colosseum SR vs 2D-guided **38.8%**.
- **[[2606.17937|ThinkingVLA]]** — A unified-autoregressive VLA that interleaves ==forward textual CoT==, predicted future images, and ==inverse CoT== action reasoning in one causal sequence via a ==Mixture-of-Transformers== (thinking expert + action expert). **+15.2-19.6pp** over baselines on RoboTwin 2.0 Horizon=2, **+10pp** real-world ALOHA long-horizon; removing Inverse CoT cuts SR **15pp**.
- **[[2503.22020|CoT-VLA]]** — A **7B** [[2409.04429|VILA-U]] ==unified multimodal foundation model== jointly trained on robot demos + action-less EPIC-KITCHENS video; emits a future-frame token *first*, then conditions actions on it via ==hybrid attention== and ==action chunking==. **+17%** real-world and **+6%** simulation over baseline VLAs — the foundational stage-based recipe.
- **[[2507.16815|ThinkAct]]** — A ==dual-system framework== for ==reinforced visual latent planning== where a slow-thinking MLLM, fine-tuned with ==action-aligned rewards==, compresses reasoning into a ==compact visual plan latent== conditioning a fast action model. **84.4%** LIBERO and **+15.5pp** SimplerEnv Google-VM over base; **48.2%** EgoPlan-Bench2 and **59.8** RoboVQA BLEU, beating GPT-4V.
- **[[2508.07917|MolmoAct]]** — Action Reasoning Model: ==three-stage autoregressive pipeline + byte-level BPE action tokenization==, emits ==depth-aware perception tokens== + ==visual reasoning traces==. **86.6%** LIBERO, **+10pp** real single-arm; **72.1%** SimplerEnv OOD, **+7.8pp** vs RT-2-X, **+22.7pp** progress vs π0-FAST bimanual; ==visual-trace steering== **75%** SR, **+33pp** vs language.
- **[[2509.25681|dVLA]]** — A unified discrete ==diffusion VLA== converting vision/language/actions to discrete tokens under one objective, with ==multimodal CoT== generating visual subgoals + text reasoning + actions. **96.4%** LIBERO and **65%** real-world, CoT adding **+6.6pp** sim / **+12.5pp** real; ==prefix attention mask + dLLM-Cache== yield ~**2×** speedup (1.3→2.9 Hz) at <**1%** SR drop.
- **[[2503.11089|EmbodiedVSR]]** — A framework feeding dynamically-updated ==scene graphs== into a ==physics-constrained chain-of-thought== for per-step geometric consistency; introduces the ==eSpatial-Benchmark== and beats GPT-4o by **+18.4%** Arm Feasibility / **+6.7%** Success Judgment on eSpatial-RoboMIND, **100%** block-assembly description, **80%** real-world reassembly.
- **[[2604.14125|HiVLA]]** — A ==hierarchical manipulation system== whose ==High-Level VLM Planner== emits ==structured JSON plans== (subtasks + bounding boxes for ==object-centric image crops==) feeding a ==DiT Action Expert== via ==cascaded cross-attention==; **83.3%** avg SR on **9** RoboTwin tasks (**+17.7pp** vs H-RDT, **+42.7pp** vs π0) with emergent error correction.
- **[[2603.07530|ICLR-VR]]** — A ==Llama2-style causal transformer== for in-context imitation learning jointly predicting ==visual reasoning traces== (5-point gripper-position polylines) and actions, with ==reasoning-trace-masking== regularization; outperforms ICRT on **12** unseen real tasks, and **8-16**-step reasoning intervals cut inference **8×** at comparable accuracy.
- **[[2601.01618|Action-Sketcher]]** — A model rendering spatial intent as a *sparse* ==Visual Sketch== of geometric primitives in a ==See-Think-Sketch-Act== pipeline, with an ==adaptive token-gated mechanism== switching between reasoning and low-latency action. **96.0%** LIBERO-Long; ablation traces **61%** of failures to sketch errors, human corrections recover **+23.0pp**.
- **[[2510.07134|TrackVLA++]]** — A visual-tracking VLA adding ==Polar Chain-of-Thought== (FOV discretized into angle-distance sectors as compact vocabulary tokens) plus a confidence-gated ==Target Identification Memory== that freezes target identity through occlusions; **74.0%** EVT-Bench distracted tracking (NavFoM **62.0%**), **+7-17%** real-world Unitree GO2 — lightweight spatial CoT.
- **[[2508.15874|Spatial-Policy]]** — A closed-loop visuomotor framework that injects explicit ==spatial reasoning== via a VLM-generated ==spatial plan table== to guide physically-plausible future-video prediction, then acts via a flow-based diffusion policy with dual-stage feedback; **86.7%** Meta-World (best baseline **53.7%**), **59.6%** iTHOR, **1.84×** faster than VideoAgent.

#### 2.2 Interactive & Continuous Spatial Guidance

Subgoals threaded through continuous interaction — humans can inject points, boxes, or traces mid-task to correct visual ambiguities.

- **[[2605.13632|GTA-VLA]]** — An interactive VLA framework with structured ==Guide-Think-Act== reasoning and optional human spatial guidance (points, boxes, traces); an ==asynchronous "slow reasoning, fast action" design== keeps control real-time. **98.6%** LIBERO, **+22pp** SimplerEnv-Plus unseen-object, human guidance recovers **+20%** of failures (SimplerEnv-Bridge **81.2% → 86.1%**).

#### 2.3 Training-Free Visual Foresight via Generative Priors

A training-free variant of visual CoT: instead of a jointly-trained VLA emitting a subgoal, an off-the-shelf image/video generation model produces the foresight image or rollout, and a separate VLM-constraint or geometric-grounding stage converts it into an executable trajectory — no policy network is trained at all.

- **[[2603.07744|AeroPlace-Flow]]** — A training-free framework where an ==image-editing model== generates a ==visual foresight goal image== for language-grounded aerial placement, then ==3D object-flow inference== grounds it into an executable path; **88/100** foresight success, **80%** flow-extraction success, **75%** end-to-end hardware placement SR.
- **[[2603.05757|EmboAlign]]** — A training-free framework filtering ==VGM-generated rollouts== via a ==two-tier scoring system== (V-JEPA-2 plausibility + ==VLM-derived compositional constraints==), then refining the selected rollout via ==nonlinear trajectory optimization==; **68.3%** avg real-robot SR, a **+43.3pp** gain over constraint-only and video-only baselines.

**Visual CoT — Decision Matrix**

| Need | Recommendation |
|---|---|
| Multi-stage manipulation with distinct goal states | [[2503.22020\|CoT-VLA]] (stage-based subgoals) |
| Interpretable depth-aware reasoning traces | [[2508.07917\|MolmoAct]] (depth tokens + attention regions) |
| Human-in-the-loop spatial correction | [[2605.13632\|GTA-VLA]] (interactive guidance) |
| RL-trained visual latent planning | [[2507.16815\|ThinkAct]] (reinforced planning module) |
| Diffusion-based action with multimodal CoT | [[2509.25681\|dVLA]] |
| Physics-constrained scene-graph CoT | [[2503.11089\|EmbodiedVSR]] |

^dm-2

> [!star] Key Papers
> - [[2503.22020|CoT-VLA]] — Foundational visual CoT for VLA; **+17%** real-world and **+6%** simulation; leverages action-less video for subgoal training
> - [[2605.13632|GTA-VLA]] — Interactive spatial guidance as first-class CoT modality; **98.6%** LIBERO, **+22pp** SimplerEnv-Plus, **+20%** human-recovery rate
> - [[2507.16815|ThinkAct]] — RL-driven visual latent planning that bridges CoT and latent reasoning
> - [[2508.07917|MolmoAct]] — Depth-aware perception tokens + visual reasoning traces; interpretable manipulation reasoning

^key-papers-2

> [!tip] When Visual CoT Helps
> Visual CoT shines for **multi-stage manipulation** where each stage has a visually distinct goal state ("first the cup is grasped, then it's at the lip of the kettle, then it's pouring"). For continuous skills (polishing a surface), visual subgoals are too abrupt — use latent reasoning instead (§3). Cross-reference [[04_VLA#4. Reasoning & Planning-Augmented VLAs]] for the broader reasoning-and-planning landscape that feeds into visual CoT, and [[06_WAM#5.1 Visual Chain-of-Thought]] for how WAM-integrated visual subgoal generation composes with world-model-augmented VLAs.

^insight-2

---

### 3. Latent Reasoning — Token-Free CoT

The 2026 frontier. Instead of emitting a long text trace and paying its inference cost, reason in the model's hidden state. Two recipes have emerged.

#### 3.1 Pre-allocated Latent Reasoning Tokens

Reserve a fixed budget of "reasoning slots" in the input sequence; let the model use them however it wants. The training objective shapes the slot usage without forcing words.

- **[[2606.31167|MIRTH]]** — A VLA fusing ==dual-scale temporal memory hubs== (long-term workspace + short-horizon) with ==mutual-information (InfoNCE) latent reasoning tokens== and ==parallel vector-wise action decoding==; **95.3%** LIBERO-Long (OpenVLA **53.7%**), **12.1%** emergent error recovery (vs **5.2%** baseline) as reasoning tokens self-organize into task clusters.
- **[[2604.22709|Abstract-CoT]]** — Replaces verbalized rationales with ==discrete abstract tokens== from a ==reserved vocabulary==; two-stage ==policy-iteration warm-up== + ==warm-started GRPO== with an ==attention-mask information bottleneck== forcing answers to depend on abstract tokens. Cuts reasoning tokens **up to 12×** at equal-or-better accuracy on MATH/AlpacaEval/HotpotQA (Qwen3+Granite).

#### 3.2 Auxiliary-Decoder-Supervised Latent Reasoning

Same idea as 3.1 but with explicit auxiliary decoders that *can* recover the reasoning trace if needed (interpretability) — without paying the cost at inference.

- **[[2607.13926|S2-VLA]]** — A driving VLA decoupling semantic and spatial reasoning to fix the ==semantic-physical gap==: an ==InternVL3== ==Multi-Scale Semantic Stream== extracts intent while a ==Task-Driven Spatial Stream== (ViT + ==BEV map==) preserves geometry, fused via a ==Dual-Stream Planning Adapter==; **87.1** PDMS on NAVSIM, **98.4%** No-Collision from a single front camera.
- **[[2604.18486|OneVL]]** — A VLM with language + visual latent tokens supervised by ==dual auxiliary decoders== (future-frame/CoT-text, training-time only); a ==prefill mechanism== runs latent tokens in one pass at ==answer-only latency== while *exceeding* explicit AR CoT (**4.46s** vs **6.58s**). **88.84 PDM-score** on NAVSIM (**+2.64 pts** vs 8B); real-time variant **86.83 PDM** at **0.24s**.
- **[[2601.05248|LaST0]]** — A dual-system ==Mixture-of-Transformers== VLA whose ==Latent Spatio-Temporal CoT== compresses 2D-visual / 3D-geometric / proprioceptive states into compact latent embeddings, a slow reasoning expert feeding a fast acting expert at asynchronous frequencies; **98.1%** LIBERO, **82%** RLBench, **15.4 Hz** — **14×** faster than explicit CoT.
- **[[2512.22939|ColaVLA]]** — A driving VLA whose ==Cognitive Latent Reasoner== relocates VLM CoT from text into ==decision-oriented meta-action embeddings==, feeding a ==hierarchical parallel planner== (coarse-to-fine, causality-preserving attention). nuScenes L2 **0.30m**, **-23%** collision; **727ms/frame** — over **5×** faster than text-VLM CoT (**>3700ms**). Driving counterpart to OneVL.
- **[[2511.19859|VITA]]** — An ==implicit visual CoT== model: future-frame prediction is internalized as an *inductive bias* over a ==shared discrete latent== (cross-modal VQ) rather than emitted explicitly, bridging the dense-vision/sparse-action gap. **96.7%** LIBERO, **80.5%** six real tasks, at **60.6ms** / **60 Hz** — implicit subgoals beat explicit prediction while staying real-time.
- **[[2509.05578|OccVLA]]** — A driving VLA whose ==Vision-Language-Occupancy backbone== treats dense ==3D occupancy prediction== as an *implicit* reasoning step (latent VQ-VAE, inactive at inference), decomposing planning into CoT meta-actions + a planning head; **0.28m** nuScenes L2 and **59.5%** NuScenes-QA from camera-only — implicit occupancy as latent reasoning.

#### 3.3 RL-Trained Latent Reasoning

Reinforce the latent reasoning with a verifiable reward signal that ties latent quality to downstream action quality.

- **[[2607.08724|LMP]]** — Reframes control reasoning as ==autoregressive variational inference== over an EOS-terminated latent sequence with ==decaying decoder variance== as a length penalty, via ==PPO-style latent RL==; beats Diffusion Policy on DROID (**95%** clean-table) and LIBERO-90 hard tasks (**0.645** vs **0.463**), steps anti-correlate with uncertainty (**r=-0.518**).
- **[[2604.28192|LaST-R1]]** — A VLA pairing ==continuous latent CoT== (==DINOv3==-grounded) with ==Latent-to-Action Policy Optimization (LAPO)== — RL jointly optimizing latent reasoning + actions — plus an ==adaptive latent CoT== stop-token for variable depth. **99.8%** avg LIBERO (one-shot SFT warm-up), **+44%** real-world over warm-up, only **8%** drop under unseen conditions.
- **[[2604.27998|Latent-GRPO]]** — A method patching three GRPO-on-latent failure modes causing ==model collapse==: ==Invalid Sample Advantage Masking==, ==One-Sided Noise Sampling==, ==Optimal Correct Path First-Token Selection==. **+7.86 pp** Pass@1 over Latent-SFT (low-difficulty), **+14.77 pp** (high-difficulty), with **3-4× shorter chains** than explicit GRPO.
- **[[2604.20328|HyLaR]]** — A method fixing hybrid discrete-continuous ==variance mismatch== via ==Decoupled Policy Optimization (DePO)==: latent actions as ==von Mises–Fisher (vMF) distribution==, ==separate tighter clipping==, ==closed-form KL==, plus a ==canvas mode==. On Qwen2.5-VL-7B: **+7.33%** [[2312.14135|V*]], **+14.50%** HRBench-8K, **-7.11%** HallusionBench.
- **[[2511.15407|IPR-1]]** — An Interactive Physical Reasoner combining ==VLM semantic priors==, ==world-model imagination==, and RL over a physics-centric ==PhysCode== latent action space via ==prediction-reinforced GRPO==; **0.252/1.173/0.493** mean Survival/Curiosity/Utility across **200** games, beating GPT-5; extends RL-trained latent reasoning beyond robots to physical-reasoning agents.

**Latent Reasoning — Decision Matrix**

| Need | Recommendation |
|---|---|
| Beat explicit CoT at answer-only latency | [[2604.18486\|OneVL]] (dual auxiliary decoders + prefill mechanism) |
| Token-free reasoning in abstract embedding space | [[2604.22709\|Abstract-CoT]] (K pre-allocated slots, parallel processing) |
| Adaptive reasoning depth tied to task success | [[2604.28192\|LaST-R1]] (RL-shaped DINOv3-grounded latent) |
| Stabilize GRPO on continuous latent space | [[2604.27998\|Latent-GRPO]] (advantage masking + one-sided noise + first-token selection) |
| Hybrid discrete-continuous reasoning (hyperspherical) | [[2604.20328\|HyLaR]] (vMF DePO + canvas-mode tokens) |
| Physical-commonsense substrate at WAM scale | [[2503.15558\|Cosmos-Reason1]] |

^dm-3

> [!warning] Stability Is Not Free in Latent RL
> Both [[2604.27998|Latent-GRPO]] and [[2604.20328|HyLaR]] document the same root cause from different angles: naive policy-gradient methods in continuous latent space cause model collapse. The fixes converge on three principles — (1) bound exploration off-manifold (advantage masking / vMF distribution), (2) align gradient direction with advantage sign (one-sided noise / decoupled clipping), (3) avoid mode averaging across alternate correct paths (first-token selection). Any new RL-for-latent-reasoning method should be checked against these three failure modes.

#### 3.4 The Silenced-Latents Pathology

A diagnostic result orthogonal to architecture: MLLM latent reasoning can be **semantically rich but functionally ignored** during answer prediction — the autoregressive decoder takes a "shortcut" through the raw visual input rather than routing through the latent reasoning slots. Improving latent quality alone does *not* fix this.

- **[[2605.02735|Silenced-Visual-Latents]]** — A ==frozen-backbone, two-stage inference-time latent optimization== framework: Stage I ==Visual Latent Warm-Up== (==chunk-wise contrastive alignment==); Stage II ==Latent-to-Answer Reinforcement== (==confidence-progression reward== + ==NES==). On Qwen2.5-VL-7B: **+8.66%** IQTest, **+5.00%** MM-Vista; MMVP **72.33% → 73.67%**.

> [!star] Key Papers
> - [[2604.18486|OneVL]] — First latent CoT to *beat* explicit CoT while preserving answer-only latency; **88.84 PDM-score** on NAVSIM — the 2026 latent-reasoning frontier
> - [[2604.22709|Abstract-CoT]] — Token-free reasoning in abstract embedding space; eliminates the discrete-token bottleneck
> - [[2604.27998|Latent-GRPO]] — GRPO for latent reasoning with three collapse fixes (invalid-sample masking, one-sided noise, first-token selection); **+14.77 pp** hard tasks, 3–4× shorter chains than explicit GRPO
> - [[2604.20328|HyLaR]] — Decoupled PPO with vMF latent distribution + canvas-mode discrete-continuous interleaving; **+14.50%** HRBench-8K
> - [[2605.02735|Silenced-Visual-Latents]] — Exposes the quality-vs-utilization gap: a latent system can be semantically rich yet functionally ignored; fixes via inference-time warm-up + NES utilization reward without touching the backbone

^key-papers-3

> [!tip] The Latent Reasoning Surprise — and Why Utilization ≠ Quality
> The conventional wisdom was that explicit text CoT works because it forces sequential decompose-then-act reasoning. [[2604.18486|OneVL]] falsified this: with dual-modal latent supervision, latent reasoning *outperforms* explicit CoT at answer-only latency — the most important VLA-reasoning result of 2026. But [[2605.02735|Silenced-Visual-Latents]] adds the essential caveat: a latent system can score well on intrinsic latent-*quality* probes while the answer head learns a shortcut that *ignores* those latents entirely. Improving latent quality does not fix utilization. Any latent-reasoning ablation must measure both — does perturbing the latents change the answer (utilization), *and* do the latents encode the right information (quality)? The two diverge. Cross-reference [[07_Latent-World-Models#4. Latent Reasoning for Embodied AI]] for the latent-substrate mechanics and [[04_VLA#1. Design-Space Principles]] for where the latent slot sits in the VLA backbone.

^insight-3

---

### 4. Test-Time Search

When the policy is uncertain, search for a better action at deployment time. Four flavors have emerged, each making a different bet on *what to search over*: roll forward candidate actions through a world model and pick the highest-scoring trajectory ([[2509.22643|VLA-Reasoner]]), wrap that search around a pre-trained policy without retraining ([[2508.12211|VLAPS]]), verify semantic alignment between the VLA's text plan and predicted action outcomes ([[2510.16281|SEAL]]), or delegate subtasks to specialized VLA tools under a high-level VLM agent ([[2605.13119|VLAs-as-Tools]]). The first three search over action *space*; the fourth searches over policy *hierarchy*.

#### 4.1 World-Model MCTS Rollouts

Sample candidate actions from the VLA, roll each forward through a learned world model, score the resulting trajectories, execute the best. The canonical "search by simulation" pattern.

- **[[2509.22643|VLA-Reasoner]]** — Plug-in test-time framework wrapping any VLA in ==online MCTS== with the ==world model== as simulator: ==KDE== samples candidates (**91.5%** vs **85.0%** Gaussian), a ==vision-based value network== scores rollouts, best executes. Real-world OpenVLA **+19pp** (**22% → 41%**), **+10pp** π0-FAST (**64% → 74%**); ==3-5× slower== but rescues miscalibrated policies.

#### 4.2 Model-Based Search Wrapped Around Pre-Trained VLAs

Same MCTS skeleton but treats the VLA as a fixed prior; no retraining. A deployment-time robustness boost for legacy policies.

- **[[2607.03751|SVA]]** — Distills ==Monte-Carlo Tree Search== into a lightweight ==Q-value model== (LoRA + MLP heads), enabling frozen-VLA best-of-N action evaluation with no simulator at deployment; π0 SimplerEnv **38.5%→50.7%**, π0.5 RoboTwin 2.0 **36.0%→43.5%**, beating a 3× larger VLA at **27%** lower latency.
- **[[2508.12211|VLAPS]]** — An inference-time framework integrating ==MCTS-inspired model-based search== + a ==world model== over temporally-abstract ==action chunks==, the pretrained VLA supplying a ==prior distribution== biasing search; **+42pp** absolute SR on a 50k-step VLA across LIBERO, and lifts a **93M** Octo to **99%** Libero-Spatial — matching **3.3B** π0-FAST without retraining.

#### 4.3 Runtime Semantic Alignment Verification

Search over candidate actions via *semantic verification* rather than world-model rollout — check whether predicted action outcomes match the VLA's own text plan. Targets the CoT-faithfulness gap.

- **[[2606.27268|E-TTS]]** — An embodied ==test-time scaling== framework doing ==Reasoning-Action Joint Sampling== (coupled candidates + history buffer) scored by ==dual vision-language verifiers== (reasoning + action) for adaptive online selection, plus feedback-guided refinement on rejections; up to **+33.14%** sim / **+26.62%** real across VLAs, **+150%** relative SR at **+46.6%** latency.
- **[[2604.21232|ReCAPA]]** — A ==Hierarchical Predictive Correction== framework predicting higher-level semantics from lower-level steps to emit early corrective signals, with multi-level ==Prompt-Trajectory Alignment== (Sinkhorn OT + score-field) and three-tier correction resampling actions / adjusting subgoals; **58.65** VisualAgentBench, **0.75** AI2-THOR SR, lowest Error-Propagation-Rate.
- **[[2511.14178|VLA-Pilot]]** — A training-free inference-time steering method whose ==Embodied Policy Steering CoT== uses an MLLM self-critic + spatial keypoints to set open-world steering objectives, then an ==Evolutionary Diffusion== loop evolves (not just selects) action proposals; **+0.31** real-world MSR, **0.50** OOD (baselines **0.12-0.19**), matching 50-demo fine-tuning.
- **[[2510.16281|SEAL]]** — Training-free runtime policy steering targeting the ==CoT faithfulness gap==: ==Hypothesize== (K candidates), ==Predict== (learned dynamics), ==Verify== (a VLM matches outcome to text plan); any backbone. **94-97%** in-distribution, **+15pp** (to **53%**) on novel compositions, **+17pp** (to **45%**) under viewpoint shifts, **347ms/step** (**~1.5-2×** latency) at K=10.

#### 4.4 Hierarchical Agent Orchestration

Search over policy *hierarchy* — a high-level VLM agent delegates subtasks to specialized VLA tools instead of searching candidate actions. The "policy hierarchy supplies the reasoning structure" alternative.

- **[[2607.18060|RoboHarness]]** — An agentic framework where a coding agent orchestrates heterogeneous ==VLA==/==RL==/==TAMP== policies as callable skills via ==Understanding==/==Memory==/==Self-Evolution== skills and a ==Memory Bridge== for in-distribution handoffs; **98.7%** LIBERO SR, **95.2%** LIBERO-LoHo, **93.2%** avg SR across 7 LIBERO-Plus perturbations, **135** real-robot tasks.
- **[[2607.08448|Harness VLA]]** — An ==asymmetric hierarchical== framework where an LLM planner orchestrates a fixed primitive library, treating a frozen VLA as a single retryable ==contact-rich primitive== alongside analytic primitives, guided by ==Task-Specific== + ==Global Memory==; **82.4%** LIBERO-Pro under perturbation (RATS **43.8%**), **96.0%** standard LIBERO with no VLA fine-tuning.
- **[[2607.06256|Semantic Handoff Diagnosis]]** — A ==plan-act-verify-replan== harness with ==handoff-aware postconditions== + multi-view VLM verification, diagnosing why competent chained π0.5 skills fail; isolated skills succeed but BEHAVIOR-1K end-to-end progress is only **19.5%**.
- **[[2607.05377|Cortex]]** — A ==bidirectionally aligned== dual-system agent pairing a ==VLM cognitive orchestrator== with a ==π0.5 reactive executor== via 32 canonical skill primitives + ==event-balanced sampling==; **95.5%** zero-shot LIBERO-Long, **65%** real-world long-horizon SR vs π0.5's **0%**.
- **[[2605.13119|VLAs-as-Tools]]** — A hierarchical framework: a high-level VLM emits ==discrete tool-invocation messages== (each VLA a bounded sub-skill), gets ==progress feedback==, and replans; ==Tool-Aligned Post-Training (TAPT)== with ==tool-family residuals==. VLM calls drop **109.5 → 1.988** (~**55×**) per task, lifting **+35.5pp** RoboTwin and **+34.6pp** Faithful Rate on LIBERO-CF-Long.

**Test-Time Search — Decision Matrix**

| Need | Recommendation |
|---|---|
| Recover from poorly-calibrated policy via tree-search | [[2509.22643\|VLA-Reasoner]] (online MCTS + world model) |
| Robustness boost for legacy VLA without retraining | [[2508.12211\|VLAPS]] (model-based search wrapper) |
| Fix CoT-action disagreement at runtime | [[2510.16281\|SEAL]] (training-free K-candidate verification) |
| Hierarchical multi-skill orchestration | [[2605.13119\|VLAs-as-Tools]] (TAPT + tool-family residuals) |

^dm-4

> [!star] Key Papers
> - [[2605.13119|VLAs-as-Tools]] — Inverts VLA-as-top-level stack: VLAs become bounded callable tools under a high-level VLM agent via TAPT; VLM calls per task drop **109.5 → 1.988**; **+35.5pp** RoboTwin and **+34.6pp** instruction fidelity — the cleanest hierarchical-reasoning win
> - [[2509.22643|VLA-Reasoner]] — Online MCTS with world model; recovers from policy mistakes via tree-search
> - [[2508.12211|VLAPS]] — Model-based search wrapping pre-trained VLAs; improves performance without retraining
> - [[2510.16281|SEAL]] — Runtime reasoning-action alignment verification; targets the **CoT faithfulness gap** by checking that predicted action outcomes match the VLA's own text plan; training-free, **+15pp** on novel compositional tasks

^key-papers-4

> [!tip] When Test-Time Search Pays
> Use search when (1) the task is **safety-critical** (medical, autonomous driving), (2) the **policy is known to be miscalibrated** under distribution shift, or (3) **inference latency is acceptable** (planning, not real-time control). Skip it for fast pick-and-place where imitation suffices. [[2510.16281|SEAL]] specifically helps when **CoT and actions disagree** — the failure mode for reasoning VLAs in novel scenarios. Cross-reference [[06_WAM#5.4 Imagination & Test-Time Reasoning]] for adaptive test-time imagination budget patterns ([[2602.08236|AVIC]]).

^insight-4

---

### 5. Reasoning-Traced Training

The 2026 trend: don't just *use* reasoning at test time — *train* the reasoning trace itself with verifiable rewards. The reasoning becomes part of the model's parameters, not a separate module. Four supervision strategies have emerged, each targeting a different failure mode: ==verifiable-reward== reasoning checks intermediate steps against programmatic predicates, ==grounded CoT== ties each step to visual evidence, ==teacher-guided== reasoning distills traces from strong reasoning models, and the ==outcome-reward trap== shows what happens when *none* of these process-level supervisions are applied.

#### 5.1 Verifiable-Reward Reasoning

Use a programmatic checker (or a strong VLM) to verify each reasoning step; train via RL on verified traces.

- **[[2607.04681|Pinocchio]]** — A learned VLM critic scoring ==behavioral faithfulness== (**0.87** balanced accuracy) whose log-probs feed a dense ==GRPO== reward, training driving-VLA reasoning for causal alignment; faithfulness **27.7%→64.8%** over SFT, **1.6×** OOD-hazard causal-alignment gain.
- **[[2606.31260|SymPlan]]** — An embodied planner using ==BDDL-driven symbolic verification== for ==multi-granular RL rewards== (GCR/EP/SP) via DAPO, plus ==correctness-gated length compression (GroupAdapt)==; **97.3%** Strict Pass on BEHAVIOR-1000 (**+25.9%** over Qwen3-8B), **79%** shorter plans (207 tokens) without accuracy loss.
- **[[2603.21341|RoboAlign]]** — A two-stage VLA framework closing the reasoning-to-action ==modality gap== via ==SFT== on VQA/CoT data then ==GRPO== with a reward on ==action-token sequence similarity==; **+17.5%** relative SR on LIBERO, **+18.9%** CALVIN, **+106.6%** real-world, lifting internal-state KNN accuracy **39.06% → 69.79%**.
- **[[2602.11124|PhyCritic]]** — A multimodal ==critic model for Physical AI== trained via two-stage ==RLVR== (Physical Skill Warmup → ==Self-Referential Critic Finetuning== where the critic first generates its own reasoning+prediction before judging candidates); **68.0%** PhyCritic-Bench (SOTA open-source, **+12pp**), **63.9%** Cosmos-Reason1-Bench as a policy, from only **4,058** samples.
- **[[2510.23569|EgoThinker]]** — An egocentric reasoning model trained on ==EgoRe-5M== (5M egocentric QA with CoT rationales + dense hand-object grounding) via ==SFT then RFT (GRPO)== for spatio-temporal localization on Qwen2-VL-7B; **+4.4%** EgoPlan long-horizon planning, **+8.4%** Referenced-Egocentric-Skill, **80.3%** EK-Visor hand-object localization — first-person embodied CoT.
- **[[2509.25852|REVER]]** — Synthesizes the ==LEAP dataset== (Vision-Instruction-Plan triplets from kinesthetic demos), optimizes a ==grammar-aware verifiable reward== with ==GRPO== to train the **7B** ==RoboFarseer== planner. **76%** open-ended planning (**2×** Gemini-2.5-Pro), **59.3%** LEAP-L MCQ, **90%** real-world 'Bring food & drinks' (**+60pp**) — forces the trace to be *causally* correct.
- **[[2509.01944|AutoDrive-R2]]** — A driving VLA: SFT on a four-step ==CoT + self-reflection== dataset (nuScenesR²-6K), then ==GRPO== with a ==physics-grounded reward== (spatial alignment, vehicle dynamics, temporal smoothness) verifying trajectory feasibility. nuScenes L2 **0.19m** (beats EMMA+ 0.29m); Waymo zero-shot **0.20m** (**-33.3%**).
- **[[2508.13998|Embodied-R1]]** — A **3B** VLM trained with two-stage ==Reinforced Fine-tuning== to master four embodiment-agnostic ==pointing== reasoning skills (referring/region/functional grounding, visual-trace gen) via multi-task reward, beating template-rigid SFT; **87.5%** zero-shot real-world xArm (**+62%** over RoboPoint), **56.2%** SimplerEnv — RFT free-form reasoning over SFT.
- **[[2506.04308|RoboRefer]]** — A 3D-aware VLM for ==multi-step spatial referring== using a disentangled depth encoder + two-stage ==SFT-then-RFT== with metric-sensitive process rewards to teach generalized step-by-step reasoning over the 20M-QA RefSpatial corpus; **89.6%** single-step SU (Gemini-2.5-Pro **+5%**), **+17.4%** RefSpatial-Bench multi-step over Gemini.
- **[[2506.00070|Robot-R1]]** — An ==RL framework== (==GRPO==, DeepSeek-R1-style) for embodied reasoning that recasts next-state prediction as ==MCQA==, training a 7B LVLM to emit explicit `<reasoning>` before answering against a composite reward. **+31%** EmbodiedBench-Manip, **40-60%** SpatialRGPTbench gains; real pick-place **16.67% → 23.96%** — beats GPT-4o on low-level control reasoning.
- **[[2505.11175|VERGSA]]** — A framework adding real-time verification to generative skill acquisition: an ==ARLET-MCTS== scheme auto-labels dense rewards from execution feedback, and a fine-tuned ==Process Reward Model== critic verifies and selects scene configs + subtask supervisions; **+24%** ATSR novel / **+36%** encountered, PRM **0.91** vs LLM-judge **0.78** — PRM verifies reasoning steps.
- **[[2503.21696|Embodied-Reasoner]]** — A deep-thinking agent trained on synthesized ==Observation-Thought-Action (OTA)== trajectories via three stages (imitation → ==rejection-sampling tuning== → ==reflection tuning== on corrected failures); **80.96%** AI2-THOR SR (GPT-o1 **71.73%**), **+39.9%** composite over GPT-4o, **50%** less repetitive exploration — trace-synthesis + reflection training.

#### 5.2 Grounded CoT

Tie each reasoning step to *visual evidence*; reject ungrounded reasoning.

- **[[2607.01658|DriveTeach-VLA]]** — A driving VLA teaching "what to see, where to look" via ==Driving-aware Vision Distillation (DVD)== bbox self-distillation and ==2D Trajectory-Guided Prompts== grounding CoT + GRPO in feasible-path regions; **90.4** PDM-Score NAVSIM (**92.7** best-of-N), **0.30m** L2 / **0.12%** collision on nuScenes.
- **[[2606.30552|ZR-0]]** — A dual-stream VLA (Qwen3-VL-2B ==System 2== + ==Diffusion Transformer== ==System 1==) trained on dense ==Embodied Chain-of-Thought (ECoT)== supervision over ==ProcCorpus-60M==, bypassing ECoT generation at inference; **97.8%** LIBERO, **69.3%** RoboCasa GR-1, real xArm **76.0** vs π0.5 **67.8** — embodiment-agnostic reasoning drives cross-embodiment transfer.
- **[[2606.03784|ERVLA]]** — A VLA scaling embodied CoT via a **226M**-sample ==hierarchical CoT corpus==, a ==Mixture-of-Transformers== fusing a reasoning module + ==Diffusion Transformer==, and a ==CoT-dropout== supervising reasoning in training but predicting actions at inference; **86.9%** avg LIBERO-Plus + **53.2%** VLABench — grounded CoT works *only* when integrated.
- **[[2604.21396|VG-CoT]]** — Pipeline (==YOLO==/==PaddleOCR==/==Grounding DINO==/==GPT-4o==) tying steps to ==object/text bounding-box evidence==, rejecting ==hallucinated reasoning==; ==3-dim eval (Rationale Quality/Answer Accuracy/Reasoning-Answer Alignment)== lifts LLaVA-1.5-7B RQ **72.2 → 83.4**, AA **48.7 → 62.5** (Qwen2.5-VL-7B AA **68.5 → 73.6**); small-text mAP **48.7 → 33.6** stays hard.
- **[[2505.21906|ChatVLA-2]]** — A ==Dynamic Mixture-of-Experts== VLA that prevents pretrained-knowledge erosion during robot fine-tuning, with a ==Reasoning Following Enhancement Module== forcing actions to track the model's open-world CoT (not explicitly-trained reasoning); **82.7%** real-robot math-reasoning manipulation and **81.4%** open-world spatial-reasoning SR (**3.52×** over DexVLA).
- **[[2505.13888|InSpire]]** — A plug-and-play VLA adding an intrinsic ==spatial-reasoning VQA== step ('In which direction is the [object]?') *before* action prediction to suppress spurious visual-action correlations, with rule-generated ground-truth directions needing no annotation; **+10.0%** unseen LIBERO, **+26%** real-world π0-FAST, beating larger CoT-VLAs at **1B**.
- **[[2412.11974|EMMA-X]]** — An embodied multimodal action model (fine-tuned **7B** OpenVLA) trained on auto-annotated trajectories with ==grounded chain-of-thought== + ==look-ahead spatial reasoning==, segmented via ==HDBSCAN== + gripper-state changes. **+24.17%** SR over OpenVLA on 12 real WidowX tasks; ablating grounded CoT drops SR **43-55%** — grounding kills hallucinated plans.
- **[[2412.03293|Diffusion-VLA]]** — A robot foundation model unifying autoregressive ==self-generated reasoning== with a diffusion policy via a ==Reasoning Injection Module== that embeds the VLM's rationale into action generation with ==FiLM== for interpretable control; **63.7%** zero-shot bin-pick of 102 unseen objects (OpenVLA **28.4%**), **82 Hz** — foundational self-generated reasoning.
- **[[2407.08693|ECoT]]** — The foundational grounded-CoT-training method: emits ==visually-grounded reasoning steps== (plan → sub-tasks → bounding boxes → gripper positions) *before* actions, with a ==synthetic annotation pipeline== on [[2403.12945|Bridge-v2]]. Built on [[2406.09246|OpenVLA]]: **+28pp** SR; one reasoning correction adds **+48pp**; async recovers **40%** of latency.

#### 5.3 Teacher-Guided Reasoning

Use a strong reasoning model as a teacher; distill its reasoning traces into the VLA.

- **[[2606.04436|3DThinkVLA]]** — A VLA co-trained on action + 3D reasoning data, disentangling ==3D geometry perception== and ==spatial reasoning== into distinct ==latent== representations; ==online 3D reasoning distillation== transfers teacher reasoning to student prompts. SOTA **98.7%** LIBERO (**100%** Spatial/Object), **81.0%** zero-shot LIBERO-Plus, **93.3%** real Realman.
- **[[2604.17800|ReFineVLA]]** — A method augmenting datasets with ==natural-language reasoning annotations== from a ==Gemini 2.0 teacher==; ==selective transfer fine-tuning== freezes SpatialVLA's lower layers + ==BC + language modeling==. **+5.0pp** over SpatialVLA on WidowX (**+21.4pp** Spoon-on-Towel), **+2.3pp / +3.5pp** Google Robot, **+9.6pp** Move Near.
- **[[2511.22134|DualVLA]]** — A post-training framework partially decoupling reasoning and action to fix ==action degeneration==, via ==dual-layer data pruning== (scene-event + kinematic keyframes) keeping action-critical reasoning and ==dual-teacher distillation== (action + reasoning teachers); **61.0%** SimplerEnv (**+8.0%**), **45→60%** real dual-arm, **20%** faster.

#### 5.4 The Outcome-Reward Trap

A 2026 diagnostic with broad implications — what fails when none of the process-level supervisions above are applied.

- **[[2604.22074|CIR/SR-Reasoning]]** — A diagnostic showing that outcome-only ==RLVR== does *not* guarantee verifiable or causally-important reasoning — standard RLVR *decreased* CIR on **19** ReasoningGym tasks and SR on **17**. The fix: ==SFT on 64-512 expert traces== (CIR ≈ **0.4**, SR **0.65-0.75**) or ==auxiliary CIR/SR rewards== targeting the reasoning *process*.
- **[[2602.06033|VLM-Intuitive-Physics]]** — Compares interactive ==GRPO== vs ==supervised fine-tuning== teaching Qwen3-VL intuitive physics via block-tower stability/displacement; neither generalizes past training tasks, both plateau below human on real images (**0.6**/**0.59** vs **0.75-0.85**) despite decodable latent competence; echoes [[2604.22074|CIR/SR-Reasoning]]'s outcome-reward trap.

#### 5.5 Adaptive Reasoning Depth

Don't reason on every step — *learn when to*. The model is trained to gate between an explicit slow-reasoning mode and a fast direct-action mode, paying CoT latency only at decision-critical junctures. This is the trainable answer to the §7 reason-vs-reflex problem.

- **[[2607.01518|Overthink-Triggered Slowdown Attack]]** — A black-box ==genetic-algorithm== search over physically-realizable ==scene-text triggers== that forces LVLM "overthinking," exposing reasoning-depth gates as an attack surface; **6.96×** latency blowup (Gemma3), **4.74×** in a real-world camera-to-model test, transferable across Kimi-VL/Qwen3-VL.
- **[[2506.13757|AutoVLA]]** — A driving VLA with an ==adaptive dual-thinking mode== (fast direct action vs slow CoT) in one autoregressive backbone via ==physical action tokenization==; ==RFT (GRPO)== with a ==reward that penalizes unnecessary CoT== teaches the gate. **+10.6%** PDMS and **-66.8%** runtime on NAVSIM — reasoning only when the scenario demands it.
- **[[2505.11917|OneTwoVLA]]** — A unified VLA fusing ==cognitive reasoning== and action in one network, switching modes via ==[BOR]/[BOA] decision tokens==; trained on a synthetic reasoning-centric VL corpus co-trained with robot data. **87%** long-horizon SR (**+30pp** over VLA baselines), recovers from **80%** of errors vs ~57% — adaptive gating buys both efficiency and error recovery.
- **[[2606.12402|DIRECT]]** — A lightweight ==multimodal context-aware router== gating *which* VLM-planner configuration runs per task — CoT depth or model size — by ==maximizing a quality-vs-cost utility== over planner scores; matches "Thinking" models at **−30%** latency, beats the **32B** model by **5.1 pts**, cuts **32.4 s** on VLABench — gating across planners, not within one.

#### 5.6 Structured Spatial Reasoning

Train the VLM to reason over an *explicit spatial representation* — a 3D scene-graph, an object-centric blueprint, or a metric Bird's-Eye-View map — rather than free-form text, then optimize it with CoT-SFT + RL. Externalizing the spatial structure is the supervision signal that grounds spatial deliberation and curbs the layout/viewpoint hallucinations that plague vision-only spatial reasoning. This is the spatial-reasoning substrate the embodied policies in §5.1–5.2 build on.

- **[[2603.22279|3D-Layout-R1]]** — A text-conditioned spatial-layout editor reasoning directly over a ==3D bounding-box scene graph== as an iterative canvas, trained by ==CoT-SFT then GRPO== (physical-plausibility rewards) on a 15K-scene CoT-edit dataset; **+15%** Mean-IoU, **25-30%** lower center-distance error, **1.000** Collision-Free, matching Gemini-2.5-Pro with a **7B/8B** base.
- **[[2603.10370|GeoSense]]** — A multimodal reasoner treating ==3D geometry as an on-demand modality==, with ==Perception Tuning== teaching an 'Internal Sense Decision' token to trigger geometric features only when needed (no 2D-stream contamination); top rank across 10 benchmarks (**56.6** spatial / **55.9** general), activating geometry for only ~**35.68%** of samples — beats rigid fusion.
- **[[2601.01984|Thinking-with-Blueprints]]** — A method training VLMs to build and analyze an object-centric ==JSON-style 'blueprint'== of scene elements via ==SFT + RL== with GPT-4o/MCTS traces and blueprint-aware rewards (Object-Cardinality, Causal-Consistency) + anti-shortcut augmentation; **92.7%** SAT-val (**+35.9%**), **79.7%** SAT-test OOD, beating GPT-5-Thinking with a **7B** base.
- **[[2511.16160|Video2Layout]]** — A framework reconstructing a ==metric-grounded cognitive map== (continuous BEV bounding-box coordinates) from video, with a structured CoT decoupling a ==Map Module== (perception) from a Think Module (deduction), trained ==SFT on sim then RFT on real==; **47.46%** avg spatial reasoning (**+3.29%** over base, surpassing grid-map and GPT-4o).

**Reasoning-Traced Training — Decision Matrix**

| Need | Recommendation |
|---|---|
| Verifiable per-step predicate checking | [[2509.25852\|REVER]] (programmatic step verification) |
| Eliminate hallucinated reasoning | [[2604.21396\|VG-CoT]] (visual-evidence grounding) |
| Distill strong-model reasoning into VLA | [[2604.17800\|ReFineVLA]] (teacher-guided fine-tuning) |
| Diagnose causally-disconnected reasoning | [[2604.22074\|CIR/SR-Reasoning]] (CIR + step rewards) |
| Learn when to reason vs act reflexively | [[2506.13757\|AutoVLA]] / [[2505.11917\|OneTwoVLA]] (adaptive depth gating) |

^dm-5

> [!star] Key Papers
> - [[2509.25852|REVER]] — Reinforced embodied planning with verifiable reward; first to RL-train reasoning traces with causality
> - [[2604.21396|VG-CoT]] — Grounded CoT tied to visual evidence; eliminates hallucinated reasoning
> - [[2604.17800|ReFineVLA]] — Teacher-guided reasoning distillation into VLAs
> - [[2604.22074|CIR/SR-Reasoning]] — Outcome rewards alone insufficient; need causally-important step rewards

^key-papers-5

> [!tip] Outcome Rewards Are Not Enough
> CIR/SR's finding is sobering: a VLA trained to maximize task success can develop reasoning traces that *look* correct but are causally disconnected from the final action. Step-level rewards on the *reasoning process* are required for trustworthy reasoning. Cross-reference [[06_WAM#7.3 RL-Driven & Co-Evolving]] for RL-driven WAM co-evolution patterns ([[2603.19370|VAMPO]]) and [[15_Self-Evolving-VLA-WAM#3. Core Mechanisms of Self-Evolution]] for how reasoning-traced training composes with self-evolution loops.

^insight-5

---

## Part C — Trade-offs & Open Problems

*Reasoning quality vs inference latency; what remains unsolved.*

### 6. Reasoning Quality vs Inference Latency

The fundamental trade-off in reasoning-augmented VLAs is that *every* slot from §1 absorbs latency differently — input prompting pays for token generation, latent reasoning hides cost inside a single forward pass, output-head reasoning scales with visual complexity, external search multiplies inference by the rollout count. The 2026 frontier collapsed the previously-strict Pareto frontier: latent reasoning now matches or beats explicit CoT *at answer-only latency*, while runtime alignment verification ([[2510.16281|SEAL]]) and test-time MCTS retain their place when robustness dominates throughput. The recipe choice is no longer "which approach is best" but "which constraint binds at deployment" — latency, interpretability, or recovery from miscalibration.

#### 6.1 Latency-Optimized Recipes

Achieve answer-only or near-base-VLA latency without sacrificing reasoning quality. The 2026 frontier when the bottleneck is *throughput* — real-time control, on-robot deployment, mobile manipulation.

- **[[2604.18486|OneVL]]** — A latent-CoT VLM with ==dual auxiliary decoders== + a ==prefill mechanism==; **88.84 PDM-score** on NAVSIM at **1.0×** base-VLA latency. The cleanest "best of both worlds" result.
- **[[2604.22709|Abstract-CoT]]** — A post-training method giving ==token-free reasoning== via K pre-allocated parallel-processed slots; **up to 12×** fewer reasoning tokens at **1.0-1.1×** base-VLA latency.
- **[[2602.08167|R&B-EnCoRe]]** — A self-supervised VLA treating reasoning as a ==latent variable== refined via ==importance-weighted variational inference (IWAE)==, trained as prior and posterior with ==reasoning dropout== distilling concise traces; cuts reasoning tokens **256.8 → 129.3**, latency **~5s → ~3s/step**, lifts manipulation SR to **80.3%** and OOD SR to **76.9%** (baseline 69.2%).
- **[[2506.07639|Fast-ECoT]]** — An inference-time accelerator for ==Embodied Chain-of-Thought== exploiting its temporal locality: ==caches/reuses high-level reasoning== across timesteps, parallel-generates steps via continuous batching, and asynchronously decouples fast action decoding from slow trace refresh; **7.7×** speedup (716 ms vs 5556 ms/step), **80.0%** LIBERO at no SR loss.
- **[[2506.01953|Fast-in-Slow]]** — A unified dual-system VLA embedding the ==fast System-1 action module== directly inside the final blocks of a ==slow System-2 VLM reasoner== so System 1 inherits pretrained knowledge, run at asynchronous 1:4 frequencies via dual-aware co-training; **69%** RLBench (CogACT **61%**), **21.9-117.7 Hz**, smaller OOD drop than baselines.
- **[[2505.08243|ECoT-Lite]]** — A family of training strategies (==Reasoning Pre-training==, ==Reasoning Dropout==) that supervise embodied reasoning *in training* but skip explicit generation at test time, isolating *why* reasoning helps — it improves representation learning, not expressivity; **89.4%** LIBERO-90, **3×** speedup (3.5+ Hz) matching non-reasoning VLAs.

#### 6.2 Quality-Optimized Recipes

Maximize reasoning robustness when latency budget is generous. The frontier when the bottleneck is *recovery from policy miscalibration* under OOD shift, novel compositions, or safety-critical decisions.

- **[[2509.22643|VLA-Reasoner]]** — A test-time search wrapper with ==online MCTS== + ==world model==; **+19pp** real-world OpenVLA at **3-5×** base-VLA latency for maximally-robust action selection.
- **[[2510.16281|SEAL]]** — A training-free runtime steering framework doing ==Hypothesize→Predict→Verify== for ==CoT-action alignment==; **~1.5-2×** latency (**347 ms/step**) for **+15pp** SR on novel compositions (**53%**) and **+17pp** under viewpoint shifts (**45%**).

#### 6.3 Interpretability-Optimized Recipes

Preserve human-readable reasoning traces alongside actions. The frontier when the bottleneck is *debugging*, multi-stage manipulation, or human-in-the-loop oversight.

- **[[2503.22020|CoT-VLA]]** — A VLA emitting ==output-head visual subgoals==; **+17%** real-world at **1.5-2.5×** base-VLA latency; the subgoal *is* the plan, fully inspectable.
- **[[2508.07917|MolmoAct]]** — An Action Reasoning Model emitting ==depth-aware perception tokens + visual reasoning traces== at **1.5-2.5×** base-VLA latency; **86.6%** LIBERO and **+22.7%** real-world task progression over π0-FAST, visual-trace steering at **75%** SR.

**Reasoning Latency — Decision Matrix**

| Approach | Reasoning Quality | Inference Latency | Best For | Source |
|----------|-------------------|-------------------|----------|--------|
| No reasoning (vanilla VLA) | Low | 1.0× | Latency-critical pick-and-place | π0, OpenVLA |
| Input-prompt CoT | Medium | 2-3× | Prototyping, language-heavy tasks | RT-2 |
| Output-head visual CoT | High | 1.5-2.5× | Multi-stage manipulation, debugging | [[2503.22020\|CoT-VLA]] |
| Latent reasoning ([[2604.22709\|Abstract-CoT]]) | High | 1.0-1.1× | Real-time control, throughput | [[2604.22709\|Abstract-CoT]] |
| Latent reasoning ([[2604.18486\|OneVL]]) | **Highest** | **1.0×** | Real-time + best accuracy | [[2604.18486\|OneVL]] |
| Runtime alignment verification ([[2510.16281\|SEAL]]) | High | ~1.5-2× (K=10, 347ms/step) | CoT-action disagreement under OOD | [[2510.16281\|SEAL]] |
| Test-time search (MCTS) | Highest | 3-5× | Safety-critical, novel tasks | [[2509.22643\|VLA-Reasoner]] |

^dm-6

> [!star] Key Papers
> - [[2604.18486|OneVL]] — Anchors the latency-optimized frontier; latent + dual auxiliary decoders beats explicit CoT at answer-only latency
> - [[2503.22020|CoT-VLA]] — Anchors the interpretability-optimized frontier; visual subgoals are inspectable plans
> - [[2509.22643|VLA-Reasoner]] — Anchors the quality-optimized frontier; MCTS + world model maximally robust at **3-5×** latency
> - [[2510.16281|SEAL]] — Hybrid quality + interpretability; runtime CoT-action alignment verification at moderate latency

^key-papers-6

> [!success] The 2026 Recipe
> If latency matters: ==Latent reasoning + dual-modal auxiliary supervision== ([[2604.18486|OneVL]] pattern). If interpretability matters: ==Output-head visual CoT== ([[2503.22020|CoT-VLA]] pattern). If recovery from miscalibration matters: ==Test-time MCTS== ([[2509.22643|VLA-Reasoner]] pattern). RL-train the reasoning trace with verifiable step rewards ([[2509.25852|REVER]] + CIR/SR). Cross-reference [[06_WAM#6.1 Training-Time Video, Test-Time Speed]] for the analogous training-time-video / test-time-speed efficiency recipe in WAMs ([[2603.16666|Fast-WAM]]) — the same train-rich-deploy-slim principle generalizes.

> [!tip] There Is No Free Reasoning — Only a Latency You Chose to Pay Somewhere
> The 2026 surprise is that the quality-latency frontier is *not* monotone: [[2604.18486|OneVL]] buys top-tier reasoning at 1.0× base latency, collapsing the old "more reasoning = more latency" intuition for the *latent* slot. But the trade-off doesn't vanish — it relocates. Latency-optimized recipes pay at training time (dual-decoder supervision is expensive to learn); quality-optimized recipes ([[2509.22643|VLA-Reasoner]], 3–5×) pay per rollout at test time; interpretability-optimized recipes ([[2503.22020|CoT-VLA]], [[2508.07917|MolmoAct]], 1.5–2.5×) pay a steady inspectability tax. The right question is not "how much reasoning?" but "*where can my deployment afford to pay?*" — throughput-bound robots pay at training, safety-critical robots pay per rollout, human-supervised robots pay for traces. Cross-reference [[07_Latent-World-Models#5. Latent vs Pixel Comparison]] for the structurally identical train-pixel / deploy-latent trade-off in world models.

^insight-6

---

### 7. Open Problems

VLA reasoning sits between "VLM that talks about plans" and "policy that executes them" — the gap is where current methods fail. The five open problems below split along an explicit axis: four are facets of the same *faithfulness* root (does the executed action actually follow from the stated plan?), and one is the orthogonal *modality coverage* gap (most reasoning is vision-only; force/tactile/audio are absent).

- **==Reasoning vs reflex==** — When should the VLA reason, and when act reflexively? "Always reason" is slow; "never reason" is brittle. ==Adaptive reasoning depth== ([[2604.28192|LaST-R1]], [[2506.13757|AutoVLA]], [[2505.11917|OneTwoVLA]]) — RFT-with-CoT-penalty and decision-token gating (§5.5) cut latency — but the gate is learned implicitly from reward, not a principled trigger.
- **==Causality verification at scale==** — ==CIR/SR== ([[2604.22074|CIR/SR-Reasoning]], [[2509.25852|REVER]]) works for narrow predicates (graspability, contact). Scaling causally-important step rewards to general manipulation is an open problem; ground-truth causal structure is rarely annotated.
- **==The CoT faithfulness gap==** — [[2510.16281|SEAL]] documents that reasoning VLAs often generate sensible text plans but produce actions *inconsistent* with them, especially under OOD shifts. [[2510.16281|SEAL]] verifies alignment at runtime, but *why* training fails to enforce it stays open. RL with action-alignment rewards is a natural fix but unproven at VLA scale.
- **==Cross-modal reasoning==** — Most VLA reasoning is vision-centric; reasoning over force, tactile, and audio modalities (relevant for contact-rich tasks) is underexplored. This is the orthogonal frontier to the faithfulness cluster — see [[10_Contact-Rich-and-Tactile-Control#3. Force-Conditioned VLA Architectures]].
- **==Reasoning generalization==** — Does a model that reasons well on [[2510.13626|LIBERO-Plus]] also reason on real-world novel tasks? Fine-grained diagnostics are emerging — [[2606.17639|ERQA-Plus]] decomposes embodied reasoning into ==five categories== via a Generator/Judge/Reviser pipeline, exposing that even strong VLMs collapse on temporal reasoning and path planning — but current benchmarks still reward in-domain CoT, not OOD-transfer CoT.

**VLA Reasoning Failure Modes — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Need adaptive reason-vs-reflex gating | [[2604.28192\|LaST-R1]] (latent) / [[2506.13757\|AutoVLA]] / [[2505.11917\|OneTwoVLA]] (token/reward gating) — works, but gate is reward-learned not principled |
| Need step-wise causal reward beyond narrow predicates | [[2509.25852\|REVER]] / [[2604.22074\|CIR/SR-Reasoning]] (process-level rewards) — works for in-regime only |
| Runtime check that action matches stated plan | [[2510.16281\|SEAL]] (K-candidate VLM critic, training-free) |
| Training-time enforcement of plan-action alignment | Action-aligned RL — unproven at VLA scale; research gap |
| Reasoning over force / tactile / audio | Cross-modal reasoning — research gap; see [[10_Contact-Rich-and-Tactile-Control#3. Force-Conditioned VLA Architectures]] for the contact-modality bridge |
| Diagnose OOD reasoning robustness | [[2606.17639\|ERQA-Plus]] (five-category reasoning taxonomy; temporal reasoning + path planning are hardest) + [[2510.13626\|LIBERO-Plus]] geometric perturbations |

^dm-7

> [!star] Key Papers — Reasoning Failure Frontier
> - [[2510.16281|SEAL]] — Canonical documentation of the *CoT faithfulness gap*: VLAs generate good plans then execute *inconsistent* actions under OOD; the load-bearing evidence that reasoning ≠ faithful execution
> - [[2509.25852|REVER]] — Process-level CIR/SR rewards as the first scalable causal-step training signal; the strongest current attack on the causality-verification problem
> - [[2604.28192|LaST-R1]] — Adaptive reasoning depth via latent state classifiers; the most credible step toward the reflex-vs-reason gate

^key-papers-7

> [!tip] The Faithfulness Gap Is the Common Root
> Four of the five problems above (reasoning vs reflex, causality verification, the [[2510.16281|SEAL]] alignment gap, reasoning generalization) trace to the same root: VLAs can *describe* a plan and *execute* an action, but no current method *enforces* that the action follows from the plan under OOD shift. Process-level rewards ([[2509.25852|REVER]] CIR/SR) and runtime alignment verification ([[2510.16281|SEAL]]) attack the symptom; the deeper fix likely requires action-aligned RL objectives that haven't been demonstrated at VLA scale. Cross-modal reasoning (force, tactile) is the orthogonal frontier. Cross-reference [[07_Latent-World-Models#6. Open Problems]] (the same opacity / latent-pixel alignment problem appearing in pure world-model form) and [[04_VLA#18. Open Problems & Failure Modes]] (VLA-side failure modes where reasoning faithfulness shows up as policy-execution drift).

^insight-7

---

## Quick-Reference Matrix

| Question | Answer |
|----------|--------|
| Need fastest reasoning? | [[2604.18486\|OneVL]] (latent + dual aux) or [[2604.22709\|Abstract-CoT]] (token-free) |
| Need interpretable reasoning? | [[2503.22020\|CoT-VLA]] (visual subgoals) or [[2508.07917\|MolmoAct]] (visual traces) |
| Need most robust reasoning? | [[2509.22643\|VLA-Reasoner]] (MCTS) or [[2508.12211\|VLAPS]] (model-based search) |
| Need runtime alignment verification (CoT-faithful actions)? | [[2510.16281\|SEAL]] (training-free, K-candidate verification via VLM critic) |
| Need RL-trained reasoning? | [[2509.25852\|REVER]], [[2604.17800\|ReFineVLA]], or [[2604.28192\|LaST-R1]] |
| Need physics reasoning? | [[2503.15558\|Cosmos-Reason1]] — see [[08_Physics-Aware-Embodied-AI#5. Physics-Aware Reasoning]] |
| Need driving reasoning? | [[2604.18486\|OneVL]] (88.84 PDM-score on NAVSIM) |
| Beware: outcome rewards alone? | [[2604.22074\|CIR/SR-Reasoning]] — use step rewards, not just outcome rewards |
| Need latent + diffusion? | [[2509.25681\|dVLA]] |

---

## Cross-References

- [[01_Embodied-AI-101]] — Embodied AI basics; reasoning is one of the four learning-strategy axes
- [[04_VLA]] — VLA deep-dive; §4 covers the broader Reasoning & Planning landscape and feeds into this note
- [[06_WAM]] — WAM deep-dive; §5 VLM-Integrated WAMs cover the world-model side of reasoning-augmented planning
- [[07_Latent-World-Models]] — §4 latent reasoning for embodied AI; complements this note's latent slot
- [[15_Self-Evolving-VLA-WAM]] — Self-evolution; reasoning enables self-critique and proactive correction
- [[08_Physics-Aware-Embodied-AI]] — Physics priors as the substrate for [[2503.15558|Cosmos-Reason1]] and physical latent reasoning ([[2604.28192|LaST-R1]])
- [[13_Egocentric-Pretraining-and-Human-Video]] — Egocentric pretraining deep-dive
- [[10_Contact-Rich-and-Tactile-Control]] — Force/tactile policies deep-dive; reasoning over multi-sensor context
- [[02_Dataset-Benchmark-Environment]] — Reasoning benchmarks ([[2507.10548|EmbRACE-3K]], [[2505.05456|SITE]])

---

*See [[04_VLA]] for the full VLA design space, [[07_Latent-World-Models]] for the broader latent-prediction landscape, or [[08_Physics-Aware-Embodied-AI]] for physics-aware reasoning.*
