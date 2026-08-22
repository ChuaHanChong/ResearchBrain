---
title: "Vision-Language-Action Models — Deep Dive"
tags:
  - VLA
  - robotics
  - foundation-model
  - manipulation
aliases:
  - "VLA Deep Dive"
  - "VLA Survey"
---

# Vision-Language-Action Models — Deep Dive

> [!abstract] Overview
> VLAs inherit robust multi-modal representations from pre-trained VLMs, giving robots semantic generalization that model-free and model-based approaches lack. From [[2212.06817|RT-1]]'s proof-of-concept (2022) to [[2504.16054|π0.5]]'s open-world household deployment (2025), VLAs have evolved from single-task imitation to general-purpose robot policies. This note maps the full VLA landscape: design principles, efficiency frontiers, spatial reasoning, world-model augmentation, RL post-training, multi-sensor integration, and failure modes.

## Evolution Graph

From Transformer-as-policy to flow-matching generalists — each step solved a specific bottleneck.

```text
1. Generalist Backbones   (one policy for many tasks)
· scaling the policy
                      +transformer policy    +web knowledge
┌────────────────┐    ╔═════════════════╗    ┌─────────────┐
│ CLIPort (2021) │───►║ RT-1 (2022)     ║───►│ RT-2 (2023) │─┐
└────────────────┘    ╚═════════════════╝    └─────────────┘ │
                                                             │    +open weights
                                                             │    ┌────────────────┐
                                                             ├───►│ OpenVLA (2024) │
                                                             │    └────────────────┘
                                                             │    +flow matching    +open-world
                                                             │    ┌────────────┐    ┌─────────────┐
                                                             └───►│ π0 (2024)  │───►│ π0.5 (2025) │
                                                                  └────────────┘    └─────────────┘

· generalist frontier
                     +scaled data
┌───────────────┐    ╔═════════════╗
│ CogACT (2024) │───►║ GR-3 (2025) ║─┐
└───────────────┘    ╚═════════════╝ │
                                     │    +interleaved
                                     │    ┌─────────────┐
                                     ├───►│ EO-1 (2025) │
                                     │    └─────────────┘
                                     │    +production scale
                                     │    ┌────────────────────┐
                                     └───►│ LingBot-VLA (2026) │
                                          └────────────────────┘

2. Efficiency   (making VLAs run on real robots)
· compression & speed
                      +action tokenizer    +small backbone
┌────────────────┐    ╔═══════════════╗    ┌────────────────┐
│ TinyVLA (2024) │───►║ FAST (2025)   ║───►│ SmolVLA (2025) │─┐
└────────────────┘    ╚═══════┬═══════╝    └────────────────┘ │
                              └──► π0 (2024)  [Generalist Backbones, above]  tokenizer adopted by π0
                                                              │    +adapter tuning           +edge deploy
                                                              │    ┌────────────────────┐    ┌──────────────┐
                                                              └───►│ VLA-Adapter (2025) │───►│ Evo-1 (2025) │
                                                                   └────────────────────┘    └──────────────┘

3. Spatial Grounding   (giving the policy 3D sense)
· 3D representation
                     +spatial tokens          +point clouds
╔═══════════════╗    ┌───────────────────┐    ┌─────────────────┐
║ 3D-VLA (2024) ║───►│ SpatialVLA (2025) │───►│ PointVLA (2025) │
╚═══════════════╝    └─────────┬─────────┘    └─────────────────┘
                               │    +2D-3D bridge
                               │    ┌──────────────────┐
                               └───►│ BridgeVLA (2025) │
                                    └──────────────────┘

4. Reasoning   (thinking before acting)
· chain-of-thought action
                      +latent plan
╔════════════════╗    ┌─────────────────┐
║ CoT-VLA (2025) ║───►│ ThinkAct (2025) │─┐
╚════════════════╝    └─────────────────┘ │
                                          │    +system-2 value
                                          │    ┌─────────────┐
                                          ├───►│ Hume (2025) │
                                          │    └─────────────┘
                                          │    +instruction tuning       +RL reasoning
                                          │    ┌────────────────────┐    ┌───────────────┐
                                          └───►│ InstructVLA (2025) │───►│ VLA-R1 (2025) │
                                               └────────────────────┘    └───────────────┘

5. World Models   (predicting the consequence of acting)
· predictive VLA
                     +latent dynamics      +dream rollouts
┌───────────────┐    ┌────────────────┐    ╔═════════════════╗
│ UP-VLA (2025) │───►│ LaDi-WM (2025) │───►║ DreamVLA (2025) ║─┐
└───────────────┘    └────────────────┘    ╚═════════════════╝ │
                                                               │    +foresight
                                                               │    ┌───────────┐
                                                               ├───►│ F1 (2025) │
                                                               │    └───────────┘
                                                               │    +JEPA objective
                                                               │    ┌─────────────────┐
                                                               └───►│ VLA-JEPA (2026) │
                                                                    └─────────────────┘

6. RL Post-Training   (past the demo ceiling)
· RL fine-tuning
                    +consistency RFT     +online RL
┌──────────────┐    ┌───────────────┐    ╔═══════════════╗
│ GRAPE (2024) │───►│ ConRFT (2025) │───►║ VLA-RL (2025) ║─┐
└──────────────┘    └───────────────┘    ╚═══════════════╝ │
                                                           │    +simple recipe
                                                           │    ┌─────────────────────┐
                                                           ├───►│ SimpleVLA-RL (2025) │
                                                           │    └─────────────────────┘
                                                           │    +verified reward
                                                           │    ┌────────────────┐
                                                           └───►│ VLA-RFT (2025) │
                                                                └────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

Six lanes, each a different pressure on the same object. Generalist backbones run from [[2109.12098|CLIPort]] to [[2504.16054|π0.5]], with [[2307.15818|RT-2]] forking into [[2406.09246|OpenVLA]]'s open weights and [[2410.24164|π0]]'s flow-matching action expert. The other five lanes are what happens once a backbone exists: making it cheap ([[2501.09747|FAST]], [[2506.01844|SmolVLA]]), giving it 3D sense ([[2501.15830|SpatialVLA]]), making it reason ([[2503.22020|CoT-VLA]]), letting it predict ([[2507.04447|DreamVLA]]), and pushing it past its demonstrations with RL ([[2505.18719|VLA-RL]]). Efficiency feeds back — [[2410.24164|π0]] adopted [[2501.09747|FAST]]'s action tokenizer.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2021 | [[2109.12098\|CLIPort]] | Backbone · Scaling | A two-stream architecture fusing a frozen CLIP semantic stream with an untrained Transporter spatial stream via lateral |
| 2022 | [[2212.06817\|RT-1]] | Backbone · Scaling | The **Robotics Transformer 1 (RT-1)** is a 35M parameter Transformer-based policy that takes image sequences and natural |
| 2023 | [[2307.15818\|RT-2]] | Backbone · Scaling | Google DeepMind's **RT-2** introduces Vision-Language-Action (VLA) models |
| 2024 | [[2403.09631\|3D-VLA]] | Spatial Grounding | A generative VLA pairing a 3D vision encoder + LLM backbone with interaction tokens over RGBD/point-cloud/bbox + a large 3D |
| 2024 | [[2406.09246\|OpenVLA]] | Backbone · Scaling | Develops and releases **OpenVLA**, a 7B-parameter |
| 2024 | [[2409.12514\|TinyVLA]] | Efficiency | A compact pre-trained VLM (70M–1.4B) + LoRA fine-tuning + Diffusion Policy action head |
| 2024 | [[2410.24164\|π0]] | Backbone · Scaling | Developed **π0**, integrating a pre-trained PaliGemma VLM backbone with a novel action expert based on conditional flow |
| 2024 | [[2411.19309\|GRAPE]] | RL Post-Training | A Trajectory-wise Preference Optimization + Guided-Cost Preference Generation that auto-synthesizes preference data |
| 2024 | [[2411.19650\|CogACT]] | Backbone · Generalist | A componentized architecture separating cognition from action via distinct vision/language/action modules + a specialized |
| 2025 | [[2501.09747\|FAST]] | Efficiency | A DCT+Huffman action tokenization scheme exploiting that adjacent action timesteps are highly correlated |
| 2025 | [[2501.15830\|SpatialVLA]] | Spatial Grounding | A spatial VLA whose Ego3D Position Encoding injects depth + egocentric 3D pixel positions + Adaptive Action Grids |
| 2025 | [[2501.18867\|UP-VLA]] | World Model | A unified autoregressive VLA (Phi-1.5) fusing continuous-encoder understanding + discrete-encoder future prediction + action |
| 2025 | [[2502.05450\|ConRFT]] | RL Post-Training | A two-stage reinforced fine-tuning on a lightweight Consistency Policy head: offline Cal-ConRFT (BC + Cal-QL) initializes |
| 2025 | [[2503.07511\|PointVLA]] | Spatial Grounding | A modular framework injecting hierarchical point-cloud 3D features into specific blocks of a frozen pretrained 2D VLA |
| 2025 | [[2503.22020\|CoT-VLA]] | Reasoning | A **7B** VILA-U unified multimodal VLA that predicts a future-frame token as a visual subgoal *first* |
| 2025 | [[2504.16054\|π0.5]] | Backbone · Scaling | **π0.5** employs a co-training framework that leverages multiple data types including mobile manipulator data |
| 2025 | [[2505.11528\|LaDi-WM]] | World Model | A latent diffusion WM with DINOv2 + SigLIP + imagination-guided iterative action refinement |
| 2025 | [[2505.18719\|VLA-RL]] | RL Post-Training | A framework formulating manipulation as multi-modal multi-turn conversation + trajectory-level RL + vision-language robotic |
| 2025 | [[2505.21432\|Hume]] | Reasoning | A dual-system VLA enabling value-guided System-2 thinking: the VLM denoises multiple action candidates and a value-query |
| 2025 | [[2506.01844\|SmolVLA]] | Efficiency | A distilled small VLA that compresses a 7B VLA into 450M params with only ~2% accuracy loss; **7x** less memory |
| 2025 | [[2506.07961\|BridgeVLA]] | Spatial Grounding | A VLA that projects 3D point clouds into 2D orthographic images so a PaliGemma backbone processes them natively |
| 2025 | [[2507.04447\|DreamVLA]] | World Model | A VLA that forecasts compact dynamic regions + depth + semantic features via block-wise structured attention + disentangled |
| 2025 | [[2507.15493\|GR-3]] | Backbone · Generalist | An end-to-end Mixture-of-Transformers generalist (pre-trained VLM + Action Diffusion Transformer) trained with a multi-stage |
| 2025 | [[2507.16815\|ThinkAct]] | Reasoning | A dual-system framework for reinforced visual latent planning where a slow-thinking MLLM |
| 2025 | [[2507.17520\|InstructVLA]] | Reasoning | An instruction-tuned VLA on Eagle2-2B with MoE adaptation dynamically switching between textual reasoning and latent action |
| 2025 | [[2508.21112\|EO-1]] | Backbone · Generalist | A unified decoder-only transformer (Qwen2.5-VL init) with interleaved vision-text-action pretraining |
| 2025 | [[2509.06951\|F1]] | World Model | A Mixture-of-Transformer with Understanding/Generation/Action experts + goal-conditioned visual foresight reframing action |
| 2025 | [[2509.09372\|VLA-Adapter]] | Efficiency | A Bridge Attention adapter with learnable injection ratio that fuses all-layer raw VLM features + all-layer ActionQuery |
| 2025 | [[2509.09674\|SimpleVLA-RL]] | RL Post-Training | A method extending veRL with GRPO + sparse binary outcome reward for online VLA RL; **91% → 99.1%** LIBERO |
| 2025 | [[2510.00406\|VLA-RFT]] | RL Post-Training | A world-model simulator that fine-tunes flow-matching VLAs via Generalized RPO with dense WM feedback |
| 2025 | [[2510.01623\|VLA-R1]] | Reasoning | A VLA-CoT data engine (13K auto CoT annotations aligned with affordance+trajectory) + SFT-then-RLVR |
| 2025 | [[2511.04555\|Evo-1]] | Efficiency | A lightweight VLA on an InternVL3-1B backbone + cross-modulated flow-matching DiT (stacked cross-attention only) |
| 2026 | [[2601.18692\|LingBot-VLA]] | Backbone · Generalist | A Mixture-of-Transformers (Qwen2.5-VL semantic backbone + Flow Matching) |
| 2026 | [[2602.10098\|VLA-JEPA]] | World Model | A full Vision-Language-Action stack pairing the JEPA principle with a flow-matching action head |

> [!tip] Three Evolutionary Phases
> **Phase 1 — Proof of concept** (2022-2023): [[2212.06817|RT-1]] proved Transformers work, [[2307.15818|RT-2]] showed VLM knowledge transfers, [[2310.08864|OXE]] built the cross-embodiment data foundation. **Phase 2 — Democratization** (2024): [[2406.09246|OpenVLA]] and [[2405.12213|Octo]] opened weights/code, [[2410.24164|π0]] introduced flow matching for continuous control. **Phase 3 — Specialization** (2025+): The field split — generalists scaled up ([[2504.16054|π0.5]] → [[2604.15483|π0.7]], Gemini, [[2604.20100|JoyAI-RA]]), efficient variants scaled down ([[2501.09747|FAST]], [[2506.01844|SmolVLA]]), WAMs added world prediction ([[2602.15922|DreamZero]]), and egocentric pretraining emerged as a fourth branch ([[2507.15597|Being-H0]], [[2602.16710|EgoScale]], [[2504.16054|π0.5]]+ego). See [[14_Egocentric-Pretraining-and-Human-Video#3. Scaling Laws for Egocentric Pretraining]] for the egocentric scaling story and [[05_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] for reasoning-augmented variants.

---

## Part A — Design Space & Architectural Axes

*Foundations + the four axes along which VLAs vary: efficiency, spatial grounding, reasoning, world-model integration.*

### 1. Design-Space Principles

Based on [[2412.14058|RoboVLMs]]' 600+ experiments — the most systematic VLA design-space study to date.

> [!success] Ideal VLA Recipe (from [[2412.14058|RoboVLMs]])
> ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions== + ==MoE== + ==Post-training on in-domain data==

#### 1.1 Backbone Selection

| Category | Models | Finding |
|----------|--------|---------|
| ==Encoder-Decoder== | Flamingo family | Outperformed by decoder-only |
| ==Decoder-Only== | LLaVA, Qwen-VL, MoonDream, [[2407.07726\|PaliGemma]], KosMos | KosMos and [[2407.07726\|PaliGemma]] are distinctly superior |

**Why these two win**: These two architectures underwent the most extensive ==vision-language pre-training== on large-scale datasets (KosMos: 1.8B image-text pairs; [[2407.07726|PaliGemma]]: WebLI-filtered). This creates stronger alignment between visual and linguistic features — critical for understanding complex spatial instructions like "pick up the red cup to the left of the blue bowl." ==Encoder-decoder== architectures (Flamingo) underperform because they split visual and language processing into separate streams that only interact through ==cross-attention==, while ==decoder-only== models (LLaVA) process both modalities in a unified sequence but lack the scale of pre-training that KosMos and [[2407.07726|PaliGemma]] received.

- **[[2109.12098|CLIPort]]** — A ==two-stream architecture== fusing a frozen ==CLIP== semantic stream with an untrained ==Transporter== spatial stream via lateral connections, predicting dense pixel-wise pick/place affordances; **>80%** SR on 10 tasks with 100 demos, real Franka deployment — the historical precedent for VLM + spatial-precision fusion.

#### 1.2 Architecture Axes

**Action Space**: ==Continuous== (recommended) — avoids compounding ==discretization errors== that plague tokenized approaches. When you discretize a 7-DoF arm into 256 bins per dimension, you get $256^7 \approx 72$ quadrillion possible actions — most of which are physically impossible. [[2510.13054|VLA-0]] showed that even representing actions as plain text numbers works, because the VLM's tokenizer already handles numerical sequences — no custom action head needed. ==Flow matching== ([[2410.24164|π0]]) goes further: it models the action distribution as a continuous flow, enabling smooth, multi-modal action generation that captures the full diversity of valid solutions rather than collapsing to a single mode. [[2605.04678|Pixels-to-Tokens-VLA]] systematically compares latent-action supervision strategies on Qwen3-VL-2B and finds the opposite for *learned* tokens: discrete latent-action token supervision (LA-Tok) beats continuous regression by **+2.2-2.7%** average, with image-based latents helping long-horizon [[2306.03310|LIBERO]]-Long (+8.4-10.8 pp) and action-based latents helping motorically complex [[2506.18088|RoboTwin-2.0]] (+17.5%) — discretization hurts when applied to *raw* joint angles, but helps when applied to a learned latent-action codebook.

**History Fusion**: ==Policy Head== (best balance) — VLM provides per-step features; separate head fuses history. [[2506.19816|CronusVLA]] extends this to multi-frame observations for temporal robustness. For truly long-horizon tasks requiring memory over minutes, [[2603.03596|MEM]] factorizes memory into ==dense short-term visual== (space-time separable attention over seconds) + ==compressed long-term language== (LLM summaries), enabling tasks requiring up to 15 minutes of memory. [[2603.12942|ReMem-VLA]] takes a different approach via ==dual-level recurrent queries== (frame-level EMA + chunk-level EMA) with gradient-free updates, hitting **94.5%** on memory-dependent simulation tasks.

**Training Loss**: ==Flow Matching== and ==MSE+BCE== achieve similar results. [[2602.18224|SimVLA]] confirmed this with a streamlined 0.5B model achieving 98.6% on [[2306.03310|LIBERO]].

- **[[2608.03052|Proprioceptive State Integration Study]]** — A controlled empirical study on π0.5 sweeping ==state representation (discrete vs continuous)==, ==history length (1–96 frames)==, and ==injection site (VLM-side vs action-side)==; an 8-frame history consistently helps, single-frame state best on VLM-side and multi-frame history on the action head, **+10.8pp** composite-task SR.
- **[[2608.01265|HERMITE-VLA]]** — Embeds a fixed ==Hermite trajectory operator== as a smooth-continuous prior over action chunks, with its `Reg` variant applying it as a ==training-time-only regularizer== discarded at inference; **98.7%** LIBERO (vs π0.5's 95.9%), **90.0%** real-world SR (vs 63.4%), **0.48×** replanning-seam discontinuity.
- **[[2607.20771|MoE-VLA]]** — A ==Mixture-of-Experts action head== replacing decoder FFN sublayers, with experts as ==LoRA deltas== over base weights and ==whole-forward-pass routing== under a ==load-balancing loss==; phase-level skills emerge (transport vs release-and-retract), **35–45%** cross-task activation at LIBERO parity with dense baselines.
- **[[2605.20856|DISC]]** — A ==two-stage hypernetwork== that generates a lightweight task-specific policy's *entire parameter set* from language alone, so the policy sees only vision — structurally preventing ==observation leakage==; **94.3%** LIBERO-90 (**+7.7pp** over OTTER), strong few-shot adaptation.
- **[[2603.10126|AR-VLA]]** — A standalone ==Autoregressive Action Expert== maintaining continuous causal history via a ==Hybrid KV Cache== + ==Dynamic Temporal Re-anchoring== that bridges asynchronous VLM staleness, replacing action-chunking with a persistent action stream; **61.5%** SimplerEnv avg (beats CogACT **52.1%**, π0.5 **51.0%**), stable **29ms** control despite 70ms VLM perception.
- **[[2505.03912|OpenHelix]]** — An open-source ==dual-system VLA== pairing a frozen MLLM (prompt-tuned) with a lightweight action generator, adding ==auxiliary multimodal-reasoning tasks==, distilled from a systematic empirical analysis of dual-system designs; improves language-instruction generalization and dynamic-object robustness with a standardized open evaluation framework.
- **[[2312.14457|QUAR-VLA]]** — A unified ==Vision-Language-Action== paradigm for quadrupeds defining an 11-D action space (velocities/gait/height) discretized to 256 bins, the **QUART** decoder-only transformer over a pre-trained MLLM, and the 259K-episode QUARD dataset; **0.66** Distinguish-Letter SR, emergent novel-instruction generalization, sim-to-real Go-to 3/20 → 13/20 via co-training.
- **[[2605.22671|BehaviorVLA]]** — A ==Mamba causal three-stream== Visuomotor Behavior Encoder that distills demos into time-invariant prototypes + phase states, paired with a Phase-conditioned decoder; **98%** LIBERO, **58%** RoboTwin 2.0 Hard (+37.7% over RDT), **70%** real bimanual generalization.
- **[[2510.01711|CRR-VLA]]** — A ==Robot State-aware Contrastive Loss (RS-CL)== that aligns VLM representations with proprioceptive states using continuous proprioceptive distances as soft contrastive labels, plus a learnable summarization token + ==view cutoff== augmentation at low compute; **69.7%** RoboCasa-Kitchen SOTA, **+13.3pp** real (45.0→58.3%), beats TCN at 2.6× lower FLOPs.

#### 1.3 Data Strategy

| Strategy | Impact |
|----------|--------|
| **In-domain only** | Best for task-specific performance |
| **Cross-embodiment ([[2310.08864\|OXE]])** | Improves few-shot learning (+17.2% on CALVIN few-shot) |
| **==Post-training==** ([[2310.08864\|OXE]] → in-domain fine-tune) | Best overall — highest gains for high-frequency skills |

[[2602.18532|VLANeXt]] distills [[2412.14058|RoboVLMs]]'s design-space lessons into 12 empirically-validated "recipes" — expressive policy modules with meta queries, action chunking, continuous-action objectives (flow matching), strong VLM backbones with soft VLM-policy connections, multi-view inputs, VLM-integrated proprioception, and an auxiliary frequency-domain loss. The resulting 2.5B-parameter [[2602.18532|VLANeXt]] achieves **80.1%** average on [[2510.13626|LIBERO-Plus]], **+10pp** over OpenVLA-OFT (7B). One useful negative finding: temporal observation history is often *not* beneficial, and world modeling is effective but computationally expensive — informing the §5 efficiency arguments below.

- **[[2602.01067|LBM Co-training Study]]** — An 89-policy empirical study (**4,000 hr** robot/human data, **50M** VL samples) isolating co-training modalities for a fixed ActionFT VLA; vision-language + cross-embodiment data compose for **+45.3%** real-world language following, while discrete action tokens show **no** gain at scale and CoT conditioning doesn't help manipulation.
- **[[2604.20012|EmbodiedMidtrain]]** — A mid-training method quantifying the VLM↔VLA *data*-distribution gap (==Maximum Mean Discrepancy==); a ==data engine== scores VLM samples by proximity to the VLA distribution and mid-trains on the top-K closest. A **1.1B** InternVL3.5 surpasses expert VLA baselines **3–8×** larger across Calvin ABC-D, SimplerEnv Bridge, and LIBERO-10.

**Design-Space — Decision Matrix**

| Design axis | Recommendation (from [[2412.14058\|RoboVLMs]] / [[2602.18532\|VLANeXt]]) |
|---|---|
| Backbone family | Decoder-only KosMos / [[2407.07726\|PaliGemma]] (most VL pre-training → best instruction grounding) |
| Action space | ==Continuous== (avoids discretization errors); [[2410.24164\|π0]] flow matching for multi-modal actions |
| History fusion | ==Policy Head== (VLM features + separate fusion head); add memory ([[2603.03596\|MEM]], [[2603.12942\|ReMem-VLA]]) for >minute horizons |
| Training loss | Flow Matching ≈ MSE+BCE ([[2602.18224\|SimVLA]] confirms parity at 0.5B / 98.6% LIBERO) |
| Data strategy | ==Post-training== (cross-embodiment [[2310.08864\|OXE]] → in-domain fine-tune) beats either alone |
| Minimal-complexity baseline | [[2510.13054\|VLA-0]] (actions-as-text on an unmodified VLM — no custom head) |

^dm-1

#### 1.4 Latent-Action & Action-Tokenization Pretraining

Tokenizer/latent-action-model pretraining schemes that produce a discrete or continuous action codebook, learned prior to or independent of the downstream action-prediction loss. Latent-action models (LAMs) infer transition codes from action-free video; tokenizers compress continuous joints into discrete codes. The shared lesson — quantize a *learned* latent, not the raw joint stream (see §1's discretization-error note).

- **[[2608.10484|SALT]]** — Adds a ==language-alignment== term to a ==residual VQ-VAE== action tokenizer, regenerating instructions from quantized latents via a frozen LM to shape codebooks with verb semantics; **71.9%** SimplerEnv WidowX (vs **42.7%** VQ-VAE, **31.2%** FAST), **39.1** verb-probe macro-F1.
- **[[2608.03563|UVT]]** — Fuses low-level robot actions with a pretrained ==Latent Action Model's== discrete dynamics code into a shared 32-D ==Unified Visuomotor Target== via a ==Multimodal VAE==; **+16.2pp** LIBERO-Spatial / **+12.6pp** LIBERO-Long at just **10k** fine-tuning steps, LIBERO-Plus Spatial robustness **34.0%→81.5%**, real bimanual Lift Pot **38%→54%**.
- **[[2607.02466|TAP]]** — A two-stage ==Task-Agnostic Pretraining== framework: Stage 1 learns ==motor priors== via self-supervised ==Inverse Dynamics== on unlabeled/random-play data (no language), Stage 2 grounds them with minimal expert BC demos; **33.32%** SIMPLER Avg-All (vs OpenVLA **7.75%**), real **65%** SR under distractors (vs BC **5%**).
- **[[2606.12366|APT]]** — A ==Bayesian factorization== splitting the policy into a language-agnostic ==Vision-Action prior== and a language-conditioned likelihood, so stage 1 pretrains the ==action expert== on balanced vision-action pairs before language enters via ==layer-wise gated fusion==; **19%** LIBERO-PRO OOD (**27%** with VLM finetuning), **90%** vs π0.5's **20%** on chained instructions.
- **[[2603.01766|NIAF]]** — A ==Neural Implicit Action Field== reformulating actions as continuous time-functions via a ==SIREN== modulated by MLLM-predicted spectral coefficients, so velocity and jerk become ==analytically differentiable== and supervised; **4.66** CALVIN length, **97.9%** LIBERO, **90%/80%** real Item-Placement/Cup-Stacking — continuous functions replace discrete waypoints.
- **[[2602.08602|MINT]]** — A ==Spectrally Disentangled Action Tokenizer== decomposing action chunks into multi-scale tokens via ==DCT-domain spectral reconstruction==, coarse tokens capturing intent, with an ==intent-based action ensemble== at inference; **93.4%** LIBERO-Long, nearly 3x MetaWorld "Very Hard" SR at 4B, enables one-shot skill transfer via intent-token injection.
- **[[2509.19958|MotoVLA]]** — A two-stage VLA using ==dynamic 3D point clouds== (Grounding-DINO + SAM2 + BootsTAPIR + MoGE depth-lifting) as an embodiment-agnostic action representation, self-supervised on unlabeled human+robot video, then aligned to robot actions with few labels via ==flow matching==; **68.2%** SIMPLER (vs π0's 56.8%), zero-shot skill transfer from human video.
- **[[2505.06111|UniVLA]]** — A two-stage ==task-centric latent action== framework that uses ==DINOv2== + language conditioning to decouple task-relevant motion from environment noise on a Prismatic-7B VLM; **95.2%** LIBERO (+18.7pp over OpenVLA), **47.1%** R2R navigation, **81.7%** real AgileX. The foundational action-free-video latent-action pretrain.
- **[[2511.21428|LAPS]]** — A fully ==unsupervised pipeline== that turns continuous industrial video into action primitives via ==Latent Action Energy== boundary detection + frozen-encoder k-means clustering; GTEA F1@5s **73.12**, industrial exocentric F1@5s **84.75**, ICSS **0.926** — discovers the action vocabulary upstream of segmentation.
- **[[2507.23682|villa-X]]** — A latent-action model with a proprioceptive ==Forward Dynamics Model== auxiliary decoder + ==embodiment context vector== that forces latents onto physical dynamics; **77.7%** SIMPLER Google / **62.5%** WidowX, zero-shot to unseen Realman/XArm.
- **[[2601.04061|CLAP]]** — A ==Contrastive Latent Action Pretraining== framework that aligns human-video latents with a robot-derived quantized action space via dual ==CLAP-NTP== (reasoning) + ==CLAP-RF== (high-freq control); **91.0%** LIBERO (82% LIBERO-Long), **61.0%** real bimanual Astribot.
- **[[2605.13403|RotVLA]]** — A ==continuous rotational latent action== model representing each latent as an ==SO(n)== rotation matrix via ==SoftVQ== + SVD projection + ==triplet temporal-compositionality== to avoid discrete-quantization discontinuity; **98.2%** LIBERO, **89.6%** RoboTwin 2.0 bimanual.
- **[[2512.04952|FASTer]]** — A learnable ==FASTerVQ== action tokenizer (==Action Patchifier== + Transformer-based ==Residual VQ==) that resolves the compression-vs-reconstruction trade-off of DCT tokenization; **97.9%** LIBERO, lowest OOD drop (**29%**) on VLABench, **87.9%** real Simpler-Bridge.
- **[[2511.02776|XR-1]]** — A versatile VLA learning ==Unified Vision-Motion Codes (UVMC)== via a dual-branch ==VQ-VAE== that jointly encodes visual dynamics and motion into a shared discrete latent with a cross-modal alignment loss, in a UVMC-guided pretrain pipeline; SOTA across 120+ tasks on **six** real embodiments, 20-shot to unseen Tien Kung 2.0, **+15%** ablation gain.
- **[[2507.01016|VQ-VLA]]** — A VLA that replaces simple action binning with a frozen convolutional residual ==VQ-VAE action tokenizer== scaled on **100×** more (real + synthetic) data so the VLM predicts chunked discrete action tokens; **80.98%** LIBERO-90 (+7.45 over OpenVLA), real long-horizon **15%→50%**, **11.84 Hz** (3× OpenVLA).
- **[[2602.21736|JALA]]** — A ==Jointly-Aligned Latent Actions== framework that aligns VLA-context predictive embeddings with inverse-dynamics latents (no pixel reconstruction) + ==UniHand-Mix== 7.5M lab + in-the-wild human videos; **96.9%** LIBERO Two-View / **92.3%** Single-View, robust to visual shift with human-only pretraining.
- **[[2601.15197|LangForce]]** — A ==Bayesian-decomposition== framework curing the VLA "vision shortcut" by maximizing conditional ==PMI== between action and instruction via a Log-Likelihood-Ratio objective over K=64 ==Latent Action Queries== (causal-masked dual branches, flow-matching); **66.5%** SimplerEnv (+11.3pp), **99.4%** LIBERO-Goal, preserves VLM reasoning at no inference overhead.
- **[[2602.10556|LAP]]** — A ==Language-Action Pre-training== method that parses continuous actions into structured natural-language tokens predicted autoregressively by PaliGemma-3B + knowledge-insulated diffusion head; **>50%** zero-shot across 3 unseen embodiments (**2×** prior), **2.5×** fewer demos to fine-tune.
- **[[2605.28634|PrimitiveVLA]]** — A ==primitive-centric disassemble-and-assemble== paradigm with 11 reusable motion primitives auto-extracted from task demos + VLM primitive planner; **+9.2%** OpenVLA on LIBERO-90, matches full-data at **50%** data, **6×** novel-task SR (to **45.5%**).
- **[[2605.24931|Latent-Action-Chunks]]** — A ==VAE==-based latent-action method that compresses high-frequency action chunks into a continuous low-frequency latent a policy predicts, plus a training-free ==Reuse-then-Refine== strategy for async-execution continuity; **−80%** Cartesian deviation (7.59→1.47mm OpenVLA-OFT), **−79%** chunk-overlap diff, **28%→74%** real Peel-Cucumber SR.
- **[[2503.01206|Action-Tokenizer-Matters-In-Context]]** — A ==Lipschitz-constrained VQ-VAE== (LipVQ-VAE) action tokenizer enforcing latent smoothness via encoder weight normalization, fed to an In-Context Robotic Transformer for ICIL; **0.530** RoboCasa (+5.3%), **0.617** ManiSkill (+6% over ACT+LFQ-VAE), best smoothness **0.63**, **12-14%** higher real Kinova Gen3 SR.

> [!star] Key Papers
> - [[2412.14058|RoboVLMs]] — The 600+-experiment design-space study that anchors every recommendation in this section
> - [[2602.18532|VLANeXt]] — Distills the design space into 12 validated recipes; 2.5B model beats 7B OpenVLA-OFT on [[2510.13626|LIBERO-Plus]]
> - [[2410.24164|π0]] — Flow-matching action head; the reference continuous-action generator
> - [[2510.13054|VLA-0]] — The minimalist counter-proof: actions-as-text on an unmodified VLM is competitive
> - [[2602.18224|SimVLA]] — Streamlined 0.5B model at 98.6% LIBERO; evidence that loss-function choice is second-order

^key-papers-1

> [!tip] The [[2510.13054|VLA-0]] Surprise
> [[2510.13054|VLA-0]] showed you don't need custom action heads, special tokenizers, or architectural changes at all — just fine-tune an unmodified VLM with actions as text. Sometimes the simplest approach wins. Cross-reference [[04_VLA#2.3 Architecture Reduction]] for the efficiency-side echo of this finding — [[2604.11757|StarVLA-alpha]]'s lightweight MLP action head reaches the same conclusion that complex action decoders are unnecessary when the VLM backbone is strong enough.

^insight-1

---

### 2. Efficient & Lightweight VLAs

Full-size VLAs (7B+) are impractical for real-time robot control because every step requires a forward pass through a multi-billion-parameter VLM. The efficiency frontier resolves this tension via four orthogonal axes — compress the action stream, distill the model, reduce the architecture, or eliminate the iterative denoising step entirely. Each strategy targets a different cost center, and they compose: e.g. a distilled small backbone with action-token compression and one-step flow stacks the savings.

#### 2.1 Compression & Tokenization

Reduce the *information* the VLA processes — token-level compression on both the visual stream and the action stream. Visual tokens are pruned, cached, or reused across frames; action chunks get frequency-domain or learned tokenization — both exploit heavy cross-timestep redundancy for near-lossless speedups.

- **[[2608.02197|AtVLA]]** — Inserts ==register tokens== into the vision encoder to absorb global information and rectify high-norm attention artifacts, then triggers ==uncertainty-gated attention-guided local refinement== (crop + re-encode) only when action uncertainty is high; **98.4%** LIBERO (vs π0's 94.2%), **69.0%** real-world (vs 46.5%), only **1.4-1.6×** inference cost.
- **[[2607.12287|Temporal Token Reuse]]** — A backbone-agnostic system-level accelerator recomputing only dynamic ==visual tokens== while caching static ones, plus a ==2-step== policy compressing multi-step ==flow matching== via ==low-rank velocity approximation== + a lightweight adaptor; **>2×** sim speedup (π0.5 **3.5 → 8.2 FPS**), **1.6×** real, **93.8%** LIBERO vs **94.4%** at 10 steps.
- **[[2606.30113|SA-VLA (State-Aware Tokenizer)]]** — A ==state-aware action tokenizer== injecting robot proprioceptive state into discrete action decoding via ==cross-attention== or a lightweight state-adapter MLP, curing the ==compression gap==; **56%** avg RoboTwin (**+23-40pp** over Binning/FAST/VQ-BET), **33%** real zero-shot AgileX (**+18-25pp**).
- **[[2606.21372|NAC]]** — A ==Neural Action Codec== adapting multi-scale ==RVQGAN== neural-audio-codec architecture to tokenize actions as multi-channel 1D signals, with kinematic-MSE loss + a ==DAC discriminator==; **49.73%** LIBERO-10 (**+5.56pp** over OAT), **50%** real across 8 tasks, only **12** tokens/chunk (vs FAST's 36).
- **[[2606.02735|S2-VLA]]** — A cleaner executor-conditioning interface combining ==Specify More== (hierarchical relabeling) + ==See Less== (==visual evidence budgeting== via learned gate heads); **94.0%/95.5%** on LIBERO-PRO goal/object and a real-robot jump from **54.2% → 79.0%** mean subtask success over π0.5.
- **[[2602.06575|ThinkProprio]]** — Promotes proprioception from passive conditioning to an *active query*: raw states become ==VLM-vocabulary tokens== fed early, then an ==embodied visual token selector== gates visual patches by language *and* state under a ==diversity regularization loss==; **4.52** CALVIN ABC→D chain length, **~88%** fewer visual tokens (100→**12**), latency **52→22 ms**.
- **[[2501.09747|FAST]]** — A ==DCT+Huffman action tokenization== scheme exploiting that adjacent action timesteps are highly correlated, so frequency-domain compression is nearly lossless; **5x** faster inference. The foundational efficiency-via-tokenization paper.
- **[[2604.03191|Compression-Gap]]** — An ==information-theoretic data-processing-inequality framework== that isolates fixed discrete codebooks as the binding bottleneck; Diffusion Policy gains **+26.0pp** (ResNet-18 → SigLIP) vs only **+10.4pp** for OAT discrete tokenization. A negative result motivating one-step flow.
- **[[2604.05323|VLA-InfoEntropy]]** — A training-free vision-token selection method ranking tokens by ==visual entropy== + ==attention entropy==, with ==timestep-conditioned dynamic selection== and ==KV-cache== reuse of low-information tokens; **1.53x** speedup (**−39.8%** latency, **−34.9%** FLOPs) at **76.4%** LIBERO (vs OpenVLA **75.0%**).
- **[[2509.22093|Action-Aware-VLA-Pruning]]** — A ==text-driven anticipatory pruning== of task-relevant visual tokens from an early layer + an ==action-aware dynamic strategy== gating pruning by end-effector motion magnitude; **1.35x** LIBERO speedup at **94.4–96.3%** SR, **1.49x** real Jaco2 (76.9→**51.8 ms**) with SR rising **85.8→88.3%**.
- **[[2506.12723|SP-VLA]]** — A joint ==action-type model scheduling== (full VLA for deliberative steps, Ridge-regression generator for intuitive steps) + ==spatio-semantic dual-aware token pruning== (cumulative attention + Canny contours); **1.5x** LIBERO / **2.4x** SimplerEnv speedup at **<3%** accuracy drop.
- **[[2506.10100|EfficientVLA]]** — A ==training-free== three-axis compression that prunes inconsequential language layers, selects task-aware diverse visual tokens, and statically caches diffusion-head features across denoising steps; **1.93x** speedup at **28.9%** FLOPs (**−0.6%** SR) on SIMPLER, **2.0x** on CogACT-Large.
- **[[2509.05614|SpecPrune-VLA]]** — A training-free two-level ==self-speculative visual-token pruning== combining action-level static pruning (global temporal context + patch-diff) with layer-level dynamic pruning (cumulative importance) gated by an ==action-aware controller==; **1.46×** (up to 1.57×) OpenVLA-OFT, **−57%** FLOPs, **<0.7%** SR drop, **1.70×** real.
- **[[2508.19257|TTF-VLA]]** — A training-free model-agnostic ==temporal token fusion== that reuses previous-frame visual tokens for static regions via ==dual-dimension detection== (grayscale pixel-diff + attention semantics) + keyframes; **+4.0pp** OpenVLA / **+2.7pp** VLA-Cache LIBERO, **+1.6pp** SimplerEnv, **+8.7%** rel real-world.
- **[[2502.02175|VLA-Cache]]** — A training-free inference accelerator that reuses ==KV representations== of visually-static tokens across frames (patch cosine-similarity + cross-attention task-relevance filter + entropy-guided layer-adaptive reuse); **1.63×** OpenVLA (**−27.3%** FLOPs, 0.3% SR drop), OpenVLA-OFT **65→79 Hz**.

#### 2.2 Distillation & Small Backbones

Compress the *model* — teacher's knowledge compresses because most VLA capacity models language understanding, not motor control.

- **[[2511.04555|Evo-1]]** (0.77B) — A lightweight VLA on an InternVL3-1B backbone + cross-modulated ==flow-matching== DiT (stacked cross-attention only) with a two-stage freeze-then-finetune recipe that preserves semantic alignment; **94.8%** LIBERO, **80.6%** Meta-World, **78%** real xArm6 at **16.4 Hz** on **2.3 GB**.
- **[[2506.01844|SmolVLA]]** (450M) — A distilled small VLA that compresses a 7B VLA into 450M params with only ~2% accuracy loss; **7x** less memory, **40%** faster training than [[2406.09246|OpenVLA]]. The canonical small-VLA baseline.
- **[[2509.09372|VLA-Adapter]]** (0.5B) — A ==Bridge Attention== adapter with ==learnable injection ratio== that fuses all-layer raw VLM features + all-layer ActionQuery; **97.3%** LIBERO without robotic pre-training, **219.2 Hz** inference (**3×** faster than OpenVLA-OFT) at **36.5 ms** latency; **4.42** avg task length on CALVIN ABC→D zero-shot.
- **[[2507.14049|EdgeVLA]]** — A small VLA pairing a ==Qwen2-0.5B SLM== + SigLIP/DINOv2 encoders with a ==non-autoregressive end-effector head== (causal mask removed so all action components emit at once); **5 ms** (**200 Hz**, **4×** over OpenVLA) at **4 GB** memory (**4×** smaller), **~7×** faster training — the SLM-plus-parallel-decode recipe.
- **[[2506.17639|RLRC]]** — A compression-recovery pipeline applying ==aggressive structured pruning== (up to 90% of the LLM) then ==SFT + PPO recovery== + optional 4-bit PTQ; **8.3×** memory cut (14.86→**1.77 GB**) + **2.3×** throughput while *surpassing* OpenVLA at **90.62%** ID / **62.50%** OOD, RL lifting OOD generalization **~30%**.
- **[[2409.12514|TinyVLA]]** — A compact pre-trained VLM (70M–1.4B) + ==LoRA fine-tuning== + ==Diffusion Policy action head==; **94.0%** real-world single-arm (vs **68.3%** OpenVLA), **44.5%** bimanual (vs **0%** OpenVLA), **20×** faster (**14 ms** vs **292 ms**) at **5.5×** fewer parameters — the early small-VLA recipe.

#### 2.3 Architecture Reduction

Replace expensive components with minimal ones — complex action decoders are unnecessary when the VLM backbone is strong enough.

- **[[2606.31382|Recovery-Free VLA Pruning]]** — Reframes ==VLA pruning== as a diagnostic probe via ==VLM-to-VLA parameter divergence== (relative ΔW), yielding a ==module-differentiated, recovery-free pruning scheme==; OpenVLA **7.5B→6.2B** params at **62.3%** SR (vs LLM-Pruner's **1.0%**), π0.5 to **5.6GB** at **89.0%** SR, no post-hoc fine-tuning.
- **[[2606.21470|ASCII]]** — Converts RGB frames into color-aware ==ASCII art== rasters so text-only LLMs serve as VLA controllers, trained via ==iterative DAgger== bootstrapped from A* expert demos; Qwen3-4B macro-SR **30.8%→89.2%**, Qwen3-8B (**80.4%**) edges Qwen3-VL-8B (**79.0%**), sim-to-real transfer — eliminates the vision encoder.
- **[[2606.20246|CLP]]** — A training-free ==CKA-guided Layer Pruning== that quantifies consecutive-layer similarity to statically remove redundant transformer "stagnant zones" before fine-tuning; up to **50%** depth cut on π0 and GR00T-N1.5 (**1.39–1.42×** fewer FLOPs, **1.94×** faster), GR00T-N1.5 real-world SR rising **73.5%→75.9%** — VLAs have removable depth redundancy.
- **[[2606.09572|CT-VAM]]** — A ==cerebello-thalamic==-inspired vision-action model decoupling high-level language grounding from high-frequency execution via a ==Thalamic Action Routing Stream== with stream-separated conditional attention + rectified-flow + ==Flow-Consistent Inpainting==; **82.1%** LIBERO at **68M** params, **90%** real on Jetson Orin NX at **20 Hz**.
- **[[2605.06175|VLA-GSE]]** — An SVD-initialized generalized+specialized expert PEFT method; **81.2%** zero-shot on [[2510.13626|LIBERO-Plus]], beating full fine-tuning by **+6.3pp** while preserving multimodal understanding.
- **[[2604.11757|StarVLA-alpha]]** — A ==lightweight MLP action head== on a strong ==pre-trained VLM backbone== with a ==minimal data pipeline== and a ==single generalist model== across embodiments; **98.8%** [[2306.03310|LIBERO]], **76.0%** SimplerEnv Google-VM, **33.6%** real RoboChallenge — continuous-action MLP matches complex action heads, proving complex action decoders are unnecessary.
- **[[2603.28740|FocusVLA]]** — A ==Modality Cascaded Attention== design (sequential action-latent/query/visual integration) + dual-level ==Focus Attention== pruning action-irrelevant patches; 0.5B beats 7B models at **98.7%** LIBERO, **58%/15%** RoboTwin 2.0 easy/hard.
- **[[2602.22896|DySL-VLA]]** — An efficient-inference VLA splitting layers into always-run ==static== vs skippable ==dynamic== layers (lightweight adapters approximate skips) gated by ==trajectory-continuity== importance + post-skip verification + skip-aware distillation; up to **3.75×** LLM speedup at **23.2 Hz** on Jetson Orin, **+41.3%** LIBERO SR over FlexiDepth.
- **[[2602.00780|Adaptive-VLA-Pruning]]** — A training-free ==Environment-aware Adaptive Pruning== (structured channel pruning whose sparsity updates from inter-frame visual similarity) + ==Interleaved Inference Orchestration== hiding overhead in action-expert "FLOPs bubbles"; **1.41×** OpenVLA-OFT at 40% prune (**2.8%** SR loss), **2.18×** with FastV — adapts to dynamic scenes.
- **[[2601.03309|VLM4VLA]]** — A ==minimalist adaptation== study integrating general-purpose VLMs into VLA policies with **<1%** added params via an MLP head + Huber-loss imitation across 24 VLMs; matches OpenVLA/π0 despite simplicity, and freezing the *vision* encoder (not language) is what hurts — locating the visual semantic gap.
- **[[2510.13054|VLA-0]]** — An unmodified ==Qwen-VL-2.5-3B== that emits actions as ==space-separated numerical text strings== via native text generation + ==masked action augmentation== + ==action ensembling==; **94.7%** LIBERO (rank **1.0** of non-pretrained), surpasses SmolVLA by **+12.5pp** on real SO-100 robot — the simplest-possible recipe.
- **[[2508.21046|CogVLA]]** — An ==instruction-driven routing + sparsification== framework: 3-stage EFA-Routing (visual aggregation) + LFP-Routing (LLM pruning) + coupled ==CAtten== with parallel action-chunk decoding; **97.4%** LIBERO, **70.0%** real ALOHA at **2.79x** faster inference, **3.12x** fewer FLOPs, **2.49x** lower training cost.
- **[[2503.20384|MoLe-VLA]]** — A dynamic ==Mixture-of-Layers== layer-skipping VLA that treats each LLM layer as an expert activated by a ==Spatial-Temporal Aware Router== + ==Cognitive self-Knowledge Distillation== to prevent cognitive collapse; **60.8%** RLBench (vs CogAct 57.2%) at **5.6×** less compute, OpenVLA **45.4→55.6%** at 50% layers, **70%** real Franka.
- **[[2406.04339|RoboMamba]]** — A ==Mamba state-space backbone== VLA (CLIP encoder + Mamba LLM + MLP pose head) replacing quadratic Transformer attention; two-stage align-then-manipulate training updates only a **0.1%** (**3.7M**) policy head; **7×** faster inference than LLaMA-AdapterV2/ManipLLM, **+7.0%** seen / **+2.0%** unseen SR — the SSM-backbone point in the efficiency design space.
- **[[2312.01990|SARA-RT]]** — A ==Self-Adaptive Robust Attention== method: ==linear attention== with ==learnable pre-processing matrices== plus an ==up-training== step converting pretrained quadratic-attention policies without retraining; constant-time inference (**~100ms** regardless of point-cloud size), **0.75** grasp SR (vs **0.64**), **14%** RT-2 speedup.

#### 2.4 One-Step & Parallel Decoding

Eliminate the iterative denoising / autoregressive bottleneck — the *amount* of refinement should be learned or skipped, not fixed.

- **[[2606.31132|ELASTIC]]** — A ==meta-MDP== learning a meta-policy to adaptively allocate test-time compute (sequential denoising strides + parallel sample pruning) via ==hybrid RL== (offline critic pretraining + online counterfactual rollouts); Pareto-dominates fixed scaling, matches Best-of-N on a real VLA while cutting latency **34%**.
- **[[2606.05737|One-Step-VLA]]** — A distillation-free ==noise-shift strategy== in ==conditional flow matching== that biases training toward high-noise states so one decode step learns an accurate velocity field for VLA's "rich-condition, compact-target" structure; one-step matches or beats 10-step at **95.6%** LIBERO-Long, validated on real bimanual π0.5.
- **[[2605.09948|LoopVLA]]** (1.2B) — A recurrent ==Loop Block== + learned sufficiency head that dynamically allocates depth per state; **−45%** params, **1.7x** throughput while maintaining [[2306.03310|LIBERO]] performance.
- **[[2605.08799|ElasticFlow]]** — A one-step ==average velocity field== policy + ==elastic time abstraction==; **14ms** inference at **71Hz**, **98.5%** [[2306.03310|LIBERO]], **5x** faster than [[2303.04137|Diffusion-Policy]] with smoother trajectories (Jerk **1.1×10⁻³** vs **3.2×10⁻³**).
- **[[2604.05672|A1]]** (7B) — A ==Molmo-7B backbone== + Qwen3 flow-matching head with ==budget-aware adaptive inference== (==multi-exit training== + action-consistency ==early-termination==) and ==Inter-Layer Truncated Flow Matching== (10→2 steps); **72.3%** latency reduction (**37.8s → 10.5s**) at **96.4%** LIBERO, plus **75.3%** LIBERO-Plus OOD (vs OpenVLA-OFT **69.6%**).
- **[[2604.05656|SnapFlow]]** — A ==progressive self-distillation== method with a ==corrected consistency objective== (marginal-velocity substitution) enabling single-step (1-NFE) action generation without architecture changes; **3.3x** faster [[2504.16054|π0.5]] (274ms→**83ms**) and **3.56x** faster SmolVLA, hitting **98.75%** LIBERO with 1-step vs the 10-step baseline's **97.75%**.
- **[[2604.04161|AAC]]** — A training-free ==inference-time== chunk-size selector from predictive uncertainty: ==action entropy== (==Gaussian differential entropy== for continuous + ==discrete entropy== for gripper) sampled over parallel candidates, picking the size where the entropy jump peaks; **+15%** real-world success (**67.0% → 82.0%**), **+2.3%** RoboCasa, **+4%** LIBERO-Long.
- **[[2604.02965|SV-VLA]]** — A ==speculative verification== scheme that decouples a heavy ==Macro-Planner== (long action chunks + a ==planning-context feature==) from a lightweight ==Verifier== which re-plans only when execution deviates past a threshold; **2.17x** speedup over closed-loop OpenVLA-OFT and **90.9%** LIBERO (**+11.4%** over open-loop chunking).
- **[[2603.26320|DFM-VLA]]** — A ==discrete flow matching== method for full-sequence action refinement that cures the "irreversible commitment" of AR/discrete-diffusion decoding via a two-stage ==stochastic-refine + greedy-validate== schedule with ==adaptive KV caching==; **4.44** CALVIN avg length, **95.7%** LIBERO, **70.8%** real bimanual (vs π0-FAST **42.5%**) at a **2.4×** speedup.
- **[[2602.20200|OptimusVLA]]** — A memory-conditioned denoising VLA that cuts NFE via a ==Global Prior Memory== (retrieves similar trajectories to adapt noise scale + NFE by retrieval confidence) + a Mamba ==Local Consistency Memory== injecting a temporal-coherence bias; **98.6%** LIBERO, NFE **10.0→3.2**, **2.9x** real / **6.5x** sim speedup.
- **[[2507.05116|VOTE]]** — A VLA compressing an action chunk into one special ==<ACT> token== read by a bottleneck MLP head + a ==trajectory ensemble voting== inference that aggregates historical predictions by cosine similarity; **up to 48.8×** A6000 / **38.6×** Jetson Orin speedup, **98.0%** LIBERO, <20% of OpenVLA-OFT's training samples.
- **[[2506.13725|CEED-VLA]]** — A ==consistency-distilled== VLA mapping any ==Jacobi-decoding== intermediate state to its fixed point in one step + ==mixed-label AR supervision== + ==early-exit decoding== skipping inefficient iterations; **4.1×** OpenVLA acceleration (225 Tokens/s) / **4.3×** frequency (**25.6 Hz**), real **13 Hz** at 75–80% dexterous SR.
- **[[2509.06932|LLaDA-VLA]]** — The first VLA built on a ==diffusion-based VLM== (d-VLM) with ==Localized Special-token Classification== (restricting the decode space to action tokens) + ==Hierarchical Action-Structured Decoding== (intra/inter-action confidence remasking) for parallel coherent action generation; **55.5%** SimplerEnv (+0.74 CALVIN length), **58%** real in-domain / **40%** OOD.
- **[[2508.20072|Discrete-Diffusion-VLA]]** — A ==masked-token discrete diffusion== action decoder unified in the VLM transformer + ==confidence-guided easy-first== adaptive inference; **96.3%** LIBERO, **~2×** lower latency, only **1.4%** language degradation OOD.
- **[[2511.14148|AsyncVLA]]** — An ==Asynchronous Flow Matching (AFM)== policy with a ==confidence rater== that masks low-confidence action tokens for regeneration + ==unified SFM/AFM training== + ==KV-cache reuse==; **97.4%** LIBERO, **70.8%** WidowX, **74.9%** Google Robot visual matching.
- **[[2511.19433|MoH]]** — A ==Mixture of Horizons== action-chunking policy fusing multiple chunk-length predictions through a gated mixture network + balance loss, with a ==cross-horizon-consensus dynamic inference== that self-truncates executable chunks; SOTA **99%** LIBERO (π0.5), up to **2.5×** throughput while resolving the foresight-vs-precision trade-off.
- **[[2503.02310|PD-VLA]]** — A training-free ==parallel decoding== scheme that swaps ==causal attention== for ==bidirectional attention== so all action tokens update simultaneously, iterating ==Jacobi decoding== to a fixed point; **2.52x** execution-frequency gain (**4.56 Hz** vs **1.81 Hz**) at **94.7%** LIBERO, real push-button **80%** (vs **60%**), pour-water **60%** (vs **10%**).
- **[[2411.02359|DeeR-VLA]]** — A ==multi-exit MLLM== VLA that terminates inference at intermediate layers via an ==action-consistency== criterion (stop when consecutive-exit actions stabilize) + auxiliary action heads per exit; **5.2–6.5×** lower LLM compute and **2–6×** less GPU memory on CALVIN LH-MTLC with no performance loss. The foundational dynamic-depth VLA.

#### 2.5 Dual-System Latency & Streaming

The other efficiency frontier targets the *control loop* rather than per-call FLOPs: skip the heavy VLM on intermediate steps, overlap generation with execution, or draft-then-verify across a fast/slow path. These compose with §2.1–2.4 and matter most when the bottleneck is wall-clock latency, not parameter count.

- **[[2608.08725|WA-SpecDec]]** — A ==World-Aware Bias== module injects frozen ==VAE== next-frame latents into prefill via a spatial ==VideoEncoder==, with a ==LoRA==-adapted target and ==KL-distilled== draft; OpenVLA LIBERO-Long **49.4%→56.2%** at **1.26-1.54x**, ActionCodec **95.6%** at **1.72x**.
- **[[2608.03483|BCP]]** — A lightweight ==Bernoulli-Continuation Head== bolted onto a frozen chunk-based VLA that models replan-vs-continue horizon selection as ordinal Bernoulli decisions, trained via RL with a ==Replanning-Efficiency Reward==; **+11.08pp** on RoboTwin 2.0 low-success tasks, real AGIBOT G1 grasping **74%→92%**, only **2.03ms** overhead.
- **[[2607.14695|Reflex]]** — A ==streaming inference== system re-architecting the VLA serving loop to parallelize vision and action generation, with ==Partitioned Attention== exploiting encoder timestep-invariance for O(1) cache updates and ==AdaRMSNorm== stabilizing ==mixed-precision==; **2.58×** speedup, **−54%** reaction latency, **50 Hz** control at **0%** stall, **+11–17pp** real-robot.
- **[[2602.12978|Legato]]** — Makes chunk-to-chunk continuity a ==native, learned property== of flow policies: a horizon-wise ==continuation vector ω== defines an ==action-noise mixture== matching RTC-style guidance; randomized delay/ramp training lets one model adapt without retraining; **~10%** shorter task completion vs RTC, lower NSPARC + Chunk-Overlap RMSE across five real tasks.
- **[[2601.20130|REMAC]]** — Trains the delay *into* the policy: ==LoRA== fine-tuning with ==prefix masking== puts loss only on actions that will actually be newly executed after inference latency, then ==Prefix-Preserved Sampling== reuses committed actions at inference; beats BID and RTC across **12** dynamic Kinetix tasks, matching models trained on **20×** more data.
- **[[2512.05964|Training-Time-RTC]]** — A ==training-time action conditioning== drop-in for Real-Time Chunking that learns action postfixes conditioned on known prefixes by ==simulating inference delay during training== (per-token flow timesteps, postfix-only loss), removing inference-time inpainting overhead; matches inference-time RTC at higher delays, **135→108 ms** on π₀.₆.
- **[[2605.29438|ElegantVLA]]** — A plug-in ==phase-adaptive inference== method with a lightweight RL scheduler using ==CKA semantic-stability cues== to allocate backbone compute; **3.77×** sim / **2.18×** real FLOPs speedup (16.6→35.0 Hz) while raising Google-Robot SR **71.08→75.00%**.
- **[[2605.02739|Latent-Bridge]]** — A lightweight model that predicts ==temporal feature deltas== so the VLM backbone is skipped on intermediate steps via a ==feature-space bridge== (GR00T) + ==KV-cache bridge== (π0.5); cuts VLM calls **50–75%**, **1.73×** GR00T speedup at **94.5%** retention.
- **[[2603.28565|StreamingVLA]]** — A ==streaming paradigm== that overlaps all VLA stages via ==State-based Action Flow Matching== (single-action generation+execution) + ==saliency-aware adaptive early observation==; **1.57×** per-action speedup, **6.45×** halting-time cut at **94.9%** (vs 95.1%).
- **[[2605.13778|Realtime-VLA-FLASH]]** — A dual-path ==speculative inference== system where a 110M ==draft model== proposes action chunks and the full path verifies/falls back; **3.04×** task-latency speedup (58.0→**19.1 ms**) at **93.8%** LIBERO (−0.3pp).
- **[[2603.22003|VP-VLA]]** — A dual-system VLA (System-2 Planner / System-1 Controller) using structured ==visual prompts== (crosshairs, bounding boxes) as an explicit interface + an auxiliary ==visual-grounding objective== on key frames; **53.8%** Robocasa-GR1-Tabletop (**+5.0%** over QwenOFT), **85%** real waste-sorting OOD at a **2.5%** generalization gap (vs **16.7%** drop).
- **[[2604.20834|PokeVLA]]** — A compact ==PokeVLM== (Qwen2.5-0.5B, 2.4M-sample embodied pretrain) + VL-Action post-training; the **1.22B** model hits **83.5%** LIBERO-Plus (SOTA), **79.3%** LIBERO-only transfer, **81.25%** real-world — pocket-sized dual-system.
- **[[2510.21817|VITA-E]]** — A concurrent see-hear-speak-act VLA pairing ==dual Active/Standby VLAs== for near-real-time interruption with a ==model-as-controller== scheme where the VLM emits `[ACT]`/`[HALT]` ==control tokens== driving state transitions; **100%** speech-interruption + emergency-stop SR, **93.3%** action-switching on a Fourier GR2 humanoid — interaction overlaps execution.
- **[[2410.15549|DP-VLA]]** — The early dual-process split: a ==Large System 2== (OpenVLA) reasons at low frequency and hands ==latent features== to a ==Small System 1== (BC-Transformer) running continuous motor control; **>10 Hz** vs OpenVLA's **~1 Hz**, beating either component alone, with decode-stage latents outperforming prefill-stage ones.
- **[[2410.05273|HiRT]]** — A ==Hierarchical Robot Transformer== imitation framework splitting a slow VLM ==System-2 understanding module== (InstructBLIP latents) from a fast lightweight ==System-1 execution policy==, running asynchronously on cached latents for high-frequency control; **9.8 Hz** (vs vanilla **4.1 Hz**) and **75.0%** real dynamic-task success vs **48.0%** for vanilla-VLA.
- **[[2410.08001|RoboDual]]** — A synergistic ==dual-system== framework pairing a LoRA-tuned 7B ==OpenVLA generalist== (slow high-level guidance via action chunks + latents) with a fast ==Diffusion-Transformer specialist== consuming RGB/depth/tactile under ==latency-aware training==; **+13.2%** CALVIN ABC→D, **15 Hz** real control (vs OpenVLA **3.9 Hz**), specialist trained in **8** GPU-hours.

#### 2.6 Post-Training Quantization

Shrink the *weights* without retraining — the lesson shared across this sub-section is that VLA quantization must be action-centric: protect the channels/blocks that carry motor fidelity and quantize the rest aggressively. Sits between §2.2's distillation and §2.5's 1-bit HBVLA on the precision-reduction axis.

- **[[2605.24011|ActQuant]]** — A sub-4-bit ==action-guided mixed-precision PTQ== assigning inter-tensor bit-widths by an ==HSIC action-sensitivity score== + intra-tensor ==Action-Mixed Fisher== scale optimization (blends action-head + LM losses), deployed via OmniModel.cpp; **95.0%/90.1%** OpenVLA-OFT LIBERO at 3.0/2.5 bpw (vs 96.9% FP16), real UR3 **75%** at 3.0 bpw.
- **[[2602.20309|QuantVLA]]** — A training-free ==selective W4A8 quantization== that integerizes the LLM backbone + DiT-head MLPs while keeping attention projections in FP, plus ==Attention Temperature Matching== + ==Output Head Balancing== per-head calibration; **70%** memory cut for π0.5 (4.27→**1.28 GB**) at **97.6%** LIBERO (vs 97.1% FP16).
- **[[2602.13710|HBVLA]]** — A ==1-bit post-training quantization== method via ==rectified-Hessian weight partitioning== protecting action-critical weights + ==Haar-domain group-wise binarization==; **90.3%** OpenVLA-OFT LIBERO (only **6.5%** drop vs other 1-bit PTQ), real Mobile-ALOHA.
- **[[2602.03782|QVLA]]** — An action-centric ==channel-wise mixed-precision quantization== with two-stage per-channel action-sensitivity estimation + a greedy bit-demotion algorithm (0/2/4/8/16-bit) that unifies quantization and structural pruning; **99.3%** of FP OpenVLA at W4A4 (**0.5%** drop) with VRAM **28.2%** and **1.47x** speedup.
- **[[2603.07904|DyQ-VLA]]** — A dynamic quantization framework (static W4 + dynamic activation bits) that reads ==Motion Fineness== + ==Angular Jerk== as real-time proxies for instantaneous quantization sensitivity, routed by a hysteresis switch; **76.1%** LIBERO (**99.5%** of BF16), **70%** memory cut, up to **1.49×** speedup reverting to BF16 only in fine phases.
- **[[2603.03380|LiteVLA-Edge]]** — An on-device control pipeline fine-tuning a ==SmolVLM-256M== backbone with aggressive ==4-bit GGUF quantization== (Q4_K_M) and full GPU layer-offload via llama.cpp on Jetson AGX Orin; **150.5 ms** (**6.6 Hz**) with **0.13 ms** jitter, a ~**220%** speedup over CPU-only LiteVLA enabling reactive closed-loop control.
- **[[2509.09090|SQAP-VLA]]** — A training-free co-design resolving the quantization-pruning incompatibility via ==quantization-aware token pruning== (top-k attention + robot-aware protection + FPS sampling) + ==Hadamard-transformed channel-wise quantization==; **79.3%** SR (**+4.5%** over FP CogACT), **1.93×** speedup, **46%** memory cut.
- **[[2506.07530|BitVLA]]** — A fully native ==1-bit VLA== ternarizing ({−1,0,1}) all LLM-backbone + vision-encoder weights (INT8 activations) via a ==Quantize-then-Distill== vision encoder with representation-alignment loss; **96.0%** LIBERO (vs 97.1% OpenVLA-OFT) at **11×** less memory (**1.4 GB**), **4.4×** lower latency (**341 Hz**). The native-1-bit counterpart to PTQ.

#### 2.7 System-Level & Edge Inference Acceleration

Optimize the *runtime system* rather than the model — kernel fusion, cross-request pipelining, and algorithm-hardware co-design push existing VLAs to real-time on edge or consumer GPUs with no accuracy loss. Orthogonal to §2.1–2.6's model-level compression: these papers leave the weights untouched and attack CPU/GPU overheads, kernel launches, and the serial autoregressive decode bottleneck.

- **[[2607.12659|Jetson-PI]]** — Onboard VLA serving that hides latency instead of shrinking the model: ==foresight-aligned asynchronous correction== predicts future ==VLM hidden states== conditioned on committed actions, ==confidence-based scheduling== skips VLM calls, and a ==llama.cpp== runtime adds graph reuse; **0.70→6.06 Hz** on Jetson Orin (**8.66×**), **+14.8%** over VLASH.
- **[[2606.07383|RhinoVLA-Technical-Report]]** — A token-efficient edge VLA (2.13B Qwen3-VL with 64 merged visual tokens + 0.40B Action Expert) co-designed with the Huixi R1 SoC via ==hardware-aware compilation== + W8A16 + a cross-robot ==72D state-action slot space== with robot-instance LoRA; **11.69 Hz** on-SoC (2× over baseline), **90.0%** avg LIBERO.
- **[[2512.20276|ActionFlow]]** — A training-free system framework that overlaps the compute-bound prefill of the current request with the memory-bound decode of historical requests via ==Cross-Request Pipelining== + ==CRS Packed-Forward== + a unified KV ring buffer; **2.56×** Jetson AGX Orin / up to **4.36×** speedup on OpenVLA-7B, lossless LIBERO SR.
- **[[2604.24447|VLA-XPU]]** — A model-hardware co-characterization of VLA pipelines across GPUs/NPUs/XPUs via a ==Cost-Energy-Time leaderboard==, plus two training-free optimizations: ==DP-Cache== (cuts diffusion-step redundancy) + ==V-AEFusion== (VLM/Action-Expert pipeline parallelism); **6.0×** on Ascend 310P, **1.3×** π0 — exposes the compute-bound-VLM vs memory-bound-AE imbalance.
- **[[2510.26742|Running-VLAs-Real-time]]** — A multi-stage system optimization (==CUDA graphs== + QKV-projection fusion + manual GEMM/kernel tuning + pinned memory) pushing a two-view live VLA to real-time on one consumer GPU; **106.5→27.3 ms** on an RTX 4090 (~4× speedup, near the **20.6 ms** lower bound), **100%** falling-pen grasping at <200 ms reaction.

**Efficient VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Sub-20ms real-time control | [[2605.08799\|ElasticFlow]] (one-step flow at **14ms/71Hz**) |
| Smallest deployable VLA | [[2506.01844\|SmolVLA]] (450M) or [[2509.09372\|VLA-Adapter]] (0.5B) |
| PEFT preserving foundational capabilities | [[2605.06175\|VLA-GSE]] (**+6.3pp** over FFT) |
| Zero architectural changes | [[2510.13054\|VLA-0]] (actions as text) |
| Compress an existing flow-matching VLA | [[2604.05656\|SnapFlow]] (**3.3x** faster [[2504.16054\|π0.5]]) |
| Training-free token reduction | [[2604.05323\|VLA-InfoEntropy]] (**1.53x** speedup) |
| Dynamic compute allocation | [[2605.09948\|LoopVLA]] (**−45%** params, **1.7x** throughput) |
| Action-stream compression | [[2501.09747\|FAST]] (DCT+Huffman, **5x** faster) |

^dm-2

> [!star] Key Papers
> - [[2605.08799|ElasticFlow]] — One-step physics-consistent policy via average velocity field; **14ms** inference at **71Hz**, **98.5%** [[2306.03310|LIBERO]], **5x** faster than [[2303.04137|Diffusion-Policy]]
> - [[2501.09747|FAST]] — DCT+Huffman action compression for **5x** faster VLA inference; the foundational efficiency-via-tokenization paper
> - [[2506.01844|SmolVLA]] — 450M-param distilled VLA; **7x** less memory, **40%** faster training; the canonical small-VLA baseline

^key-papers-2

> [!tip] When Smaller Is Enough
> For structured environments with known objects, [[2506.01844|SmolVLA]] (450M) matches larger models. For open-world tasks with novel objects, you still need 3B+. The sweet spot: use [[2501.09747|FAST]] tokenization on a mid-size model, or one-step flow ([[2605.08799|ElasticFlow]]) when sub-20ms control matters. Cross-reference [[06_WAM#6. Efficient & Action-Centered WAMs]] for the WAM-side efficiency recipe (training-time video, test-time speed).

^insight-2

---

### 3. Spatial & 3D-Aware VLAs

Standard VLAs process 2D images and lack explicit 3D understanding — but real-world manipulation requires reasoning about depth, contact, and viewpoint-invariant geometry. The cluster splits along three orthogonal strategies for injecting 3D awareness: add explicit depth/point-cloud streams (architectural complexity), supervise implicit 3D perception during training (deploy-time efficiency), or align the encoder with a 3D-pretrained teacher (zero inference overhead). Each strategy trades a different cost — explicit approaches generalize best to novel viewpoints, implicit approaches deploy cheapest, representation alignment is the recent compromise.

#### 3.1 Explicit 3D Integration

Add depth sensors, point clouds, or 3D coordinate embeddings as additional input modalities. Strongest generalization to novel viewpoints because the geometry is *actually present* — at the cost of architectural complexity and sensor requirements.

- **[[2608.10756|Semantic-3DGS Mobile Manipulation]]** — ==Active Semantic-3DGS== (view-scoring + ==VGGT== geometry + ==CLIP==/==DINOv2== distillation) feeds a ==PPO== reachability-aware base-posture controller and ==Late-Block Semantic Injection== into a frozen diffusion VLA; **60%** long-horizon SR (vs **40%** PointVLA), **74%** cluttered pick (vs **52%**).
- **[[2608.05042|BridgeVLA++]]** — Extends [[2506.07961|BridgeVLA]]'s ==2D-heatmap pre-training== + orthographic-projection 3D fine-tuning with a unified ==spatio-temporal memory== (temporal keyframes for coarse reasoning, point-cloud memory for occlusion-robust localization); **93.7%** RLBench, **96.0%** RMBench (**+13pp** over MemoryWAM), **95.4%** real Franka at **3** demos/task.
- **[[2607.12356|VistaVLA]]** — Builds a ==3D Gaussian-grounded cognitive representation== (RGB-D rendering + SigLIP2/DINOv2 distillation into Gaussian primitives) compressed by a parameter-free ==Merge-then-Query (MtQ)== mechanism into 64 context tokens; **+22.8pp** real-world SR over VLA-Adapter, LIBERO-Pro-Swap OOD **1.7%→12.2%**.
- **[[2607.11498|Robot-Centric Pointmaps]]** — Converts per-pixel depth into an ==end-effector-centered pointmap== (camera→robot-base frame, re-centered at the gripper) via an encoder init'd from the VLA's RGB weights, fused ==element-wise== with RGB tokens; **+7.6pp** π0.5 RoboCasa (55.3→**62.9%**), **+11.7pp** real Franka on unseen viewpoints (55.0→**66.7%**).
- **[[2607.06564|Lift3D-VLA]]** — Lifts a 2D VLA to 3D via camera-aligned ==2D model-lifting== + ==Geometry-Centric Masked Autoencoding== (static point reconstruction + future geometric prediction) + ==layer-wise temporal action decoding==; **88.6%** MetaWorld, **82.8%** RLBench, **71%** real, only **6-8%** OOD degradation.
- **[[2606.03943|PointAction]]** — A ==3D-pointmap-as-universal-action== framework where a ==universal video-to-point model== predicts dynamic 3D pointmaps from embodiment-agnostic video + a lightweight ==point-to-action decoder==; **47.7%** in-distribution + **17.0%** unseen-task SR on RoboCasa365 (2–**2.5×** over baselines), **43.0%** cross-embodiment real xArm7.
- **[[2606.02274|Dexterity-BEV]]** — A 3D-aware VLA integrating per-pixel 3D into multi-view RGB-D via ==aligned vertex maps + vertex spectrums== and a canonical ==Bird's-Eye-View reference frame==; **89.9%** avg on modified-pose LIBERO where 2D baselines fall **<10%**, plus **76.7%** "Fold Mailer Box" (vs X-VLA **56.7%**) and **93.3%** "Handover Book" real bimanual.
- **[[2508.17230|FVP]]** — A self-supervised ==4D Visual Pre-training== objective training a ==conditional diffusion model== to predict the next 3D point cloud, as a plug-in for any 3D encoder; **+16.9%/+24.7%** in-domain/OOD on 12 sim benchmarks, **+15–55%** absolute across 12 real tasks/platforms, lifts RDT-1B corner-placement **14/20** vs **8/20** 2D-only.
- **[[2508.09071|GeoVLA]]** — A ==dual-path== architecture: a frozen VLM for 2D vision-language parallel to a ==Point Embedding Network== (PEN) using an ==end-effector token== as spatial anchor, fused by a ==3D-enhanced Action Expert== (3DAE) Diffusion Transformer with static-routed MoE; **97.7%** [[2306.03310|LIBERO]], **77%** ManiSkill2; robust to viewpoint/scale shifts.
- **[[2605.11832|AML-VLA]]** — A ==Geometry-Guided Gated Transformer== (G³T) fusing synthesized multi-view + monocular geometric priors with Action Manifold Learning; **98.6%** [[2306.03310|LIBERO]], **85.7%** [[2510.13626|LIBERO-Plus]], **86.06%** [[2506.18088|RoboTwin-2.0]] real bimanual.
- **[[2604.12908|VGA]]** — A ==VGGT== 3D-world-model backbone + Progressive Volumetric Modulation for vision-to-geometry mapping; **98.1%** [[2306.03310|LIBERO]] with **+6%** OOD.
- **[[2603.25399|LaMP]]** — A ==dual-expert== framework where a Motion Expert learns dense ==3D scene flow== as a latent motion prior via ==conditional flow matching==, fused into last-layer VLM features by ==gated cross-attention== to condition the Action Expert; **98.3%** [[2306.03310|LIBERO]] (**96.7%** Long), **79.3%** LIBERO-Plus OOD (**+9.7pp** over OpenVLA-OFT), **62.5%** real OOD.
- **[[2603.24393|3D-MIX]]** — A plug-and-play ==VGGT-derived 3D feature fusion== with ==semantic-conditioned adaptive gating== (==GatedFusion==) blending 3D geometry with 2D MLLM semantics into GR00T-/π-style VLAs unchanged; **98.05%** LIBERO, **68.23%** SIMPLER (**+10.42%** over baseline), **+12.51%** OOD on RynnBrain-8B.
- **[[2603.12730|AnchorVLA4D]]** — A spatial-temporal VLA adding the episode's ==initial anchor frame== plus a lightweight ==Any4D spatial encoder== (geometric anchor↔current relationship) concatenated into a Qwen2.5-VL-3B's hidden states + ScaleDP head; **64.6%** Simpler-WidowX (**+13.6pp** over baseline), **80%** real, at only **+16%** latency.
- **[[2603.09079|GST-VLA]]** — A 3D depth-aware VLA encoding scenes as ==anisotropic Gaussian spatial tokens== (position + surface orientation + confidence, adaptively allocated) plus a ==Depth-Aware Chain-of-Thought== forcing explicit SE(3) geometric targets before action; **83.1%** LIBERO-Pro (vs SpatialVLA **76.8%**), **+9.2pp** on precision insertion over DepthVLA.
- **[[2602.23721|StemVLA]]** — Fuses 2D images with a ==4D Historical Spatiotemporal Representation== (VGGT features aggregated over time) and a ==3D Future Spatial-Geometry World Knowledge Predictor (FSGWP)== supervised via L2 loss; **92.0%** avg LIBERO (vs SpatialVLA **78.1%**), FSGWP alone lifts LIBERO-Long **67.0%→86.0%**.
- **[[2602.19710|Pose-VLA]]** — A ==decoupled learning paradigm== separating camera-centric 3D-prior pretraining from embodiment-specific post-training, using discretized ==pose tokens== shared across states and actions; **87.3** AP15 Objectron (**+16.1pp** over Qwen3-VL), **79.1%** RoboTwin 2.0 Hard (**+14.0pp** over π0), **96.0%** LIBERO, **81.25%** real-world across four tasks.
- **[[2602.10698|AugVLA-3D]]** — A sensor-free 3D augmentation injecting ==VGGT monocular-depth point clouds== encoded by a PointNet into a VLA, regularized by a lightweight ==Action Assistant== so the geometry aligns with manipulation without destabilizing the backbone; **54%** (100-demo) RoboCasa-GR1 vs GR00T **50%**, improved dexterous bimanual placement.
- **[[2510.13375|DepthVLA]]** — A ==mixture-of-transformers== VLA unifying a VLM, a pretrained ==depth expert== (DINOv2-L + Depth-Anything-V2), and an action expert via shared block-wise-masked attention, trained end-to-end with flow matching; **74.8%** Simpler-WidowX (vs π0 **58.8%**), **94.9%** LIBERO, **79%** real progress (vs **65%**).
- **[[2507.00416|Evo-0]]** — A VLA fusing ==VGGT-derived 3D tokens== from multi-view RGB into 2D VLM tokens via lightweight cross-attention (LoRA backbone), no depth sensor; **+15pp** sim (56% RLBench vs π0 41%) and **+28.88pp** real (57.41% vs 28.53%), with up to **+40pp** robustness under distractors/viewpoint shift.
- **[[2503.07511|PointVLA]]** — A modular framework injecting ==hierarchical point-cloud 3D features== into specific blocks of a frozen pretrained 2D VLA via ==skip-block analysis== that finds low-disruption injection points; discriminates real objects from photographs, adapts to object heights, learns long-horizon tasks from **20** demos — the foundational 3D-into-pretrained-VLA baseline.
- **[[2506.22242|4D-VLA]]** — A VLA with ==3D coordinate spatial vision tokens== + ==adaptive Memory Bank Sampling== using learnable temporal positional encodings on InternVL-4B; **+12.1pp** avg over OpenVLA on LIBERO (**+25.4pp** on LONG); **81.0%** in-view + **73.8%** cross-view on MV-Bench; **85.63%** real Franka (vs **27.70%** OpenVLA).
- **[[2506.01196|OG-VLA]]** — A 3D-aware VLA that builds a multi-view RGBD point cloud, renders ==canonical orthographic views==, and has the VLM emit ==image tokens== decoded by a diffusion model into annotated views from which 6-DoF poses are read; **37.7%** ARNOLD Novel-Pose (+10.8% rel over PerAct), **90%** novel-object pickup, real from 3–5 demos.
- **[[2501.15830|SpatialVLA]]** — A spatial VLA whose ==Ego3D Position Encoding== injects depth + egocentric 3D pixel positions + ==Adaptive Action Grids== using parameterized Gaussians for non-uniform spatial tokens, ==two-stage trained== on **1.1M** demos; **71.9%/68.8%** SimplerEnv Google Robot, **78.1%** LIBERO — the foundational explicit-3D baseline for VLAs.
- **[[2602.11236|ABot-M0]]** — An ==Action Manifold Learning (AML)== model predicting clean actions on a ==low-dimensional manifold== + ==UniACT-dataset== harmonizing **6M+** trajectories + ==modular VGGT/Qwen-Image-Edit geometric priors== via cross-attention; **98.6%** LIBERO, **80.5%** LIBERO-Plus (vs **42.9%** UniVLA), **58.3%** RoboCasa GR1 (vs **47.6%** GR00T-N1.6).
- **[[2403.09631|3D-VLA]]** — A generative VLA pairing a ==3D vision encoder== + LLM backbone with ==interaction tokens== over RGBD/point-cloud/bbox + a large 3D embodied-instruction dataset, generating multimodal goal states (RGBD + point clouds). The foundational generative 3D-VLA-as-world-model baseline.
- **[[2605.29416|3DVLA]]** — A ==plug-and-play== 3D-reasoning module for pretrained VLAs via ==multi-view spatial fusion== + ==object-centric 3D instance module== (entities in 3D, not 2D bboxes); SOTA **86.0%** LIBERO-Plus, **+6.9pp** RoboTwin 2.0 hard with π0.
- **[[2605.21414|PointACT]]** — A dual-system VLA pairing a frozen VLM + ==3D-aware action expert== with ==multi-scale point-action interaction== (bottleneck windowed self-attention over point clouds); **96.0%** LIBERO, **82.3%** RLBench, smoother contact-rich real SO-100/UR5.
- **[[2605.05126|ConsisVLA-4D]]** — A spatiotemporal-consistency VLA whose ==Cross-View Aligner== selects instruction-relevant object tokens + ==Cross-Object Fuser== aggregates spatial geometry across viewpoints; **98.1%** LIBERO (+20% over SpatialVLA), **70.0%** real long-horizon bimanual.
- **[[2603.12193|SaPaVe]]** — A decoupled ==active perception== architecture where a LoRA Camera Adapter + separate camera/manipulation decoders learn semantic viewpoint control (==ActiveViewPose-200K==) then active manipulation, with ==Universal Spatial Knowledge Injection==; **84.3%** active-perception (vs Gemini-2.5-Pro 72.7%), **85.0%** real manip (vs π0 45%).
- **[[2601.08325|ActiveVLA]]** — A coarse-to-fine ==active perception== VLA: 3D Crucial-Area Perception + ==Active Viewpoint Selection== (visibility/distance/diversity scoring) + Active 3D Zoom-in re-render feeding a 3D action-prediction head; **91.8%** RLBench, **65.9%** COLOSSEUM, **51.3%** GemBench — viewpoint control for occlusion-heavy tasks.
- **[[2512.21970|StereoVLA]]** — A ==GeoSem Vision Encoder== fusing FoundationStereo's ==filtered cost volume== with SigLIP/DINOv2 features, co-trained with ==Interaction-Region Depth Estimation== and ==Camera Parameter Estimation==; **+33.4pp** real-world SR over RGB/RGBD/multi-camera baselines, robust to camera-pose randomization, strong zero-shot on LIBERO-MV-R.
- **[[2512.13080|VIPA-VLA]]** — A ==dual-encoder== (2D VLM + 3D vision encoder) VLA pretrained on ==Hand3D== human videos to align 2D semantics with 3D spatial features then learn 3D motion priors from discretized wrist trajectories; **96.8%** LIBERO, **45.8%** RoboCasa, **50%** real "Wipe-Board-Unseen" where baselines hit 0–10%.
- **[[2511.17199|VLA-4D]]** — A VLA embedding 4D awareness into both streams: ==Fourier spatiotemporal embeddings== fuse 3D coords + 1D time into visual features, and the action space adds an explicit ==step-duration variable Δt==; **97.4%** LIBERO at **5.8 s** avg completion, smooth global trajectories with stable local motion speeds.
- **[[2510.17439|FALCON-Spatial-VLA]]** — An ==Embodied Spatial Model== that extracts global 3D geometric priors from RGB (+optional depth/pose) into a ==Spatial-Enhanced Action Head== preserving the 2D VLM's alignment; **62.9%** SimplerEnv-Google, **70.0%** real cluttered (**+25.6%** over SpatialVLA), lifts height-sensitive SR 60→80%.
- **[[2510.14836|QDepth-VLA]]** — An ==auxiliary quantized-depth prediction== VLA: a VQ-VAE turns depth into discrete tokens predicted by a dedicated ==depth expert== fed straight from the vision encoder + ==hybrid attention==; **+8.8%** LIBERO-Spatial over open-π0, **+29.7%** SimplerEnv long-horizon, single-view rivaling multi-view.
- **[[2506.07961|BridgeVLA]]** — A VLA that projects 3D point clouds into ==2D orthographic== images so a PaliGemma backbone processes them natively + a ==2D-heatmap pretraining== phase whose heatmaps back-project to 3D targets; **88.2%** RLBench (vs RVT-2 81.4%), **95.4%** real with only **3** demos/task.
- **[[2502.13143|SoFar]]** — A ==semantic orientation== representation (reference-frame-free, language-grounded direction) + ==OrienText300K== + ==PointSO== cross-modal 3D Transformer for zero-shot 6-DoF reasoning; **85.3%** positional / **48.9%** real 6-DoF manip, **48.7%** Open6DOR V2 — orientation bridges spatial reasoning and manipulation.
- **[[2505.05800|3D-CAVLA]]** — An ==OpenVLA-OFT== variant adding ==CoT narrative instructions== (GPT-4 decomposition) + RGB-D→point-cloud depth encoder + ==Task-Aware ROI detection==; **98.1%** LIBERO, **+8.8pp** on LIBERO-Unseen novel tasks.
- **[[2605.24642|GFM-VLA-Study]]** — A diagnostic study that linear-probes GR00T-N1.5's geometric deficiency (**0.73m** vs VGGT **0.41m** depth RMSE) and compares Early/Late-Fusion vs Spatial Forcing integration; quantifies *why* explicit 3D helps.
- **[[2605.12369|GuidedVLA]]** — A method specializing ==attention-head subsets== in the action decoder with auxiliary supervision for ==object grounding + skill recognition==; **75.4%** LIBERO-Plus (+7.2 over π0), RoboTwin 2.0 **77.4→90.6%**.

#### 3.2 Implicit 3D Reasoning

Achieve spatial awareness without explicit depth input — supervise 3D understanding at training time or overlay 2D cues. Cheapest to deploy but can fail when the camera moves significantly from training distribution.

- **[[2608.01066|OC-VLA++]]** — Extends [[2508.13103|OC-VLA]] with ==geometry-guided paired-view supervision== (synthetic views from a frozen monocular 3D reconstruction model) + a ==cross-view action-equivariance== training objective, no architecture changes; **48.3%** vs **40.8%** OC-VLA at max real-world camera shift, **+4.4pp** multi-view sim (52.4%→56.8%).
- **[[2606.06761|AxisGuide]]** — Projects the robot's base-frame action axes as RGB-encoded arrows from the end-effector's pixel location, forming a 3-channel ==action coordinate cue image== concatenated with the RGB observation, no depth sensor needed; **+19.88pp** real-world Pick-Up (**30.12%→50.00%**), **+13.33pp** in sim, at only **+0.13%** params and **~5.4ms** latency.
- **[[2605.14950|Evo-Depth]]** — A lightweight ==Implicit Depth Encoding Module== (multi-view-depth init) + ==FiLM-style Spatial Enhancement== injecting implicit depth into 2D VL features; **95.4%** LIBERO, **84.4%** Meta-World, **90%** real xArm6 — depth without a depth sensor.
- **[[2602.10109|ST4VLA]]** — A ==dual-system== VLA (Qwen2.5-VL planner + DINOv2 Diffusion-Transformer action expert) with two-stage ==spatial-grounding pretraining== then ==spatially-guided post-training==, activating internal scene-geometry reasoning via ==spatial prompting==; **95.9%** LIBERO, **84.6%** SimplerEnv-Google VM, strong unseen-object/instruction generalization.
- **[[2512.02902|VLA-Generalizability-Study]]** — A study decoupling ==spatial (visual encoder)== from ==physical (VLM + action expert)== modeling: ==Feature Token Modulation== (4K-param affine on visual tokens) lifts novel-viewpoint SR 48.5→**87.1%**, while ==Feature Linear Adaptation== (LoRA) hits **94.8%** on Libero-V at **99×** fewer trainable params.
- **[[2511.01571|PixelVLA]]** — A pixel-grounded VLA with ==visual-prompt-aware== + ==multiscale pixel-aware== encoders + ==Pixel-160K== auto-annotated dataset; **86.7%** LIBERO, **61.4%/50.1%** SimplerEnv-Google VM/VA (+28.7%/+10.1% over OpenVLA).
- **[[2510.13778|InternVLA-M1]]** — A dual-system VLM planner (Qwen2.5-VL-3B) + diffusion action expert with ==spatially-guided two-stage training==; **+14.6%** SimplerEnv-Google, **+9.8%** WidowX, strong unseen generalization.
- **[[2509.14117|GeoAware-VLA]]** — A VLA replacing the standard vision encoder with a frozen ==VGGT geometric foundation model== + a lightweight multi-scale projection layer for view-invariant features, no explicit 3D; **+35pp** zero-shot unseen-viewpoint LIBERO, **96.8%** LIBERO / **94.8%** CALVIN in-distribution with the VQ-BeT head.
- **[[2508.13103|OC-VLA]]** — A plug-and-play ==observation-centric== reframing that predicts actions in the ==camera observation space== (via extrinsic calibration), not the robot base frame, to remove the camera/control spatial-misalignment "learning conflict"; **+14%** discrete / **+8%** continuous sim, **77.5%** real 10-shot, only **−14%** under a novel zero-shot viewpoint.
- **[[2508.10333|ReconVLA]]** — A ==gaze-region reconstructive== VLA where a ==diffusion-transformer denoiser== on the visual tokens predicts noise on latent ==scene tokens== of the gaze region (==Grounding DINO==); **3.95** avg subtask length on CALVIN ABC→D, stack-block **59.3% → 79.5%**; the denoiser generalizes to contact regions — close to [[2603.05687|CGP]]'s denoiser.
- **[[2508.07917|MolmoAct]]** — A ==three-stage autoregressive pipeline==: depth-aware perception tokens → visual reasoning traces → low-level actions with ==byte-level BPE action tokenization==; **86.6%** LIBERO, **+10pp** real-world single-arm + **+22.7pp** bimanual over π0-FAST, **75%** visual-trace steering SR (**+33pp** over language steering).
- **[[2412.10345|TraceVLA]]** — A ==visual trace prompting== method overlaying ==Co-Tracker== multi-point historical trajectories on the current observation; **47.7%** SimplerEnv (+7.5pp over OpenVLA), **74.8%** LIBERO, **6/10** on unseen "Pickplace Banana" where OpenVLA fails; **~0.03 s/step** inference overhead.

#### 3.3 Representation Alignment

Align the student VLA's visual encoder with a frozen **3D-geometry** teacher (VGGT, DINOv2-FiT3D, depth models, 3D trackers) — inject spatial awareness *at the encoder* before linguistic entanglement, with zero inference overhead. The newest direction, fastest path to deployment.

- **[[2608.04633|Mind-VLA]]** — Focuses 3D supervision on the instruction-specified target object via canonical ==tri-view== (top/front/side) + VGGT features supervising dedicated object queries, removed at inference; **93.9%** LIBERO at **345M** params, only **-13pp** under ~25% target occlusion (vs -21 to -29pp for instruction-agnostic baselines).
- **[[2608.03727|Track4Action]]** — Distills world-centric 3D motion/geometry cues from a frozen `Track4World` 3D tracker into learnable ==track queries== via action-aligned video ==privileged supervision==, discarding the tracker for ==tracker-free deployment==; **82.3%** LIBERO-Plus zero-shot robustness, **+20pp** real bimanual over the alignment-free baseline.
- **[[2608.01826|MVUCF]]** — A ==training-only geometry injection== stage shaping a multi-camera VLA's upper hidden states via a ==depth objective== + ==cross-view correspondence objective==, with auxiliary heads discarded so inference stays RGB-only; depth MAE **4.9cm→0.44cm**, cross-view Hit@1 **0.4%→64%**, **+22.4pp** LIBERO-Plus, **81.7%** real humanoid SR.
- **[[2606.03240|GeoAlign]]** — A ==state-guided geometry alignment== method: post-training a depth model's encoder on robot-domain RGB-D yields ==Geometry-Enhanced Post-Trained (GEP) features== from RGB alone; **99.0%** LIBERO (over GR00T N1.6's **97.0%**) and **78.8%** on eight geometry-critical real ALOHA tasks (vs RGB-only **65.0%** / π0.5 **67.5%**).
- **[[2605.10485|VEGA]]** — A representation-alignment method that aligns a student [[2304.07193|DINOv2]] visual encoder with a frozen ==DINOv2-FiT3D== teacher (fine-tuned on multi-view-consistent 3D Gaussian Splatting) via patch-cosine loss + lightweight LayerNorm+MLP projector; **[[2506.18088|RoboTwin-2.0]] SOTA** (Easy **67.5%**, Hard **30.7%**) at **zero inference overhead**.
- **[[2602.17951|ROCKET]]** — A ==residual-oriented multi-layer alignment== injecting 3D into a 2D-pretrained VLA via a *single shared projector* across aligned student/teacher layer pairs (avoids gradient interference) + ==Matryoshka sparse activation==; **98.5%** LIBERO at **~4%** of prior compute, **81.7%** LIBERO-Plus with biggest gains under robot/layout shift.
- **[[2512.00903|SwiftVLA]]** — A VLA distilling frozen 4D ==VGGT== spatiotemporal features into a lightweight VLM via learnable ==Fusion Tokens== (supervised by future-EE-trajectory) + ==mask-and-reconstruct== so the 4D branch is dropped at inference; **0.53** RoboTwin 2.0 (vs SmolVLA 0.29), **94.7%** LIBERO, **18×** faster on Jetson Orin.
- **[[2510.12276|Spatial-Forcing]]** — An ==implicit cosine-similarity alignment== of a VLA causal-attention layer to ==VGGT 3D foundation model== features (24th layer); **98.5%** LIBERO at **3.8×** training + **5.9×** data efficiency, **zero inference overhead**.

**Spatial VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Novel-viewpoint generalization | Explicit: [[2508.09071\|GeoVLA]] or [[2605.11832\|AML-VLA]] |
| Deploy without depth sensors | Implicit: [[2510.12276\|Spatial-Forcing]] or [[2412.10345\|TraceVLA]] |
| Zero inference overhead, 2D deployment | Representation alignment: [[2605.10485\|VEGA]] |
| Bimanual real-world manipulation | [[2605.11832\|AML-VLA]] (**86.06%** [[2506.18088\|RoboTwin-2.0]]) |
| 3D plug-and-play for existing VLA | [[2603.24393\|3D-MIX]] (**+12.51%** OOD) |
| Foundational adaptive 3D representation | [[2501.15830\|SpatialVLA]] |
| 4D temporal-spatial context | [[2506.22242\|4D-VLA]] |

^dm-3

> [!star] Key Papers
> - [[2508.09071|GeoVLA]] — Dual-path 2D-VLM + 3D point-cloud PEN with end-effector anchor + MoE 3DAE; **97.7%** [[2306.03310|LIBERO]]; the cleanest explicit-3D architecture
> - [[2605.10485|VEGA]] — DINOv2-FiT3D teacher alignment via patch-cosine loss; **[[2506.18088|RoboTwin-2.0]] SOTA** with **zero inference overhead**; representation alignment beats explicit 3D fusion
> - [[2501.15830|SpatialVLA]] — Foundational adaptive 3D spatial representations for VLAs; the canonical explicit-3D baseline

^key-papers-3

> [!tip] 3D Without 3D Sensors
> The field is split three ways: explicit ([[2501.15830|SpatialVLA]], [[2506.22242|4D-VLA]], [[2508.09071|GeoVLA]]) generalizes best to novel viewpoints but requires depth sensors; implicit ([[2510.12276|Spatial-Forcing]], [[2412.10345|TraceVLA]]) deploys cheapest but degrades under camera drift; representation alignment ([[2605.10485|VEGA]]) is the 2026 compromise — 3D priors inherited at training-time, 2D-only pipeline at deployment. Cross-reference [[07_Latent-World-Models#2. JEPA Evolution: Visual-Only → Dense → Vision-Language → Vision-Language-Action]] for the JEPA-side 3D-aware predictors and [[02_Dataset-Benchmark-Environment#9. Spatial Reasoning & 3D Benchmarks]] for the 3D-grounded benchmarks that test these claims.

^insight-3

---

### 4. Reasoning & Planning-Augmented VLAs

Pure imitation is brittle on long-horizon tasks with novel compositions or sparse decision points. The reasoning-augmented cluster adds test-time deliberation to improve robustness, but the *where* of the reasoning insertion matters as much as the *whether*. Four insertion strategies have emerged: reason in the language/visual space before action generation (chain-of-thought), simulate forward via a world model (online MCTS), generate-then-verify (draft-and-verify), or invert the stack entirely so a VLM agent calls the VLA as a tool. See [[05_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] for the full taxonomy of insertion points.

#### 4.1 Action & Visual Chain-of-Thought

Reason in the *action* or *visual* space before committing to the final trajectory. Reasoning is grounded in physical coordinates or image goals, not in language tokens.

- **[[2602.21157|HALO]]** — A unified VLA running ==Embodied Multimodal CoT== (textual subtask plan → visual subgoals → action) over a ==Mixture-of-Transformers== with understanding/visual-generation/action experts + an automated EM-CoT data pipeline; **80.5%/26.4%** RoboTwin 2.0 Easy/Hard (+34.1/+10.1 over π0), robust real long-horizon under distractors.
- **[[2601.11404|ACoT-VLA]]** — An ==Action Chain-of-Thought== VLA where an ==Explicit Action Reasoner== generates kinematic reference trajectories + an ==Implicit Action Reasoner== extracts ==latent action priors==, fused by an ==Action-Guided Prediction head==; **98.5%** LIBERO (**+1.6%** SOTA), **84.1%** LIBERO-Plus OOD, **66.7%** real (vs π0.5 **61.0%**).
- **[[2503.22020|CoT-VLA]]** — A ==visual CoT== VLA that first predicts a future image frame as a ==visual subgoal==, then generates actions conditioned on it, on a 7B ==VILA-U== unified backbone trained two-stage over robot demos + ==action-less video==; **+17%** real-world and **+6%** simulation over SOTA VLAs, strong on multi-instruction Franka-Tabletop tasks.
- **[[2604.22709|Abstract-CoT]]** — A ==discrete abstract token vocabulary== reasoning method + ==policy-iteration warm-up + GRPO RL== with attention-mask information bottleneck; **up to 12× fewer** reasoning tokens at comparable/superior performance on MATH, AlpacaEval, HotpotQA across Qwen3 + Granite.
- **[[2604.21396|VG-CoT]]** — A ==visual-evidence-grounded rationale== method with bounding-box coords from YOLO+PaddleOCR+Grounding DINO+GPT-4o + ==3-dim eval (Rationale Quality + Answer Accuracy + Reasoning-Answer Alignment)==; LLaVA-1.5-7B RQ **72.2 → 83.4**, AA **48.7 → 62.5** after fine-tuning.
- **[[2509.25681|dVLA]]** — A unified discrete ==diffusion== VLA over vision/language/action + ==multimodal CoT== generating visual subgoals + textual reasoning + actions; **96.4%** LIBERO + **65%** real-world (CoT adds **+6.6pp** sim, **+12.5pp** real); ==prefix attention + KV cache== for **~2×** speedup (1.3→2.9 Hz).
- **[[2503.11089|EmbodiedVSR]]** — A physics-constrained CoT method grounded in a ==dynamic scene graph==; **+18.4%** Arm Feasibility, **80%** real-world reassembly success.

#### 4.2 Online MCTS & World-Model Verification

Use the world model as a simulator at inference time: sample action candidates, simulate forward, score outcomes, select the best. Highest robustness on novel tasks at **3-5x** latency cost.

- **[[2509.22643|VLA-Reasoner]]** — A ==plug-in online MCTS== method with learned world model + ==KDE action sampling== + ==vision-based value network==; **+19pp** absolute on OpenVLA real-world (**22% → 41%**) + **+10pp** on π0-FAST (**64% → 74%**); KDE (**91.5%**) beats Gaussian sampling (**85.0%**).
- **[[2507.16815|ThinkAct]]** — A ==dual-system MLLM + action model== with ==reinforced visual latent planning== via ==action-aligned rewards== (goal completion + trajectory consistency); **+15.5pp** SimplerEnv Google-VM, **84.4%** LIBERO, **48.2%** EgoPlan-Bench2, RoboVQA BLEU **59.8** + emergent few-shot adaptation + self-correction.
- **[[2509.25852|REVER]]** — A ==LEAP dataset== (kinesthetic demos → Vision-Instruction-Plan triplets) + ==verifiable reward (format + semantic similarity)== with GRPO; RoboFarseer-**7B** scores **59.3%** LEAP-L MCQ + **76%** open-ended planning (2× Gemini-2.5-Pro); **90%** real "Bring food & drinks" (+60pp over low-level only).
- **[[2505.21432|Hume]]** — A dual-system VLA enabling ==value-guided System-2 thinking==: the VLM denoises multiple action candidates and a ==value-query head== picks best-of-N, while ==cascaded action denoising== hands partially-denoised chunks to System-1 for real-time refinement; **98.6%** LIBERO (rank 1), **91%/87%** real WidowX/Franka (value worth −78%).

#### 4.3 Draft-and-Verify

Generate a fast open-loop action draft, then verify it with a closed-loop check. The middle-ground latency profile between pure imitation and full MCTS.

- **[[2603.18091|ADV]]** — An Action Draft-and-Verify framework pairing a ==diffusion draft== with a ==VLM verify== step into one self-verifying loop; **+19.7%** real-world success.
- **[[2604.18486|OneVL]]** — A ==dual-modal latent supervision== model: visual auxiliary decoder predicts future frames (world model) + language auxiliary decoder reconstructs CoT text + ==prefill inference== for answer-only latency; **88.84 PDM-score** on NAVSIM (+2.64 over prior 8B), latency **4.46s** vs **6.58s** AR CoT — first latent CoT to outperform explicit AR CoT.
- **[[2604.17800|ReFineVLA]]** — A teacher-guided ==natural-language rationale annotation== method (observation → situation analysis → spatial reasoning → task planning via Gemini 2.0) + ==selective transfer fine-tuning== + ==multi-objective BC + LM loss==; **+5.0pp** WidowX avg (+21.4 Spoon-on-Towel), **+2.3/+3.5pp** Google Robot, **+9.6pp** Move-Near.
- **[[2602.12281|Scaling-Verification-VLA]]** — A ==CoVer-VLA== hierarchical test-time ==contrastive verifier== of vision-language-action alignment (rephrase aug + bi-directional InfoNCE); **+15%** ID / **+12%** OOD over scaling policy pretraining. Verification scales better than policy.
- **[[2510.10975|RoVer]]** — Bolts a compact ==Process Reward Model== onto a *frozen* VLA at inference, scoring candidate actions for reliability while also predicting a ==6D refinement direction== that guides sampling, with a ==shared perception cache== amortizing features; **+18.4%** relative SR@5 for Dita on CALVIN (50.0→**59.2%**), real Diffusion Policy **72.9→88.6%**.

#### 4.4 VLA-as-Tool Inversion

Invert the typical stack entirely — VLM agent at the top, VLAs as bounded callable executors below. Decouples high-level planning from low-level execution; redistributes the long-horizon dual burden across components.

- **[[2608.05738|VLA-Talker]]** — Replaces generative chain-of-thought with an ==agentic tool-use loop== querying external perception modules for grounded spatial evidence, injected as ==read-only paraphrased context== supervised only on action tokens, then aligns tool-invocation timing via ==GRPO==; **97.4%** LIBERO, **4.6×** faster than generative CoT (**78ms** vs 359ms/decision).
- **[[2607.11119|VIA]]** — Bypasses the VLA layer: a frontier agent perceives a browser-based ==3D point-cloud interface== and drives the robot via ==MCP kinematic tools== — no robot-specific fine-tuning; **60–88%** zero-shot SR across six tasks, **100%** on the "Rainbow" assembly, textual waypoint demos lift CC-Opus's LIBERO-Goal **77%→100%**, at **$4.1–15.1** per episode.
- **[[2606.10267|Hi-VLA-Orchestration-Study]]** — A systematic study unifying ==hierarchical VLA== agents under one VLM-planner + VLA-controller framework; an ==Optimized Hierarchy== beats Naive-Hierarchy and Flat-VLA on long-horizon ALOHA tasks (sim+real); even a near-perfect scripted low-level policy collapses **~95%→~0%** once the hierarchy is ablated away.
- **[[2605.13119|VLAs-as-Tools]]** — A strategy formalizing VLAs as ==bounded, callable executors== invoked by a VLM agent via a ==Bidirectional VLA tool-family interface== adapted by ==Tool-Aligned Post-Training (TAPT)==; **+35.5pp** OpenVLA-OFT on RoboTwin, **+34.6pp** Faithful Rate on LIBERO-CF-Long; VLM calls **109.5 → 1.988** per task (~**55x** reduction).
- **[[2604.21924|LoHo-Manip]]** — A hierarchical ==VLM task manager + VLA executor== with ==receding-horizon== plan + ==visual-trace conditioning==; **97.5%** avg LIBERO, RoboVQA BLEU **63.1**, EgoPlan-Bench2 **56.7%**, **0.39** vs **0.24** π0.5 on VLABench.
- **[[2602.13193|Steerable Policies]]** — VLA models trained on ==six command styles==, commanded by a fine-tuned ==embodied-reasoner VLM== or an off-the-shelf VLM picking the best abstraction via ==in-context learning==; near-**100%** SR with a human oracle, outperforms five baselines when reasoner-controlled, and the in-context variant universally beats OpenVLA + a SayCan-like baseline.
- **[[2502.19417|Hi-Robot]]** — A hierarchical ==System-1/System-2== stack where a high-level VLM turns open-ended instructions and real-time corrections into atomic commands for a low-level VLA, trained on ==synthetic VLM-generated== prompts; beats GPT-4o + flat-VLA on instruction accuracy/task progress (synthetic data **+46%** IA). The foundational hierarchical instruction-following VLA.
- **[[2606.18363|Guava]]** — A universal harness that distills embodied tool-use into a compact open-source VLM via ==Perception-Reasoning-Action loops== + ==semantic action abstractions== + SFT-then-GRPO on <2,000 frontier-VLM trajectories; Guava-Agent-4B hits **75.6%** sim (beats GPT-5.4 **70.2%**), **86%/92%** zero-shot real ID/OOD, RL lifting shell-game **6.7%→60.0%**.
- **[[2603.11558|RoboClaw]]** — A VLM meta-controller unifying data collection, policy learning, and execution via in-context reasoning over structured memory, with ==Entangled Action Pairs== (forward + inverse recovery policy) enabling self-resetting autonomous data collection; **53.7%** less human collection time, **8.04x** fewer interventions, **+25%** long-horizon SR over baselines.
- **[[2508.07033|P3]]** — A versatile embodied-agent framework with ==active omni-task perception== (VLM scene graphs proposing new tasks), ==feedback-agnostic tool plug-ins== integrating navigation/manipulation/IoT/web without bidirectional feedback, and an LLM ==dynamic multi-task planner== over priorities/dependencies; **77.09%** active-task ID, robust across 11 real humanoid tasks.
- **[[2505.23450|Agentic-Robot]]** — A brain-inspired ==Standardized Action Procedure== orchestrating a GPT-4o reasoning planner + OpenVLA executor + fine-tuned Qwen2.5-VL verifier in a closed perception-reasoning-execution-verification loop with recovery; **79.6%** LIBERO, **61.6%** LIBERO-Long (+12.1% over OpenVLA), verifier worth **26.5%**.

#### 4.5 Latent & Efficient Reasoning

The cost of reasoning is latency — explicit token-by-token CoT can be **80×** slower. This sub-section compresses deliberation into *continuous latent* steps or makes it *adaptive* (think only when the task is hard), recovering reasoning's robustness benefit without its real-time penalty.

- **[[2602.01166|LaRA-VLA]]** — A latent-reasoning VLA folding multi-modal CoT into ==continuous latent representations== on Qwen3-VL + ==curriculum== replacing discrete CoT with learnable latents; **97.9%** LIBERO, **68.8%** SimplerEnv-WidowX SOTA — latent reasoning at no token cost.
- **[[2602.07845|RD-VLA]]** — A ==weight-tied recurrent transformer== that iteratively refines a latent "scratchpad" with an ==adaptive stopping criterion==; **93.0%** LIBERO beating larger token-reasoning models, **−34%** compute, up to **80×** faster than explicit-CoT VLAs.
- **[[2601.09708|Fast-ThinkAct]]** — A ==teacher-student distillation== that compresses verbose textual CoT into compact ==verbalizable latent vectors== via DPO-like preference distillation; **−89.3%** latency (9.3× faster than ThinkAct-7B) while beating SOTA reasoning VLAs.
- **[[2603.05147|Act,-Think-or-Abstain]]** — A SmolVLA backbone re-purposed as a ==task-complexity detector== for a dynamic act/think/abstain policy; **84.34%** Macro-F1 ID/OOD classification with zero fully-OOD-as-Act errors, **+6.67%** on hard tasks via selective thinking.
- **[[2510.00600|Hybrid-Training-VLA]]** — A ==Hybrid Training== scheme learning three conditional action distributions (act / think / follow) under one weighted-NLL objective, so the model internalizes CoT but runs in a fast think-free 'act' mode at deployment; **63%** real (vs OpenVLA 41%), **~3 Hz** (vs ECoT 3×, hierarchical 4× slower).
- **[[2507.17520|InstructVLA]]** — An instruction-tuned VLA on Eagle2-2B with ==MoE adaptation== dynamically switching between textual reasoning and ==latent action== generation, two-stage Action-Pretraining→VLA-IT over a 650K instruction set + the SimplerEnv-Instruct benchmark; **+92%** over fine-tuned OpenVLA (46.0 vs 23.9%), **+36.1%** from internal test-time thinking.

#### 4.6 Affordance-Centric Prediction

Predict object affordances, contact geometry, or spatial anchors as an intermediate target the action expert conditions on — grounding deliberation in *where* and *how* to interact rather than free-form language, so the action head can focus purely on motion.

- **[[2601.07060|PALM]]** — A multi-modal transformer + ==DiT== policy with a fine-grained ==affordance predictor== anticipating object relevance, contact geometry, and motion; **82.0%** CALVIN ABC→D (+17.7pp, avg length **4.48**), **94.5%** LIBERO (91.8% LONG).
- **[[2510.01623|VLA-R1]]** — A ==VLA-CoT data engine== (13K auto CoT annotations aligned with affordance+trajectory) + SFT-then-RLVR; **+17.78%** affordance IoU, **−17.25%** trajectory distance on ShareRobot with robust cross-domain transfer.
- **[[2505.08548|FSD]]** — A VLM that generates embodiment-agnostic ==visual aids== (affordance boxes/points, object-centric traces) via ==Spatial-Relationship CoT==; avg rank **1.3** across 5 spatial benchmarks (matches GPT-4o), **61.82%** VABench affordance points.
- **[[2505.16517|ManipLVM-R1]]** — An ==RLVR== framework with rule-based rewards for affordance perception + trajectory prediction; ManipLVM-R1-3B hits **31.0** IoU (vs RoboBrain-7B **11.79**) at **50%** data and best OOD Grasp-IoU **34.65**.
- **[[2605.22183|AVP]]** — An end-to-end VLA with an explicit ==visual-primitive interface== where the VLM predicts discretized 2D spatial anchors as next-stage subtasks so the action expert offloads spatial reasoning to focus on motion; **90.28%** chess / **86.18%** pick-place, **83%** unseen board-to-board (π0.5 **0%**).

#### 4.7 Symbolic & Structured Long-Horizon Planning

When horizons span many decision points, an affordance target isn't enough either — the policy needs an explicit *plan structure*: symbolic/PDDL scene graphs, hierarchical logic world models, subgoal anticipation, or value-guided search over the whole trajectory.

- **[[2605.01772|Anticipation-VLA]]** — An ==Anticipation Model== generating ==recursive multimodal (text+image) subgoals== adaptive in granularity + ==Optimal Value Function== for progress re-planning every K steps; **80.8%** avg LIBERO, **+107%** improvement on unseen real-world configurations vs π0.5.
- **[[2512.16909|MomaGraph]]** — A ==state-aware unified scene graph== (spatial + functional, part-level interactive elements) with MomaGraph-R1, a 7B VLM trained via ==DAPO RL== with a graph-alignment reward in a ==Graph-then-Plan== paradigm for mobile manipulation; **71.6%** MomaGraph-Bench (matches closed-source), **70%** real RobotEra Q5 long-horizon SR in unseen households.
- **[[2602.21531|LiLo-VLA]]** — A modular long-horizon framework decoupling a ==classical-motion-planning Reaching Module== from an ==object-centric VLA Interaction Module== (wrist-cam + clutter-masking augmentation) with closed-loop recovery; **69%** SR / **86%** progress on a 21-task suite (vs π0.5 **28%**, OpenVLA-OFT **2%**), **85%** real, **0%**→stable on permuted sequences.
- **[[2602.13086|UniManip]]** — A zero-shot manipulation framework built on a ==Bi-level Agentic Operational Graph== (Agentic Logic Layer + Semantic-Operational State Graph) with a ==task-to-motion bridge== (conservative recon + relaxed IK) and closed-loop recovery; **93.75%** zero-shot SR (vs NORA-1.5 **71.25%**), **82.5%** cluttered, fine-tune-free mobile transfer.
- **[[2506.00411|LoHoVLA]]** — A unified long-horizon VLA that ==jointly predicts linguistic sub-tasks and robot actions== on a shared PaliGemma-3B with ==hierarchical closed-loop control== distinguishing planning from execution errors (re-plans only past a K=2 failure threshold) + the LoHoSet dataset; **85.1%** reward / **81.0%** SR vs **8.2%** best hierarchical baseline.
- **[[2602.11291|H-WM]]** — A ==Hierarchical World Model== where a ==Logic World Model== (fine-tuned LLM, symbolic planning dynamics) + Visual WM jointly guide the VLA; **64.8%** LIBERO-LoHo vs **6.4%** unguided — logic guidance alone adds **+40pp**.
- **[[2511.04357|GraSP-VLA]]** — A ==Multi-Layer Continuous Scene Graph== with temporal aggregation + auto-generated ==PDDL actions== chaining a bank of low-level VLA policies; beats end-to-end VLA fine-tuning on SO-101 — **0.6 vs 0.2** SR on 2-skill tasks, **0.4 vs 0.1** on 4-skill, **0.4 vs 0.0** on 6-skill, Action Accuracy **0.96**.
- **[[2601.00969|V-VLAPS]]** — A lightweight ==MLP value function== over VLA latents trained on Monte-Carlo returns + value-guided search; **+5.2pp** spatial / **+2.8pp** object suites over VLAPS, **+31pp** on a hard spatial task.

**Reasoning VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Decouple planning from execution | [[2605.13119\|VLAs-as-Tools]] (**+35.5pp** RoboTwin, ~**55x** fewer VLM calls) |
| Long-horizon visual reasoning | [[2503.22020\|CoT-VLA]] or [[2604.22709\|Abstract-CoT]] |
| Novel-task generalization via simulation | [[2509.22643\|VLA-Reasoner]] (online MCTS) |
| Self-verification with latency budget | [[2603.18091\|ADV]] (draft-and-verify) |
| Skill recombination for OOD tasks | [[2505.03500\|TLI]] (extrapolation **9% → 83%**) |
| Physics-grounded scene reasoning | [[2503.11089\|EmbodiedVSR]] (**+18.4%** Arm Feasibility) |
| RL-trained reasoning over manipulation | [[2509.25852\|REVER]] or [[2507.16815\|ThinkAct]] |
| Reason in the action space | [[2601.11404\|ACoT-VLA]] |

^dm-4

> [!star] Key Architectural Inversion
> - [[2605.13119|VLAs-as-Tools]] — Reframes VLAs as bounded callable tools rather than top-level policies; TAPT-trained tool-family with discrete invocation + continuous progress feedback decouples high-level VLM planning from low-level VLA execution; **+35.5pp** RoboTwin, **+34.6pp** instruction fidelity, ~**55x** reduction in VLM call frequency
> - [[2502.19417|Hi-Robot]] — The foundational System-1/System-2 hierarchical split, establishing VLM-planner + VLA-executor as a design pattern before the "tool" framing crystallized it, trained entirely on synthetic VLM-generated corrections rather than costly human-annotated hierarchy data
> - [[2606.10267|Hi-VLA-Orchestration-Study]] — The systematic dissection of *why* the inversion works: isolates which hierarchy design choices (termination conditions, observation representation, memory) actually drive the gains versus cosmetic variation, validating an "Optimized Hierarchy" recipe

^key-papers-4

> [!tip] When Reasoning Helps
> Reasoning adds latency, so it's not always worth it. Use it for: (1) long-horizon tasks with many decision points, (2) novel task compositions ([[2505.03500|TLI]]), (3) tasks requiring spatial inference. Skip it for fast pick-and-place where imitation suffices. Cross-reference [[05_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] for the full insertion-point taxonomy and [[06_WAM#5. VLM-Integrated WAMs]] for VLM-integrated WAMs that fuse reasoning with dynamics prediction. For the physics-grounded flavor of that inference step, see [[08_Physics-Aware-Embodied-AI#5. Physics-Aware Reasoning]].

^insight-4

---

### 5. World-Model-Augmented VLAs

VLAs that incorporate learned dynamics models for planning, imagination, or co-training. The integration *style* defines the trade-off: the world model can be co-trained iteratively with the VLA, distilled into latent predictors, trained as a video-co-training auxiliary objective and stripped at deployment, used only as a rehearsal tool during post-training, or unified end-to-end with the policy under a shared backbone. See [[06_WAM#1. The Design Space]] for the full WAM taxonomy as standalone models; this section covers the *VLA-integration* angle.

#### 5.1 Iterative Co-Improvement

VLA and world model alternate training rounds — the WM generates synthetic data for the VLA, the VLA's improving actions give the WM harder scenarios. Each round improves both, but the WM is always one step behind the current policy.

- **[[2602.12063|VLAW]]** — An ==iterative co-improvement== of VLA + ==action-conditioned world model== with limited real rollouts (including failures) + ==VLM-reward-filtered synthetic trajectories==; **+39.2pp** absolute SR (**0.46 → 0.868**), WM FVD **225.13 → 64.12**, synthetic-data contribution **+11.6pp** — canonical mutual-improvement template.
- **[[2602.06508|World-VLA-Loop]]** — A framework co-evolving a state-aware ==video world model== + VLA in ==closed-loop== with a ==SANS (Success/Near-Success)== dataset capturing failure modes; WM hits SSIM **0.91**, **>80%** outcome-alignment; RL post-training lifts LIBERO SR up to **+24.0%**.
- **[[2602.11075|RISE]]** — An ==RL via Imagination== method inside a learned ==Compositional World Model== (Controllable Dynamics + multi-view futures); **85–95%** on real dynamic-sorting/packing/box-closing tasks with far fewer training steps.
- **[[2602.13977|WoVR]]** — A method stabilizing the action-conditioned WM via ==dual-channel action injection + first-frame anchoring== + ==hallucination-aware policy optimization== (keyframe-initialized rollouts); **23 FPS**, improves LIBERO VLA SR while serving as a reliable simulator.
- **[[2511.09515|WMPO]]** — A pixel-space ==OpenSora video WM== + lightweight ==binary-reward model== for on-policy RL in imagination; **+15.2pp** over RL baselines with emergent self-correction — RL without real-world rollouts.
- **[[2603.16860|DreamPlan]]** — A Qwen3-VL-8B keypoint planner + ==CogVideoX-5B action-conditioned WM== trained on sub-optimal exploratory data; reliably simulates deformable dynamics (PSNR **26.25**), **0.60** real deformable-manip score.
- **[[2604.21741|Hi-WM]]** — An ==interactive WM== that moves human intervention into ==state caching, trajectory rollback, branching== for virtual corrective supervision; **+37.9pp** avg real-world SR, ~**$100K** saved at scale by avoiding physical rollouts.

#### 5.2 Latent World Model

Attach a JEPA-style or latent-diffusion predictor to the VLA backbone — predictions happen in embedding space (~10ms) rather than video space (~150ms). The speed-quality sweet spot.

- **[[2607.01586|VLAFlow]]** — A unified ==flow-matching== framework comparing four training paradigms (action-only, language-supervised co-training, ==future latent alignment== via frozen ==V-JEPA 2==, and their joint combination); joint **MindLWPI** hits **99.1%** LIBERO / **74.8%** LIBERO-Plus — action-only pretraining alone is unstable.
- **[[2602.10098|VLA-JEPA]]** — A ==JEPA-style latent world model== predicting future latent representations + ==leakage-free state prediction== + ==learnable state-transition + action tokens== on Qwen3-VL + flow-matching action head; **97.2%** LIBERO + **79.5%** LIBERO-Plus + **65.2%** SimplerEnv Google Robot at **~10 ms/step**.
- **[[2603.03195|CoWVLA]]** — A VLA whose fine-tuned ==video VAE Latent Motion Extractor== disentangles static structure from dynamic motion, and an ==autoregressive VLA Decoder== aligns continuous ==latent motion== with discrete actions (==chain-of-world reasoning==); **95.6%** LIBERO, **76.0%** SimplerEnv-WidowX, latent-motion modeling (**0.877**) beating LAPA/villa-X.
- **[[2603.29844|DIAL]]** — A ==dual-system== VLA (System-2 VLM intent / System-1 policy) with a ==differentiable latent intent bottleneck==: System-2 predicts a future-subgoal ==latent intent== via ==latent world modeling==, System-1 decodes it through ==flow matching==; **70.2%** RoboCasa GR1 (vs GR00T-N1.6 **47.6%**), **10×** data efficiency (**58.3%** at 10% data).
- **[[2505.15659|FLARE]]** — A ==Future Latent Representation Alignment== method predicting compact future-state latents (not pixels) via an ==action-aware observation embedding== + ==diffusion transformer policy==, ==co-trained== on action-free human videos; up to **+26%** over baselines, **95%** real-world SR at just **100** trajectories/task, generalizes to novel objects from single demos.
- **[[2505.11528|LaDi-WM]]** — A latent diffusion WM with [[2304.07193|DINOv2]] + SigLIP + ==imagination-guided iterative action refinement==; **68.7%** LIBERO-LONG with 10 demos (**+15.1%** over SOTA).
- **[[2604.28192|LaST-R1]]** — A continuous ==latent CoT== VLA via DINOv3 embeddings + ==Latent-to-Action Policy Optimization (LAPO)== joint RL + ==adaptive latent CoT== with learnable stop token; **99.8%** avg LIBERO with **1-shot SFT** warm-up, **+44%** real-world avg, only **−8%** under unseen objects/backgrounds/lighting.
- **[[2604.17876|OFlow]]** — A ==shared semantic latent space== model on DINOv2 + ==causally-constrained Diffusion Transformer with flow matching== for future-semantic-state prediction + ==K-means object-aware factorization== + ControlNet; **96.6%** LIBERO, **72.3%** LIBERO-Plus, **85.6%** MT50, **69%** real avg (**+18pp** GR00T-N1.5) at **~30 Hz**.

#### 5.3 Video Co-Training

Video-prediction supervision at train time; deployment runs on distilled/compact representations only — no explicit video generation. The dominant 2026 efficient-WAM recipe.

- **[[2608.09771|SLIM]]** — A ==Mixture-of-Transformers== backbone couples ==inverse-dynamics flow-matching== + ==forward-dynamics L1== against an ==EMA== latent target, dropping future latents at deployment; **97.5%** LIBERO / **77.45%** LIBERO-Plus at **0.47B** params, **60.6ms** (**3.19x** faster than π0.5).
- **[[2607.08182|LEEVLA]]** — A VLA pairing ==Drift-Guided Dynamic Prioritization== (attention on task-critical, spatially-active regions) with ==Structured Feature Flow Generation== (==Prototype-to-Periphery prediction== + ==Mutual-Neighborhood Contrastive loss==) modeling latent environment evolution, training-only; **98.2%** LIBERO, **78.5%** real-world (vs OpenVLA's **40%**).
- **[[2603.16666|Fast-WAM]]** — A ==Mixture-of-Transformer== that decouples video co-training (train) from future-imagination (inference); ==structured attention== prevents future-video leakage; **91.8%** RoboTwin + **97.6%** LIBERO at **190 ms** inference vs **810 ms** imagine-then-execute variants (**4× faster**).
- **[[2511.07732|ViPRA]]** — A VLA learning motion-centric latent actions from videos + flow-matching action head, learning control priors from actionless video; **69.8%** SIMPLER, **79%** LIBERO-Long, **22Hz** real-time.
- **[[2602.12099|GigaBrain-0.5M*]]** — A world model predicting future states and values, with a ==RAMP== policy conditioned on those dense predictions; **+30pts** over RL baselines on long-horizon manipulation; **51.67%** RoboChallenge.
- **[[2604.25859|PFD]]** — A ==Privileged Foresight Distillation== method where a teacher sees real future frames and distills the ==foresight residual== into a small adapter; **98.1%** LIBERO (+1.15 over Fast-WAM), only **+2 ms/step**, **3.0–4.2×** faster than test-time generation.
- **[[2603.16195|S-VAM]]** — A ==self-distilling== geometric+semantic decoupler (DPAv3/DINOv2-supervised) that foresees representations in one forward pass, skipping multi-step video gen; CALVIN seq **4.16**, **72.8%** MetaWorld.

#### 5.4 Rehearsal & Forecasting

Compact, structured forecasting (dynamic regions/depth/semantics — never full pixel video) used either as training-only auxiliary supervision or as a lightweight non-pixel action-conditioning signal at inference — never a pixel-space rollout planner.

- **[[2509.24948|RehearseVLA]]** — A ==world-model-based virtual simulator== with ==VGGT + CLIP geometry features== injected into U-Net diffusion + ==VLM-guided instant reflector== with continuous reward + dynamic task-completion termination; **79.6%** LIBERO with only **5 demos/task** (vs **74.85%** OpenVLA-OFT), real clean-table **20% → 30%**.
- **[[2507.04447|DreamVLA]]** — A VLA that forecasts compact ==dynamic regions + depth + semantic features== via ==block-wise structured attention + disentangled queries== + a diffusion action head conditioned on world embedding; CALVIN avg length **4.44**, **92.6%** LIBERO, **76.7%** real-world (vs **50.8%** Diffusion Policy, **45.0%** Octo-Base).

#### 5.5 Unified VLA + WM

Single end-to-end architecture combining understanding, imagination, and action under a shared backbone or latent variable — joint video+action denoising active at inference. The tightest integration — strongest semantic transfer at moderate latency.

- **[[2602.15922|DreamZero]]** — A 14B ==autoregressive diffusion transformer== jointly predicting future video frames and robot actions, with **DreamZero-Flash** decoupling noise schedules for real-time control; **39.5%** unseen-task progress (vs **16.3%** SOTA VLA), **42%** cross-embodiment transfer from video-only demos, **7Hz** inference.
- **[[2601.16163|Cosmos-Policy]]** — A ==Cosmos-Predict2 latent video diffusion== fine-tuned as unified policy + world model + value function via ==latent-frame injection== (proprio + actions + states + multi-cam); SOTA **98.5%** LIBERO, **67.1%** RoboCasa, **93.6%** real ALOHA; model-based planning adds **+12.5pp** on hardest ALOHA tasks.
- **[[2607.24159|DeVA]]** — A ==decoupled Video-Action architecture== with video/action experts linked by ==multi-level feature interaction==, decoders predicting ==affordance== and ==relative-depth== maps for guidance; **72.0%** RoboCasa / **99.0%** LIBERO, **80.8%** LIBERO-Plus (**+11.2pp** over OpenVLA-OFT), **74%** real bimanual vs GR00T-N1.6's **48%** and Cosmos-Policy's **34%**.
- **[[2604.06168|Action-Images]]** — A representation encoding 7-DoF actions as ==multi-view 2D Gaussian heatmap action images== of EE-position/up/normal + ==unified video-action joint training== with diverse masking; zero-shot **60%** RLBench reach-target + **45%** real-world close-drawer (vs **0–20%** baselines); PSNR **23.48** vs **20.83** TesserAct.
- **[[2604.09330|VAG]]** — A ==dual-stream flow-matching== framework synchronously denoising video + action conditioned on an initial image + instruction, with an ==adaptive 3D pooling== module passing global video context to the action branch (no extra params); **45%** AgiBot SR (vs two-stage **29%**), and VAG-synthesized data lifts downstream VLA real SR **35%→55%**.
- **[[2602.10717|SDA]]** — A ==COSMOS-Predict2 video WM== ==adversarially distilled== for few-step inference + ==length-agnostic keyframe imagination==; FVD **571→212**, **98.1%** LIBERO — say-dream-act at deployment speed.
- **[[2603.00110|MCSWIM]]** — An autoregressive video-gen backbone repurposed as a ==multimodal continuous== video-action world model in a shared physical embedding (no quantization); **90.8%** LIBERO (+8.8 over WorldVLA), **74%** ManiSkill.
- **[[2603.10448|DiT4DiT]]** — A joint video-action model where a video DiT conditions an action DiT via denoising features; **98.6%** [[2306.03310|LIBERO]], **10x** sample efficiency.
- **[[2512.06963|VideoVLA]]** — A pretrained ==CogVideoX DiT== video generator repurposed into a manipulator, jointly denoising future video + action chunks in one ==unified multi-modal sequence==; **65.2%** SIMPLER novel-object SR, **+28.2pp** over 2nd-best on 8 novel skills; imagination quality predicts action reliability.
- **[[2604.26848|STARRY]]** — An ==action-centric world model== jointly denoising spatial-temporal latents + action sequences + ==Geometry-Aware Selective Attention Modulation (GASAM)== biasing attention toward EE-relevant tokens; **93.82%** RoboTwin 2.0 Clean (+0.89pp over LingBot-VA), **70.8%** real bimanual (+31.7pp over π0.5).
- **[[2604.27792|MotuBrain]]** — A ==UniDiffuser three-stream Mixture-of-Transformers== over video+action+text + ==4-level data pyramid== + ==two-stage pretrain== + inference stack (DiT cache + FP8); **95.8%** RoboTwin 2.0 Clean / **96.1%** Random; **EWMScore 63.77** WorldArena; **11 Hz** humanoid control with only **50–100** post-train trajectories.
- **[[2605.15153|Pelican-Unified]]** — A single-model unification of understanding + reasoning + imagination + action via a shared ==latent variable z== + ==UFG diffusion transformer==, jointly generating future video + actions; **64.7** VLM avg, **93.5%** RoboTwin, **1st** WorldArena.
- **[[2604.26694|X-WAM]]** — A unified 4D world-action model where a ==depth adaptation module== injects 3D awareness into a ==Diffusion Transformer== and ==Asynchronous Noise Sampling== aligns noise over a ==unified denoising sequence==; **79.2%** RoboCasa (**+12.1pp** over Cosmos Policy), **+2.34 dB** PSNR, **4.5×** action-latency speedup (4665→**1033 ms**) at **15 Hz**.
- **[[2604.14732|WVA]]** — A model combining a video generator, a trajectory-value head, and an action decoder with ==MPPI latent optimization==, planning implicitly through latent-space trajectory refinement; **98.1%** [[2306.03310|LIBERO]], **75.6%** real dual-arm.
- **[[2604.11135|AIM]]** — A model jointly predicting ==Action-based Spatial Value Maps== with future RGB frames as a spatial interface, where ==intent-causal attention== forces the action branch to read the future only through those maps + a ==self-distillation RL== stage on dense map-derived rewards; **94.0%/92.1%** RoboTwin Easy/Hard (**+15.3pp** over π0.5 hard).
- **[[2603.25406|MMaDA-VLA]]** — A native pretrained ==discrete-diffusion VLA== embedding language+vision+action in one token space, jointly predicting future ==goal observations + action chunk== via parallel iterative denoising (models dynamics without an auxiliary WM); **98.0%** LIBERO, **4.78** CALVIN ABC→D avg length, **83.3–93.3%** real AgileX Piper.
- **[[2506.19850|UniVLA]]** — An 8.5B autoregressive Transformer encoding all modalities as ==discrete tokens== + ==two-stage train== (action-free video WM post-train → action-annotated fine-tune); SOTA on CALVIN, **95.5%** LIBERO avg, **94.0%** LIBERO-Long; WM pretrain enables CALVIN gains with only **10%** fine-tuning data.
- **[[2511.17502|RynnVLA-002]]** — A ==Chameleon-initialized autoregressive== unified VLA+WM + ==attention masking for action gen== to mitigate error propagation + continuous ==Action Transformer head== with parallel learnable queries; **97.4%** LIBERO continuous-action, **>80%** real cluttered "Place the block"; integrated WM lifts real SR **+50%** in ablations.
- **[[2511.01718|UD-VLA]]** — A unified diffusion VLA synchronously generating future images + actions via a ==Joint Discrete Denoising Diffusion Process== in a single transformer with ==hybrid attention==, using visual foresight as an explicit chain-of-thought for action; **92.7%** LIBERO, **4.64** CALVIN ABCD avg length, **4.3×** faster inference than autoregressive, **>80%** real UR5e OOD.
- **[[2509.06951|F1]]** — A ==Mixture-of-Transformer== with Understanding/Generation/Action experts + ==goal-conditioned visual foresight== reframing action as ==foresight-guided inverse dynamics==; **82.2%** avg real Genie (vs π0 **65.2%**), **93.3%** handover.
- **[[2501.18867|UP-VLA]]** — A ==unified autoregressive== VLA (Phi-1.5) fusing continuous-encoder understanding + discrete-encoder future prediction + action in one sequence; CALVIN ABC→D length **4.08** (+33% SOTA), strong unseen-semantic real Franka.
- **[[2605.12167|MoLA]]** — A VLA where ==Stable Video Diffusion== imagines RGB rollouts + a ==Mixture of Inverse Dynamics Models== (modality-aware: semantic/depth/flow) infers latent actions; **92.7%** LIBERO-Plus (+13.2pp), **97.0%** LIBERO, **73.0%** real UR5e.
- **[[2603.10422|World2Act]]** — A ==latent action post-training== method aligning VLA actions to WM video-dynamics latents via contrastive matching (no pixel supervision) + LLM atomic-skill decomposition; **66.3%** RoboCasa with fewer demos, +2.5% GR00T-N1.6.
- **[[2605.21862|EvoScene-VLA]]** — A recurrent latent ==scene interface== (observation slots + action-updated prior slots) where the action decoder jointly denoises next chunk + scene state; **89.1%** RoboTwin Clean (+1.9), robust under randomized init.

**WM-Augmented VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Fast latent prediction (~10ms) | [[2602.10098\|VLA-JEPA]] or [[2603.03195\|CoWVLA]] |
| Production deployment (no test-time imagination) | [[2603.16666\|Fast-WAM]] |
| Iterative WM ↔ VLA co-improvement | [[2602.12063\|VLAW]] |
| Unified end-to-end VLA + WM | [[2605.15153\|Pelican-Unified]] (**93.5%** RoboTwin) or [[2601.16163\|Cosmos-Policy]] (**98.5%** LIBERO, model-based planning at test time) |
| Learn from action-free human video | [[2505.15659\|FLARE]] or [[2511.07732\|ViPRA]] |
| Rehearsal-only WM (training tool) | [[2509.24948\|RehearseVLA]] |
| Comprehensive forecasting auxiliary supervision | [[2507.04447\|DreamVLA]] (depth + semantics + dynamics) |
| RAMP-style dense WM conditioning | [[2602.12099\|GigaBrain-0.5M*]] (**+30pts** over RL baselines) |
| Latent diffusion WM for few-shot manipulation | [[2505.11528\|LaDi-WM]] (**+15.1%** over SOTA at 10 demos) |

^dm-5

> [!star] Key Papers
> - [[2602.10098|VLA-JEPA]] — Latent JEPA predictor attached to VLA; **~10ms** prediction in embedding space vs **~150ms** in video space; the right speed-quality trade-off
> - [[2603.16666|Fast-WAM]] — Video co-training without test-time imagination; WAM-level representations at VLA-level speed
> - [[2605.15153|Pelican-Unified]] — Single-model unification via shared latent z + UFG diffusion transformer; **93.5%** RoboTwin, **1st** WorldArena; the canonical unified architecture
> - [[2602.15922|DreamZero]] — Joint video + action prediction (14B WAM); the landmark zero-shot generalization paper for WAM-augmented VLAs

^key-papers-5

> [!tip] The Speed-Quality Trade-off
> WAM-augmented VLAs are more robust (spatiotemporal priors from video pretraining) but **4.8x** slower than pure VLAs ([[2603.22078|WAM-vs-VLA-Robustness]]). [[2603.16666|Fast-WAM]] shows you can get most of the benefit without test-time imagination — use video co-training, not video generation. Cross-reference [[06_WAM#2. VideoGen WAMs]] for the full WAM taxonomy and [[07_Latent-World-Models#2. JEPA Evolution: Visual-Only → Dense → Vision-Language → Vision-Language-Action]] for the JEPA lineage these latent-WM-VLAs descend from.

^insight-5

---

## Part B — Training, Specialization & Continual Learning

*Post-training recipes, force/humanoid specialization, and continual / self-evolving setups.*

### 6. RL Post-Training for VLAs

Imitation learning alone leaves performance on the table — SFT only reproduces demonstrated behaviors. RL pushes beyond the demonstration ceiling by optimizing for task success, but the *risk* of RL is degrading the VLM backbone's visual understanding. The cluster organizes around three resolutions of this tension: stabilize SFT itself to prevent collapse, engineer better reward signals, or apply parameter-efficient updates that keep the VLM backbone frozen.

#### 6.1 Conservative SFT & Stable Fine-Tuning

Stabilize the SFT side of the recipe so RL doesn't start from a damaged policy. Bound parameter disruption to preserve foundational capabilities.

- **[[2606.09009|SyVLA]]** — A dual-system VLA whose ==annotation-free Intention Decoupling== (gradient-norm masking separates control from reasoning) + ==Similar-Sample Guided RL== (fixed-advantage IL data merged into rollouts) stabilizes real-world RL against collapse; **0.73** ID / **0.64** OOD real SR, decoupling adding **+0.43**, no-RL-guidance collapsing to **0.00**.
- **[[2605.08879|ConSFT]]** — A conservative SFT method that exponentially down-weights low-confidence transitions to bound parameter disruption; **34%** [[2306.03310|LIBERO]] retention vs vanilla SFT collapse.
- **[[2501.16664|iRe-VLA]]** — A ==two-stage online RL ↔ SFT alternation== with ==LoRA== + frozen core VLM parameters; validated on Metaworld + Franka Kitchen + real Panda — the canonical stable RL recipe for VLAs.
- **[[2603.26666|VLA-OPD]]** — An on-policy distillation method with ==Reverse-KL== for dense token-level RL supervision from a frozen teacher's logits; **>90%** SR on LIBERO-Object within 10 steps and **3x** faster convergence than GRPO, lifting avg SR **48.9%→87.4%** on LIBERO and **45.2%→71.1%** on RoboTwin 2.0.
- **[[2502.05450|ConRFT]]** — A two-stage reinforced fine-tuning on a lightweight ==Consistency Policy== head: offline ==Cal-ConRFT== (==BC== + ==Cal-QL==) initializes from small inconsistent demos, online ==HIL-ConRFT== adapts with human-in-the-loop; **96.3%** across 8 real tasks (**+144%** over SFT), beating HIL-SERL **31.9%**.
- **[[2502.19645|OpenVLA-OFT]]** — A systematic FT-recipe study (==parallel decoding + action chunking + continuous actions + L1 loss==); **97.1%** LIBERO (from 76.5%), **26×** throughput (**109.7 Hz**). The canonical optimized-fine-tuning baseline.
- **[[2604.01570|FAN-Prior]]** — A ==Feasible Action Neighborhood== KL regularizer that shapes the policy toward a smooth unimodal Gaussian; **+11.7%** ID / **+5.2%** OOD on ManiSkill, OpenVLA-OFT to **98.8%** LIBERO-Spatial.
- **[[2509.11417|VLA-Pretrain-Preserve]]** — A ==partially-frozen dual encoder== (frozen high-level + trainable specialist) + string action tokenizer; **+40%** OpenVLA in sim, **76.6%** OOD visual robustness.
- **[[2509.02055|Align-Then-Steer]]** — An ==InfoVAE unified latent== that embeds adaptation actions into pretrain modes (reverse KL) + classifier-guidance steering; **+9.8%** RDT-1B / **+8.7%** π0 sim, **+32%** real dual-arm.
- **[[2505.19789|RL-for-VLA-Study]]** — An empirical RL-vs-SFT study on OpenVLA across a vision/semantics/execution generalization benchmark with an efficient PPO recipe; RL beats the strongest SFT baseline by **+42.6%** on unseen objects/tables — RL's gain is semantic + execution robustness, not visual.
- **[[2503.05833|Refined-Policy-Distillation]]** — An RL method distilling compact task-specific policies from generalist VLA teachers by folding a ==Behavioral-Cloning== MSE term into ==PPO== to guide exploration; outperforms vanilla PPO in sparse-reward settings, still beating PPO after a camera-angle shift collapses the teacher VLAs' own SR (Octo **67%→0%**, OpenVLA **27%→4.5%**).

#### 6.2 Reward Design & Q-Value Engineering

Design better reward and value signals — most VLA RL fails because the reward is sparse, the value estimate is unstable, or the policy can't bootstrap from offline data efficiently.

- **[[2608.13026|Temporal GRPO]]** — Aligns rollouts to a frozen planner's semantic stages as ordered credit intervals, then assigns per-stage normalized advantages under ==entered-stage gating== inside one clipped ==GRPO== update; **75.8%** RoboTwin 2.0 (vs **68.8%** SimpleVLA-RL), **99.1%** LIBERO-Long.
- **[[2608.05999|HiRoC]]** — A hierarchical VLA post-training framework decoupling an SFT-trained ==planner== generating executable subgoals from an executor trained via subgoal-conditioned SFT then ==hierarchical GRPO== combining task- and subgoal-level advantages; **93.5%** LIBERO SOTA (**+10.06pp**), best zero-shot generalization on all 7 LIBERO-Plus perturbations, validated sim-to-real.
- **[[2608.01013|OpenVLA-OFT-CDPR]]** — Aligns OpenVLA-OFT to a novel cable-driven robot embodiment via ==two-stage RL== (PPO directional control → GRPO object-conditioned commands) with a ==dense geometry-computed reward== and zero embodiment-specific demonstrations; directional SR **34.25%→53.50%**, **9.75%** object-conditioned strict SR with consistent target-approaching behavior.
- **[[2607.12892|UR-VC]]** — A training-free correction of time-derived progress labels: retrieves ==SigLIP-2==-similar states from other episodes under locality/similarity constraints, averaging their time labels to recover ==non-monotonic progress==; **98%** cross-episode coverage, flags **13.4%** of frames as local regressions, lifting real bimanual cloth flatten-fold SR **72.8%→78.9%**.
- **[[2606.17043|HABC]]** — A ==Hierarchical Advantage Weighting== online-RL fine-tuner decomposing sparse episode outcomes into a ==dual-head critic== (viability + efficiency) blended by a state-adaptive gate for per-transition flow-matching weights, plus ==intervention-aware credit assignment==; up to **92%** real bimanual SR with emergent autonomous error recovery.
- **[[2512.01801|GR-RL]]** — A multi-stage RL-augmented pipeline (data filtering + ==morphological-symmetry augmentation== + online RL) on a ==MoT== VLA with a ==multi-task distributional critic==, plus online latent-noise steering + critic distillation to fix the train-deploy mismatch; **83.3%** autonomous shoe-lacing (millimeter-precision soft-body), filtering+aug **45.7→83.3%**.
- **[[2511.15605|SRPO]]** — A ==self-referential progress reward== from the model's own successful trajectories via ==V-JEPA 2 latent world representations== + ==L2-distance clustering==; SOTA **99.2%** LIBERO (+103% rel. over 1-shot SFT) in only **200** RL steps, **+167%** rel. on LIBERO-Plus, Spearman **0.998** progress correlation.
- **[[2606.09630|ReCoVLA]]** — A failure-recovery framework training an additive ==residual== RL policy in a frozen VLA's latent space, where a VLM identifies failure categories/stages and a deterministic ==reward compiler== emits ==stage-gated rewards== activated only when preconditions hold; **36.7%→66.7%** sim SR, **61.7%** zero-shot physical, OpenVLA **23.3%→45.0%**.
- **[[2606.05468|FlowPRO]]** — A reward-free offline RL for flow-matching VLAs: ==RPRO== extends ==Proximalized Preference Optimization== to continuous actions with a ==proximal regularizer== anchoring implicit-reward magnitude to stop reward-hacking; highest SR / fastest completion across 4 bimanual tasks ($p<10^{-3}$); dropping the regularizer collapses to **13%/5%** SR.
- **[[2606.04968|ForesightFlow]]** — A ==potential-guided flow matching== method that augments the flow state with a ==success-potential vector==, so advantage is read off without a separate critic; matches separate-critic IDQL on BEHAVIOR-1K (**39.6%**), **35.4%** real bimanual SR while cutting training cost **38%**.
- **[[2606.02313|VLA-Aerial-Nav-GRPO]]** — An ==Expert-Guided GRPO (EG-GRPO)== that folds few-shot expert demos into the online RL loop to stabilize sparse-reward intent alignment for UAV navigation; SR **26.1% → 55.6%** (**+29.5pp**), **+60.9%** intent-alignment, zero-shot real-UAV transfer.
- **[[2605.13105|PAIR-VLA]]** — A method augmenting PPO with ==paired-view auxiliary objectives== (task-preserving + task-altering) for explicit behavior-level guidance under visual shift; **+9.10pp** OpenVLA (87.00%), **+16.62pp** π0.5 OOD.
- **[[2605.08774|ProcVLM]]** — A procedure-grounded progress reward via ProcCorpus-60M frame-level annotations; **+25.0pp** real-robot Stack-Bowls vs noisy teleop baseline.
- **[[2605.05544|AQC]]** — An Adaptive Q-Chunking method via a per-scale advantage criterion $(Q_k − V_k)/γ^k$ for offline-to-online RL; **100%** on OGBench cube-double, **63.2%** on RoboCasa-GR1 with GR00T N1.6.
- **[[2605.05172|Q2RL]]** — A method extracting Q-values from a BC policy via the ==Boltzmann assumption== to seed online RL with Q-gating; **3.75x** improvement on real robot in 1-2 hrs without original BC data.
- **[[2604.05614|GPLA]]** — An iterative ==preference learning (SimPO)== that refines a hierarchical VLA (high-level VLM decomposer + low-level action generator) scored by an ==action-conditioned grounding model==; near-supervised trajectory quality (MSE **0.045** vs **0.043** SmolVLA), **0.98** BERTScore coherence.
- **[[2604.17706|OmniVLA-RL]]** — An online VLA RL with spatial understanding: a ==Mixture-of-Transformers== with ==Spatial/Reasoning/Action experts== + ==Flow-GSPO== recasting deterministic ==flow matching== as an ==SDE== for stable exploration; **97.6%** LIBERO, **70%** LIBERO-Plus in the first **50 steps**, Flow-GSPO adding **+39.1%** over SFT.
- **[[2604.19730|FASTER]]** — A lightweight ==noise-level critic (Q_dn)==, modeling denoising as an ==MDP==, that filters unpromising initial noise before full ==diffusion-policy denoising==; **8× FLOP reduction**, **4.5×** training-update speedup, **1.7×** lower inference latency, scales to a **3.3B-parameter VLA** with **8× less compute**, matching base performance.
- **[[2604.27472|PRTS]]** — A ==Language-Conditioned Contrastive RL== with ==temporal weighting + bidirectional contrastive objective== + ==role-aware causal mask== (custom FlashAttention); SOTA **98.4%** LIBERO, zero-shot **81.4%** LIBERO-Plus + **58.8%** LIBERO-Pro, **73.8%** real-world robustness avg.
- **[[2604.18107|PDF]]** — An ==Uncertainty-Based Action Voting== + lightweight ==Perturbation head== with ==REINFORCE + KL regularizer==; **+8pp** on LIBERO over OpenVLA (**0.77** vs **0.69**), HNS **1.07** on Atari-57 (positive change on 47/57 games).
- **[[2509.15937|VLAC]]** — A model unifying actor + ==dense-reward critic== in one InternVL autoregressive model predicting pairwise progress; critic hits **0.95** VOC-F1 OOD one-shot, separates success/fail (**0.89** vs **0.44**).
- **[[2509.04063|ARFM]]** — An ==Adaptive Reinforced Flow Matching== that folds an RL advantage into the flow loss with an adaptive scaling factor; **92.1%** LIBERO (+4.5 over π0), **+11.4%** robustness to action noise.
- **[[2603.27670|ProgressVLA]]** — A frozen DINOv2+CLIP ==progress estimator== (normalized 0–1) guiding a two-stage latent ==diffusion policy==; **95.2%** CALVIN 1-in-a-row, **84.5%** LIBERO — dense progress without manual reward.
- **[[2603.15600|Active-Critic-RL]]** — A ==PRIMO-R1== method reframing progress estimation as generative reasoning + outcome-based ==GRPO==; MRA **82.90** (+9.10 over Qwen2.5-VL-72B) — RL elicits a progress critic.
- **[[2603.13925|SmoothVLA]]** — A ==physics-informed hybrid reward== (sparse task success + dense ==trajectory-jerk penalty==) optimized by ==GRPO== to resolve the exploration-stability paradox; **80.5%** LIBERO (**+6.6pp** over Octo), **+24.2%** LIBERO-Plus over SFT, smoothness **+4.5%** vs SFT.
- **[[2602.02454|World-Gymnast]]** — An imagined-rollout RL method fine-tuning VLA policies via ==RL inside an action-conditioned video WM== (WorldGym), a ==VLM (GPT-4o)== assigning binary task-completion rewards under ==GRPO== with KV-caching; up to **18×** real-robot SR over SFT (**72%** vs **4%**), **81%** held-out SR with synthesized distractors — beats software simulators on 3/4 tasks.
- **[[2602.00743|SA-VLA]]** — A ==spatially-aware flow-matching RL==: spatial-token fusion of multi-view features + ==step-level dense rewards== over Reach/Place/Leave phases (signed geometric-distance change) + ==Spatially-Conditioned Annealed Noise== for targeted exploration; **83.75%** SR with faster, smoother convergence than ablations.
- **[[2506.08440|TGRPO]]** — A method where an LLM auto-decomposes tasks into ==multi-stage dense rewards== + ==Trajectory-wise GRPO==; **80.7%** LIBERO over OpenVLA-SFT (76.5%) and DPO/GRAPE.
- **[[2505.18719|VLA-RL]]** — A framework formulating manipulation as ==multi-modal multi-turn conversation== + ==trajectory-level RL== + ==vision-language robotic process reward model== + GPU-balanced vectorized envs + critic warmup; **+4.5pp** over SFT on LIBERO matching π0-FAST commercial perf.
- **[[2503.08007|MoRE]]** — A scalable ==RL quadruped VLA== combining multiple ==LoRA experts== in a multimodal-LLM backbone with an RL objective + conservative regularization to learn from mixed-quality (including failed) trajectories; outperforms baselines across **6** quadruped skills in sim, real Unitree Go2 transfer, improved OOD generalization.
- **[[2412.09858|RLDG]]** — A method distilling task-specialized RL policies into a generalist VLA via filtered optimal rollouts; **+37%** Connector-Insertion, **+33%** FMB-Insertion over human-teleop baselines.
- **[[2411.19309|GRAPE]]** — A ==Trajectory-wise Preference Optimization== + ==Guided-Cost Preference Generation== that auto-synthesizes preference data; **+131.72%** Simpler-Env / **+11%** real over OpenVLA-DPO. The foundational preference-aligned VLA recipe.
- **[[2403.13358|QUARD-Auto]]** — A ==GeRM== decoder-only ==MoE VLA== trained with ==offline CQL== on 257K auto-collected quadruped episodes (success+failure); **71–90.5%** over 99 sub-tasks at **39.31M** active params; learns from mixed-quality data.
- **[[2604.08168|ViVa]]** — A ==Video diffusion Transformer== repurposed as a value function jointly predicting scalar value + future proprioception via ==normalized episode-success labels==; **73%** real-world box-assembly SR (vs **58%** VLM-based value, **42–53%** imitation-only) + robust pants-folding novel-object generalization.
- **[[2505.17016|RIPT-VLA]]** — A third training stage with ==binary success/failure rewards== via ==REINFORCE leave-one-out (RLOO) + PPO== + ==dynamic sampling==; LIBERO-90 SR **88.6% → 94.3%** (QueST), LIBERO-LONG **+21.2pp** (**50.2% → 71.4%**), **>80%** SR with single-demo training.
- **[[2510.00406|VLA-RFT]]** — A ==world-model simulator== that fine-tunes flow-matching VLAs via ==Generalized RPO== with dense WM feedback; **+4.5pp** LIBERO in only **400** iters, robust to OOD — RL without real rollouts.

#### 6.3 Parameter-Efficient & Knowledge-Preserving Updates

Apply LoRA, freeze the VLM backbone, or insulate gradients — preserve the VLM's broad spatial and semantic knowledge while allowing the policy to specialize.

- **[[2608.11363|MiDAS (Minimal-Data Adaptation)]]** — ==LoRA== BC anchors a task, then a frozen-backbone ==tanh-Gaussian residual actor-critic== predicts executed actions directly, stabilized by offline warmup + success balancing + ==Best-of-N== distillation; **91.2%** LIBERO-Long from **1** demo (vs **33.5%** BC).
- **[[2607.13429|Anchor-Align]]** — Adds two objectives to behavior cloning: ==Vision-Language Anchoring== distills layer-wise features from a frozen copy of the pretrained VLM, and ==Language-Action Alignment== turns continuous targets into discrete ==motion-direction labels==; **22.6%** on LIBERO-PRO position-swap (baselines ~0), GQA retention **6→70%**, alignment **16.8→78.4%**.
- **[[2607.10172|LoRA-VLA Efficiency Study]]** — Sweeps ==LoRA== rank **8–256** on π0 for industrial UR5e assembly to locate adapter capacity: **r ≥ 32** matches full fine-tuning on Average Task Progress (within **2pp**), cutting peak VRAM **~70%** (36.2→**10.8 GiB**) at **15%** trainable parameters — yet freezing the VLM or ==SigLIP== encoder collapses ATP to **~0.15**.
- **[[2505.23705|Knowledge-Insulation-VLA]]** — A ==stop gradient== method from the continuous ==action expert== into the VLM backbone, with a ==joint discrete + continuous action objective== and ==co-training== on general VL data to prevent ==catastrophic forgetting==; preserves visual representations during RL fine-tuning, converging up to **7.5×** faster than diffusion VLAs.
- **[[2601.14133|TwinBrainVLA]]** — An asymmetric dual-stream VLA preventing catastrophic forgetting via a frozen generalist ==Left Brain== + trainable ==Right Brain== bridged by an ==Asymmetric Mixture-of-Transformers== (unidirectional flow) feeding a flow-matching action expert; **+7.4pp** SimplerEnv / **+7.0pp** RoboCasa over Isaac-GR00T-N1.6, preserving VL understanding.
- **[[2603.11653|VLA-RL-Continual-Learning]]** — A Simple Sequential Fine-Tuning recipe (==LoRA== + RL) challenging the assumption that continual RL needs complex machinery; **<2%** Negative Backward Transfer across five lifelong RL benchmarks, with the final policy often beating the multi-task oracle on unseen tasks.
- **[[2603.03818|VLA-Continual-Learning]]** — A study of pretrained π0 + GR00T N1.5 + ==Experience Replay== with tiny buffers; **2–4×** lower NBT vs non-pretrained even with **2%** replay, and apparent forgetting recovers in **<10%** of original training steps — pretraining alters the continual-learning regime.
- **[[2510.05580|MetaVLA]]** — A backbone-agnostic ==Context-Aware Meta Co-Training==: a lightweight Attentive-Neural-Process ==Meta-Action-Reasoner== adapts from diverse context tasks via LoRA; **79.3%** LIBERO (+4.4 over OpenVLA), **−68.75%** training steps, consolidates 4 task models into 1 at **+0.3 ms**/token.
- **[[2605.21854|CrossVLA]]** — A tractable ==surrogate log-probability== (velocity-MSE) that makes ==DPO== work for flow-matching VLAs + LoRA/DoRA comparison; **+10.4pp** OpenVLA mean across LIBERO suites with KV-cache.
- **[[2605.10903|CapVector]]** — A method extracting ==capability vectors== (param difference between standard-SFT and auxiliary-objective-SFT models) and merging them into the base; matches Spatial-Forcing on LIBERO with fewer steps, and lifts OpenVLA-OFT's RoboTwin 2.0 avg SR from **6.7% → 31.8%** via transferable OOD gains.
- **[[2604.24182|M2-VLA]]** — A frozen VLM perceptual backbone + ==Mixture of Layers== extracting task-critical spatial features; **95.3%** LIBERO, **80%** real generalization while preserving VL reasoning.

#### 6.4 Scaling RL & Online / Distributed Fine-Tuning

The newest RL frontier is *systems*: distributed/asynchronous infrastructure that makes online RL tractable at fleet scale, and flow-native RL algorithms (modeling denoising as an MDP) that close the gap left by SFT. These papers are less about the reward and more about *throughput, stability, and the data flywheel*.

- **[[2607.29172|CLIFT]]** — A ==non-invasive, API-only== improvement loop for black-box models like Gemini Robotics On-Device (GROD): a ==preference-calibrated reward model== scores rollouts, ==retrieval-based advantage conditioning== labels chunks, then re-fine-tunes each cycle; lifts GROD SR **53–93%→96–100%**, beating episode-selection (**96%** vs **~84%** Bimanual Plate Handover).
- **[[2606.31846|Z-1]]** — An efficient RL post-training framework for flow-based VLAs applying task-wise ==GRPO== adapted to ==flow-SDE==, with ==Shared-Prefix/Tree-Structured Branching==, ==Success-Aware Reward Decay==, and ==Selective VLM-Action Expert Joint Training==; **80.6%** avg on 24 RoboCasa tasks (**+13.2pp** over SFT), beating X-WAM's **79.2%**.
- **[[2605.12236|TMRL]]** — ==Context-Smoothed Pre-training== injects diffusion noise into a policy's *input context*, expanding coherent action-support coverage; ==Timestep-Modulated RL== then exposes the diffusion timestep as an RL-controlled ==coverage dial==; **up to 200%** RL sample-efficiency gain on OGBench, enabling real-world π0 RL fine-tuning on WidowX/Franka Panda where DSRL fails.
- **[[2509.09674|SimpleVLA-RL]]** — A method extending ==veRL== with ==GRPO== + sparse ==binary outcome reward== for online VLA RL; **91% → 99.1%** LIBERO, big data-efficiency gain from a single trajectory. The canonical scalable online-RL recipe.
- **[[2510.06710|RLinf-VLA]]** — A unified framework across VLA architectures, RL algorithms (PPO/GRPO), and simulators with ==flexible GPU allocation==; **98.11%** LIBERO-130, **+20–85%** over baselines, **2.27×** training speedup.
- **[[2510.25889|piRL]]** — An online RL method for flow-based VLAs (π0/π0.5/GR00T) via ==Flow-Noise== (learnable noise network, denoising-as-MDP) + ==Flow-SDE==; **+29.2%** π0 / **+31.0%** π0.5, **98.3%** few-shot+RL.
- **[[2510.09976|FPO]]** — A ==likelihood-free policy ratio== from per-sample ==conditional flow-matching== loss changes makes PPO-style clipped RL tractable on flow VLAs like π0, with multi-step Euler latent-space exploration; **87.2%** LIBERO, **65.3%** LIBERO-Long, lifts π0 ~40→**>65%** on ALOHA Transfer-Cube.
- **[[2605.13276|D-VLA]]** — A ==Plane Decoupling== method isolating the high-freq data plane from the low-freq weight-control plane + a ==four-thread Swimlane== async pipeline; **+86.26%** throughput for π0.5 (237 steps/s) in distributed RL.
- **[[2605.00416|LWD]]** — A ==Learning While Deploying== data flywheel + ==Distributional Implicit Value Learning==; **0.95** avg SR across 8 tasks on a **16-robot** dual-arm fleet — fleet-scale continuous improvement.
- **[[2511.14659|NORA-1.5]]** — A 3B NORA backbone + flow-matching expert with ==DPO post-training== on OXE; **95.0%** LIBERO with consistent SimplerEnv + real Galaxea gains. Scalable preference post-training.
- **[[2511.14759|RECAP]]** — An ==RL with Experience and Corrections== method (advantage-conditioned policies) iterating autonomous rollouts + human interventions on π*0.6; doubles throughput, halves failures, **>90%** real laundry/espresso.
- **[[2605.22896|Agentic-VLA]]** — An agentic online-adaptation framework with ==Adaptive Reward Synthesis== (sub-goal-decomposed dense rewards), ==Language-Guided Exploration== (VLM suggestions over random), and an ==Experience Memory== for cross-task warm-start; **97.8%** LIBERO (+2.0 over EVOLVE-VLA), **2.4×** faster convergence, **31.2%** zero-shot transfer (vs 0%).
- **[[2605.19282|Pion]]** — A ==spectral high-pass momentum optimizer== (drop-in Muon replacement) with Promotion+Suppression Newton-Schulz; **100%** LIBERO-Object, **85.6%** real (vs Muon **38.9%**), prevents RLVR collapse.
- **[[2505.03238|RobotxR1]]** — A method extending ==R1-Zero== with LLMs in a closed-loop RL pipeline + SFT-then-RLVR; **+14.03pp** decision accuracy, Qwen2.5-3B beats GPT-4o (**63.3%** vs 58.5%) control adaptability.
- **[[2412.06685|PA-RL]]** — Decouples the RL algorithm from the policy class via ==global Q-value action selection== + ==local gradient ascent==, distilled into any backbone (Gaussian/diffusion/transformer), plugging into ==Cal-QL/IQL==; real OpenVLA fine-tuning **40%→70%** SR in 40 min. The policy-agnostic precursor to this section's flow-native RL work.

**RL Post-Training — Decision Matrix**

| Need | Recommendation |
|---|---|
| Stable VLA RL recipe (canonical baseline) | [[2501.16664\|iRe-VLA]] (RL/SFT alternation + LoRA + frozen VLM) |
| Preserve VLM backbone capabilities | [[2505.23705\|Knowledge-Insulation-VLA]] (stop-gradient) or [[2605.08879\|ConSFT]] (**34%** retention) |
| Bootstrap from BC policy without retraining | [[2605.05172\|Q2RL]] (**3.75x** in 1-2 hrs) |
| Offline-to-online RL with strong final performance | [[2605.05544\|AQC]] (**100%** OGBench cube-double) |
| Procedure-grounded reward (no manual reward eng.) | [[2605.08774\|ProcVLM]] (**+25.0pp** real-robot) |
| Deployment-loop RL | [[2505.17016\|RIPT-VLA]] |
| Continual / sequential task RL | [[2603.11653\|VLA-RL-Continual-Learning]] (LoRA + RL) |
| Preference-based alignment | [[2604.05614\|GPLA]] (SimPO) or [[2411.19309\|GRAPE]] (trajectory-wise TPO) |
| Spatial-understanding-aware RL | [[2604.17706\|OmniVLA-RL]] (Flow-GSPO) |
| Scalable online RL infrastructure | [[2510.06710\|RLinf-VLA]] (**+20–85%**, 2.27× speedup) or [[2509.09674\|SimpleVLA-RL]] (**99.1%** LIBERO) |
| Online RL for flow-based VLAs | [[2510.25889\|piRL]] (Flow-Noise denoising-as-MDP, **+31%** π0.5) |
| Fleet-scale deployment flywheel | [[2605.00416\|LWD]] (**0.95** SR on 16-robot fleet) |

^dm-6

> [!success] The RL Recipe for VLAs
> 1. ==SFT== on demonstration data (format learning) — use [[2605.08879|ConSFT]] to prevent collapse
> 2. ==RL with verifiable rewards== (task success signal) — use [[2605.08774|ProcVLM]] for dense progress reward
> 3. ==LoRA== for parameter-efficient updates ([[2501.16664|iRe-VLA]] alternation pattern)
> 4. ==Knowledge insulation==: keep VLM backbone frozen from action gradients ([[2505.23705|Knowledge-Insulation-VLA]])

> [!star] Key Papers
> - [[2505.23705|Knowledge-Insulation-VLA]] — Stop-gradient from action expert to VLM backbone preserves visual representations during RL fine-tuning
> - [[2501.16664|iRe-VLA]] — Two-stage alternation between online RL and SFT with LoRA + frozen VLM; the canonical stable RL recipe for VLAs
> - [[2505.17016|RIPT-VLA]] — Interactive post-training treats deployment trials as RL signal; closes the loop between deployment and learning

^key-papers-6

> [!tip] Why RL Works for VLAs
> VLAs pre-trained on diverse data already have good representations — RL doesn't need to learn from scratch. It just needs to *calibrate* the policy to the deployment environment. LoRA makes this cheap, and VLAs don't catastrophically forget ([[2603.03818|VLA-Continual-Learning]]). Cross-reference [[14_Egocentric-Pretraining-and-Human-Video#4. Pretraining Recipes — Three Generations]] for how egocentric pretraining + RL post-training compose, and [[06_WAM#5. VLM-Integrated WAMs]] for how VLM-integrated WAMs handle the same backbone-preservation problem. The algorithm-side treatment of the same optimizers — off-policy efficiency, flow-policy optimization — is [[03_Imitation-Learning-and-RL#4. RL Algorithms, Efficiency & Policy Representations]].

^insight-6

---

### 7. Multi-Sensor & Force-Aware VLAs

Vision-only policies fail on contact-rich tasks (insertion, assembly, surface following) because cameras cannot see force — visual feedback is delayed and ambiguous during contact. The architectural insight that emerged across this cluster is that **force should be treated as a first-class modality routed through dedicated experts**, not concatenated naively with visual tokens. Late-fusion of force after VLM encoding outperforms early concatenation by **10-20pp** on contact-rich benchmarks because the pretrained VLM representations are preserved rather than diluted with raw F/T noise. The cluster splits into two architectural strategies: force routed through dedicated MoE experts (first-class modality), or tactile signals fused into the visual stream (augmented vision).

> See [[11_Contact-Rich-and-Tactile-Control#1. Design-Space Principles]] for the full deep-dive — covering tactile sensor hardware ([[2509.18830|DexSkin]], [[2604.28156|FlexiTac]], [[2604.20689|FingerEye]]), the three landmark force-conditioned VLA architectures, force-as-generation-conditioning ([[2505.19386|Force-Prompting]]), contact-rich benchmarks, and open problems.

#### 7.1 Force as First-Class Modality

Route force through dedicated MoE experts with late fusion — preserves VLM representations while letting the policy specialize on contact dynamics.

- **[[2603.15169|ForceVLA2]]** — A ==Cross-Scale MoE== + VLM force prompts for contact-rich manipulation at **66%** avg SR (**+48pp** over [[2410.24164|π0]]); current SOTA.
- **[[2505.22159|ForceVLA]]** — A VLA routing 6-axis force/torque through a ==Force-aware MoE== for contact-rich manipulation; **+23.2%** over [[2410.24164|π0]]. The foundational late-fusion-with-phase-aware-gating pattern that defined the cluster.
- **[[2507.09160|Tactile-VLA]]** — A ==force-aware action expert== + CoT failure recovery; **90%** Charger, **80%** zero-shot blackboard wiping; autonomously adjusts force (3.5N → 6.7N).
- **[[2512.23864|DreamTacVLA]]** — A VLA grounded in ==contact physics== via hierarchical multi-scale tactile perception + ==predictive tactile modeling== on a hybrid sim-tactile + real dataset; **95.0%** Peg-in-Hole, **85.7%** USB Insertion, **81.1%** Gear Assembly — tactile imagination for contact-rich tasks.

#### 7.2 Multi-Modal Memory & Tactile-Fused Vision

Treat tactile / proprioceptive history as long-horizon perceptual memory; fuse it with the visual stream rather than routing through separate experts.

- **[[2606.29384|Event-VLA]]** — A robustness add-on fusing event-camera streams into a frozen VLA via ==Physical Residual Event Integration== (instantaneous/salient/persistent channels) + an ==action-conditioned gated cross-attention== interface injected post-backbone; **95.6%** severe-low-light sim SR (vs RGB-only's 69.6%), real near-dark **52.5%** vs 12.5%, no normal-light regression.
- **[[2606.17598|MuseVLA]]** — An adaptive multimodal-sensing VLA where the model emits a ==task-relevant sensor token== to select on-demand modalities, then renders them as ==grounded sensor images== (color-coded heatmaps overlaid on RGB) for one shared encoder; **76.4%** avg across thermal/acoustic/mmWave tasks (vs RGB-only **22.2%**), **13.23→6.61 GB**, **+39%** zero-shot.
- **[[2606.12105|DAM-VLA]]** — A ==decoupled asynchronous== multimodal VLA processing vision, force, proprioception, and language at their native sensor rates via per-modality latent buffers + ==Gated Cross-Attention== fusion of visual memory and force tokens; **95.2%** avg on seven contact-rich tasks (vs **40.95%** synchronous) at smooth **100 Hz** control.
- **[[2602.19764|DeMUSE]]** — A multi-sensory fusion in a ==Diffusion-Transformer== with ==AdaMN== + ==sparse MoE==; **83.2%** on MetaWorld MT50 (vs RDT-1B **77.9%**, RT-2 **52.2%**); MoE-4E cuts compute **42.6%** while raising SR over dense (**83.2%** vs **78.5%**).
- **[[2511.01210|OmniVLA]]** — A multi-sensor VLA fusing infrared, mmWave radar, and acoustic signals as ==sensor-masked images== (sensor heatmaps overlaid on Grounded-SAM2 semantic regions) into a frozen-encoder VLA with per-modality MLP projectors; **84%** real SR (**+59%** over RGB-only, **+28%** over raw fusion) on thermal/radar/acoustic-dependent tasks at ~50% fewer episodes.
- **[[2510.23763|OmniAction]]** — A ==RoboOmni== Perceiver-Thinker-Talker-Executor unifying speech/audio/vision/action, trained on the **141,162**-episode OmniAction dataset; **85.6%** on cross-modal contextual instructions vs NORA's 25.9%, **0.49×** latency vs ASR+OpenVLA.
- **[[2508.19236|MemoryVLA]]** — A bio-inspired ==Cognition-Memory-Action== framework whose ==Perceptual-Cognitive Memory Bank== stores perceptual + cognitive context, ==retrieving decision-relevant history==, ==gate==-fusing with observations, and ==consolidating==; **71.9%** SimplerEnv-Bridge (**+14.6pp** over CogACT-Large), **83%** real long-horizon (**+26pp**).
- **[[2501.04693|FuSe]]** — A finetuning recipe adding ==tactile + audio encoders== to generalist policies (Octo, PaliGemma-VLA), aligned by ==multimodal contrastive + generative language losses==; **>60%** real SR, strongest in visual occlusion, enabling cross-modal compositional prompting.

**Multi-Sensor VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Contact-rich manipulation SOTA | [[2603.15169\|ForceVLA2]] (**66%** SR, **+48pp** over [[2410.24164\|π0]]) |
| Foundational force-MoE baseline | [[2505.22159\|ForceVLA]] (Force-aware MoE) |
| Force in augmented action space + CoT recovery | [[2507.09160\|Tactile-VLA]] |
| Long-horizon perceptual memory | [[2508.19236\|MemoryVLA]] |
| Tactile hardware deep-dive | See [[11_Contact-Rich-and-Tactile-Control#2. Tactile Sensors as a Sensing Modality]] |

^dm-7

> [!star] Key Papers
> - [[2603.15169|ForceVLA2]] — Cross-Scale MoE + force prompts at VLM level; current SOTA at **66%** avg SR (**+48pp** over [[2410.24164|π0]])
> - [[2505.22159|ForceVLA]] — Foundational Force-aware MoE architecture; the late-fusion-with-phase-aware-gating pattern that defined the cluster
> - [[2507.09160|Tactile-VLA]] — Force in augmented action space + CoT failure recovery that autonomously adjusts force (3.5N→6.7N)

^key-papers-7

> [!tip] Late-Fusion Wins
> The cluster's design lesson: force must be late-fused after VLM encoding (not concatenated as another token), and routed through dedicated experts (not blended into the main attention stack). Cross-reference [[11_Contact-Rich-and-Tactile-Control#3. Force-Conditioned VLA Architectures]] for the full tactile hardware + force-conditioned VLA deep-dive, and [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks]] for the contact-rich benchmark landscape (insertion, assembly, wiping).

^insight-7

---

### 8. Humanoid & Bimanual VLAs

Single-arm tabletop manipulation is the default VLA setting — but real robots have two arms, legs, and whole-body coordination. The DoF jump alone is substantial (7 → 14 → 50+), and the *coordination* requirement compounds it: bimanual tasks demand synchronized timing across arms, humanoids couple every joint via balance constraints. The cluster splits along these two axes — bimanual composition (synchronize two arms) vs whole-body humanoid control (balance-aware policy) vs cross-embodiment multi-platform stacks that generalize across both.

#### 8.1 Bimanual Manipulation

The 14-DoF coordination problem: two arms must be synchronized in time and space, not just controlled independently.

- **[[2606.13279|Dual-Level-Bimanual-VLA]]** — A ==Dual-Level Structural Decomposition== framework augmenting a VLA with a ==View-Selective Visual Router== (dynamic wrist-view weighting) + an ==Interaction-Aware Action MoE== (coordinated vs arm-wise pathways); up to **+37%** absolute sim and **+50%** real-world hard-setting SR over monolithic baselines.
- **[[2605.18722|Dexora]]** — An open-source dual-arm dual-hand ==36-DoF== platform (two 6-DoF arms + two 12-DoF XHANDs) + a hybrid exoskeleton/Vision-Pro teleop pipeline + a ==discriminator-guided quality-aware== training recipe; **89.6%** basic / **66.7%** dexterous real tasks (beats GR00T N1, π0), transfers to lower-DoF embodiments.
- **[[2603.03836|SkillVLA]]** — A dual-arm VLA fighting ==skill entanglement== via a two-level architecture (high-level VLM emits per-arm sub-prompts → separate low-level experts) + an ==adaptive cooperation estimator== predicting a scalar α gating cross-attention; **51%** on novel skill combinations (baselines ~0%), **−21%** completion time, strong with **5** demos.
- **[[2511.05275|TwinVLA]]** — A composition of two ==pre-trained single-arm VLAs== with shared encoder + ==Joint Attention== + ==MoE== on shared inputs + ==attention re-weighting==; requires only **~50** bimanual episodes + **~25 H100-days**; **76%** real Anubis (vs **45%** RDT-1B); **75.8%** Tabletop-Sim Easy vs **61.6%** RDT-1B.
- **[[2410.07864|RDT-1B]]** — A **1.2B** ==Diffusion Transformer== pretrained on **1M+** trajectories from 46 robot datasets via a ==Physically Interpretable Unified Action Space==, then fine-tuned on 6,000 bimanual demos; **56%** avg SR improvement over SOTA baselines on real ALOHA, adapting to new skills from just **1–5** demos — the canonical scaled-bimanual baseline.

#### 8.2 Whole-Body Humanoid Control

Coordinate arms, legs, and torso in a high-dimensional action space where balance constraints couple every joint. Requires dual-process architectures (slow reasoning + fast reactive control) and proprioception-aware prediction.

- **[[2506.13751|LeVERB]]** — A whole-body humanoid VLA (Unitree G1) via a latent vision-language "verb" vector + ==dual-process control== (10Hz VLA reasoning / 50Hz reactive WBC); residual ==CVAE== for VL alignment + ==DAgger== distillation; **58.5%** sim, **7.8x** over naive hierarchical VLA (vs **7.5%** naive hierarchical), zero-shot sim-to-real.
- **[[2604.07993|HEX]]** — A ==hierarchical== humanoid VLA (high-level policy + ==RL whole-body controller==) with a ==Unified Proprioceptive Predictor== using a ==morphology-based MoE== + a ==review-and-forecast== visual-history cache; **79.8%** in-distribution real (vs GR00T-N1.5 **70.2%**), **61.8%** across unseen scenes (vs π0.5 **44.3%**).
- **[[2603.12263|Psi0]]** — A ==triple-system==: Qwen3-VL (System-2) + ==Multi-modal Diffusion Transformer== action expert (System-1) + RL lower-body controller (System-0) + ==Real-Time Action Chunking==; **+40pp** avg over GR00T N1.6 on 8 long-horizon loco-manipulation tasks using only **800 hr** human video + **30 hr** robot data.
- **[[2502.14795|Humanoid-VLA]]** — A first humanoid VLA with ==Language-Motion Pre-Alignment== + ==Vision-Conditioned Fine-Tuning== + ==self-supervised compositional motion quantization==; FID **0.467** HumanML3D (**+47.5%** vs MDM); real Unitree G1 hits **10/10** Turn-to-object + **9/10** Hold/Kick.
- **[[2512.20188|DuoCore-FS]]** — An asynchronous fast-slow whole-body VLA where a slow VLM (1–3 Hz semantic reasoning) and a fast diffusion policy (25–30 Hz, 25-DoF) exchange state through a ==differentiable bridge buffer==, with a ==geometry-aware RVQ-VAE action tokenizer== + cross-timescale co-training; **90%** SR at **32.3 Hz** (~3× synchronous), **50%** OOD (vs 10%).
- **[[2512.11047|WholeBodyVLA]]** — A ==unified latent learning== VLA with separate ==VQ-VAE LAMs== for manipulation + locomotion (action-free human egocentric video) + ==LMO RL policy==; **78.0%** avg on Bag-Packing/Box-Loading/Cart-Pushing whole-body loco-manipulation.
- **[[2604.19734|UniT]]** — A ==Unified Latent Action Tokenizer== that, via ==Visual Anchoring==, projects human + humanoid behaviors into a shared token space + ==tri-branch encoder== with Residual-VQ; **66.7%** RoboCasa, **10×** data efficiency, real human→humanoid transfer.
- **[[2508.16943|LHM-Humanoid]]** — A ==dual-teacher== distillation of loco-manipulation policies into a unified VLA policy; **71.14%** Success-All (vs end-to-end RL **0.00%**), generalizes to **66 unseen** long-horizon whole-body tasks.

#### 8.3 Cross-Embodiment & Multi-Platform

Foundation models designed to generalize across embodiment classes (single-arm, bimanual, humanoid) with shared backbones or token spaces.

- **[[2606.12352|CHORUS]]** — A decentralized multi-robot framework adapting a pretrained π0.5 into one ==shared policy== where each robot runs an independent copy on local observations + a robot-identifying prompt (no inference-time communication), pooled-trajectory flow-matching fine-tuned; **+64pp** mean SR over decentralized diffusion, **90%** three-robot transport.
- **[[2604.07430|HY-Embodied-0.5]]** — A foundation model family with ==MoT== (Mixture of Transformers); leads **16/22** embodied benchmarks across multi-embodiment.
- **[[2602.12062|HoloBrain-0]]** — An embodiment-prior-aware end-to-end VLA + ==RoboOrchard== open-source ecosystem + ==SimpleRTC asynchronous inference== + ==Teacher Forcing==; **0.2B** variant hits **90.8%** RoboTwin 2.0 + **74.0%** zero-shot LIBERO-Plus + **+5.65–8.02pp** over π0.5 on 10 real tasks.
- **[[2512.00975|MM-ACT]]** — A unified discrete-token text+image+action model via ==mask token predictor== + ==Context-Shared Multimodal Learning== + ==one-step parallel decoding==; **96.3%** LIBERO, **72.0%** real Franka, **52.38%** RoboTwin2.0 bimanual unseen, **0.22s** for 8-chunk action at up to **40 Hz**.

#### 8.4 Dexterous-Hand VLAs

Multi-finger dexterous hands are the highest-DoF embodiment, and the hardware varies wildly (4–24 joints, different kinematics). The shared move here is a *hand-agnostic latent action space* — train the policy on a shared code and let per-hand encoders/decoders absorb the morphology — so one VLA serves many hands and skills transfer across them.

- **[[2603.10158|XL-VLA]]** — A VLA whose per-hand ==latent encoders/decoders== form a shared, embodiment-invariant ==multi-headed VAE== action space the policy operates entirely within; **0.72** mean SR over 4 hands × 10 tasks (**+40%** rel. over π0), **57%** rel. gain co-training a Unitree G1, beating kinematic-retargeting zero-shot.
- **[[2603.00732|UniHM]]** — A ==morphology-agnostic VQ-VAE== tokenizer that gives diverse hands a shared latent + a Qwen3-0.6B VLM (progressive-masking curriculum) generating sequences refined by a ==physics-guided optimization== module; **61.40** MPJPE on DexYCB-Seen (lower than SOTA baselines) and **65%** real-world "Grab" SR across hand setups.
- **[[2512.24210|GR-Dexter]]** — A 4B-parameter ==Mixture-of-Transformer== VLA driving a 21-DoF tactile-sensing ==ByteDexter V2== bimanual hand, co-trained on a multi-source ==data pyramid== (teleop + web VL + cross-embodiment + 800h human-egocentric video) via ==dynamic mixing==; **0.97→0.89** ID→OOD makeup-decluttering SR (vs plain-VLA's **0.64** OOD), **0.85** SR on 23 unseen objects.
- **[[2502.20900|DexGraspVLA]]** — A hierarchical dexterous-grasping VLA pairing a high-level VLM planner (Qwen) emitting ==domain-invariant bounding-box affordances== with a low-level ==DiT closed-loop policy== over frozen-foundation-model (SAM/DINOv2) ==domain-invariant features==; **90.8%** zero-shot grasping across 1,287 unseen object/lighting/background combos, **89.6%** "clear the table".

**Humanoid & Bimanual — Decision Matrix**

| Need | Recommendation |
|---|---|
| Bimanual via composition (data-efficient) | [[2511.05275\|TwinVLA]] |
| Scaled bimanual foundation model | [[2410.07864\|RDT-1B]] (1.2B diffusion) |
| Whole-body humanoid (Unitree G1) | [[2506.13751\|LeVERB]] (**58.5%** sim, **7.8x** over hierarchical) |
| Cross-embodiment humanoid | [[2604.07993\|HEX]] (MoE proprioceptive predictor) |
| Humanoid loco-manipulation (open) | [[2603.12263\|Psi0]] |
| Multi-embodiment foundation | [[2604.07430\|HY-Embodied-0.5]] (**16/22** benchmark wins) |
| First-VLA-for-humanoid baseline | [[2502.14795\|Humanoid-VLA]] |
| Open-source full-stack ecosystem | [[2602.12062\|HoloBrain-0]] |

^dm-8

> [!star] Key Papers
> - [[2506.13751|LeVERB]] — Latent vision-language "verb" vector + dual-process control (10Hz VLA / 50Hz WBC); **58.5%** sim, **7.8x** over naive hierarchical; canonical whole-body humanoid VLA
> - [[2511.05275|TwinVLA]] — Compose two single-arm VLAs for bimanual tasks; coordination as a thin layer on top of individual skill; data-efficient
> - [[2410.07864|RDT-1B]] — 1.2B diffusion foundation model for bimanual manipulation; the canonical scaled-bimanual baseline
> - [[2604.07430|HY-Embodied-0.5]] — Foundation model family with MoT for multi-embodiment; leads **16/22** embodied benchmarks

^key-papers-8

> [!tip] Bimanual Scaling
> [[2511.05275|TwinVLA]] shows you can compose two pre-trained single-arm VLAs rather than training a bimanual model from scratch — data-efficient and surprisingly effective. The key insight: coordination can be learned as a thin layer on top of individual skill. For humanoids, the dual-process pattern ([[2506.13751|LeVERB]]'s 10Hz reasoning + 50Hz reactive WBC) is the canonical resolution of the high-DoF / balance-constraint tension. Cross-reference [[14_Egocentric-Pretraining-and-Human-Video#5. Transfer Mechanisms — Hand → Gripper]] for egocentric humanoid loco-manipulation transfer (kinematic alignment) and [[02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation]] for the humanoid benchmark landscape. The controller layer these humanoid VLAs sit on top of is [[12_Whole-Body-and-Locomotion-Control#1. Whole-Body Control & Coordination]].

^insight-8

---

### 9. Self-Evolving & Continual VLAs

VLAs that autonomously improve through self-play, continual learning, or evolutionary strategies. The cluster organizes around the *source* of the improvement signal — sequential task fine-tuning (continual learning), error detection and recovery mid-task (self-correction), or evolutionary / counterfactual exploration of policy variants. The 2026 result that unites the cluster: pre-trained VLAs on diverse cross-embodiment data are *naturally* resistant to catastrophic forgetting — the opposite of the NLP literature. See [[16_Self-Evolving-VLA-WAM#2. Self-Evolving Agent vs VLA vs WAM]] for the full deep-dive comparing self-evolving VLAs, WAMs, and agents.

#### 9.1 Continual Learning Across Tasks

Sequential task fine-tuning with parameter-efficient updates (LoRA) preserves prior capabilities — the conventional NLP wisdom that "fine-tuning destroys prior knowledge" does not hold for VLAs trained on diverse data.

- **[[2608.05970|SkillMemo]]** — ==Expert-Guided Trajectory Segmentation== (MoE + synergy loss) decomposes demos into atomic skills stored in a ==Skill-Level Memory Architecture==, retrieved to fuse expert-activation profiles with the policy's gating at inference; **98.0%** with a π0.5 backbone, unseen LIBERO-Spatial **75.6%** (vs 72.1% baseline).
- **[[2605.15735|UAM]]** — A framework reframing catastrophic forgetting as the ==embodiment tax== (unfreeze kills understanding, freeze kills action); ==dual-stream== VLM **Semantic Expert** + parallel **Dorsal Expert** (UMM prior + visual-dynamics objective); retains **>95%** MMMU/MME/MMBench/TextVQA while improving OOD bimanual ALOHA.
- **[[2603.03818|VLA-Continual-Learning]]** — A study showing pretrained VLAs (π0, GR00T N1.5) achieve **2–4×** lower NBT even with **2%** replay, recovering "forgotten" skills in **<10%** original training steps — simple sequential fine-tuning works.
- **[[2603.11653|VLA-RL-Continual-Learning]]** — Sequential ==LoRA==-based RL fine-tuning across five lifelong benchmarks with **<2%** Negative Backward Transfer, robust across OpenVLA and π0 and task orderings — the RL-side twin of [[2603.03818|VLA-Continual-Learning]]'s SFT result.
- **[[2602.03445|CRL-VLA]]** — A ==dual-critic architecture== (frozen Goal-Conditioned Value critic + trainable Monte Carlo critic) + ==asymmetric regulation== with PPO+KL; achieves positive Backward Transfer **0.17** + Final Average Return **0.74** in multi-task.
- **[[2602.10503|Long-Lived-Robots]]** — A ==LifeLong-RFT== recipe: chunking-level on-policy ==GRPO== + ==Multi-Dimensional Process Reward (QACR+CTAR+FCR)==; **+8.7pp** real Franka multi-task, **+19.6pp** forward transfer on LIBERO continual + NBT **1.5 vs 6.8** SFT, using only **20%** of SFT data.
- **[[2603.09030|PlayWorld]]** — An ==autonomous robot self-play== method with a VLM ==Task Proposer== + ==curriculum learning== on Stable-Video-Diffusion; Pearson **0.8766** with real-world policy success, **+65%** real-world SR via in-model fine-tuning — the "free data" continual recipe.
- **[[2605.29562|VLA-Pro]]** — A method storing ==per-task LoRA procedural-memory adapters== over a shared base + structured procedural states; **+207%** unseen RoboTwin (RDT) / **+47%** (π0.5), **+7.1pp** RLBench zero-shot — cross-task procedural transfer.
- **[[2511.18085|Stellar-VLA]]** — A ==Dirichlet-Process== non-parametric model (DPMM/HDP) for an adaptively expanding knowledge space + VAE self-supervised cycle; **>50%** avg improvement on LIBERO with reduced NBT.
- **[[2601.09512|CLARE]]** — A modular ==low-rank adapters== per task (freeze old) + ==autoencoder routing==; **75.11%** AUC (DiT-Dec, +15% over exemplar baselines), near-zero NBT — autonomous continual adaptation.
- **[[2605.26820|VLA-Continual-Forgetting]]** — A real-world sequential 4-task study: naive FT drops avg **99.2→17.8**, but ==experience replay== at 0.2 buffer/freq keeps all tasks within **10pp** — the real-world replay-budget result.
- **[[2510.12710|Reflective-Self-Adaptation]]** — A ==dual-pathway== method learning from failures + successes where VLM causal failure analysis synthesizes ==dense adaptive rewards==; **83.6%** LIBERO with faster convergence, no human intervention.
- **[[2511.02239|LACY]]** — A unified ==Language↔Action cycle== (L2A/A2L/L2C) with a ==self-improving L2A2L loop== + filtering; **95%** L2A, **76%** A2L in sim, self-improvement boosts A2L to **85%** — language-action consistency as self-supervision.

#### 9.2 Self-Correction & Failure Recovery

Detect errors mid-task and recover — a stronger form of autonomy than continual learning. The agent monitors its own confidence or subtask completion, backtracks when it goes wrong, and avoids continuing with a doomed plan.

- **[[2605.09410|RePO-VLA]]** — A method where ==Recovery-Aware Initialization== + ==Value-Conditioned Refinement== structurally reuse successful/failed/recovered trajectories; recovery SR **15→37%** (clean) / **15.4→43%** (randomized) under injected failures.
- **[[2601.02295|CycleVLA]]** — A proactive self-correction VLA fine-tuned with explicit ==stop/progress signals== on LLM-decomposed subtasks, where an off-the-shelf VLM does zero-shot ==failure prediction== (`transit` vs `backtrack`) and ==Minimum Bayes Risk (MBR) decoding== picks robust recovery actions; **95.3%** LIBERO (vs OpenVLA **76.5%**), MBR adding up to **+9.9%**.
- **[[2602.21633|SC-VLA-WorldImagination]]** — A two-stage ==Sparse World Imagination + Online Action Refinement== via ==residual RL== with ==intrinsic dense rewards== from SPI physical-evolution prediction; **86%** ManiSkill3 (vs **72%** GR00T N1.5, **55%** π_0), **−43%** steps to success, **71%** real ARX5 (vs **57%** GR00T N1.5).
- **[[2605.01191|Sentinel-VLA]]** — A ==metacognitive architecture== with a ==Status Monitor Expert== for on-demand error reasoning + ==EC-Gen== error-annotation pipeline; **63.5%** seen / **51.3%** unseen RLBench (vs π0 57.8/42.0) at **13 ms/action**.
- **[[2602.01811|VLA-SCT]]** — A ==training-free== modular control layer: ==Trajectory Evaluation== + ==Grasp Perturbation== for self-correction and termination; **81.55%** LIBERO (+6.1pp over OpenVLA) without retraining.
- **[[2512.03913|VINE]]** — A hierarchical System-2 planner + System-1 executor with a ==failure-aware value estimator== (trained on successes + failures); **+17.4%** relative over VLM-as-planner on unseen plug-insertion vs π0.
- **[[2512.02787|ViFailback]]** — A method where ==seven explicit visual symbols== (arrows/crosshairs/labels) annotate failures for multimodal corrective guidance + 5.2K-sample dataset; ViFailback-8B **93.70%** closed / **72.64%** open (+39.14% over Gemini-2.5-Pro).
- **[[2509.14889|CollabVLA]]** — An InternVL2.5 + ==MoE== + ==diffusion DiT== VLA unifying reasoning, reflection, and action with a ==dream-together== self-reflective stage; **88.6** CONREF, best across all 8 Simpler-Collab subtasks while preserving VLM skills.
- **[[2405.17418|SC-VLA]]** — A dual-process ==fast 6-DoF pose + slow reflective error correction== with adaptive expert feedback; **87%** seen / **68%** unseen sim (+30%/+21% over ManipLLM). The foundational fast/slow self-correcting VLA.
- **[[2406.11548|AIC-MLLM]]** — An MLLM that predicts manipulation poses + comprehends ==visual+textual correction prompts== (mask positional, highlight rotational errors); **0.75** unseen-category sim SR, strong real Franka recovery.

#### 9.3 Evolutionary & Counterfactual Adaptation

Explore policy variants via evolutionary strategies or counterfactual reasoning — learn from hypothetical alternatives, not just observed failures.

- **[[2511.16166|EvoVLA]]** — The first end-to-end self-evolving VLA framework, combatting ==stage hallucination== via a ==Stage-Aligned Reward== and ==fragile memory== via ==Long-Horizon Memory== + ==Pose-Based Object Exploration==; **69.2%** sim SR (**+10.2pp** over baselines), hallucination rate **38.5%→14.8%**, **1.5x** sample efficiency, **54.6%** real-robot SR (**+11.0pp**).
- **[[2512.24426|CF-VLA]]** — A ==counterfactual self-reflection== VLA: a ==self-reflective loop== anticipates consequences and revises plans, ==time-segmented meta-actions== abstract behavior, and a ==rollout-filter-label pipeline== auto-mines counterfactual scenarios; cuts collisions **25–30%** with **9–10%** lower MinADE/MinFDE and ~**50%** lower think-rate.

**Self-Evolving VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Sequential task continual learning | [[2603.11653\|VLA-RL-Continual-Learning]] (LoRA + RL) |
| Evidence that VLAs resist forgetting | [[2603.03818\|VLA-Continual-Learning]] |
| Proactive self-correction at runtime | [[2601.02295\|CycleVLA]] (subtask backtracking + MBR) |
| End-to-end self-evolution framework | [[2511.16166\|EvoVLA]] (overcomes stage hallucination) |
| Counterfactual reasoning over alternatives | [[2512.24426\|CF-VLA]] |
| Long-lived deployment continual learning | [[2602.10503\|Long-Lived-Robots]] |
| Self-play world-model training | [[2603.09030\|PlayWorld]] |

^dm-9

> [!star] Key Papers
> - [[2511.16166|EvoVLA]] — First end-to-end self-evolving VLA; overcomes stage hallucination and fragile memory through evolutionary strategies
> - [[2603.03818|VLA-Continual-Learning]] — Showed pre-trained VLAs are naturally resistant to catastrophic forgetting; simple sequential fine-tuning works
> - [[2601.02295|CycleVLA]] — Proactive self-correction via subtask backtracking and MBR decoding; detects and recovers from errors without restarting

^key-papers-9

> [!tip] The Continual Learning Surprise
> Two independent studies ([[2603.11653|VLA-RL-Continual-Learning]], [[2603.03818|VLA-Continual-Learning]]) found the same result: VLAs pre-trained on diverse data are *naturally* resistant to catastrophic forgetting. You don't need complex continual learning algorithms — simple sequential fine-tuning works. This is the opposite of what the NLP literature suggests. ==LoRA=='s low-rank constraint further stabilizes this: updates are confined to a low-dimensional subspace, preserving the vast majority of pre-trained parameters. Cross-reference [[16_Self-Evolving-VLA-WAM#6. Self-Evolving VLAs]] for the full self-evolution deep-dive across VLAs / WAMs / agents, and [[06_WAM#7. Self-Evolving WAMs]] for the WAM-side self-evolution mechanisms (reflective planning, self-play, RL co-evolution).

^insight-9

---

## Part C — Capabilities, Foundations & Evaluation

*Beyond the Markovian tabletop: memory and long horizons, cross-embodiment transfer, runtime adaptation, safety, the generalist foundation-model layer, embodied-VLM brains, and the evaluation methodology that keeps all of it honest.*

### 10. Memory-Augmented & Long-Horizon VLAs

Most VLAs assume the Markov property — the next action depends only on the current frame. This breaks on long-horizon tasks where the right action depends on *what already happened*: which drawer was opened, which object was already placed, where a now-occluded target used to be. The cluster splits along *what is remembered*: persistent spatial/object memory that survives occlusion and viewpoint change, vs. progress/hindsight state that tracks how far the task has advanced. The shared move is to break the single-frame assumption with an explicit, compressed memory the policy can attend over.

#### 10.1 Persistent Spatial & Object Memory

Maintain a durable representation of the scene — a 3D voxel map, an episodic keyframe store, or object slots — so the policy can act on objects that have left the camera view or whose identity must persist across time.

- **[[2608.09410|HyMeS]]** — ==Flow-matching== fine-tunes motor skills in weights while a coding agent revises an executable memory-update program from rollout traces, gated by **PACE** multi-frame ==Qwen3-VL-8B== verification; **66.2%** cumulative SR on RoboMemArena (**+4.5pp**).
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

#### 10.2 Progress-Aware & Hindsight Control

Track *task progress* explicitly — a scalar or structured estimate of how far the task has advanced — and use past dynamics (hindsight) to disambiguate the current step. This corrects error accumulation that pure reactive policies suffer on long horizons.

- **[[2608.02326|ChainVLA]]** — A unified, revisable ==execution state== (Progress Context + Motion Tail) explicitly passed across successive VLA queries so task evidence and unexecuted motion both persist across replanning; **62.8%** RMBench (vs Mem-0's 52.8%), **98.8%** avg LIBERO; ablating either component collapses SR to **11.2%/3.0%**.
- **[[2606.17463|WeaveLA]]** — An event-driven action-side ==latent memory weaving== interface bolted onto a frozen VLA backbone that writes a ==Memory Weaver==-compressed task state at sub-goal completion events to condition the next action expert via memory-conditioned AdaRMS; lifts RoboMME avg SR **19.0%→24.7%** and SWINGXTIMES **0%→47.8%** on repetition tasks.
- **[[2603.09292|See-Plan-Rewind]]** — A ==See-Plan-Rewind== cycle that decomposes tasks into spatially-grounded 2D subgoals with explicit ==error-recovery rewind==; **91.8%** LIBERO (+5.0 over MolmoAct), SOTA OOD robustness on LIBERO-Plus.
- **[[2604.17880|ST-π]]** — A ==Spatiotemporal VLM== that decomposes tasks into ==causally-ordered chunk-level prompts== (semantic + spatial + temporal) + ==Spatiotemporal Action Expert==; highest SR and shortest completion across four LIBERO suites, surpassing OpenVLA, Octo, SpatialVLA, TraceVLA, 4D-VLA, CogACT, and π0.5, plus leads all three real STAR-dataset suites.
- **[[2512.09928|HiF-VLA]]** — A ==Hindsight-Insight-Foresight== bidirectional temporal reasoning over compact codec ==motion vectors== (past/current/future dynamics); **94.4%/96.4%** LIBERO-Long third/multi-view at negligible overhead.
- **[[2508.19958|Long-VLA]]** — An end-to-end long-horizon VLA that decomposes trajectories into ==moving vs interaction phases== with a phase identifier + a ==dynamic binary input-masking== that selectively attends to phase-relevant views (third-person for moving, ego for interaction); up to **+81%** rel over base on 10-step L-CALVIN (avg length **8.24**), real 8-step where baseline fails.

**Memory-Augmented VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| Act on out-of-vision objects | [[2605.22283\|SOMA]] (persistent 3D spatial memory) or [[2511.18112\|EchoVLA]] |
| Long-horizon with error recovery | [[2604.18791\|HELM]] (**81.5%** LIBERO-LONG + verifier) |
| Lightweight history retrofit for a pretrained VLA | [[2510.00695\|HAMLET]] (**+47.2%**, ~1% overhead) |
| Object-identity / non-Markovian diagnosis | [[2511.11478\|LIBERO-Mem]] (benchmark + Embodied-SlotSSM) |
| Explicit progress tracking | [[2603.09292\|See-Plan-Rewind]] or [[2604.17880\|ST-π]] |
| Efficient past+future dynamics | [[2512.09928\|HiF-VLA]] (codec motion vectors) |

^dm-10

> [!star] Key Papers
> - [[2604.18791|HELM]] — The cleanest memory + verification pairing; episodic keyframe store plus a learned state verifier, each contributing measurable LIBERO-LONG gains
> - [[2605.22283|SOMA]] — Reframes long-horizon failure as *out-of-vision* failure and solves it with a persistent 3D spatial-semantic memory
> - [[2511.11478|LIBERO-Mem]] — The diagnostic that proves the problem is real: standard VLAs collapse on object-centric non-Markovian tasks

^key-papers-10

> [!tip] Memory Is the Cure for Markovian Myopia
> Every paper here starts from the same observation: the single-frame assumption silently caps long-horizon performance, and naively stacking raw frames is too expensive. The winning move is a *compressed, attendable* memory — a 3D voxel map ([[2605.22283|SOMA]]), an episodic keyframe store ([[2604.18791|HELM]]), learned moment tokens ([[2510.00695|HAMLET]]), or codec motion vectors ([[2512.09928|HiF-VLA]]) — diagnosed by [[2511.11478|LIBERO-Mem]]. Cross-reference [[07_Latent-World-Models#3. Broader Latent Prediction Landscape]] for the latent-world-model side of long-horizon memory and [[02_Dataset-Benchmark-Environment#10. Long-Horizon Task Benchmarks]] for the benchmarks that test these claims. See [[09_Robot-Memory#3.2 Memory Baked into the VLA Backbone]] and [[09_Robot-Memory#4. Progress-Aware & Hindsight Control]] for the full cross-domain memory deep-dive this section's §10.1/§10.2 feed.

^insight-10

---

### 11. Cross-Embodiment & Domain-Transfer VLAs

A policy trained on one robot rarely transfers to another: action spaces differ (7-DoF arm vs parallel-jaw vs dexterous hand), kinematics differ, and the appearance gap between sim and real, or between video and robot, is large. This cluster tackles *the transfer itself* — either by abstracting the action space so embodiment differences vanish, or by closing the visual/physical domain gap that blocks sim-to-real and video-to-robot transfer. The unifying insight: heterogeneity is the bottleneck, and the fix is a shared representation (action or visual) that absorbs the variation.

#### 11.1 Embodiment-Agnostic Action Spaces

Define an action representation that is invariant to the specific gripper, hand, or base — so a single policy serves many embodiments, and knowledge transfers across them rather than being relearned per robot.

- **[[2608.06374|DyPES-VLA]]** — A cross-embodiment VLA learning ==shared dynamics priors== via future-prediction on action-free video + robot demos, decoded by an ==embodiment-specific MoE Diffusion Transformer== head; **89.02%** RoboTwin 2.0, **98.0%** LIBERO (one checkpoint), **75.6%** real avg (Franka/AgileX/G1) vs ACT's **32.4%**.
- **[[2510.10274|X-VLA]]** — A ==soft-prompt mechanism== assigning learnable embeddings per hardware configuration for heterogeneity-aware guidance on a flow-matching backbone; X-VLA-0.9B is SOTA on **5/6** benchmarks (LIBERO, Simpler, VLABench, RoboTwin-2.0, NAVSIM), 3 real platforms.
- **[[2512.05693|HiMoE-VLA]]** — A generalist VLA with a ==Hierarchical Mixture-of-Experts== (==Action-Space MoE== at shallow layers + ==Heterogeneity-Balancing MoE== at deep layers) on PaliGemma that absorbs cross-embodiment action-space/frequency diversity to prevent negative transfer; **97.8%** LIBERO, **3.967** CALVIN, **75.0%/63.7%** real xArm7/Aloha.
- **[[2605.25044|X-DiffVLA]]** — A unified ==diffusion action head== over a standardized action space across bases/grippers/dexterous hands + ==Embodied Forcing==; **64.5%** RoboCasa across embodiments (+15.3pp over π0.5), **71.0%** Isaac Gym.
- **[[2605.30280|Qwen-VLA]]** — A Qwen3.5-4B + ==flow-matching DiT policy== with ==embodiment-aware prompt conditioning== (textual platform/control descriptions); **97.9%** LIBERO, **56.7%** RoboCasa-GR1, **83.6%** real ALOHA — unifying tasks/environments/embodiments.
- **[[2505.07817|LangToMo]]** — A dual-system framework using ==pixel-motion forecasts as a universal, embodiment-agnostic representation==: a System-2 diffusion model self-supervisedly generates text-conditioned pixel motion from one frame, and System-1 maps it to actions (learned or geometric); **71.3%** real xArm, **33.8%** zero-shot (vs GPT-4o 18.8%), **57.7%** MetaWorld.
- **[[2409.03299|RT-1-X-SCARA-Transfer]]** — A case study fine-tuning ==RT-1-X== onto a 40-year-old kidney-workspace SCARA absent from training; zero-shot fails, **100** teleop demos reach **23%** (80% near-miss) — quantifies the kinematic-novelty transfer cost.
- **[[2501.10105|UniAct]]** — A framework learning a discrete ==Universal Action Space== (a VQ codebook of atomic cross-embodiment behaviors) extracted by a shared VLM, with lightweight per-robot MLP decoders translating universal actions to control; UniAct-0.5B beats **14×**-larger OpenVLA-7B/LAPA-7B on cross-embodiment generalization, adapting to new robots by tuning only **0.8%** of params.

#### 11.2 Sim-to-Real & Video-Transfer Adaptation

Close the appearance/physics gap so policies learned in simulation or from video survive on real hardware — via video augmentation, robot-centric inverse-dynamics stabilization, physics-conditioned real-to-sim-to-real, or inference-time physics guidance.

- **[[2606.20118|Pose6DAug]]** — Reconstructs a target mesh in the source's canonical frame so its pose trajectory transfers directly, composited via depth-ordered ==3D mesh-pose guided video== inpainting; **+7pp** OOD SR (**42.9%**) over base, beating 2D-editing and sim-based augmentation.
- **[[2512.18396|AOMGen]]** — Recovers articulated motion from a robot trajectory via ==3D Gaussian Splatting== reconstruction + contact/joint-axis optimization, then swaps category-level assets for physics-consistent demo synthesis; **150** samples lift a flow-matching VLA **0%→88.66%** SR.
- **[[2605.02757|VideoTransfer-VLA]]** — A ==video augmentation== framework where LLM-rewritten captions + depth-controlled conditional video diffusion synthesize visually diverse training videos; **+10.0%** RDT-1B RoboTwin 2.0 Hard, **+5.1%** LIBERO-Plus, real AgileX gains.
- **[[2604.17887|StableIDM]]** — A method stabilizing inverse-dynamics against manipulator truncation via ==robot-centric masking== + ==directional feature aggregation== + ==temporal dynamics refinement==; **30.7%** AgiBot truncated subset (vs Vidar 18.6%) for video-to-action transfer.
- **[[2603.25038|AirVLA]]** — A method adapting ==π0== to an aerial manipulator with real-time chunking + ==physics-aware inference-time guidance== (payload-aware action modification); **50%** aerial pick-place (vs **0%** naive π0), **62.5%** zero-shot navigate-then-grasp.
- **[[2507.02190|cVLA]]** — A lightweight ==camera-space VLA== (fine-tuned PaliGemma2) predicting end-effector keyposes directly in 2D image-frame coordinates, trained purely on randomized ManiSkill sim for zero-shot sim-to-real, with ==beam-search-NMS== decoding for diverse trajectories; **15** real Franka tabletop tasks zero-shot, Top-3 error **33.94% → 25.00%**, embodiment-agnostic.
- **[[2510.11689|Phys2Real]]** — A ==real-to-sim-to-real== pipeline conditioning RL policies on physical parameters (friction, mass), fused with VLM-inferred priors via ==inverse-variance weighting== at deployment; **100%** weighted T-block SR (vs **79.17%** DR), **57.14%** top-weighted variant (vs **23.81%** DR), **14.2%** faster hammer-pushing.

**Cross-Embodiment VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| One policy across many robots (SOTA) | [[2510.10274\|X-VLA]] (soft-prompt, 5/6 benchmarks) |
| Unified action space incl. dexterous hands | [[2605.25044\|X-DiffVLA]] (**+15.3pp** RoboCasa) |
| Transfer capabilities without retraining | [[2605.10903\|CapVector]] (capability-vector merging) |
| Sim-to-real via physics conditioning | [[2510.11689\|Phys2Real]] (**100%** weighted T-block) |
| Video-to-robot transfer | [[2605.02757\|VideoTransfer-VLA]] or [[2604.17887\|StableIDM]] |
| Cross-embodiment deployment infrastructure | [[2605.11564\|RIO]] (**130 ms** latency) |

^dm-11

> [!star] Key Papers
> - [[2510.10274|X-VLA]] — The reference embodiment-agnostic architecture: a soft-prompt per hardware config absorbs heterogeneity while one backbone serves all
> - [[2510.11689|Phys2Real]] — Establishes that *physics conditioning* beats blind domain randomization for sim-to-real on physically-distinct objects
> - [[2409.03299|RT-1-X-SCARA-Transfer]] — The honest negative result that quantifies how badly cross-embodiment transfer fails on truly novel kinematics

^key-papers-11

> [!tip] Heterogeneity Is the Real Bottleneck
> Whether the gap is *action-space* (gripper vs dexterous hand) or *domain* (sim vs real, video vs robot), the winning recipe is the same: absorb the variation into a shared representation rather than relearning per embodiment. Soft prompts ([[2510.10274|X-VLA]]), unified diffusion heads ([[2605.25044|X-DiffVLA]]), and physics conditioning ([[2510.11689|Phys2Real]]) all instantiate this. Cross-reference [[15_Sim-to-Real-Transfer#1. Design-Space Principles]] for the full sim-to-real deep-dive and [[14_Egocentric-Pretraining-and-Human-Video#5. Transfer Mechanisms — Hand → Gripper]] for human-video-to-robot kinematic transfer.

^insight-11

---

### 12. Runtime Adaptation & Inference-Time Steering

A pretrained VLA is a *fixed* policy — but the deployment world is not the training world. This cluster keeps the weights (mostly) frozen and improves behavior *at inference time*: either by adapting online from sparse reward without resets, or by steering the action distribution through verification, guidance, or auxiliary signals. The dividing line is whether adaptation updates parameters online (test-time RL) or leaves them frozen and reshapes sampling (steering). Both buy robustness without the cost — and risk — of a full retraining loop.

#### 12.1 Test-Time RL & On-the-Fly Adaptation

Adapt the policy *during deployment* from sparse outcome signals, intervention data, or pseudo-counts — no environment resets, no offline retraining. The policy calibrates itself to the deployment distribution in minutes to hours.

- **[[2608.09448|VANE]]** — A router blends ==Mixture of Latent Prompts== per task, a ==Latent-Action DiT== ==World-Predictive Interface== predicts features 8 steps ahead, and **AGV-TTT** commits a shadow prompt only if later predictions confirm improvement; **71.2%** WidowX avg (**+3.8pp** over TTT-VLA), **98.7%** fewer backward passes.
- **[[2607.25516|IDR]]** — A training-free infer-diagnose-refine loop measuring each observation's ==causal effect== on the action by comparing factual against ==zero-padded counterfactual== inputs, then applying ==Gated Residual Fusion== with a ==bounded proprioceptive regularizer==; **+6.33%** for X-VLA on SIMPLER, real ARX5 **56.5→75.3%**, **33.3%** vs **0%** on a 5-step task.
- **[[2606.31958|SARL]]** — ==Semantic Action RL== reframes adaptation as a ==semantic MDP== where "actions" are language prompts to a frozen VLA: it learns a ==Q-function== over VLM-generated candidate prompts, sampled via softmax; near-0%→**~80%** SR within **60-100** online episodes on LIBERO-10 and real WidowX.
- **[[2606.29892|T2VLA]]** — A ==test-time RL== framework replacing external reward with intrinsic ==generation-confidence== reward via ==confidence-driven dual expert bootstrapping== + ==DTW-based hybrid similarity== for GRPO; **+6.2pp** LIBERO (**97.2%**), **+24.2pp** π0, **+21.3pp** RoboTwin 2.0 — no external reward needed.
- **[[2606.25800|ROAD-VLA]]** — An online self-distillation framework building an ==advantage-guided proximal teacher== in action space that perturbs student logits via agreement-gated advantages, turning sparse reward into dense token-level supervision via a KL-regularized improvement problem; **88%** ID / **73%** OOD vs PPO's 85/69%, faster convergence and lower variance under shift.
- **[[2606.03127|TTT-VLA]]** — A test-time training method doing ==latent prompt optimization==: an implicit ==latent prompt== is updated at deployment by a ==self-supervised state-grounding proxy== over an offline buffer while the backbone stays frozen; SimplerEnv WidowX rises **51.1% → 67.4%** single-embodiment and **22.8% → 31.6%** multi-embodiment.
- **[[2512.14666|EVOLVE-VLA]]** — A ==test-time training== method via online ==GRPO== with a ==learned task progress estimator== (no oracle rewards) + ==accumulative progress estimation== + ==progressive horizon extension==; **+6.5pp** LIBERO avg (**89.2% → 95.8%**), **+17.7pp** in 1-shot regime, breaks **0%** barrier on unseen tasks (**20.8%** zero-task-demo SR).
- **[[2601.06748|TT-VLA]]** — A ==test-time RL== method with a ==dense step-wise reward== that adapts the policy online during inference (no fine-tuning, resets, or human help); **+44%** relative across 15 unseen tasks for Nora/OpenVLA. The canonical reset-free test-time-RL recipe.
- **[[2510.26406|Hi-ORS]]** — A ==rejection sampling== method with an outcome-reward filter selecting only successful real rollouts (no unstable Q-function); masters contact-rich tasks in **1.5 hours** of real-world RL, beating HIL-SERL.
- **[[2508.02062|RICL]]** — Finetunes only the LLM component of π0-FAST-DROID (frozen image encoder) to inject ==in-context learning==: retrieves the closest demonstrations by image embedding, augments context, blended via a distance-weighted ==action interpolation layer==; **2.5%→31.25%** SR on 8 novel real tasks from 20 demos, **61.67%** after further fine-tuning (vs **31.67%**).
- **[[2605.25477|EXPO-FT]]** — An off-policy RL via a lightweight ==edit policy== refining a frozen VLA's actions (no backprop through the VLA); perfect **30/30** real-world SR across 8 tasks (vs HG-DAgger 22.1/30).
- **[[2605.30226|BORA]]** — An ==offline RL== consistency policy (1–3 denoise steps) + action-conditioned critic, then online ==Residual Chunk Actor==; **+14pt** SR / **+25pt** unseen-object generalization over imitation baseline.
- **[[2604.23073|RLT]]** — A compact learned ==RL token== summarizing VLA features as a low-dim RL state for a lightweight online actor-critic; **3×** speedup, **20→65%** on hard screw-installation.
- **[[2506.07127|APO]]** — A ==human-robot collaboration== method labeling desirable actions and the preceding K steps as undesirable + ==prospect-theory preference optimization==; **48.0%** RoboMimic, beating DPO/KTO on fine-grained tasks.

#### 12.2 Verifier-Free Sampling & Policy Steering

Leave the policy frozen and reshape its *output distribution* at inference — via confidence-based candidate selection, classifier-free-style guidance, world-model verification, or injecting auxiliary representations. Cheap, training-free or near-so, and composable with any backbone.

- **[[2607.14280|DiMaS]]** — Steers flow-matching VLAs where linear steering fails: partition representations by ==empirical quantiles== of a continuous behavioral feature, learn an ==optimal transport map== from feature-absent to feature-present, then gate it with a ==binary classifier== and tunable α; significant speed and displacement modulation on SmolVLA and π0.5 at a **6%** SR cost.
- **[[2607.07076|PriGo]]** — A ==plug-and-play test-time primitive guidance== framework: **PANet** predicts ==probabilistic primitive distributions== (**94.0%** LIBERO) that steer pretrained diffusion/flow policies via ==differentiable guidance== on the denoising step; **+3-7pp** sim, **+26pp** real over vanilla CogACT.
- **[[2606.13675|FRS]]** — A ==Flow Reversal Steering== method that deterministically inverts the flow-matching process to map a coarse VLM/human reference action back to its noise vector then re-denoises it into a precise in-distribution action; **+10%** absolute on 11 hard LIBERO tasks zero-shot, **+60%** absolute real-world DROID via DSBC on 10 rollouts.
- **[[2606.13435|GIVE]]** — A ==dual-path visual-semantic== gesture-grounding method overlaying hand skeletons + pointing rays on the image (==Visual Gesture Prompting==) and appending VLM-parsed intent text (==Semantic Intent Parsing==) into a frozen VLA with no architecture change; **86.7%** Identify SR / **80.0%** across all real HRI stages (vs baseline 46.7%/6.7%).
- **[[2606.14084|SDN]]** — A training-free two-stage inference-time selection over diffusion VLAs treating ==initial noise as a controllable DoF==: a ==Grounding Filter== (kNN contrastive over object-masked negatives) rejects spurious-visual actions, then ==Kinematic Stability Refinement== minimizes JerkRMS; **+18.33pp** real ALOHA (30.0→48.33%), do-no-harm in sim.
- **[[2606.12475|Collaborative VLA]]** — Identifies ==demonstration action leakage== causing premature "false starts" in action-chunking VLAs (Diffusion Transformer, π0.5) for implicit HRC, fixed via inference-time ==FK Steering + Basin Pull Steering== toward demo-derived ==basin points== with no retraining; **-14%** task time, **-55%** critical failures in a 16-participant assembly study.
- **[[2606.12299|Harmless-VLA-Steering]]** — Learns a ==language feedback policy== steering a frozen VLA purely via language input, combining narrated-video priors + interactive LLM search with a ==conformalized improvement head== that abstains when harmful; **+12.7pp** SR, cuts harmful-steering false positives **38.92%→9.31%** (sim) / **61.11%→2.22%** (hardware).
- **[[2512.07472|AFI]]** — A training-free plug-in building ==3D Spatial Affordance Fields== (VLM-parsed sub-goals + target/obstacle cost field) with ==proprioceptive memory-trap detection== that rolls back and re-ranks VLA trajectories by affordance alignment; **+17–26%** OOD over π0/π0.5 at **185 ms** (5 Hz), model-agnostic.
- **[[2512.02834|TACO]]** — A ==test-time anti-exploration via pseudo-counts== method: generate candidates, verify with a ==Coin Flipping Network== that penalizes OOD actions; **+9.1%** RoboTwin, **+16%** real dual-arm — steers toward in-distribution actions.
- **[[2511.22555|JITI]]** — A ==Just-in-Time Intervention== framework refining manipulation elegance from mixed-quality data via an ==Elegance Critic== (Calibrated Q-Learning) that guides a frozen VLA only at decision-critical Q-fluctuation moments, plus the ==LIBERO-Elegant== benchmark; **+17.4–21.2pp** sim ESR, **+23.7pp** real ESR, **−60%** interventions.
- **[[2510.05681|MG-Select]]** — A ==verifier-free== test-time scaling that samples N actions and selects via ==condition-masking distributional confidence== (KL divergence); **+168%** relative π0-FAST low-data RoboCasa, **+28%** real Franka.
- **[[2603.24584|TAG]]** — A ==Target-Agnostic Guidance== method, a CFG-style inference-time residual contrasting original vs target-agnostic observations; π0.5 LIBERO-Long **89.6→97.0%**, VLABench **29.4→55.4%**.
- **[[2510.22201|ACG]]** — A training-free ==Action Coherence Guidance== that steers flow-matching policies away from an engineered incoherent vector field; **+30.8%** real strawberry-stacking (43.6→74.4%), +6.7% RoboCasa.
- **[[2602.03973|VLS]]** — A method where VLMs ground OOD inputs and ==programmatically generate differentiable rewards== to steer a frozen π0.5's denoising; **94%** CALVIN movable-object (**7.4×**) / **87%** articulated (**9.6×**) over prior steering.
- **[[2603.12772|PVI]]** — An encoder-agnostic ==zero-initialized projection== injecting auxiliary visual features (e.g., ==V-JEPA2== temporal) into a pretrained VLA's action expert; **+24.0pp** (35.7→59.7%) on 20 bimanual tasks over GR00T-N1.5.
- **[[2509.00328|VLA Activation Steering]]** — The first ==mechanistic-interpretability== framework for VLAs: identifies causally-linked FFN ==value vectors== ("fast"/"up" concepts retained from VLM pretraining), overridden in real time via training-free ==activation injection==; up to **148.54%** end-effector-displacement gain in sim, zero-shot speed/height steering on a physical UR5.
- **[[2506.17811|RoboMonkey]]** — A test-time scaling framework that samples N candidate actions via ==Gaussian perturbation== and selects with a ==learned action verifier== trained on automatically-synthesized action-preference data, served on an SGLang VLA engine; **+25pp** real OOD (35→**60%**), **+9pp** ID over OpenVLA, verifies 16 candidates in ~650 ms.
- **[[2505.03500|TLI]]** — A ==Text Latent Interpolation== method where task-specific ==text latents== are ==linearly interpolated in the residual stream== to recombine skills, on a new `libero-ood` benchmark; extrapolation **9% → 83%** on OOD tasks, and re-injecting the text latent restores **11–28% → 81–94%** under blank prompts — named "spatial overfitting".
- **[[2502.01828|FOREWARN]]** — A two-stage ==foresight + forethought== method: a ==DreamerV3 latent WM== predicts candidate-action futures, a VLM narrates+evaluates them; **+50%** narration accuracy, Cup-task SR 0.30→0.80 — policy steering by imagined narration.
- **[[2605.08434|AFIL]]** — A failure-informed VLA using ==online-generated failure trajectories== as ==adaptive negative guidance== via a ==Dual Action Generator== (shared backbone, parallel success/fail heads) with strength scaled by success-fail noise cosine similarity; **96.9→98.4%** LIBERO over π0.5, **62.7%** vs **14.7%** OOD Lift-Cylinder.
- **[[2605.06222|FFDC-WAM]]** — A ==WAM macro-planner== + lightweight high-frequency ==Future-Forward-Dynamics-Causal verifier== gating when to trust imagination; RoboTwin Rand.hard **54.2→76.4%** while cutting WAM calls **69.1%**.
- **[[2410.01971|BYOVLA]]** — A weights-frozen ==run-time observation intervention== that localizes task-irrelevant regions (GPT-4o + Grounded-SAM2), probes the VLA's ==visual sensitivity==, and inpaints only regions that demonstrably perturb actions; recovers Octo's full **40%** distractor drop, **+20–25%** OpenVLA under clutter. The foundational input-intervention robustness method.

#### 12.3 Instruction-Conditioned Switching & Rejection

A complementary runtime axis: the *instruction* itself changes mid-task or arrives defective, and the policy must re-target or refuse rather than execute blindly. These VLAs train conditional-behavior heads so a single policy switches tasks or rejects bad commands online.

- **[[2603.17300|ReSteer]]** — Fixes mid-execution steerability: ==Conditional Mutual Information== is a rollout-free proxy (r=**0.74**), ==SteerGen== synthesizes switch trajectories, and ==Self-Refining Behavioral Cloning== reinforces steering; **+8.8pp** sim LIBERO-Goal, **73%** real DROID steering SR (**2.2×** over the **33%** fine-tuned baseline) while holding **85%** single-task SR.
- **[[2506.10826|RationalVLA]]** — A dual-system VLA pairing a pre-trained MLLM with a robot policy via learnable ==latent-space embeddings== that transmit either action intent or a clear ==rejection signal==, plus the ==RAMA== benchmark (14K instructions, 6 defect dimensions); **+14.5pp** SR over baselines, **85%/80%** real basic/long-horizon defective-instruction tasks (vs 16.7%/8.3%).
- **[[2506.03574|SwitchVLA]]** — An execution-aware VLA that models mid-task ==task switching as conditional behavior prediction== via ==contact-state supervision== + forward/rollback/advance behavior modes, learned from existing trajectories with no switch-specific demos; **50.9%** LIBERO-Goal mid-switch (vs 8.3–11.1%), **95.1–96.5%** real mid-switch (vs 0–4.8%).

**Runtime Adaptation — Decision Matrix**

| Need | Recommendation |
|---|---|
| Reset-free online adaptation at deployment | [[2601.06748\|TT-VLA]] (**+44%** unseen tasks) |
| Real-world RL in hours, not days | [[2510.26406\|Hi-ORS]] (**1.5 hr** contact-rich) or [[2605.25477\|EXPO-FT]] (**30/30**) |
| Training-free distribution steering | [[2603.24584\|TAG]] or [[2510.22201\|ACG]] (CFG-style guidance) |
| Verifier-free best-of-N selection | [[2510.05681\|MG-Select]] (**+168%** low-data) |
| Inject auxiliary representations into a frozen VLA | [[2603.12772\|PVI]] (**+24pp** via V-JEPA2) |
| World-model-verified steering | [[2502.01828\|FOREWARN]] or [[2605.06222\|FFDC-WAM]] (**−69%** WAM calls) |
| Reject or switch on defective/changing mid-task instructions | [[2506.10826\|RationalVLA]] (rejection signal) or [[2506.03574\|SwitchVLA]] (conditional switching) |

^dm-12

> [!star] Key Papers
> - [[2601.06748|TT-VLA]] — Establishes that VLAs can adapt online at inference with no resets, fine-tuning, or human intervention — the clean test-time-RL formulation
> - [[2510.05681|MG-Select]] — The reference verifier-free steering result: a distributional-confidence criterion selects the best of N candidates with no learned verifier
> - [[2605.06222|FFDC-WAM]] — Shows runtime verification can decide *when* to invoke the expensive world model, cutting imagination calls by two-thirds

^key-papers-12

> [!tip] Frozen Weights, Better Behavior
> Two philosophies coexist: update online from sparse reward (test-time RL — [[2601.06748|TT-VLA]], [[2510.26406|Hi-ORS]]) or leave weights frozen and reshape sampling (steering — [[2510.05681|MG-Select]], [[2603.24584|TAG]], [[2502.01828|FOREWARN]]). Steering is cheaper and composable; test-time RL adapts further but risks the same instability §6 fights. Reach for steering first; escalate to test-time RL when the distribution gap is large. Cross-reference [[16_Self-Evolving-VLA-WAM#3. Core Mechanisms of Self-Evolution]] for the self-evolving view and [[06_WAM#5. VLM-Integrated WAMs]] for WAM-verified steering at the dynamics level.

^insight-12

---

### 13. Safety, Robustness & Adversarial VLAs

A VLA that controls a physical arm is an attack surface and a safety risk in a way a chatbot is not — a successful attack moves the world, and a silent failure can break hardware or hurt a person. This is the largest cluster in the file because the problem is three-fold: VLAs are *attackable* (adversarial patches, textures, prompts, backdoors), they are *brittle* (small OOD shifts collapse success), and they need *runtime guardrails* (detect failure before it propagates). The sub-sections track these three: offense (red-teaming/attacks), defense-by-robustness (OOD generalization), and defense-by-monitoring (runtime verification).

#### 13.1 Adversarial Attacks & Red-Teaming

Systematically *break* VLAs to map the threat surface — adversarial patches and 3D textures in the visual channel, jailbreak-style prompt attacks and backdoors in the language channel, and automated red-teaming that searches for failure-inducing instructions. The control-authority threat model (force arbitrary physical actions) is what makes these distinct from LLM attacks.

- **[[2608.10393|DURA]]** — ==Diffusion-guided patch optimization== partially noises a benign seed patch then ==DDIM==-denoises it for naturalness, guided by white-box ==action-loss== backprop or a black-box ==score-function estimator== over forward-noised latents; **100%** white-box / **86.0%** black-box ASR on OpenVLA, **100%** on π0-FAST.
- **[[2608.03207|DRIFT-VLA]]** — A universal physical adversarial patch perturbing only the ==first denoising step== of a flow-matching VLA's velocity field via PGD, exploiting an "early injection, full-path amplification" effect; **99.8%** ASR on π₀ across LIBERO (vs UADA's 13.2%, EDPA's 25.3%), **99.3%** on π₀.5, inducing a "phantom grasp" failure.
- **[[2607.12571|TrustVLA]]** — Names two mechanistic signatures of a triggered VLA backdoor — ==epistemic homogenization== and anomalous ==attention reallocation== — then detects with a ==Dirichlet evidence framework==, localizes by ==attention rank promotion==, and recovers by ==localized inpainting==, all on frozen weights; BadVLA ASR **100→7.0%**, INFUSE **100→2.2%**, zero false alarms.
- **[[2607.04146|!Imperio]]** — Demonstrates ==trigger-word data poisoning== on ==smolVLA==: injecting **3** poisoned episodes (**1%** ratio) into 320 clean episodes induces **0.0%** triggered task success (full denial-of-service) while clean-prompt SR stays stable at **~50%**, generalizing across trigger placement.
- **[[2607.03758|Planner-Agnostic Adversarial Attack Framework]]** — Attacks the *goal region*, not a pose: an offline ==kinematic occupancy heatmap== over ==manipulability== and clearance is occluded online by ==greedy== obstacle placement with no planner access; **0%** planning SR across all **9** classical configs at ≤**5** obstacles, OpenVLA to **0%** with **3**.
- **[[2511.12149|AttackVLA]]** — A unified ==attack+backdoor evaluation framework== + ==BackdoorVLA== bi-modal trigger; **100%** untargeted ASR and **95.4%** static-state induction (FreezeVLA) on OpenVLA, **75.35%** backdoor target rate, **50.00%** targeted ASR on a physical Franka arm — the first targeted physical-robot backdoor threat model. The standardized attack benchmark.
- **[[2411.13587|VLA-Adversarial-Vulnerabilities]]** — A study of three robot-specific attack objectives (==UADA==, ==UPA==, ==TMA==); untargeted attacks reach ~**100%** task-failure in sim *and* physical settings. The foundational demonstration that VLAs are catastrophically attackable.
- **[[2506.03350|GCG-VLA]]** — An attack adapting ==Greedy Coordinate Gradient== jailbreaks to optimize ==adversarial text suffixes== for ==control authority==; **77–97%** success in 3–10 min, persistence **28×** baseline, sim-to-real transfer.
- **[[2605.00880|AFM]]** — An ==Adversarial Flow Matching== attack crafting imperceptible perturbations on driving VLAs by matching perturbation flow to a target trajectory; **88.24%** ASR on TransFuser / **87.14%** on SimLingo at LPIPS as low as **0.074**, inducing active hijacking up to **40.06%** off-road rate — exposing the flow-matching action head as an attack surface.
- **[[2604.09651|FlowHijack]]** — A ==dynamics-aware backdoor== for flow-matching VLAs: a trigger steers the velocity field so denoising converges to attacker-chosen trajectories, clean behavior preserved; up to **100%** ASR, retaining **82.2%** under target-position filtering and **55.6–67.7%** after 10,000 steps of clean fine-tuning — the first backdoor for flow-matching action generators.
- **[[2604.01618|Tex3D]]** — An end-to-end optimization of ==physically-realizable 3D adversarial textures== with ==foreground-background decoupling==; raises task failure from 2.8–24.1% to **69.3–90.5%** across four VLAs.
- **[[2510.13237|EDPA]]** — An ==Embedding Disruption Patch Attack==, model-agnostic and needing only visual-encoder access; **+74.7%** OpenVLA failure vs clean, with an ==adversarial-fine-tuning== defense that recovers most of it.
- **[[2511.21192|UPA-RFAS]]** — A single ==universal transferable physical patch== via feature-space ℓ1+contrastive deviation + ==Patch Attention Dominance== + ==Patch Semantic Misalignment== losses; drops black-box OpenVLA-OFT 98.25→**5.75%** sim / 91.25→**40.25%** physical, transferring even to π0.
- **[[2505.16640|BadVLA]]** — A two-stage ==objective-decoupled backdoor==: inject perception-module triggers via reference-aligned latent separation, then restore clean performance by fine-tuning on clean data; near-**100%** ASR with negligible clean-accuracy loss, surviving JPEG/Gaussian noise and evading existing defenses.
- **[[2604.22591|RedVLA]]** — A two-stage ==physical red teaming== method (==Risk Scenario Synthesis== + ==Trajectory-Driven Risk Amplification==); **64.9–95.5%** ASR across six VLAs at state/cumulative/conditional levels.
- **[[2411.18676|ERT]]** — An ==Embodied Red Teaming== method framing instruction generation as feedback-driven optimization; drops 3D-Diffuser/OpenVLA from **92.9→53.0%** CALVIN. The foundational instruction-level red-teaming method.
- **[[2603.12510|Q-DIG]]** — A red-teaming method framing it as ==Quality-Diversity optimization== for diverse, human-like adversarial prompts; **0.972** archive coverage, more human-like than ERT/Rephrase.
- **[[2604.05595|DAERT]]** — A ==diversity-aware RL red-teaming== method mitigating mode collapse; drops π0 from **93.33→5.85%** with adversarial instructions while maximizing semantic diversity.
- **[[2502.06575|RoboART]]** — A ==predictive red-teaming== framework (==edit-and-predict==) that uses language-conditioned diffusion image edits + a VLM critic to synthesize off-nominal observations, then scores a ==policy-specific latent anomaly detector== to forecast per-factor degradation without hardware; Spearman **0.8/0.7** vs real, targeted data lifting SR **2–7×**.

#### 13.2 Robustness & OOD Generalization

Defend by *being robust* — preserve visual grounding under low-data fine-tuning, regularize for smoothness, dual-expert designs that keep motor priors frozen, and audits that quantify how badly current VLAs degrade under realistic perturbation. The recurring finding: standard VLAs lose 50–80% success under modest OOD shift.

- **[[2608.04692|Task-Vector Negation Audit]]** — A closed-loop audit of per-skill ==task-vector subtraction== (data/gradient-free, MergeVLA) finding target-suppression is robust but control-skill locality is fragile, with suppressed skills rapidly ==relearnable== rather than erased; LIBERO-Goal control retention **57.8%→52%**, **4/5** cases collapse a control skill to **0%**.
- **[[2608.04396|CofactVLA]]** — Fixes the "vision-override phenomenon" via a ==Dual-path Deconfounding Graph== (factual vs counterfactual observation-only branch) with ==Action-Level Orthogonal Projection Guidance== + ==Feature-Level Counterfactual Covariance Reduction==; **98.5%** LIBERO, **69.1%** LIBERO-Plus OOD, **+52.3pp** real-world OOD over baselines.
- **[[2608.03231|SARF]]** — Defends against ==Attention-Guided Semantic Disruption== patches (which hijack action-to-vision cross-attention) via a zero-inference-overhead ==teacher-student== fine-tune of only the visual encoder, combining ==feature anchoring== + ==policy-critical attention distillation==; cuts OpenVLA's attacked failure rate **100%→28.6%**, real-world SR **23%→65%**.
- **[[2608.02497|GSR]]** — Traces VLA paraphrase-instruction failure to an architectural bottleneck (unstable joint vision-language encoding), not lost semantics, and fixes it via ==Grounded Semantic Re-binding== that decouples a frozen T5's stable instruction semantics from dynamic vision; **+24.1pp** VLA-Adapter / **+44.6pp** SmolVLA on LIBERO-Para, no paraphrase data needed.
- **[[2607.14698|ChromaGuard]]** — ==Chroma-preserving adversarial training== restricting ==hue perturbations== while allowing other bounded augmentations, defending against ==FLARE==, a ==black-box physical spotlight attack== zeroing baseline VLA SR (**0.0%** across all simulation suites, **115.5 cm** error); ChromaGuard holds **92.5%** SmolVLA SR under attack.
- **[[2607.10655|AFP]]** — A policy-agnostic ==mask predictor== emits ==task-conditioned relevance masks== supplying an ==auxiliary grounding loss== that pulls policy attention onto causal evidence, applied by ==projected-gradient update== so it never fights the action loss and dropped at inference; attention Soft-IoU **0.170→0.934**, π0.5 OOD **0.22→0.59** sim, **0.30→0.67** real.
- **[[2607.01378|Neuro-Symbolic VLA Safety]]** — Injects ==minimum-norm CBF corrections== *during* π0.5's ==flow-matching denoising== via a trajectory-level ==discrete-time exponential Control Barrier Function== (SLSQP), letting the policy adapt rather than reacting post-hoc; **82.81%** CAR / **81.62%** TSR on SafeLIBERO, nearly doubling AEGIS's long-horizon TSR (**76.75%** vs **43.75%**).
- **[[2604.21192|VLA-Open-World-Audit]]** — A BEHAVIOR-1K reproducibility audit: Q-score disparities **>27%** between reported and reproduced, grasp failure the dominant error — quantifies how perturbation-sensitive top VLAs really are.
- **[[2601.04052|RSS]]** — Diagnoses ==modality collapse== — dense visual signal drowning sparse language — then fixes it twice: ==Monte Carlo Syntactic Integration== densifies the instruction manifold via an ==Oracle Teacher==, and ==Residual Affordance Steering== subtracts a visual ==affordance prior== from action logits; **+29.85pp** for π0, **+11.08pp** for π0.5 on instruction overwriting.
- **[[2509.18953|Eva-VLA]]** — A method parameterizing ==3D rotations + dynamic lighting + natural adversarial placement==; OpenVLA/UniVLA failure surges from 4.0–23.5% to **>80%** under optimized physical transforms — the realistic-perturbation stress test.
- **[[2508.06426|Robot Policy Shortcut Learning]]** — A theory + empirical account of ==shortcut learning== from ==dataset diversity and fragmentation==: low diversity + high inter-dataset disparity inflates spurious task-irrelevant/task-relevant mutual information; ==bridge data== + viewpoint/object-swap augmentation cuts shortcut degree, lifts OOD SR across Diffusion Policy/MiniVLA/π0.
- **[[2603.22126|ROBOGATE]]** — A ==two-stage adaptive sampling== (Latin-Hypercube → ==boundary-focused== on the 30–70% transition zone) + a logistic risk model yielding closed-form failure boundaries and a deployment-gate leaderboard; **all 7** SOTA VLAs score **0/68** on Isaac-Sim industrial scenes despite high LIBERO SR.
- **[[2503.03480|SafeVLA]]** — A formulation of safety as a ==Constrained MDP== with an ==Integrated Safety Approach==; **83.58%** reduction in cumulative safety cost *and* **+3.85%** task SR — safety and performance aren't a strict trade-off.
- **[[2511.01331|RobustVLA]]** — A theoretically-derived ==Jacobian + smoothness regularization== in the PPO objective; **82.5%** under observation perturbations / **54.8%** under action perturbations on LIBERO, beating all baselines.
- **[[2511.06385|PACS]]** — A ==Path-Consistent Safety filter== that modifies only speed/acceleration along a Diffusion-Policy/VLA's intended path (built from chunked actions) so it never enters OOD states, with a reachability-based real-time failsafe; **up to +68%** SR over reactive CBFs, SR on par with unprotected (**79% vs 80%**) at **0%** violations, **0.20 ms**/step.
- **[[2604.23121|DeLock]]** — A ==visual-encoder weight-drift L2 regularization== + ==Contrastive Prompt Guidance== that preserve grounding under low-data fine-tuning, diagnosed via a dedicated **8-task** lock-in-probe benchmark; standard SFT policies show **collapsed cross-attention** on novel prompts while DeLock resists scene perturbation and beats both concept- and spatial-lock-in probes.
- **[[2607.13597|Semantic Anchoring]]** — Shows action-instruction alignment erodes during fine-tuning and tracks OOD success at Spearman **ρ=0.964**, then ==contrastively aligns== mid-layer action representations to a frozen encoder's ==semantic manifold==, a ==shared-private decomposition== anchoring only the intention channel; **+6.3%** π₀ / **+7.2%** SpatialVLA, **+21.5%** real OOD.
- **[[2606.27295|LA4VLA]]** — A VLA pretraining framework doing ==vision-agnostic language-action pretraining== by masking visual observations to build vision-independent action priors, on the 33K-episode ==LA4-33K== atomic-action dataset; **95.30%** LIBERO / **83.00%** MetaWorld, **+45.0pp** real xArm6 (38.3→83.3%), **70.0%** under visual noise vs 27.5% — cures the visual-shortcut.
- **[[2605.10925|PriorVLA]]** — A ==Dual Action Experts== design: frozen Prior Expert preserves motor priors + trainable Adaptation Expert specializes; **77% ID / 53% OOD** RoboTwin 2.0 (+10/+11pp over π0.5).
- **[[2512.11891|VLSA]]** — A plug-and-play ==Safety Constraint layer== wrapping any VLA: a VLM + GroundingDINO localize obstacles in 3D, modeled as ==Minimum Volume Enclosing Ellipsoids==, and a ==Control Barrier Function QP== minimally adjusts nominal actions, no retraining; **77.85%** collision-avoidance (4× over π0.5's **18.69%**) + **68.13%** TSR at **0.356 ms**/loop.
- **[[2512.08333|RETAIN]]** — A ==robust finetuning via parameter merging== method linearly interpolating a pretrained generalist and a task-finetuned policy with modality-specific (vision/language/action) weights; **~40%** higher real OOD SR while preserving generalist skill and enabling sequential continual-skill merging.
- **[[2511.22780|Distracted-Robot]]** — A clutter-robustness audit introducing the ==Dual-View Feature Congestion (DvFC)== psychophysical measure over 6,000 sim + 216 real scenarios on five VLAs (Octo/OpenVLA/CogACT/π0/SpatialVLA); clutter drops SR up to **34%** (π0 collision **0.287**), DvFC inversely tracks SR, and distractor-augmented fine-tuning recovers only **18%**.
- **[[2511.19878|MAPS]]** — A ==Module-Wise Proximity Scheduling== that extends Selective Projection Decay with a per-submodule schedule (high regularization on early visual layers → low on late language layers); **+26.9%** SimplerEnv OOD for MiniVLA-OFT, real Franka ID 40→**72.5%** / OOD 22.5→**52.5%**, parameter-free.
- **[[2510.00037|RobustVLA-VLA]]** — A method jointly hardening output (PGD worst-case ==action-noise== regularization) and input (==UCB bandit== adaptively selecting impactful observation/environment/language perturbations) on diffusion VLAs; **+14.0%** avg over π0 across 17 perturbations, **+65.6%** real with 25 demos, at π0-comparable speed.
- **[[2503.03734|OTTER]]** — A VLA that ==freezes the pre-trained CLIP== vision/language encoders to preserve semantic alignment and adds ==text-aware visual feature extraction== (temperature-weighted attention selecting patches by language similarity); **62%** unseen real pick-place (vs OpenVLA 9%, Octo 12%), and fine-tuning CLIP collapses it 62→15% — frozen-encoder generalization.
- **[[2502.19250|ObjectVLA]]** — A diffusion VLA achieving ==open-world novel-object== manipulation without demos via ==co-training== on robot trajectories + diverse image-text data with injected ==localization (bounding-box) metadata== linking objects↔language↔actions; **64%** SR on 100 OOD objects (100% ID), **+46.7%** over OpenVLA, 80–90% on new objects after one epoch of phone photos.

#### 13.3 Runtime Verification & Failure Detection

Defend by *monitoring* — detect when the policy is failing or about to fail and intervene. Approaches read the VLA's own internal embeddings, train world-model uncertainty estimators, fine-tune VLMs as failure judges, or calibrate sequential confidence. The common goal: catch failure early enough to recover or hand off.

- **[[2608.13474|VLA Task-Progress Probe]]** — A ==contrastive probe== on **π0.5**'s ==residual-stream== embeddings decodes task progress while preserving language-counterfactual sensitivity, then compares it to an expected-completion baseline as a runtime OOD detector; only method with stable AUROC (**0.796-0.833**) on held-out tasks, beating supervised SAFE.
- **[[2608.09125|TDHD]]** — Samples primary + perturbed noise through the same deterministic ==flow-matching== velocity field and measures per-step ==L2 divergence== between resulting action chunks, truncating at a dual-threshold horizon; **60%/80%** needle/tissue SR (vs **55%/55%** baseline) on a real dual-arm surgical platform.
- **[[2608.04510|GUARD]]** — Detects diffusion-VLA failures by building ==counterfactual KV caches== (ablating top-salient visual/language tokens) and comparing the action head's denoising response to the original, feeding sensitivity/bias/grounding diagnostics into a ==functional-conformal-prediction== alarm; **88.84%** unseen-task ROC-AUC (**+5.73pp** over FIPER) at **1.14-1.27×** overhead.
- **[[2608.02958|ValueFormer]]** — A compact **3.5M**-param ==causal transformer value function== with a ==stage-aware, success-then-decay labeling scheme== producing dense per-frame progress + a binary mistake-detection head, policy-agnostic and running at 2 Hz alongside any frozen VLA; MAE **0.015**, on-robot A/B lifted task completion **70%→85%**.
- **[[2606.18043|VFD]]** — An epistemic-uncertainty estimator for flow-based VLAs, ==Velocity Field Disagreement==, reading ensemble velocity-field disagreement (theoretically linking KL to L2 velocity differences), paired with the ==SAVE== active-fine-tuning loop; Spearman **−0.71** with SR (calibrated at M=2), **67%** failure-detection accuracy / **79%** TPR, **22–50%** fewer demos.
- **[[2606.09740|ProbeAct]]** — A training-free inference-time failure-recovery framework using a multi-target ==hidden-state probe== to read 3D object positions from the VLA's visual backbone + an object-agnostic kinematic state machine + a ==hierarchical CBF filter== deflecting from memory-trap locations; **74.1%** LIBERO-plus (vs OpenVLA-OFT **69.6%**), strongest under geometric shift.
- **[[2605.30834|Hide-and-Seek]]** — A method extracting ==internal action embeddings== into a lightweight ==LSTM sequential detector== with inter/intra-trajectory contrastive losses; SOTA balanced accuracy (**0.852** OpenVLA LIBERO-10) over 12 baselines.
- **[[2605.22446|Pre-VLA]]** — A ==preemptive verification== method transforming PPO-critic advantages into absolute safety constraints + failure-aware penalty; **0.83** F1, **0.02** invalid-action false-pass, improved closed-loop LIBERO SR.
- **[[2604.16677|ReconVLA]]** — An external ==uncertainty-aware== module (Conformal Quantile Regression action selection + SMD failure detector), no retraining; **+17%** π0 SR (0.56→0.73, up to +40% on hard tasks).
- **[[2602.16182|WM-Failure-Classifier]]** — A hybrid ==supervised failure classification + anomaly detection== on a world-model backbone with ==conformal latent-prediction-error==; **>90%** accuracy across success/known-failure/OOD.
- **[[2603.06987|Foundational-WM]]** — A ==history-conditioned probabilistic WM== trained only on nominal trajectories in Cosmos-Tokenizer latent space; uncertainty rises on OOD/anomalous inputs for bimanual-manipulator failure detection, beating competing learning-based detectors by **3.8pp** higher failure-detection rate with **~20×** fewer trainable parameters on real cable manipulation.
- **[[2602.12405|Self-Refining-VLM-Failure]]** — An ==ARMOR== multi-task self-refinement VLM with separate binary-detection + NL-reasoning heads; top scores across four robotic failure datasets (RLBench-Fail/Maniskill-Fail/Sparrow-Fail/ARMBench), beating baseline fine-tuning **+25.6%** detection under distribution shift, iterative refinement lifting reasoning **+42.4%** Round 0→1.
- **[[2512.01946|FailCoT]]** — An automated cross-environment failure-data generation + ==Guardian-8B== judge; SOTA on three unseen real benchmarks (RoboFail/UR5-Fail/RoboVQA), surpassing GPT-4o, and when wired into a 3D-LOTUS++ policy lifts sim SR **0.45→0.54** on 10 unseen RLBench tasks and real UR5 perturbed "Put food" from **4/20→15/20**. Scales failure-reasoning data.
- **[[2604.20472|TDQC]]** — A ==sequential calibration== in a POMDP via a ==sequential Brier score== (theoretically equivalent to learning a Q-function); lower Brier and higher ROC-AUC for failure detection across OpenVLA/UniVLA/π0/π0-FAST, and the calibrated Q-function used for test-time action search lifts OpenVLA's unseen-task SR by **+13%** on LIBERO-10. The calibration-theory grounding.
- **[[2601.07821|FARL]]** — A method pre-training task + ==recovery policy== + ==latent WM with a constraint-prediction head== forecasting future failures; **−43.6%** failure episodes on FailureBench, dramatic real Franka reduction.
- **[[2505.10547|FORTRESS]]** — A ==slow-fast hierarchical== framework: VLMs proactively identify semantic fallback goals + calibrate ==OOD-aware safety cost functions== via ==conformal prediction==, then a rapid ==Reach-Avoid RRT== planner generates safe fallback trajectories; **>0.90** balanced OOD-detection accuracy, **>90%** safe fallback-landing SR in CARLA, real-time on a quadrotor.
- **[[2503.15202|VLM-BT-Failure-Handling]]** — A VLM-reasoning + reactive ==dynamic Behavior-Tree== generation for real-time failure handling; **100%** REFLECT-benchmark SR and failure detection in AI2-THOR + real ABB YuMi.
- **[[2306.15724|REFLECT]]** — A ==Hierarchical Robot Summary== that converts RGB-D/audio into scene graphs + event captions for LLM failure reasoning; **88.4%** sim / **68.8%** real explanation success. The foundational failure-explanation framework.
- **[[2303.07280|SuccessVQA]]** — A reframing of ==success detection as VQA== on a generative VLM (Flamingo-3B); **59.3%** balanced accuracy on unseen-language tasks (vs bespoke **49.9%**). The foundational VLM-as-success-detector baseline.

**Safety & Robustness — Decision Matrix**

| Need | Recommendation |
|---|---|
| Standardized attack/backdoor evaluation | [[2511.12149\|AttackVLA]] (unified framework) |
| Automated red-teaming for failure instructions | [[2411.18676\|ERT]] or [[2604.05595\|DAERT]] (π0 93→5.85%) |
| Physical-perturbation robustness stress test | [[2509.18953\|Eva-VLA]] (>80% failure under 3D transforms) |
| Safety-constrained policy (cost + success) | [[2503.03480\|SafeVLA]] (CMDP, −83.58% cost) |
| Preserve grounding under low-data FT | [[2604.23121\|DeLock]] or [[2605.10925\|PriorVLA]] (dual experts) |
| Internal-embedding failure detection | [[2605.30834\|Hide-and-Seek]] (**0.852** bal-acc) |
| World-model uncertainty monitoring | [[2602.16182\|WM-Failure-Classifier]] or [[2603.06987\|Foundational-WM]] |
| Predict-and-recover from failure | [[2601.07821\|FARL]] (−43.6% failures) |

^dm-13

> [!star] Key Papers
> - [[2411.13587|VLA-Adversarial-Vulnerabilities]] — The foundational proof that VLAs are catastrophically attackable; defined the robot-specific attack objectives the field now uses
> - [[2503.03480|SafeVLA]] — Establishes that safety (CMDP constraints) and task success are not a strict trade-off — both improve together
> - [[2605.30834|Hide-and-Seek]] — The reference internal-embedding failure detector; reads the VLA's own representations rather than bolting on external sensors
> - [[2509.18953|Eva-VLA]] — The realistic-perturbation audit that exposes how a modest 3D shift collapses SOTA VLAs to >80% failure

^key-papers-13

> [!tip] Offense, Robustness, and Monitoring Are One Problem
> The three sub-sections are a single defense-in-depth story: red-teaming ([[2411.13587|VLA-Adversarial-Vulnerabilities]], [[2411.18676|ERT]]) maps the attack surface, robustness methods ([[2503.03480|SafeVLA]], [[2605.10925|PriorVLA]]) shrink it, and runtime monitors ([[2605.30834|Hide-and-Seek]], [[2601.07821|FARL]]) catch what slips through. No single layer suffices — an attacked-and-robustified policy still needs a monitor, and a monitored policy still needs robustness so the monitor isn't constantly firing. Cross-reference [[04_VLA#18. Open Problems & Failure Modes]] below for the orthogonal *intrinsic* failure modes (spatial overfitting, embodiment tax) and [[16_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]] for the self-evolving recovery view.

^insight-13

---

### 14. VLA Foundation Models & Infrastructure

Above the per-paper innovations sits a layer of *generalist foundation models* — full systems trained at scale and released as reports, and the codebases/hardware that make VLA research reproducible. This cluster is less about a single mechanism and more about *integration and engineering*: which backbone, which action head, which tokenizer, assembled into a deployable generalist, plus the open infrastructure that lets others build on it. These are the reference systems the rest of the field benchmarks against.

#### 14.1 Generalist Foundation-Model Reports

End-to-end generalist VLAs released as system reports — the reference architectures combining a strong VLM backbone with a continuous-action head, trained on large heterogeneous corpora.

- **[[2607.06655|Pelican-VLA 0.5]]** — A Qwen3-VL generalist (6000+ hr cross-embodiment pretraining) using ==Bottleneck Tokens== + a ==curriculum bottleneck mask== to force manipulation-centric attention through a constrained perception-action interface; **91.4%** RoboTwin, **80%** real TienKung humanoid, exposing a "representation-to-action gap."
- **[[2607.04426|ACE-Brain-0.5]]** — An 8B unified embodied foundation model (Qwen3-VL-8B ==mixture-of-transformer== + ==Omni-Vision Encoder== + ==Action Expert==) integrating spatial perception, decision-making, embodied interaction, self-monitoring, and self-improvement via ==SSR+== training; **98.2%** LIBERO, **63.8%** RxR Val-Unseen, **+8.8pp** R2R SR.
- **[[2606.17846|Qwen-RobotManip]]** — A Qwen-VL VLA foundation model (decoupled backbone + ==Diffusion Transformer action expert==) whose ==unified 80-D state-action alignment== + camera-frame delta-pose turns ~38,100 hr of heterogeneous data into synergy; **+7.0** LIBERO-Plus / **+21.5** RoboTwin-Hard / **+22.6** RoboTwin-IF, **3.2×** zero-shot cross-embodiment, **45%** RoboChallenge 1st.
- **[[2606.14409|HyVLA-0.5]]** — A full real-world robot-learning stack: a 4B VLM + ==flow-matching action expert== + compact memory encoder trained on Hy-UMI-10K (10,000+ hr sub-mm UMI demos), refined by reward-free ==FlowPRO== preference optimization; **90.9%/90.1%** RoboTwin 2.0 Clean/Rand, cross-embodiment transfer to JAKA/Astribot without target teleop.
- **[[2508.21112|EO-1]]** — A unified ==decoder-only== transformer (Qwen2.5-VL init) with ==interleaved vision-text-action pretraining==; **58.5** RoboVQA BLEU-4 (beats GPT-4o 47.2), SOTA control — reasoning and control in one model.
- **[[2507.15493|GR-3]]** — An end-to-end ==Mixture-of-Transformers== generalist (pre-trained VLM + Action Diffusion Transformer) trained with a multi-stage recipe (robot imitation + web VL co-training + few-shot human-VR data) on the ByteMini 22-DoF bi-manual robot; **77.1%** unseen-instruction / **57.8%** unseen-object pick-place (→86.7% with 10 VR demos), **97.5%** long-horizon bussing.
- **[[2503.20020|Gemini-Robotics]]** — Google DeepMind's ==Gemini 2.0==-derived robotics family: ==Gemini Robotics-ER== adds embodied reasoning (open-world 3D perception, trajectory + grasp prediction, the ==ERQA== benchmark) and ==Gemini Robotics== is the low-latency VLA trained on thousands of hours of teleoperated data; **20** dexterous tasks, **79%** long-horizon, **>70%** from **100** demos.
- **[[2503.19757|Dita]]** — A ==Diffusion Transformer== policy on a LLaMA-style causal backbone with ==in-context conditioning==; **83.7%** SimplerEnv coke-can (vs OpenVLA 16.3%). The foundational scalable-DiT generalist.
- **[[2410.15959|DiT-Policy]]** — An ==in-context conditional diffusion transformer== denoising 7-DoF action chunks from a single static RGB; **3.61** CALVIN avg length, **50.0%** 5-instruction SR. The DiT-policy reference.
- **[[2502.13130|Magma]]** — A ConvNeXt + LLaMA-3-8B agent foundation model with ==Set-of-Mark== action grounding + ==Trace-of-Mark== trajectory learning from video; one model spans UI navigation + robotic manipulation with strong **zero-shot** cross-domain transfer — unifies digital-agent and embodied action.
- **[[2507.05331|LBM-TRI]]** — A TRI ==Large Behavior Model==: a ==Diffusion Transformer== pretrained on ~**1,695 hours** of real+sim demos, evaluated under ==blind A/B testing==; finetuned LBMs beat single-task baselines and widen the gap OOD (**10/16** vs **3/16** sim tasks under shift) — rigorous evidence that pretrain-then-finetune wins.
- **[[2503.10631|HybridVLA]]** — A VLA unifying ==diffusion + autoregressive== action generation in one LLM backbone via a ==collaborative training recipe==; **74%** RLBench (+33% over OpenVLA, +14% over CogACT).
- **[[2411.19650|CogACT]]** — A ==componentized== architecture separating cognition from action via distinct vision/language/action modules + a specialized DiT action module; **61.3%/74.8%** SIMPLER VA/VM, beats RT-2-X.
- **[[2504.19854|NORA]]** — A small generalist on Qwen-2.5-VL-3B + ==FAST+ tokenization== + FlashAttention/bf16; OpenVLA-comparable LIBERO at **57%** lower overhead, runs on consumer GPUs.
- **[[2509.04996|FLOWER]]** — A 950M VLA via ==intermediate modality fusion== (prunes VLM layers, conditions Flow Transformer on intermediate embeddings); **4.53** CALVIN ABC seq, **99%** pretraining-cost reduction.
- **[[2601.18692|LingBot-VLA]]** — A ==Mixture-of-Transformers== (Qwen2.5-VL semantic backbone + Flow Matching); **+4.28%** SR / **+7.76%** PS over π0.5 on the GM-100 real benchmark; the pragmatic foundation-model report.
- **[[2605.03269|RLDX-1]]** — A ==Multi-Stream Action Transformer== integrating vision/language/proprioception/physical signals for motion awareness + memory; **97.8%** LIBERO, **>70%** RoboCasa Kitchen.
- **[[2605.02881|MolmoAct2]]** — A ==Molmo2-ER== open embodied-reasoning VLM backbone + open robot demos (incl. bimanual); **63.8%** embodied-reasoning (+17% over Molmo2), **87.1%** MolmoAct2-DROID — open action-reasoning model.
- **[[2311.01378|RoboFlamingo]]** — A VLA adapting ==OpenFlamingo== via a ==decoupled VLM-backbone + LSTM policy head== with efficient freeze-and-finetune (perceiver resampler + cross-attention only); **2×** CALVIN avg successful-sequence length with zero-shot transfer to novel scenes + GPT-4-enriched instructions — the canonical "VLM as robot imitator".

#### 14.2 Codebases, Pipelines & Tooling

Open-source infrastructure — unified training stacks, modular codebases, and low-cost hardware — that lowers the barrier to VLA research and makes results reproducible.

- **[[2608.08183|Socratic Models-ChatGLM]]** — Swaps online ChatGPT for a locally-deployed ==ChatGLM2-6B== (==INT4== quantized, ==FastChat==+==Autogen== local API) in a ==ViLD==+CLIPort code-policy pipeline; **100%** completion at **85-92%** scores on single/multi-step UR5 tasks — removes the API-cost and network-dependency barrier from Code-as-Policies-style deployment.
- **[[2607.22997|AMD ROCm VLA Pipeline]]** — A Real2Sim2Real loop fine-tunes ==SmolVLA-450M== on Genesis grasp demos while ==3D Gaussian Splatting== scene reconstruction + domain randomization trains Go2/G1 locomotion on non-CUDA hardware; **7-11 min** convergence, **<2.4GB** VRAM.
- **[[2604.19728|VLA-Foundry]]** — A ==unified open-source framework== integrating LLM/VLM/VLA training in one codebase; near-linear DDP scaling, its Qwen3-VL-based **FOUNDRY-QWEN3VLA-2.1B-MT** beats LBM-MT by **+20pp** aggregate SR on closed-source bimanual tasks, while a from-scratch **FOUNDRY-VLA-1.7B** reaches HellaSwag **66.7** / PIQA **77.5**.
- **[[2604.05014|StarVLA]]** — A modular ==backbone–action-head== codebase supporting VLM *and* world-model backbones with pluggable heads + unified I/O; StarVLA-OFT **96.6%** LIBERO, StarVLA-GR00T **65.3%** SimplerEnv.
- **[[2606.03392|OpenEAI-Platform]]** — An open ==$790 6+1-DoF arm== (GA-optimized) + OpenEAI-VLA; manipulation comparable to >$8K commercial arms, **0.75** π0 SR — democratized embodied-AI hardware.
- **[[2605.11564|RIO]]** — An open-source ==Node + Middleware== robot I/O framework with ==asynchronous inference== for cross-embodiment deployment; **130.3 ms** observation-to-action latency (vs LeRobot 581.2 ms), runs VLAs / Diffusion Policy / RL.
- **[[2604.01179|Florence-2-ROS-2-Wrapper]]** — An open-source ==ROS 2 wrapper== hosting **Florence-2** in one node for local multi-mode VLM inference, exposing ==topics + synchronous services + asynchronous actions== over prompt-based task tokens (detection, captioning, OCR); **9.75 FPS** detection on RTX 3060 Mobile (base), 26.6 FPS on RTX 3080 Ti — advanced VLMs on consumer GPUs.

#### 14.3 Serving, Scheduling & Fleet-Scale Deployment

Deploying RFMs across a *fleet* rather than a single robot raises a distinct systems question: how to share GPU and network resources and schedule inference across many robots and model components while meeting per-task service-level objectives.

- **[[2607.01088|ROSA]]** — A ==centralized, server-scale serving architecture== + ==factory-objective-driven scheduler== maximizing ==weighted robot action throughput== across a shared GPU pool with a declarative multi-model SLO/safety spec; up to **12.06x** SLO-qualified factory productivity over dedicated per-robot serving, **99.9%** SLO compliance, **8.6x** fewer GPUs.
- **[[2602.13052|QA-Co-Inference]]** — Derives ==information-theoretic rate-distortion bounds== linking quantization bit-width to a tractable ==L1-norm parameter distortion== surrogate, jointly optimized via ==Successive Convex Approximation==; highest CIDEr on **3.75B**-param BLIP-2 and **176M**-param GIT over DRL/fixed-frequency baselines on a real Jetson-AGX-Orin/server testbed.

**Foundation Models — Decision Matrix**

| Need | Recommendation |
|---|---|
| Unified reasoning + control generalist | [[2508.21112\|EO-1]] (RoboVQA 58.5 BLEU-4) |
| Scalable DiT generalist baseline | [[2503.19757\|Dita]] or [[2410.15959\|DiT-Policy]] |
| Hybrid diffusion + autoregressive | [[2503.10631\|HybridVLA]] (**74%** RLBench) |
| Small / consumer-GPU generalist | [[2504.19854\|NORA]] or [[2509.04996\|FLOWER]] (950M, −99% pretrain) |
| Unified LLM/VLM/VLA training codebase | [[2604.19728\|VLA-Foundry]] or [[2604.05014\|StarVLA]] |
| Low-cost open hardware | [[2606.03392\|OpenEAI-Platform]] ($790 arm) |

^dm-14

> [!star] Key Papers
> - [[2508.21112|EO-1]] — The reference unified embodied foundation model: interleaved vision-text-action pretraining gives both strong reasoning and strong control in one decoder
> - [[2503.19757|Dita]] — Established the scalable Diffusion-Transformer generalist; the architecture much of the field's continuous-action work descends from
> - [[2604.05014|StarVLA]] — The modular codebase that made "backbone + pluggable action head" a reproducible research substrate

^key-papers-14

> [!tip] The Generalist Layer Is Now an Engineering Problem
> By 2026 the design space (§1) is largely settled — strong VLM backbone, continuous action head, heterogeneous pretraining — so the foundation-model frontier is *integration and scale*, not architecture novelty. The differentiators are tokenization efficiency ([[2504.19854|NORA]], [[2509.04996|FLOWER]]), unified training stacks ([[2604.19728|VLA-Foundry]]), and open hardware ([[2606.03392|OpenEAI-Platform]]). Cross-reference [[04_VLA#1. Design-Space Principles]] for the design choices these systems instantiate and [[02_Dataset-Benchmark-Environment#1. Cross-Embodiment Scale Datasets]] for the data corpora they train on.

^insight-14

---

### 15. Embodied VLM Brains & Reasoning Foundation

A VLA needs a *brain* — a VLM whose spatial, temporal, and causal reasoning is grounded in embodiment, not just web images. This cluster covers the embodied-VLM foundation models that serve as the high-level reasoner (often paired with a separate low-level controller) and the domain-specialized VLAs that adapt the recipe to driving, gaming, navigation, and aerial control. The shared thesis: general-purpose VLMs confuse first/third-person, struggle with spatial relations, and lack physical grounding — so embodied pretraining is necessary before the brain can drive a body.

#### 15.1 Embodied VLM Foundation Models

VLMs purpose-built or post-trained for embodiment — 3D spatial reasoning, temporal-causal grounding, and affordance understanding — that serve as the cognitive layer of a hierarchical robot system.

- **[[2607.17977|RynnBrain 1.1]]** — An embodied foundation-model family (2B/9B/122B-A10B, Qwen3.5) adding ==Contact Point Prediction== + ==Native 3D Grounding== pretraining tasks and a ==unified cross-embodiment action space== with ==embodiment-specific masking== for its RynnBrain-VLA flow-matching policy; RefSpatial-Bench **79.1**, real-robot SR **60.00%→86.67%** over a Qwen-based VLA.
- **[[2607.07403|Megamind]]** — A fully-onboard multi-agent VLM system (3B-parameter models, RAI framework) with a supervisory two-state self-feedback loop for task delegation and recovery, replacing cloud-dependent VLA deployment; fine-tuning lifted package-inspection accuracy **76.7%→91.5%** (F1 **0.755→0.915**), real-time on an AMD Ryzen AI mini PC across 5 industrial task categories.
- **[[2507.02029|RoboBrain-2.0]]** — A heterogeneous encoder-decoder (Qwen2.5-VL decoder) for embodied spatial reasoning; 32B variant is SOTA on BLINK (**83.63**), RoboSpatial (**72.43**), RefSpatial. The reference embodied-reasoning brain.
- **[[2601.14352|RoboBrain-2.5]]** — A brain adding precise ==3D spatial reasoning== via decoupled ==(u,v,d)== coordinate prediction + collision-free 3D keypoint sequences; **75.82** 2D spatial avg (beats Gemini-3-Pro 66.14), **44%** manipulation SR.
- **[[2601.21199|Thinker]]** — A 10B unified vision-language-time VLM for images/videos/instructions; Thinker-7B SOTA RoboVQA (**63.5** BLEU vs GPT-4V 26.8) — temporal grounding as a first-class axis.
- **[[2511.16518|MiMo-Embodied]]** — A cross-embodied VLM unifying autonomous-driving + embodied-AI via ==4-stage training== (SFT → embodied SFT → CoT → RLHF); SOTA across **17** embodied + **12** driving benchmarks (**29** total), demonstrating positive cross-domain transfer.
- **[[2511.00108|Pelican-VL-1.0]]** — A 7B–72B open embodied-brain family + ==Deliberate Practice Policy Optimization==; **+20.3%** over base, beats 100B open models by **10.6%**, stable against forgetting.
- **[[2509.01106|Robix]]** — A unified high-level ==cognitive layer== generating atomic commands + verbal responses; Robix-32B **92.6%** task progress in human-in-the-loop (edges Gemini-2.5-Pro 91%) — the planning/interaction brain.
- **[[2510.11027|Vlaser]]** — An InternVL3 backbone + flow-matching action expert + ==Vlaser-6M== synergistic-reasoning corpus; SOTA across 12 embodied-reasoning benchmarks (2B avg **15.2→45.3**).
- **[[2604.19839|EUEA]]** — A method fine-tuning one VLM with ==four environmental-understanding skills== as reward-free ==POMDP== sub-skills + a ==sampling-based recovery step== + ==GRPO== refinement; **+10.96%** ALFRED SR over BC, **86.48%** via recovery, **99.40%** goal recognition — closes the action-understanding gap zero-shot VLMs lack.
- **[[2604.18484|XEmbodied]]** — An embodied VLM foundation model injecting ==3D geometric priors== via a cross-attention ==3D Adapter== plus an ==Efficient Image-Embodied Adapter== distilling physical cues into compact tokens via a four-stage curriculum; SOTA/competitive on **18** benchmarks (**55.28%** Ego3DBench, **77.01%** DriveLMM-o1), robust zero-shot OOD.
- **[[2512.12822|LEMON]]** — A unified ==3D multimodal transformer== processing point-cloud patches and language as one sequence with a ==Z-Y-X hierarchical spatial partitioning== + separator tokens, trained on a three-stage recognition→captioning→scene-QA curriculum; LEMON-7B GPT-4 score **57.22** on 3D MM-Vet, **74.32%** 3D-GRAND SOTA, first power-law scaling evidence for 3D LMMs.
- **[[2512.24125|GenieReasoner]]** — An ==ERIQ== benchmark (6,052 embodied QA) + reasoner; **82.72%** ERIQ (+41% over baselines), excelling at action understanding and human-intention comprehension.
- **[[2506.00123|VeBrain]]** — A unified framework reformulating control as ==2D keypoint detection + embodied skill recognition== + ==Robotic Adapter== (Point Tracker / Movement Controller / Skill Executor / Dynamic Takeover) + ==VeBrain-600k with CoT==; **+31.5pp** avg over other unified frameworks, **+5.6pp** MMVet, **+5.2 CIDEr** ScanQAval, **+50pp** Complex Transport.
- **[[2504.12680|Embodied-R]]** — A collaborative framework where a large VLM perceives and a small LM reasons via RL with ==logical consistency reward==, plus a ==key frame extractor== that reduces compute; it **Matches or beats** OpenAI-o1 / Gemini-2.5-Pro on spatial reasoning while generalizing OOD to EgoSchema / MVBench — proves small LMs match large via RL + consistency.
- **[[2401.08577|MultiPLY]]** — The first multisensory object-centric embodied LLM that actively explores a 3D world to gather ==visual/audio/tactile/thermal== data via ==action tokens + state tokens==, trained on the **500K**-point ==Multisensory Universe== corpus; **56.7%** object retrieval (vs PointBind-LLM **48.9%**), **41.6%** tool-use, **30.2%** task decomposition.
- **[[2311.12871|LEO]]** — An embodied generalist agent perceiving/grounding/reasoning/planning/acting in 3D via a ==decoder-only LLM== unifying egocentric-2D + global-3D + text tokens, two-stage ==3D-VL alignment then VL-action instruction tuning== with ==Object-centric Chain-of-Thought==; matches or beats task-specific models on 3D captioning/QA, manipulation, navigation, zero-shot transfer.
- **[[2307.12981|3D-LLM]]** — Injects the 3D world into LLMs via a ==3D-language data-generation pipeline== (300K+ points from Objaverse/ScanNet/HM3D) + ==3D features== from multi-view 2D encoders, with ==position embeddings== + ==location tokens==; **+9%** BLEU-1 over SOTA on ScanQA, ~**1.03-1.1m** ScanRefer grounding error — precursor to 3D-VLA's action-generating extension.
- **[[2303.03378|PaLM-E]]** — The landmark embodied multimodal LM injecting continuous sensor observations (state, 2D images, 3D OSRT scenes) into a PaLM transformer as ==multimodal sentences==, co-trained across robotics/VQA/captioning/language; **94.9%** tabletop manipulation, SOTA OK-VQA at 562B, one/zero-shot transfer to new tasks — established the embodied-VLM-brain paradigm.

#### 15.2 Domain-Specialized VLAs (Game, Aerial)

The VLA recipe transplanted to non-tabletop, non-driving domains — video games, aerial mission control, embodied visual tracking, medicine, and scientific laboratories — where the action space and grounding differ but the vision-language-action pattern holds (autonomous driving has grown into its own cluster, §15.3).

- **[[2606.13578|LabVLA]]** — A Qwen3-VL-4B VLA for lab manipulation trained on ==RoboGenesis==, an Isaac-Sim data engine generating protocol-grounded lab demos, via FAST-token pretraining then ==flow matching== with ==Knowledge Insulation==; **71.1%** ID / **70.0%** OOD on LabUtopia (**+7.8/+6.8pp**), **80%** real Franka sim-to-real transfer.
- **[[2505.23189|TrackVLA]]** — A unified VLA for ==embodied visual tracking== on a shared Vicuna-7B backbone (task-dependent decoding for understanding vs action) + an ==anchor-based diffusion action model== denoising waypoints from clustered patterns; perfect zero-shot Gym-UnrealCV, **10 FPS** (~100× over GPT-4o), **90%/70%** real quadruped medium/hard.
- **[[2505.15206|EndoVLA]]** — A Qwen2-VL-7B VLA for autonomous endoscopic tracking (2-DOF continuum robot) via ==Dual-Phase Fine-tuning== (SFT + ==GRPO== on IoU/Motion-Angle/Format rewards); **86.1%** IoU polyp tracking (**+340.9%** over single-phase), **100%** zero-shot fruit-sequence generalization — extends the VLA recipe to surgical robotics.
- **[[2601.02427|NitroGen]]** — An open vision-action foundation model (==SigLIP 2== + ==Diffusion Transformer==) ==behavior-cloned== on 40K hr of gameplay video labeled via input-overlay action extraction (R² **0.84** joystick); zero-shot **44.8%** 3D-combat / **61.5%** 2D tasks, fine-tuning beats from-scratch by up to **52%** — the game-foundation exemplar.
- **[[2503.16365|JARVIS-VLA]]** — A Minecraft VLA acting from text+vision via keyboard/mouse via ==ActVLP== (Act from Visual Language Post-Training), a 3-stage paradigm that boosts the VLM's world knowledge, visual recognition, and spatial grounding on ==non-trajectory data== before action tuning; SOTA MCU (**+40%** over baselines on 1K atomic tasks), generalizes across VLM backbones.
- **[[2503.09527|CombatVLA]]** — A VLA for real-time action-RPG combat + ==CUBench==; **63.61%** (beats GPT-4o 57.29%, Gemini-2.0 57.90%), excelling at reasoning — the game-domain VLA exemplar.
- **[[2501.05014|UAV-VLA]]** — A ==zero-shot aerial mission generation== system: a three-module LLM+VLM pipeline translates NL instructions into UAV flight plans grounded in ==open satellite imagery==, bypassing task-specific training; **34.22 m** KNN-RMSE waypoint accuracy, 30 missions in 5 min (**6.5×** faster than a human operator). The aerial mission-planning exemplar.

#### 15.3 Autonomous-Driving VLAs

The VLA recipe specialized to driving: trajectory planning as the action space, NAVSIM/Bench2Drive as the benchmark. The shared frontier here is *grounding* — MoE scene/skill specialization, unified language-action tokenization, and learning-from-failure RL — to stop the "blind planning" that plagues naive driving VLAs.

- **[[2608.13395|FIRE-VLA]]** — Routes batch-relative low-reward-variance rollout groups to ==privileged self-distillation== from a frozen round-start copy reading future waypoints, adding a capped ==Jensen-Shannon loss== to ==GRPO==; nuScenes mean L2 **1.848→1.500m** (**18.8%** cut), CVaR99 **118.58→79.21m**.
- **[[2605.21061|Driving-VLA-IK]]** — A driving VLA grounded with ==next-visual-state prediction== + an ==Inverse-Kinematics== objective to stop "blind planning"; 0.5B model **92.2** NAVSIM-v1 PDMS (+19.0 over OpenDriveVLA), matching 7–8B VLAs.
- **[[2604.02190|UniDriveVLA]]** — A ==Mixture-of-Transformers== with masked joint attention decoupling understanding/perception/action + a ==sparse spatial perception module== + 3-stage progressive training; **78.37** Bench2Drive Driving Score, lowest nuScenes L2 without ego-state, retaining VQA ability.
- **[[2604.01765|DriveDreamer-Policy]]** — A unified ==driving world-action model== (LLM + lightweight generative experts for depth/video/action) with causal modeling; SOTA **89.2** Navsim-v1 PDMS, **88.7** v2 EPDMS.
- **[[2603.25740|Drive-My-Way]]** — A personalized driving VLA fusing visual input, user profiles, and instructions + a ==Personalized Driving Dataset== (30 drivers) with ==GRPO== reinforcement fine-tuning + style-aware reward adaptation; **18.77%** efficiency gain for aggressive instructions (vs SimLingo 3.70%), highest user ratings ID + OOD.
- **[[2603.14851|AutoMoT]]** — A ==Mixture-of-Transformers== (frozen VLM Scene-Understanding Expert + task Action Expert) with ==asynchronous inference== sharing a KV cache + joint attention; **87.34%** Bench2Drive Driving Score, **0.07%** nuScenes collision, **86.8%** latency cut (7.6x) at only **+1.24%** L2.
- **[[2603.01441|LinkVLA]]** — A ==unified language-action tokenization== in one VLM with a ==bidirectional== understand-and-generate objective + ==coarse-to-fine== parallel waypoint generation; **91.01** Bench2Drive Driving Score / **74.55%** SR (+5.94 over SimLingo), **361→48 ms** (**86%** latency cut).
- **[[2603.01063|ELF-VLA]]** — An ==Explicit Learning from Failures== method: a VLM teacher generates ==diagnostic feedback== that, with difficult-sample curation + ==Policy Shaping==, refines trajectories during GRPO; SOTA **91.0** NAVSIMv1 / **87.1** NAVSIMv2 PDMS, total-failure rate **2.73→1.08%**.
- **[[2602.21172|NoRD]]** — A ==reasoning-free== driving VLA (Qwen2.5VL-3B) trained weak-SFT then ==Dr. GRPO== (drops the std term to fight difficulty bias); **85.6** NAVSIM PDM (BoN 92.4 beats reasoning AutoVLA-BoN), outperforming models using **12–17×** more data; Dr. GRPO adds **+11.68%** vs +0.67% standard GRPO.
- **[[2512.04733|E3AD]]** — An ==emotion-aware== driving VLA using a ==Valence-Arousal-Dominance== model to read emotional tone/urgency from commands + a ==dual-pathway spatial reasoning== module (egocentric + allocentric fusion) trained with DPO for emotion-action consistency; **−20.00%** FDE, **+6.86%** Talk2Car IoU, **>0.8** Spearman/Kendall with human VAD — human-centric driving.
- **[[2509.20109|Discrete-Diffusion-VLA-VLA]]** — A ==discrete-diffusion== driving VLA (from a Diffusion LM) tokenizing 2D trajectories + a gradient-free two-stage ==reflective inference== (goal-conditioned then safety-guided regeneration via inpainting); **91.1** NAVSIM PDMS, DAC 99.3 / TTC 93.5, oracle-reflection reaches near-human 94.7.
- **[[2509.00789|CogDriver]]** — A driving VLA instilling ==cognitive inertia== via narrative-annotated ==CogDriver-Data== (persistent-intent rationales from a Multi-View Spatiotemporal MLLM) + a ==Temporal Coherence Module== keeping a dynamic world-state for long-range reasoning; **78.21** Driving Score / **56.93%** SR Bench2Drive (**+22%/+63%** rel), **0.34 m** nuScenes L2.
- **[[2506.24044|VLA4AD Survey]]** — The first survey of Vision-Language-Action models for autonomous driving, formalizing a taxonomy of interfaces/modules/outputs, tracing four evolutionary stages, and consolidating **20+** VLA4AD models plus datasets/benchmarks; identifies six open challenges spanning robustness, real-time performance, and multimodal alignment.
- **[[2505.16278|DriveMoE]]** — A ==Scene-Specialized Vision MoE== (dynamic camera-view selection) + ==Skill-Specialized Action MoE== fighting mode-averaging, two-stage teacher-forcing→adaptive training; SOTA Bench2Drive (**+22.8%** Driving Score, **+62.1%** SR over Drive-π0) at competitive **260 ms** latency.

#### 15.4 Alternative Instruction & Supervision Interfaces

Most VLAs assume a clean text instruction; this cluster widens the *input/supervision channel* — raw speech, natural-language motion supervision, or object-centric visual prompts — so the policy is specified or taught through a richer interface than typed commands.

- **[[2607.13605|Stage-Information VLA Study]]** — Frames subtask conditioning as an *interface* problem and finds the obvious channel loses: current-stage text (**TASKCTX**) trails the plain full-task baseline under direct fine-tuning (**50.24%** vs **57.45%**), while a ==normalized ordinal stage index== in the robot state wins only under ==baseline-first continuation==, **+4.69pp**.
- **[[2605.27284|FineVLA]]** — A ==fine-grained instruction alignment== method via cleaned, clustered, human-verified annotations on 47K trajectories + RoboFine-Bench; **71.0%** VQA (+8.9 over Gemini-3.1-Pro), FG-only training lifts policy SR.
- **[[2605.22812|GesVLA]]** — A dual-VLM treating ==gesture as a first-class modality== tightly coupled with language and action via cross-attention + semi-synthetic data; **94.3%** real target identification, **83.3%** real manipulation.
- **[[2506.21250|ACTLLM]]** — An LLM manipulation policy generating ==structured scene descriptions== (object, color, coordinates) as human-interpretable state via a JSON schema, with an ==action-consistency loss== deriving actions from the state embedding and an MDP reframed as multi-turn visual dialogue; **93.4%** VIMA-BENCH L3, **+13pp** CLIPORT over PAFF for compositional generalization.
- **[[2505.02166|CrayonRobo]]** — An ==object-centric prompt-driven== VLA (LLaMA-adapter + CLIP encoder) combining language with ==visual prompts== (contact points, orientations, movement directions) plus keyframe sequencing to decompose long-horizon tasks; higher SR than baselines, robust to visual-prompt noise, zero-shot real transfer without sim-to-real fine-tuning.
- **[[2505.02152|Interleave-VLA]]** — A method adapting VLAs to ==interleaved image-text instructions== via a lightweight module + special tokens + the auto-generated ==Open Interleaved X-Embodiment Dataset==; **2×** sim OOD / **2–3×** real generalization over text-only VLAs, zero-shot following cropped/web/sketch visual instructions.
- **[[2502.13508|VLAS]]** — An end-to-end VLA natively integrating a ==Whisper speech encoder== (no ASR pipeline) plus a ==Voice RAG== module that extracts voiceprints to retrieve user-specific knowledge for personalized manipulation; **54.6%** CALVIN-speech (vs 40.2% VLA+ASR), **>86%** customized-task SR, **2.79%** WER. The foundational speech-instruction VLA.
- **[[2411.00508|CLIP-RT]]** — A VLA learning from ==natural-language supervision==: non-experts teleoperate via language (LLM-translated to actions), ==Stochastic Trajectory Augmentation== diversifies demos, and a contrastive-imitation CLIP backbone maps observations+instructions to ==NL motion primitives==; **53%** real novel tasks (vs OpenVLA 29%), **93.1%** LIBERO at 1.3B (**163.8 Hz**).

#### 15.5 Navigation-Domain VLAs

Vision-Language *Navigation* transplants the embodied-VLM-brain recipe to a moving camera instead of a manipulating arm — the action space is waypoints, not grasps, but the same lesson holds: raw VLM perspective-taking is not enough without embodied, self-aware reasoning.

- **[[2605.22816|AwareVLN]]** — A unified VLM triggering sparse ==self-reflective reasoning== only at critical navigation nodes (scene description, progress, next plan), with supervision auto-generated via DAgger trajectories (no manual annotation); **73.5%** SR / **65.4%** SPL R2R-CE, **67.6%** SR RxR-CE from monocular RGB alone, strong sim-to-real transfer over NaVid/NaVILA.

**Embodied-VLM Brain — Decision Matrix**

| Need | Recommendation |
|---|---|
| Embodied spatial-reasoning brain | [[2507.02029\|RoboBrain-2.0]] or [[2601.14352\|RoboBrain-2.5]] (3D coords) |
| High-level planning/interaction layer | [[2509.01106\|Robix]] (**92.6%** task progress) |
| Embodied reasoning + action in one | [[2510.11027\|Vlaser]] (12-benchmark SOTA) |
| Open embodied-brain weights | [[2511.00108\|Pelican-VL-1.0]] (7B–72B) |
| Game / non-tabletop foundation policy | [[2601.02427\|NitroGen]] (40K-hr gameplay) or [[2503.09527\|CombatVLA]] |
| Driving-domain VLA (planning + grounding) | [[2603.01441\|LinkVLA]] (**91.01** Bench2Drive) or [[2604.02190\|UniDriveVLA]] |
| Learning-from-failure driving RL | [[2603.01063\|ELF-VLA]] (**91.0** NAVSIMv1) |
| Navigation-domain VLA | [[2605.22816\|AwareVLN]] (**73.5%** R2R-CE) |
| Speech / voice-instructed policy | [[2502.13508\|VLAS]] (**54.6%** CALVIN-speech, no ASR) |
| Teach via language / visual prompts (no typed task) | [[2411.00508\|CLIP-RT]] (NL supervision) or [[2505.02166\|CrayonRobo]] (visual prompts) |

^dm-15

> [!star] Key Papers
> - [[2507.02029|RoboBrain-2.0]] — The reference embodied-reasoning brain; sets the spatial-reasoning bar that the hierarchical-robot literature builds on
> - [[2510.11027|Vlaser]] — Shows synergistic embodied-reasoning pretraining can triple a VLM's embodied-benchmark score before it ever drives an arm
> - [[2604.01765|DriveDreamer-Policy]] — The cleanest cross-domain proof that the world-action-model recipe transfers from tabletop to autonomous driving

^key-papers-15

> [!tip] The Brain Needs Embodied Pretraining
> The unifying finding across this cluster: a general-purpose VLM is *not* an embodied brain — it confuses perspectives, fumbles spatial relations, and lacks physical grounding ([[2601.21199|Thinker]], [[2510.11027|Vlaser]]). Embodied post-training (3D coordinates, temporal grounding, affordances) is the prerequisite, and once you have a strong brain it transplants across domains — driving ([[2604.01765|DriveDreamer-Policy]]), games ([[2503.09527|CombatVLA]]), navigation ([[2605.22816|AwareVLN]]). Cross-reference [[05_VLA-Reasoning-and-CoT#5. Reasoning-Traced Training]] for the reasoning-foundation deep-dive and [[04_VLA#4. Reasoning & Planning-Augmented VLAs]] above for where this reasoning plugs into the action stack.

^insight-15

---

### 16. VLA Evaluation & Benchmarking Methodology

How we measure VLAs shapes what we build — and the field's default metric, binary task success, hides as much as it reveals. This cluster is about *measurement honesty*: diagnostic evaluation that goes beyond pass/fail, reproducible real/sim protocols that make numbers comparable across labs, and capability benchmarks that probe spatial intelligence rather than aggregate success. The recurring lesson: binary success inflates apparent capability, and two policies with identical success rates can differ wildly in trajectory quality, robustness, and speed.

#### 16.1 Beyond-Binary & Diagnostic Evaluation

Replace the single success bit with multi-dimensional diagnostics — fine-grained constraint satisfaction, trajectory quality, uncertainty, and internal value signals — that reveal *how* and *why* a policy succeeds or fails.

- **[[2606.30686|VLA Physical Reasoning Position Paper]]** — Decomposes VLA policies into ==semantic mapping== vs ==physical action decision==, arguing task-success benchmarks exhibit ==non-identifiability== (attribution/source/representation-level) that cannot verify physical reasoning; proposes controlled-variation evaluation reform.
- **[[2605.19986|MetaFine]]** — A ==compositional task graph== with atomic skills + three-dimensional diagnostic probe; shows binary success inflates capability up to **70%** (top policies **80%** "Grasp Part" but **12%** "Rotate Along" under fine-grained constraints).
- **[[2605.11479|Discounted Liveness OPE]]** — Reformulates OPE as a ==discounted liveness problem== via a min-function ==Bellman operator==; a ==two-stage bootstrapped== framework corrects ==truncation bias== via anchor-value propagation into truncated episodes; statistically significant gains across a LIBERO VLA, a diffusion-policy peg-insertion task, and hardware cloth folding.
- **[[2603.28545|ManipArena]]** — A standardized real-world ==reasoning-oriented== eval (20 tabletop+mobile tasks, server-side green-screen control); baselines max **42.7%** (640.5/1500), quantifying the generalist gap.
- **[[2507.17049|VLA-Uncertainty-Eval]]** — An evaluation of eight ==uncertainty== + five ==quality metrics== beyond success; SpatialVLA's **43.5–69.1%** "high-quality" successes show same-success policies differ in execution quality.
- **[[2605.28527|VLA-Value-Probing]]** — A ==probing-to-selection== protocol that decodes ==value-like signals== from frozen VLA features via linear ridge probes; R² **0.51–0.55** (vs scalar baseline 0.03) — frozen VLAs already know success.
- **[[2605.00321|Embodied-Interpretability]]** — A causal-attribution framework casting visual-action attribution as interventional estimation: an ==Interventional Significance Score== (KL under interventions) gives faithful explanations, a ==Nuisance Mass Ratio== scores reliance on task-irrelevant regions; NMR@k=10 shows **−0.77** Pearson with SR — spurious reliance predicts OOD failure.
- **[[2506.09930|INT-ACT]]** — A 50-task generalization benchmark (object diversity, language complexity, vision-language thinking) with an ==Intention Correct Rate== metric that decouples high-level understanding from low-level execution; exposes that VLAs hit **80–100%** intention correctness yet collapse on task success under shift, losing the VLM's linguistic robustness.

#### 16.2 Reproducible Real/Sim Evaluation

Make evaluation comparable and affordable — low-cost reproducible hardware, statistically-grounded sim-to-real inference, time-to-success primitives, and structured task suites — so reported numbers mean the same thing across labs.

- **[[2608.09892|XPolicyLab]]** — A unified ==adapter contract== + ==WebSocket RPC== serving bridge decouples N policies from M evaluation environments across sim and physical robots; connecting a VLA to a new environment drops from **300** to **~0** lines of code.
- **[[2605.20774|VLA-REPLICA]]** — A ~**$1050** off-the-shelf real-world benchmark for reproducible evaluation; π0.5 **0.54** vs ACT **0.18** ID, quantifying the pretraining benefit on standardized cheap hardware.
- **[[2605.29710|PhAIL]]** — A ==time-to-success CDF== as the eval primitive (jointly captures reliability + throughput); best VLAs are **~7×** slower than human teleop, **<19%** Human-Relative Throughput.
- **[[2603.13966|vla-eval]]** — A unified VLA eval harness across [[2306.03310|LIBERO]]/[[2112.03227|CALVIN]]/[[2405.05941|SimplerEnv]] whose client-server architecture decouples inference from execution; **47x speedup on [[2306.03310|LIBERO]]** (14h → 18min / 2,000 episodes); reproduced 6 VLAs / 3 benchmarks, exposed pitfalls (wrong proprioception **55pp**, quaternion errors **14–39pp**).
- **[[2510.04354|SureSim]]** — A policy-eval method casting it as ==Prediction-Powered Inference== over paired real/sim outcomes; **−20–25%** real-hardware effort for the same statistical confidence — cheaper honest evaluation.
- **[[2507.00435|RoboEval]]** — A structured ==bimanual== eval (8 tasks × variations, multi-dimensional metrics); same-success policies differ **4×** in Cartesian jerk, **2.7×** in path length — behavior beyond success.
- **[[2506.17561|VLA-OS]]** — A composable VLA series with ==interchangeable VLM backbone + plug-and-play planning/action heads== for controlled comparison; visually-grounded planning consistently beats language-based.
- **[[2604.09860|RoboLab]]** — An ==LLM-driven== three-stage scene/task generation + geometric solver for scalable high-fidelity sim; π0.5 **28.0%** on RoboLab-120 (13.5% on complex) — exposes the procedural-task gap.
- **[[2601.22153|DynamicVLA]]** — A 0.4B ==FastViT== VLA + ==DOM benchmark== for dynamic-object manipulation; **47.06%** DOM (vs GR00T-N1.5 13.05%) at **8.53s** — benchmark for moving targets.

#### 16.3 Spatial-Intelligence & Capability Benchmarks

Probe *specific capabilities* — 3D spatial structure, active interaction, social norms, interactive world modeling — rather than aggregate manipulation success, exposing exactly where VLMs and VLAs fall short of human competence.

- **[[2605.29074|Embodied3DBench]]** — A robot-centric ==3D spatial== benchmark (6 categories, 2D+3D) with an Isaac-Sim pipeline generating 21K+ QA pairs; 13 SOTA VLMs (even GPT-5) fail to combine metric grounding with interaction prediction, while fine-tuning Qwen3-VL-4B on 1.3M pairs lifts 3D Grounding **+40.5** points and 3D Grasp Point **+49.9** points (avg **+32.4**).
- **[[2605.18746|ESI-Bench]]** — An OmniGibson ==active-interaction== benchmark (3,081 tasks); active exploration lifts Gemini-3.1 View-Hallucination **39.9→68.1%** — measures embodied spatial intelligence that closes the perception loop.
- **[[2605.06234|RobotEQ]]** — The first ==active-intelligence== benchmark (social-norm adherence by unguided AI); GPT-5.5 Macro-F1 **66.45%**, all models far below human — the passive→active intelligence gap.
- **[[2602.20687|NativeEmbodied]]** — A ==native low-level primitive action space== (AI2THOR) with decoupled high/low-level task hierarchy; GPT-o3 only **34.64%** Search, strong on perception but weak on spatial — exposes the planning-execution gap.

#### 16.4 Efficiency & Inference-Performance Characterization

Measure *what efficiency actually costs* — analytical performance models, cross-hardware throughput characterization, and embodied-execution metrics that expose where computational savings trade against physical execution quality. The shared lesson: inference-FLOP cuts are not free, and a model's "efficiency" depends on the hardware, the metric, and the robot's motion, not just parameter count.

- **[[2602.18397|VLA-Perf]]** — A roofline-based analytical performance model decomposing VLA inference into ==Vision Encoder + VLM Backbone + Action Expert== to predict latency across architectures and hardware (73.3–82.6% fidelity to a Triton π0); datacenter GPUs hit **61–314 Hz** vs Jetson Thor **19 Hz**, and diffusion VLAs run **1–2 orders** faster than AR with chunking.
- **[[2603.19131|Embodied-Efficiency]]** — A study introducing ==embodied-efficiency metrics== (task time, path length, jerk-L2, action rate) showing compression preserves SR but harms execution: weight pruning/quantization raises jerk-L2 up to **+19.5%** and visual-token pruning blows π0.5 jerk **204%→375%** — inference savings degrade physical execution.
- **[[2509.11480|Edge-to-Cloud-VLA]]** — A cross-platform characterization of five VLAs (OpenVLA, SpatialVLA, OFT, VOTE, QwenVLA) across Jetson AGX Orin and four datacenter GPUs on SR/latency/throughput/memory; VOTE-1T tops **96.9%** LIBERO, and an optimized edge device hits **55.57 Hz** > a V100's **32.28 Hz** — edge can beat older datacenter GPUs.

**Evaluation Methodology — Decision Matrix**

| Need | Recommendation |
|---|---|
| Diagnose beyond binary success | [[2605.19986\|MetaFine]] (binary inflates **70%**) |
| Trajectory-quality metrics | [[2507.17049\|VLA-Uncertainty-Eval]] or [[2507.00435\|RoboEval]] |
| Low-cost reproducible real eval | [[2605.20774\|VLA-REPLICA]] (~$1050) |
| Statistically-efficient sim-to-real eval | [[2510.04354\|SureSim]] (**−25%** real effort) |
| Reliability + throughput jointly | [[2605.29710\|PhAIL]] (time-to-success CDF) |
| 3D spatial-intelligence probe | [[2605.29074\|Embodied3DBench]] or [[2605.18746\|ESI-Bench]] |
| Composable controlled comparison | [[2506.17561\|VLA-OS]] (interchangeable heads) |

^dm-16

> [!star] Key Papers
> - [[2605.19986|MetaFine]] — The diagnostic that proves binary success inflates apparent VLA capability by up to 70% once fine-grained constraints are enforced
> - [[2507.00435|RoboEval]] — Shows two policies with identical success rates can differ 4× in jerk and 2.7× in path length — behavior is the missing dimension
> - [[2510.04354|SureSim]] — Brings prediction-powered inference to robot evaluation, cutting the real-hardware cost of statistically honest numbers

^key-papers-16

> [!tip] Binary Success Is a Liar
> The unifying finding: pass/fail hides most of what matters. Fine-grained constraints expose 70% inflation ([[2605.19986|MetaFine]]), same-success policies differ in jerk/path/uncertainty ([[2507.00435|RoboEval]], [[2507.17049|VLA-Uncertainty-Eval]]), and capability benchmarks show VLMs far below human on 3D grounding and active intelligence ([[2605.29074|Embodied3DBench]], [[2605.06234|RobotEQ]]). Report trajectory quality, time-to-success ([[2605.29710|PhAIL]]), and reproducible cheap real numbers ([[2605.20774|VLA-REPLICA]]) — not just a success bit. Cross-reference [[02_Dataset-Benchmark-Environment#5. Diagnostic & Evaluation Datasets]] for the full benchmark landscape and [[04_VLA#18. Open Problems & Failure Modes]] below for the failure modes these diagnostics surface.

^insight-16

---

### 17. Surveys & Open Challenges

The field has matured enough to need maps — systematic reviews of the VLA landscape (architecture taxonomies, dataset/benchmark catalogs, and consensus open-challenge lists) that trace VLA architecture history and articulate the open challenges the per-paper work is collectively chipping at. These are the orientation documents: read them to place any single paper in the larger arc.

- **[[2608.01851|Weights-vs-Skills-Survey]]** — Categorizes robot-learning into =="weights"== (VLA models) vs =="skills"== (code-as-policy agents), with a five-rung ==self-improvement ladder== (Feedback/Memory/Search) classifying **77** systems + **225** cataloged works (2016-2026); flags the sparsely-populated "full self-improving loop" frontier.
- **[[2607.06706|VLA for UAVs and Bimanual Manipulation Review]]** — A review of **183** contributions (2017-2026) unifying bimanual manipulation and unmanned aerial robotics under one VLA taxonomy, showing ==flow-matching== and ==RECAP== self-improvement transfer across domains; laundry-folding **60%→90%+**, CognitiveDrone **77.2%** SR.
- **[[2604.23775|VLA-Safety-Survey]]** — The first comprehensive review of VLA safety with a unified ==threat/defense taxonomy by timing==: training-time backdoors (GoBA, SilentDrift) vs inference-time jailbreaks (RoboPAIR) and physical interventions, mapped to defenses across **6** deployment domains; flags a fragmented evaluation landscape lacking real-world long-horizon safety metrics.
- **[[2604.15395|Foundation-Models-in-Robotics-Survey]]** — A systematic review of **435** articles under a ==six-criteria taxonomy== (FM type / architecture / paradigm / stage / task / domain) tracing a ==five-phase evolution== (RT-1 → PaLM-E → GR00T N1); flags the dataset gap in tactile + failure/recovery data — the broadest FM-in-robotics map.
- **[[2512.11362|VLA-Anatomy-Survey]]** — A structured pedagogical survey dissecting VLAs into ==Modules== (perception, brain, action), tracing ==Milestones== (2017–2025), and giving a ==challenge-centric== analysis of five grand challenges (alignment, instruction following, open-world generalization, safety, data/benchmarking) with future directions. A learning-path reference.
- **[[2508.15201|VLA-Manipulation-Survey-2]]** — A systematic review structured across five dimensions, tracing the field's shift to ==Transformer==-based architectures since 2023 and consolidating the ==data pyramid== as the scalable training recipe; surveys dual-system VLA designs and flags data scarcity, generalization, and real-world deployment as the persisting gaps.
- **[[2507.10672|VLA-Manipulation-Survey]]** — A systematic review of **102** VLA models, **26** datasets, **12** simulators (2022–2025); structured taxonomy separating large generalists (RT-2, Octo) from modular specialists (DexVLA, CLIPort). The reference catalog.
- **[[2507.01925|Action-Tokenization-Survey]]** — A survey unifying VLAs as processes generating a chain of ==action tokens== from vision+language, with an ==eight-type taxonomy== (language description, code, affordance, raw action, etc.) analyzing each type's properties/limits; surfaces hierarchical-VLA and the "Data Pyramid" as key trends. The action-token-centric reference.
- **[[2506.20966|VLA-Post-Training-Survey]]** — A review of **129** VLA post-training studies via a ==human-motor-learning taxonomy== (Newell's constraints: perception / embodiment / task comprehension / integration); documents LIBERO **75% → 98%** over **16 months** and CALVIN **3.5 → 4.3** sequence length — maps the adaptation design space.
- **[[2505.04769|VLA-Concepts-Survey]]** — A survey categorizing **80+** VLA models from foundational integration (2022–23) to specialization (2024–25) across **6** domains; quantifies the deployment bottlenecks — autoregressive decoding caps speed at **3–5 Hz**, **~82%** collision accuracy, up to **40%** unseen-task degradation.
- **[[2510.24795|Efficient-VLA-Survey]]** — The first survey dedicated to ==efficient VLAs==, taxonomizing the whole "model–training–data" stack into Efficient Model Design (linear attention, Mamba, quantization, pruning), Efficient Training (data/parameter-efficient pre/post-training), and Efficient Data Collection. The reference map for §2.
- **[[2510.17111|Efficient-VLA-Survey-2]]** — A systematic survey of efficient VLAs for embodied manipulation with a ==four-dimensional taxonomy== (model architecture, perception feature processing, action generation, training/inference) and five future directions (model-data co-optimization, efficient spatio-temporal perception, compact action gen, efficiency-centric eval).
- **[[2509.19012|Pure-VLA-Survey]]** — A review of **300+** "pure VLA" methods with a taxonomy by ==action-generation strategy== (autoregression / diffusion / reinforcement / hybrid) plus foundational datasets and simulators; flags data scarcity, architectural heterogeneity, and real-time inference as the core open challenges.
- **[[2508.13073|Large-VLM-based-VLA-Survey]]** — A survey defining and taxonomizing large-VLM-based VLAs into ==monolithic== (single/dual-system) vs ==hierarchical== (planner-only / planner+policy) paradigms, surveying their integration with RL, training-free optimization, human-video learning, and world models.
- **[[2510.07077|VLA-Robotics-Real-World-Review]]** — A ==systematic, full-stack review== tracing VLA architecture from CNN-era to transformer/diffusion across the ==sensorimotor / world / affordance-based== model taxonomy; identifies the trend toward VLM-backed, hierarchically-structured models + practical gradient-insulation/PEFT considerations.
- **[[2511.05936|10-VLA-Challenges]]** — An expert-consensus catalog of **10** open challenges (multimodal sensing, robust reasoning, data quality, evaluation, cross-robot generalization, efficiency, whole-body coordination, safety) + 6 emerging trends.
- **[[2405.14093|VLA-for-Embodied-AI-Survey]]** — An early structuring survey with a ==hierarchical control taxonomy== (low-level policies vs high-level planners) + PVRs / dynamics / world-model components; aggregates datasets + simulators + benchmarks into a resource hub for language-conditioned robotics.
- **[[2312.07843|Foundation-Models-Robotics-Applications]]** — An early landscape survey mapping foundation models (LLMs/ViTs/VLMs) onto robot perception, decision-making, and control, covering ==Robot Transformers== (RT-1/RT-2) for language-conditioned manipulation and open-vocabulary perception — the pre-"VLA" orientation document.

**Surveys — Decision Matrix**

| Need | Recommendation |
|---|---|
| Comprehensive model/dataset/simulator catalog | [[2507.10672\|VLA-Manipulation-Survey]] (102 models) |
| Architecture-history + practical deployment review | [[2510.07077\|VLA-Robotics-Real-World-Review]] |
| Open-challenge orientation | [[2511.05936\|10-VLA-Challenges]] |

^dm-17

> [!star] Key Papers
> - [[2507.10672|VLA-Manipulation-Survey]] — The most comprehensive landscape catalog: 102 models, 26 datasets, 12 simulators with a clean generalist-vs-specialist taxonomy
> - [[2511.05936|10-VLA-Challenges]] — The consensus open-challenge map; the cleanest articulation of what the field still has to solve
> - [[2510.07077|VLA-Robotics-Real-World-Review]] — The full-stack history that situates each architectural era against the bottleneck it solved

^key-papers-17

> [!tip] Read the Map Before the Territory
> These surveys converge on the same arc this deep-dive traces: proof-of-concept → democratization → specialization, with the open frontier now in robustness, evaluation, cross-embodiment, and whole-body coordination. The [[2511.05936|10-VLA-Challenges]] list maps almost one-to-one onto this file's Part C clusters (memory, cross-embodiment, safety, evaluation) — read it to see which §10–§16 cluster attacks which named challenge. Cross-reference [[12_Benchmarks-and-Surveys#4. Robotics & Embodied AI Surveys]] for the vault-wide survey index and [[04_VLA#18. Open Problems & Failure Modes]] below for the failure-mode synthesis these surveys flag as the field's hardest problems.

^insight-17

---

## Part D — Open Problems & Failure Modes

*Where VLAs break: brittleness, distribution shift, action-space failure modes.*

### 18. Open Problems & Failure Modes

Understanding when VLAs break is as important as knowing when they work.

- **Spatial overfitting** — [[2505.03500|TLI]] shows VLAs map object names to *fixed training locations* instead of abstract identities; novel object positions collapse π0's `libero-ood` SR to a **9%** baseline.
- **Visual perturbation brittleness** — [[2603.22078|WAM-vs-VLA-Robustness]] finds VLAs struggle under camera/light/background changes: on RoboTwin 2.0-Plus, WAM LingBot-VA holds **74.2%** SR under perturbation vs π0.5's **58.6%**, though π0.5 recovers to the top LIBERO-Plus score (**85.7%**) with diverse training — WAMs are more robust (spatiotemporal priors from video pretraining) but not unconditionally so.
- **Adversarial patch attacks** — [[2606.03556|VLA-Patch-Attack]] shows a static physical patch from a trajectory *prefix* reaches **90.7%** ASR on LIBERO, dropping real-robot success **72% → 12%**; a single patch causes persistent long-horizon failure under partial observability.
- **Embodiment tax (VLM degradation during VLA training)** — [[2605.15735|UAM]] finds naive VLA fine-tuning destroys **>5–30%** of the underlying VLM's multimodal capability (MMMU/MME/MMBench/TextVQA), and freezing preserves understanding but kills action; a dual-stream architecture (Semantic Expert + Dorsal Expert with a generative prior) retains **>95%** VLM competence while improving OOD manipulation — control-visual features need their own parameters.
- **Detail-oriented failure** — [[2601.11421|GM-100]]'s 100 detail-oriented tasks expose very low VLA success rates — the best model (π0.5) hits only **24.9%** avg SR on the Xtrainer platform; current VLAs are coarse-grained, so fine manipulation is unsolved.
- **Counterfactual failures (vision > language)** — [[2602.17659|CAG]] finds OpenVLA-OFT scores 0.4% on counterfactual tasks vs 78.6% on originals, ignoring language when visual cues conflict; an inference-time [[2602.17659|CAG]] scheme with a VA prior mitigates this, adding +15.5% grounding.
- **Instruction paraphrase brittleness** — [[2603.28301|LIBERO-Para]] shows paraphrased instructions cause 22-52pp drops; VLAs overfit to exact instruction surface form.
- **Cross-modal failure recovery** — [[2510.01642|FailSafe]] reasons over failures and generates recoveries, hitting **0.9094** failure-detection accuracy and lifting downstream SR by **+22.6%** (OpenVLA) / **+8.0%** (OpenVLA-OFT), and turning an unseen xArm-6 "Stack Cube" from **56%→76%**; recovery requires reasoning beyond reactive policies.
- **Inference speed** — WAMs are ≥4.8x slower than VLAs ([[2504.16054|π0.5]] at 63ms/chunk is fastest); real-time control needs efficient architectures.
- **Physical degradation (joint malfunction)** — [[2605.16056|Health-VLA]] finds standard VLAs assume ideal hardware and performance collapses when joints degrade (e.g., 45% → 0% as shoulder weakness rises); conditioning the VLA on a 7D joint-health vector via a lightweight **Health Projector** (~900K params) recovers J1 from **45%→89%** at 0.3 weakness with **178** episodes of degraded-joint demos.
- **Architectural complexity ≠ generalization** — [[2510.13054|VLA-0]] fine-tunes an unmodified VLM to emit actions as plain text — no custom action head, no new tokens, no vocabulary changes — and still hits **94.7%** average LIBERO SR (rank 1.0) and beats a pretrained SmolVLA baseline by **12.5 points** real-world; the bulk of the field's action-head engineering isn't what's buying robustness.

#### 18.1 Failure Detection for VLAs

How does a deployed VLA know when it is failing? Multiple complementary approaches have emerged:

- **Internal feature monitoring** — [[2506.09937|SAFE]] extracts features from the VLA's own hidden layers and uses ==conformal prediction== to flag when the model's internal state differs from its training distribution — no external sensors needed, and at under **1ms** added inference overhead. This works because VLA representations encode task-relevant uncertainty even when the output actions look confident.
- **Semantic misalignment** — [[2509.16072|I-FailSense]] uses a VLM to compare the expected task outcome with the observed scene — detecting failures through ==semantic reasoning== rather than numerical thresholds; **90.64%** accuracy on D_SMF-CALVIN, **89.0%** on D_AHA, **74.28%** sim-to-real. This catches failures that look normal in feature space but are semantically wrong (e.g., picking up the wrong object).
- **Predictive failure** — [[2510.09459|FIPER]] combines ==OOD detection== with ==action uncertainty== to predict failures *before* they happen; **0.65** avg Timestep-Wise Accuracy, **0.78** overall accuracy, giving the system time to intervene or hand off to a human operator. This is especially valuable for safety-critical tasks where post-hoc detection is too late.
- **Density-based OOD via normalizing flows** — [[2603.11106|RC-NF]] learns the joint distribution of successful task execution via ==robot-conditioned normalizing flows==, signaling deviations in under **100ms** for real-time intervention.
- **Density-based OOD via conformal thresholds** — [[2503.08558|FAIL-Detect]] uses a novel ==logpZO== flow-based density estimator with ==Conformal Prediction== thresholds, achieving 78% balanced accuracy without any failure data.
- **Multi-detector ensembles** — [[2410.04640|Sentinel]] runs ==STAC== (Statistical Temporal Action Consistency via ==MMD==/KL-divergence) for erratic failures in parallel with a VLM for task progression failures — together detecting 18% more failures than either alone.
- **Confidence calibration** — [[2507.17383|VLA-Confidence-Calibration]] introduces ==Action-Wise Platt Scaling== + prompt ensembles to reduce Expected Calibration Error by over **20%** — trustworthy uncertainty scores for each action dimension.
- **Uncertainty from the policy's own loss** — [[2410.14868|Diff-DAgger]] uses the diffusion policy's training objective directly as an uncertainty signal, achieving **39%** higher F1 in failure prediction than ensemble baselines.
- **LLM-driven reactive recovery** — [[2407.08735|AESOP]] combines a fast embedding-based LLM anomaly detector with a slow generative LLM for deliberative intervention, using latency-aware multi-contingency MPC to achieve **100%** recovery in simulated quadrotor anomalies.
- **Human-shared-control scaling** — [[2510.02298|ARMADA]] uses ==FLOAT== (optimal-transport-based failure detection) to achieve **95%** accuracy and pool interventions across multiple robots, cutting human intervention by **23.3%**.

**Open Problems — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Spatial overfitting (names → fixed locations) | Identity-abstracting representations; diagnose with [[2505.03500\|TLI]] |
| Visual perturbation brittleness | WAM augmentation (video priors) per [[2603.22078\|WAM-vs-VLA-Robustness]] |
| Embodiment tax (VLM degrades during VLA training) | Dual-stream Semantic + Dorsal experts ([[2605.15735\|UAM]], retains **>95%** VLM competence) |
| Counterfactual failure (vision overrides language) | Inference-time [[2602.17659\|CAG]] with VA prior (**+15.5%** grounding) |
| Instruction paraphrase brittleness | Paraphrase-augmented training; diagnose with [[2603.28301\|LIBERO-Para]] |
| Failure detection at deployment | Internal monitoring ([[2506.09937\|SAFE]]), predictive OOD ([[2510.09459\|FIPER]]), density flows ([[2503.08558\|FAIL-Detect]]) |
| Failure recovery (not just detection) | Reasoning-based recovery ([[2510.01642\|FailSafe]], [[2601.02295\|CycleVLA]]) |
| Physical hardware degradation | Condition on joint-health vector ([[2605.16056\|Health-VLA]], **45%→89%** at 0.3 weakness) |

^dm-18

> [!star] Key Papers — VLA Failure Frontier
> - [[2603.22078|WAM-vs-VLA-Robustness]] — The definitive VLA-vs-WAM brittleness comparison; sets the visual-perturbation failure baseline
> - [[2605.15735|UAM]] — Names and quantifies the "embodiment tax"; dual-stream fix retains **>95%** VLM competence while improving OOD action
> - [[2510.09459|FIPER]] — Predictive failure (OOD + action uncertainty) before the failure happens; the safety-critical detection reference
> - [[2602.17659|CAG]] — Isolates the vision-overrides-language counterfactual failure (0.4% vs 78.6%); inference-time mitigation
> - [[2510.13054|VLA-0]] — Minimalist baseline whose robustness exposes how much architectural complexity is *not* buying generalization

^key-papers-18

> [!tip] The Robustness Hierarchy
> From most to least robust: (1) WAMs with video pretraining, (2) VLAs with diverse cross-embodiment training ([[2504.16054|π0.5]]), (3) VLAs with in-domain-only training. If robustness matters more than speed, consider WAM augmentation. If speed matters, use knowledge insulation + diverse training. Cross-reference [[13_Navigation-and-Mobile-Manipulation#2. Vision-Language Navigation]] for how the same hierarchy re-derives itself once the embodiment moves, and [[15_Sim-to-Real-Transfer#4. Real2Sim2Real Loops & Digital Twins]] for the transfer-side lever on tier (3).

^insight-18

---

## Quick-Reference Matrix

| Question | Answer |
|----------|--------|
| Why VLAs? | Strong robustness in real scenarios via VLM pre-training |
| Which backbone? | KosMos, [[2407.07726\|PaliGemma]] (extensive multi-modal pre-training) |
| Current generalist SOTA? | [[2604.15483\|π0.7]] (steerable open-world) and [[2604.20100\|JoyAI-RA]] (multi-embodiment) |
| Egocentric pretraining? | [[2507.15597\|Being-H0]], [[2602.16710\|EgoScale]], [[2512.22414\|π0.5-+-ego]] — see [[14_Egocentric-Pretraining-and-Human-Video#4. Pretraining Recipes — Three Generations]] |
| How to formulate? | ==Continuous actions== + ==Policy Head== for history fusion |
| How to train? | Flow Matching ≈ MSE; ==MoE== for zero-shot generalization |
| Data strategy? | ==Post-training==: cross-embodiment pre-train → in-domain fine-tune |
| Need efficiency? | [[2605.08799\|ElasticFlow]] (one-step FM, **14ms**), [[2501.09747\|FAST]] tokenization, or [[2506.01844\|SmolVLA]] (450M) |
| Need 3D? | [[2508.09071\|GeoVLA]] / [[2501.15830\|SpatialVLA]] (explicit), [[2510.12276\|Spatial-Forcing]] (implicit), or [[2605.10485\|VEGA]] (representation alignment, zero inference cost) |
| Need parameter-efficient FT? | [[2605.06175\|VLA-GSE]] (SVD generalized+specialized experts) — beats FFT **+6.3pp** on [[2510.13626\|LIBERO-Plus]] |
| Need to preserve foundational capabilities? | [[2605.08879\|ConSFT]] (confidence-weighted SFT bounds parameter disruption) |
| Need reasoning? | [[2503.22020\|CoT-VLA]] (visual CoT), [[2507.16815\|ThinkAct]] (RL latent), or [[2509.22643\|VLA-Reasoner]] (MCTS) — full taxonomy in [[05_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] |
| Need world model? | [[2602.12063\|VLAW]] (co-improvement), [[2603.16666\|Fast-WAM]] (no latency), or [[2604.26694\|X-WAM]] (4D unified) |
| Need RL? | [[2505.18719\|VLA-RL]], [[2505.17016\|RIPT-VLA]], or [[2511.15605\|SRPO]] + Knowledge Insulation + LoRA |
| Need physics priors? | [[2503.15558\|Cosmos-Reason1]] — see [[08_Physics-Aware-Embodied-AI#1. Design-Space Principles]] for the full physics-aware design space |
| Need bimanual? | [[2511.05275\|TwinVLA]] (compose two single-arm) or [[2410.07864\|RDT-1B]] |
| Need long-horizon memory? | [[2604.18791\|HELM]] (episodic store + verifier) or [[2510.00695\|HAMLET]] — see [[04_VLA#10. Memory-Augmented & Long-Horizon VLAs]] |
| Need cross-embodiment transfer? | [[2510.10274\|X-VLA]] (soft-prompt) — see [[04_VLA#11. Cross-Embodiment & Domain-Transfer VLAs]] |
| Need runtime adaptation (frozen weights)? | [[2601.06748\|TT-VLA]] (test-time RL) or [[2510.05681\|MG-Select]] (steering) — see [[04_VLA#12. Runtime Adaptation & Inference-Time Steering]] |
| Need safety / attack analysis? | [[2503.03480\|SafeVLA]], [[2411.13587\|VLA-Adversarial-Vulnerabilities]] — see [[04_VLA#13. Safety, Robustness & Adversarial VLAs]] |
| Need a generalist foundation model? | [[2508.21112\|EO-1]] or [[2503.19757\|Dita]] — see [[04_VLA#14. VLA Foundation Models & Infrastructure]] |
| Need honest evaluation? | [[2605.19986\|MetaFine]] (binary inflates **70%**) — see [[04_VLA#16. VLA Evaluation & Benchmarking Methodology]] |
| Need robustness? | WAM augmentation or diverse cross-embodiment training |

---

## Cross-References

- [[01_Embodied-AI-101]] — VLA vs WAM basics and four learning strategies
- [[06_WAM]] — Full WAM taxonomy (VideoGen, VLM-based, From Scratch)
- [[07_Latent-World-Models]] — JEPA evolution lineage ([[2506.09985|V-JEPA-2]] → [[2602.10098|VLA-JEPA]])
- [[16_Self-Evolving-VLA-WAM]] — Self-evolving VLAs, failure detection, and continual learning
- [[08_Physics-Aware-Embodied-AI]] — Physics priors for embodied AI; physics-coupled VLA pipelines
- [[05_VLA-Reasoning-and-CoT]] — Full taxonomy of where to insert reasoning into VLA pipelines
- [[14_Egocentric-Pretraining-and-Human-Video]] — Egocentric scaling laws and human→robot transfer
- [[11_Contact-Rich-and-Tactile-Control]] — Force/tactile policies deep-dive; expands §7 Multi-Sensor & Force-Aware
- [[15_Sim-to-Real-Transfer]] — Sim-to-Real Transfer deep-dive; complements VLA evaluation and deployment
- [[02_Dataset-Benchmark-Environment]] — Datasets, benchmarks, and simulation platforms

---

*See [[06_WAM]] for the world-model alternative, [[05_VLA-Reasoning-and-CoT]] for reasoning depth, or [[01_Embodied-AI-101]] to start from the basics.*
