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
> **Sim-based self-evolving WAM via PS-uGRPO (Physics-Spatial unified GRPO).** A pretrained unified WAM self-discovers failures via [[2510.09459|FIPER]] (proactive) and self-corrects via a **single unified GRPO loop on the joint (action, imagination) log-prob**, driven by a task + physics + spatial reward (Eq. 4). Policy and world-model co-evolve under one RL signal through the shared backbone θ. MSE (with variable-length prefix AR) and LPIPS serve as dense anchors. No task-specific demonstrations required. Primary pilot backbones: [[2504.02792|UWM]] and [[2601.16163|Cosmos Policy]].

## Literature

### Prior self-evolving methods

Score weights: loop 0.30, label-free 0.20, gating 0.15, empirical 0.15, novelty 0.10, fit 0.05, code 0.05.

#### With public code

| Rank | Score | Paper | Repo | Model type | WM updated? | Policy updated? | Co-evolve? |
|---|---|---|---|---|---|---|---|
| 1 | 4.7 | [[2511.09515\|WMPO]] | [WM-PO/WMPO](https://github.com/WM-PO/WMPO) | VLA + pixel-space video WM (on-policy GRPO in imagination) | ≈ frozen during inner GRPO; fine-tuned in outer lifelong loop | ✓ GRPO | ≈ outer-loop (not headline) |
| 2 | 4.6 | [[2511.15605\|SRPO]] | [sii-research/siiRL](https://github.com/sii-research/siiRL) | VLA + frozen V-JEPA-2 latent WM (latent-cluster self-rewarding RL) | ✗ (V-JEPA-2 frozen — trajectory clustering only) | ✓ RL | NO |
| 3 | 4.5 | [[2509.15155\|Self-Improving EFM]] | [self-improving-efms](https://github.com/self-improving-efms/self-improving-efms.github.io/blob/main/pointmass_notebook.ipynb) | EFM (steps-to-go → dense reward + success detector; pointmass ref impl) | ≈ (no explicit WM — steps-to-go head inside unified EFM) | ✓ | Ambiguous — unified end-to-end update |
| 4 | 4.4 | [[2602.13977\|WoVR]] | [RLinf/RLinf](https://github.com/RLinf/RLinf) — ⚠ **partial**: KIR + masked GRPO shipped; **PACE not shipped** | VLA + video-diffusion WM (masked GRPO + KIR + PACE) | ✓ PACE periodically refines WM | ✓ masked GRPO + KIR | **YES — explicit co-evolution** (paper) |
| 5 | 4.3 | [[2510.00406\|VLA-RFT]] | [OpenHelix-Team/VLA-RFT](https://github.com/OpenHelix-Team/VLA-RFT) | VLA + learned video world simulator (GRPO with verified rewards) | ✗ (WM trained offline — frozen during RFT) | ✓ GRPO | NO |
| 6 | 4.3 | [[2602.11075\|RISE]] | [OpenDriveLab/RISE](https://github.com/OpenDriveLab/RISE) | Compositional WM: Dynamics + Progress Value Model; online RL in imagination. **PVM stacked in our `r^task` (Eq. 5)** | ✗ (WM + PVM frozen during loop) | ✓ online RL on imagined rollouts | NO — WM frozen during loop |
| 7 | 4.2 | [[2603.19370\|VAMPO]] | [OpenHelix-Team/VAMPO](https://github.com/OpenHelix-Team/VAMPO) | Video Prediction Model (GRPO over denoising-as-MDP; latent-consistency reward) | ≈ unified VPM is the policy | ✓ GRPO over denoising | Ambiguous — unified VPM |
| 8 | 4.2 | [[2510.09459\|FIPER]] | [utiasDSL/fiper](https://github.com/utiasDSL/fiper) (MIT) | Failure predictor — RND-OE obs + ACE action + conformal threshold (AND). **Stacked: per-channel OR-union in Eq. 1/2** | N/A (detector only) | N/A (detector only) | NO — gate; attribution signal |
| 9 | 4.1 | [[2602.12063\|VLAW]] | [Robert-gyj/Ctrl-World](https://github.com/Robert-gyj/Ctrl-World) (MIT) — ⚠ **partial**: WM post-training shipped; VLM reward filter + VLA post-training NOT shipped | VLA + action-conditioned WM (iterative: rollouts fine-tune WM → VLM-filtered WM rollouts post-train VLA) | ✓ (FVD 225 → 64) | ✓ | **YES — iterative alternation** (paper) |
| 10 | 4.0 | [[2511.16166\|EvoVLA]] | [AIGeeksGroup/EvoVLA](https://github.com/AIGeeksGroup/EvoVLA) | VLA (stage tracker + intrinsic reward). **Stage-bonus concept stacked in `r^task`** | ✗ | ✓ | NO |
| 11 | 3.9 | [[2602.21633\|SC-VLA]] | [Kisaragi0/SC-VLA](https://github.com/Kisaragi0/SC-VLA) | VLA with SPI (aux progress-prediction heads) + OAR (online residual RL via reshaped reward) | ✗ (no separate WM) | ✓ residual RL | NO |
| 12 | 3.8 | [[2602.12099\|GigaBrain-0.5M*]] | [open-gigaai/giga-brain-0](https://github.com/open-gigaai/giga-brain-0) (Apache-2.0) | VLA + WM continual joint training with HIL rollouts | ✓ continually fine-tuned on HIL rollouts | ✓ joint VLA training | **YES — via HIL rollouts** |
| 13 | 3.5 | [[2511.07732\|ViPRA]] | [sroutray/vipra](https://github.com/sroutray/vipra) (Apache-2.0, ICLR 2026) | 3-stage pretraining + adaptation: actionless-video latent actions → VLM pretraining → flow-matching adaptation | ✓ VLM pretrained jointly on video + latent actions | ✓ flow-matching decoder fine-tuned | NO — pretrain-then-adapt |

#### Project-site only (design references)

| Score | Paper | Code status | Co-evol mechanism |
|---|---|---|---|
| 4.3 | [[2602.06508\|World-VLA-Loop]] | [project site](https://showlab.github.io/World-VLA-Loop/) only | Closed-loop video WM + VLA with jointly-trained reward head; SANS dataset |
| 3.6 | [[2604.01985\|WAV]] | [project site](https://world-action-verifier.github.io/) only | Verification-guided: subgoal generator + sparse IDM flag WM failures → collect action-labeled rollouts |
| 3.4 | [[2510.26433\|CoLA-World]] | arxiv-only | Warm-up freezes OpenSora WM to train Latent Action Model, then unfreeze and co-evolve |

### Unified WAM backbones

Seven code-available **World Action Models** whose action and future-state paths share transformer weights (no parallel expert stacks, no adapter fusion). Ordered by scale.

**Pilot backbones** (full detail):

| # | Paper | Paradigm | Backbone | Scale | Imagination output | Action output | Head symmetry |
|---|---|---|---|---|---|---|---|
| 1 | [[2504.02792\|UWM]] | Diffusion (DDPM + DDIM) | Shared DiT + independent diffusion timesteps $t_a, t_{o'}$ | ~0.2B | Single-Linear image patch decoder | Symmetric encoder/decoder: 2-Linear + Mish MLP | Near-symmetric |
| 2 | [[2601.16163\|Cosmos Policy]] | Latent video diffusion | Cosmos-Predict2 single video denoiser | 2B | Future frames as latent frames | Actions as latent frames | **Fully symmetric** |

**Additional candidates** (same unified-weights criterion, deferred to second-backbone validation or future work):

| Paper | Paradigm | Scale | Symmetry |
|---|---|---|---|
| [[2412.15109\|Seer]] (GPT-2 + ViT-MAE, predictive inverse dynamics) | Hybrid | ~316M total | Asymmetric |
| [[2501.18867\|UP-VLA]] (Show-o: Phi-1.5 + CLIP ViT) | Hybrid | ~1.5B | Asymmetric |
| [[2506.21539\|WorldVLA]] (Chameleon-init AR, shared image/text/action vocab) | AR (discrete) | 7B / 34B | Fully symmetric |
| [[2506.19850\|UniVLA]] (Emu3 AR transformer) | AR (discrete) | 8.5B | Fully symmetric |
| [[2602.15922\|DreamZero]] (AR-DiT video + action chunks) | Flow-matching | 14B | Near-symmetric |

**Paradigm groups**:

| Paradigm | Backbones | RL mechanism |
|---|---|---|
| Diffusion | UWM, Cosmos Policy, DreamZero | Flow-GRPO directly applies |
| AR (discrete) | UniVLA, WorldVLA | GRPO → sequence-level categorical policy-gradient |
| Hybrid | Seer, UP-VLA | Per-head routing care required |

**Decision axes**:
- **Head symmetry**: Cosmos / UniVLA / WorldVLA fully symmetric.
- **Scale vs. iteration cost**: UWM 0.2B and Seer 300M fastest; DreamZero 14B has strongest zero-shot prior.
- **Imagination explicitness**: UWM / Cosmos / Seer / UniVLA / DreamZero paper-demonstrate long-horizon generation; WorldVLA / UP-VLA inherit imagination from backbone.

**Rejected** (fail the unified-weights test): Fast-WAM (MoT), Genie Envisioner (parallel action transformer), JEPA-VLA (adapter fusion), Dita / HybridVLA / Magma (unified body but no future-state prediction — policy-only).

## Proposal: Sim-based self-evolving WAM

### Core loop

Given a pretrained unified-backbone WAM ([[2601.16163|Cosmos Policy]] or [[2504.02792|UWM]]) and a simulator with next-state + success ground truth, the backbone's policy and world-model **co-evolve through a single GRPO loop** (PS-uGRPO, Eq. 11) whose reward combines task, physics, and spatial signals. Three dense anchors — MSE with prefix-AR (Eq. 12), LPIPS (Eq. 13), DreamDojo TC (Eq. 14) — supply the per-pixel and per-velocity gradient that scalar RL cannot.

**Attribution** — per-channel FIPER + sim: per-step WM-error `‖ŵ_{t+1} − o^sim_{t+1}‖² > τ_δ` (RND-OE channel) defines the WM-attributed set `M_img`; trajectory `r_i = 0` with ACE-flagged policy uncertainty (ACE channel) defines `F_pol`. The step-indexed update set `U = F_pol ∪ proj(M_img)` focuses the RL gradient on attributed failures only; successes are left alone.

**Unified gradient** — PS-uGRPO's single negative advantage on `U` pushes θ away from (bad action, bad imagination) pairs; anchor losses apply on `M_img` regardless. Both heads update in one optimizer step through shared θ — architectural co-evolution via the unified RL signal, not two separate losses.

**Multi-round iteration** — each round, attribution tracks the current failure frontier; θ updates on confirmed mistakes. Periodic FIPER thresholds, PVM, and IDM recalibration on fresh successes (§Algorithm step 10).

**Deployment portability (policy + FIPER only, not the WM)** — the *policy* and *FIPER* transfer to real-robot deployment; FIPER uses only model-internal state, providing a runtime safety layer without sim ground truth. The **WM does not transfer**: its rewards (`r^phys`, `r^spatial`) and anchors (MSE, LPIPS) all reference sim, so it learns sim physics. WM-as-deployment-imagination requires a separate real-corpus fine-tune — see §Sim-to-Real Gap.

> [!warning] Cold-start protocol
>
> **Not circular — standard conformal bootstrap.** Round 0 runs all $K$ rollouts through pure sim verification (no FIPER); the resulting success set calibrates thresholds $\tau_{\text{ACE}}, \tau_{\text{RND}}$. Rounds N ≥ 1 continue calling sim; FIPER adds a parallel attribution channel, not a sim substitute. **Backbone precondition**: ≥ 5–10% Round-0 zero-shot success (scope limit, not rescue); $\tau_{\text{ACE}}, \tau_{\text{RND}}$ and PVM refit every `RECAL` rounds on the sliding success window (§Algorithm step 10).
>
> **Pre-Round-0 one-time calibration** (reused across rounds; re-fit only on substantial distribution shift):
> - **IDM** ([[2603.17808|EVA]]): trained on sim-rollout `(o_t, o_{t+1}) → a_t` pairs until held-out validation accuracy ≥ 80%; supplement with random-action rollouts for coverage.
> - **PVM** ([[2602.11075|RISE]]): fit on sim's successful rollouts to predict normalized progress-toward-goal.
> - **VLM discriminator** ([[2603.23376|ABot-PhysWorld]]) + **LPIPS Alex-lin** (frozen AlexNet + learned linear calibration): both loaded pretrained, plug-and-play.
>
> **Self-evolving compatibility**: IDM and PVM train on sim rollouts + sim's success oracle — same dependency tier as the simulator itself. We avoid demo-trained reward models, human preferences, and annotated stage labels that would defeat the claim.
>
> **Known caveats**: (i) PVM cold-start needs ≥ 5–10% backbone zero-shot success; (ii) IDM needs random-action rollouts to cover action space; (iii) optional IDM refit on `RECAL` cadence if policy drifts materially.

### Mechanism synthesis

Eleven mechanisms stack into PS-uGRPO + three anchors (Eq. 15, derived in §Mathematics); six related mechanisms are considered and rejected or reserved for deployment.

**Stacked (11)** — each contributes a specific term of Eq. 15:

| Paper | Contribution (what we take) | Target term | What we skip |
|---|---|---|---|
| [[2511.09515\|WMPO]] | GRPO-in-imagination compute graph; K joint rollouts per batch | PS-uGRPO scaffolding (Eq. 11) | Outer lifelong WM fine-tune |
| [[2505.05470\|Flow-GRPO]] | ODE→SDE conversion (both heads); denoising reduction | $\log \pi_\theta$, $\log u_\theta$ (Eq. 10) | Image-gen benchmarks |
| [[2510.09459\|FIPER]] | RND-OE + ACE dual-channel conformal gate | `F_pol`, `M_img` → `𝒰` (Eq. 11) | AND-rule (→ per-channel OR) |
| [[2602.13977\|WoVR]] | KIR keyframe-init rollouts | `M_img` segmentation (Eq. 2) | PACE (shared-θ subsumes) |
| [[2602.11075\|RISE]] | PVM for dense task reward | `V_ψ` in `r^task` (Eq. 5) | Demo warm-up |
| [[2511.16166\|EvoVLA]] | Stage-aligned intrinsic bonus | `λ_stage · r^stage` (Eq. 5) | Gemini hard negatives (→ sim subgoals) |
| [[2603.17808\|EVA]] | Smoothness + out-of-bound penalty on IDM-extracted actions (gripper-kinematic axis of `r^phys`) | `ρ_smooth · S_IDM` + `ρ_bound · 𝟙[a ∉ 𝒜_embod]` in `r^phys` (Eq. 6) | Separate post-training stage (merged into PS-uGRPO) |
| [[2603.23376\|ABot-PhysWorld]] | Decoupled VLM discriminator's plausibility score — used verbatim (weights, scoring interface); object-state axis of `r^phys` | `ρ_VLM · D_phys(ô_t, ô_t+1)` in `r^phys` (Eq. 6) | Diffusion-DPO pair-construction (we consume scalar score as GRPO reward) |
| [[2602.06949\|DreamDojo]] | Velocity-change TC loss (DreamDojo's Eq. 4), over $K_{\text{lat}}$ latent frames per video chunk | `β_TC · L^TC` (Eq. 14). Active on video-chunk backbones ($K_{\text{lat}} \geq 4$); inactive on UWM ($K_{\text{lat}} = 1$) | Relative-action conditioning + chunked injection (backbone-provided) |
| [[2602.00743\|SA-VLA]] | Phase-conditioned signed geometric reward (Reach/Place/Leave) | `η_geo · Δ_geo(phase)` in `r^spatial` (Eq. 7) | SCAN annealed-noise (Flow-GRPO's SDE subsumes) |
| [[2511.07403\|SpatialThinker]] | CIoU bbox-alignment reward | `η_CIoU · CIoU(bbox)` in `r^spatial` | STVQA-7K dataset (sim bboxes replace) |
| [[2603.25685\|Persistent Robot WMs]] | Variable-length-prefix AR training (F4 mitigation) | `L_img^flow-prefix` (Eq. 12) — essential dense anchor | Reward-contrasted denoising (PS-uGRPO subsumes with richer reward) |
| [[1801.03924\|LPIPS]] | Perceptual anchor (partial F5 mitigation) | `γ · L_img^LPIPS` (Eq. 13) | Extensive backbone fine-tuning (paper warns against; Alex-lin frozen) |

**Alternatives / deployment-only (6)** — noted for completeness, not in the stack. Each row has a distinct reason for exclusion (not just "alt reward"):

| Paper | Role | Why not stacked |
|---|---|---|
| [[2602.21633\|SC-VLA]] | Sparse World Imagination = auxiliary progress-prediction heads + reward reshaping | Not an initial-state sampler (paper's SPI = *Sparse Predictive Imagination*, not *Sparse-imagination Preferential*); progress-prediction role is redundant with RISE's PVM |
| [[2511.07732\|ViPRA]] | Pretraining choice (pre-Round-0 backbone) | Not in the loop; flow-matching decoder adaptation is superseded by Flow-GRPO |
| [[2511.15605\|SRPO]] | Deployment-fallback reward (V-JEPA-2 latent-cluster) | Sim oracle is direct during training; SRPO only fills in when sim is unavailable |
| [[2510.00406\|VLA-RFT]] | GRPO with pixel+LPIPS verified reward inside a **frozen** WM simulator | **Role mismatch**: VLA-RFT freezes the WM and RLs the policy inside it; we co-train the WM via PS-uGRPO. Also **LPIPS role mismatch**: they use it as a reward; we use it as a dense anchor loss (Eq. 13) |
| [[2603.19370\|VAMPO]] | Denoising-as-MDP with latent-consistency reward | **Mechanism supersession**: VAMPO's denoising-step MDP is subsumed by our Flow-GRPO ODE→SDE at the environment level; composing both would double-wrap RL (MDP-within-MDP) |
| [[2603.27866\|Wan-R1]] | GRPO with endpoint / temporal-order / structural-consistency rewards | **Reward subsumption**: all three map onto our Eq. 4 decomposition (`Δ_geo`, `D_TC`, CIoU); our physics+spatial is strictly richer (adds EVA IDM + ABot-PhysWorld VLM) and manipulation-native |

**Stacking order**: PS-uGRPO core (Eq. 11: WMPO + Flow-GRPO + FIPER + WoVR KIR) → compose `r^uni` (Eq. 4: task + physics + spatial) → add three anchors (Eqs. 12, 13, 14). Component credit in §Baselines ablations.

> [!note] WMPO-specific inheritance
> We adopt WMPO's compute-graph skeleton (K rollouts → group-relative advantage → GRPO update) but replace four pieces:
>
> | WMPO | Ours |
> |---|---|
> | Imagined rollouts from a frozen WM | Sim rollouts (ground truth) — sim-supervised but WM is *co-trained* inside PS-uGRPO |
> | Rollout-trained reward model (success/failure only) | Unified reward `r^uni` = task + physics + spatial (Eq. 4) |
> | Policy-only GRPO; WM frozen | PS-uGRPO (Eq. 11) over joint (action, imagination) log-prob; both heads update via the same advantage |
> | Periodic WM fine-tune in an outer loop | Per-step MSE + LPIPS + TC anchors (Eqs. 12, 13, 14) co-updating the WM head inside the same optimizer step |

### Mathematics

**TL;DR**: $L_{\text{total}}(\theta) = L_{\text{PS-uGRPO}} + \beta_{\text{MSE}} \cdot L^{\text{flow-prefix}} + \gamma \cdot L^{\text{LPIPS}} + \beta_{\text{TC}} \cdot L^{\text{TC}}$. One unified GRPO on the joint action+imagination log-prob under a task + EVA physics + spatial reward; three dense anchors (MSE with variable-length prefix AR, LPIPS, DreamDojo temporal-consistency) prevent high-dim decoder collapse. Both heads co-evolve under a **single** RL signal through shared θ. Equations 1–11 follow; symbol glossary in §Notation at the end of this subsection.

**Failure sets** — policy-attributed trajectories (Eq. 1) and WM-attributed per-step mispredictions (Eq. 2):

$$
F_{\text{pol}} = \{\, i \,:\, \mathrm{ACE}(\tau_i) > \tau_{\text{ACE}} \wedge r_i = 0 \,\} \tag{1}
$$

$$
M_{\text{img}} = \{\, (i, j, t) \,:\, o_{i, j H_{\text{kir}}} \text{ keyframe},\ t \in [j H_{\text{kir}}, (j+1) H_{\text{kir}}),\ \mathrm{RND\text{-}OE}(o_{i,t}) > \tau_{\text{RND}} \wedge \|\hat{w}_{i,t+1} - o_{i,t+1}^{\text{sim}}\|^2 > \tau_\delta \,\} \tag{2}
$$

The step-indexed update set mixes trajectory-level and step-level attributions cleanly via a **per-channel OR-union**:

$$
\mathcal{U} = \{(i, t) : i \in F_{\text{pol}},\, t \in \{0, \ldots, T-1\}\} \;\cup\; \{(i, t) : \exists j,\, (i, j, t) \in M_{\text{img}}\} \tag{3}
$$

Policy-attributed trajectories contribute all their steps; WM-attributed failures contribute only the specific mis-prediction step. We use OR (not FIPER's official AND) — AND detects but cannot separate cause; precision is regained via per-channel sim-verification inside each set. FIPER's reference code natively supports both operations and per-channel thresholds (`operation={"and","or"}`, independent `quantile1`/`quantile2`); §Baselines ablation quantifies the tradeoff.

**Unified reward** — task + physics + spatial (Eq. 4):

$$
r^{\text{uni}}_{i,t} \;=\; w_T \cdot r^{\text{task}}_{i,t} \;+\; w_P \cdot r^{\text{phys}}_{i,t} \;+\; w_S \cdot r^{\text{spatial}}_{i,t} \tag{4}
$$

Each component defined below, used directly from its source paper.

*Task component* ([[2602.11075|RISE]] PVM + [[2511.16166|EvoVLA]] stage bonus):

$$
r^{\text{task}}_{i,t} = V_\psi(o_{i,t}, \text{goal}) + \lambda_{\text{stage}} \cdot r^{\text{stage}}_{i,t} \tag{5}
$$

**RISE PVM term**: $V_\psi$ trained on sim successes to predict progress-toward-goal (0 → 1). Dense per-step signal. **EvoVLA stage-bonus term**: $r^{\text{stage}}_{i,t}$ from sim's per-subgoal oracle (grasp → transport → release); $\lambda_{\text{stage}} \ge 0$ weights the bonus. EvoVLA's Gemini-hard-negative SAR training is bypassed — sim oracle replaces it.

*Physics component* — [[2603.17808|EVA]] (gripper-kinematics) + [[2603.23376|ABot-PhysWorld]] (object-state):

$$
r^{\text{phys}}_{i,t} \;=\; -\rho_{\text{smooth}} \cdot S_{\text{IDM}}\bigl(\hat{o}_{i, t-1:t+2}\bigr) \;-\; \rho_{\text{bound}} \cdot \mathbb{1}\bigl[\hat{a}^{\text{IDM}}_{i,t} \notin \mathcal{A}_{\text{embod}}\bigr] \;+\; \rho_{\text{VLM}} \cdot D_{\text{phys}}\bigl(\hat{o}_{i,t}, \hat{o}_{i,t+1}\bigr) \tag{6}
$$

**EVA terms**: $\hat{a}^{\text{IDM}}_{i,t} = \mathrm{IDM}(\hat{o}_{i,t}, \hat{o}_{i,t+1})$; $S_{\text{IDM}} = \|v\|_2 + \|\mathrm{acc}\|_2 + \|\mathrm{jerk}\|_2$ on finite differences of $\hat{a}^{\text{IDM}}$; $\mathcal{A}_{\text{embod}}$ is the robot's feasible action set. Catches gripper-kinematic failures (chatter, out-of-bound velocities). **ABot-PhysWorld term**: $D_{\text{phys}} \in [0, 1]$ is the discriminator's sigmoid plausibility score (higher = better). Catches object-state failures EVA misses (penetration, anti-gravity, object-permanence, rigidity). Discriminator used verbatim — we consume its scalar as a GRPO reward instead of a DPO preference signal (algorithm-level choice; reward model unchanged). Manipulation-native (3M real-robot clips; PBench Domain Score **0.9306**).

DreamDojo's temporal consistency is a **loss**, not a reward — see Eq. 14.

*Spatial component* — [[2602.00743|SA-VLA]] (phase-geometric) + [[2511.07403|SpatialThinker]] (CIoU):

$$
r^{\text{spatial}}_{i,t} = \eta_{\text{geo}} \cdot \Delta_{\text{geo}}\bigl(\text{phase}_t\bigr) + \eta_{\text{CIoU}} \cdot \mathrm{CIoU}\bigl(\mathrm{bbox}(\hat{o}_{i,t+1}),\, \mathrm{bbox}(o^{\text{sim}}_{i,t+1})\bigr) \tag{7}
$$

**SA-VLA phase-geometric term**: $\Delta_{\text{geo}}$ = signed geometric-distance change per phase — **Reach**: ↓ gripper→object; **Place**: ↓ object→target; **Leave**: ↑ gripper retreat. Normalized distances $\in [0, 1]$ (SA-VLA Eqs. 7–8). **SpatialThinker CIoU term**: $\mathrm{CIoU} \in [0, 1]$ via $(\mathrm{CIoU}_{\text{raw}} + 1)/2$ normalization, on object bboxes (imagined vs. sim next-frame).

**Group-relative advantage** on unified reward — Eq. 8:

$$
\mu_t = \tfrac{1}{K}\textstyle\sum_i r^{\text{uni}}_{i,t}, \quad \sigma_t = \sqrt{\tfrac{1}{K}\textstyle\sum_i (r^{\text{uni}}_{i,t} - \mu_t)^2}, \quad A^{\text{uni}}_{i,t} = \frac{r^{\text{uni}}_{i,t} - \mu_t}{\sigma_t + \epsilon_{\text{num}}} \tag{8}
$$

**Flow-GRPO SDE** — [[2505.05470|Flow-GRPO]] ODE→SDE conversion applies to *both* heads (Eq. 9). Action head via $v_\theta$; WM head via $u_\theta$ (same form with substituted variables):

$$
da_s = \bigl[ v_\theta(a_s;\, o_{i,t}, c) + \tfrac{\sigma_{\text{flow}}^2(s)}{2} \nabla_{a_s} \log p_s(a_s) \bigr] ds + \sigma_{\text{flow}}(s)\, dW_s \tag{9}
$$

Denoising reduction: $S_{\text{train}}=10 \ll S_{\text{infer}}=40$ (Flow-GRPO's SD3.5-M settings) gives ~4× rollout speedup at no inference-quality cost.

**Joint log-prob factorization** — Eq. 10. On a unified backbone (UWM, Cosmos Policy), policy actions and imagined next-observations are conditionally independent given $(o_{i,t}, a_{i,t}, c)$, so the joint log-prob decomposes:

$$
\log \pi_\theta^{\text{joint}}(a_{i,t},\, \hat{o}_{i,t+1} \mid o_{i,t}, c) = \log \pi_\theta(a_{i,t} \mid o_{i,t}, c) + \log u_\theta(\hat{o}_{i,t+1} \mid o_{i,t}, a_{i,t}, c) \tag{10}
$$

Both summands computed via Flow-GRPO ODE→SDE (Eq. 9) on their respective heads. For AR-token backbones ([[2506.19850|UniVLA]], [[2506.21539|WorldVLA]]), replace the WM-head flow log-prob with the AR-token log-prob $\sum_k \log p_\theta(z^{(k)}_{i,t+1} \mid \cdots)$ from Eq. 12 below — the joint factorization still holds.

**PS-uGRPO — unified Physics-Spatial GRPO loss** (Eq. 11):

$$
L_{\text{PS-uGRPO}}(\theta) = -\frac{1}{|\mathcal{U}|} \sum_{(i,t) \in \mathcal{U}} A^{\text{uni}}_{i,t} \cdot \log \pi_\theta^{\text{joint}}\bigl(a_{i,t},\, \hat{o}_{i,t+1} \mid o_{i,t}, c\bigr) \tag{11}
$$

One loss, one advantage, one joint log-prob — both heads updated by a single RL signal.

**MSE anchor with variable-length prefix AR** — F4 mitigation (Eq. 12, flow-matching):

$$
L_{\text{img}}^{\text{flow-prefix}}(\theta) = \mathbb{E}_{k \sim \mathcal{U}[0, K_{\max}]} \, \frac{1}{|M_{\text{img}}|} \sum_{(i,j,t) \in M_{\text{img}}} \mathbb{E}_{s, \varepsilon} \bigl[\, \|u_\theta(x_s;\, \tilde{o}_{i,t-k:t}, a_{i,t}, s) - v^\ast(o^{\text{sim}}_{i,t+1})\|^2 \,\bigr] \tag{12}
$$

$\tilde{o}_{i,t-k:t}$ = WAM's free-rolled obs sequence (ground-truth at $k=0$, fully imagined at $k=K_{\max}$); interpolates teacher-forced and free-rollout, eliminating exposure bias. AR-backbone analog: token CE with VQ targets $z_{i,t+1} = \mathrm{VQ}(o^{\text{sim}}_{i,t+1})$.

**LPIPS perceptual anchor** — F5 partial mitigation (Eq. 13):

$$
L_{\text{img}}^{\text{LPIPS}}(\theta) = \frac{1}{|M_{\text{img}}|} \sum_{(i,j,t) \in M_{\text{img}}} \mathrm{LPIPS}\bigl(\mathrm{Dec}(\hat{x}^{\text{clean}}_{i,t+1}),\, o^{\text{sim}}_{i,t+1}\bigr) \tag{13}
$$

**Decode**: LPIPS needs an RGB image. Flow-matching: single-Euler-step at $s \approx 0.9$, $\hat{x}^{\text{clean}} = x_s + (1-s) u_\theta$, then frozen-VAE decode $\mathrm{Dec}(\cdot)$ — approach used by [[2510.00406|VLA-RFT]] and [[2601.20218|DenseGRPO]]. AR backbones ([[2506.19850|UniVLA]], [[2506.21539|WorldVLA]]): decode $\mathrm{Dec}(\arg\max_k p_\theta)$ with straight-through estimator, standard in Emu3. LPIPS backbone is frozen Alex-lin.

**DreamDojo temporal-consistency anchor** — F4+F5 support (Eq. 14), [[2602.06949|DreamDojo]] Eq. (4) over $K_{\text{lat}}$ latent frames **within** a single video-chunk generation:

$$
L^{\text{TC}}(\theta) = \frac{1}{|M_{\text{img}}|} \sum_{(i,j,t) \in M_{\text{img}}} \mathbb{E}\Bigl[\sum_{k=1}^{K_{\text{lat}}-1} \bigl\|(z^{(k+1)}_{i,t} - z^{(k)}_{i,t}) - (v^{\ast(k+1)}_{i,t} - v^{\ast(k)}_{i,t})\bigr\|^2\Bigr] \tag{14}
$$

$z^{(k)}_{i,t} = u_\theta(x^{(k)}_{i,t}, k, c)$ = predicted velocity for the $k$-th latent frame; $v^{\ast(k)}_{i,t}$ = ground-truth velocity (sim frames through backbone's VAE + finite-difference); $K_{\text{lat}}$ = backbone-specific latent-frame count per generation. $\beta_{\text{TC}} = 0.1$ (DreamDojo's λ).

**Backbone applicability**: active on video-chunk backbones ([[2601.16163|Cosmos Policy]] Wan2.1 4:1 compression $K_{\text{lat}} \geq 4$; [[2602.15922|DreamZero]] video chunks); inactive on [[2504.02792|UWM]] ($K_{\text{lat}} = 1$, inner sum empty) — set $\beta_{\text{TC}} = 0$ on UWM pilot.

**Full objective** — unified RL + three dense anchors (Eq. 15):

$$
L_{\text{total}}(\theta) = L_{\text{PS-uGRPO}}(\theta) + \beta_{\text{MSE}} \cdot L_{\text{img}}^{\text{flow-prefix}}(\theta) + \gamma \cdot L_{\text{img}}^{\text{LPIPS}}(\theta) + \beta_{\text{TC}} \cdot L^{\text{TC}}(\theta) \tag{15}
$$

The PS-uGRPO term is the dominant training signal; the three anchors provide dense gradient RL advantage cannot. Defaults: $\beta_{\text{MSE}} = \gamma = \beta_{\text{TC}} = 0.1$.

#### WAM failure modes — mapping to Eq. 15 terms

Eq. 15's four terms jointly close all five failure modes of the current WAM's imagination:

| Mode | Closed by |
|---|---|
| **F1** Action-conditioning misalignment | MSE anchor (Eq. 12, `k=0`) + physics IDM term (Eq. 6) |
| **F2** Observation OOD | MSE anchor (Eq. 12) on OOD sim observations |
| **F3** Unseen dynamics | Physics reward (Eq. 6) + MSE anchor |
| **F4** Compounding / teacher-forcing trap | Prefix-AR in Eq. 12 (random `k ∈ [0, K_max]`) + DreamDojo TC anchor (Eq. 14) |
| **F5** Modal collapse | PS-uGRPO spatial + physics rewards (Eq. 11) + LPIPS anchor (Eq. 13) + TC anchor (Eq. 14) |

The unified GRPO does the task / physics / spatial work; the three anchors (MSE, LPIPS, TC) keep the high-dimensional decoder trainable. Dimensionality argument: scalar RL advantage is ~$\mathcal{O}(1)$ bits/sample; the WM image head outputs ~$\mathcal{O}(10^5)$ scalars/sample — RL alone is ~$10^5\times$ more information-sparse than per-pixel supervision, so anchor weights $> 0$ prevent decoder collapse (C4 tests this).

**Notation** — grouped by role. Every symbol appearing in Eqs. 1–15 is defined here exactly once.

*Parameters and functions*:
- $\theta$ — shared backbone parameters (body + heads via LoRA / full-FT split per §LoRA).
- $\pi_\theta(a \mid o, c)$ — policy (action head).
- $v_\theta(a_s;\, o, c)$ — action-head flow-matching velocity predictor (drives Eq. 9 SDE).
- $u_\theta(x_s;\, o, a, s)$ — image/video-head flow-matching velocity predictor (WM; Eq. 11).
- $p_\theta(z \mid \cdot)$ — AR-head next-token probability (Eq. 12; UniVLA / WorldVLA backbones).
- $f_\theta(o, a)$ — WM single-step prediction: $\hat{w}_{i,t+1} = f_\theta(o_{i,t}, a_{i,t})$.
- $V_\psi(o, \text{goal})$ — [[2602.11075|RISE]] Progress Value Model (parameters $\psi$ separate from $\theta$; trained on sim successes).

*Rollouts and sim oracle*:
- Rollout index $i \in \{1, \ldots, K\}$; $K$ = per-batch group size.
- Horizon $T$; rollout $\tau_i = (o_{i,0}, a_{i,0}, \ldots, o_{i,T})$.
- Environment step $t \in \{0, \ldots, T-1\}$ (distinct from flow time $s$ below).
- Initial states: $o_{i,0} \sim p_0^{\text{sim}}$ (uniform over the simulator's reset distribution).
- Sim oracle outputs: $r_i \in \{0,1\}$ (trajectory success) and per-step $o^{\text{sim}}_{i,t+1}$.
- $c$ — language task instruction (shared across a rollout's steps).
- $\text{goal}$ — goal spec input to $V_\psi$; derived from $c$.

*FIPER scores / thresholds*:
- $\mathrm{ACE}(\tau_i)$ — action-chunk entropy; $\mathrm{RND\text{-}OE}(o_{i,t})$ — observation OOD.
- $\tau_{\text{ACE}}, \tau_{\text{RND}}$ — conformal thresholds (calibrated per §Cold-start protocol).
- $\tau_\delta$ — L2 threshold for WM mismatch $\|\hat{w}_{i,t+1} - o^{\text{sim}}_{i,t+1}\|^2 > \tau_\delta$.

*WoVR KIR segmentation*:
- $H_{\text{kir}} \ll T$ — keyframe segment length.
- Segment $j$ spans $[j H_{\text{kir}}, (j+1)H_{\text{kir}})$; $o_{i, j H_{\text{kir}}}$ is its keyframe by construction (no separate keyframe set — observations at multiples of $H_{\text{kir}}$ are the keyframes).

*Unified reward components* (Eqs. 4–7):
- $r^{\text{uni}}_{i,t}$ — unified per-step reward driving PS-uGRPO.
- $r^{\text{task}}_{i,t} = V_\psi(o_{i,t}, \text{goal}) + \lambda_{\text{stage}} r^{\text{stage}}_{i,t}$ — task component (RISE PVM + EvoVLA stage bonus).
- $r^{\text{stage}}_{i,t}$ — stage-bonus reward from sim's per-subgoal signal; $\lambda_{\text{stage}} \ge 0$ — stage-bonus weight.
- $r^{\text{phys}}_{i,t}$ — physics component: IDM action-consistency + temporal-consistency penalty.
- $r^{\text{spatial}}_{i,t}$ — spatial component: phase-conditioned geometric reward + CIoU bbox alignment.
- $w_T, w_P, w_S \ge 0$ — top-level reward weights (task, physics, spatial); defaults $w_T = 1.0$, $w_P = w_S = 0.3$.

*Physics reward internals* (two-axis: EVA gripper-kinematic + ABot-PhysWorld object-state):
- $\mathrm{IDM}(\cdot, \cdot)$ — pretrained inverse dynamics model mapping two adjacent frames to the inferred action ([[2603.17808|EVA]]'s IDM, retrained on sim-rollout data).
- $\hat{a}^{\text{IDM}}_{i,t} = \mathrm{IDM}(\hat{o}_{i,t}, \hat{o}_{i,t+1})$ — IDM-extracted action from WAM-generated adjacent frames.
- $S_{\text{IDM}}(\cdot) = \|v\|_2 + \|\mathrm{acc}\|_2 + \|\mathrm{jerk}\|_2$ — smoothness penalty; derivatives are finite differences of $\hat{a}^{\text{IDM}}$ across the 3-frame window.
- $\mathcal{A}_{\text{embod}}$ — robot's feasible action set (joint velocity / acceleration bounds).
- $D_{\text{phys}}(\cdot, \cdot) \in [0, 1]$ — [[2603.23376|ABot-PhysWorld]]'s decoupled VLM discriminator applied to an adjacent-frame pair; sigmoid output, higher = more physically plausible. Discriminator used verbatim; only the downstream consumer changes (their DPO → our GRPO reward).
- $\rho_{\text{smooth}}, \rho_{\text{bound}}, \rho_{\text{VLM}}$ — physics sub-weights; defaults $\rho_{\text{smooth}} = \rho_{\text{bound}} = 1.0$, $\rho_{\text{VLM}} = 0.5$ (VLM reward is higher-variance — conservative default).

*Spatial reward internals*:
- $\text{phase}_t \in \{\text{Reach}, \text{Place}, \text{Leave}\}$ — manipulation phase at step $t$ (from sim's subgoal oracle).
- $\Delta_{\text{geo}}(\text{phase}_t)$ — signed geometric-distance change for the current phase (Reach: shrinking gripper→object; Place: shrinking object→target; Leave: growing retreat distance).
- $\mathrm{bbox}(\cdot)$ — object bounding-box extractor; applied to both the WAM-imagined next-frame $\hat{o}_{i,t+1}$ and the sim ground-truth $o^{\text{sim}}_{i,t+1}$.
- $\mathrm{CIoU}(\cdot, \cdot) \in [0, 1]$ — Complete IoU (Zheng et al. 2020) for bbox alignment, mapped to $[0,1]$ as $(\mathrm{CIoU}_{\text{raw}} + 1) / 2$ (SpatialThinker's reference normalization).
- $\eta_{\text{geo}}, \eta_{\text{CIoU}}$ — spatial sub-weights; defaults $\eta_{\text{geo}} = 1.0$, $\eta_{\text{CIoU}} = 0.5$.

*GRPO statistics* (Eq. 8):
- $\mu_t, \sigma_t$ — per-timestep mean and std of $r^{\text{uni}}_{\cdot, t}$ over the $K$ rollouts.
- $A^{\text{uni}}_{i,t}$ — per-timestep unified advantage.
- $\epsilon_{\text{num}}$ — small constant for denominator numerical stability.
- $\mathcal{U}$ — step-indexed update set (attribution-routed failure focus, Eq. 3): policy-attributed trajectories contribute all their steps, WM-attributed failures contribute only the specific mis-prediction step.

*Flow-matching SDE variables* (Eqs. 9, 10, 12):
- $s \in [0,1]$ — flow time (distinct from environment step $t$).
- $a_s, x_s$ — interpolant samples at flow time $s$; $x_s = s \cdot o^{\text{sim}}_{i,t+1} + (1-s)\varepsilon$.
- $\varepsilon \sim \mathcal{N}(0, I)$ — flow-matching noise (distinct from $\epsilon_{\text{num}}$).
- $\sigma_{\text{flow}}(s)$ — SDE diffusion coefficient (distinct from GRPO's $\sigma_t$).
- $p_s(a_s)$ — marginal density of $a_s$ under the flow.
- $dW_s$ — Wiener increment.
- $v^\ast$ — ground-truth flow velocity target; for the interpolant above, $v^\ast(o^{\text{sim}}_{i,t+1}) = o^{\text{sim}}_{i,t+1} - \varepsilon$.
- $\pi_\theta^{\text{joint}}$ — joint action + imagined-next-observation log-prob; factorizes per Eq. 10.

*AR-token variables* (AR-backbone analog of Eq. 12):
- $z_{i,t+1} = \mathrm{VQ}(o^{\text{sim}}_{i,t+1})$ — VQ-tokenized next observation.
- $\mathrm{VQ}(\cdot)$ — vector-quantizer encoder (backbone-specific).
- $k$ — token index within $z_{i,t+1}$.

*Anchor losses* (Eqs. 12, 13, 14):
- $K_{\max}$ — maximum rollout prefix length for F4 mitigation; default $K_{\max} = 4$ ([[2603.25685|Persistent Robot WMs]] training-schedule).
- $\tilde{o}_{i,t-k:t}$ — WAM's free-rolled observation sequence of length $k$ (ground-truth at $k=0$, pure WAM-imagined at $k=K_{\max}$).
- $\mathrm{LPIPS}(\cdot, \cdot)$ — learned perceptual image patch similarity (Alex-lin backbone frozen).
- $\hat{x}^{\text{clean}}_{i,t+1} = x_s + (1-s) \cdot u_\theta(x_s; o_{i,t}, a_{i,t}, s)$ evaluated at $s \approx 0.9$ — single-Euler-step clean prediction from the flow-matching head (flow-matching backbones only). For AR backbones, $\mathrm{Dec}(\arg\max p_\theta)$ with straight-through estimator.
- $\mathrm{Dec}(\cdot)$ — backbone's frozen pixel decoder (VAE for flow-matching; VQ-GAN for AR).
- $z^{(k)}_{i,t} = u_\theta(x^{(k)}_{i,t}, k, c)$ — predicted velocity for the $k$-th latent frame within the WM's video-chunk generation at env-step $t$ (DreamDojo notation).
- $v^{\ast(k)}_{i,t}$ — ground-truth velocity for the $k$-th latent frame: encode sim's rollout frames `[o^sim_t, o^sim_{t+1}, …]` through the backbone's frozen VAE at its temporal compression ratio, then take finite-differences across the resulting latent sequence.
- $K_{\text{lat}}$ — WM's per-generation latent-frame count; backbone-specific ([[2601.16163|Cosmos Policy]] $K_{\text{lat}} \geq 4$ via Wan2.1's 4:1 compression; [[2602.15922|DreamZero]] multi-frame; [[2504.02792|UWM]] $K_{\text{lat}}=1$ → TC inactive). Disambiguated from batch-size $K$.

*Loss weights* (Eq. 15):
- $\beta_{\text{MSE}} \ge 0$ — MSE anchor weight; default $0.1$.
- $\gamma \ge 0$ — LPIPS anchor weight; default $0.1$.
- $\beta_{\text{TC}} \ge 0$ — DreamDojo TC anchor weight; default $0.1$ (matches DreamDojo's $\lambda$).

### Algorithm

```python
# Round N: PS-uGRPO — unified Physics-Spatial GRPO + MSE/LPIPS anchors.
# One RL loop on joint (action, imagination) log-prob; anchor losses prevent decoder collapse.

# 1. Joint rollout — policy generates actions, WM generates imagined next-frames, sim steps.
#    Each rollout yields both real (a, o_sim) and imagined (a, o_hat) trajectories.
rollouts = [joint_rollout_in_sim(θ, T=T) for _ in range(K)]   # returns (a, o_sim, o_hat) per step

# 2. FIPER proactive flagging (model-internal).
ace_score = [ACE(τ) for τ in rollouts]
rnd_score = [[RND_OE(o_sim[i,t]) for t in range(T)] for i in range(K)]

# 3. Attribution: F_pol (policy-caused failure) ∪ M_img (WM-caused step failure).
F_pol = {i for i in range(K) if ace_score[i] > τ_ACE and env_success(rollouts[i]) == 0}

M_img = set()
for i in range(K):
    for j in range(T // H_kir):                                # KIR segmentation
        for t in range(j * H_kir, (j+1) * H_kir):
            if rnd_score[i][t] > τ_RND and \
               ||o_hat[i,t+1] - o_sim[i, t+1]||**2 > τ_δ:
                M_img.add((i, j, t))

U = {(i, t) for i in F_pol for t in range(T)} \
    | {(i, t) for (i, _, t) in M_img}                          # step-indexed update set

# 4. Unified reward (Eq. 4).
for i in range(K):
    for t in range(T):
        r_task[i,t] = PVM_ψ(o_sim[i,t], goal) + λ_stage * stage_tracker(o_sim[i,t])
        a_idm       = IDM(o_hat[i,t], o_hat[i,t+1])
        r_phys[i,t] = (- ρ_smooth * smoothness_penalty(a_idm_window)
                       - ρ_bound  * int(a_idm not in A_embod)
                       + ρ_VLM    * D_phys(o_hat[i,t], o_hat[i,t+1]))
        r_spat[i,t] = (  η_geo  * signed_geo_delta(phase[i,t], o_sim[i,t:t+2], a[i,t])
                       + η_CIoU * CIoU(bbox(o_hat[i,t+1]), bbox(o_sim[i,t+1])))
        r_uni[i,t]  = w_T * r_task[i,t] + w_P * r_phys[i,t] + w_S * r_spat[i,t]

# 5. Group-relative advantage (Eq. 8).
μ_t, σ_t = per-timestep statistics of r_uni over K
A_uni[i,t] = (r_uni[i,t] - μ_t) / (σ_t + ε_num)

# 6. PS-uGRPO — single RL loss on joint log-prob (Eq. 11).
L_PS_uGRPO = 0.0
for (i, t) in U:
    log_pi_joint = (  flow_grpo_log_prob(π_θ, a[i,t]       | o_sim[i,t],        c)
                    + flow_grpo_log_prob(u_θ, o_hat[i,t+1] | o_sim[i,t], a[i,t], c))
    L_PS_uGRPO  -= A_uni[i,t] * log_pi_joint
L_PS_uGRPO /= max(len(U), 1)

# 7. MSE anchor with variable-length prefix AR (Eq. 12).
L_img_MSE = 0.0
for (i, j, t) in M_img:
    k = uniform_int(0, K_max)
    obs_context = o_sim[i,t] if k == 0 else θ.wm_rollout(o_sim[i,t-k], a[i,t-k:t])
    L_img_MSE += flow_matching_loss(θ.wm_predict(obs_context, a[i,t]), o_sim[i,t+1])
L_img_MSE /= max(len(M_img), 1)

# 8. LPIPS anchor (Eq. 13).
L_img_LPIPS = mean(LPIPS(o_hat[i,t+1], o_sim[i,t+1]) for (i, _, t) in M_img)

# 9. DreamDojo TC anchor (Eq. 14). Inactive on single-frame backbones (K_lat = 1).
L_TC = 0.0
if K_lat > 1:
    for (i, _, t) in M_img:
        for k in range(1, K_lat):
            z_k, z_km1 = u_θ(x_k_t, k, c), u_θ(x_km1_t, k-1, c)
            v_k, v_km1 = v_star_k_t,        v_star_km1_t
            L_TC += ||(z_k - z_km1) - (v_k - v_km1)||**2
    L_TC /= max(len(M_img) * (K_lat - 1), 1)

# 10. Full objective (Eq. 15).
L_total = L_PS_uGRPO + β_MSE * L_img_MSE + γ * L_img_LPIPS + β_TC * L_TC
L_total.backward()
optimizer.step()

# 11. Periodic recalibration on sliding success window.
if round_n % RECAL == 0:
    recent_successes = [τ for τ in rollouts if env_success(τ) == 1]
    FIPER.refit_thresholds(recent_successes)   # τ_ACE, τ_RND
    PVM_ψ.fit(recent_successes)                # RISE value model
    IDM.fit_if_needed(recent_successes)        # inverse-dynamics model for physics reward
```

**Variant A** (full-`K` GRPO, not failure-focused): replace `U = F_pol ∪ M_img-proj` with $\mathcal{U} = \{1,\ldots,K\} \times \{0,\ldots,T-1\}$. Tests whether attribution-routed update outperforms standard GRPO at matched gradient steps.

**Hyperparameter defaults**:
- Reward weights: `w_T = 1.0`, `w_P = w_S = 0.3`; physics sub-weights `ρ_smooth = ρ_bound = 1.0` (EVA), `ρ_VLM = 0.5` (ABot-PhysWorld); spatial sub-weights `η_geo = 1.0`, `η_CIoU = 0.5`.
- Anchor weights: `β_MSE = γ = β_TC = 0.1` (RL dominates; three anchors provide dense gradient only).
- LoRA `r = 32, α_lora = 64`; LR `1e-4` (LoRA) / `1e-5` to `5e-6` (heads).
- Rollout: `K = 16–32` per batch; `H_kir ≈ T/8`; `K_max = 4` (prefix-AR depth); `S_train = 10, S_infer = 40`.
- **FIPER thresholds — aggressive per-channel OR-union**: `τ_ACE, τ_RND` set at the **60th conformal percentile** (vs. FIPER's original 95th), favoring recall for broad self-discovery. Combined with the OR-union `𝒰` (§Mathematics) and sim-verification false-alarm filter, this maximizes failure coverage at sim-compute cost.

### Baselines

Four external baselines + one asymmetric internal baseline, each isolating one design choice. All run on the same LIBERO suite + same unified backbone (UWM) for apples-to-apples; PLD additionally runs with its published backbone to anchor against its own 99% LIBERO number.

| Baseline | What it has | What it isolates (tests our design choice) | Repo |
|---|---|---|---|
| **[[2511.00091\|PLD]]** (no-WM residual RL) | Frozen VLA base + lightweight residual RL specialists + SFT distillation; **99% LIBERO** | Does the WM (and hence physics+spatial rewards computed from imagined frames) buy anything over no-WM residual RL? Tests C3 | [PLD project page](https://wenlixiao.com/self-improve-VLA-PLD) (code not yet released as of 2026-04) |
| **[[2511.09515\|WMPO]]-in-sim** (WMPO's compute graph with sim rollouts) | Policy-only GRPO; no `r^phys`, no `r^spatial`, no WM anchor losses | Does unified (policy + WM) GRPO with physics+spatial rewards beat policy-only GRPO at matched compute? Tests C1a, C1b | [WM-PO/WMPO](https://github.com/WM-PO/WMPO) |
| **[[2602.13977\|WoVR]]** (OpenVLA-OFT backbone) | Masked GRPO + KIR + PACE co-evolution; **69.2% LIBERO** | Does PS-uGRPO (single unified update) beat WoVR's three-stage orchestration at matched compute? | [RLinf/RLinf](https://github.com/RLinf/RLinf) |
| **[[2509.09674\|SimpleVLA-RL]]** (full-FT, no WM, no FIPER) | OpenVLA-OFT 7B full fine-tune with verified sim reward; single-task | Does LoRA + unified backbone beat full-FT single-task RL at matched task count? Tests LoRA-on-body efficacy | [PRIME-RL/SimpleVLA-RL](https://github.com/PRIME-RL/SimpleVLA-RL) |
| **Asymmetric RL+supervised** (internal ablation; policy-only Flow-GRPO + supervised MSE on WM; `w_P = w_S = 0`) | Tests C1a: does unified RL on both heads (+ physics+spatial rewards) beat the asymmetric split at matched compute? | (self — Eq. 11 degraded) |

**Primary vs. ours**: PLD is the reviewer's default skeptical question for C3; the **asymmetric internal baseline** is the reviewer's default question for C1. Both are gated — see §Novelty for the failure-mode pivots.

**Ablations within PS-uGRPO** — credit attribution across Eq. 15's components:

| Ablation | Tests |
|---|---|
| **Reward-term dropouts** — `w_T=0`, `w_P=0`, `w_S=0`, EVA-only (`ρ_VLM=0`), VLM-only (`ρ_smooth=ρ_bound=0`), no-PVM, `λ_stage=0`, random-init IDM (8 runs) | C1c — each component's contribution to `r^uni`. Expected: `w_P=0` drops ≥3pp on contact-rich; `w_S=0` drops ≥3pp on spatial-perturbed; `w_T=0` collapses entirely; EVA-only catches kinematic failures but misses object-state; VLM-only catches object-state but misses chatter; random-IDM ≈ no-gain vs. `w_P=0` |
| **Sparse-reward ablation** — replace all per-step dense rewards with terminal-only task success (`r^uni_{i,t} = r_i · 𝟙[t=T-1]`) | Quantifies dense-reward contribution to the paper's headline claim (C1). Expected: ≥ 10pp drop on LIBERO-Long (aligns with [[2601.20218|DenseGRPO]] + [[2603.27866|Wan-R1]] findings on sparse-vs-dense for flow-matching RL) |
| **Attribution-routing variants** — FIPER AND-combined; sim-only attribution (no FIPER); Variant A (`U = full K × T`); **conservative thresholds (95th conformal percentile, FIPER's original default)** vs. our aggressive 60th-percentile setting | C2 — per-channel OR-union vs. AND, FIPER vs. sim-only, attribution-focus vs. full-GRPO, broad self-discovery vs. high-precision detection. Conservative-threshold run tests whether aggressive self-discovery hurts or helps |
| **Anchor dropouts** — `β_MSE=0`, `γ=0`, `β_TC=0`, `K_max=0` (4 runs) | C4 + F4/F5 — per-head decoder collapse under RL-only (`β_MSE=0`); perceptual anchor effect (`γ=0`); DreamDojo TC necessity (`β_TC=0`); prefix-AR necessity (`K_max=0`) |

### Novelty

Four contributions, each a falsifiable claim against a named prior-work target. The per-channel OR-union attribution, failure-focused update set `𝒰`, anchor losses, and shared-backbone co-evolution are *consequences* of the unified-GRPO formulation, not independent contributions.

| Contribution | Falsifiable claim | Prior-work target |
|---|---|---|
| **C1 — PS-uGRPO: unified physics-and-spatial-aware GRPO on policy + world-model** (Eq. 11, with joint log-prob Eq. 10 and unified reward Eq. 4) | **C1a**: at matched compute on LIBERO, PS-uGRPO beats asymmetric (RL-on-policy + supervised-on-WM) by ≥ 5 pp on LIBERO-Long (physics reward drives long-horizon stability). **C1b**: on spatial-perturbed LIBERO, PS-uGRPO beats asymmetric by ≥ 5 pp (spatial reward drives geometric robustness). **C1c**: removing either `r^phys` (Eq. 6) or `r^spatial` (Eq. 7) degrades the respective axis by ≥ 3 pp — verifies component-level credit attribution | No prior work runs unified GRPO on both heads of a unified WAM backbone. [[2511.09515\|WMPO]]: RL on policy only. [[2603.17808\|EVA]]: RL on WM only (kinematic, no spatial). [[2602.00743\|SA-VLA]]: spatial rewards but supervised-only L_img. [[2511.07403\|SpatialThinker]]: GRPO with spatial rewards on MLLMs, not VLAs |
| **C2 — Per-channel OR-union attribution routing** — RND-OE → WM-caused failure, ACE → policy-caused failure; union forms attribution set `𝒰` (Eq. 11) | **C2a**: per-channel OR-union has higher attribution precision than FIPER's AND-combined detector. **C2b**: FIPER-enabled beats FIPER-disabled (sim-only attribution) by ≥ 3 pp on attribution precision or downstream success. If C2b fails, FIPER is dropped and `𝒰` becomes sim-only — still valid but weaker | [[2510.09459\|FIPER]] paper recommends AND for detection; reference code supports both AND and OR (`operation` flag) + per-channel thresholds — we pick OR + aggressive thresholds for attribution + broad self-discovery. No prior work validates this configuration for cause attribution |
| **C3 — PS-uGRPO beats no-WM residual RL on sample efficiency / OOD transfer** | **C3a**: on LIBERO, our method reaches 90% with ≤ 50% of [[2511.00091\|PLD]]'s rollouts. **C3b**: on held-out OOD tasks, our transfer exceeds PLD's by ≥ 10 pp | [[2511.00091\|PLD]] hits 99% LIBERO *without any WM*. If C3a+C3b both fail, the WM (and therefore `r^phys` + `r^spatial` from imagined frames) is dead weight; paper reframes as "attribution-gated sim-SFT with task reward only" |
| **C4 — UWM's distinct decoders make per-head gradient asymmetry empirically observable** | Under anchor-free PS-uGRPO (on UWM: `β_MSE = γ = 0`, since `β_TC = 0` is UWM's default with $K_{\text{lat}}=1$; on Cosmos Policy: `β_MSE = γ = β_TC = 0`), $\|\nabla_\theta L_{\text{PS-uGRPO}}\|_{\text{action decoder}} / \|\nabla_\theta L_{\text{PS-uGRPO}}\|_{\text{patch decoder}}$ diverges monotonically over training rounds on UWM. Anchor losses bound the ratio: MSE + LPIPS on UWM; MSE + LPIPS + TC on Cosmos. **Decoder-collapse diagnostic**: direct empirical evidence for "anchors are necessary" | No prior work measures this ratio on [[2504.02792\|UWM]] — novel diagnostic, hinges on UWM's structural asymmetry (2-Linear+Mish action decoder vs. 1-Linear patch decoder). Cosmos's single denoiser cannot host this test |

## Backbones

### Summary

| Backbone | Pure PS-uGRPO (no anchors) suffices? | Needs anchors (Eqs. 12, 13, 14)? | What to ablate |
|---|---|---|---|
| [[2601.16163\|Cosmos Policy]] | ✓ (single denoiser → automatic imag-policy *alignment* under shared RL gradient) | Optional — sharpens imagination *fidelity* | `β_MSE = γ = 0` vs. defaults; FVD on held-out benchmark decoupled from task reward |
| [[2504.02792\|UWM]] | ✗ — patch decoder cut off from direct policy gradient; WM receives only the weaker log `u_θ` signal; DiT body still updates via shared self-attention | **Required** for sharp image decoding (C4) | Per-head gradient-norm ratio (C4); `β_MSE = 0` vs. `β_MSE = 0.1` image-decoder FVD; per-head frozen-weight ablation |

#### Cosmos Policy — detailed plan

Cosmos Policy is a single denoiser over all modalities (proprio, actions, value, multi-view images) injected as latent frames — no separate action/image heads. RL-only gradient therefore updates imagination parameters as a side effect of the action gradient through shared θ. Reward / steps-to-go are added as additional latent-frame modalities.

| Imagination gain | Under PS-uGRPO alone | Needs anchors (Eqs. 12, 13, 14)? |
|---|---|---|
| **Imag-policy alignment** (WM future matches policy distribution) | ✓ Free — shared weights | no |
| **Imag fidelity** (prediction matches physical reality, low FVD/SSIM) | ✗ Sparse RL may degrade it | yes |

**Ablation caveat**: single-denoiser makes fidelity-vs-alignment hard to separate. Defend by setting `β_MSE = γ = 0` in one run and measuring FVD/SSIM on an imagination benchmark decoupled from task reward.

#### UWM — detailed plan

[[2504.02792|UWM]] shares DiT body + AdaLN final layer; splits only at the output projection (2-Linear+Mish action decoder vs. 1-Linear patch decoder). Under PS-uGRPO alone (no anchors), the patch decoder only receives the weaker `log u_θ` gradient — observable symptom: asymmetric per-head gradient norms + drifting image fidelity. MSE + LPIPS anchors (Eqs. 12, 13) restore patch-decoder gradient and rebalance the body update (TC anchor Eq. 14 is inactive on UWM, `K_lat = 1`). Because the two decoders are structurally distinct (unlike Cosmos's single denoiser), per-head frozen-weight ablations are feasible.

> [!tip] Thesis advantage
> Falsifiable hypothesis, enabled by UWM's distinct heads (C4): *"anchor-free PS-uGRPO induces asymmetric per-head gradient norms and image-fidelity drift; MSE + LPIPS anchors (Eqs. 12, 13) restore balance on UWM — TC anchor Eq. 14 is inactive for UWM's single-latent-frame output."* Per-head gradient-norm ratios, frozen-weight ablations, and direct image-decoder FVD are all tractable on UWM — all infeasible on Cosmos's single denoiser.

If the archived code targets UWM, pilot on UWM first; Cosmos Policy follows as second-backbone validation.

#### LoRA weight-update strategy

Multi-round continual learning rules out full backbone fine-tuning (accumulating forgetting, poor compute scaling). Use LoRA on the shared body + full-FT on thin heads.

| Module | Strategy | Why |
|---|---|---|
| Shared DiT / AR body | **LoRA** (r=32, α=64) on attention Q/K/V/O + FFN up/down | Low-rank constraint bounds drift; compute-tractable for 14B |
| Action head (MLP / flow head) | **Full FT** at 1e-5 to 5e-6 | Small; receives direct RL gradient |
| Image patch decoder (UWM) | **Full FT** at 1e-5 | Small; preserves per-head diagnostic |
| AdaLN / timestep embeddings | **Frozen** | Fragile under LoRA |

**VLA-specific evidence**:

| Paper | Evidence |
|---|---|
| [[2603.11653\|VLA-RL-CL]] Table 3 | **Direct continual-VLA+GRPO ablation**: Without-LoRA → NBT = 40.9 ± 11.8 (catastrophic forgetting); default Seq. FT (LoRA r=32) → NBT ≈ 0.3, preserved zero-shot |
| [[2505.17016\|RIPT-VLA]] | Exact recommended split: LoRA r=32 (LR 1e-4) on backbone + full-FT action head (LR 1e-5) |

**Mechanism transferability** — flow-matching RL is domain-independent:
- [[2505.05470|Flow-GRPO]] — r=32, α=64 on SD3.5-M image generation · [yifan123/flow_grpo](https://github.com/yifan123/flow_grpo)
- [[2510.09976|FPO-Lyu]] — CFM-likelihood-free PPO on π₀; 87.2% LIBERO — empirical VLA bridge
- [[2505.22094|ReinFlow]] — learnable noise injection instead of ODE→SDE · [ReinFlow/ReinFlow](https://github.com/ReinFlow/ReinFlow)
- [[2507.21053|FPO-Berkeley]] — McAllister et al., "Flow Matching Policy Gradients" — independent CFM-likelihood-free precedent; distinct from FPO-Lyu despite name collision

[[2509.09674|SimpleVLA-RL]] (full-FT on OpenVLA-OFT 7B, 8×A800 80GB, single-task only) is infeasible for our multi-round multi-task pilot — motivates LoRA over full-FT.


## Sim-to-Real Gap

The three anchor losses (Eqs. 12, 13, 14) supervise the WM against sim's `o^sim_{t+1}`; PS-uGRPO's physics and spatial rewards (Eqs. 6, 7) are also computed against sim-ground-truth states — [[2603.17808|EVA]]'s IDM (trained on sim transitions, §Cold-start) and bbox extractors both reference sim. The WM therefore learns **sim physics**, not real physics.

**Policy sim-to-real** and **FIPER sim-to-real** are in scope (standard — policy via domain randomization per [[2601.16163|Cosmos Policy]] / [[2511.09515|WMPO]]; FIPER via real-rollout threshold re-fit per [[2510.09459|FIPER]]'s own demonstration). **WM sim-to-real is out of scope** — the WM is sim-fit and stays behind at deployment; imagination-based planning on real robots requires a separate real-corpus WM fine-tune (DROID, AgiBot) in a follow-up paper.

**Deployment recipe**: ship (policy + FIPER) to the real robot; discard the WM unless a follow-up real-corpus fine-tune is run. The WM is a training-time scaffold — consumed by PS-uGRPO (Eq. 11) and all three anchors (Eqs. 12, 13, 14) during sim training only.

## Excluded

Papers / mechanisms the proposal does not use, and why.

### Demo / human-in-loop dependent

| Anchor | Why excluded |
|---|---|
| [[2509.15155\|Self-Improving EFM]] | Steps-to-go bootstrap requires SFT demos — not available |
| [[2511.15605\|SRPO]] latent clusters | Cluster fit requires demo successes (SRPO's V-JEPA-2 distance retained as *deployment-fallback reward only*) |
| [[2511.16166\|EvoVLA]] full SAR + POE + Long-Horizon-Memory pipeline | SAR's Gemini-generated hard negatives are LLM-dependent; we adopt only the stage-bonus *concept* with sim per-subgoal signals replacing the Gemini-annotated curriculum |
| [[2602.12099\|GigaBrain-0.5M*]] | HIL rollouts require human-in-the-loop correction — not available |

### Redundant on unified backbones

| Anchor | Why redundant |
|---|---|
| [[2602.13977\|WoVR]] PACE | Batch WM fine-tune; shared-θ co-evolves for free (PACE is a modular-backbone cost). Cited as baseline |
| [[2602.12063\|VLAW]] | Policy→WM→policy alternation collapses into a single joint update on shared backbone |
| [[2602.06508\|World-VLA-Loop]] / [[2604.01985\|WAV]] / [[2510.26433\|CoLA-World]] | Alternative gating / co-evolution designs (project-site only, no runnable code) |

### Out of scope for this paper

| Topic | Why deferred |
|---|---|
| Real-robot WM training | Our WM is sim-fit. Transferring the WM itself to real requires DROID / AgiBot fine-tune — follow-up paper, not this one |
| Imagination-based planning at real-robot deployment | Requires the above; deployment recipe here is policy + FIPER only |
