---
title: Planning
date: 2026-04-23
tags:
  - project
  - planning
  - self-evolving
  - vla
  - wam
aliases:
  - Planning
---

# Planning

> [!info] Scope
> Self-improving WAM building blocks for robotics. Three literature sections below — prior self-evolving methods with code, co-evolving design references without code, unified WAM backbones as candidate substrates — followed by the proposal. Primary pilot backbones: [[2504.02792|UWM]] and [[2601.16163|Cosmos Policy]].

> [!tip] How blocks compose (code-available anchors only)
> Role buckets:
> - **Imagination substrate** (GRPO inside a WM): WMPO (frozen pixel-space video WM), VLA-RFT (learned video simulator)
> - **WM–policy co-evolution update rule**: WoVR (PACE — ⚠ not in code), VLAW (iterative alternation — ⚠ WM side only in code), GigaBrain (continual joint training with HILR)
> - **Label-free self-reward** (needs initial SFT demos): SRPO (V-JEPA-2 clustering), Self-Improving EFM (steps-to-go head), EvoVLA (stage-tracker intrinsic reward)
> - **Expert-anchored reward**: VAMPO (latent-consistency vs. expert future dynamics; unified VPM — mechanism reference, not a separate substrate)
> - **Hallucination gate**: WoVR (KIR + masked GRPO — ✓ shipped)
> - **Failure attribution (label-free, dual-channel)**: FIPER (RND-OE obs + ACE action; AND-logic in paper — per-channel re-routing loses the AND FPR guarantee, needs per-channel recalibration)
> - **Recovery-data mining**: SC-VLA (sparse imagination of tricky states), GigaBrain (HILR supplies corrective action labels — a gate can route data but cannot synthesize labels)
>
> **Stacking recipe**:
> 1. **Backbone** — imagination substrate (frozen WM, learned simulator, or a unified backbone; see Proposal).
> 2. **Reward** — label-free self-reward (SRPO clustering or EFM steps-to-go; both need SFT demos).
> 3. **Gate** — FIPER's two channels (per-channel recalibrated) for imag-side vs. policy-side routing.
> 4. **Update rule** — FIPER-gated dual loss **complements** (does not replace) PACE and HILR: the gate routes rollouts between `L_RL` and `L_img`; it does not schedule batch WM fine-tuning (PACE) or synthesize corrective action labels (HILR).
> 5. **Hard-case seeding** — SC-VLA-style sparse imagination for tricky states.

## Prior self-evolving methods (with code)

Composite score: loop closure (0.30), label-free-ness (0.20), gating quality (0.15), empirical evidence (0.15), novelty (0.10), embodied fit (0.05), code (0.05).

