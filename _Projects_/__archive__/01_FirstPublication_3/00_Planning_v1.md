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
> **Sim-based self-evolving WAM via PS-uGRPO (Physics-Spatial unified GRPO).** A pretrained unified WAM self-discovers failures via [[2510.09459|FIPER]] (proactive) and self-corrects via a **single unified GRPO loop on the joint (action, imagination) log-prob**, driven by a task + physics + spatial reward (Eq. 4). Policy and world-model co-evolve under one RL signal through the shared backbone θ. MSE (variable-length prefix AR), LPIPS, and DreamDojo TC serve as dense anchors. No task-specific demonstrations required. Primary pilot backbones: [[2504.02792|UWM]] and [[2601.16163|Cosmos-Policy]].

## Literature

### Prior self-evolving methods

Score weights: loop 0.30, label-free 0.20, gating 0.15, empirical 0.15, novelty 0.10, fit 0.05, code 0.05.

#### With public code

| Rank | Score | Paper | Repo | Model type | WM updated? | Policy updated? | Co-evolve? |
|---|---|---|---|---|---|---|---|
| 1 | 4.7 | [[2511.09515\|WMPO]] | [WM-PO/WMPO](https://github.com/WM-PO/WMPO) | VLA + pixel-space video WM (on-policy GRPO in imagination) | ≈ frozen during inner GRPO; fine-tuned in outer lifelong loop | ✓ GRPO | ≈ outer-loop (not headline) |
| 2 | 4.6 | [[2511.15605\|SRPO]] | [sii-research/siiRL](https://github.com/sii-research/siiRL) | VLA + frozen V-JEPA-2 latent WM (latent-cluster self-rewarding RL) | ✗ (V-JEPA-2 frozen — trajectory clustering only) | ✓ RL | NO |
| 3 | 4.5 | [[2509.15155\|Self-Improving-EFM]] | [self-improving-efms](https://github.com/self-improving-efms/self-improving-efms.github.io/blob/main/pointmass_notebook.ipynb) | EFM (steps-to-go → dense reward + success detector; pointmass ref impl) | ≈ (no explicit WM — steps-to-go head inside unified EFM) | ✓ | Ambiguous — unified end-to-end update |
| 4 | 4.4 | [[2602.13977\|WoVR]] | [RLinf/RLinf](https://github.com/RLinf/RLinf) — ⚠ **partial**: KIR + masked GRPO shipped; **PACE not shipped** | VLA + video-diffusion WM (masked GRPO + KIR + PACE) | ✓ PACE periodically refines WM | ✓ masked GRPO + KIR | **YES — explicit co-evolution** (paper) |
| 5 | 4.3 | [[2510.00406\|VLA-RFT]] | [OpenHelix-Team/VLA-RFT](https://github.com/OpenHelix-Team/VLA-RFT) | VLA + learned video world simulator (GRPO with verified rewards) | ✗ (WM trained offline — frozen during RFT) | ✓ GRPO | NO |
| 6 | 4.3 | [[2602.11075\|RISE]] | [OpenDriveLab/RISE](https://github.com/OpenDriveLab/RISE) | Compositional WM: Dynamics + Progress Value Model; online RL in imagination. **PVM stacked in our `r^task` (Eq. 5)** | ✗ (WM + PVM frozen during loop) | ✓ online RL on imagined rollouts | NO — WM frozen during loop |
| 7 | 4.2 | [[2603.19370\|VAMPO]] | [OpenHelix-Team/VAMPO](https://github.com/OpenHelix-Team/VAMPO) | Video Prediction Model (GRPO over denoising-as-MDP; latent-consistency reward) | ≈ unified VPM is the policy | ✓ GRPO over denoising | Ambiguous — unified VPM |
| 8 | 4.2 | [[2510.09459\|FIPER]] | [utiasDSL/fiper](https://github.com/utiasDSL/fiper) (MIT) | Failure predictor — RND-OE obs + ACE action + conformal threshold (AND). **Stacked: per-channel OR-union in Eq. 1/2** | N/A (detector only) | N/A (detector only) | NO — gate; attribution signal |
| 9 | 4.1 | [[2602.12063\|VLAW]] | [Robert-gyj/Ctrl-World](https://github.com/Robert-gyj/Ctrl-World) (MIT) — ⚠ **partial**: WM post-training shipped; VLM reward filter + VLA post-training NOT shipped | VLA + action-conditioned WM (iterative: rollouts fine-tune WM → VLM-filtered WM rollouts post-train VLA) | ✓ (FVD 225 → 64) | ✓ | **YES — iterative alternation** (paper) |
| 10 | 4.0 | [[2511.16166\|EvoVLA]] | [AIGeeksGroup/EvoVLA](https://github.com/AIGeeksGroup/EvoVLA) | VLA (POE pose-curiosity + Long-Horizon Memory). **POE pose-curiosity stacked in `r^task`** ([[1705.05363\|ICM]]-style forward dynamics on pose) | ✗ | ✓ | NO |
| 11 | 3.9 | [[2602.21633\|SC-VLA]] | [Kisaragi0/SC-VLA](https://github.com/Kisaragi0/SC-VLA) | VLA with SPI (aux progress-prediction heads) + OAR (online residual RL via reshaped reward) | ✗ (no separate WM) | ✓ residual RL | NO |
| 12 | 3.8 | [[2602.12099\|GigaBrain-0.5M*]] | [open-gigaai/giga-brain-0](https://github.com/open-gigaai/giga-brain-0) (Apache-2.0) | VLA + WM continual joint training with HIL rollouts | ✓ continually fine-tuned on HIL rollouts | ✓ joint VLA training | **YES — via HIL rollouts** |
| 13 | 3.5 | [[2511.07732\|ViPRA]] | [sroutray/vipra](https://github.com/sroutray/vipra) (Apache-2.0, ICLR 2026) | 3-stage pretraining + adaptation: actionless-video latent actions → VLM pretraining → flow-matching adaptation | ✓ VLM pretrained jointly on video + latent actions | ✓ flow-matching decoder fine-tuned | NO — pretrain-then-adapt |

#### Project-site only (design references)

[[2602.06508|World-VLA-Loop]] (closed-loop WM ↔ VLA with jointly-trained reward, SANS dataset; project site), [[2604.01985|WAV]] (subgoal-generator + sparse IDM verification; project site), [[2510.26433|CoLA-World]] (warm-up freezes OpenSora WM → train Latent Action Model → unfreeze + co-evolve; arxiv-only). All paper-only — no runnable code.

### Unified WAM backbones

Seven code-available **World Action Models** whose action and future-state paths share transformer weights (no parallel expert stacks, no adapter fusion). Ordered by scale.

**Pilot backbones** (full detail):

| # | Paper | Paradigm | Backbone | Scale | Imagination output | Action output | Head symmetry |
|---|---|---|---|---|---|---|---|
| 1 | [[2504.02792\|UWM]] | Diffusion (DDPM + DDIM) | Shared DiT + independent diffusion timesteps $t_a, t_{o'}$ | ~0.2B | Single-Linear image patch decoder | Symmetric encoder/decoder: 2-Linear + Mish MLP | Near-symmetric |
| 2 | [[2601.16163\|Cosmos-Policy]] | Latent video diffusion | Cosmos-Predict2 single video denoiser | 2B | Future frames as latent frames | Actions as latent frames | **Fully symmetric** |

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

Given a pretrained unified-backbone WAM ([[2601.16163|Cosmos-Policy]] or [[2504.02792|UWM]]) and a simulator with next-state + success ground truth, the backbone's policy and world-model **co-evolve through a single GRPO loop** (PS-uGRPO, Eq. 11) whose reward combines task, physics, and spatial signals. Three dense anchors — MSE with prefix-AR (Eq. 12), LPIPS (Eq. 13), DreamDojo TC (Eq. 14) — supply the per-pixel and per-velocity gradient that scalar RL cannot.

**Attribution** — per-channel FIPER + sim: per-step WM-error `‖ŵ_{t+1} − o^sim_{t+1}‖² > τ_δ` (RND-OE channel) defines the WM-attributed set `M_img`; trajectory `r_i = 0` with ACE-flagged policy uncertainty (ACE channel) defines `F_pol`. The step-indexed update set `U = F_pol ∪ proj(M_img)` focuses the RL gradient on attributed failures only; successes are left alone.

**Unified gradient** — PS-uGRPO's single negative advantage on `U` pushes θ away from (bad action, bad imagination) pairs; anchor losses apply on `M_img` regardless. Both heads update in one optimizer step through shared θ — architectural co-evolution via the unified RL signal, not two separate losses.

**Multi-round iteration** — each round, attribution tracks the current failure frontier; θ updates on confirmed mistakes. Periodic FIPER thresholds and PVM recalibration on fresh successes (§Algorithm step 10).

**Deployment portability (policy + FIPER only, not the WM)** — the *policy* and *FIPER* transfer to real-robot deployment; FIPER uses only model-internal state, providing a runtime safety layer without sim ground truth. The **WM does not transfer**: its rewards (`r^phys`, `r^spatial`) and anchors (MSE, LPIPS) all reference sim, so it learns sim physics. WM-as-deployment-imagination requires a separate real-corpus fine-tune — see §Sim-to-Real Gap.

> [!warning] Cold-start protocol
>
> Round 0 runs $K$ rollouts through pure sim verification (no FIPER); the resulting success set calibrates thresholds $\tau_{\text{ACE}}, \tau_{\text{RND}}$. Rounds N ≥ 1 continue calling sim; FIPER adds a parallel attribution channel. **Backbone precondition**: ≥ 5–10% Round-0 zero-shot success. $\tau_{\text{ACE}}, \tau_{\text{RND}}$ and PVM refit every `RECAL` rounds on the sliding success window (§Algorithm step 10).
>
> **Pre-Round-0 one-time calibration** (sim rollouts + sim oracle only — same dependency tier as the simulator; no demos, no LLM, no human labels):
> - **PVM** ([[2602.11075|RISE]]): TD bootstrap on sim successes + failures with `±1` terminals (RISE Eq. 6); squash to `[0,1]` via `(V+1)/2`.
> - **POE forward-dynamics model $\hat{f}_{\text{fwd}}$** ([[2511.16166|EvoVLA]] / [[1705.05363|ICM]]): small MLP on sim transitions $(z_t, a_t, z_{t+1})$ with pose features $z = \psi(T_{\text{ee}}^{-1} T_{\text{obj}})$; ~10k random-action rollouts, MSE loss (~minutes on CPU).
> - **V-JEPA 2 surprise scorer** ([[2601.10553|WMReward]] over [[2506.09985|V-JEPA-2]] ViT-g, ~1B, MIT) + **LPIPS Alex-lin** (frozen): both pretrained, plug-and-play.
> - **No IDM needed**: physics signal is the frozen-JEPA residual ($D_{\text{phys}}$); avoids the architectural-prior-sharing reward-hacking risk of learned-IDM critics co-evolving with a same-family policy.
>
> **Caveats**: (i) PVM cold-start needs ≥ 5–10% zero-shot success; (ii) $D_{\text{phys}}$ is uninformative on near-random imagined frames at cold-start until imagination stabilizes.

### Mechanism synthesis

Ten mechanisms compose PS-uGRPO + three anchor sources (Eq. 15, derived in §Mathematics); six related mechanisms are considered and rejected or reserved for deployment.

**Stacked (10 + 3 anchors)** — each contributes a specific term of Eq. 15:

| Paper | Contribution (what we take) | Target term | What we skip |
|---|---|---|---|
| [[2511.09515\|WMPO]] | (i) GRPO-in-imagination compute graph; K joint rollouts per batch — PS-uGRPO scaffolding; (ii) **asymmetric dual-clip** `ε_low=0.20, ε_high=0.28`; (iii) **no-KL** (no reference model); (iv) **dynamic sampling filter** (drop all-success / all-fail K-groups) | PS-uGRPO scaffolding + clip + sampling refinements (Eq. 11) | Outer lifelong WM fine-tune; VideoMAE reward model (replaced by V-JEPA 2 surprise + sim oracle) |
| [[2505.05470\|Flow-GRPO]] | ODE→SDE conversion (both heads); denoising reduction | $\log \pi_\theta$, $\log u_\theta$ (Eq. 10) | Image-gen benchmarks |
| [[2510.09459\|FIPER]] | RND-OE + ACE dual-channel conformal gate | `F_pol`, `M_img` → `𝒰` (Eq. 11) | AND-rule (→ per-channel OR) |
| [[2602.13977\|WoVR]] | (i) KIR keyframe-init rollouts; (ii) **trajectory-length normalization** `1/T_valid_i` (WoVR paper Eq. 11) — replaces flat `1/|U|` so short successful trajectories get proportional credit | `M_img` segmentation (Eq. 2) + `1/T_valid_i` weighting in Eq. 11 | PACE (shared-θ subsumes); dual-channel action injection / first-frame anchoring (backbone-provided); binary success reward (PVM is denser) |
| [[2602.11075\|RISE]] | PVM for dense task reward | `V_ψ` in `r^task` (Eq. 5) | Demo warm-up |
| [[2511.16166\|EvoVLA]] | POE pose-grounded curiosity (forward-dynamics prediction error on relative gripper-to-object pose); [[1705.05363\|ICM]] is the canonical underlying method | `λ_cur · r^cur` (Eq. 5) | SAR (CLIP + Gemini hard negatives — LLM-dependent), Long-Horizon Memory (system-architectural) |
| [[2012.06644\|CAPS]] | 1st-order temporal action-smoothness regularizer; ICRA 2021 canonical reference. [[2210.13702\|DeXtreme]] action-delta penalty as manipulation corroboration | `λ_smooth · S_act` in `r^task` (Eq. 5) — folded into task component as action-quality penalty | Spatial smoothness term, direct policy regularization (we use temporal only, route through GRPO advantage) |
| [[2601.10553\|WMReward]] (over [[2506.09985\|V-JEPA-2]] ViT-g) | Frozen V-JEPA 2 surprise score on adjacent imagined frames; ~1B, MIT, no LLM, no fine-tuning; SOTA PhysicsIQ (62.0%) | `λ_phys · D_phys` in `r^phys` (Eq. 6) — object-state physics axis | Best-of-N video selection (their use); we route the scalar into GRPO advantage |
| [[2602.06949\|DreamDojo]] | Velocity-change TC loss (DreamDojo's Eq. 4), over $K_{\text{lat}}$ latent frames per video chunk | `β_TC · L^TC` (Eq. 14). Active on multi-latent-frame backbones: UWM default config $K_{\text{lat}} \approx 8$ (17 future frames + temporal-patch-2); Cosmos Wan2.1 4:1 → $K_{\text{lat}} \geq 4$. Inactive only on $K_{\text{lat}}=1$ configs | Relative-action conditioning + chunked injection (backbone-provided) |
| [[2602.00743\|SA-VLA]] | Phase-conditioned signed geometric reward (Reach/Place/Leave) | `λ_geo · Δ_geo(phase)` in `r^spatial` (Eq. 7) | SCAN annealed-noise (Flow-GRPO's SDE subsumes) |
| [[2511.07403\|SpatialThinker]] | CIoU bbox-alignment reward | `λ_CIoU · CIoU(bbox)` in `r^spatial` | STVQA-7K dataset (sim bboxes replace) |
| [[2603.25685\|Persistent-Robot-WMs]] | Variable-length-prefix AR training (F4 mitigation) | `L_img^flow-prefix` (Eq. 12) — essential dense anchor | Reward-contrasted denoising (PS-uGRPO subsumes with richer reward) |
| [[1801.03924\|LPIPS]] | Perceptual anchor (partial F5 mitigation) | `β_LPIPS · L_img^LPIPS` (Eq. 13) | Extensive backbone fine-tuning (paper warns against; Alex-lin frozen) |

**Alternatives / deployment-only (6)** — noted for completeness, not in the stack. Each row has a distinct reason for exclusion (not just "alt reward"):

| Paper | Role | Why not stacked |
|---|---|---|
| [[2602.21633\|SC-VLA]] | Sparse World Imagination = auxiliary progress-prediction heads + reward reshaping | Not an initial-state sampler (paper's SPI = *Sparse Predictive Imagination*, not *Sparse-imagination Preferential*); progress-prediction role is redundant with RISE's PVM |
| [[2511.07732\|ViPRA]] | Pretraining choice (pre-Round-0 backbone) | Not in the loop; flow-matching decoder adaptation is superseded by Flow-GRPO |
| [[2511.15605\|SRPO]] | Deployment-fallback reward (V-JEPA-2 latent-cluster) | Sim oracle is direct during training; SRPO only fills in when sim is unavailable |
| [[2510.00406\|VLA-RFT]] | GRPO with pixel+LPIPS verified reward inside a **frozen** WM simulator | **Role mismatch**: VLA-RFT freezes the WM and RLs the policy inside it; we co-train the WM via PS-uGRPO. Also **LPIPS role mismatch**: they use it as a reward; we use it as a dense anchor loss (Eq. 13) |
| [[2603.19370\|VAMPO]] | Denoising-as-MDP with latent-consistency reward | **Mechanism supersession**: VAMPO's denoising-step MDP is subsumed by our Flow-GRPO ODE→SDE at the environment level; composing both would double-wrap RL (MDP-within-MDP) |
| [[2603.27866\|Wan-R1]] | GRPO with endpoint / temporal-order / structural-consistency rewards | **Reward subsumption**: all three map onto our Eq. 4 decomposition (`Δ_geo`, `D_TC`, CIoU); our physics+spatial is strictly richer (adds CAPS action-smoothness in r^task + WMReward V-JEPA 2 surprise on imagined frames) and manipulation-native |

**Stacking order**: PS-uGRPO core (Eq. 11: WMPO + Flow-GRPO + FIPER + WoVR KIR) → compose `r^uni` (Eq. 4: task + physics + spatial) → add three anchors (Eqs. 12, 13, 14). Component credit in §Baselines ablations. **WMPO-specific deviations** (sim rollouts vs. imagined; unified `r^uni` vs. binary success; joint-log-prob GRPO vs. policy-only; per-step anchors vs. outer WM fine-tune) are made explicit in the WMPO row above and Eq. 11.

### Mathematics

**TL;DR**: $L_{\text{total}}(\theta) = L_{\text{PS-uGRPO}} + \beta_{\text{MSE}} \cdot L^{\text{flow-prefix}} + \beta_{\text{LPIPS}} \cdot L^{\text{LPIPS}} + \beta_{\text{TC}} \cdot L^{\text{TC}}$. One unified GRPO on the joint action+imagination log-prob under a task (PVM + POE + CAPS smoothness) + physics (V-JEPA 2 surprise on imagined frames) + spatial (Δ_geo + CIoU on imagined frames) reward; three dense anchors (MSE with variable-length prefix AR, LPIPS, DreamDojo temporal-consistency) prevent high-dim decoder collapse. Both heads co-evolve under a **single** RL signal through shared θ. Equations 1–11 follow; symbol glossary in §Notation at the end of this subsection.

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

Policy-attributed trajectories contribute all their steps; WM-attributed failures contribute only the specific mis-prediction step. We use OR (not FIPER's official AND) — AND detects but cannot separate cause; precision is regained via per-channel sim-verification inside each set. §Baselines ablation quantifies the tradeoff.

**Unified reward** — task + physics + spatial (Eq. 4):

$$
r^{\text{uni}}_{i,t} \;=\; w_T \cdot r^{\text{task}}_{i,t} \;+\; w_P \cdot r^{\text{phys}}_{i,t} \;+\; w_S \cdot r^{\text{spatial}}_{i,t} \tag{4}
$$

Each component defined below, used directly from its source paper.

**Task component** — task progress + pose-grounded curiosity + action quality (Eq. 5; [[2602.11075|RISE]] PVM + [[2511.16166|EvoVLA]] POE + [[2012.06644|CAPS]] action smoothness):

$$
r^{\text{task}}_{i,t} = V_\psi(o_{i,t}, \text{goal}) + \lambda_{\text{cur}} \cdot r^{\text{cur}}_{i,t} - \lambda_{\text{smooth}} \cdot S_{\text{act}}(a_{i, t-1:t+1}) \tag{5}
$$

$V_\psi$ per RISE Eq. 6 (TD bootstrap on sim successes + failures, ±1 terminals; squash via $(V+1)/2$); $r^{\text{cur}}_{i,t} = \tfrac{\eta}{2}\|\mathrm{sg}(\hat{f}_{\text{fwd}}(z_{i,t}, a_{i,t})) - z_{i,t+1}\|^2$ on pose features $z_t = \psi(T_{\text{ee}}^{-1} T_{\text{obj}}) \in \mathbb{R}^6$ (stop-gradient on the prediction is load-bearing — prevents policy from gaming curiosity by degrading $\hat{f}_{\text{fwd}}$); $S_{\text{act}} = \|a_{i,t} - a_{i,t-1}\|_2$ (1st-order CAPS-faithful). Defaults in §Notation.

**Physics component** — V-JEPA 2 surprise residual on WAM imagined output (Eq. 6; [[2601.10553|WMReward]]):

$$
r^{\text{phys}}_{i,t} = \lambda_{\text{phys}} \cdot D_{\text{phys}}(\hat{o}_{i,t}, \hat{o}_{i,t+1}) \tag{6}
$$

**WMReward V-JEPA 2 surprise**: $D_{\text{phys}} = \tfrac{1}{2}(1 + \cos(P_\phi(E_\theta(\hat{o}_{i, \le t})), E_\theta(\hat{o}_{i,t+1}))) \in [0, 1]$ (rescaling of WMReward's $1-\cos$ loss), with frozen V-JEPA 2 ViT-g $(E_\theta, P_\phi)$ (~1B, matches WMReward default) — no LLM, no fine-tuning. Catches imagined object-state failures (penetration, anti-gravity, permanence).

**Spatial component** — phase-geometric + bbox alignment on WAM imagined frames (Eq. 7; [[2602.00743|SA-VLA]] + [[2511.07403|SpatialThinker]]):

$$
r^{\text{spatial}}_{i,t} = \lambda_{\text{geo}} \cdot \Delta_{\text{geo}}\bigl(\text{phase}_t\bigr) + \lambda_{\text{CIoU}} \cdot \mathrm{CIoU}\bigl(\mathrm{bbox}(\hat{o}_{i,t+1}),\, \mathrm{bbox}(o^{\text{sim}}_{i,t+1})\bigr) \tag{7}
$$

**SA-VLA phase-geometric**: $\Delta_{\text{geo}}$ = signed geometric-distance change per phase (Reach: ↓gripper→object; Place: ↓object→target; Leave: ↑retreat). Normalized $\in [0,1]$ (SA-VLA Eqs. 8–10). **SpatialThinker CIoU**: on imagined vs. sim bboxes; we rescale $(\mathrm{CIoU}_{\text{raw}} + 1)/2 \in [0,1]$ for additive composability (our addition; SpatialThinker uses raw mean CIoU). See §Notation for implementation details.

**Group-relative advantage** on unified reward — Eq. 8:

$$
\mu_t = \tfrac{1}{K}\textstyle\sum_i r^{\text{uni}}_{i,t}, \quad \sigma_t = \sqrt{\tfrac{1}{K}\textstyle\sum_i (r^{\text{uni}}_{i,t} - \mu_t)^2}, \quad A^{\text{uni}}_{i,t} = \frac{r^{\text{uni}}_{i,t} - \mu_t}{\sigma_t + \epsilon_{\text{num}}} \tag{8}
$$

**Flow-GRPO SDE** — [[2505.05470|Flow-GRPO]] ODE→SDE conversion applies to *both* heads (Eq. 9). Action head via $v_\theta$; WM head via $u_\theta$ (same form with substituted variables):

$$
da_s = \bigl[ v_\theta(a_s;\, o_{i,t}, c) + \tfrac{\sigma_{\text{flow}}^2(s)}{2} \nabla_{a_s} \log p_s(a_s) \bigr] ds + \sigma_{\text{flow}}(s)\, dW_s \tag{9}
$$

Denoising reduction: $S_{\text{train}}=10 \ll S_{\text{infer}}=40$ (Flow-GRPO's SD3.5-M settings) gives ~4× rollout speedup at no inference-quality cost.

**Joint log-prob factorization** — Eq. 10. UWM: action and image heads run with **independent timesteps** $(t_a, t_{o'})$ — exact conditional-independence factorization. Cosmos Policy: shared timestep — Eq. 10 is a logical regrouping of one packed-sequence log-prob aligned to $r^{\text{uni}}$'s reward channels. Either reading gives the same Eq. 11 update.

$$
\log \pi_\theta^{\text{joint}}(a_{i,t},\, \hat{o}_{i,t+1} \mid o_{i,t}, c) = \log \pi_\theta(a_{i,t} \mid o_{i,t}, c) + \log u_\theta(\hat{o}_{i,t+1} \mid o_{i,t}, a_{i,t}, c) \tag{10}
$$

For AR-token backbones ([[2506.19850|UniVLA]], [[2506.21539|WorldVLA]]), replace $\log u_\theta$ with the AR-token log-prob $\sum_k \log p_\theta(z^{(k)}_{i,t+1} \mid \cdots)$ — factorization still holds.

**PS-uGRPO — unified Physics-Spatial GRPO loss** (Eq. 11), with **WoVR** trajectory-length normalization and **WMPO** asymmetric dual-clip:

$$
L_{\text{PS-uGRPO}}(\theta) = -\frac{1}{|\mathcal{U}_{\text{traj}}|} \sum_{i \in \mathcal{U}_{\text{traj}}} \frac{1}{T^{\text{valid}}_i} \sum_{t \in \mathcal{U}_i} \min\bigl(\rho_{i,t} A^{\text{uni}}_{i,t},\ \mathrm{clip}(\rho_{i,t}, 1 - \varepsilon_{\text{low}}, 1 + \varepsilon_{\text{high}}) A^{\text{uni}}_{i,t}\bigr) \tag{11}
$$

where $\mathcal{U}_{\text{traj}} = \{i : \mathcal{U}_i \ne \emptyset\}$, $\mathcal{U}_i = \{t : (i,t) \in \mathcal{U}\}$ (other symbols in §Notation). **Inherited refinements**: [[2602.13977|WoVR]] paper Eq. 11 per-trajectory $1/T^{\text{valid}}_i$ length-norm + [[2511.09515|WMPO]] asymmetric dual-clip ($\varepsilon_{\text{low}}=0.20, \varepsilon_{\text{high}}=0.28$, WMPO Table 4) + WMPO no-KL (LoRA + clip control drift) + WMPO dynamic sampling (drop all-collapse K-groups; §Algorithm step 1.5 — extends WMPO's binary 0/1 filter to dense rewards).

One loss, one advantage, one joint log-prob — both heads updated by a single RL signal.

**MSE anchor with variable-length prefix AR** — F4 mitigation (Eq. 12, flow-matching):

$$
L_{\text{img}}^{\text{flow-prefix}}(\theta) = \mathbb{E}_{k \sim \mathcal{U}[0, K_{\max}]} \, \frac{1}{|M_{\text{img}}|} \sum_{(i,j,t) \in M_{\text{img}}} \mathbb{E}_{s, \varepsilon} \bigl[\, \|u_\theta(x_s;\, \tilde{o}_{i,t-k:t}, a_{i,t}, s) - v^\ast(o^{\text{sim}}_{i,t+1})\|^2 \,\bigr] \tag{12}
$$

$\tilde{o}_{i,t-k:t}$ = WAM's free-rolled obs ($k=0$ ground-truth, $k=K_{\max}$ fully imagined) — interpolates teacher-forced and free-rollout, eliminating exposure bias. AR-backbone analog: token CE with VQ targets.

**LPIPS perceptual anchor** — F5 partial mitigation (Eq. 13):

$$
L_{\text{img}}^{\text{LPIPS}}(\theta) = \frac{1}{|M_{\text{img}}|} \sum_{(i,j,t) \in M_{\text{img}}} \mathrm{LPIPS}\bigl(\mathrm{Dec}(\hat{x}^{\text{clean}}_{i,t+1}),\, o^{\text{sim}}_{i,t+1}\bigr) \tag{13}
$$

**Decode**: flow-matching uses single-Euler-step at $s \approx 0.9$ + frozen-VAE decode (per [[2510.00406|VLA-RFT]] / [[2601.20218|DenseGRPO]]); AR backbones use straight-through $\arg\max$ decode. LPIPS backbone is frozen Alex-lin.

**DreamDojo temporal-consistency anchor** — F4+F5 support (Eq. 14), [[2602.06949|DreamDojo]] Eq. (4) over $K_{\text{lat}}$ latent frames **within** a single video-chunk generation:

$$
L^{\text{TC}}(\theta) = \frac{1}{|M_{\text{img}}|} \sum_{(i,j,t) \in M_{\text{img}}} \mathbb{E}\Bigl[\sum_{k=1}^{K_{\text{lat}}-1} \bigl\|(z^{(k+1)}_{i,t} - z^{(k)}_{i,t}) - (v^{\ast(k+1)}_{i,t} - v^{\ast(k)}_{i,t})\bigr\|^2\Bigr] \tag{14}
$$

$z^{(k)}_{i,t} = u_\theta(x^{(k)}_{i,t}, k, c)$ = predicted velocity at latent frame $k$; $v^{\ast(k)}_{i,t}$ = ground-truth velocity (sim → backbone-VAE + finite difference); $K_{\text{lat}}$ = backbone-specific latent-frame count. Active when $K_{\text{lat}} > 1$ (Cosmos $\geq 4$, UWM ≈8, DreamZero); inactive on $K_{\text{lat}}=1$ configs. $\beta_{\text{TC}} = 0.1$ (our default; DreamDojo doesn't publish a numerical λ).

**Full objective** — unified RL + three dense anchors (Eq. 15):

$$
L_{\text{total}}(\theta) = L_{\text{PS-uGRPO}}(\theta) + \beta_{\text{MSE}} \cdot L_{\text{img}}^{\text{flow-prefix}}(\theta) + \beta_{\text{LPIPS}} \cdot L_{\text{img}}^{\text{LPIPS}}(\theta) + \beta_{\text{TC}} \cdot L^{\text{TC}}(\theta) \tag{15}
$$

The PS-uGRPO term is the dominant training signal; the three anchors provide dense gradient RL advantage cannot. Defaults: $\beta_{\text{MSE}} = \beta_{\text{LPIPS}} = \beta_{\text{TC}} = 0.1$.

#### WAM failure modes — mapping to Eq. 15 terms

Eq. 15's four terms jointly close all five failure modes of the current WAM's imagination:

| Mode | Closed by |
|---|---|
| **F1** Action-conditioning misalignment | MSE anchor (Eq. 12, `k=0`) + r^task action-smoothness term (Eq. 5) + r^phys V-JEPA 2 surprise on imagined frames (Eq. 6) |
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
- $f_\theta(o, a)$ — WM single-step prediction; produces estimate $\hat{w}_{i,t+1}$ (used in Eq. 2).
- $V_\psi(o, \text{goal})$ — [[2602.11075|RISE]] Progress Value Model (parameters $\psi$ separate from $\theta$); see Eq. 5 prose for RISE Eq. 6 cold-start details.

*Rollouts and sim oracle*:
- $i \in \{1, \ldots, K\}$ — rollout index; $K$ = per-batch group size.
- $T$ — rollout horizon; $\tau_i = (o_{i,0}, a_{i,0}, \ldots, o_{i,T})$.
- $t \in \{0, \ldots, T-1\}$ — environment step (distinct from flow time $s$ below).
- $T^{\text{valid}}_i$ — per-trajectory valid length (up-to-first-success); [[2602.13977|WoVR]] length-normalization in Eq. 11.
- $o_{i,0} \sim p_0^{\text{sim}}$ — initial state (uniform over the simulator's reset distribution).
- $r_i \in \{0,1\}$ — sim trajectory-success oracle; $o^{\text{sim}}_{i,t+1}$ — per-step sim ground-truth observation.
- $c$ — language task instruction (shared across a rollout's steps).
- $\text{goal}$ — goal spec input to $V_\psi$ (derived from $c$).

*GRPO clip + sampling* ([[2511.09515|WMPO]]-faithful refinements; see Eq. 11):
- $\rho_{i,t}$ — PPO/GRPO probability ratio $\pi_\theta^{\text{joint}}/\pi_{\theta_{\text{old}}}^{\text{joint}}$.
- $\varepsilon_{\text{low}}, \varepsilon_{\text{high}}$ — asymmetric dual-clip bounds; defaults $0.20, 0.28$ (WMPO Table 4).
- No KL term; dynamic sampling filter — see Eq. 11.

*FIPER scores / thresholds*:
- $\mathrm{ACE}(\tau_i)$ — action-chunk entropy; $\mathrm{RND\text{-}OE}(o_{i,t})$ — observation OOD.
- $\tau_{\text{ACE}}, \tau_{\text{RND}}$ — conformal thresholds (calibrated per §Cold-start protocol).
- $\tau_\delta$ — L2 threshold for WM mismatch $\|\hat{w}_{i,t+1} - o^{\text{sim}}_{i,t+1}\|^2 > \tau_\delta$.

*WoVR KIR segmentation* (Eq. 2):
- $H_{\text{kir}} \ll T$ — keyframe segment length.
- $j$ — segment index spanning $[j H_{\text{kir}}, (j+1) H_{\text{kir}})$; observations at multiples of $H_{\text{kir}}$ serve as keyframes.

*Unified reward components* (Eqs. 4–7):
- $r^{\text{uni}}_{i,t}$ — unified per-step reward driving PS-uGRPO.
- $r^{\text{task}}_{i,t}$ — task component (RISE PVM + EvoVLA POE + CAPS smoothness; Eq. 5).
- $r^{\text{phys}}_{i,t}$ — physics component (V-JEPA 2 surprise on imagined frames; Eq. 6).
- $r^{\text{spatial}}_{i,t}$ — spatial component (phase-geometric + CIoU bbox alignment on imagined frames; Eq. 7).
- $z_t = \psi(T_{\text{ee}}^{-1} \cdot T_{\text{obj}}) \in \mathbb{R}^6$ — relative gripper-to-object pose feature; sim provides $T_{\text{ee}}, T_{\text{obj}}$ directly.
- $r^{\text{cur}}_{i,t}$ — pose-curiosity reward (POE forward-dynamics prediction error; Eq. 5 prose). $\hat{f}_{\text{fwd}}$ pre-trained on sim transitions during cold-start.
- $S_{\text{act}}$ — 1st-order action smoothness (Eq. 5 prose).
- $w_T, w_P, w_S \ge 0$ — top-level reward weights; defaults $w_T = 1.0$, $w_P = w_S = 0.3$.
- $\lambda_{\text{cur}}, \lambda_{\text{smooth}} \ge 0$ — r^task sub-weights; defaults $\lambda_{\text{cur}} = 0.6$ (EvoVLA's $\rho$), $\lambda_{\text{smooth}} = 0.1$.
- $\eta$ — POE intrinsic scale (default $1.0$).

*Physics reward internals* (Eq. 6):
- $E_\theta, P_\phi$ — frozen [[2506.09985|V-JEPA-2]] ViT-g encoder + predictor (~1B, MIT; matches WMReward default `vitg`); context window $\le t$ at 256² resolution.
- $D_{\text{phys}} \in [0, 1]$ — [[2601.10553|WMReward]] surprise score (higher = imagined next frame matches predictor's expectation).
- $\lambda_{\text{phys}} \ge 0$ — physics weight; default $1.0$.

*Spatial reward internals* (Eq. 7):
- $\text{phase}_t \in \{\text{Reach}, \text{Place}, \text{Leave}\}$ — manipulation phase from sim's subgoal oracle.
- $\Delta_{\text{geo}}(\text{phase}_t)$ — signed geometric-distance change per phase (see Eq. 7 prose for sign convention).
- $\mathrm{bbox}(\cdot)$ — object bounding-box extractor; applied to imagined $\hat{o}_{i,t+1}$ and sim $o^{\text{sim}}_{i,t+1}$.
- $\mathrm{CIoU}(\cdot, \cdot) \in [0, 1]$ — Complete IoU (Zheng et al. 2020), rescaled from raw $[-1,1]$ via $(\mathrm{CIoU}_{\text{raw}} + 1)/2$.
- $\lambda_{\text{geo}}, \lambda_{\text{CIoU}}$ — spatial sub-weights; defaults $1.0, 0.5$.

*GRPO statistics* (Eq. 8):
- $\mu_t, \sigma_t$ — per-timestep mean and std of $r^{\text{uni}}_{\cdot, t}$ over the $K$ rollouts.
- $A^{\text{uni}}_{i,t}$ — per-timestep unified advantage.
- $\epsilon_{\text{num}}$ — small constant for denominator numerical stability.
- $\mathcal{U}$ — step-indexed update set (attribution-routed failure focus; Eq. 3).

*Flow-matching SDE variables* (Eqs. 9, 10, 12):
- $s \in [0,1]$ — flow time (distinct from environment step $t$).
- $a_s, x_s$ — flow-matching interpolant samples at flow time $s$ (action and image variants).
- $\varepsilon \sim \mathcal{N}(0, I)$ — flow-matching noise (distinct from $\epsilon_{\text{num}}$).
- $\sigma_{\text{flow}}(s)$ — SDE diffusion coefficient (distinct from GRPO's $\sigma_t$).
- $p_s(a_s)$ — marginal density of $a_s$ under the flow.
- $dW_s$ — Wiener increment.
- $v^\ast$ — ground-truth flow velocity target (Eq. 12).
- $\pi_\theta^{\text{joint}}$ — joint action + imagined-next-observation log-prob (factorizes per Eq. 10).

*AR-token variables* (AR-backbone analog of Eq. 12):
- $z_{i,t+1}$ — VQ-tokenized next observation (target for AR-backbone CE loss).
- $\mathrm{VQ}(\cdot)$ — vector-quantizer encoder (backbone-specific).
- $k$ — token index within $z_{i,t+1}$.

*Anchor losses* (Eqs. 12, 13, 14):
- $K_{\max}$ — maximum rollout prefix length for F4 mitigation; default $9$ (matches [[2603.25685|Persistent-Robot-WMs]] §S1, $P \sim \mathrm{Unif}\{0, \ldots, 9\}$).
- $\tilde{o}_{i,t-k:t}$ — WAM's free-rolled observation sequence of length $k$ (ground-truth at $k=0$, pure WAM-imagined at $k=K_{\max}$).
- $\mathrm{LPIPS}(\cdot, \cdot)$ — learned perceptual image patch similarity (Alex-lin backbone frozen).
- $\hat{x}^{\text{clean}}_{i,t+1}$ — single-Euler-step clean prediction at $s \approx 0.9$ for flow-matching backbones (formula in Eq. 13 prose); AR backbones use $\mathrm{Dec}(\arg\max p_\theta)$ with straight-through estimator.
- $\mathrm{Dec}(\cdot)$ — backbone's frozen pixel decoder (VAE for flow-matching; VQ-GAN for AR).
- $z^{(k)}_{i,t}$ — predicted velocity at latent frame $k$ within the WM's video-chunk generation (DreamDojo notation; formula in Eq. 14).
- $v^{\ast(k)}_{i,t}$ — ground-truth velocity at latent frame $k$ (sim → backbone-VAE + finite difference; details in Eq. 14 prose).
- $K_{\text{lat}}$ — WM's per-generation latent-frame count (backbone- and config-specific; see Eq. 14 prose); TC anchor inactive when $K_{\text{lat}} = 1$. Disambiguated from batch-size $K$.

*Loss weights* (Eq. 15):
- $\beta_{\text{MSE}} \ge 0$ — MSE anchor weight; default $0.1$.
- $\beta_{\text{LPIPS}} \ge 0$ — LPIPS anchor weight; default $0.1$.
- $\beta_{\text{TC}} \ge 0$ — DreamDojo TC anchor weight; default $0.1$ (our default; DreamDojo doesn't publish a numerical $\lambda$).

### Algorithm

```python
# Round N: PS-uGRPO — unified Physics-Spatial GRPO + MSE / LPIPS / TC anchors.
# One RL loop on joint (action, imagination) log-prob; anchor losses prevent decoder collapse.

# 1. Joint rollout — policy generates actions, WM generates imagined next-frames, sim steps.
#    Each rollout yields both real (a, o_sim) and imagined (a, o_hat) trajectories.
rollouts = [joint_rollout_in_sim(θ, T=T) for _ in range(K)]   # returns (a, o_sim, o_hat) per step

# 1.5. WMPO dynamic sampling filter — drop K-groups with no advantage signal; resample to fill batch.
while all_collapse(rollouts):                              # all r^uni_i identical (e.g. all 0 or all 1)
    rollouts = [joint_rollout_in_sim(θ, T=T) for _ in range(K)]

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
        z_t   = pose_feat(T_ee[i,t], T_obj[i,t])                       # sim-provided relative pose
        z_tp1 = pose_feat(T_ee[i,t+1], T_obj[i,t+1])
        r_cur = (η/2) * ||sg(f_fwd_hat(z_t, a[i,t])) - z_tp1||**2       # EvoVLA POE / ICM pose-curiosity (stop-gradient on prediction)
        r_task[i,t] = (PVM_ψ(o_sim[i,t], goal)
                       + λ_cur * r_cur
                       - λ_smooth * S_act(a[i, t-1:t+1]))               # CAPS action smoothness
        r_phys[i,t] = λ_phys * D_phys(o_hat[i,:t+1], o_hat[i,t+1])      # WMReward V-JEPA 2 surprise: predictor uses full imagined history o_hat[≤t]
        r_spat[i,t] = (  λ_geo  * signed_geo_delta(phase[i,t], o_sim[i,t:t+2], a[i,t])
                       + λ_CIoU * CIoU(bbox(o_hat[i,t+1]), bbox(o_sim[i,t+1])))
        r_uni[i,t]  = w_T * r_task[i,t] + w_P * r_phys[i,t] + w_S * r_spat[i,t]

# 5. Group-relative advantage (Eq. 8).
μ_t, σ_t = per-timestep statistics of r_uni over K
A_uni[i,t] = (r_uni[i,t] - μ_t) / (σ_t + ε_num)

# 6. PS-uGRPO — single RL loss on joint log-prob (Eq. 11).
# log_pi_joint_old: snapshot of joint log-prob computed under θ_old (parameters before this update step);
# standard PPO/GRPO bookkeeping — cached per-rollout when collecting the batch.
L_PS_uGRPO = 0.0
U_traj = {i for (i, _) in U}                                # WoVR trajectory-level outer sum
for i in U_traj:
    L_traj_i = 0.0
    U_i = [t for (idx, t) in U if idx == i]
    for t in U_i:
        log_pi_joint = (  flow_grpo_log_prob(π_θ, a[i,t]       | o_sim[i,t],        c)
                        + flow_grpo_log_prob(u_θ, o_hat[i,t+1] | o_sim[i,t], a[i,t], c))
        ρ = exp(log_pi_joint - log_pi_joint_old[i,t])       # PPO/GRPO probability ratio
        # WMPO asymmetric dual-clip: ε_low=0.20, ε_high=0.28 (favors exploration on +A)
        clip_term = clip(ρ, 1 - ε_low, 1 + ε_high) * A_uni[i,t]
        L_traj_i -= min(ρ * A_uni[i,t], clip_term)
    L_PS_uGRPO += L_traj_i / max(T_valid[i], 1)              # WoVR per-trajectory length norm
L_PS_uGRPO /= max(len(U_traj), 1)
# Note: no KL penalty — WMPO design (no reference model); LoRA + clip range bound drift.

# 7. MSE anchor with variable-length prefix AR (Eq. 12).
L_img_MSE = 0.0
for (i, j, t) in M_img:
    k = uniform_int(0, K_max)
    obs_context = o_sim[i,t] if k == 0 else θ.wm_rollout(o_sim[i,t-k], a[i,t-k:t])
    L_img_MSE += flow_matching_loss(θ.wm_predict(obs_context, a[i,t]), o_sim[i,t+1])
L_img_MSE /= max(len(M_img), 1)

# 8. LPIPS anchor (Eq. 13). Use single-Euler-step clean prediction at s≈0.9 (not full-inference o_hat) for gradient flow.
L_img_LPIPS = 0.0
for (i, _, t) in M_img:
    x_clean = single_euler_step(u_θ, o_sim[i,t], a[i,t], s=0.9)         # single-step clean latent
    L_img_LPIPS += LPIPS(Dec(x_clean), o_sim[i,t+1])                    # frozen Alex-lin LPIPS; flow-matching backbones
    # AR backbone analog: LPIPS(Dec(argmax p_θ(z|·)), o_sim[i,t+1]) with straight-through.
L_img_LPIPS /= max(len(M_img), 1)

# 9. DreamDojo TC anchor (Eq. 14). Inactive on single-frame backbones (K_lat = 1).
# x[i,t,k] = noised latent at frame k of the WM's video-chunk generation at env-step t.
# v_star[i,t,k] = encode(o_sim[i,t+k]) through backbone-VAE; then take finite-differences across k.
L_TC = 0.0
if K_lat > 1:
    for (i, _, t) in M_img:
        for k in range(1, K_lat):
            z_k, z_km1 = u_θ(x[i,t,k], k, c), u_θ(x[i,t,k-1], k-1, c)
            v_k, v_km1 = v_star[i,t,k],       v_star[i,t,k-1]
            L_TC += ||(z_k - z_km1) - (v_k - v_km1)||**2
    L_TC /= max(len(M_img) * (K_lat - 1), 1)

# 10. Full objective (Eq. 15).
L_total = L_PS_uGRPO + β_MSE * L_img_MSE + β_LPIPS * L_img_LPIPS + β_TC * L_TC
L_total.backward()
optimizer.step()

# 11. Periodic recalibration on sliding success window.
if round_n % RECAL == 0:
    recent_successes = [τ for τ in rollouts if env_success(τ) == 1]
    FIPER.refit_thresholds(recent_successes)   # τ_ACE, τ_RND
    PVM_ψ.fit(recent_successes)                # RISE value model
```

**Variant A** (full-`K` GRPO, not failure-focused): replace `U = F_pol ∪ M_img-proj` with $\mathcal{U} = \{1,\ldots,K\} \times \{0,\ldots,T-1\}$. Tests whether attribution-routed update outperforms standard GRPO at matched gradient steps.

**Hyperparameter defaults**:
- Reward weights: `w_T = 1.0`, `w_P = w_S = 0.3`; r^task sub-weights `λ_cur = 0.6` (EvoVLA's published intrinsic weight ρ from §3.2), `λ_smooth = 0.1` (CAPS action smoothness, small relative to PVM); r^phys sub-weight `λ_phys = 1.0` (WMReward V-JEPA 2 surprise); spatial sub-weights `λ_geo = 1.0`, `λ_CIoU = 0.5`.
- **GRPO clip + sampling defaults** (WMPO): `ε_low = 0.20`, `ε_high = 0.28` (asymmetric dual-clip); no KL term (no reference model); dynamic sampling filter active (drop all-collapse K-groups, resample). **Trajectory normalization** (WoVR): per-trajectory `1/T_valid_i` weighting in Eq. 11, where `T_valid_i` = up-to-first-success length.
- Anchor weights: `β_MSE = β_LPIPS = β_TC = 0.1` (RL dominates; three anchors provide dense gradient only).
- LoRA `r = 32, α_lora = 64`; LR `1e-4` (LoRA) / `1e-5` to `5e-6` (heads).
- Rollout: `K = 16–32` per batch; `H_kir ≈ T/8`; `K_max = 9` (prefix-AR depth, matches PRWM); `S_train = 10, S_infer = 40`.
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
| **Reward-term dropouts** — `w_T=0`, `w_P=0`, `w_S=0`, no-PVM, `λ_cur=0` (POE pose-curiosity off), `λ_smooth=0` (CAPS action-smoothness off), `λ_phys=0` (V-JEPA 2 surprise off) (7 runs) | C1c — each component's contribution to `r^uni`. Expected: `w_P=0` drops ≥3pp on contact-rich (V-JEPA 2 surprise drives imagination physics); `w_S=0` drops ≥3pp on spatial-perturbed; `w_T=0` collapses entirely; `λ_cur=0` slows long-horizon exploration; `λ_smooth=0` raises chatter / oscillation in policy actions; `λ_phys=0` allows imagination to drift toward physics-violating frames |
| **Sparse-reward ablation** — replace all per-step dense rewards with terminal-only task success (`r^uni_{i,t} = r_i · 𝟙[t=T-1]`) | Quantifies dense-reward contribution to the paper's headline claim (C1). Expected: ≥ 10pp drop on LIBERO-Long (aligns with [[2601.20218|DenseGRPO]] + [[2603.27866|Wan-R1]] findings on sparse-vs-dense for flow-matching RL) |
| **Attribution-routing variants** — FIPER AND-combined; sim-only attribution (no FIPER); Variant A (`U = full K × T`); **conservative thresholds (95th conformal percentile, FIPER's original default)** vs. our aggressive 60th-percentile setting | C2 — per-channel OR-union vs. AND, FIPER vs. sim-only, attribution-focus vs. full-GRPO, broad self-discovery vs. high-precision detection. Conservative-threshold run tests whether aggressive self-discovery hurts or helps |
| **Anchor dropouts** — `β_MSE=0`, `β_LPIPS=0`, `β_TC=0`, `K_max=0` (4 runs) | C4 + F4/F5 — per-head decoder collapse under RL-only (`β_MSE=0`); perceptual anchor effect (`β_LPIPS=0`); DreamDojo TC necessity (`β_TC=0`); prefix-AR necessity (`K_max=0`) |

### Novelty

Four contributions, each a falsifiable claim against a named prior-work target. The per-channel OR-union attribution, failure-focused update set `𝒰`, anchor losses, and shared-backbone co-evolution are *consequences* of the unified-GRPO formulation, not independent contributions.

| Contribution | Falsifiable claim | Prior-work target |
|---|---|---|
| **C1 — PS-uGRPO: unified physics-and-spatial-aware GRPO on policy + world-model** (Eq. 11, with joint log-prob Eq. 10 and unified reward Eq. 4) | **C1a**: at matched compute on LIBERO, PS-uGRPO beats asymmetric (RL-on-policy + supervised-on-WM) by ≥ 5 pp on LIBERO-Long (physics reward drives long-horizon stability). **C1b**: on spatial-perturbed LIBERO, PS-uGRPO beats asymmetric by ≥ 5 pp (spatial reward drives geometric robustness). **C1c**: removing either `r^phys` (Eq. 6) or `r^spatial` (Eq. 7) degrades the respective axis by ≥ 3 pp — verifies component-level credit attribution | No prior work runs unified GRPO on both heads of a unified WAM backbone with disjoint-family physics signals. [[2511.09515\|WMPO]]: RL on policy only. [[2602.00743\|SA-VLA]]: spatial rewards but supervised-only L_img. [[2511.07403\|SpatialThinker]]: GRPO with spatial rewards on MLLMs, not VLAs |
| **C2 — Per-channel OR-union attribution routing** — RND-OE → WM-caused failure, ACE → policy-caused failure; union forms attribution set `𝒰` (Eq. 11) | **C2a**: per-channel OR-union has higher attribution precision than FIPER's AND-combined detector. **C2b**: FIPER-enabled beats FIPER-disabled (sim-only attribution) by ≥ 3 pp on attribution precision or downstream success. If C2b fails, FIPER is dropped and `𝒰` becomes sim-only — still valid but weaker | [[2510.09459\|FIPER]] paper recommends AND for detection; reference code supports both AND and OR (`operation` flag) + per-channel thresholds — we pick OR + aggressive thresholds for attribution + broad self-discovery. No prior work validates this configuration for cause attribution |
| **C3 — PS-uGRPO beats no-WM residual RL on sample efficiency / OOD transfer** | **C3a**: on LIBERO, our method reaches 90% with ≤ 50% of [[2511.00091\|PLD]]'s rollouts. **C3b**: on held-out OOD tasks, our transfer exceeds PLD's by ≥ 10 pp | [[2511.00091\|PLD]] hits 99% LIBERO *without any WM*. If C3a+C3b both fail, the WM (and therefore `r^phys` + `r^spatial` from imagined frames) is dead weight; paper reframes as "attribution-gated sim-SFT with task reward only" |
| **C4 — UWM's distinct decoders make per-head gradient asymmetry empirically observable** | Under anchor-free PS-uGRPO (`β_MSE = β_LPIPS = β_TC = 0` on both UWM and Cosmos Policy under default configs $K_{\text{lat}} \approx 8$ and $\geq 4$ respectively), $\|\nabla_\theta L_{\text{PS-uGRPO}}\|_{\text{action decoder}} / \|\nabla_\theta L_{\text{PS-uGRPO}}\|_{\text{patch decoder}}$ diverges monotonically over training rounds on UWM. Anchor losses bound the ratio: MSE + LPIPS + TC on both. **Decoder-collapse diagnostic**: direct empirical evidence for "anchors are necessary" | No prior work measures this ratio on [[2504.02792\|UWM]] — novel diagnostic, hinges on UWM's structural asymmetry (2-Linear+Mish action decoder vs. 1-Linear patch decoder). Cosmos's single denoiser cannot host this test |

## Backbones

### Summary

| Backbone | Pure PS-uGRPO (no anchors) suffices? | Needs anchors (Eqs. 12, 13, 14)? | What to ablate |
|---|---|---|---|
| [[2601.16163\|Cosmos-Policy]] | ✓ (single denoiser → automatic imag-policy *alignment* under shared RL gradient) | Optional — sharpens imagination *fidelity* | `β_MSE = β_LPIPS = 0` vs. defaults; FVD on held-out benchmark decoupled from task reward |
| [[2504.02792\|UWM]] | ✗ — patch decoder cut off from direct policy gradient; WM receives only the weaker log `u_θ` signal; DiT body still updates via shared self-attention | **Required** for sharp image decoding (C4) | Per-head gradient-norm ratio (C4); `β_MSE = 0` vs. `β_MSE = 0.1` image-decoder FVD; per-head frozen-weight ablation |

#### Cosmos Policy — detailed plan

Cosmos Policy is a single denoiser over all modalities (proprio, actions, value, multi-view images) injected as latent frames — no separate action/image heads. RL-only gradient therefore updates imagination parameters as a side effect of the action gradient through shared θ. Reward / steps-to-go are added as additional latent-frame modalities.

| Imagination gain | Under PS-uGRPO alone | Needs anchors (Eqs. 12, 13, 14)? |
|---|---|---|
| **Imag-policy alignment** (WM future matches policy distribution) | ✓ Free — shared weights | no |
| **Imag fidelity** (prediction matches physical reality, low FVD/SSIM) | ✗ Sparse RL may degrade it | yes |

Single-denoiser blends fidelity and alignment; defend by setting `β_MSE = β_LPIPS = 0` in one run and measuring FVD/SSIM on an imagination benchmark decoupled from task reward.

#### UWM — detailed plan

[[2504.02792|UWM]] shares DiT body + AdaLN final layer; splits only at the output projection (2-Linear+Mish action decoder vs. 1-Linear patch decoder). Under PS-uGRPO alone, the patch decoder receives only the weaker `log u_θ` gradient — symptom: asymmetric per-head gradient norms + drifting image fidelity. MSE + LPIPS + TC anchors restore patch-decoder gradient and rebalance the body update; UWM's default config ($K_{\text{lat}} \approx 8$) keeps TC active. Distinct decoders make per-head frozen-weight ablations feasible — the C4 diagnostic (gradient-norm ratio, FVD) is the thesis advantage, infeasible on Cosmos's single denoiser. Pilot on UWM first; Cosmos Policy follows as second-backbone validation.

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

**Mechanism transferability** — flow-matching RL is domain-independent: [[2505.05470|Flow-GRPO]] (SD3.5-M, r=32/α=64), [[2510.09976|FPO-Lyu]] (87.2% LIBERO on π₀, CFM-likelihood-free PPO), [[2505.22094|ReinFlow]] (learnable noise injection alternative to ODE→SDE), [[2507.21053|FPO-Berkeley]] (independent CFM-likelihood-free precedent).


## Sim-to-Real Gap

The three anchor losses (Eqs. 12, 13, 14) supervise the WM against sim's `o^sim_{t+1}`; PS-uGRPO's physics and spatial rewards (Eqs. 6, 7) are computed on WAM imagined frames — D_phys via frozen V-JEPA 2 (manipulation-relevant prior from V-JEPA 2's pretraining); bbox extractors reference sim. The WM therefore learns **sim physics**, not real physics.

**Policy sim-to-real** and **FIPER sim-to-real** are in scope (standard — policy via domain randomization per [[2601.16163|Cosmos-Policy]] / [[2511.09515|WMPO]]; FIPER via real-rollout threshold re-fit per [[2510.09459|FIPER]]'s own demonstration). **WM sim-to-real is out of scope** — the WM is sim-fit and stays behind at deployment; imagination-based planning on real robots requires a separate real-corpus WM fine-tune (DROID, AgiBot) in a follow-up paper.

**Deployment recipe**: ship (policy + FIPER) to the real robot; discard the WM unless a follow-up real-corpus fine-tune is run. The WM is a training-time scaffold — consumed by PS-uGRPO (Eq. 11) and all three anchors (Eqs. 12, 13, 14) during sim training only.

## Excluded

Papers / mechanisms the proposal does not use, and why.

### Demo / human-in-loop / LLM dependent

| Excluded | Why |
|---|---|
| [[2509.15155\|Self-Improving-EFM]] steps-to-go | Requires SFT demos |
| [[2511.15605\|SRPO]] latent clusters | Cluster fit needs demo successes (V-JEPA-2 distance retained as deployment-fallback reward only) |
| [[2511.16166\|EvoVLA]] SAR | CLIP + Gemini hard negatives — LLM-dependent. We adopt **POE faithfully** (pose-curiosity); skip Long-Horizon Memory (system-architectural) |
| [[2603.23376\|ABot-PhysWorld]] | LLM-tainted at every stage (Qwen3-VL captions, Qwen3-VL + Gemini 3 Pro DPO triplets, Qwen2.5-VL-72B PBench). Replaced by [[2601.10553\|WMReward]] V-JEPA 2 surprise |
| [[2602.12099\|GigaBrain-0.5M*]] | HIL rollouts require human-in-loop correction |

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
