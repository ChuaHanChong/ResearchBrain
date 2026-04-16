---
title: "How to Build a Self-Evolving WAM (Fast-WAM + VLA-JEPA)"
tags:
  - self-evolving
  - WAM
  - robotics
  - Fast-WAM
  - VLA-JEPA
  - flow-matching
  - methodology
aliases:
  - "Self-Evolving WAM (Fast-WAM + VLA-JEPA)"
  - "Self-Evolving Fast-WAM"
  - "Self-Evolving VLA-JEPA"
---

# How to Build a Self-Evolving WAM (Fast-WAM + VLA-JEPA)

> [!abstract] One-Line Summary
> Start from ==two open-source WAMs== — ==Fast-WAM== (97.6% LIBERO, MoT with Video DiT) and ==VLA-JEPA== (97.2% LIBERO, 79.5% LIBERO-Plus OOD, V-JEPA2 latent world model). Self-discover weaknesses at three levels: environment (world model prediction error + [[2412.02818|RoboMD]] RL adversary), action ([[2509.19292|SOE]] adapted for FM + [[2510.25889|πRL]] Flow-SDE), and behavioral ([[2511.00091|PLD]] probing). Self-improve via LoRA fine-tuning (ActionDiT for Fast-WAM, Qwen3-VL action head for VLA-JEPA). Evaluate on ==OOD benchmarks== ([[2510.03827|LIBERO-PRO]], [[2602.06556|LIBERO-X]], [[2603.28301|LIBERO-Para]], [[2601.11421|GM-100]]) where static models fail.

> [!info] Context
> This methodology is informed by [[00_How-to-Build-Self-Evolving-WAM|the original Self-Evolving WAM Blueprint]] and its two adversarial critiques ([[01_Critique-Self-Evolving-WAM|domain transfer critique]], [[01_Critique-Methodology-Self-Evolving-WAM|methodology critique]]). It retains the thesis that static WAMs need self-evolution, but grounds it in a concrete, open-source base model with verified compatible methods.
>
> **Revision history**: v1 ("LeWM++") tried to start from a World Model and bolt on actions — backwards. v2 proposed a hypothetical "Compact MoT WAM" at 25-55M — a target nobody asked for, with an architecture that didn't exist. ==This v3 starts from two real, open-source WAMs (Fast-WAM + VLA-JEPA) and focuses on extending their competence to scenarios where static models fail.==

---

## The Research Question

> [!danger] Both WAMs Get ~97% on Standard [[2306.03310|LIBERO]]
> Fast-WAM achieves 97.6%, VLA-JEPA achieves 97.2%. There is almost no room for self-evolution to improve in-distribution performance. Adding co-evolution to push from ~97% to ~98% is not a meaningful contribution.

> [!success] But Static Models Fail When the World Changes
> The contribution is not improving a strong WAM on its training distribution — it's ==extending its competence boundary to scenarios where static models fail==:

| Failure Scenario | Evidence | Gap |
|-----------------|----------|-----|
| **Visual/spatial perturbations** | [[2603.22078\|WAM vs VLA Robustness]]: π0.5 drops to ==58.6%== on RoboTwin 2.0-Plus; [[2510.03827\|LIBERO-PRO]]: VLAs collapse from >90% to ==near 0%== under minor perturbations; [[2602.06556\|LIBERO-X]]: only ==39.4%== at easiest level | Fast-WAM never tested; VLA-JEPA has 79.5% LIBERO-Plus but untested on PRO/X |
| **Language paraphrase** | [[2603.28301\|LIBERO-Para]]: ==22.8-51.9pp drops== from paraphrased instructions alone | Both untested — do they overfit to instruction phrasing? |
| **Detail-oriented tasks** | [[2601.11421\|GM-100]]: best VLA achieves only ==24.9%== on detail-oriented manipulation | Both untested on GM-100 |
| **Novel compositions** | [[2505.03500\|TLI]]: only ==9%== on novel spatial compositions | Structural limitation of all static models |
| **Unseen tasks** | [[2602.15922\|DreamZero]]: ==39.5%== on unseen tasks (similar scale) | Both WAMs' unseen-task performance unpublished |

> [!tip] The Thesis (Sharpened)
> **Self-evolution doesn't make a good WAM better on tasks it already solves. It makes a good WAM robust to tasks it has never seen.** The contribution: demonstrate that self-evolution closes the distribution-shift gap for two strong WAMs (Fast-WAM + VLA-JEPA), using methods verified to be compatible with both architectures — proving the approach is framework-agnostic.

---

## Base Models

We evaluate on ==two open-source WAMs== to demonstrate framework-agnostic applicability. Both use ==flow matching for actions== — all self-evolution methods (πRL, SOE, PLD, RoboMD) work identically on both.

