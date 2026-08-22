---
title: "Robot Memory: Spatial & Temporal Persistence — Deep Dive"
tags:
  - robot-memory
  - episodic-memory
  - spatial-memory
  - long-horizon
aliases:
  - "Robot Memory"
  - "Spatial and Temporal Memory"
---

# Robot Memory: Spatial & Temporal Persistence — Deep Dive

> [!abstract] Overview
> A policy that only sees the current frame cannot count, cannot recall an occluded object, and cannot tell "I already checked here" from "I never looked." This deep-dive maps how the field gives robots a past: episodic and retrieval memory that stores and recalls specific experiences, object-permanence and keyframe-history policies that track what left the frame, persistent spatial memory and cognitive maps that survive a full mission, progress-aware and hindsight control that reasons about *when* in a task it is, memory-augmented LLM/VLM reasoning, and memory as the substrate for self-evolution after deployment. A short final section points at the adjacent — and larger — literature on memory inside *generative* world models, where the problem is rollout visual consistency rather than robot decision-making, and at the benchmarks built specifically to test non-Markovian policies.

## Evolution Graph

```text
1. Episodic & Retrieval Memory   (how the past gets stored and pulled back on demand)
· working & episodic memory (navigation)
                      +scene-graph palace       +long-term         +curiosity-driven memory
                                                bench
╔════════════════╗    ┌────────────────────┐    ┌─────────────┐    ┌───────────────────────────────┐
║ MemoNav (2024) ║───►│ Mind-Palace (2025) │───►│ LMEE (2026) │───►│ Remember-to-be-Curious (2026) │
╚════════════════╝    └────────────────────┘    └─────────────┘    └───────────────────────────────┘

· retrieval & dynamic memory (navigation)
                           +purge moved objects
┌─────────────────────┐    ╔════════════════╗
│ Embodied-RAG (2024) │───►║ DynaMem (2024) ║
└─────────────────────┘    ╚════════════════╝
                                  │
                                  │    +world-model memory
                                  │    ┌───────────────┐
                                  ├───►│ Memoir (2025) │
                                  │    └───────────────┘
                                  │
                                  │    +3DGS memory
                                  │    ┌──────────────┐
                                  └───►│ GSMem (2026) │
                                       └──────────────┘

2. Object-Permanence & Keyframe-History   (what a policy believes about what it can't see)
· object permanence & identity
                                         +3D Gaussian identity
╔═══════════════════════════════════╗    ┌─────────────────────────────────────────┐
║ Out-of-Sight-Still-in-Mind (2023) ║───►│ Persistent-Object-Gaussian-Splat (2025) │
╚═══════════════════════════════════╝    └─────────────────────────────────────────┘
                                                              │
                                                              │    +role-indexed         +spatio-temporal
                                                              │    tokenization          memory
                                                              │    ┌────────────────┐    ┌────────────────────┐
                                                              └───►│ POT-VLA (2026) │───►│ BridgeVLA++ (2026) │
                                                                   └────────────────┘    └────────────────────┘

· keyframe-history compression
                      +VLM salient      +event-keyframe      +episode-local
                      keyframes         bank                 latent belief
╔════════════════╗    ┌────────────┐    ┌───────────────┐    ┌──────────────┐
║ ProDapt (2025) ║───►│ BPP (2026) │───►│ KEMO (2026)   │───►│ TFP (2026)   │
╚════════════════╝    └────────────┘    └───────────────┘    └──────────────┘

3. Persistent Spatial Memory & Cognitive Maps   (durable representations of space)
· scene-graph & map representation
                      +memory              +scene graph           +persistent 3D
                      snapshots                                   memory layer
╔════════════════╗    ┌───────────────┐    ┌─────────────────┐    ┌────────────────────┐
║ MultiON (2020) ║───►│ 3D-Mem (2024) │───►│ GraphEQA (2024) │───►│ HoloAgent-0 (2026) │
╚════════════════╝    └───────────────┘    └─────────────────┘    └────────────────────┘

· memory baked into the VLA backbone
                     +declarative               +recurrent         +dual latent
                     scene+episodic memory      memory tokens      memory condenser
╔═══════════════╗    ┌─────────────────────┐    ┌─────────────┐    ┌──────────────────┐
║ HAMLET (2025) ║───►│ EchoVLA (2025)      │───►│ μVLA (2026) │───►│ LaMem-VLA (2026) │
╚═══════════════╝    └─────────────────────┘    └─────────────┘    └──────────────────┘

4. Progress-Aware & Hindsight Control   (temporal self-awareness during execution)
· phase-and-hindsight reasoning
                       +hindsight-insight-foresight      +error-recovery rewind        +revisable
                                                                                       execution state
╔═════════════════╗    ┌────────────────────────────┐    ┌────────────────────────┐    ┌─────────────────┐
║ Long-VLA (2025) ║───►│ HiF-VLA (2025)             │───►│ See-Plan-Rewind (2026) │───►│ ChainVLA (2026) │
╚═════════════════╝    └────────────────────────────┘    └────────────────────────┘    └─────────────────┘

5. Memory-Augmented Reasoning & Planning   (LLM/VLM reasoning grounded in persistent stores)
· agentic memory-grounded reasoning
                                 +cognitive map       +four parallel           +semantic 3D Gaussian
                                                      memory stores            memory
╔═══════════════════════════╗    ┌───────────────┐    ┌───────────────────┐    ┌──────────────────────┐
║ Memory-Centric-EQA (2025) ║───►│ CLiViS (2025) │───►│ RoboMemory (2025) │───►│ GaussExplorer (2026) │
╚═══════════════════════════╝    └───────────────┘    └───────────────────┘    └──────────────────────┘

6. Memory-Driven Self-Evolution   (memory as the substrate for lifelong improvement)
· hierarchical & skill-library memory
                      +hierarchical
                      incremental memory
╔════════════════╗    ┌───────────────────┐
║ Voyager (2023) ║───►│ FrankenBot (2025) │
╚════════════════╝    └───────────────────┘
                                │
                                │    +recursive summarized nodes                +value-guided
                                │                                               elite/transition banks
                                │    ┌─────────────────────────────────────┐    ┌────────────────────┐
                                └───►│ Hierarchical-Episodic-Memory (2026) │───►│ OnEvoMemory (2026) │
                                     └─────────────────────────────────────┘    └────────────────────┘

7. Generative World-Model Memory — Landmarks   (a different problem: rollout visual consistency)
· memory-consistency mechanisms in video world models
                       +DINO-Map 3D memory
╔═════════════════╗    ┌──────────────────────────────────┐
║ WorldMem (2025) ║───►│ 3D-Persistent-Embodied-WM (2025) │
╚═════════════════╝    └──────────────────────────────────┘
                                        │
                                        │    +three-tier spatial memory                +rolling-window
                                        │                                              memory compression
                                        │    ┌────────────────────────────────────┐    ┌──────────────────┐
                                        └───►│ Long-Term-Spatial-Memory-WM (2025) │───►│ RELIC (2025)     │
                                             └────────────────────────────────────┘    └──────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

**Read the arrows as axis-and-date ordering, not a confirmed citation chain.** None of the papers in these threads cite each other by ID in their own KH summaries — checked directly, not assumed. The delta above each box names that paper's own contribution, not a verified "built on the predecessor" claim; several of these clusters are more likely independent, convergent developments than a real lineage (this file's own §1 tip already calls one "reinvented three times," and §4's calls its cluster "converged independently... within a five-month window"). The one edge with an actual outside source — [[13_Navigation-and-Mobile-Manipulation|13_Navigation]]'s own [[2409.18313|Embodied-RAG]]→[[2411.04999|DynaMem]] fork, reused here rather than re-derived — was re-checked for this note and also has no confirmed citation between the two; treat it the same as the rest.

Seven lanes, one per mechanism family, plus an eighth (Memory Benchmarks) that has no papers of its own and stays off the diagram. Episodic & retrieval memory runs two navigation threads — [[2402.19161|MemoNav]]'s working-memory line reaching [[2605.22814|Remember-to-be-Curious]], and [[2409.18313|Embodied-RAG]]'s retrieval line forking at [[2411.04999|DynaMem]] into [[2510.08553|Memoir]] and [[2603.19137|GSMem]]. Object-permanence and keyframe-history split into an identity-tracking line ([[2309.15278|Out-of-Sight-Still-in-Mind]] to [[2608.05042|BridgeVLA++]]) and a keyframe-compression line ([[2503.00193|ProDapt]] to [[2607.08283|TFP]]). Persistent spatial memory carries a scene-graph thread ([[2012.03912|MultiON]] to [[2606.23565|HoloAgent-0]]) alongside a thread of memory baked directly into the VLA backbone ([[2510.00695|HAMLET]] to [[2607.07608|LaMem-VLA]]). Progress-aware control, memory-augmented reasoning, self-evolution, and the generative-WM landmarks each run a single thread — the last one is deliberately light: [[06_WAM]] carries the other ~30 memory-in-video-diffusion papers this file does not duplicate.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2024 | [[2402.19161\|MemoNav]] | Episodic · Nav Working | A biologically-inspired working memory (STM + LTM + dynamically-built WM) with a selective forgetting module |
| 2025 | [[2507.12846\|Mind-Palace]] | Episodic · Nav Working | A hierarchical scene-graph 'Robotic Mind Palace' over multi-episode history, with an LLM interleaving recall and exploration |
| 2026 | [[2601.10744\|LMEE]] | Episodic · Nav Working | A Long-term Memory Embodied Exploration paradigm + LMEE-Bench unifying multi-goal nav with memory-based QA |
| 2026 | [[2605.22814\|Remember-to-be-Curious]] | Episodic · Nav Working | An explorer pairing a persistent 3D Gaussian Splatting forward model with a long-context transformer holding episodic memory |
| 2024 | [[2409.18313\|Embodied-RAG]] | Episodic · Nav Retrieval | A system building a semantic forest of hierarchical robot-snapshot clusters, LLM-summarized at each level, for nav and Q&A |
| 2024 | [[2411.04999\|DynaMem]] | Episodic · Nav Retrieval | A dynamic 3D voxel memory that ray-casts to detect and purge moved or removed objects from the scene |
| 2025 | [[2510.08553\|Memoir]] | Episodic · Nav Retrieval | A memory-persistent VLN agent using a language-conditioned world model to imagine future states as retrieval queries |
| 2026 | [[2603.19137\|GSMem]] | Episodic · Nav Retrieval | A persistent 3D Gaussian Splatting spatial memory re-rendering explored areas for VLM re-observation |
| 2023 | [[2309.15278\|Out-of-Sight-Still-in-Mind]] | Permanence · Identity | A DOOM/LOOM object-oriented memory hallucinating point clouds or propagating latents for occluded objects |
| 2025 | [[2503.05189\|Persistent-Object-Gaussian-Splat]] | Permanence · Identity | A persistent object representation (POGS) embedding grouping + CLIP + DINO features into 3D Gaussians to keep identity through occlusion |
| 2026 | [[2607.18016\|POT-VLA]] | Permanence · Identity | A closed-loop humanoid VLA introducing Persistent Object Tokenization, a role-indexed 3D object memory in the action-head |
| 2026 | [[2608.05042\|BridgeVLA++]] | Permanence · Identity | Extends BridgeVLA's 2D-heatmap pre-training with a unified spatio-temporal memory for occlusion-robust localization |
| 2025 | [[2503.00193\|ProDapt]] | Permanence · Keyframe | A proprioceptive policy conditioning a diffusion model on contact 'keypoints' selected by spatial distance and normal force |
| 2026 | [[2602.15010\|BPP]] | Permanence · Keyframe | A Big Picture Policies method conditioning on VLM-detected salient keyframes at 1 Hz with latency masking |
| 2026 | [[2606.23589\|KEMO]] | Permanence · Keyframe | A lightweight plug-in memory augmenting a VLA with a temporally-ordered bank of event keyframes |
| 2026 | [[2607.08283\|TFP]] | Permanence · Keyframe | A memory-fusion policy augmenting a chunked VLA with an episode-local latent belief from Liquid Time-Constant networks |
| 2020 | [[2012.03912\|MultiON]] | Spatial Mem · Scene-Graph | A benchmark of map-memory for sequential multi-object navigation |
| 2024 | [[2411.17735\|3D-Mem]] | Spatial Mem · Scene-Graph | A scene memory representing space as multi-view Memory Snapshots (explored) plus Frontier Snapshots (unexplored) |
| 2024 | [[2412.14480\|GraphEQA]] | Spatial Mem · Scene-Graph | Builds online 3D metric-semantic scene graphs enriched with LLM room labels and semantically-connected frontier nodes |
| 2026 | [[2606.23565\|HoloAgent-0]] | Spatial Mem · Scene-Graph | A unified embodied-agent framework grounding LLM planning in a persistent 3D Spatial Memory Layer |
| 2025 | [[2510.00695\|HAMLET]] | Spatial Mem · VLA-Backbone | A History-Aware Memory with Learned Tokens where per-timestep moment tokens compress history into a fine-tunable module |
| 2025 | [[2511.18112\|EchoVLA]] | Spatial Mem · VLA-Backbone | A biologically-inspired declarative memory: persistent voxelized Scene Memory plus time-indexed Episodic Memory |
| 2026 | [[2606.12497\|μVLA]] | Spatial Mem · VLA-Backbone | A minimal recurrent-memory VLA inserting learnable memory tokens into an OpenVLA-OFT backbone via TBPTT |
| 2026 | [[2607.07608\|LaMem-VLA]] | Spatial Mem · VLA-Backbone | A dual latent memory VLA weaving a short-term visual vault and long-term action-hidden-state vault into the VLM sequence |
| 2025 | [[2508.19958\|Long-VLA]] | Progress-Hindsight | An end-to-end long-horizon VLA that decomposes trajectories into moving vs interaction phases via a phase identifier |
| 2025 | [[2512.09928\|HiF-VLA]] | Progress-Hindsight | A Hindsight-Insight-Foresight bidirectional temporal reasoning over compact codec motion vectors |
| 2026 | [[2603.09292\|See-Plan-Rewind]] | Progress-Hindsight | A See-Plan-Rewind cycle that decomposes tasks into spatially-grounded 2D subgoals with explicit error-recovery rewind |
| 2026 | [[2604.17880\|ST-π]] | Progress-Hindsight | A Spatiotemporal VLM that decomposes tasks into causally-ordered chunk-level prompts plus a Spatiotemporal Action Expert |
| 2026 | [[2606.17463\|WeaveLA]] | Progress-Hindsight | An event-driven latent memory weaving interface bolted onto a frozen VLA that writes compressed task state at sub-goals |
| 2026 | [[2608.02326\|ChainVLA]] | Progress-Hindsight | A unified, revisable execution state passed across successive VLA queries so task evidence persists across replanning |
| 2025 | [[2505.13948\|Memory-Centric-EQA]] | Reasoning Mem | A memory-centric Embodied-QA framework centralizing a memory store to guide planner, stopping, and answering modules |
| 2025 | [[2506.17629\|CLiViS]] | Reasoning Mem | A training-free embodied-visual-reasoning framework where an LLM and VLM jointly update a Cognitive Map plus Evidence Memory |
| 2025 | [[2508.01415\|RoboMemory]] | Reasoning Mem | A brain-inspired multi-memory agentic framework unifying four parallel stores over a LoRA-finetuned VLA |
| 2026 | [[2601.13132\|GaussExplorer]] | Reasoning Mem | An embodied exploration and reasoning framework over semantic 3D Gaussian Splatting queried by an LLM's evidence categories |
| 2026 | [[2606.28592\|E2-CARE]] | Reasoning Mem | Unifies environment, robot embodiment, and humans in one 3D dynamic scene graph an LLM reasons over for safety constraints |
| 2026 | [[2606.29786\|OP3DSG]] | Reasoning Mem | Builds a unified open-vocab 3D scene graph via knowledge-guided part detection and geometry-anchored multi-agent reasoning |
| 2026 | [[2607.14252\|MEMORA]] | Reasoning Mem | An Embodied Action Memory system built from egocentric video via four typed memory stores with online revision |
| 2026 | [[2608.04765\|Language-Memory VLA]] | Reasoning Mem | A hierarchical VLA whose high-level branch emits recursive language memory conditioning a low-level action branch |
| 2023 | [[2305.16291\|Voyager]] | Self-Evolution | The foundational open-ended embodied agent: frozen GPT-4 drives an automatic curriculum plus a persistent skill library |
| 2025 | [[2506.21627\|FrankenBot]] | Self-Evolution | A brain-morphic VLM-orchestration agent whose Hierarchical Incremental Memory enables cross-task skill reuse |
| 2026 | [[2604.11306\|Hierarchical-Episodic-Memory]] | Self-Evolution | An H²-Emv system building a hierarchical episodic memory of recursively summarized nodes with decay-based forgetting |
| 2026 | [[2608.08749\|OnEvoMemory]] | Self-Evolution | A value-guided hierarchical memory (elite/transition/short-term banks) bolted onto a frozen VLA via gated cross-attention |
| 2025 | [[2504.12369\|WorldMem]] | Generative WM Mem | A token-level memory bank with state-aware memory attention letting a diffusion transformer persist events over hundreds of frames |
| 2025 | [[2505.05495\|3D-Persistent-Embodied-WM]] | Generative WM Mem | An action-guided RGB-D video diffusion model with an explicit DINO-Map 3D memory injected via cross-attention experts |
| 2025 | [[2506.05284\|Long-Term-Spatial-Memory-WM]] | Generative WM Mem | A memory-augmented video WM with three tiers, including a geometry-grounded 3D point-cloud spatial memory via TSDF fusion |
| 2025 | [[2512.04040\|RELIC]] | Generative WM Mem | An interactive video world model distilling a bidirectional diffusion teacher into a real-time causal autoregressive student |
| 2026 | [[2602.08025\|MIND-Bench]] | Generative WM Mem | The first open-domain closed-loop benchmark isolating memory consistency and action control in generative world models |
| 2026 | [[2603.25716\|HyDRA]] | Generative WM Mem | A Hybrid Memory paradigm preserving both static-background consistency and dynamic-subject identity across re-entry |
| 2026 | [[2605.18813\|CoME]] | Generative WM Mem | Composition of Memory Experts for diffusion world models, fusing short/long/spatial-term memory experts via contrastive PoCE |
| 2026 | [[2606.09803\|Echo-Memory]] | Generative WM Mem | A controlled study fixing the video DiT backbone to sweep four memory families under a replay/in-domain/open-domain protocol |

## Part A — Core Memory Mechanisms

*What gets stored, and how it gets pulled back.*

### 1. Episodic & Retrieval Memory

A policy without episodic memory cannot answer "have I been here before?" or "what did I already try?" — every decision is made from the current frame alone, so any task that spans more than a glance collapses into repeated mistakes. Episodic and retrieval memory fixes this by storing a compact, queryable record of past experience — snapshots, keyframes, gist tokens, event boundaries — and retrieving the task-relevant slice on demand, rather than replaying the full history through the context window.

The three sub-sections below split on *domain*, not mechanism, because the same retrieval ideas (compression, forgetting, hierarchical stores) recur in each — navigation's episodic memory, navigation's dynamic/retrieval memory, and manipulation's episodic memory each independently arrived at similar structures under different names. That convergence is itself the finding: episodic memory for embodied agents is not domain-specific machinery, it is a design pattern reinvented per community.

#### 1.1 Working & Episodic Memory (Navigation)

Biologically-inspired short-term/long-term stores and hierarchical scene-graph "palaces" over multi-episode exploration history.

- **[[2608.10886|GESTO]]** — A persistent ==4D scene graph== coupled to a ==two-level activity hierarchy== (interactions grouped by an LLM into goal-driven events), built fully automatically via VLM extraction + grounding + refinement; **0.71/0.75/0.70** text/binary/time on EGG, far above the same ungrounded pipeline (**0.33/0.29/0.50**) — the event hierarchy carries temporal reasoning.

- **[[2608.01456|MeMento]]** — A ==preference-conditioned multimodal memory compressor== using a ==Perceiver-style module== with learned queries to distil relevant evidence from long histories into a fixed token budget, paired with the new **DunphyBench** benchmark; **+15.74%** accuracy at **-85.38%** memory vs baselines, best-VLM still trails human (**58.3%** vs **83.3%**).

- **[[2607.01043|DART-VLN]]** — A training-free test-time controller for discrete VLN pairing ==memory-slot reweighting== (recency, visit count, novelty) with an ==anti-loop next-hop penalty== on action scores, leaving the frozen backbone untouched; runtime cut **937.99s→552.27s** on R2R val-unseen with SPL **64→66** — forgetting and loop-suppression as inference-time knobs, no retraining.

- **[[2402.19161|MemoNav]]** — A biologically-inspired ==working memory== (STM + LTM + dynamically-built WM) with a ==selective forgetting== module that prunes low-attention nodes; **+7.9–8.5%** SR/PR over VGM on multi-goal Gibson/MP3D tasks, with aggressive forgetting helping most on long-horizon goals — forgetting as an active navigation skill.

- **[[2507.12846|Mind-Palace]]** — A ==hierarchical scene-graph== "Robotic Mind Palace" over multi-episode history, with an LLM interleaving memory recall and active exploration via Value-of-Information early stopping; **+12–28%** answer correctness and **77%** fewer retrieved images on long-term EQA, on a legged robot over a **1,000 m²** office — multi-episodic memory for embodied Q&A.

- **[[2605.22814|Remember-to-be-Curious]]** — An explorer pairing a persistent online ==3D Gaussian Splatting== forward model (curiosity reward from prediction error) with a ==long-context transformer== whose ==global linear-attention memory== holds episodic context, trained map-free via ==PPO== on RGB alone; beat active-mapping baselines on 3D scene completeness, zero-shot to AI-generated worlds.

- **[[2601.10744|LMEE]]** — A ==Long-term Memory Embodied Exploration== paradigm + LMEE-Bench unifying multi-goal nav with memory-based QA, where ==MemoryExplorer== (Qwen2.5-VL-7B, RL-tuned with a multi-task reward) actively recalls episodic memory; **23.53** SR / **43.62** MLLM-Score on LMEE-Bench, **46.40** SR on GOAT-Bench, real X3 transfer — active memory for exploration.

- **[[2111.09793|Robotic-Interestingness]]** — An unsupervised online-learning method for "interestingness" via a ==4-D visual memory== with ==FFT translation-invariant reading== that writes novel features and loses interest in repetition; **69 FPS**, **+18.9–31.9%** from online learning, beating unsupervised + weakly-supervised baselines — a reward-free novelty signal for exploration.

#### 1.2 Retrieval-Augmented & Dynamic Memory (Navigation)

Memory that changes shape as the world does — purging moved objects, re-ranking by recency, or persisting a 3D Gaussian scene that can be re-rendered for a fresh VLM look.

- **[[2608.19059|LT-Mem]]** — A multi-session Tri-Memory (Live/Delta/Meta) framework: ==five-evidence cross-session re-identification== + a ==volatility-aware Bayesian update policy== (overwrite/hold/multi-hypothesis) logs MOVE/APPEAR/DISAPPEAR events across revisits; **0.910** Event F1 (best baseline **0.790**) at order-of-magnitude lower token cost, w/o Re-ID collapses to **0.140**.

- **[[2608.10449|PBD-AG]]** — A ==baseline-delta graph== freezes an immutable baseline via cross-batch consensus, then appends typed audit events for moved/removed objects, with ==visibility-gated existence log-odds== admitting negative evidence only when provably observable; **0.833** dynamic IDF1, **zero** identity switches.

- **[[2607.04057|PreSIST]]** — Proactively predicts how long an object will remain via instance-level ==survival priors== feeding a ==probabilistic persistence filter==; ==PreSIST-Lang== infers ==persistence quantiles== zero-shot from a VLM/LLM, ==PreSIST-Vis== distills this to **~0.04s**/query, improving long-term relocalization — proactive beats reactive re-perception.

- **[[2606.30404|HUMEMBR]]** — A predictive-navigation memory pairing ==face + Keypoint-Promptable-ReID clustering== for persistent multi-day human identity with a ==retrieval-augmented LLM== over five structured query functions, driving routine-conditioned navigation; **75.41%** PersonEQA (**-83%** tokens), **90-100%** real-robot SR on a Spot.

- **[[2606.28720|CubifyGS]]** — An object-centric ==3D Gaussian Splatting== map treating rearranged objects as reusable assets in a ==global asset library==, using ==ray-casted occupancy== to detect vanishing objects and ==semantic-aware asset retrieval== instead of gradient re-optimization; **+35.83%** PSNR, **40×** faster than continuous-training dynamic SLAM.

- **[[2606.25206|RAVEN]]** — A training-free ==visuo-spatio-temporal memory== storing compact ==visual embeddings== (pose + timestamp) in a ==vector database==, queried by a VLM agent via text-/time-/position-based ==retrieval tools== to bypass captioning; widened the gap over caption memory to **30%** on hard queries at **>250×** compression, **97.1%** real Go1 SR — embeddings over captions.

- **[[2603.19137|GSMem]]** — A persistent ==3D Gaussian Splatting spatial memory== re-rendering explored areas for VLM re-observation, via ==multi-level retrieval-rendering== (object scene graphs + an optimization-free 3D language field) and hybrid semantic-geometric exploration; **67.2%** SR / **46.9%** SPL on GOAT-Bench, SOTA on A-EQA — spatial recollection over object/view-based memory.

- **[[2602.00551|APEX-Aerial]]** — A ==decoupled memory-based explorer== for aerial object-goal nav: ==dynamic 3D grid maps== (Attraction / Exploration / Obstacle) give persistent spatial-semantic memory while an ==asynchronous parallel== framework decouples VLM inference from RL control; **+4.2%** SR / **+2.8%** SPL on UAV-ON at **0.97 s** latency — async dynamic memory for aerial search.

- **[[2506.15096|DyNaVLM]]** — A zero-shot VLN system giving a ==VLM== a ==dynamic continuous action space== (spatially-sampled, safety-filtered targets from RGB-D) and a ==self-refining graph memory== of object instances + topological relations built online; **45.0%** SR on ObjectNav and best-among-VLM **25.5%** SR on GOAT-Bench, real Go2 deployment — graph memory that refines itself.

- **[[2409.18313|Embodied-RAG]]** — A system building a ==semantic forest== (hierarchical clusters of robot snapshots with hybrid spatial+semantic distance, LLM-summarized at each level) for navigation and Q&A; outperformed Naive/Graph/Light-RAG on Find and Explain queries and built memory for a 1-km environment (3,353 nodes) **7.38× faster** than GraphRAG — RAG as embodied spatial memory.

- **[[2511.14004|STAR-Memory-Action]]** — An LLM policy unifying ==memory retrieval (search in time)== over a non-parametric timestamped store with ==embodied actions (search in space)== in one decision loop; **0.67** vs **0.56** SR over a temporal-retrieval-only baseline on Interactive Object Search, transferred to a physical Tiago robot — searching memory and the world in a single loop.

- **[[2510.08553|Memoir]]** — A memory-persistent VLN agent using a ==language-conditioned world model== to imagine future states as ==retrieval queries== over a ==Hybrid Viewpoint-Level Memory== of observations and behaviors on a persistent graph; **+5.4%** SPL on unseen IR2R (73.3% vs 67.9%) at an **8.3× training speedup** and **74%** less inference memory — imagination-guided experience recall.

- **[[2411.04999|DynaMem]]** — A dynamic ==3D voxel memory== that ray-casts to detect and purge moved/removed objects, with two-stage VLM-feature + mLLM-QA querying that reports "not found"; **70%** pick-and-drop SR on non-stationary objects (**2×** over static baselines), cutting localization failures **53.3% → 6.7%** — dynamic memory for open-world mobile manipulation.

#### 1.3 Episodic & Compression Memory for Manipulation

The manipulation-side answer to the same problem, plus the robot-control world-action-models that gained a memory module rather than a scene graph: compressed action histories, gist tokens, hybrid memory banks, and event-boundary anchors that let a policy disambiguate two visually-identical moments that demand different actions.

- **[[2607.06678|NativeMEM]]** — A ==Native Memory Compression== scheme repurposing a pretrained VLA's own vision encoder to compress each historical frame-view into one action-relevant token, via a ==two-stage== tokenizer-then-VLA finetune pipeline; **84.0%** sim / **98.7%** real long-horizon SR, **5,000**-frame histories under real-time (**<100 ms**) latency.

- **[[2606.30318|Chronos]]** — Treats the full observation history as an intrinsic ==selective state-space model (Mamba)== latent, refined by a ==physics-informed second-order Schrödinger-inspired action bridge== that predicts ==acceleration fields== via a ==quartic bell noise schedule==; RMBench **73.6%** avg SR (**+62.4pp** over π0.5), ALOHA insertion **90%** vs diffusion **66%**.

- **[[2606.29774|ACM]]** — An ==Analytic Concept-centric Memory== framework organizing experience around structured object concepts (parts, templates, affordances, transitions, skills) with ==manipulation-aware retrieval== + precondition/effect checking; **70%** RMBench SR (vs memory-augmented VLA baselines' 28-53%), **84%** real memory tasks at **98%** retrieval accuracy.

- **[[2606.25136|Long-Horizon]]** — HALO, an attention-based visuomotor policy distilling ==VLM priors== via a co-trained ==Video Question-Answering== objective to guide ==top-k sparse-attention== memory retrieval, suppressing spurious historical correlations; **41%** sim / **55%** real long-horizon SR (vs Standard Transformer's 22%/36%), cutting drift (JSD 0.07→0.06).

- **[[2606.21188|CAMP]]** — A Compressed Action Memory Policy learning a recurrent ==behavioral memory== by self-supervised reconstruction of past actions, compressing them via ==DCT low-frequency coefficients== + a Vector Quantizer, fused into a diffusion policy; **94%** Push-T-Multi-Goals (vs memoryless DP's 56%), **64.3%** on 3D Memory-Manip-Bench, 7/10 real where memoryless baselines score 0.

- **[[2606.20562|MemoryWAM]]** — A World Action Model with a hybrid ==Mixture-of-Transformers== memory: a sliding-window short-term store, persistent ==event-boundary anchor frames==, and ==gist tokens== (8/frame, 15× compression) for long-range history; **83.0%** RMBench (vs full-history LingBot-VA's 78.2%, FastWAM's 5.9%), 18/20 real Shell-Game at full-attention SR with lower latency/GPU memory.

- **[[2604.15814|Continual-Hand-Eye-Calibration]]** — A ==Spatial-Aware Replay Strategy== (hybrid-distance ==Poisson disk sampling== + density-based replacement) paired with ==Structure-Preserving Dual Distillation== decomposing localization knowledge into coarse topological + fine metric components; **98.4%** accuracy / **1.6%** forgetting rate on a robotic-manipulation dataset.

- **[[2509.01657|IWR]]** — Reframes few-shot-IL data retrieval as ==importance sampling==, replacing the L2-nearest-neighbor rule (shown equivalent to a degenerate zero-bandwidth KDE) with ==Gaussian KDE== ratios of target-vs-prior latent densities; **+4.4–5.8%** over Behavior/Flow Retrieval and SAILOR on Robomimic/LIBERO-10, **+30%** real Bridge V2 long-horizon SR.

- **[[2510.20328|MemER]]** — A hierarchical ==VLM keyframe-nomination== high-level policy + generalist low-level policy with ==single-linkage-clustering experience retrieval==; **59/60** object retrievals and 1 wrong scoop on long-horizon tasks, on par with human-provided subtasks, at ~1 Hz/~2 Hz.

- **[[2603.24576|Chameleon]]** — A human-episodic-memory-inspired policy with ==spatiotemporal anchors== + ==multi-timescale episodic states== + a ==HoloHead imagination objective== for goal-directed retrieval; **100.0%** episodic-recall DSR, **73.5%** spatial-tracking, **72.2%** sequential; pattern separation over aliased states.

- **[[2603.18494|MemoAct]]** — An ==Atkinson-Shiffrin-inspired hierarchical memory== policy pairing a lossless ==Short-Term Memory Bank== with a compressed ==Long-Term Memory Bank== via a consolidation module, decoded by conditional diffusion; **96.5%** on its MemoryRTBench vs MVMP's 72% (ACT 4.5%, DP 3%), the plug-and-play module lifting DP3 **26→76.5%**.

- **[[2501.18564|SAM2Act]]** — A multi-view ==SAM2-encoder== transformer with cascaded upsampling, extended by ==SAM2Act+=='s explicit ==memory bank + attention==; **86.8%** RLBench and **94.3%** on the non-Markovian MemoryBench, smallest **4.3%** Colosseum perturbation drop.

- **[[2606.10363|HiMem-WAM]]** — A Hierarchical Memory-Gated World-Action Model combining ==hierarchical latent action== learning with a boundary-aware memory-gated module that writes compact task states at skill transitions, no test-time video gen; **97.7%** LIBERO, **76.0%** LIBERO-Plus, **26.3%** RMBench memory tasks (vs ACT **10.8%**), +**25.0%** real Hard tasks.

- **[[2606.27677|DiM-WAM]]** — Adds ==Diverse Historical Event Memory== (K parallel bounded memory banks with ==novelty-aware compression== + ==mass-weighted fusion== + ==task-progress-aware auxiliary loss==) to a joint video-action WAM for long-horizon temporal disambiguation; RMBench **34.8%→69.8%** full-task SR over a LingBot-VA baseline, real Franka **52.5%→90.0%**.

- **[[2508.19236|MemoryVLA]]** — A ==Perceptual-Cognitive Memory Bank (PCMB)== dual-memory VLA: low-level perceptual details (recent F/T, contact events) + high-level cognitive semantics (task progress); **+26pp** over [[2503.22020|CogACT]] on real-world long-horizon temporal tasks (**83%**) at only **+3.6%** latency, **+0.8 GB** GPU; not force-specialized, but maps cleanly onto force history.

- **[[2104.10218|Episodic-Memory-Manipulation]]** — An episodic-memory framework that decomposes the work cell into modular ==finite-state-machine elements== and synthesizes an Application State Machine from a *single* demonstration; built-in ==exception handling== lets the robot detect novel states and request human guidance — generalizing task logic beyond fixed coordinates.

- **[[2606.12372|UniIntervene]]** — An agentic real-world ==RL== method formulating intervention as an internal ==value-risk== decision: a temporal value-risk critic detects unproductive exploration from action-conditioned value dynamics and a memory-guided ==goal-conditioned recovery== policy retrieves high-value states; **88%** success, **57%** less human intervention, **+8.6%** over HiL-SERL.

- **[[2605.14810|CaMeRL]]** — A collision-aware + memory-enhanced UAV-navigation method: a ==VAE== extracts safety-relevant latents from depth (supervised by collision-aware depth maps) and an ==LSTM== integrates temporal context for partial observability, trained with PPO; **0.77** success in ultra-small-obstacle vs MAVRL's **0.29**, real dense-forest flight at **1.4 m/s**.

- **[[2505.13696|ESWM]]** — An ==Episodic Spatial World Model== meta-trained to infer missing components of sparse one-step (state, action, end-state) tuples from an ==external editable memory bank==; ESWM-T explores **+16.8%** more unique states than EPN, navigates at **96.8%** SR (**+18%** vs EPN) with **99.2%** path optimality, adapts to new obstacles (**93%** vs **72%** EPN, **56%** RL).

- **[[2508.04931|INTENTION]]** — A ==VLM intuitive-perceptor + memory== framework inferring humanoid motion tendencies without explicit instructions, building a ==MemoGraph== of interaction episodes as scene graphs matched at inference; **84%** planning / **72%** execution on intuitive tasks (vs 20%/15% LLM-BT), comparable on standard manipulation, real humanoid intuitive reasoning.

- **[[2602.04600|Act-Sense-Act]]** — A non-Markovian active-perception VLA (CoMe-VLA) pretrained on large-scale egocentric human data then robot-fine-tuned in a unified egocentric action space, via a ==Cognitive Auxiliary Head== + ==Dual-Track Memory==; **83.3%** mean SR over five long-horizon tasks (vs OpenVLA-OFT **12.7%**), **72.0→87.3%** as human data scales 400k→800k.

- **[[2607.24190|Kim Episodic Memory]]** — An ==episodic memory module== on humanoid robot head Kim storing conversational fragments as ==vector embeddings== with ==LLM-derived emotional metadata==, retrieved via ==hybrid recency + emotional-intensity scoring==; **+0.60** Cohen's d Sociability (**p<.001**) — §1.2's embedding-retrieval pattern, applied to conversational memory.

**Episodic & Retrieval Memory — Decision Matrix**

| Need | Recommendation |
|---|---|
| Disambiguate visually-aliased states in manipulation | [[2603.24576\|Chameleon]] (**100.0%** episodic-recall DSR) |
| Explicit memory-bank policy + non-Markovian benchmark | [[2501.18564\|SAM2Act]] (**94.3%** MemoryBench) |
| Long-horizon navigation exploration with memory-based QA | [[2601.10744\|LMEE]] + LMEE-Bench |
| Purge moved/removed objects from a dynamic scene | [[2411.04999\|DynaMem]] |
| Compress full history into a fixed token budget | [[2608.01456\|MeMento]] (**-85.38%** memory, **+15.74%** accuracy) |
| Robot-control WAM with a dedicated memory module | [[2606.20562\|MemoryWAM]], [[2606.10363\|HiMem-WAM]], [[2606.27677\|DiM-WAM]] |

^dm-1

> [!star] Key Papers
> - [[2402.19161|MemoNav]] — established the biologically-inspired STM+LTM working-memory paradigm that [[2507.12846|Mind-Palace]] and [[2601.10744|LMEE]] both build on.
> - [[2411.04999|DynaMem]] — the reference dynamic-memory design (ray-cast purging of moved objects); nearly every later retrieval-memory nav paper compares against it.
> - [[2603.24576|Chameleon]] — the clearest existence proof that human-episodic-memory structure (spatiotemporal anchors, pattern separation) transfers to manipulation.
> - [[2606.20562|MemoryWAM]] — the first world-action model to treat memory as a first-class module rather than a longer context window.
> - [[2104.10218|Episodic-Memory-Manipulation]] — the earliest paper in this file (2021); single-demo task synthesis via finite-state-machine memory predates the current wave by four years.

^key-papers-1

> [!tip] Same Pattern, Reinvented Three Times
> Navigation's working memory (§1.1), navigation's dynamic memory (§1.2), and manipulation's episodic memory (§1.3) converged on the same three ideas — hierarchical short/long-term stores, event-boundary compression, and retrieval-on-demand — from three separate research communities that rarely cite each other. That convergence is the strongest available evidence that episodic memory is a *domain-independent* embodied-AI primitive, not a navigation trick or a manipulation trick. See [[13_Navigation-and-Mobile-Manipulation#3.2 Working & Episodic Memory]] and [[10_Manipulation-Skill-Learning#4.1 Episodic & Retrieval Memory]] for the two source domains this section unifies.

^insight-1

### 2. Object-Permanence & Keyframe-History Policies

A different failure mode than §1: the object is still there, the policy just can't see it right now. Rather than retrieving from an episodic store, these policies maintain explicit beliefs about objects — including occluded ones — or distill the observation history into a handful of semantically salient keyframes instead of carrying every raw frame. The distinction matters because the fix is different: episodic memory answers "what happened," object-permanence answers "what's still true about the world even though I can't currently observe it."

Two sub-sections split on *what persists*: an object's identity through occlusion (§2.1), or the moments worth remembering out of a long history (§2.2). Both trade raw-frame carrying for a compressed, structured stand-in.

#### 2.1 Object Permanence & Identity Tracking

Keep an object's identity — position, grasp state, role — alive across occlusion, handover, and exit/re-entry from the frame, without re-detecting it from scratch each time it reappears.

- **[[2608.05042|BridgeVLA++]]** — Extends [[2506.07961|BridgeVLA]]'s ==2D-heatmap pre-training== + orthographic-projection 3D fine-tuning with a unified ==spatio-temporal memory== (temporal keyframes for coarse reasoning, point-cloud memory for occlusion-robust localization); **93.7%** RLBench, **96.0%** RMBench (**+13pp** over MemoryWAM), **95.4%** real Franka at **3** demos/task.

- **[[2309.15278|Out-of-Sight-Still-in-Mind]]** — A ==DOOM/LOOM object-oriented memory== hallucinating point clouds or propagating latents for occluded objects, with a ==relational dynamics + CEM planner==; **0.976** relational F1, near-1.0 planning success, **19/20** real; +10–20% F1 over implicit memory.

- **[[2503.05189|Persistent-Object-Gaussian-Splat]]** — A persistent object representation (POGS) embedding ==grouping + CLIP + DINO features into 3D Gaussians== with an online tracking loop optimizing object poses to keep identity through occlusion and handover, no CAD models; **2.92 cm** placement error, up to 12 consecutive resets, recovering from **80%** of in-grasp tool perturbations.

- **[[2607.18016|POT-VLA]]** — A closed-loop humanoid VLA introducing ==Persistent Object Tokenization (POT)==, a role-indexed 3D object memory in the ==GR00T-N1.7== action-head, plus a ==geometric predicate supervisor== for verification/recovery; **71/80** real G1 loco-manip trials (vs **39/80** baseline), **9/10** under novel objects — mitigates "object-state divergence" in long-horizon tasks.

- **[[2608.05523|HERA]]** — A parameter-efficient adapter (==Register-Routed Patch Memory==, **3.00M** params) bolting a ==Structured Memory Bank== + gated Memory/Workspace Registers onto a frozen V-JEPA 2-G predictor for occlusion-robust physical prediction; **54.35%** IntPhys2 pairwise AvgSurprise (**+1.78pp** over baseline), **+17.31pp** on Immutability (Fixed Camera).

#### 2.2 Keyframe-History Compression

Rather than tracking objects explicitly, distill the raw history into a small set of salient keyframes — detected by deceleration, VLM saliency, or event boundaries — and condition on those instead of the full sequence.

- **[[2607.08283|TFP]]** — A memory-fusion policy augmenting a chunked VLA with an episode-local latent belief driven by ==Liquid Time-Constant networks==, modulating a ==flow-matching action decoder== via ==AdaLN== conditioning; **98.75%** LIBERO (vs π₀.₅'s 96.9%), **75.0%** on occluded ShellGameTouch, fewer real stage-memory failures on a Galaxea A1.

- **[[2606.31493|ChronoFlow-Policy]]** — A diffusion visuomotor policy unifying past-current-future gripper-object interaction via a compact ==3D keypoint representation (ChronoFlow)==, jointly learning ChronoFlow prediction + actions via a ==co-training objective== to resolve non-Markovian dependencies; **72%** MetaWorld / **66%** RoboTwin 2.0, **87%** real deformable towel-folding.

- **[[2606.23589|KEMO]]** — A lightweight plug-in memory augmenting a VLA with a temporally-ordered bank of ==event keyframes==, detected from deceleration cues + a visual-change filter (no labels) and fused via masked cross-attention + gated residual fusion; **+23.6pp** Task SR (27.8→51.4%) and **+34.1pp** Stage Completion (42.3→76.4%) over a memory-free baseline across 6 real dual-arm tasks.

- **[[2602.15010|BPP]]** — A ==Big Picture Policies== method conditioning on VLM-detected (Gemini-3-Pro) salient ==keyframes== at 1 Hz with ==latency masking==; **+70%** real bimanual SR over history-conditioned baselines, beating even the oracle on Variable-Password; robust to imperfect keyframes.

- **[[2503.00193|ProDapt]]** — A proprioceptive policy conditioning a diffusion model on ==contact "keypoints"== — past contact events a ==keypoint manager== selects by spatial distance and normal-force direction — fed alongside short-term proprioception as long-term memory; **80%** on an "Elbow" task where all baselines (even H_o=50) fail, completing tasks faster at real-time inference.

- **[[2511.00153|EgoMI]]** — An ==egocentric whole-body data system== capturing synchronized human head + hand trajectories for a semi-humanoid with a fully-actuated camera head, plus ==SPARKS==, a training-free spatial-memory keyframe selector for dynamic head motion; active-head policy **36/40** vs 29/40 wrist-only on tabletop search, **35/40** vs 0/40 on shelf search.

**Object-Permanence & Keyframe-History — Decision Matrix**

| Need | Recommendation |
|---|---|
| Occlusion-robust identity through handover | [[2503.05189\|Persistent-Object-Gaussian-Splat]] (**2.92 cm** placement error) |
| Role-indexed persistent object memory in a VLA action-head | [[2607.18016\|POT-VLA]] (**71/80** vs **39/80** baseline) |
| Cheap semantic keyframes at 1 Hz | [[2602.15010\|BPP]] (**+70%** real bimanual SR) |
| Occlusion-robust adapter on a frozen world-model predictor | [[2608.05523\|HERA]] (**3.00M** params) |
| Non-Markovian dependency via co-trained keypoint prediction | [[2606.31493\|ChronoFlow-Policy]] |

^dm-2

> [!star] Key Papers
> - [[2309.15278|Out-of-Sight-Still-in-Mind]] — the earliest and still-cited reference for hallucinating occluded-object state via relational dynamics.
> - [[2503.05189|Persistent-Object-Gaussian-Splat]] — established 3D-Gaussian identity tracking as a CAD-free alternative to re-detection.
> - [[2608.05042|BridgeVLA++]] — the current state of the art for combining keyframe and point-cloud memory in one spatio-temporal module.
> - [[2503.00193|ProDapt]] — the clearest demonstration that a handful of contact keypoints can substitute for full proprioceptive history.

^key-papers-2

> [!tip] Two Kinds of "Remembering What You Can't See"
> Object-permanence and keyframe-history solve the same visibility gap with opposite strategies — track the *thing* (explicit per-object state that survives occlusion) versus track the *moment* (compress history to the few frames that matter). Policies that need precise re-grasping after occlusion want §2.1; policies that just need to disambiguate "have I done this step yet" want §2.2. See [[10_Manipulation-Skill-Learning#4.2 Object-Permanence & Keyframe-History Policies]] for the manipulation-side source and §1 above for the complementary retrieval-based approach to the same non-Markovian problem.

^insight-2

## Part B — Memory-Integrated Architectures

*Where the memory lives once it's built into a policy or a reasoner.*

### 3. Persistent Spatial Memory & Cognitive Maps

Episodic memory (§1) remembers *events*; this section remembers *space* — a representation of the environment that survives across an entire mission, not just a few steps. The distinction is structural: a cognitive map is queried by location and relation ("what's near the kitchen?"), not by recency or similarity to the current observation. That makes it the substrate long-horizon exploration, multi-room search, and embodied QA all build on.

Two sub-sections split on *where the map lives*: as an explicit external structure the agent queries (§3.1 — scene graphs, voxel grids, Gaussian splats), or baked directly into the policy's own weights via memory tokens threaded through the VLA backbone (§3.2). The first is legible and inspectable; the second is faster and end-to-end trainable. Neither has displaced the other.

#### 3.1 Scene-Graph & Map Representations

External, queryable structures — 3D scene graphs, voxel grids, Gaussian-splat memories — built online as the agent explores, then re-consulted by a separate planner or VLM.

- **[[2608.09816|Hierarchical Fast-Slow ReAct Agent]]** — An ==event-triggered bounded reason-retrieve-act loop== fires on four structural triggers, retrieving keyframes from a coordinate-anchored two-tier memory only when text can't decide; **68.75%** SR on HM3D at **5.00** model calls/episode — deliberating at every frontier scores *below* greedy.

- **[[2607.23797|VLMM]]** — An ==attention-scheduling== framework minimizing value-weighted staleness via a derived ==√·-law== setting re-observation frequency by item importance and change rate, tracked with a ==Vision-Language-Motion Map==; **21-26%** lower staleness vs a real CLIP zero-shot prior — freshness as active scheduling, not a passive store.

- **[[2607.13245|JITOMA]]** — Replaces ahead-of-time 3DSG construction with ==just-in-time scene graph growth==: a two-tier memory of ephemeral hypotheses + dormant anchors only triggers ==dense captioning== on task-relevant nodes; **1-4** active objects vs hundreds for baselines, **9-21x** faster than ConceptGraphs, **+5.0** IoU / **+9.4** mR@1 — avoids "cognitive myopia" in LLM planners.

- **[[2607.05543|GEM-Occ]]** — Converts transient visual geometry into persistent ==Gaussian Evidence Memory==: semantic Gaussian occupancy + explicit free-space ray evidence, updated by ==visibility/uncertainty-aware causal fusion== across rooms and buildings; **+3.85** IoU / **+2.68** mIoU online, **-40%** memory building-scale — with the new HIOcc hierarchical-indoor benchmark.

- **[[2606.31144|Modular VLA Framework]]** — A ROS-based mobile framework building a real-time ==3D semantic voxel map== (OwlViT) fused with a ==VLM query-classification + context-aware-prompt== pipeline (Gemini 2.0 Flash) for numerical/reference/instruction queries; exploration time cut **50%** (8m42s→4m17s) — persistent semantic memory as the language-grounding substrate.

- **[[2606.23565|HoloAgent-0]]** — A unified embodied-agent framework grounding LLM planning in a persistent ==3D Spatial Memory Layer== and a ==typed embodied-skill interface== for closed-loop feedback-driven re-planning; **97.70%** Top-1 SR in real long-horizon apartment nav and **31.58%** / **29.93%** mIoU mapping on ScanNet / Replica — memory-centric agent for nav + mobile manipulation.

- **[[2509.20739|Semantic-Object-Exploration]]** — A legged-robot object-exploration method pairing ==confidence-calibrated semantic arbitration== over scene+object cues with a ==controlled-growth topological memory== and ==LLM utility-driven subgoal selection==; **90.1%** semantic accuracy (**+4.8 pp**) and **85.8%** node-selection accuracy on a Unitree Go1 — topological memory over dense maps.

- **[[2502.00931|VL-Nav]]** — A ==neuro-symbolic== VLN agent pairing a NeSy task planner over a ==symbolic 3D scene graph== + object-centric memory (Qwen3-VL) with a NeSy exploration system fusing neural semantic cues, geometric heuristics, and curiosity; **86.3%** real-world SR over long (483 m) multi-floor routes and **79.2%** in DARPA TIAMAT sim — symbolic memory for reasoning-based nav.

- **[[2012.03912|MultiON]]** — A benchmark of map-memory for sequential multi-object navigation; explicit semantic maps held **48%** SR on 3-ON tasks vs **10%** for an RNN-only agent, and learned-map agents gained up to **+25%** SR when a goal had been seen before — the foundational evidence that *explicit* semantic memory beats implicit memory as task complexity grows.

- **[[2412.14480|GraphEQA]]** — Builds online ==3D metric-semantic scene graphs== enriched with LLM room labels and semantically-connected frontier nodes, fused with a top-K task-relevant visual memory to ground a hierarchical VLM planner; **63.5%** SR on HM-EQA (vs Explore-EQA's **51.7%**), false positives cut to **6.36%** vs **24.56%** — incremental online scene graphs beat full offline access.

- **[[2411.17735|3D-Mem]]** — A scene memory representing space as multi-view ==Memory Snapshots== (explored) + ==Frontier Snapshots== (unexplored) built via co-visibility clustering for VLM-guided exploration; **69.1%** SR on GOAT-Bench lifelong nav using only **10.94** snapshots from **39.76** observations (**3.26** after prefiltering) — compact, queryable 3D scene memory.

- **[[2605.21133|Spatial-Brain-Cerebellum]]** — A hierarchical ==multi-agent== humanoid whole-body manipulation framework pairing a VLM-driven ==Active Spatial Brain== (active perception + memory + adaptive planning) with a ==Generalizable Action Cerebellum== (A* navigation + reachable-space solver + VLM grasping); **60.0%** vs 0% on Task-4-Hard, **69.6%** unseen-item SR, no task-specific data.

#### 3.2 Memory Baked into the VLA Backbone

Rather than an external map, thread memory directly through the policy's own transformer — moment tokens, declarative scene/episodic memory, recurrent memory tokens — so recall is a forward pass, not a lookup.

- **[[2608.09410|HyMeS]]** — ==Flow-matching== fine-tunes motor skills in weights while a coding agent revises an executable memory-update program from rollout traces, gated by **PACE** multi-frame ==Qwen3-VL-8B== verification; **66.2%** cumulative SR on RoboMemArena (**+4.5pp**).

- **[[2608.06729|AtlasVLA]]** — Threads two backbone-native stores through a diffusion action head: a ==voxel-hashed Persistent World State Memory== (wrist tokens back-projected to 3D) and an ==Ego-Working State Memory== (intent-aware queries preventing drift); **97.6%** LIBERO wrist-only (beats third-person-and-wrist OpenVLA-OFT), **94.6%** LIBERO-Long (**+7.0pp** over [[2508.19236|MemoryVLA]]).

- **[[2607.18231|FM-VLA]]** — Augments a VLA action expert with two proprioceptive memory tokens: a ==VAE==-compressed long-horizon wrench-history latent and a short-window joint-state projector, giving force-based rather than visual temporal context; **83.3%** avg SR on contact-rich memory-dependent tasks vs **27.8%** memoryless and **33.3%** visual-memory baselines.

- **[[2607.07608|LaMem-VLA]]** — A ==dual latent memory== VLA weaving a short-term visual vault + long-term action-hidden-state vault directly into the VLM's input sequence via a ==Latent Memory Condenser==; **73.9%** SimplerEnv-Bridge (**+16.6pp** over CogACT), **97.6%** LIBERO avg.

- **[[2606.29936|OpenSPM]]** — A decompositional architecture separating semantic/experience retrieval from geometric action generation via a ==key spatial pose memory== of object-centric relative poses at phase boundaries, feeding a closed-loop ==flow-matching== generator; **85.6%** LIBERO-GOAL at **0.24M** params / **1033.3 Hz**; ablating the memory drops SR to **23.8%**.

- **[[2606.17480|GeneralVLA-2]]** — A hierarchical-VLA upgrade adding ==GeoFuse-MV3D== (multi-view RGB-D + geometry-prior fusion + mask verification for faithful 3D recon) and a ==governed KnowledgeBank== (quality/confidence/lifecycle metadata + precision retrieval) for trustworthy long-term memory; higher SR on **10/14** RLBench tasks + all four real Franka tasks, training-free.

- **[[2606.12497|μVLA]]** — A minimal recurrent-memory VLA inserting learnable ==memory tokens== into an OpenVLA-OFT backbone with ==TBPTT== + an attention-mask guard, isolating recurrence for partially observable manipulation; **0.84** avg SR on MIKASA-Robo (vs **0.42** memoryless) while retaining **96.2%** on fully observable LIBERO.

- **[[2605.22283|SOMA]]** — A persistent ==spatial-semantic 3D memory== built by multi-view head-camera scanning (2D detections lifted to a unified 3D frame) + dynamic refinement; **30%/25%** pick/place on "Invisible-to-Invisible" out-of-vision PnP where 2D VLAs fail.

- **[[2511.18960|AVA-VLA]]** — A ==POMDP reformulation== of VLA whose ==recurrent state== drives an ==Active Visual Attention== module over task-relevant tokens; **98.0%** avg LIBERO SR (vs OpenVLA-OFT **96.8%**), **99.6%/84.1%** CALVIN 1-in-a-row/5-in-a-row, best avg on **four** real Mobile ALOHA tasks. The recurrent state accommodates *force history*; "active force attention" is unbuilt.

- **[[2511.18112|EchoVLA]]** — A biologically-inspired ==declarative memory==: persistent voxelized ==Scene Memory== + time-indexed ==Episodic Memory== with coarse-to-fine retrieval; **0.31** RoboCasa mobile manip (vs π0.5 0.20), **0.44** real TidyBot++.

- **[[2604.18791|HELM]]** — An ==Episodic Memory Module== (CLIP-retrieved keyframe key-value store) + learned ==State Verifier==; **81.5%** LIBERO-LONG (+23.1pp over OpenVLA), **54.2%** LIBERO-Recovery (vs 12.3%) — memory + verification compose.

- **[[2510.00695|HAMLET]]** — A ==History-Aware Memory with Learned Tokens== where per-timestep "moment tokens" compress history into a fine-tunable module; **+47.2%** real history-dependent SR (66.7% vs 12.5%) at ~**1%** overhead.

- **[[2511.11478|LIBERO-Mem]]** — A non-Markovian benchmark (10 tasks: object memory, temporal dependency, identity ambiguity) + ==Embodied-SlotSSM== slot-centric VLA; exposes that current VLAs hit only **14.8%** subgoal completion on memory-critical tasks.

- **[[2605.14712|IntentVLA]]** — A VLA modeling ==short-horizon intent== from recent visual history via a frozen ==VGGT-1B== geometry-aware encoder over past head-cam frames; **45.8%** on AliasBench (vs **9.0%** baseline), **−17.6%** inter-chunk consistency error.

- **[[2509.20297|mindmap]]** — A 3D diffusion policy pairing a DDPM trajectory generator with a continuously-built ==metric-semantic 3D reconstruction== (frozen AM-RADIO features) processed via separate encoders so the policy attends to out-of-view objects; **76%** avg on novel spatial-memory tasks (**+56pp** over 3D Diffuser Actor), **97%** Mug-in-Drawer, extends to bimanual humanoids.

**Persistent Spatial Memory & Cognitive Maps — Decision Matrix**

| Need | Recommendation |
|---|---|
| Foundational map-memory benchmark | [[2012.03912\|MultiON]] |
| Multi-view snapshot memory for VLM-guided exploration | [[2411.17735\|3D-Mem]] |
| 3D metric-semantic scene graph with LLM room labels | [[2412.14480\|GraphEQA]] |
| Persistent 3D memory layer for closed-loop LLM re-planning | [[2606.23565\|HoloAgent-0]] |
| Memory tokens dropped into an existing VLA backbone | [[2606.12497\|μVLA]] (minimal, OpenVLA-OFT + TBPTT) |
| Non-Markovian benchmark for VLA memory ablation | [[2511.11478\|LIBERO-Mem]] |
| Wrist-only spatial + task-progress memory, no third-person camera | [[2608.06729\|AtlasVLA]] (**97.6%** LIBERO) |
| Force/proprioceptive memory rather than visual history | [[2607.18231\|FM-VLA]] (**83.3%** contact-rich SR) |

^dm-3

> [!star] Key Papers
> - [[2012.03912|MultiON]] — the original map-memory benchmark that every later semantic-map paper in this section still targets.
> - [[2411.17735|3D-Mem]] — the reference Memory-Snapshot / Frontier-Snapshot design most 2025-2026 scene-memory papers extend.
> - [[2412.14480|GraphEQA]] — the canonical online 3D scene-graph construction for embodied QA.
> - [[2510.00695|HAMLET]] — the first clean demonstration that "moment tokens" baked into the backbone beat frame-stacking without an external map at all.

^key-papers-3

> [!tip] External Map or Internal Tokens — the Field Hasn't Chosen
> §3.1's external scene graphs are inspectable and composable with any planner, but add a construction-and-query pipeline outside the policy. §3.2's backbone-native memory tokens are faster (one forward pass, no separate map to maintain) but opaque — you can't print out what a memory token "knows." 2026 papers increasingly hedge with both ([[2606.17480|GeneralVLA-2]]'s governed KnowledgeBank feeding a still-external map). See [[04_VLA#10.1 Persistent Spatial & Object Memory]] for the VLA-backbone source and [[13_Navigation-and-Mobile-Manipulation#3.1 Semantic & Cognitive Maps]] for the full 31-paper scene-graph landscape this section curates a 10-paper memory-framed subset from.

^insight-3

### 4. Progress-Aware & Hindsight Control

A VLA that treats every step identically cannot tell "I'm mid-reach" from "I just knocked the object over and need to recover." Progress-aware and hindsight control gives the policy temporal self-awareness — an explicit notion of which phase of the task it occupies, and the ability to look backward at what just happened before deciding what to do next. This is a narrower, VLA-architecture-specific problem than §1's general episodic memory: the state being tracked is not "what happened five minutes ago" but "where am I in *this* execution, right now."

All six papers share one axis — bidirectional temporal reasoning threaded through the action head itself — but split on *how* that state is represented: as discrete phases the policy explicitly names, or as an unnamed continuous representation, carried across queries or recomputed as a past/current/future window.

#### 4.1 Explicit Phase & Subgoal Decomposition

Break the task into named phases or subgoals up front, then condition behavior on which one is currently active.

- **[[2604.17880|ST-π]]** — A ==Spatiotemporal VLM== that decomposes tasks into ==causally-ordered chunk-level prompts== (semantic + spatial + temporal) + ==Spatiotemporal Action Expert==; highest SR and shortest completion across four LIBERO suites, surpassing OpenVLA, Octo, SpatialVLA, TraceVLA, 4D-VLA, CogACT, and π0.5, plus leads all three real STAR-dataset suites.

- **[[2603.09292|See-Plan-Rewind]]** — A ==See-Plan-Rewind== cycle that decomposes tasks into spatially-grounded 2D subgoals with explicit ==error-recovery rewind==; **91.8%** LIBERO (+5.0 over MolmoAct), SOTA OOD robustness on LIBERO-Plus.

- **[[2508.19958|Long-VLA]]** — An end-to-end long-horizon VLA that decomposes trajectories into ==moving vs interaction phases== with a phase identifier + a ==dynamic binary input-masking== that selectively attends to phase-relevant views (third-person for moving, ego for interaction); up to **+81%** rel over base on 10-step L-CALVIN (avg length **8.24**), real 8-step where baseline fails.

#### 4.2 Continuous, Unnamed Temporal Representations

No named phases — the state is a continuous representation instead of a labeled index: either a revisable execution-state vector persisted and updated across successive queries (ChainVLA, WeaveLA), or a bidirectional past/current/future window over compact motion vectors recomputed at each step (HiF-VLA).

- **[[2608.02326|ChainVLA]]** — A unified, revisable ==execution state== (Progress Context + Motion Tail) explicitly passed across successive VLA queries so task evidence and unexecuted motion both persist across replanning; **62.8%** RMBench (vs Mem-0's 52.8%), **98.8%** avg LIBERO; ablating either component collapses SR to **11.2%/3.0%**.

- **[[2606.17463|WeaveLA]]** — An event-driven action-side ==latent memory weaving== interface bolted onto a frozen VLA backbone that writes a ==Memory Weaver==-compressed task state at sub-goal completion events to condition the next action expert via memory-conditioned AdaRMS; lifts RoboMME avg SR **19.0%→24.7%** and SWINGXTIMES **0%→47.8%** on repetition tasks.

- **[[2512.09928|HiF-VLA]]** — A ==Hindsight-Insight-Foresight== bidirectional temporal reasoning over compact codec ==motion vectors== (past/current/future dynamics); **94.4%/96.4%** LIBERO-Long third/multi-view at negligible overhead.

**Progress-Aware & Hindsight Control — Decision Matrix**

| Need | Recommendation |
|---|---|
| Phase-decomposed long-horizon execution | [[2508.19958\|Long-VLA]] (moving vs interaction phases) |
| Bidirectional past/current/future temporal reasoning | [[2512.09928\|HiF-VLA]] |
| Explicit error-recovery rewind on subgoal failure | [[2603.09292\|See-Plan-Rewind]] |
| Drop-in memory-weaving on a frozen VLA backbone | [[2606.17463\|WeaveLA]] |
| Revisable execution state across replanning queries | [[2608.02326\|ChainVLA]] |

^dm-4

> [!star] Key Papers — Temporal Self-Awareness Landmarks
> - [[2508.19958|Long-VLA]] — the reference phase-decomposition design (moving vs interaction) that later papers in this section refine rather than replace.
> - [[2512.09928|HiF-VLA]] — the cleanest formalization of hindsight-insight-foresight as one bidirectional reasoning module.
> - [[2608.02326|ChainVLA]] — the most recent and most general: a single revisable execution state that survives arbitrary replanning, not just a fixed phase count.

^key-papers-4

> [!tip] Progress Tracking Is Memory, Just Very Short
> Every mechanism here is a special case of episodic memory (§1) collapsed to the timescale of a single task execution — the state being carried is "where am I in this rollout," not "what happened across episodes." The six papers converged independently on the same fix (explicit progress/phase state threaded through the action head) within a five-month window (2025-05 to 2026-08), suggesting the field had exhausted frame-stacking's headroom around the same time everywhere. See §1 above for the longer-horizon analog and [[05_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] for where temporal reasoning sits among the field's other reasoning-insertion points.

^insight-4

### 5. Memory-Augmented Reasoning & Planning

§1-§4 build memory *for a policy*. This section builds memory *for a reasoner* — an LLM or VLM sitting above the action layer that needs a persistent store to plan, answer questions, or enforce constraints across a long episode. The distinguishing feature is architectural: memory here is explicitly queried and updated by symbolic or language-model reasoning (a 'Cognitive Map,' a typed knowledge graph, a multi-store agentic loop), not implicitly threaded through action-head weights.

All ten papers share the same axis — a memory store that a reasoning module explicitly reads and writes — but split on *what the memory is for*: answering questions and directing exploration, grounding planning in an explicit 3D scene graph, or running as an explicit multi-store agent architecture.

#### 5.1 Embodied QA & Exploration Memory

Memory whose job is to guide *where to look next* and *what the answer is* — centralizing evidence across an exploration episode.

- **[[2601.13132|GaussExplorer]]** — An embodied exploration + reasoning framework over ==semantic 3D Gaussian Splatting== (open-set CLIP per Gaussian), where an LLM extracts query 'evidence categories' to search-and-cluster objects and a VLM ==novel-view judge== evaluates perturbed camera poses; **57.8** LLM-Match EM-EQA (3D-Mem **54.6**), **12.87** 3D mIoU referring segmentation.

- **[[2506.17629|CLiViS]]** — A ==training-free== embodied-visual-reasoning framework orchestrating LLM↔VLM synergy: the LLM emits focused sub-instructions, the VLM perceives target video segments, and both update a =='Cognitive Map'== (Scene Navigation + Object Relation Graphs) + Evidence Memory; **55.4%** OpenEQA, **69.4%** EgoSchema (**48.4%** avg), beating Socratic models **+20.2%**.

- **[[2505.13948|Memory-Centric-EQA]]** — A ==memory-centric== Embodied-QA framework (MemoryEQA) centralizing a memory store to guide planner, stopping, and answering modules, via a ==viewpoint-contrastive== update rule, entropy-based adaptive retrieval, and a query-complexity dynamic-k mechanism, plus the MT-HM3D benchmark; **43.11%** SR (**+9.9pp**) with fewer exploration steps, SOTA on OpenEQA.

#### 5.2 3D Scene-Graph Memory for Planning

Memory as an explicit 3D scene graph a downstream planner reasons over directly — one paper carries that graph as far as an enforced safety filter, the other stops at planning/navigation.

- **[[2606.29786|OP3DSG]]** — Builds a unified open-vocab 3D scene graph (objects + interactive parts + spatial/functional relations + affordances) via ==knowledge-guided part detection== and ==geometry-anchored, CoT-inspired multi-agent LLM reasoning==; **+31.2pp** part-node R@3 on UniGraph3D, deployed on a Stretch3 robot for QA/planning/navigation.

- **[[2606.28592|E2-CARE]]** — Unifies environment, robot embodiment, and humans in one ==3D dynamic scene graph==, over which an ==LLM== reasons about context to synthesize safety constraints + preferences per skill, enforced by an ==Operational-Space CBF== filter; **~95%** success / **80%** constraint satisfaction across 130 environments + 5 embodiments (**+15-40pp**) at **~0.15ms** overhead.

#### 5.3 Multi-Store Agentic Memory Architectures

Memory factored into several named, typed stores (temporal, semantic, episodic) that an agent loop coordinates explicitly.

- **[[2608.04933|Mimir]]** — A ==neuro-symbolic== memory system separating ==World Memory== (entity/attribute graph persisting knowledge about unseen objects) from ==Task Memory== (goal status, hand state, failed hypotheses) via a ==dynamic grounding== module; **+23.0%** avg SR across 13 backbones, **68.0%/90.0%** SR on EB-ALFRED/EB-Habitat (**+16.0pp** over prior-best [[2508.01415|RoboMemory]]).

- **[[2608.04765|Language-Memory VLA]]** — A hierarchical VLA whose high-level branch emits ==recursive language memory== (rolling-compression over history + near-future intent) + subtasks conditioning a low-level flow-matching action branch; BEHAVIOR-1K stage SR **30.0% → 40.0%**, Genie Sim 3.0 sorting **41.7% → 63.9%**; enables in-context failure recovery on a real XLeRobot.

- **[[2607.18840|WorldScape Policy 2.0]]** — Combines a ==causal short-term visual memory== with a VLM-based ==event memory== for ==latent subgoal reasoning==, trained on the new ManipEvent-5M event-grounded dataset; **94.3%** avg SR across 50 bimanual sim tasks (**+14.5pp** over VLA baselines), **75%** real long-horizon autonomous planning.

- **[[2607.14252|MEMORA]]** — An ==Embodied Action Memory (EAM)== system built from egocentric video via four ==typed memory stores== (Environment, Entity, Activity, Inferred Knowledge) with online ==Memory Editor== revision and ==offline consolidation==; **+20.5pp** memory-assessment accuracy, **+16.6%** OOD generalization planning, **~18×** fewer entity records vs append-only logs.

- **[[2508.01415|RoboMemory]]** — A ==brain-inspired multi-memory== agentic framework with a Perception-Memory-Retrieval-Planning-Execution loop and Planner-Critic module, unifying four parallel stores (Temporal, Spatial ==Knowledge Graph==, Semantic, Episodic) over a LoRA-finetuned VLA; **70.5%** avg EmbodiedBench SR (Claude-3.5-Sonnet **69.5%**), real-world repeat-task SR **26.67% → 46.67%**.

**Memory-Augmented Reasoning & Planning — Decision Matrix**

| Need | Recommendation |
|---|---|
| Memory-centralized embodied QA | [[2505.13948\|Memory-Centric-EQA]] + MT-HM3D benchmark |
| Training-free LLM↔VLM cognitive-map reasoning | [[2506.17629\|CLiViS]] |
| Four-store brain-inspired agentic memory | [[2508.01415\|RoboMemory]] (Temporal/Spatial-KG/Semantic/Episodic) |
| Best raw SR: neuro-symbolic World/Task memory split | [[2608.04933\|Mimir]] (**+16.0pp** over RoboMemory) |
| Safety-constraint synthesis from a unified scene graph | [[2606.28592\|E2-CARE]] (Operational-Space CBF) |
| Recursive language memory feeding a low-level action branch | [[2608.04765\|Language-Memory VLA]] |
| VLM event memory for bimanual subgoal reasoning | [[2607.18840\|WorldScape Policy 2.0]] (**94.3%** avg SR) |

^dm-5

> [!star] Key Papers
> - [[2505.13948|Memory-Centric-EQA]] — the reference design for centralizing memory as the hub every EQA sub-module queries, rather than a peripheral cache.
> - [[2508.01415|RoboMemory]] — the most architecturally ambitious: four parallel typed stores (temporal, spatial-KG, semantic, episodic) unified under one Planner-Critic loop.
> - [[2608.04933|Mimir]] — the current best raw SR in this section (**+16.0pp** over RoboMemory), via a simpler two-store World/Task split rather than four parallel stores — architectural ambition and raw performance point different directions.
> - [[2606.29786|OP3DSG]] — establishes open-vocabulary 3D scene graphs with interactive parts and affordances as first-class memory content, not just object labels.

^key-papers-5

> [!tip] The Reasoner Wants a Graph, the Policy Wants a Token
> Compare this section's memory stores (scene graphs, typed knowledge graphs, Gaussian-splat evidence) to §3.2's — a reasoning module needs memory it can query symbolically and explain, so it reaches for structured, inspectable representations, while a policy's backbone-native memory (§3.2) reaches for opaque tokens because speed matters more than legibility at 10-50 Hz control rates. See §3 above for the token-native counterpart and [[16_Self-Evolving-VLA-WAM#7.1 Experience Distillation & Memory-Driven Evolution]] for what happens when this reasoning-layer memory starts rewriting the policy itself.

^insight-5

## Part C — Lifecycle, Landscape & Evaluation

*What happens to memory after deployment, its generative-model cousin, and how any of this gets measured.*

### 6. Memory-Driven Self-Evolution

Every prior section treats memory as something a policy *uses* at inference time. This section treats memory as something a policy *learns from* after deployment — the substrate a self-evolving agent writes failures, successes, and distilled experience cards into, then reads back to update its own behavior without a full retraining pass. This is the deployment-lifecycle bookend to §1's episodic memory: same storage problem, but the consumer is the training loop rather than the action head.

Two sub-sections split on *trigger*: memory written specifically when something goes wrong (§6.1), versus memory as a general substrate for distilling and replaying experience regardless of outcome (§6.2).

#### 6.1 Memory-Augmented & Failure-Driven Evolution

Memory that activates on failure — anomaly detection, error recovery, and incremental skill pools that grow specifically from what went wrong.

- **[[2608.08749|OnEvoMemory]]** — A ==value-guided hierarchical memory== (elite/transition/short-term banks) bolted onto a frozen VLA via ==gated cross-attention==; online rollouts refine only the memory + ==action-conditioned value estimator==; LiberoLong-10 **86.2%→90.2%**, RMBench SwapBlocks **0%→14%**.

- **[[2606.03598|PHASER]]** — A ==Phase-aware semantic experience replay== method for continual VLA via ==phase-centric capacity allocation== + ==multi-modal interference-aware routing== + an ==Auto-PC pipeline== that auto-discovers phase boundaries; up to **+31%** ASR over standard Experience Replay, hitting **87.8%** LIBERO-Goal / **85.8%** LIBERO-Long for OpenVLA-OFT-7B.

- **[[2605.10993|ECHO-VLA]]** — A ==hierarchical hyperbolic memory (HAE)== + autonomous memory consolidation; cone-tree retrieval + virtual-memory interpolation; **+12.8pp** LIBERO-Long.

- **[[2510.02298|ARMADA]]** — A ==FLOAT== (optimal-transport failure detector, **~95%** accuracy) plus ==multi-robot shared control== that routes interventions to free operators, while ==adaptive rewinding== collects high-quality corrective demos; the rewind-collected data lifts SR **+25.9%** and cuts human intervention **23.3%**.

- **[[2603.09030|PlayWorld]]** — An autonomous ==VLM Task Proposer + VLA Executer== self-play loop + ==Stable-Video-Diffusion== backbone finetuned via ==curriculum learning== on diverse contact-rich play; captures failure modes (slips, missed grasps) absent in human data, **Pearson 0.8766** predicted-vs-real SR correlation, **+65%** real-world SR via in-model fine-tune.

- **[[2502.07645|Action-Labels-Sets-Rethinking]]** — A ==set-valued supervision== method (CLIC) for incremental learning from interactive corrections: ==desired action sets== (polytopes / circles) tolerate noisy, partial, relative feedback via a ==policy-weighted Bayesian KL update== stable as old pointwise targets go stale; **80%** real Insert-T (vs **30%** Diffusion Policy / **10%** IBC).

- **[[2410.02995|RWLA]]** — ==Retrieval-based Weighted Local Adaptation==: task-agnostic pre-deployment 'review' retrieves scenario-similar demos by image+language embedding distance, ==selectively weighting== failure-divergent frames for local fine-tuning; LIBERO **39.65%→52.42%** over vanilla ER.

#### 6.2 Experience Distillation & Memory-Driven Evolution

A broader substrate: hierarchical episodic memory, phase-aware replay, and value-guided banks that consolidate experience into reusable structure regardless of whether the episode succeeded.

- **[[2607.00272|ASPIRE]]** — A continual-learning code-as-policy agent whose ==closed-loop execution engine== emits ==per-primitive multimodal traces==, distilling repairs into a persistent ==skill library== via ==evolutionary search==; **+77%** LIBERO-Pro Object, **+42.5%** Spatial SR gains; sim-to-real token cost **61.94M → 6.58M**.

- **[[2606.03374|eMEM]]** — A ==hybrid spatio-temporal memory system== for embodied agents built on a ==biologically-inspired tiered architecture== with a two-phase consolidation pipeline; **80.8** weighted-mean on eMEM-Bench v1, a flat retention curve at **100%** hit rate from 1 hour to 1 year, and a 30-pp drop when ablated to plain RAG.

- **[[2605.25832|AUTO-ROBOTIST]]** — A self-evolving agent converting ==robot-design trials into a 3-level NL skill library== (archetypes/rules/observations) with ADD/DIAGNOSE/MERGE maintenance; **1.47×** convergence speedup and +1.55 cross-scale fitness over a genetic-algorithm baseline.

- **[[2510.16079|EVOLVER]]** — A method that extracts structured ==experience cards== per episode via ==offline self-distillation==, then evolves the policy with ==GRPO + composite reward==; cards accumulate in a persistent bank; **0.382** avg EM over 7 QA benchmarks scaling monotonically from **0.150** (0.5B) to **0.382** (3B), self-distillation beating external-teacher distillation (**0.370**).

- **[[2506.21627|FrankenBot]]** — A brain-morphic VLM-orchestration agent whose ==Multi-level Anomaly Handling== gives real-time error recovery and whose ==Hierarchical Incremental Memory (HIMM)== + Incremental Skill Pool enable cross-task skill reuse, typically with *one VLM call per task*; **73%** real-world SR (vs VoxPoser **46%** / ReKep **55%**) across ten tasks.

- **[[2604.11306|Hierarchical-Episodic-Memory]]** — An ==H²-Emv== system that builds a ==hierarchical episodic memory== of recursively summarized nodes online, with ==LLM-estimated decay-based forgetting== and ==feedback-based relevance learning==; **45%** smaller memory, **35%** lower query compute, **+70%** second-round QA accuracy after feedback; deployed on the Armar-7 humanoid.

- **[[2602.04411|Self-evolving-Embodied-AI]]** — A paradigm-defining survey proposing a ==unified closed-loop framework== of five co-evolving modules (memory self-updating, task self-switching, environment self-prediction, embodiment self-adaptation, model self-evolution) that this file's agent/VLA/WAM split instantiates piecemeal.

- **[[2305.16291|Voyager]]** — The foundational open-ended embodied agent: frozen blackbox GPT-4 drives an ==automatic curriculum== + persistent ==skill library== of executable JS skills + ==iterative prompting== with ==self-verification==; **3.3×** more unique items, only method to reach the diamond tier, **73%** drop when self-verification is ablated — precursor to later skill-library agents.

- **[[2501.10395|t-DGR]]** — A lifelong-learning method via ==trajectory-based deep generative replay== (a ==diffusion== generator conditioned on timestep) + an ==AttentionTuner== that guides Transformer self-attention with human memory-dependency annotations; **81.9%** CW10 / **83.9%** CW20 and **99.8%** Mortar Mayhem vs **20.8%** vanilla, with **14–16×** less annotation effort.

**Memory-Driven Self-Evolution — Decision Matrix**

| Need | Recommendation |
|---|---|
| Foundational open-ended skill-library agent | [[2305.16291\|Voyager]] |
| Real-time error recovery + cross-task skill reuse | [[2506.21627\|FrankenBot]] (Hierarchical Incremental Memory) |
| Multi-robot failure routing + adaptive rewind | [[2510.02298\|ARMADA]] (**~95%** failure-detection accuracy) |
| Lifelong learning without catastrophic forgetting | [[2501.10395\|t-DGR]] (trajectory generative replay) |
| Phase-aware continual VLA replay | [[2606.03598\|PHASER]] (auto-discovered phase boundaries) |
| Value-guided elite/transition memory bolted onto a frozen VLA | [[2608.08749\|OnEvoMemory]] |

^dm-6

> [!star] Key Papers
> - [[2305.16291|Voyager]] — the foundational open-ended agent; every later skill-library-memory paper in this section is a specialization of its curriculum-plus-library pattern.
> - [[2506.21627|FrankenBot]] — the clearest bridge from failure-driven anomaly handling to a reusable Hierarchical Incremental Memory.
> - [[2604.11306|Hierarchical-Episodic-Memory]] — the most explicit borrowing of human memory-consolidation theory (decay-based forgetting) for a self-evolving agent.
> - [[2501.10395|t-DGR]] — the reference generative-replay solution to catastrophic forgetting, still the comparison point for later continual-learning work in this section.

^key-papers-6

> [!tip] Self-Evolution's Memory Is the Training Loop's Memory
> The mechanisms here (hierarchical stores, decay-based forgetting, value-guided elite banks) are the *same* primitives as §1's episodic memory, redirected at a different consumer: instead of feeding the current action, they feed the next gradient update or curriculum step. A system that gets this right doesn't need a separate "memory module" and "continual-learning module" — [[2602.04411|Self-evolving-Embodied-AI]]'s five-module framework names memory self-updating as one co-equal axis alongside task, environment, embodiment, and model self-adaptation. See [[16_Self-Evolving-VLA-WAM#6.3 Memory-Augmented & Failure-Driven Evolution]] for the source section and §1 above for the inference-time counterpart these mechanisms mirror.

^insight-6

### 7. Generative World-Model Memory — Landmarks

A genuinely *different* memory problem from everything above. §1-§6 all ask what a robot's *decision-making* should remember; this section asks what a *generative video model* should remember so a rendered rollout stays visually consistent — an object exited frame-left five seconds ago, and when the camera pans back, it needs to still be there, in the right place, looking the same. That is a rollout-fidelity problem, not a control problem, and it lives natively inside [[06_WAM]]'s ~39-paper memory landscape.

This section exists only to point readers at that fuller landscape, not to duplicate it — the eight papers below are the field's clearest landmarks (the first token-level memory bank, the first controlled ablation study, the first dedicated benchmark), curated as an entry point, split by *how many named mechanisms* each memory design combines, plus a third group that proposes no new mechanism at all — it measures memory mechanisms rather than adding one. For the complete generative-WAM memory literature, go to [[06_WAM#2.6 Neural Game Engines & Persistent Simulation]] directly.

#### 7.1 Single-Mechanism Memory Representations

One clearly-named memory structure carries the whole design — a 3D feature map, a token bank, a compressed cache — with no second mechanism fused in.

- **[[2505.05495|3D-Persistent-Embodied-WM]]** — An action-guided RGB-D ==video diffusion== (CogVideoX) with an explicit ==DINO-Map== 3D memory injected via cross-attention experts + ==Plücker== action embeddings for pixel-wise camera control; **FVD 91.9** (vs NWM **194.0**), **81.7%** scene-revisit consistency, improved MPC + policy learning, coherent **112-frame** rollouts.

- **[[2512.04040|RELIC]]** — An interactive video world model with long-horizon memory: a ==two-stage distillation== turns a 20-second bidirectional video-diffusion teacher into a real-time causal autoregressive student + a ==memory compression== (rolling-window cache + downsampled KV tokens); lowest RPE for action accuracy, **16 FPS** at 480×832, exploration to **20 seconds**.

- **[[2504.12369|WorldMem]]** — A ==token-level memory bank== with ==state-aware memory attention== (Plücker pose + timestamp embeddings) retrieved via ==FOV-overlap confidence scoring==, letting a conditional diffusion transformer persist objects/events across hundreds of frames; **PSNR 23.98** beyond context window (vs DF's severe collapse) on Minecraft + RealEstate10K.

#### 7.2 Composed & Multi-Component Memory Architectures

Two or more explicitly named memory sub-mechanisms fused into one system — multiple tiers, multiple experts, or a tokenizer paired with a separate retrieval mechanism.

- **[[2506.05284|Long-Term-Spatial-Memory-WM]]** — A memory-augmented video WM with three tiers (working frames, geometry-grounded ==3D point-cloud spatial memory== via ==TSDF fusion==, sparse episodic keyframes) on CogVideoX-5B for infinite-length consistent rollouts; **19.10 PSNR** view-recall vs 11.71–12.16 baselines, top VBench aesthetic/motion scores.

- **[[2605.18813|CoME]]** — ==Composition of Memory Experts== for diffusion world models: Short-Term/Long-Term (==LoRA test-time finetuned==)/Spatial-Long-Term memory experts fused via a ==Product of Contrastive Experts (PoCE)== that suppresses spurious modes; LPIPS **0.209→0.097** Memory Maze, RECON navigation ATE **1.13→0.96** vs NWM, at **60×** less compute than full-attention scaling.

- **[[2603.25716|HyDRA]]** — A ==Hybrid Memory== paradigm for dynamic video world models preserving both static-background consistency and dynamic-subject identity across out-of-view exit/re-entry, via a ==3D-convolution Memory Tokenizer== + ==Dynamic Retrieval Attention==, plus the HM-World (**59,225**-clip) benchmark; **PSNR 20.357** / **DSC 0.849**, beating commercial WorldPlay zero-shot.

#### 7.3 Diagnostic Studies & Benchmarks

Papers whose contribution is measuring memory mechanisms in general, not proposing a new one.

- **[[2606.09803|Echo-Memory]]** — A controlled study of ==memory in action world models== that fixes the video DiT backbone and sweeps four memory families (Context, Compression, Spatial, State-Space) under a three-branch replay/in-domain/open-domain protocol; block-wise State-Space recurrence tops open-domain VLM score at **69.00** vs raw Context **58.63** and Spatial max **17.12**.

- **[[2602.08025|MIND-Bench]]** — The first open-domain closed-loop ==revisited benchmark== isolating ==memory consistency== (temporal stability + contextual coherence) and ==action control== (accuracy + motion-scale generalization), built from **250** UE5 1080p videos over 8 scenes + an autoregressive MIND-World baseline; action accuracy deteriorates even with memory and in-domain actions.

**Generative World-Model Memory — Decision Matrix**

| Need | Recommendation |
|---|---|
| The reference token-level memory-bank design | [[2504.12369\|WorldMem]] |
| Isolate which memory family (Context/Compression/Spatial/State-Space) actually helps | [[2606.09803\|Echo-Memory]] |
| A benchmark that separates memory consistency from action control | [[2602.08025\|MIND-Bench]] |
| Real-time causal rollout with bounded memory compression | [[2512.04040\|RELIC]] (**16 FPS**) |
| Full generative-WAM memory landscape (~39 papers) | [[06_WAM#2.6 Neural Game Engines & Persistent Simulation]] |

^dm-7

> [!star] Key Papers — Generative-Memory Landmarks
> - [[2504.12369|WorldMem]] — the first token-level memory bank with state-aware attention for long-horizon diffusion-transformer persistence; the reference design nearly every later paper here compares against.
> - [[2606.09803|Echo-Memory]] — the field's first controlled ablation isolating *which* memory mechanism (not just *that* memory helps) drives consistency gains.
> - [[2602.08025|MIND-Bench]] — the first benchmark to separate memory consistency from action control as independently measurable axes, rather than conflating them into one success rate.

^key-papers-7

> [!tip] Same Word, Different Problem — Do Not Conflate
> "Memory" in a generative world model means *pixel persistence across a rollout*; "memory" everywhere else in this file means *information a decision-maker recalls to act correctly*. The two only interact where a WAM's imagined rollout feeds back into policy training — and even there, a visually-consistent hallucination and a behaviorally-correct recall are separate properties that can each hold without the other. See [[06_WAM#2.6 Neural Game Engines & Persistent Simulation]] for the full generative-memory landscape this section deliberately does not duplicate.

^insight-7

### 8. Memory Benchmarks & Diagnostics

Every mechanism above needs a way to prove it actually uses memory rather than getting lucky on tasks that don't require it. This section carries no L3 bullets of its own — it is a pointer to where the vault's memory-specific benchmarks already live, since duplicating five fully-described benchmark bullets here would just be a second, staler copy of [[02_Dataset-Benchmark-Environment#5.3 Memory-Specific Benchmarks]].

The common design pattern across all of them: construct a task where success is *provably* impossible without carrying information across a gap — an occlusion, a delay, a change of view — then score a memory-equipped policy against a memory-free or full-history baseline to confirm the axis is real, not an artifact of the benchmark.

**Memory Benchmarks & Diagnostics — Decision Matrix**

| Need | Recommendation |
|---|---|
| Comprehensive sim + real memory-failure benchmark | [[2605.10921\|RoboMemArena]] (**26 sim + 5 real** tasks, **68.9%** memory-dependent) |
| Spatial memory staleness (stored claim still true, not just present) | [[2608.04574\|SpatialSTALE]] |
| Persistence across consecutive questions, not per-episode reset | [[2607.21571\|Sequential-EQA]] (only 3D-Mem shows a real gain) |
| VQ-VAE proprioceptive memory over a non-Markovian unlocking suite | [[2603.09513\|VQ-Memory]] (**+31.3pp** avg SR) |
| Decompose *which* memory type (temporal/spatial/object/procedural) a policy lacks | [[2603.04639\|RoboMME]] (**16** long-horizon tasks) |
| Dual-arm benchmark graded by Task Memory Complexity | [[2603.01229\|RMBench]] (**9** tasks, Mem-0 baseline) |
| Memory-RL benchmark unifying Object/Spatial/Sequential/Capacity | [[2502.10550\|MIKASA]] (**32** memory-intensive tasks) |
| One dimension of a broader sim-and-real capability suite | [[2607.04434\|RoboDojo]] (Memory is 1 of 5 dimensions) |

^dm-8

> [!star] Key Papers — Memory-Isolation Benchmarks
> - [[2605.10921|RoboMemArena]] — the first comprehensive robotic-memory benchmark spanning both simulation and real hardware; the closest thing this axis has to a standard suite.
> - [[2603.04639|RoboMME]] — the only benchmark that decomposes *which kind* of memory (temporal, spatial, object, procedural) a policy is missing, rather than reporting one aggregate score.
> - [[2502.10550|MIKASA]] — the clearest demonstration that standard RL baselines (PPO-LSTM, SAC, TD-MPC2) collapse to near-zero on memory-intensive tasks that full-state PPO solves trivially, isolating memory as the limiting factor rather than a confound.

^key-papers-8

> [!tip] A Benchmark Is Only a Memory Benchmark If Memory-Free Fails
> The design invariant across all seven dedicated suites is the same: pair every memory-dependent task with a memory-free or full-history baseline that provably cannot solve it, so a claimed "memory" gain is not just a harder task in disguise — [[2502.10550|MIKASA]]'s PPO-MLP-vs-PPO-LSTM collapse and [[2603.01229|RMBench]]'s ACT-scores-zero real-world result are the cleanest examples of this discipline. A newer, sharper failure mode two 2026-07/08 papers isolate: even a memory-equipped policy fails if what it stored has gone *stale* rather than merely thin — [[2608.04574|SpatialSTALE]] measures this directly, and §3.1's [[2607.23797|VLMM]] treats re-observation scheduling as the fix, not just diagnosis. See [[02_Dataset-Benchmark-Environment#5.3 Memory-Specific Benchmarks]] for the full benchmark descriptions this section points at rather than duplicates.

^insight-8

## Quick-Reference Matrix

| Question | Answer |
|---|---|
| My policy can't tell two visually-identical moments apart — what do I need? | Episodic memory (§1) — [[2603.24576\|Chameleon]] or [[2501.18564\|SAM2Act]] |
| An object left the frame and I need to remember where it was | Object permanence (§2.1) — [[2503.05189\|Persistent-Object-Gaussian-Splat]] |
| I need a map that survives a whole mission, not just a few steps | Persistent spatial memory (§3.1) — [[2411.17735\|3D-Mem]] or [[2412.14480\|GraphEQA]] |
| I want memory as tokens inside my VLA, no external map | Backbone-native memory (§3.2) — [[2510.00695\|HAMLET]] |
| My policy needs to know which phase of the task it's in | Progress-aware control (§4) — [[2508.19958\|Long-VLA]] |
| An LLM/VLM needs a persistent store to plan or answer questions | Memory-augmented reasoning (§5) — [[2508.01415\|RoboMemory]] |
| I want my agent to improve after deployment without full retraining | Memory-driven self-evolution (§6) — [[2305.16291\|Voyager]] or [[2501.10395\|t-DGR]] |
| My video world model forgets objects that leave and re-enter frame | Generative-WM memory (§7) — [[2504.12369\|WorldMem]], or the full landscape at [[06_WAM#2.6 Neural Game Engines & Persistent Simulation]] |
| I need to prove my policy actually uses memory, not just get lucky | Memory benchmarks (§8) — [[2605.10921\|RoboMemArena]] or [[2502.10550\|MIKASA]] |
| Spatial persistence vs temporal/episodic memory — which do I need? | Spatial (§3) is viewpoint-invariant and SLAM-adjacent; episodic (§1) is order-sensitive and decays — see the design-risk note in the Overview |

## Cross-References

- [[10_Manipulation-Skill-Learning]] — the manipulation-side source for §1.3's episodic/compression memory and §2's object-permanence policies.
- [[03_Imitation-Learning-and-RL]] — cites §1.3's [[2104.10218|Episodic-Memory-Manipulation]], [[2606.12372|UniIntervene]], and [[2605.14810|CaMeRL]] as memory-guided answers to non-Markovian BC/RL, and §6.2's [[2501.10395|t-DGR]] as the generative-replay fix to model staleness.
- [[13_Navigation-and-Mobile-Manipulation]] — the navigation-side source for §1.1, §1.2, and §3.1's semantic-map subset.
- [[11_Contact-Rich-and-Tactile-Control]] — cites §1.3's [[2508.19236|MemoryVLA]] dual-memory bank for cross-domain (force-history) memory context.
- [[14_Egocentric-Pretraining-and-Human-Video]] — cites §1.3's [[2602.04600|Act-Sense-Act]] Dual-Track Memory as the non-Markovian complement to hand-to-gripper transfer mechanisms.
- [[04_VLA]] — the source for §3.2's backbone-native memory and §4's progress-aware/hindsight control.
- [[05_VLA-Reasoning-and-CoT]] — the source for §5's memory-augmented reasoning; see also its four reasoning-insertion-slot framing.
- [[06_WAM#2.6 Neural Game Engines & Persistent Simulation]] — the full ~39-paper generative-memory landscape §7 curates eight landmarks from.
- [[07_Latent-World-Models]] — ESWM (§1.3) and HERA (§2.1) sit at the JEPA/latent-world-model boundary of robot memory.
- [[12_Whole-Body-and-Locomotion-Control]] — humanoid-specific memory (INTENTION, POT-VLA, EgoMI, Spatial-Brain-Cerebellum) scattered across §1, §2, and §3.
- [[16_Self-Evolving-VLA-WAM]] — the source for §6's memory-driven self-evolution and the umbrella self-evolution framework §6's tip references.
- [[02_Dataset-Benchmark-Environment]] — the canonical home for §8's memory-specific benchmarks; this file only points at them.
- [[15_Sim-to-Real-Transfer]] — RoboDojo's Memory dimension, referenced in §8, sits inside its broader sim-and-real capability suite.

---
*See [[06_WAM#2.6 Neural Game Engines & Persistent Simulation]] for the adjacent generative-memory landscape, [[10_Manipulation-Skill-Learning]] for where episodic memory research started for this vault, or [[01_Embodied-AI-101]] to start from the basics.*