| Rank | Score | Paper | Repo | Model type | WM updated? | Policy updated? | Co-evolve? |
|---|---|---|---|---|---|---|---|
| 1 | 4.7 | [[2511.09515\|WMPO]] | [WM-PO/WMPO](https://github.com/WM-PO/WMPO) | VLA + pixel-space video WM (on-policy GRPO in imagination) | ≈ frozen during inner GRPO; fine-tuned in outer lifelong loop | ✓ GRPO | ≈ outer-loop (not headline) |
| 2 | 4.6 | [[2511.15605\|SRPO]] | [sii-research/siiRL](https://github.com/sii-research/siiRL) | VLA + frozen V-JEPA-2 latent WM (latent-cluster self-rewarding RL) | ✗ (V-JEPA-2 frozen — trajectory clustering only) | ✓ RL | NO |
| 3 | 4.5 | [[2509.15155\|Self-Improving EFM]] | [self-improving-efms](https://github.com/self-improving-efms/self-improving-efms.github.io/blob/main/pointmass_notebook.ipynb) | EFM (steps-to-go → dense reward + success detector; pointmass ref impl) | ≈ (no explicit WM — steps-to-go head inside unified EFM) | ✓ | Ambiguous — unified end-to-end update |
| 4 | 4.4 | [[2602.13977\|WoVR]] | [RLinf/RLinf](https://github.com/RLinf/RLinf) — ⚠ **partial**: KIR + masked GRPO shipped; **PACE not shipped** (reimplement from paper §4.3) | VLA + video-diffusion WM (masked GRPO + KIR + PACE) | ✓ PACE periodically refines WM from evolving policy | ✓ masked GRPO + KIR | **YES — explicit co-evolution** (paper) |
| 5 | 4.3 | [[2510.00406\|VLA-RFT]] | [OpenHelix-Team/VLA-RFT](https://github.com/OpenHelix-Team/VLA-RFT) | VLA + learned video world simulator (GRPO with verified rewards) | ✗ (WM trained offline — frozen as simulator during RFT) | ✓ GRPO | NO |
| 6 | 4.2 | [[2603.19370\|VAMPO]] | [OpenHelix-Team/VAMPO](https://github.com/OpenHelix-Team/VAMPO) | Video Prediction Model (GRPO over denoising-as-MDP; latent-consistency reward) | ≈ unified VPM is the policy | ✓ GRPO over denoising | Ambiguous — unified VPM |
| 7 | 4.2 | [[2510.09459\|FIPER]] | [utiasDSL/fiper](https://github.com/utiasDSL/fiper) (MIT) | Failure predictor — RND-OE obs + ACE action + conformal threshold (AND) | N/A (detector only) | N/A (detector only) | NO — gate; attribution signal |
| 8 | 4.1 | [[2602.12063\|VLAW]] | [Robert-gyj/Ctrl-World](https://github.com/Robert-gyj/Ctrl-World) (MIT) — ⚠ **partial**: WM post-training shipped; **VLM reward filter + VLA post-training NOT shipped** | VLA + action-conditioned WM (iterative: rollouts fine-tune WM → VLM-filtered WM rollouts post-train VLA) | ✓ fine-tuned on rollouts incl. failures (FVD 225 → 64) | ✓ post-trained on VLM-filtered synthetic rollouts | **YES — iterative alternation** (paper) |
| 9 | 4.0 | [[2511.16166\|EvoVLA]] | [AIGeeksGroup/EvoVLA](https://github.com/AIGeeksGroup/EvoVLA) | VLA (stage tracker + intrinsic reward) | ✗ (stage tracker only) | ✓ | NO |
| 10 | 3.9 | [[2602.21633\|SC-VLA]] | [Kisaragi0/SC-VLA](https://github.com/Kisaragi0/SC-VLA) | VLA (sparse world imagination → intrinsic reward → residual RL) | ✗ (SPI imagination pre-trained) | ✓ residual RL | NO |
| 11 | 3.8 | [[2602.12099\|GigaBrain-0.5M*]] | [open-gigaai/giga-brain-0](https://github.com/open-gigaai/giga-brain-0) (Apache-2.0) | VLA + WM continual joint training with HILR (Stage-4 SFT corrective labels) | ✓ continually fine-tuned on HILR-augmented rollouts | ✓ joint VLA training | **YES — via HILR** (humans supply labels; gate cannot synthesize) |

## Co-evolving WAM references (project-site only)

| Score | Paper | Code status | Co-evol mechanism |
|---|---|---|---|
| 4.3 | [[2602.06508\|World-VLA-Loop]] | [project site](https://showlab.github.io/World-VLA-Loop/) only | Closed-loop state-aware video WM + VLA with jointly-trained reward head; SANS (Success + Near-Success) dataset |
| 3.6 | [[2604.01985\|WAV]] | [project site](https://world-action-verifier.github.io/) only | Verification-guided: subgoal generator (action-free) + sparse IDM flag WM failures → collect action-labeled rollouts |
| 3.4 | [[2510.26433\|CoLA-World]] | arxiv-only | Warm-up freezes pre-trained OpenSora WM to train Latent Action Model (LAM), then unfreeze and co-evolve LAM + WM |

## Unified WAM backbones (candidate substrates)

Seven code-available **World Action Models** in which the action-inference path and the future-state prediction path share transformer weights (not parallel expert stacks, not adapter fusion). Ordered by scale.

| # | Paper | Paradigm | Backbone | Scale | Imagination output | Action output | Head symmetry |
|---|---|---|---|---|---|---|---|
| 1 | [[2504.02792\|UWM]] | Diffusion (rectified flow) | Shared DiT + independent diffusion timesteps $t_a, t_{o'}$ | ~0.2B | Single-Linear image patch decoder | 2-layer action MLP (Linear→Mish→Linear) | Near-symmetric — both thin vs. DiT body; action slightly deeper |
| 2 | [[2412.15109\|Seer]] | Hybrid (causal LM + latent diffusion) | Shared GPT-2, unidirectional attention lets action tokens read past + future | ~300M | 2-block image decoder on `obs_tokens` | Thin action MLP on `action_pred_token` | Near-symmetric — both thin; image slightly deeper |
| 3 | [[2501.18867\|UP-VLA]] | Hybrid (LM + continuous action head) | Show-o (Phi-1.5 LM + CLIP ViT) with resized vocab for image tokens | ~1.5B | CE on image-token positions via shared LM head | Single MAP block + Linear on last-layer hidden states | **Asymmetric** — image via AR tokens; action via regression |
| 4 | [[2601.16163\|Cosmos Policy]] | Latent video diffusion | Cosmos-Predict2 single video denoiser | 2B | Same denoiser — future frames as latent frames | Same denoiser — actions as latent frames | **Fully symmetric** — zero separation |
| 5 | [[2506.21539\|WorldVLA]] | Autoregressive (discrete) | Chameleon-based AR; three separate tokenizers (image/text/action) share a single vocabulary | Chameleon-scale (size unstated) | AR next-token on image tokens via shared LM head | AR next-token on action tokens via shared LM head | Fully symmetric — single LM head |
| 6 | [[2506.19850\|UniVLA]] | Autoregressive (discrete) | Single Emu3 AR transformer; all modalities as discrete tokens | 8.5B | AR next-token on VQ image tokens via shared LM head | AR next-token on FAST action tokens via shared LM head | Fully symmetric — single LM head |
| 7 | [[2602.15922\|DreamZero]] | Diffusion (flow-matching, **shared** denoising timestep for video + action) | Autoregressive DiT backbone (pretrained video model) + minimal add-on state/action encoders and video/action decoders; single end-to-end joint objective | 14B | Video decoder on shared DiT | Action decoder on shared DiT | Near-symmetric — both are minimal decoder add-ons on shared DiT |

**Paradigm groups**:
- **Diffusion (continuous latents)** — UWM, Cosmos Policy, DreamZero → VAMPO-style GRPO-over-denoising applies directly
- **Autoregressive (discrete tokens)** — UniVLA, WorldVLA → GRPO adapts to sequence-level categorical policy-gradient
- **Hybrid (LM body + asymmetric heads)** — Seer, UP-VLA → mixed approach; requires per-head routing care

**Decision axes for the pilot**:
- **Head symmetry**: higher symmetry → cleaner gradient flow for `L_RL` and `L_img`; Cosmos Policy + UniVLA + WorldVLA are fully symmetric
- **Scale vs. iteration cost**: UWM (~0.2B) and Seer (~300M) are fastest to iterate on; DreamZero (14B) has the strongest zero-shot prior but highest compute overhead
- **Imagination explicitness**: UWM, Cosmos Policy, Seer, UniVLA, DreamZero paper-demonstrate long-horizon generation; WorldVLA and UP-VLA inherit imagination from their backbone (Chameleon / Show-o) without explicit long-horizon demos

**Rejected** (structurally similar-sounding but failing the unified-weights test): Fast-WAM (MoT: parallel action expert), Genie Envisioner (parallel action transformer stack), JEPA-VLA (adapter fusion), Dita / HybridVLA / Magma (unified body but no future-state prediction — policy-only).

## Proposal: Gated dual-loss self-evolution

### 1. Core claim

Unified-backbone WAMs — [[2601.16163|Cosmos Policy]] and [[2504.02792|UWM]] — can self-evolve from a single interaction stream via a **FIPER-gated dual loss**:

$$
L_{\text{total}} = \alpha \cdot L_{\text{RL}}^{\text{ACE-gated}} + \beta \cdot L_{\text{img}}^{\text{RND-OE-gated}}
$$

- `L_RL` = advantage × action likelihood, with advantage from an [[2509.15155|EFM]]-style steps-to-go self-reward head (bootstrapped from SFT demos, label-free post-SFT); gated by [[2510.09459|FIPER]]'s ACE.
- `L_img` = video diffusion loss on collected rollouts, gated by FIPER's RND-OE (only update imagination on in-distribution futures).
- Both terms backprop to shared backbone weights θ → co-evolution is architectural, not orchestrated.

The shared backbone receives mixed gradient; FIPER's two channels certify *which* rollouts are credible evidence for *which* head.

**Framing advantage**: we orchestrate *which loss term a given rollout contributes to*, not *which module to update* (as WoVR/VLAW/GigaBrain do). Same outcome, simpler architecture.

### 2. Backbone-specific plans

| Backbone | Pure RL suffices? | Needs `L_img`? | What to ablate |
|---|---|---|---|
| [[2601.16163\|Cosmos Policy]] | ✓ (single denoiser → automatic imag-policy *alignment*) | Optional — sharpens imagination *fidelity* (pure RL only guarantees alignment, may degrade FVD) | α-only vs. α+β; imagination FVD before/after on a held-out benchmark decoupled from task reward |
| [[2504.02792\|UWM]] | ✗ — only final image-projection head is cut off under action-only loss; DiT body still receives gradient via shared self-attention (see §2b) | **Required** for sharp image decoding | per-head gradient-norm ratio; λ=0 vs. λ>0 image-decoder FVD; per-head frozen-weight ablation |

#### 2a. Cosmos Policy — detailed plan

Cosmos Policy is a single denoiser handling all modalities (proprio, actions, value, multi-view images as latent frames) — no separate action/image heads.

Surface-form: looks like VLA-style RL applied to the denoiser. Because the denoiser is single, imagination parameters get updated as a side effect of the RL gradient.

```
RL task-success reward
        │
        ▼  GRPO advantage × ∇log π_θ(a | o)
        ▼
Gradient flows through single Cosmos denoiser θ
        │
  ┌─────┴─────┐
  ▼           ▼
action       imagination
pathway      pathway
(direct)     (indirect — same θ, update direction chosen for actions)
```

Two flavors of "imagination improvement":

| Flavor | Under RL-only | What it needs |
|---|---|---|
| **Imag-policy alignment** (WM's predicted future matches current policy distribution) | ✓ Free — same weights; this is what PACE pays compute for in modular backbones | Nothing extra |
| **Imag fidelity** (video prediction matches physical reality — low FVD/SSIM) | ✗ Not guaranteed — RL may even degrade fidelity as task-relevant features crowd out realism | `L_img` term (video diffusion loss on in-distribution rollouts) |

**FIPER as routing signal** (not just filter): RND-OE high → veto rollout's contribution to `L_img`; ACE high → veto contribution to `L_RL`; either channel can silence a rollout on its side. Reward head is added as a latent-frame modality in the Cosmos denoiser.

**Caveat**: single-denoiser ablation is hard — reviewers will ask *"how do you know fidelity improved rather than just alignment?"* Defend by holding `L_img` out in one run and measuring FVD/SSIM on an imagination benchmark decoupled from task reward.

#### 2b. UWM — detailed plan

[[2504.02792|UWM]] is a shared DiT backbone with two separate denoising heads:

- **Shared**: image input embedding, action encoder, transformer body, final AdaLN head
- **Split only at the last projection**: action-denoising output vs. image-patch-denoising output

Under an action-only loss, only the final image-projection head is cut off from gradient. The DiT body, final AdaLN head, and image input embedding all receive gradient via shared self-attention. Observable symptom of pure RL: asymmetric per-head gradient norms and progressively drifting image-reconstruction fidelity as the action-side update direction dominates.

Same loss form as Cosmos (§1); `L_img` restores gradient to the image projection and rebalances the shared-backbone update direction.

**Per-head routing** (more natural than Cosmos because the heads are structurally distinct): `L_RL` gradient path = shared DiT → action head; `L_img` gradient path = shared DiT → image-patch head; FIPER's RND-OE gates image-loss rollouts, ACE gates RL-loss rollouts (per-channel recalibration required — see §1). Per-head frozen-weight ablations are feasible.

> [!tip] Thesis advantage
> UWM is **more ablatable than Cosmos Policy**: per-head gradient-norm ratios, per-head frozen-weight ablations, and a direct FVD measurement on the image decoder are all tractable. Sharp falsifiable hypothesis: *"pure VLA-RL induces asymmetric per-head gradient norms and image-fidelity drift; gated `L_img` restores balance"* — architecture-grounded, not overstated.

**Practical note**: if the archived code from the previous iteration targets UWM, UWM is the lower-activation-energy path for the pilot. Cosmos Policy can follow as second-backbone validation.

### 3. Building-block integration

Which prior-method anchors compose into the proposal, and how.

#### Core stack (minimum to make either backbone self-evolve)

| Anchor | Role | UWM | Cosmos Policy |
|---|---|---|---|
| [[2509.15155\|Self-Improving EFM]] | Label-free reward for `L_RL` (steps-to-go head, SFT-bootstrapped) | add as third head on shared DiT | add as latent-frame modality in the denoiser |
| [[2510.09459\|FIPER]] | The gate — RND-OE routes `L_img`, ACE routes `L_RL` (per-channel recalibration required) | ✓ direct | ✓ direct |
| [[2511.09515\|WMPO]] | GRPO-in-imagination compute-graph infrastructure for `L_RL` | ✓ | ✓ |
| [[2603.19370\|VAMPO]] | GRPO-over-denoising-as-MDP mechanism | ✓ applied to action head | ✓ applied to unified denoiser |

#### Optional complements (stack for robustness)

| Anchor | Role | UWM | Cosmos Policy |
|---|---|---|---|
| [[2602.13977\|WoVR]] KIR + masked GRPO | Hallucination gate at the imagination level (keyframe-init + spurious-reward masking); complements FIPER | ✓ shipped | ✓ shipped |
| [[2602.21633\|SC-VLA]] | Sparse-imagination hard-case data mining | ✓ | ✓ |
| [[2511.15605\|SRPO]] | Alternative / fallback label-free reward (latent-cluster) — swap with EFM steps-to-go | ✓ | ✓ |
| [[2510.00406\|VLA-RFT]] | Verified-reward trajectory-comparison as an alt reward source | mechanism only | mechanism only |
| [[2511.16166\|EvoVLA]] | Stage-tracker intrinsic reward as auxiliary signal | auxiliary | auxiliary |

#### Not needed on unified backbones (redundant or orthogonal)

| Anchor | Why |
|---|---|
| [[2602.13977\|WoVR]] PACE | Batch WM fine-tune; unified backbones already co-evolve for free via shared weights. Cite as baseline only. |
| [[2602.12063\|VLAW]] | Alternation (policy→WM→policy) collapses into single-shot joint updates on a shared backbone. Cite as blueprint. |
| [[2602.12099\|GigaBrain-0.5M*]] | HILR supplies corrective action labels (supervision); unified-backbone co-evolution is architectural. Gate cannot synthesize labels — HILR is orthogonal. |
| [[2602.06508\|World-VLA-Loop]] / [[2604.01985\|WAV]] / [[2510.26433\|CoLA-World]] | Alternative gating / co-evolution mechanisms (design references, no code). |