> [!info] Why Fast-WAM?
> ==Strongest open-source WAM== (97.6% [[2306.03310|LIBERO]], 91.8% [[2506.18088|RoboTwin]]). Published code ([GitHub](https://github.com/yuantianyuan01/FastWAM)) + checkpoints ([HuggingFace](https://huggingface.co/yuanty/fastwam)). MoT architecture: ActionDiT (~640M) + Video DiT (~5B, [Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)). ==Flow-matching action head==. World model: Video DiT predicts future frames in pixel/video space. Video DiT kept during self-evolving loop (810ms, A100) for prediction error + dreams; stripped for deployment (190ms, 20-30 Hz). Trade-off: prediction error requires A100 (5B Video DiT); OOD performance untested.

> [!info] Why VLA-JEPA?
> ==Strongest open-source JEPA-based WAM== (97.2% [[2306.03310|LIBERO]], ==79.5% LIBERO-Plus OOD==, 65.2% [[2405.05941|SimplerEnv]]). Published code ([GitHub](https://github.com/ginwind/VLA-JEPA)) + checkpoints ([HuggingFace](https://huggingface.co/ginwind/VLA-JEPA)), Apache 2.0. Architecture: V-JEPA2 (ViT-L) world model + Qwen3-VL-2B VLM backbone. ==Flow-matching action head== (same as Fast-WAM — all exploration methods transfer). World model: V-JEPA2 has latent prediction capability (`vj_encoder` + `vj_predictor` modules) but is ==dormant at inference by default== — needs explicit activation for prediction error in the self-evolving loop. LIBERO-Plus eval built into repo. Trade-off: slightly lower in-distribution (97.2% vs 97.6%); latent-level dreams only (no pixel video).

**Key differences only** (everything else is the same):

| | Fast-WAM ([[2603.16666\|paper]]) | VLA-JEPA ([[2602.10098\|paper]]) |
|---|---|---|
| **World model** | Video DiT (~5B) — ==pixel/video== prediction | V-JEPA2 (ViT-L) — ==latent== prediction |
| **VLM backbone** | T5 text encoder | Qwen3-VL-2B |
| **LIBERO / OOD** | ==97.6%== / untested | 97.2% / ==79.5% LIBERO-Plus OOD== |
| **Prediction error** | ==Expensive== (5B Video DiT, A100) | ==Free== (V-JEPA2 is integrated) |
| **LoRA target** | ActionDiT attention layers (~640M) | VLA action head + Qwen3-VL-2B |
| **Dream space** | Pixel-level future frames | Latent-level future states |

### Actual Architecture (from GitHub)

Fast-WAM's codebase reveals the concrete architecture:

```
Training (MoT — Mixture of Transformers):
  Observation → Wan2.2 VAE Encoder → Latent Patches
                     ↓
       ┌─────────────┴─────────────┐
       ↓                           ↓
  ActionDiT                    Video DiT
  (hidden=1024, 30 layers,    (hidden=3072, 30 layers,
   24 heads, ~640M)            24 heads, Wan2.2-5B)
       ↓                           ↓
  Action Chunks               Future Frames
  (flow matching)             (flow matching)
       └─────────────┬─────────────┘
              Mixed Attention
              (shared visual tokens)

Self-Evolving Mode (Full MoT — Video DiT KEPT):
  Observation → Wan2.2 VAE → ActionDiT + Video DiT → Action Chunks + Future Frames
                                (~5.6B total, ~810ms per step, ~1.2 Hz on A100)
                                Video DiT enables: prediction error, dream generation,
                                world model supervision for self-evolving loop

Deployment Mode (ActionDiT only — Video DiT stripped):
  Observation → Wan2.2 VAE → ActionDiT → Action Chunks
                                (~640M, ~190ms, ~20-30 Hz)
```

| Component | Architecture | Params | Role |
|-----------|-------------|--------|------|
| **VAE Encoder** | [Wan2.1-T2V-1.3B](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) tokenizer | Shared | Encodes RGB → latent patches |
| **ActionDiT** | DiT: hidden=1024, ffn=4096, 30 layers, 24 heads | ==~640M== | Predicts action chunks via flow matching — ==LoRA fine-tuned during self-evolution== |
| **Video DiT** | DiT: hidden=3072, ffn=14336, 30 layers, 24 heads | ~5B ([Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)) | ==Kept during self-evolving loop== — provides prediction error, dream generation, world model supervision. Frozen (not fine-tuned). Stripped only for final deployment. |
| **T5 Encoder** | T5 text encoder | Shared | Language conditioning for task instructions |
| **MoT** | Mixed attention between ActionDiT and Video DiT | N/A | Enables joint training with shared visual tokens |

### Compute Requirements

**Fast-WAM:**

| Task | GPUs Needed | Feasible for Us? |
|------|-------------|-----------------|
| **Self-evolving sim rollouts** (full MoT: ActionDiT + Video DiT) | ==A100 (80GB)== | Yes — ~810ms/step, sufficient for sim data collection |
| **LoRA fine-tuning** (ActionDiT only, Video DiT frozen) | ==2-4 GPUs== | Yes — LoRA trains <1% of ActionDiT parameters |
| **Final deployment** (ActionDiT only, Video DiT stripped) | ==1 GPU== | Yes — ~190ms, 20-30 Hz real-time control |
| **Full MoT training from scratch** | 8-64 GPUs | No — use released checkpoints as starting point |

**VLA-JEPA:**

| Task | GPUs Needed | Feasible for Us? |
|------|-------------|-----------------|
| **Self-evolving sim rollouts** (V-JEPA2 activated) | ==Standard GPU== | Yes — no 5B Video DiT branch, lighter compute |
| **LoRA fine-tuning** (Qwen3-VL-2B action head) | ==1-2 GPUs== | Yes — smaller action head than Fast-WAM's ActionDiT |
| **Final deployment** (action head only, or full model) | ==1 GPU== | Yes — V-JEPA2 is lightweight, optionally retained |
| **Full model training from scratch** | Multiple GPUs | No — use released checkpoints as starting point |

> [!tip] Two Modes, One Model
> During the self-evolving loop (sim), we run the ==full model== with world model active — Fast-WAM: full MoT on A100 (Video DiT provides prediction error + dreams, ~1.2 Hz); VLA-JEPA: V-JEPA2 activated for prediction error (standard GPU, lightweight). After self-evolution, we ==strip the world model== for deployment — Fast-WAM: ActionDiT alone at 20-30 Hz; VLA-JEPA: action head alone (or V-JEPA2 optionally retained since it's lightweight). Self-evolved improvements are baked into LoRA-updated weights for both.

---

## The Key Methodological Shift: One Integrated Self-Evolving Loop

The original blueprint proposed ==three nested loops running simultaneously== (Inner, Middle, Outer). The methodology critique ([[01_Critique-Methodology-Self-Evolving-WAM|Part IV]]) showed this creates destructive interference — Inner Loop forward-updates (ms) are overwritten by Middle Loop backprop (hours), and the system has no external ground truth.

> [!danger] The Original Failure
> Nesting three separate loops assumes they ==compose gracefully==. No evidence exists that they do. Each loop was validated in isolation in its source paper, and no paper tested the interaction between any two loops.

> [!success] The Fix: One Integrated Loop with External Measurement
> Instead of three nested loops, we use ==one integrated self-evolving loop== that combines self-discovery (DIVERSIFY + DETECT + EXPLORE), self-improvement (PROBE + LEARN + DISTILL + DREAM), and external measurement (MEASURE on held-out benchmarks). Each step uses a verified method; the loop is tested as a whole with ==OOD benchmarks as the external ground truth==.

---

## Phase 0-1: Establish the Baseline and the Gap

### Phase 0: Reproduce Baselines (Both Models)

**Goal**: Confirm published results using released checkpoints for both WAMs.

1. Load Fast-WAM checkpoints from HuggingFace (`yuanty/fastwam`)
2. Evaluate Fast-WAM on standard [[2306.03310|LIBERO]] (target: ~97.6%) and [[2506.18088|RoboTwin]] (target: ~91.8%)
3. Load VLA-JEPA checkpoints from HuggingFace (`ginwind/VLA-JEPA`)
4. Evaluate VLA-JEPA on standard LIBERO (target: ~97.2%), LIBERO-Plus (target: ~79.5%), and [[2405.05941|SimplerEnv]] (target: ~65.2%)

This is validation, not training. Should take hours, not days.

### Phase 1: Establish Failure Cases (The First Contribution)

**Goal**: Demonstrate ==where both WAMs fail== on OOD scenarios — nobody has published Fast-WAM's OOD results, and VLA-JEPA's coverage is partial (LIBERO-Plus only).

| Test | Benchmark | What It Measures | Expected Outcome |
|------|-----------|-----------------|-----------------|
| Spatial/object perturbations | [[2510.03827\|LIBERO-PRO]] (4 perturbation dims) | Object attributes, positions, language, environment | VLAs collapse from >90% to ==near 0%==. Both WAMs: untested |
| Hierarchical robustness | [[2602.06556\|LIBERO-X]] (5 difficulty levels, 600 tasks) | Progressive spatial, object property, instruction perturbations | VLAs: ==39.4%== at easiest level. Both WAMs: untested |
| Visual perturbations | [[2603.22078\|LIBERO-Plus]] (7 perturbation dims, 21 sub-dims) | Camera, lighting, background, layout shifts | π0.5: 85.7% → 58.6% on perturbed RoboTwin. VLA-JEPA: 79.5% LIBERO-Plus |
| Language paraphrase | [[2603.28301\|LIBERO-Para]] | Semantically equivalent instruction variations | VLAs drop ==22.8-51.9pp==. Both WAMs: untested |
| Detail-oriented tasks | [[2601.11421\|GM-100]] (100 tasks) | Precision manipulation | Best VLA: 24.9%. Both WAMs: unpublished |
| Long-horizon | [[2112.03227\|CALVIN]] (5-step chains) ([GitHub](https://github.com/mees/calvin)) | Multi-step instruction following | Best: 4.33 completion length ([[2412.14803\|VPP]]) |

> [!tip] Establishing the Gap IS a Contribution
> If Fast-WAM drops from 97.6% to 40% on LIBERO-Plus physics perturbations — and VLA-JEPA drops similarly on LIBERO-PRO despite its 79.5% LIBERO-Plus baseline — those results alone are publishable. They quantify the robustness gap for the two strongest open-source WAMs. Self-evolution then becomes the proposed solution.

---

## Self-Evolution Methods: What Works with Both WAMs

> [!danger] The Diffusion Gap
> ==No existing literature has tested self-evolution loops on diffusion/flow-matching architectures.== All proven self-evolution methods (STaR, TTRL, VLAW, EvoAgent) were tested on autoregressive LLMs, RL agents, or separate world models. This is both a risk (uncharted territory) and a contribution (first to demonstrate it).

> [!warning] VLAW Is Incompatible with Both WAMs
> [[2602.12063|VLAW]]'s co-evolution requires ==separate== world model and policy that alternate training. Fast-WAM trains them ==jointly== via MoT with shared attention; VLA-JEPA integrates V-JEPA2 and the action head in a unified forward pass. You can't alternate what's already joint/integrated. The principle (use world model dreams to improve policy) transfers, but VLAW's specific alternation mechanism does not.

### Verified Compatible Methods

| Method | Paper | Compatibility | Role |
|--------|-------|---------------|------|
| **SAFE VLA feature probing** | [[2506.09937\|SAFE]] | ==98%== | ==Failure detection baseline==: probe VLA hidden states → conformal prediction threshold. Tested on pi0, pi0-FAST, OpenVLA. <1ms overhead. NeurIPS 2025 |
| **πRL Flow-SDE** | [[2510.25889\|πRL]] | ==95%== | ==Action-level uncertainty==: converts ODE to SDE for stochastic sampling. Tested on pi0/pi0.5, 29-31% gains |
| **SOE adapted for FM** | [[2509.19292\|SOE]] | ==90%== | ==Action-level active probing==: VIB is architecture-agnostic MLPs + conditioning noise injection. Swap DDPM decoder for FM equivalents |
| **World model prediction error** | Inspired by [[2602.20057\|AdaWorldPolicy]] | ==70%== | ==Environment-level discovery==: prediction error in latent space. ==Our novel use== of the world model — the principle transfers, not the architecture |
| **RoboMD RL adversary** | [[2412.02818\|RoboMD]] | ==98%== | ==Environment-level active probing==: RL adversary actively searches for failure-inducing conditions. Policy-agnostic black-box |
| **ResFiT residual RL** | [[2509.19301\|ResFiT]] | ==95%== | ==Recovery baseline==: frozen base + bounded residual + off-policy TD3 + distributional critic. Treats base as black box |
| **PLD enhancements** | [[2511.00091\|PLD]] | ==95%== | ==Recovery improvements==: SAC entropy + Cal-QL conservative warmup + hybrid data collection. Tested on π0 + OpenVLA |
| **Q-chunking** | [[2507.07969\|Q-chunking]] | ==90%== | ==Chunk-aware Q==: Q-function over H-step action chunks, not per-step. Unbiased n-step backups. NeurIPS 2025 |
| **RFS dual modulation** | [[2602.01789\|RFS]] | ==85%== | ==Noise steering + residual==: joint input/output modulation for FM policies. Enables global behavioral shifts + local corrections |
| **PlayWorld** | [[2603.09030\|PlayWorld]] | ==100%== | ==Data collection==: autonomous self-play rollouts including failures. Architecture-agnostic |

### Verified Incompatible Methods

| Method | Paper | Why Incompatible |
|--------|-------|-----------------|
| **VLAW alternation** | [[2602.12063\|VLAW]] | Requires separate models. Fast-WAM is joint via MoT; VLA-JEPA integrates world model and action head |
| **SIGReg** | [[2603.19312\|LeWM]] | Designed for JEPA collapse. Flow matching doesn't collapse (irrelevant for both WAMs) |
| **CEM planning** | [[2603.19312\|LeWM]] | Both WAMs output actions directly, not state predictions. Can't roll forward through the action head |
| **DyWA FiLM** (as-is) | [[2503.16806\|DyWA]] | Uses point cloud input. Both WAMs use RGB-based pipelines. The FiLM concept transfers but needs significant adaptation |
| **NavMorph CEM** | [[2506.23468\|NavMorph]] | Can only interpolate — retrieves similar past experiences, can't handle genuinely novel physics |

---

## Phase 2: The Self-Evolving Loop

**Goal**: Both WAMs ==discover their own weaknesses== at three levels (environment, action, language) and improve on them — without human-designed perturbation types. The loop is ==identical for both models== except DETECT (Video DiT vs V-JEPA2), DISTILL (ActionDiT vs Qwen3-VL action head), and DREAM (pixel vs latent space).

### Three Levels of Self-Discovery

| Level | What It Discovers | Active (stress-tests) | Passive (measures signals) |
|-------|------------------|----------------------|--------------------------|
| **Environment** | Which sim conditions are hard | [[2412.02818\|RoboMD]] RL adversary (policy-agnostic) | SAFE VLA feature probing ([[2506.09937\|SAFE]]) + world model prediction error |
| **Action** | Which action variations cause failure | [[2509.19292\|SOE]] adapted for FM — VIB MLPs + conditioning noise, swap decoder | [[2510.25889\|πRL]] Flow-SDE stochastic sampling |
| **Behavioral** | Where the model actually fails | Residual RL probing: [[2509.19301\|ResFiT]] + [[2511.00091\|PLD]] + [[2507.07969\|Q-chunking]] + [[2602.01789\|RFS]] | — |
| **Language** | Instruction phrasing sensitivity | LLM paraphrase augmentation | Action divergence across paraphrases |

### The Method: DIVERSIFY → IMAGINE + DETECT → EXPLORE → PROBE → LEARN → DISTILL + DREAM → MEASURE

```
1. DIVERSIFY: Deploy WAM in broadly randomized sim environments
   Fast-WAM: full MoT (ActionDiT + Video DiT) on A100
   VLA-JEPA: full model (standard GPU — no 5B branch)
   + Language augmentation: LLM generates 3-5 paraphrases per task
    ↓
2. DETECT: Multi-signal failure detection →
   Signal 1: SAFE VLA feature probing (NeurIPS 2025, <1ms)
   Signal 2: World model prediction error
     Fast-WAM: Video DiT (pixel/VAE latent, A100)
     VLA-JEPA: V-JEPA2 (JEPA latent, free)
   Signal 3: Action-chunk entropy (FIPER, optional)
   Flag episode if ≥2 signals fire simultaneously
    ↓
3. EXPLORE (three active probing levels):
   a. ENVIRONMENTAL: RoboMD RL adversary searches for
      failure-inducing sim conditions (policy-agnostic)
   b. ACTION: SOE (adapted for FM) perturbs conditioning →
      finds action-level weaknesses
   c. UNCERTAINTY: πRL Flow-SDE → diverse action sampling →
      high variance = model is uncertain
   (all three work identically on both WAMs — flow matching)
    ↓
4. PROBE + LEARN: Layered residual recovery
   Layer 1: ResFiT residual off-policy RL (baseline)
   Layer 2: PLD enhancements (SAC + Cal-QL + hybrid rollout)
   Layer 3: Q-chunking (chunk-aware Q) + RFS (dual modulation)
    ↓
5. DISTILL: Recovery data → LoRA fine-tune action model
   Fast-WAM: LoRA on ActionDiT (non-mixed-attention layers only)
   VLA-JEPA: LoRA on Qwen3-VL-2B action head
   (world model frozen in both — provides supervision only)
   + Replay buffer (2% old data) prevents forgetting
    ↓
6. DREAM: World model generates additional future-state rollouts
   Fast-WAM: Video DiT → pixel-level dreams
   VLA-JEPA: V-JEPA2 → latent-level dreams
    ↓
7. MEASURE: Benchmark evaluation (LIBERO-PRO, LIBERO-X, etc.)
   Benchmarks are the EXAM, not the TEXTBOOK.
   → Repeat from step 1
```

### How the Methods Integrate

| Step | Level | Method | Paper | What It Does |
|------|-------|--------|-------|-------------|
| DIVERSIFY | Environment | Broad procedural randomization + language augmentation | [[2603.16861\|MolmoBot]], [[2506.12851\|KungfuBot]] | Diverse sim conditions + paraphrased instructions |
| DETECT (signal 1) | VLA confidence | SAFE VLA feature probing | [[2506.09937\|SAFE]] (NeurIPS 2025) | Probe VLA hidden states → conformal prediction threshold. <1ms, zero-shot to unseen tasks. |
| DETECT (signal 2) | World model | Prediction error (latent space) | Inspired by [[2602.20057\|AdaWorldPolicy]] | World model predicts future → high error = surprise. Fast-WAM: Video DiT (pixel/VAE latent); VLA-JEPA: V-JEPA2 (JEPA latent). ==Our novel use of the world model.== |
| DETECT (fusion) | Both | Multi-signal fusion (≥2 of 3) | ==Our design== | Combine SAFE + prediction error + action entropy → flag if ≥2 fire. |
| EXPLORE (env) | Environment | RL adversary | [[2412.02818\|RoboMD]] | Actively searches for failure-inducing conditions. Policy-agnostic. |
| EXPLORE (action) | Action | SOE adapted for FM | [[2509.19292\|SOE]] | VIB MLPs + conditioning noise. Replace DDPM decoder with FM equivalents. |
| EXPLORE (uncertainty) | Action | Flow-SDE stochastic sampling | [[2510.25889\|πRL]], [[2505.05470\|Flow-GRPO]] | ODE → SDE → stochastic action samples → high variance = uncertainty |
| PROBE + LEARN | Behavioral | Layered residual RL | [[2509.19301\|ResFiT]] + [[2511.00091\|PLD]] + [[2507.07969\|Q-chunking]] + [[2602.01789\|RFS]] | ResFiT residual baseline → PLD SAC/Cal-QL/hybrid → Q-chunking + RFS dual modulation. |
| DREAM | Environment | World model imagination | [[2603.16666\|Fast-WAM]] Video DiT / [[2602.10098\|VLA-JEPA]] V-JEPA2 | Future-state rollouts from imagination — extra training data. Fast-WAM: pixel-level; VLA-JEPA: latent-level. |
| Data collection | Both | Self-play rollouts | [[2603.09030\|PlayWorld]] | Autonomous diverse rollouts including failures. |

### Training Data (All Self-Generated)

| Source | What It Is | How Generated |
|--------|-----------|---------------|
| **Flow-SDE diverse rollouts** | Action variations from stochastic ODE sampling | [[2510.25889\|πRL]] Flow-SDE generates diverse action chunks |
| **High-error scenarios** | Environments where world model is surprised | World model prediction error identifies these (Fast-WAM: Video DiT; VLA-JEPA: V-JEPA2) |
| **SOE exploration rollouts** | Action variations from conditioning perturbation | [[2509.19292\|SOE]] adapted for FM perturbs VIB latent |
| **PLD recovery data** | Recovery trajectories from failure states | [[2511.00091\|PLD]] + [[2510.25889\|πRL]] RL specialists generate these |
| **Dream rollouts** | Future-state imagination | World model generates from diverse initial conditions (Fast-WAM: Video DiT pixel dreams; VLA-JEPA: V-JEPA2 latent dreams) |
| **Autonomous rollouts** | Diverse self-play including failures | [[2603.09030\|PlayWorld]]-style deployment in sim |
| **Replay buffer** | 2% of original [[2306.03310\|LIBERO]] demonstrations | Prevents forgetting ([[2603.03818\|VLA CL]]) |

### Why NOT VLAW?

> [[2602.12063|VLAW]]'s "co-evolution" requires ==separate== world model and policy. Both our WAMs integrate them: Fast-WAM trains jointly via MoT; VLA-JEPA unifies V-JEPA2 and the action head. We use "self-evolving loop" instead: world model prediction error (inspired by [[2602.20057|AdaWorldPolicy]]) + SOE adapted for FM ([[2509.19292|SOE]]) + πRL Flow-SDE ([[2510.25889|πRL]]) + PLD failure probing ([[2511.00091|PLD]]).

### Success Criterion

Measurable improvement on ==OOD benchmarks==, not standard LIBERO:

| Metric | Baseline (Phase 1) | Target After Self-Evolving Loop |
|--------|-------------------|-------------------------------|
| [[2510.03827\|LIBERO-PRO]] success rate | Measured in Phase 1 | >15% improvement |
| [[2602.06556\|LIBERO-X]] success rate | Measured in Phase 1 | >10% improvement |
| [[2603.28301\|LIBERO-Para]] success rate | Measured in Phase 1 | >10% improvement |
| [[2601.11421\|GM-100]] detail tasks | Measured in Phase 1 | >10% improvement |

**Done when**: positive improvement slope for $\geq 3$ consecutive rounds on OOD scenarios, with <2% regression on standard [[2306.03310|LIBERO]].

---

## Why Simple Continual Learning Suffices

The original blueprint proposed three simultaneous CL mechanisms: EWC, Latent Experience Replay, and Task-Aware Gradient Projection. The methodology critique showed these ==fight each other==:

> EWC says "don't change weight $w_i$." Gradient Projection says "change $w_i$, but only orthogonally." If the orthogonal subspace is empty, the system is frozen — it can never learn anything new. — [[01_Critique-Methodology-Self-Evolving-WAM#2.4 The Three CL Mechanisms Conflict|Part II.4]]

The strongest counter-evidence:

- [[2603.11653|VLA RL Continual Learning]]: Simple LoRA fine-tuning achieves ==$<2\%$ forgetting==. Tested on [[2410.24164|π0]] (flow-matching VLA — same training paradigm as both WAMs). Complex CL methods were consistently outperformed.
- [[2603.03818|VLA Continual Learning]]: Only ==$2\%$ replay buffer== needed for near-zero backward transfer.

> [!success] The Principle
> ==LoRA + replay buffer.== That's it. LoRA constrains updates to low-rank (preventing catastrophic changes), replay prevents forgetting, and flow matching's objective is inherently stable. No SIGReg, no EWC, no gradient projection.

---

## Data & Simulation Strategy

> [!info] No Robot Available
> This methodology targets ==simulation-only== training and evaluation. All benchmarks, data collection, and self-evolution loops run in simulation. The key validation from [[2603.16861|MolmoBot]]: large-scale procedural simulation enables ==79.2% real-world zero-shot transfer== without any real data — sim-only is a viable research path.

### Simulation Benchmarks

| Benchmark | Scale | WAMs Tested On It | Role |
|-----------|-------|-------------------|------|
| **[[2306.03310\|LIBERO]]** | 130 language-conditioned tasks, 7-DOF arm ([GitHub](https://github.com/Lifelong-Robot-Learning/LIBERO)) | Fast-WAM (97.6%), VLA-JEPA (97.2%), [[2601.16163\|Cosmos Policy]] (98.5%) | ==Primary benchmark== — both WAMs' target, [MuJoCo](https://mujoco.org)-based |
| **LIBERO-Plus** ([[2603.22078\|WAM vs VLA Robustness]]) | LIBERO + 7 perturbation dimensions, 21 sub-dimensions | Fast-WAM untested; VLA-JEPA: ==79.5%==; [[2410.24164\|π0.5]] drops from 85.7% to 58.6% on perturbed RoboTwin | ==OOD evaluation== — where self-evolution should show improvement |
| **[[2601.11421\|GM-100]]** | 100 detail-oriented tasks, 2 platforms | Best VLA ([[2410.24164\|π0.5]]): 24.9% | ==Detail task evaluation== — the hard frontier |
| **[[2506.18088\|RoboTwin 2.0]]** | Bimanual, 5D domain randomization ([GitHub](https://github.com/TianxingChen/RoboTwin)) | [[2603.16666\|Fast-WAM]] (91.8%), [[2512.13030\|Motus]] (88.66%) | ==Secondary== — harder bimanual tasks |
| **[[2405.05941\|SimplerEnv]]** | Perturbation diagnostics ($r > 0.85$ sim-real) ([GitHub](https://github.com/simpler-env/SimplerEnv)) | [[2508.19236\|MemoryVLA]] (71.9%) | ==Diagnostic== — cheap policy ranking, detects regression |

### Training Data Sources

| Source | Scale | Open? | Role |
|--------|-------|-------|------|
| **Fast-WAM checkpoints** | Pre-trained ActionDiT + Video DiT | Yes ([HuggingFace](https://huggingface.co/yuanty/fastwam)) | ==Starting point #1== — no need to train from scratch |
| **VLA-JEPA checkpoints** | Pre-trained V-JEPA2 + Qwen3-VL-2B + action head | Yes ([HuggingFace](https://huggingface.co/ginwind/VLA-JEPA)) | ==Starting point #2== — no need to train from scratch |
| **[[2306.03310\|LIBERO]] demonstrations** | ~24h teleoperated, 34 tasks ([download](https://github.com/Lifelong-Robot-Learning/LIBERO)) | Yes | Benchmark data for evaluation and optional fine-tuning |
| **MolmoBot-Data** (procedural sim) | ==1.8M trajectories==, 232K environments, 48K objects ([GitHub](https://github.com/allenai/molmobot)) | Yes | Procedural data for co-evolution diversity ([[2603.16861\|MolmoBot]]) |
| **Self-generated rollouts** | Unbounded | N/A | WAM rollouts in sim including failures — the ==self-evolution data source== |

> [!tip] Diversity Beats Scale
> [[2403.12945|DROID]] showed that 76K diverse trajectories outperform 1M+ less-diverse trajectories. For self-evolution, ==procedural diversity in physics parameters== (the Outer Loop) is the key lever.

### Simulation Engine

**[MuJoCo](https://mujoco.org)** as the primary engine — [[2306.03310|LIBERO]]'s native backend, free, open-source, well-documented ([GitHub](https://github.com/google-deepmind/mujoco)). Physics parameters (mass, friction, damping) directly exposed for broad procedural randomization and [[2412.02818|RoboMD]] adversarial search.

### Domain Randomization

Following [[2506.18088|RoboTwin 2.0]]'s 5-dimension approach + [[2603.16861|MolmoBot]]'s procedural generation:

| Dimension | What to Randomize | Source |
|-----------|-------------------|--------|
| **Camera** | Position, angle, field of view | [[2506.18088\|RoboTwin 2.0]] |
| **Lighting** | Direction, intensity, color temperature | [[2506.18088\|RoboTwin 2.0]] |
| **Background** | Textures, distractor objects | [[2506.18088\|RoboTwin 2.0]] |
| **Physics** | Object mass, friction, damping, size | Broad randomization ([[2506.12851\|KungfuBot]]-style) |
| **Language** | Task instruction paraphrases | [[2506.18088\|RoboTwin 2.0]] |
| **Objects** | Geometry, texture, count (procedural) | [[2603.16861\|MolmoBot]] |

> [!warning] Physics randomization supports self-discovery
> Broad physics randomization provides diverse conditions for world model prediction error to flag (Video DiT for Fast-WAM, V-JEPA2 for VLA-JEPA). [[2412.02818|RoboMD]]'s RL adversary then actively searches within this space for failure-inducing regimes — this is the environment-level active probing from the self-evolving loop (Step 3a).

---

## What Survives from the Original Blueprint

| Retained | Changed | Dropped |
|----------|---------|---------|
| The thesis: static WAMs need self-evolution | 14B DreamZero → ==two open-source WAMs (Fast-WAM + VLA-JEPA), world models kept== | LeWM entirely (SIGReg, CEM — unnecessary for flow matching) |
| Self-evolution loop structure | Three nested loops → ==one integrated self-evolving loop== (DIVERSIFY → DETECT → EXPLORE → PROBE → LEARN → DISTILL → DREAM → MEASURE) | NavMorph CEM (can only interpolate) |
| Self-discovery mechanism | Human-designed perturbations → ==three-level self-directed discovery== (environment + action + language, active + passive) | AVIC adaptive depth (miscited for manipulation) |
| PlayWorld autonomous data collection | Hypothetical "Compact MoT WAM" → ==use actual released checkpoints (Fast-WAM + VLA-JEPA)== | SPIRAL CriticAgent (evaluates video, not physics) |
| Failure data is non-negotiable | Full model (sim) → stripped action model (deploy) for both WAMs | DyWA FiLM as-is (point cloud input, needs significant adaptation) |
| Convergence via held-out eval | Standard LIBERO evaluation → ==OOD evaluation (LIBERO-Plus, GM-100, physics perturbations)== | Plan2Explore curiosity ensemble (70B overhead) |
| Sequential loop validation | | Absolute Zero's verifier (requires physics oracle) |

---

## FAQ

> [!question] What is the formula?
> **WAM (with world model active) + πRL + AdaWorldPolicy (principle) + PLD + PlayWorld = Self-Evolving WAM.** Applied identically to both Fast-WAM and VLA-JEPA.
> - [[2510.25889|πRL]]: ==Flow-SDE stochastic exploration + RL mechanism== for flow matching. Provides passive uncertainty signal + RL training for PLD specialists.
> - [[2509.19292|SOE]] adapted for FM: ==Active action-level probing==. VIB is just MLPs + conditioning noise — swap DDPM decoder for the action model's FM decoder.
> - World model prediction error (inspired by [[2602.20057|AdaWorldPolicy]]): ==Environment-level discovery==. Our novel use of each WAM's world model (Video DiT for Fast-WAM, V-JEPA2 for VLA-JEPA).
> - [[2511.00091|PLD]]: ==Failure recovery== (probe → learn → distill). πRL provides the RL training for PLD's specialists.
> - [[2603.09030|PlayWorld]]: ==Autonomous data collection==.

> [!question] What is the training data?
> ==Self-generated sim rollouts.== The model acts in perturbed [[2306.03310|LIBERO]] scenarios in [MuJoCo](https://mujoco.org), and its own trajectories (successes + failures + adapted rollouts) become the training data. A 2% replay buffer of original demonstrations prevents forgetting. No new human demonstrations needed — that's what makes it "self-evolving."

> [!question] Benchmarks are NOT training data?
> Correct. Benchmarks ([[2510.03827|LIBERO-PRO]], [[2602.06556|LIBERO-X]], [[2603.28301|LIBERO-Para]], [[2601.11421|GM-100]]) are ==held-out evaluation only==. Never trained on. Used before the self-evolving loop (Phase 1: measure the gap) and after (measure improvement).

> [!question] How does the model find its own weaknesses?
> ==Active + passive probing at three levels (identical for both WAMs):==
> 1. **Environment (active)**: [[2412.02818|RoboMD]] RL adversary searches for failure-inducing conditions (policy-agnostic)
> 2. **Environment (passive)**: World model prediction error flags surprise — Fast-WAM: Video DiT (pixel/VAE latent); VLA-JEPA: V-JEPA2 (JEPA latent)
> 3. **Action (active)**: [[2509.19292|SOE]] adapted for FM — VIB is just MLPs + conditioning noise injection. Swap DDPM decoder for the action model's FM decoder. Finds ==behavioral boundaries==.
> 4. **Action (passive)**: [[2510.25889|πRL]] Flow-SDE measures action uncertainty
> 5. **Behavioral**: [[2511.00091|PLD]] deploys model → observes failures → trains recovery
> 6. **Language**: LLM paraphrases instructions → compares action divergence
>
> Benchmarks ==measure== whether improvements transfer — they don't ==design== the curriculum.

> [!question] Can both WAMs imagine future states?
> ==Yes, when the world model is kept active.== Fast-WAM: full MoT mode (810ms, ~1.2 Hz on A100) — Video DiT provides prediction error, dream generation, and world model supervision. VLA-JEPA: V-JEPA2 activated for prediction error and latent-level dreams (standard GPU, lightweight). After self-evolution, we strip the world model for deployment — Fast-WAM: ActionDiT alone (190ms, 20-30 Hz); VLA-JEPA: action head alone (or V-JEPA2 optionally retained). Improvements are baked into LoRA-updated weights for both.

> [!question] What does "self-evolving" mean? Why not "co-evolution"?
> "Co-evolution" was [[2602.12063|VLAW]]'s term for alternating between a separate world model and policy. Both our WAMs integrate them: Fast-WAM trains jointly via MoT; VLA-JEPA unifies V-JEPA2 and the action head. There's nothing to alternate. **"Self-evolving loop"** means: the model generates its own training data through targeted failure discovery ([[2511.00091|PLD]]), adapts on-the-fly ([[2602.20057|AdaWorldPolicy]]), and distills improvements back into itself. One model evolving itself — demonstrated on two architectures.

> [!question] Is this post-training research?
> Yes. Both WAMs are already pre-trained (by their respective authors). We use their released checkpoints and apply ==post-training== methods (LoRA fine-tuning, online adaptation, targeted data generation) to extend their capabilities to OOD scenarios. Same framing as [[2511.00091|PLD]], [[2602.20057|AdaWorldPolicy]], and [[2603.11653|VLA RL CL]].

---

## Summary: Five Design Principles

> [!tip] 1. Start from real, open-source WAMs
> Fast-WAM (640M ActionDiT + 5B Video DiT) and VLA-JEPA (V-JEPA2 + Qwen3-VL-2B) — both with published checkpoints. Not hypothetical architectures. Not World Models with bolted-on actions. ==Two real models you can download and evaluate today.==

> [!tip] 2. Extend to where they fail, not where they succeed
> Self-evolution doesn't improve ~97% → ~99% on standard LIBERO. It improves ==the unknown% on LIBERO-PRO, LIBERO-X, GM-100, and physics perturbations== for both WAMs. Establishing these failure cases is the first contribution.

> [!tip] 3. Use methods verified for both architectures
> [[2510.25889|πRL]] (Flow-SDE + RL) tested on pi0/pi0.5 flow-matching VLAs — both WAMs use flow matching. [[2511.00091|PLD]] tested on pi0 (flow matching). [[2509.19292|SOE]] VIB is architecture-agnostic MLPs. [[2412.02818|RoboMD]] is policy-agnostic. World model prediction error is our novel contribution (inspired by [[2602.20057|AdaWorldPolicy]], adapted for both Video DiT and V-JEPA2). ==Every method verified compatible with both WAMs or explicitly flagged as needing adaptation.==

> [!tip] 4. One integrated loop with external measurement
> Instead of three nested loops that interfere ([[01_Critique-Methodology-Self-Evolving-WAM#Part IV: Why the Three Loops Can't Be Nested|Part IV]]), use ==one self-evolving loop== (DIVERSIFY → DETECT → EXPLORE → PROBE → LEARN → DISTILL → DREAM → MEASURE). OOD benchmarks provide ==external ground truth== — no circular self-grading.

> [!tip] 5. If it fails, the failure is publishable
> If both WAMs drop to 40% on physics perturbations → that quantifies the robustness gap. If online LoRA doesn't help → that's a finding about the limits of test-time adaptation for flow matching. If self-evolution works on one WAM but not the other → that reveals which architectural choices enable adaptability. ==Every negative result informs the field.==

---

## Key Papers Referenced

### Base Models

| Paper | Role |
|-------|------|
| [[2603.16666\|Fast-WAM]] | Base WAM #1: MoT architecture (ActionDiT + Video DiT), joint flow matching, 97.6% LIBERO. Open-source ([GitHub](https://github.com/yuantianyuan01/FastWAM), [HuggingFace](https://huggingface.co/yuanty/fastwam)) |

| [[2602.10098\|VLA-JEPA]] | Base WAM #2: JEPA latent world model (V-JEPA2 ViT-L) + flow-matching action head + Qwen3-VL-2B. 97.2% LIBERO, ==79.5% LIBERO-Plus OOD==. Open-source ([GitHub](https://github.com/ginwind/VLA-JEPA), [HuggingFace](https://huggingface.co/ginwind/VLA-JEPA)) |

### Self-Evolution Methods — Core (6 methods)

| Paper | Role | What It Does |
|-------|------|-------------|
| [[2510.25889\|πRL]] | ==Action uncertainty + RL training== | Flow-SDE converts ODE to SDE for stochastic action sampling (note: SDE logic is integrated with RL loop in codebase — extraction needed for standalone use per [[2505.05470\|Flow-GRPO]] math). Provides RL mechanism for PLD specialists. 29-31% gains on pi0/pi0.5 |
| [[2509.19292\|SOE]] | ==Action active probing== | VIB MLPs + conditioning noise. Swap DDPM decoder for the action model's FM decoder. Finds behavioral boundaries. 50.8% improvement |
| World model prediction error (inspired by [[2602.20057\|AdaWorldPolicy]]) | ==Environment discovery== | World model predicts future → high error = surprise. ==Our novel use of each WAM's world model== (Fast-WAM: Video DiT pixel/VAE latent; VLA-JEPA: V-JEPA2 JEPA latent). |
| [[2412.02818|RoboMD]] | ==Environment active probing== | RL adversary searches for failure-inducing conditions. Policy-agnostic. 80.7% diagnosis accuracy |
| [[2511.00091\|PLD]] | ==Failure recovery== | Probe failures → residual RL specialists → distill back. 99% LIBERO. Tested on pi0 (flow matching) |
| [[2603.09030\|PlayWorld]] | ==Data collection== | Autonomous self-play rollouts including failures. 65% improvement. Architecture-agnostic |

### Self-Evolution Methods — Supporting Evidence (papers that validate our approach)

| Paper | What It Validates |
|-------|-------------------|
| [[2603.11653\|VLA RL Continual Learning]] | LoRA + GRPO achieves <2% forgetting on [[2410.24164\|π0]] (flow matching) — confirms our LoRA fine-tuning strategy works |
| [[2603.03818\|VLA Continual Learning]] | Only 2% replay buffer needed — confirms replay-only CL is sufficient |
| [[2504.18471\|AFM]] | Flow matching supports continual dynamics adaptation — confirms the training paradigm is compatible |
| [[2505.05470\|Flow-GRPO]] | ODE-to-SDE conversion enables stochastic exploration in flow matching — theoretical foundation for πRL |
| [[2505.22094\|ReinFlow]] | First online RL for flow matching robot control. Noise injection enables exploration in Franka Kitchen/RoboMimic |
| [[2603.04029\|Self-Adapting RL]] | World model prediction residuals detect OOD without human-specified change types — validates self-directed discovery |
| [[2510.09459\|FIPER]] | Runtime failure prediction via RND + action entropy — works with diffusion/flow matching, no failure data needed |

### OOD Evaluation Benchmarks

| Paper | What It Tests |
|-------|---------------|
| [[2510.03827\|LIBERO-PRO]] | 4 perturbation dimensions (object attributes, positions, language, environment). VLAs collapse from >90% to ==near 0%== |
| [[2602.06556\|LIBERO-X]] | 5 hierarchical difficulty levels, 600 tasks. VLAs: 39.4% at easiest level. Progressive spatial/object/instruction perturbations |
| [[2603.22078\|WAM vs VLA Robustness]] | LIBERO-Plus: 7 perturbation dimensions, 21 sub-dims. π0.5: 58.6% on perturbed RoboTwin |
| [[2603.28301\|LIBERO-Para]] | Paraphrase robustness: 22.8-51.9pp drops from semantically equivalent instructions |
| [[2601.11421\|GM-100]] | 100 detail-oriented tasks. Best VLA ([[2410.24164\|π0.5]]): 24.9%. The hard frontier |
| [[2505.03500\|TLI]] | 9% on novel spatial compositions. Structural limitation of static models |
| [[2306.03310\|LIBERO]] | Primary in-distribution benchmark: 130 tasks ([GitHub](https://github.com/Lifelong-Robot-Learning/LIBERO)) |
| [[2112.03227\|CALVIN]] | Long-horizon multi-step: 5-step chains. Best: 4.33 ([[2412.14803\|VPP]]) |

### Motivation (Why Self-Evolution)

| Paper | What It Shows |
|-------|---------------|
| [[2603.22078\|WAM vs VLA Robustness]] | Static models face speed-quality tradeoff; both fail under distribution shift |
| [[2511.16166\|EvoVLA]] | Self-evolution reduces stage hallucination by 23.7pp |
| [[2601.11421\|GM-100]] | Best VLA achieves only 24.9% on detail-oriented manipulation |
| [[2602.15922\|DreamZero]] | 39.5% on unseen tasks — even 14B models struggle OOD |

### Data & Simulation

| Paper | What We Use |
|-------|-------------|
| [[2603.16861\|MolmoBot]] | Procedural sim data (1.8M trajectories, MuJoCo). 79.2% real-world zero-shot |
| [[2403.12945\|DROID]] | Diversity > scale for generalization |
| [[2506.18088\|RoboTwin 2.0]] | 5-dimension domain randomization strategy |
| [[2405.05941\|SimplerEnv]] | Diagnostic benchmark, $r > 0.85$ sim-real correlation |

### Architecture Context

| Paper | Role |
|-------|------|
| [[2603.17240\|GigaWorld-Policy]] | Action-centered WAM design, curriculum training, 9x speedup. Validates the MoT pattern |
| [[2512.13030\|Motus]] | MoT with latent actions, tri-model joint attention. Validates the architecture class |
| [[2506.01844\|SmolVLA]] | Layer skipping, token reduction, async inference. Future compression reference |
| [[2601.16163\|Cosmos Policy]] | Fine-tuned foundation video model as WAM. 98.5% LIBERO, 93.6% real-world ALOHA |
| [[2410.24164\|π0]] | Flow-matching VLA from Physical Intelligence. LoRA + GRPO continual learning validated on this architecture |

### Critiques Informing This Design

| Document | Key Contribution |
|----------|-----------------|
| [[01_Critique-Self-Evolving-WAM]] | Domain transfer analysis: only 6 of ~15 papers on real manipulation. Critical miscitations |
| [[01_Critique-Methodology-Self-Evolving-WAM]] | Structural analysis: loops can't nest, CL fights self-evolution, no external ground truth |

---

*Revision of [[00_How-to-Build-Self-Evolving-WAM]]. Informed by [[01_Critique-Self-Evolving-WAM]] and [[01_Critique-Methodology-Self-Evolving-WAM]]. See also: [[06_Self-Evolving-VLA-WAM]] | [[04_WAM]] | [[03_VLA]]*
