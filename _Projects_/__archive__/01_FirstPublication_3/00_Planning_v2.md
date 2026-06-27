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
> **Sim-based self-evolving WAM via single-stage cooperative-RL: PS-uGRPO + RoboMD-modified-to-GRPO failure-finder.** A pretrained unified WAM (Cosmos Policy / UWM) is fine-tuned via LoRA under a **single unified GRPO loop on the joint (action, imagination) log-prob**, driven by a task + physics + spatial reward (Eq. 1). A small failure-finder network ([[2412.02818|RoboMD]]-modified-to-GRPO) actively selects hard perturbations from a hand-coded XML bank; both networks update concurrently in one optimizer step per round. The Cosmos base $\theta_{\text{base}}$ stays FROZEN throughout — dual-purpose: body for LoRA adapters AND encoder feeding the failure-finder. MSE (variable-length prefix AR), LPIPS, and DreamDojo TC serve as dense anchors. No task-specific demonstrations required. Primary pilot backbones: [[2504.02792|UWM]] and [[2601.16163|Cosmos-Policy]].

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
| 6 | 4.3 | [[2602.11075\|RISE]] | [OpenDriveLab/RISE](https://github.com/OpenDriveLab/RISE) | Compositional WM: Dynamics + Progress Value Model; online RL in imagination | ✗ (WM + PVM frozen during loop) | ✓ online RL on imagined rollouts | NO — WM frozen during loop |
| 7 | 4.2 | [[2603.19370\|VAMPO]] | [OpenHelix-Team/VAMPO](https://github.com/OpenHelix-Team/VAMPO) | Video Prediction Model (GRPO over denoising-as-MDP; latent-consistency reward) | ≈ unified VPM is the policy | ✓ GRPO over denoising | Ambiguous — unified VPM |
| 8 | 4.2 | [[2412.02818\|RoboMD]] | [riteshkanchi/RoboMD](https://github.com/riteshkanchi/RoboMD) | Active failure-search via PPO over learned ViT+CLIP semantic-failure embedding; argmin to discrete XML perturbation bank. **Stacked: modified to GRPO + frozen-base encoder + concurrent training (Eq. 9)** | N/A (curriculum generator) | N/A (curriculum generator) | NO — outer-loop perturbation curriculum |
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

Given a pretrained unified-backbone WAM ([[2601.16163|Cosmos-Policy]] or [[2504.02792|UWM]]) and a simulator with next-state + success ground truth, the backbone's policy and world-model **co-evolve through a single GRPO loop** (PS-uGRPO, Eq. 8) whose reward combines task, physics, and spatial signals. Three dense anchors — MSE with prefix-AR (Eq. 10), LPIPS (Eq. 11), DreamDojo TC (Eq. 12) — supply the per-pixel and per-velocity gradient that scalar RL cannot.

**Active failure-search** — a small failure-finder network $\theta_{\text{finder}}$ ([[2412.02818|RoboMD]]-modified-to-GRPO) selects which sim perturbation to deploy each round: continuous action over an embedding manifold (frozen $\theta_{\text{base}}$); argmin to the nearest XML edit anchor in bank $B$ realizes the perturbation in MuJoCo. Reward is the **regret-aligned** signal $r^{\text{finder}}_j = -\bar r^{\text{uni}}_j + \lambda_\sigma \cdot \overline{|A^{\text{uni}}|}_j$ (Eq. 9): (a) **currency-aligned** with PS-uGRPO — surfaces physics/spatial failures, not just task-incompletion; (b) **learning-signal aware** (mean absolute PS-uGRPO advantage — ACCEL/PAIRED regret) — avoids the all-fail-uniform trap where group advantages collapse. Full $K \times T$ rollout enters the PS-uGRPO update; group-relative advantage in Eq. 5 implicitly down-weights solved rollouts.

**Unified gradient** — PS-uGRPO's signed advantage on the joint (action, imagination) log-prob pushes $\theta_{\text{lora}}$ toward high-advantage rollouts and away from low-advantage ones; anchor losses apply on the full batch. The failure-finder loss $\alpha \cdot L_{\text{finder}}$ enters the same backward pass on $\theta_{\text{finder}}$. Single $L_{\text{total}}\text{.backward()}$ + single $\text{optimizer.step()}$ per round updates **both** trainable components; $\theta_{\text{base}}$ stays frozen — architectural co-evolution via cooperative-RL, not three-stage orchestration.

**Multi-round iteration** — each round, the failure-finder selects perturbations, Cosmos rolls out, both networks update concurrently. Periodic PVM recalibration on fresh successes (§Algorithm step 10).

**Deployment portability (policy only, not the WM or failure-finder)** — only the deployed policy (Cosmos $\theta_{\text{base}}$ + LoRA $\theta_{\text{lora}}$, fused) transfers to real-robot deployment. The **WM does not transfer**: its rewards (`r^phys`, `r^spatial`) and anchors (MSE, LPIPS) all reference sim, so it learns sim physics. The **failure-finder does not transfer**: its perturbation bank is sim-only XML edits. WM-as-deployment-imagination requires a separate real-corpus fine-tune — see §Sim-to-Real Gap.

> [!warning] Cold-start protocol
>
> Round 0 runs $K$ rollouts through pure sim verification. **Backbone precondition**: ≥ 5–10% Round-0 zero-shot success. PVM refit every `RECAL` rounds on the sliding success window (§Algorithm step 10).
>
> **Pre-Round-0 one-time calibration** (sim rollouts + sim oracle only — same dependency tier as the simulator; no demos, no LLM, no human labels):
> - **Progress reward** ([[2511.15605|SRPO]] over [[2506.09985|V-JEPA-2]] ViT-g — same encoder as $D_{\text{phys}}$, no extra dependency): DBSCAN-cluster successful trajectories' V-JEPA 2 latents (density-based, no fixed $k$); per-trajectory reward $V^{\text{SRPO}}(\tau_i) = 1 - (d_i - d_{\min})/(d_{\max} - d_{\min}) \in [0,1]$ with $d_i = \min_k \|z_{\tau_i} - z^{\text{cent}}_k\|_2$, broadcast to all $T$ steps. Cold-start threshold: ≥ 1 success per batch (DBSCAN `min_samples`). One frozen V-JEPA 2 serves two reward channels: per-frame physics (Eq. 3) + per-trajectory progress (Eq. 2).
> - **POE forward-dynamics model $\hat{f}_{\text{fwd}}$** ([[2511.16166|EvoVLA]] / [[1705.05363|ICM]]): small MLP on sim transitions $(z_t, a_t, z_{t+1})$ with pose features $z = \psi(T_{\text{ee}}^{-1} T_{\text{obj}})$; ~10k random-action rollouts, MSE loss (~minutes on CPU).
> - **V-JEPA 2 surprise scorer** ([[2601.10553|WMReward]] over [[2506.09985|V-JEPA-2]] ViT-g, ~1B, MIT) + **LPIPS Alex-lin** (frozen): both pretrained, plug-and-play.
> - **LoRA setup**: freeze Cosmos base $\theta_{\text{base}}$; initialize LoRA adapters $\theta_{\text{lora}}$ ($r=32$, $\alpha_{\text{lora}}=64$) on attention Q/K/V/O + FFN up/down per §LoRA strategy.
> - **Hand-coded XML perturbation bank** ([[2412.02818|RoboMD]]-inspired): 14–19 edits per LIBERO task variant (RoboMD-counted: lift=16, stack=16, square=14, can=19, thread=14; cube/object color, table size, lighting, robot color, etc.). One-time engineering, ~few hundred lines.
> - **Pre-compute perturbation anchor embeddings $B$**: under FROZEN $\theta_{\text{base}}$ (which never changes after this point), encode each XML edit's resulting scene → 512-d anchor; store as bank $B = \{e_1, \ldots, e_M\}$. One-shot, no refresh needed (since $\theta_{\text{base}}$ is permanently frozen by the LoRA design).
> - **Failure-finder GRPO initialization**: random init at Round 0 (no pretraining); embedding source = frozen $\theta_{\text{base}}$ body. **Cold-start guards**: (a) **warm-up phase** — for the first $N_{\text{warmup}}$ rounds (default 20), force uniform-random selection across bank $B$, then switch to learned selection (ACCEL-style guard against premature commitment); (b) **entropy bonus** on $\pi_{\text{finder}}$ (weight $\eta_{\text{ent}} \approx 0.01$, decay to 0 by round ~100). No separate embedding-model training — frozen $\theta_{\text{base}}$ is the encoder.
> - **No IDM needed**: physics signal is the frozen-JEPA residual ($D_{\text{phys}}$); avoids the architectural-prior-sharing reward-hacking risk of learned-IDM critics co-evolving with a same-family policy.
>
> **Caveats**: (i) Progress reward needs ≥ DBSCAN `min_samples` successes per batch (default 5) before a centroid forms; until then $V^{\text{SRPO}} \equiv 0$ and PS-uGRPO relies on $r^{\text{phys}} + r^{\text{spatial}}$ alone; (ii) $D_{\text{phys}}$ uninformative on near-random imagined frames until imagination stabilizes; (iii) failure-finder learning rate ~10× slower than PS-uGRPO's to mitigate non-stationarity.

### Mechanism synthesis

Ten mechanisms compose PS-uGRPO + three anchor sources + RoboMD-modified failure-finder (Eq. 13, derived in §Mathematics); five related mechanisms are considered and rejected or reserved for deployment.

**Stacked (11 + 3 anchors)** — each contributes a specific term of Eq. 13:

| Paper | Contribution (what we take) | Target term | What we skip |
|---|---|---|---|
| [[2511.09515\|WMPO]] | (i) GRPO-in-imagination compute graph; K joint rollouts per batch — PS-uGRPO scaffolding; (ii) **asymmetric dual-clip** `ε_low=0.20, ε_high=0.28`; (iii) **no-KL** (DAPO-style: memory + exploration); (iv) **dynamic sampling filter** (drop all-success / all-fail K-groups) | PS-uGRPO + failure-finder scaffolding + clip + sampling refinements (Eqs. 8, 9) | Outer lifelong WM fine-tune; VideoMAE reward model (we use V-JEPA 2 surprise + sim oracle) |
| [[2505.05470\|Flow-GRPO]] | ODE→SDE conversion (image-only in source); denoising reduction | $\log \pi_\theta$, $\log u_\theta$ (Eq. 7); we extend to both heads | Image-gen benchmarks |
| [[2412.02818\|RoboMD]] | (i) Continuous-embedding active failure-search; (ii) hand-coded XML perturbation bank per task; (iii) argmin quantization from continuous latent → discrete edit | `α · L_finder` (Eq. 9) + outer-loop perturbation curriculum (§Algorithm step 0.5) | (i) PPO → **GRPO** with WMPO refinements (asymmetric dual-clip, no-KL, dynamic sampling); (ii) Discover→Summarize→Restructure 3-stage pipeline → **concurrent updates per round**; (iii) Separately-trained ViT+CLIP contrastive embedding → **frozen Cosmos $\theta_{\text{base}}$ as encoder** (saves ~hours of cold-start; LoRA's frozen-base structure provides permanent stability); (iv) Binary `1 − task_success` reward → **regret-aligned reward** $-\bar r^{\text{uni}}_j + \lambda_\sigma \cdot \overline{\|A^{\text{uni}}\|}_j$ (currency-aligned with PS-uGRPO + ACCEL/PAIRED-style learning-signal — surfaces physics/spatial failures and avoids all-collapse perturbations) |
| [[2602.13977\|WoVR]] | **Trajectory-length normalization** `1/T_valid_i` (WoVR paper Eq. 11) — gives short successful trajectories proportional credit | `1/T_valid_i` weighting in Eq. 8 | KIR keyframe-init rollouts (group-relative advantage subsumes); PACE (shared-θ subsumes); dual-channel action injection / first-frame anchoring (backbone-provided) |
| [[2511.15605\|SRPO]] | DBSCAN over V-JEPA 2 trajectory latents + inverse-L2 to nearest centroid (LIBERO 99.2%, SRPO-validated). **Anti-hacking property** (our derivation): trajectory-level reference comparison — distortions move away from successful clusters → low reward. Same **family** as [[2510.00406\|VLA-RFT]]'s verified-reward pattern (different references: own-batch successes vs. WM goal-rollouts). Caveat: a coordinated distortion could land near a centroid while violating physics — bounded, not zero | $V^{\text{SRPO}}$ in `r^task` (Eq. 2) | (i) z-score + $\phi$ activation → min-max-normalized $[0,1]$ (our adaptation); (ii) one-shot SFT base init (we use Cosmos pretrained); (iii) ImageBind alternative scorer |
| [[2509.20570\|PIRF]] | Decoder-restricted gradient routing for physics rewards | Gradient routing on `r^phys` (Eq. 3) | PDE-residual reward (we use V-JEPA 2 surprise); resolution-stratified U-Net layer selection (we use VAE-decoder + final-N DiT blocks heuristic — DiT trunks are single-resolution) |
| [[2511.16166\|EvoVLA]] | POE pose-grounded curiosity (forward-dynamics prediction error on relative gripper-to-object pose); [[1705.05363\|ICM]] is the canonical underlying method | `λ_cur · r^cur` (Eq. 2) | SAR (CLIP + Gemini hard negatives — LLM-dependent), Long-Horizon Memory (system-architectural) |
| [[2012.06644\|CAPS]] | 1st-order temporal action-smoothness regularizer; ICRA 2021 canonical reference. [[2210.13702\|DeXtreme]] action-delta penalty as manipulation corroboration | `λ_smooth · S_act` in `r^task` (Eq. 2) — folded into task component as action-quality penalty | Spatial smoothness term, direct policy regularization (we use temporal only, route through GRPO advantage) |
| [[2601.10553\|WMReward]] (over [[2506.09985\|V-JEPA-2]] ViT-g) | Frozen V-JEPA 2 surprise score on adjacent imagined frames; ~1B, MIT, no LLM, no fine-tuning; SOTA PhysicsIQ (62.0%) | `λ_phys · D_phys` in `r^phys` (Eq. 3) — object-state physics axis | Best-of-N video selection (their use); we route the scalar into GRPO advantage |
| [[2602.06949\|DreamDojo]] | Velocity-change TC loss (DreamDojo's Eq. 4), over $K_{\text{lat}}$ latent frames per video chunk | `β_TC · L^TC` (Eq. 12). Active on multi-latent-frame backbones: UWM default config $K_{\text{lat}} \approx 8$ (17 future frames + temporal-patch-2); Cosmos Wan2.1 4:1 → $K_{\text{lat}} \geq 4$. Inactive only on $K_{\text{lat}}=1$ configs | Relative-action conditioning + chunked injection (backbone-provided) |
| [[2602.00743\|SA-VLA]] | Phase-conditioned signed geometric reward (Reach/Place/Leave) | `λ_geo · Δ_geo(phase)` in `r^spatial` (Eq. 4) | SCAN annealed-noise (Flow-GRPO's SDE subsumes) |
| [[2511.07403\|SpatialThinker]] | CIoU bbox-alignment reward | `λ_CIoU · CIoU(bbox)` in `r^spatial` | STVQA-7K dataset (sim bboxes replace) |
| [[2603.25685\|Persistent-Robot-WMs]] | Variable-length-prefix AR training (F4 mitigation) | `L_img^flow-prefix` (Eq. 10) — essential dense anchor | Reward-contrasted denoising (PS-uGRPO subsumes with richer reward) |
| [[1801.03924\|LPIPS]] | Perceptual anchor (partial F5 mitigation) | `β_LPIPS · L_img^LPIPS` (Eq. 11) | Extensive backbone fine-tuning (paper warns against; Alex-lin frozen) |

**Alternatives / deployment-only (5)** — noted for completeness, not in the stack. Each row has a distinct reason for exclusion (not just "alt reward"):

| Paper | Role | Why not stacked |
|---|---|---|
| [[2602.21633\|SC-VLA]] | Sparse World Imagination = auxiliary progress-prediction heads + reward reshaping | Not an initial-state sampler (paper's SPI = *Sparse Predictive Imagination*, not *Sparse-imagination Preferential*); progress-prediction role is redundant with RISE's PVM |
| [[2511.07732\|ViPRA]] | Pretraining choice (pre-Round-0 backbone) | Not in the loop; flow-matching decoder adaptation is superseded by Flow-GRPO |
| [[2510.00406\|VLA-RFT]] | GRPO with pixel+LPIPS verified reward inside a **frozen** WM simulator | **Role mismatch**: VLA-RFT freezes the WM and RLs the policy inside it; we co-train the WM via PS-uGRPO. Also **LPIPS role mismatch**: they use it as a reward; we use it as a dense anchor loss (Eq. 11) |
| [[2603.19370\|VAMPO]] | Denoising-as-MDP with latent-consistency reward | **Mechanism supersession**: VAMPO's denoising-step MDP is subsumed by our Flow-GRPO ODE→SDE at the environment level; composing both would double-wrap RL (MDP-within-MDP) |

**Stacking order**: PS-uGRPO core (Eq. 8: WMPO + Flow-GRPO + WoVR length-norm) → compose `r^uni` (Eq. 1: task + physics + spatial) → add failure-finder GRPO (Eq. 9: RoboMD-modified) → add three anchors (Eqs. 10, 11, 12). Component credit in §Baselines ablations. **WMPO-specific deviations** (sim rollouts vs. imagined; unified `r^uni` vs. binary success; joint-log-prob GRPO vs. policy-only; per-step anchors vs. outer WM fine-tune) are made explicit in the WMPO row above and Eq. 8.

### Mathematics

**TL;DR**: $L_{\text{total}}(\theta) = L_{\text{PS-uGRPO}} + \alpha \cdot L_{\text{finder}} + \beta_{\text{MSE}} \cdot L^{\text{flow-prefix}} + \beta_{\text{LPIPS}} \cdot L^{\text{LPIPS}} + \beta_{\text{TC}} \cdot L^{\text{TC}}$. **Single-stage cooperative-RL**: PS-uGRPO trains LoRA $\theta_{\text{lora}}$ via joint (action, imagination) GRPO on $r^{\text{uni}}$ (task + physics + spatial); failure-finder $\theta_{\text{finder}}$ (RoboMD-modified-to-GRPO) selects perturbations from a hand-coded XML bank; three dense anchors prevent decoder collapse. Both update concurrently; $\theta_{\text{base}}$ frozen, dual-purpose (LoRA body + finder encoder). Equations 1–13 follow; symbols in §Notation.

**Unified reward** — task + physics + spatial (Eq. 1):

$$
r^{\text{uni}}_{i,t} \;=\; w_T \cdot r^{\text{task}}_{i,t} \;+\; w_P \cdot r^{\text{phys}}_{i,t} \;+\; w_S \cdot r^{\text{spatial}}_{i,t} \tag{1}
$$

Each component defined below, used directly from its source paper.

**Task component** — trajectory progress + pose-grounded curiosity + action quality (Eq. 2; [[2511.15605|SRPO]] progress + [[2511.16166|EvoVLA]] POE + [[2012.06644|CAPS]] action smoothness):

$$
r^{\text{task}}_{i,t} = V^{\text{SRPO}}(\tau_i) + \lambda_{\text{cur}} \cdot r^{\text{cur}}_{i,t} - \lambda_{\text{smooth}} \cdot S_{\text{act}}(a_{i, t-1:t+1}) \tag{2}
$$

$V^{\text{SRPO}}(\tau_i) = 1 - (d_i - d_{\min})/(d_{\max} - d_{\min}) \in [0,1]$ with $d_i = \min_k \|z_{\tau_i} - z^{\text{cent}}_k\|_2$. $z_{\tau_i} = E_\theta(\tau_i)$ is the V-JEPA 2 ViT-g trajectory latent (reuses Eq. 3's frozen encoder); centers $\{z^{\text{cent}}_k\}$ are batch-internal DBSCAN over successful-trajectory latents (density-based, no fixed $k$). SRPO-original normalizes via z-score + activation $\phi$; we use min-max for bounded $[0,1]$ output. Reward broadcast to all $T$ steps. $r^{\text{cur}}_{i,t} = \tfrac{\eta}{2}\|\mathrm{sg}(\hat{f}_{\text{fwd}}(z_{i,t}, a_{i,t})) - z_{i,t+1}\|^2$ on pose features $z_t = \psi(T_{\text{ee}}^{-1} T_{\text{obj}}) \in \mathbb{R}^6$ (stop-gradient on prediction prevents policy from gaming curiosity, per EvoVLA Eq. 7 — non-standard ICM); $S_{\text{act}} = \|a_{i,t} - a_{i,t-1}\|_2$ (1st-order CAPS).

**Physics component** — V-JEPA 2 surprise residual on WAM imagined output (Eq. 3; [[2601.10553|WMReward]]):

$$
r^{\text{phys}}_{i,t} = \lambda_{\text{phys}} \cdot D_{\text{phys}}(\hat{o}_{i,t}, \hat{o}_{i,t+1}) \tag{3}
$$

**WMReward V-JEPA 2 surprise**: $D_{\text{phys}} = \tfrac{1}{2}(1 + \cos(P_\phi(E_\theta(\hat{o}_{i, t-C+1:t})), E_\theta(\hat{o}_{i,t+1}))) \in [0, 1]$ (rescaling of WMReward's $1-\cos$ loss; context $C = 8$ per WMReward Table 7), frozen V-JEPA 2 ViT-g $(E_\theta, P_\phi)$ (~1B). Catches imagined object-state failures (penetration, anti-gravity, permanence). **Decoder-restricted gradient routing**: $r^{\text{phys}}$ gradient flows only to the VAE decoder + final-N DiT blocks. PIRF-original is U-Net-resolution-stratified; we use a decoder-restricted heuristic for DiT, ablated `OFF` in §Baselines.

**Spatial component** — phase-geometric + bbox alignment on WAM imagined frames (Eq. 4; [[2602.00743|SA-VLA]] + [[2511.07403|SpatialThinker]]):

$$
r^{\text{spatial}}_{i,t} = \lambda_{\text{geo}} \cdot \Delta_{\text{geo}}\bigl(\text{phase}_t\bigr) + \lambda_{\text{CIoU}} \cdot \mathrm{CIoU}\bigl(\mathrm{bbox}(\hat{o}_{i,t+1}),\, \mathrm{bbox}(o^{\text{sim}}_{i,t+1})\bigr) \tag{4}
$$

**SA-VLA phase-geometric**: SA-VLA Eqs. 8–10 define per-phase signed temporal differences in normalized distances — Reach: $d^{\text{ro}}_{t-1} - d^{\text{ro}}_t$; Place: $d^{\text{od}}_{t-1} - d^{\text{od}}_t$; Leave: $d^{\text{ro}}_t - d^{\text{ro}}_{t-1}$. We aggregate these into a single signed scalar $\Delta_{\text{geo}}(\text{phase}_t)$ (our notation; SA-VLA keeps the per-phase rewards separate). **SpatialThinker CIoU**: on imagined vs. sim bboxes; SpatialThinker's CIoU is already $\in [0,1]$, used directly without rescaling.

**Group-relative advantage** on unified reward — Eq. 5:

$$
\mu_t = \tfrac{1}{K}\textstyle\sum_i r^{\text{uni}}_{i,t}, \quad \sigma_t = \sqrt{\tfrac{1}{K}\textstyle\sum_i (r^{\text{uni}}_{i,t} - \mu_t)^2}, \quad A^{\text{uni}}_{i,t} = \frac{r^{\text{uni}}_{i,t} - \mu_t}{\sigma_t + \epsilon_{\text{num}}} \tag{5}
$$

**Flow-GRPO SDE** — Flow-GRPO ([[2505.05470|Flow-GRPO]]) demonstrates ODE→SDE for image-only flow-matching; we extend it to both heads (Eq. 6). Action head via $v_\theta$; WM head via $u_\theta$ (same form with substituted variables):

$$
da_s = \bigl[ v_\theta(a_s;\, o_{i,t}, c) + \tfrac{\sigma_{\text{flow}}^2(s)}{2} \nabla_{a_s} \log p_s(a_s) \bigr] ds + \sigma_{\text{flow}}(s)\, dW_s \tag{6}
$$

Denoising reduction: $S_{\text{train}}=10 \ll S_{\text{infer}}=40$ (Flow-GRPO's SD3.5-M settings) gives ~4× rollout speedup at no inference-quality cost.

**Joint log-prob factorization** — Eq. 7. UWM: independent timesteps $(t_a, t_{o'})$ → exact conditional-independence factorization. Cosmos: shared timestep → logical regrouping of the packed-sequence log-prob aligned to $r^{\text{uni}}$'s channels.

$$
\log \pi_\theta^{\text{joint}}(a_{i,t},\, \hat{o}_{i,t+1} \mid o_{i,t}, c) = \log \pi_\theta(a_{i,t} \mid o_{i,t}, c) + \log u_\theta(\hat{o}_{i,t+1} \mid o_{i,t}, a_{i,t}, c) \tag{7}
$$

For AR-token backbones ([[2506.19850|UniVLA]], [[2506.21539|WorldVLA]]), replace $\log u_\theta$ with the AR-token log-prob $\sum_k \log p_\theta(z^{(k)}_{i,t+1} \mid \cdots)$ — factorization still holds.

**PS-uGRPO — unified Physics-Spatial GRPO loss** (Eq. 8), trains LoRA adapters $\theta_{\text{lora}}$ on Cosmos / UWM (base $\theta_{\text{base}}$ frozen). With **WoVR** trajectory-length normalization and **WMPO** asymmetric dual-clip:

$$
L_{\text{PS-uGRPO}}(\theta_{\text{lora}}) = -\frac{1}{K} \sum_{i=1}^{K} \frac{1}{T^{\text{valid}}_i} \sum_{t=0}^{T-1} \min\bigl(\rho_{i,t} A^{\text{uni}}_{i,t},\ \mathrm{clip}(\rho_{i,t}, 1 - \varepsilon_{\text{low}}, 1 + \varepsilon_{\text{high}}) A^{\text{uni}}_{i,t}\bigr) \tag{8}
$$

Outer sum over **all $K$ rollouts**, inner over **all $T$ steps**. **Inherited refinements** (see §Mechanism synthesis): [[2602.13977|WoVR]] $1/T^{\text{valid}}_i$ length-norm; [[2511.09515|WMPO]] asymmetric dual-clip ($\varepsilon_{\text{low}}=0.20, \varepsilon_{\text{high}}=0.28$) + no-KL + dynamic sampling (extends WMPO's binary filter to dense rewards; §Algorithm step 1.5).

**Failure-finder GRPO** (Eq. 9) — small RL network $\theta_{\text{finder}}$ that selects perturbations from a hand-coded XML bank, modified from [[2412.02818|RoboMD]] (PPO → GRPO):

$$
L_{\text{finder}}(\theta_{\text{finder}}) = -\frac{1}{K_{\text{finder}}} \sum_{j=1}^{K_{\text{finder}}} \min\bigl(\rho_j A^{\text{fail}}_j,\ \mathrm{clip}(\rho_j, 1 - \varepsilon_{\text{low}}, 1 + \varepsilon_{\text{high}}) A^{\text{fail}}_j\bigr) - \eta_{\text{ent}} \cdot \mathcal{H}\bigl(\pi_{\text{finder}}(\cdot \mid h)\bigr) \tag{9}
$$

with **regret-aligned reward**:

$$r^{\text{finder}}_j = \underbrace{- \bar r^{\text{uni}}_j}_{\text{(a) currency-aligned}} + \lambda_\sigma \cdot \underbrace{\overline{|A^{\text{uni}}|}_j}_{\text{(b) learning-signal}}, \quad \bar r^{\text{uni}}_j = \frac{1}{KT}\sum_{i,t} r^{\text{uni}}_{j,i,t}, \quad \overline{|A^{\text{uni}}|}_j = \frac{1}{KT}\sum_{i,t} |A^{\text{uni}}_{j,i,t}|$$

$A^{\text{fail}}_j = (r^{\text{finder}}_j - \mu_G) / (\sigma_G + \epsilon_{\text{num}})$ — group-relative advantage over $K_{\text{finder}}$ perturbations. **Two reward terms**: (a) **currency-alignment** with PS-uGRPO — surfaces physics/spatial failures, not just task-incompletion; (b) **regret-style learning-signal** (ACCEL/PAIRED) — rewards mean-absolute PS-uGRPO advantage, avoids the all-fail-uniform trap where group advantages collapse to zero.

**MSE anchor with variable-length prefix AR** — F4 mitigation (Eq. 10, flow-matching):

$$
L_{\text{img}}^{\text{flow-prefix}}(\theta) = \mathbb{E}_{k \sim \mathcal{U}[0, K_{\max}]} \, \frac{1}{KT} \sum_{i=1}^{K}\sum_{t=0}^{T-1} \mathbb{E}_{s, \varepsilon} \bigl[\, \|u_\theta(x_s;\, \tilde{o}_{i,t-k:t}, a_{i,t}, s) - v^\ast(o^{\text{sim}}_{i,t+1})\|^2 \,\bigr] \tag{10}
$$

$\tilde{o}_{i,t-k:t}$ = WAM's free-rolled obs ($k=0$ ground-truth, $k=K_{\max}$ fully imagined) — interpolates teacher-forced and free-rollout, eliminating exposure bias. Sum runs over the full batch (no $M_{\text{img}}$ filter). AR-backbone analog: token CE with VQ targets.

**LPIPS perceptual anchor** — F5 partial mitigation (Eq. 11):

$$
L_{\text{img}}^{\text{LPIPS}}(\theta) = \frac{1}{KT} \sum_{i=1}^{K}\sum_{t=0}^{T-1} \mathrm{LPIPS}\bigl(\mathrm{Dec}(\hat{x}^{\text{clean}}_{i,t+1}),\, o^{\text{sim}}_{i,t+1}\bigr) \tag{11}
$$

**Decode**: flow-matching uses single-Euler-step at $s \approx 0.9$ + frozen-VAE decode (per [[2510.00406|VLA-RFT]] / [[2601.20218|DenseGRPO]]); AR backbones use straight-through $\arg\max$ decode. LPIPS backbone is frozen Alex-lin.

**DreamDojo temporal-consistency anchor** — F4+F5 support (Eq. 12), [[2602.06949|DreamDojo]] Eq. (4) over $K_{\text{lat}}$ latent frames **within** a single video-chunk generation:

$$
L^{\text{TC}}(\theta) = \frac{1}{KT} \sum_{i=1}^{K}\sum_{t=0}^{T-1} \mathbb{E}\Bigl[\sum_{k=1}^{K_{\text{lat}}-1} \bigl\|(z^{(k+1)}_{i,t} - z^{(k)}_{i,t}) - (v^{\ast(k+1)}_{i,t} - v^{\ast(k)}_{i,t})\bigr\|^2\Bigr] \tag{12}
$$

$z^{(k)}_{i,t} = u_\theta(x^{(k)}_{i,t}, k, c)$ = predicted velocity at latent frame $k$; $v^{\ast(k)}_{i,t}$ = ground-truth velocity (sim → backbone-VAE + finite difference); $K_{\text{lat}}$ = backbone-specific latent-frame count. Active when $K_{\text{lat}} > 1$ (Cosmos $\geq 4$, UWM ≈8, DreamZero); inactive on $K_{\text{lat}}=1$ configs. $\beta_{\text{TC}} = 0.1$ (our default; DreamDojo doesn't publish a numerical λ).

**Full objective** — single-stage cooperative-RL + three dense anchors (Eq. 13):

$$
L_{\text{total}}(\theta_{\text{lora}}, \theta_{\text{finder}}) = L_{\text{PS-uGRPO}}(\theta_{\text{lora}}) + \alpha \cdot L_{\text{finder}}(\theta_{\text{finder}}) + \beta_{\text{MSE}} \cdot L_{\text{img}}^{\text{flow-prefix}} + \beta_{\text{LPIPS}} \cdot L_{\text{img}}^{\text{LPIPS}} + \beta_{\text{TC}} \cdot L^{\text{TC}} \tag{13}
$$

PS-uGRPO drives $\theta_{\text{lora}}$; anchors supply dense gradient where RL advantage is sparse; $\alpha \cdot L_{\text{finder}}$ drives $\theta_{\text{finder}}$. Single `L_total.backward()` + `optimizer.step()` updates both; $\theta_{\text{base}}$ stays frozen. Defaults: $\beta_{\text{MSE}} = \beta_{\text{LPIPS}} = \beta_{\text{TC}} = 0.1$, $\alpha = 0.05$.

#### WAM failure modes — mapping to Eq. 13 terms

Eq. 13's terms jointly close all five failure modes of the current WAM's imagination:

| Mode | Closed by |
|---|---|
| **F1** Action-conditioning misalignment | MSE anchor (Eq. 10, `k=0`) + r^task action-smoothness term (Eq. 2) + r^phys V-JEPA 2 surprise on imagined frames (Eq. 3) |
| **F2** Observation OOD | MSE anchor (Eq. 10) on OOD sim observations + failure-finder (Eq. 9) actively pushes policy into OOD perturbations |
| **F3** Unseen dynamics | Physics reward (Eq. 3) + MSE anchor |
| **F4** Compounding / teacher-forcing trap | Prefix-AR in Eq. 10 (random `k ∈ [0, K_max]`) + DreamDojo TC anchor (Eq. 12) |
| **F5** Modal collapse | PS-uGRPO spatial + physics rewards (Eq. 8) + LPIPS anchor (Eq. 11) + TC anchor (Eq. 12) |

The unified GRPO does task / physics / spatial work; anchors (MSE, LPIPS, TC) keep the high-dimensional decoder trainable. Scalar RL advantage is information-sparse vs. per-pixel supervision, so $\beta > 0$ is required to prevent decoder collapse (C3 tests this).

**Notation** — grouped by role. Every symbol appearing in Eqs. 1–13 is defined here exactly once.

*Parameters and functions*:
- $\theta_{\text{base}}$ — Cosmos / UWM **base weights**, FROZEN throughout training (per §LoRA strategy). Dual-purpose: (a) body for LoRA adapter training, (b) encoder feeding the failure-finder.
- $\theta_{\text{lora}}$ — LoRA adapter weights on top of $\theta_{\text{base}}$ (PS-uGRPO trains these; default rank $r=32$, $\alpha_{\text{lora}}=64$).
- $\theta_{\text{finder}}$ — failure-finder network parameters (small RL net trained via Eq. 9; second trainable component beyond $\theta_{\text{lora}}$).
- $\pi_\theta(a \mid o, c)$ — policy (action head); $\theta = \theta_{\text{base}} + \theta_{\text{lora}}$ at inference.
- $v_\theta(a_s;\, o, c)$ — action-head flow-matching velocity predictor (drives Eq. 6 SDE).
- $u_\theta(x_s;\, o, a, s)$ — image/video-head flow-matching velocity predictor (WM; Eq. 8).
- $p_\theta(z \mid \cdot)$ — AR-head next-token probability (Eq. 10; UniVLA / WorldVLA backbones).
- $V^{\text{SRPO}}(\tau_i) \in [0,1]$ — [[2511.15605|SRPO]] progress reward (Eq. 2); per-batch min-max-normalized inverse L2 distance to nearest DBSCAN centroid; broadcast to all $T$ steps. Reuses Eq. 3's frozen V-JEPA 2 encoder.
- $z_{\tau_i}, \{z^{\text{cent}}_k\}$ — V-JEPA 2 trajectory latent and DBSCAN centroids over batch-internal successes (density-based; cluster count data-driven via `eps`, `min_samples`).

*Rollouts and sim oracle*:
- $i \in \{1, \ldots, K\}$ — rollout index; $K$ = per-batch group size.
- $T$ — rollout horizon; $\tau_i = (o_{i,0}, a_{i,0}, \ldots, o_{i,T})$.
- $t \in \{0, \ldots, T-1\}$ — environment step (distinct from flow time $s$ below).
- $T^{\text{valid}}_i$ — per-trajectory valid length (up-to-first-success); [[2602.13977|WoVR]] length-normalization in Eq. 8.
- $o_{i,0} \sim p_0^{\text{sim}}$ — initial state (uniform over sim reset distribution; perturbed with prob $p_{\text{perturb}}$ per failure-finder selection).
- $r_i \in \{0,1\}$ — sim trajectory-success oracle; $o^{\text{sim}}_{i,t+1}$ — per-step sim ground-truth observation.
- $c$ — language task instruction (shared across a rollout's steps).

*GRPO clip + sampling* ([[2511.09515|WMPO]]-faithful; applies to Eqs. 8 and 9):
- $\rho_{i,t}$ — PS-uGRPO probability ratio $\pi_\theta^{\text{joint}}/\pi_{\theta_{\text{old}}}^{\text{joint}}$.
- $\rho_j$ — failure-finder probability ratio (perturbation policy).
- $\varepsilon_{\text{low}}, \varepsilon_{\text{high}}$ — asymmetric dual-clip bounds; defaults $0.20, 0.28$.

*Unified reward components* (Eqs. 1–4):
- $r^{\text{uni}}_{i,t}$ — unified per-step reward driving PS-uGRPO.
- $r^{\text{task}}_{i,t}$ — task component (SRPO progress + EvoVLA POE + CAPS smoothness; Eq. 2).
- $r^{\text{phys}}_{i,t}$ — physics component (V-JEPA 2 surprise on imagined frames; Eq. 3).
- $r^{\text{spatial}}_{i,t}$ — spatial component (phase-geometric + CIoU bbox alignment on imagined frames; Eq. 4).
- $z_t = \psi(T_{\text{ee}}^{-1} \cdot T_{\text{obj}}) \in \mathbb{R}^6$ — relative gripper-to-object pose feature; sim provides $T_{\text{ee}}, T_{\text{obj}}$ directly.
- $r^{\text{cur}}_{i,t}$ — pose-curiosity reward (POE forward-dynamics prediction error; Eq. 2 prose). $\hat{f}_{\text{fwd}}$ pre-trained on sim transitions during cold-start.
- $S_{\text{act}}$ — 1st-order action smoothness (Eq. 2 prose).
- $w_T, w_P, w_S \ge 0$ — top-level reward weights; defaults $w_T = 1.0$, $w_P = w_S = 0.3$.
- $\lambda_{\text{cur}}, \lambda_{\text{smooth}} \ge 0$ — r^task sub-weights; defaults $\lambda_{\text{cur}} = 0.6$ (EvoVLA's $\rho$), $\lambda_{\text{smooth}} = 0.1$.
- $\eta$ — POE intrinsic scale (default $1.0$).

*Physics reward internals* (Eq. 3):
- $E_\theta, P_\phi$ — frozen [[2506.09985|V-JEPA-2]] ViT-g encoder + predictor (~1B, MIT; matches WMReward default `vitg`); context window $\le t$ at 256² resolution.
- $D_{\text{phys}} \in [0, 1]$ — [[2601.10553|WMReward]] surprise score (higher = imagined next frame matches predictor's expectation).
- $\lambda_{\text{phys}} \ge 0$ — physics weight; default $1.0$.

*Spatial reward internals* (Eq. 4):
- $\text{phase}_t \in \{\text{Reach}, \text{Place}, \text{Leave}\}$ — manipulation phase from sim's subgoal oracle.
- $\Delta_{\text{geo}}(\text{phase}_t)$ — signed scalar aggregating SA-VLA's per-phase temporal-distance differences (our notation; sign convention in Eq. 4 prose).
- $\mathrm{bbox}(\cdot)$ — object bounding-box extractor; applied to imagined $\hat{o}_{i,t+1}$ and sim $o^{\text{sim}}_{i,t+1}$.
- $\mathrm{CIoU}(\cdot, \cdot) \in [0, 1]$ — Complete IoU (Zheng et al. 2020), used directly per SpatialThinker.
- $\lambda_{\text{geo}}, \lambda_{\text{CIoU}}$ — spatial sub-weights; defaults $1.0, 0.5$.

*GRPO statistics* (Eq. 5):
- $\mu_t, \sigma_t$ — per-timestep mean and std of $r^{\text{uni}}_{\cdot, t}$ over the $K$ rollouts.
- $A^{\text{uni}}_{i,t}$ — per-timestep unified advantage.
- $\epsilon_{\text{num}}$ — small constant for denominator numerical stability.

*Flow-matching SDE variables* (Eqs. 6, 7, 10; flow time $s$ disambiguated from env step $t$, GRPO $\sigma_t$, num $\epsilon_{\text{num}}$):
- $s \in [0,1]$ — flow time.
- $a_s, x_s$ — flow interpolant samples (action and image variants).
- $\varepsilon \sim \mathcal{N}(0, I)$ — flow noise.
- $\sigma_{\text{flow}}(s)$ — SDE diffusion coefficient.
- $p_s(a_s)$ — marginal density of $a_s$ under the flow.
- $dW_s$ — Wiener increment.
- $v^\ast$ — ground-truth flow velocity target (Eq. 10).
- $\pi_\theta^{\text{joint}}$ — joint action + imagined-next-observation log-prob (factorizes per Eq. 7).

*AR-token variables* (AR-backbone analog of Eq. 10):
- $z_{i,t+1}$ — VQ-tokenized next observation (target for AR-backbone CE loss).
- $\mathrm{VQ}(\cdot)$ — vector-quantizer encoder (backbone-specific).
- $k$ — token index within $z_{i,t+1}$.

*Failure-finder* (Eq. 9; [[2412.02818|RoboMD]]-modified-to-GRPO):
- $B = \{e_1, \ldots, e_M\}$ — perturbation-bank anchor embeddings; $M = 14$–19 per task (see §Cold-start).
- $h_t = \mathrm{body}_{\theta_{\text{base}}}(\text{scene\_image})$ — frozen-base scene embedding; finder's input.
- $K_{\text{finder}}$ — finder GRPO group size; default $8$.
- $\bar r^{\text{uni}}_j, \overline{|A^{\text{uni}}|}_j$ — mean $r^{\text{uni}}$ and mean $|A^{\text{uni}}|$ on perturbation $j$ over $K \times T$ transitions (currency + regret terms in $r^{\text{finder}}_j$).
- $r^{\text{finder}}_j$ — combined finder reward (Eq. 9).
- $\lambda_\sigma \ge 0$ — learning-signal weight; default $0.5$.
- $A^{\text{fail}}_j$ — group-relative advantage on $r^{\text{finder}}_j$.
- $\alpha \ge 0$ — finder loss weight; default $0.05$.
- $p_{\text{perturb}}$ — per-round perturbation probability; default $0.5$.
- $N_{\text{warmup}}$ — warm-up rounds with uniform-random selection; default $20$.
- $\eta_{\text{ent}} \ge 0$ — entropy bonus weight; default $0.01$, decays to $0$ by round ~100.
- $\mathcal{H}(\pi_{\text{finder}}(\cdot \mid h))$ — finder policy entropy.
- $\overline{\text{success}}_j$ — empirical task-success rate; diagnostics only (not in $r^{\text{finder}}_j$).

*Anchor losses* (Eqs. 10, 11, 12):
- $K_{\max}$ — max rollout prefix length; default $9$ ([[2603.25685|Persistent-Robot-WMs]] §S1).
- $\tilde{o}_{i,t-k:t}$ — WAM free-rolled obs of length $k$ (ground-truth at $k=0$, fully imagined at $k=K_{\max}$).
- $\mathrm{LPIPS}(\cdot, \cdot)$ — learned perceptual similarity (frozen Alex-lin).
- $\hat{x}^{\text{clean}}_{i,t+1}$ — single-Euler-step clean prediction at $s \approx 0.9$ (flow); AR uses $\mathrm{Dec}(\arg\max p_\theta)$ + straight-through.
- $\mathrm{Dec}(\cdot)$ — frozen pixel decoder (VAE / VQ-GAN).
- $z^{(k)}_{i,t}, v^{\ast(k)}_{i,t}$ — DreamDojo predicted / ground-truth velocity at latent frame $k$ (Eq. 12).
- $K_{\text{lat}}$ — WM per-generation latent-frame count; TC inactive when $K_{\text{lat}} = 1$. Disambiguated from batch-size $K$.

*Loss weights* (Eq. 13):
- $\beta_{\text{MSE}} \ge 0$ — MSE anchor weight; default $0.1$.
- $\beta_{\text{LPIPS}} \ge 0$ — LPIPS anchor weight; default $0.1$.
- $\beta_{\text{TC}} \ge 0$ — DreamDojo TC anchor weight; default $0.1$ (our default; DreamDojo doesn't publish a numerical $\lambda$).

### Algorithm

```python
# Round N. PS-uGRPO (LoRA θ_lora) + failure-finder (θ_finder) update concurrently; θ_base frozen.

# 0.5. Failure-finder selects perturbation (Eq. 9). Warm-up: uniform-random for first N_warmup rounds.
perturbation_group = []
for j in range(K_finder):
    if random() < p_perturb:
        h = body_θ_base(scene_image)
        if N < N_warmup:
            edit_j = uniform_random_choice(B)
            z_j = anchor_embedding(edit_j, B)
        else:
            z_j = π_finder(h)
            edit_j = argmin_quantize(z_j, B)
        perturbation_group.append((j, edit_j, z_j))
    else:
        perturbation_group.append((j, NO_PERTURB, None))

# 1. Joint rollout: K rollouts per perturbation; K * K_finder total per round.
rollouts_per_perturb = {}
for (j, edit_j, _) in perturbation_group:
    env_j = apply_xml_edit(env, edit_j) if edit_j != NO_PERTURB else env
    rollouts_per_perturb[j] = [joint_rollout_in_sim(θ_base + θ_lora, env_j, T=T) for _ in range(K)]

# 1.5. WMPO dynamic sampling filter — drop all-collapse perturbation groups.
for j in list(rollouts_per_perturb):
    if all_collapse(rollouts_per_perturb[j]):
        rollouts_per_perturb.pop(j)

# 2. Diagnostics (logging only; failure-finder reward uses r^uni, not task_success).
success_rate = {j: mean_success(rollouts_per_perturb[j]) for j in rollouts_per_perturb}

# 4. Unified reward (Eq. 1). SRPO progress: DBSCAN over batch successes in V-JEPA 2 latent.
z_traj          = {(j,i): VJEPA2_encode(rollouts_per_perturb[j][i]) for j, _ in rollouts_per_perturb.items() for i in range(K)}
success_latents = [z_traj[(j,i)] for (j,i) in z_traj if env_success(rollouts_per_perturb[j][i])]
centroids       = DBSCAN(success_latents, eps=eps_dbscan, min_samples=min_pts).centroids if success_latents else []
d               = {k: min_L2(z_traj[k], centroids) for k in z_traj} if centroids else {}
d_min, d_max    = (min(d.values()), max(d.values())) if d else (0.0, 1.0)
V_SRPO          = {k: 1 - (d[k] - d_min) / (d_max - d_min + ε_num) if centroids else 0.0
                   for k in z_traj}                                                      # broadcast to all T steps
for j, rollouts in rollouts_per_perturb.items():
    for i, rollout in enumerate(rollouts):
        for t in range(T):
            z_t   = pose_feat(T_ee[i,t], T_obj[i,t])
            z_tp1 = pose_feat(T_ee[i,t+1], T_obj[i,t+1])
            r_cur = (η/2) * ||sg(f_fwd_hat(z_t, a[i,t])) - z_tp1||**2       # POE
            r_task[j,i,t] = (V_SRPO[(j,i)]
                             + λ_cur * r_cur
                             - λ_smooth * S_act(a[i, t-1:t+1]))             # CAPS smoothness
            r_phys[j,i,t] = λ_phys * D_phys(o_hat[i,:t+1], o_hat[i,t+1])    # V-JEPA 2 surprise
            r_spat[j,i,t] = (  λ_geo  * signed_geo_delta(phase[i,t], o_sim[i,t:t+2], a[i,t])
                             + λ_CIoU * CIoU(bbox(o_hat[i,t+1]), bbox(o_sim[i,t+1])))
            r_uni[j,i,t]  = w_T * r_task[j,i,t] + w_P * r_phys[j,i,t] + w_S * r_spat[j,i,t]

# 5. Group-relative advantage (Eq. 5).
μ_t, σ_t = per-timestep statistics of r_uni over (j,i)
A_uni[j,i,t] = (r_uni[j,i,t] - μ_t) / (σ_t + ε_num)

# 6. PS-uGRPO loss on θ_lora (Eq. 8).
L_PS_uGRPO = 0.0
for j in rollouts_per_perturb:
    for i in range(K):
        L_traj = 0.0
        for t in range(T):
            log_pi_joint = (  flow_grpo_log_prob(π_(θ_base+θ_lora), a[i,t]       | o_sim[i,t],        c)
                            + flow_grpo_log_prob(u_(θ_base+θ_lora), o_hat[i,t+1] | o_sim[i,t], a[i,t], c))
            ρ = exp(log_pi_joint - log_pi_joint_old[j,i,t])
            clip_term = clip(ρ, 1 - ε_low, 1 + ε_high) * A_uni[j,i,t]   # WMPO asymmetric dual-clip
            L_traj -= min(ρ * A_uni[j,i,t], clip_term)
        L_PS_uGRPO += L_traj / max(T_valid[j,i], 1)              # WoVR length-norm
L_PS_uGRPO /= max(K * len(rollouts_per_perturb), 1)

# 6.5. Failure-finder loss on θ_finder (Eq. 9; regret-aligned r^finder + entropy bonus).
mean_r_uni    = {j: mean(r_uni[j,:,:])      for j in rollouts_per_perturb}
mean_abs_A    = {j: mean(abs(A_uni[j,:,:])) for j in rollouts_per_perturb}
finder_reward = {j: -mean_r_uni[j] + λ_σ * mean_abs_A[j] for j in rollouts_per_perturb}
μ_G, σ_G = group_stats(finder_reward.values())
A_fail = {j: (finder_reward[j] - μ_G) / (σ_G + ε_num) for j in rollouts_per_perturb}

L_finder = 0.0
for j_idx, j in enumerate(rollouts_per_perturb):
    if perturbation_group[j_idx][2] is None:
        continue
    z_j = perturbation_group[j_idx][2]
    h = body_θ_base(scene_image)
    log_π_finder = π_finder(z_j | h)
    ρ_j = exp(log_π_finder - log_π_finder_old[j])
    clip_term = clip(ρ_j, 1 - ε_low, 1 + ε_high) * A_fail[j]
    L_finder -= min(ρ_j * A_fail[j], clip_term)
L_finder /= max(K_finder, 1)
L_finder -= η_ent * mean_entropy(π_finder, h)                     # entropy bonus (decays to 0 by ~round 100)

# 7. MSE anchor with prefix-AR (Eq. 10).
L_img_MSE = 0.0
n_anchor = 0
for j in rollouts_per_perturb:
    for i in range(K):
        for t in range(T):
            k = uniform_int(0, K_max)
            obs_context = o_sim[i,t] if k == 0 else (θ_base+θ_lora).wm_rollout(o_sim[i,t-k], a[i,t-k:t])
            L_img_MSE += flow_matching_loss((θ_base+θ_lora).wm_predict(obs_context, a[i,t]), o_sim[i,t+1])
            n_anchor += 1
L_img_MSE /= max(n_anchor, 1)

# 8. LPIPS anchor (Eq. 11; single-Euler-step at s≈0.9).
L_img_LPIPS = 0.0
n_lpips = 0
for j in rollouts_per_perturb:
    for i in range(K):
        for t in range(T):
            x_clean = single_euler_step(u_(θ_base+θ_lora), o_sim[i,t], a[i,t], s=0.9)
            L_img_LPIPS += LPIPS(Dec(x_clean), o_sim[i,t+1])              # frozen Alex-lin
            n_lpips += 1
L_img_LPIPS /= max(n_lpips, 1)

# 9. DreamDojo TC anchor (Eq. 12; inactive on K_lat = 1).
L_TC = 0.0
n_tc = 0
if K_lat > 1:
    for j in rollouts_per_perturb:
        for i in range(K):
            for t in range(T):
                for k in range(1, K_lat):
                    z_k, z_km1 = u_(θ_base+θ_lora)(x[i,t,k], k, c), u_(θ_base+θ_lora)(x[i,t,k-1], k-1, c)
                    v_k, v_km1 = v_star[i,t,k],                    v_star[i,t,k-1]
                    L_TC += ||(z_k - z_km1) - (v_k - v_km1)||**2
                n_tc += K_lat - 1
    L_TC /= max(n_tc, 1)

# 10. Full objective (Eq. 13). One backward + step updates θ_lora and θ_finder.
L_total = L_PS_uGRPO + α * L_finder + β_MSE * L_img_MSE + β_LPIPS * L_img_LPIPS + β_TC * L_TC
L_total.backward()
optimizer.step()

# 11. Recalibration: SRPO clusters are batch-internal (re-fit per round in step 4); no separate refresh needed.
```

**Hyperparameter defaults**:
- Reward weights: `w_T = 1.0`, `w_P = w_S = 0.3`; r^task sub-weights `λ_cur = 0.6` (EvoVLA $\rho$, §3.2), `λ_smooth = 0.1` (CAPS, small relative to $V^{\text{SRPO}}$); r^phys sub-weight `λ_phys = 1.0`; spatial sub-weights `λ_geo = 1.0`, `λ_CIoU = 0.5`.
- **GRPO clip + sampling defaults** (WMPO; apply to both PS-uGRPO and failure-finder): `ε_low = 0.20`, `ε_high = 0.28` (asymmetric dual-clip); no KL term (no reference model); dynamic sampling filter active (drop all-collapse K-groups, resample). **Trajectory normalization** (WoVR): per-trajectory `1/T_valid_i` weighting in Eq. 8, where `T_valid_i` = up-to-first-success length.
- Failure-finder: `K_finder = 8` (perturbation group size); `α = 0.05` (failure-finder loss weight); `λ_σ = 0.5` (learning-signal weight in `r^finder`; ablate `{0, 0.5, 1.0}`); `p_perturb = 0.5` (50% perturbed + 50% clean rollouts per round); `M = 14–19` perturbation arms per task (RoboMD-counted). **Cold-start guards**: `N_warmup = 20` (warm-up rounds with uniform-random selection); `η_ent = 0.01` initial entropy bonus, linearly decayed to `0` by round 100. Failure-finder LR ≈ 10× slower than PS-uGRPO's.
- SRPO progress reward: DBSCAN `eps = 0.5` (V-JEPA 2 latent space, ablate `{0.3, 0.5, 0.7}`), `min_samples = 5`. Decoder-restricted gradient routing for `r^phys`: final-N DiT blocks with `N = 4` (ablate `OFF`).
- Anchor weights: `β_MSE = β_LPIPS = β_TC = 0.1` (RL dominates; three anchors provide dense gradient only).
- LoRA `r = 32, α_lora = 64`; LR `1e-4` (LoRA) / `1e-5` to `5e-6` (heads). Cosmos $\theta_{\text{base}}$ permanently FROZEN.
- Rollout: `K = 16–32` per batch; `K_max = 9` (prefix-AR depth, matches PRWM); `S_train = 10, S_infer = 40`.

### Baselines

Four external baselines + one asymmetric internal baseline, each isolating one design choice. All run on the same LIBERO suite + same unified backbone (UWM) for apples-to-apples; PLD additionally runs with its published backbone to anchor against its own 99% LIBERO number.

| Baseline | What it has | What it isolates (tests our design choice) | Repo |
|---|---|---|---|
| **[[2511.00091\|PLD]]** (no-WM residual RL) | Frozen VLA base + lightweight residual RL specialists + SFT distillation; **99% LIBERO** | Does the WM (and hence physics+spatial rewards computed from imagined frames) buy anything over no-WM residual RL? Tests C3 | [PLD project page](https://wenlixiao.com/self-improve-VLA-PLD) (code not yet released as of 2026-04) |
| **[[2511.09515\|WMPO]]-in-sim** (WMPO's compute graph with sim rollouts) | Policy-only GRPO; no `r^phys`, no `r^spatial`, no WM anchor losses | Does unified (policy + WM) GRPO with physics+spatial rewards beat policy-only GRPO at matched compute? Tests C1a, C1b | [WM-PO/WMPO](https://github.com/WM-PO/WMPO) |
| **[[2602.13977\|WoVR]]** (OpenVLA-OFT backbone) | Masked GRPO + KIR + PACE co-evolution; **69.2% LIBERO** | Does PS-uGRPO (single unified update) beat WoVR's three-stage orchestration at matched compute? | [RLinf/RLinf](https://github.com/RLinf/RLinf) |
| **[[2509.09674\|SimpleVLA-RL]]** (full-FT, no WM, no failure-finder) | OpenVLA-OFT 7B full fine-tune with verified sim reward; single-task | Does LoRA + unified backbone beat full-FT single-task RL at matched task count? Tests LoRA-on-body efficacy | [PRIME-RL/SimpleVLA-RL](https://github.com/PRIME-RL/SimpleVLA-RL) |
| **Asymmetric RL+supervised** (internal ablation; policy-only Flow-GRPO + supervised MSE on WM; `w_P = w_S = 0`) | Tests C1a: does unified RL on both heads (+ physics+spatial rewards) beat the asymmetric split at matched compute? | (self — Eq. 11 degraded) |

**Ablations within PS-uGRPO** — credit attribution across Eq. 13's components:

| Ablation | Tests |
|---|---|
| **Reward-term dropouts** — `w_T=0`, `w_P=0`, `w_S=0`, no-PVM, `λ_cur=0` (POE pose-curiosity off), `λ_smooth=0` (CAPS action-smoothness off), `λ_phys=0` (V-JEPA 2 surprise off) (7 runs) | C1c — each component's contribution to `r^uni`. Expected: `w_P=0` drops ≥3pp on contact-rich (V-JEPA 2 surprise drives imagination physics); `w_S=0` drops ≥3pp on spatial-perturbed; `w_T=0` collapses entirely; `λ_cur=0` slows long-horizon exploration; `λ_smooth=0` raises chatter / oscillation in policy actions; `λ_phys=0` allows imagination to drift toward physics-violating frames |
| **Sparse-reward ablation** — replace all per-step dense rewards with terminal-only task success (`r^uni_{i,t} = r_i · 𝟙[t=T-1]`) | Quantifies dense-reward contribution to the paper's headline claim (C1). Expected: ≥ 10pp drop on LIBERO-Long (aligns with [[2601.20218|DenseGRPO]]'s sparse-vs-dense finding for flow-matching RL) |
| **Failure-finder ablations** (6 runs) — (a) `α=0` with `p_perturb=0` (pure PS-uGRPO, no perturbation); (b) `α=0` with uniform-random perturbation sampling; (c) `α=0` with fixed perturbation distribution; (d) full failure-finder (`α=0.05`, `λ_σ=0.5`); (e) `λ_σ=0` (currency-aligned only — tests learning-signal term); (f) `r^finder = 1 − success_rate` (binary reward — tests currency-alignment) | Tests (1) **learned vs. unlearned** — full failure-finder beats random / fixed / no-perturbation; (2) **regret-aligned vs. binary** — full reward beats (e) and (f) on physics-perturbed and spatial-perturbed subsets. Expected: full failure-finder beats all on LIBERO-Pro / LIBERO-Plus. Backs C1 |
| **Anchor dropouts** — `β_MSE=0`, `β_LPIPS=0`, `β_TC=0`, `K_max=0` (4 runs) | C3 + F4/F5 — per-head decoder collapse under RL-only (`β_MSE=0`); perceptual anchor effect (`β_LPIPS=0`); DreamDojo TC necessity (`β_TC=0`); prefix-AR necessity (`K_max=0`) |
| **Decoder-routing dropout** — PIRF `OFF` (`r^phys` gradient flows through full DiT body, vs. final-4 DiT blocks ON) (1 run) | Tests §Honest concerns Risk #2. Expected: full-body gradient degrades general manipulation semantics (extrapolating PIRF's U-Net "global-fidelity degradation" finding to DiT-VLAs; specific VLA properties not tested in PIRF source) |

### Novelty

Three contributions, each a falsifiable claim against a named prior-work target. The shared-backbone co-evolution, anchor losses, and full-K×T update set are *consequences* of the unified-GRPO formulation, not independent contributions.

| Contribution | Falsifiable claim | Prior-work target |
|---|---|---|
| **C1 — Single-stage cooperative-RL self-evolving WAM** (Eqs. 8 + 9: PS-uGRPO + RoboMD-modified-to-GRPO failure-finder, joint log-prob Eq. 7, unified reward Eq. 1, full objective Eq. 13) | **C1a**: at matched compute on LIBERO, PS-uGRPO beats asymmetric (RL-on-policy + supervised-on-WM) by ≥ 5 pp on LIBERO-Long (physics reward drives long-horizon stability). **C1b**: on spatial-perturbed LIBERO, PS-uGRPO beats asymmetric by ≥ 5 pp (spatial reward drives geometric robustness). **C1c**: removing either `r^phys` (Eq. 3) or `r^spatial` (Eq. 4) degrades the respective axis by ≥ 3 pp — verifies component-level credit attribution. **C1d**: failure-finder ON (`α=0.05`) beats failure-finder OFF (`α=0`, no perturbation) by ≥ 3 pp on OOD generalization (LIBERO-Pro / LIBERO-Plus); learned curriculum beats random / fixed perturbation sampling | No prior work runs single-stage cooperative-RL on a unified WAM backbone with concurrent updates of policy (LoRA) and curriculum (failure-finder). [[2511.09515\|WMPO]]: RL on policy only. [[2412.02818\|RoboMD]]: three-stage Discover→Summarize→Restructure pipeline with separate ViT+CLIP embedding training. [[2602.00743\|SA-VLA]]: spatial rewards but supervised-only L_img. [[2511.07403\|SpatialThinker]]: GRPO with spatial rewards on MLLMs, not VLAs |
| **C2 — PS-uGRPO beats no-WM residual RL on sample efficiency / OOD transfer** | **C2a**: on LIBERO, our method reaches 90% with ≤ 50% of [[2511.00091\|PLD]]'s rollouts. **C2b**: on held-out OOD tasks (LIBERO-Pro / LIBERO-Plus), our transfer exceeds PLD's by ≥ 10 pp | [[2511.00091\|PLD]] hits 99% LIBERO *without any WM*. If C2a+C2b both fail, the WM (and therefore `r^phys` + `r^spatial` from imagined frames) is dead weight; paper reframes as "perturbation-curriculum-gated sim-SFT with task reward only" |
| **C3 — UWM's distinct decoders make per-head gradient asymmetry empirically observable** | Under anchor-free PS-uGRPO (`β_MSE = β_LPIPS = β_TC = 0` on both UWM and Cosmos Policy under default configs $K_{\text{lat}} \approx 8$ and $\geq 4$ respectively), $\|\nabla_{\theta_{\text{lora}}} L_{\text{PS-uGRPO}}\|_{\text{action decoder}} / \|\nabla_{\theta_{\text{lora}}} L_{\text{PS-uGRPO}}\|_{\text{patch decoder}}$ diverges monotonically over training rounds on UWM. Anchor losses bound the ratio: MSE + LPIPS + TC on both. **Decoder-collapse diagnostic**: direct empirical evidence for "anchors are necessary" | No prior work measures this ratio on [[2504.02792\|UWM]] — novel diagnostic, hinges on UWM's structural asymmetry (2-Linear+Mish action decoder vs. 1-Linear patch decoder). Cosmos's single denoiser cannot host this test |

## Backbones

### Summary

| Backbone | Pure PS-uGRPO (no anchors) suffices? | Needs anchors (Eqs. 10, 11, 12)? | What to ablate |
|---|---|---|---|
| [[2601.16163\|Cosmos-Policy]] | ✓ (single denoiser → automatic imag-policy *alignment* under shared RL gradient) | Optional — sharpens imagination *fidelity* | `β_MSE = β_LPIPS = 0` vs. defaults; FVD on held-out benchmark decoupled from task reward |
| [[2504.02792\|UWM]] | ✗ — patch decoder cut off from direct policy gradient; WM receives only the weaker log `u_θ` signal; DiT body still updates via shared self-attention | **Required** for sharp image decoding (C3) | Per-head gradient-norm ratio (C3); `β_MSE = 0` vs. `β_MSE = 0.1` image-decoder FVD; per-head frozen-weight ablation |

#### Cosmos Policy — detailed plan

Cosmos Policy is a single denoiser over all modalities (proprio, actions, value, multi-view images) injected as latent frames — no separate action/image heads. RL-only gradient therefore updates imagination parameters as a side effect of the action gradient through shared θ. Reward / steps-to-go are added as additional latent-frame modalities.

| Imagination gain | Under PS-uGRPO alone | Needs anchors (Eqs. 10, 11, 12)? |
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

**Mechanism transferability** — [[2510.09976|FPO]] (87.2% LIBERO on π₀, CFM-likelihood-free PPO) and [[2505.22094|ReinFlow]] corroborate that flow-matching RL works at VLA scales.


## Sim-to-Real Gap

The three anchor losses (Eqs. 10, 11, 12) supervise the WM against sim's `o^sim_{t+1}`; PS-uGRPO's physics and spatial rewards (Eqs. 3, 4) are computed on WAM imagined frames — `D_phys` via frozen V-JEPA 2 (manipulation-relevant prior from V-JEPA 2's pretraining); bbox extractors reference sim. The WM therefore learns **sim physics**, not real physics.

**Policy sim-to-real** is in scope (standard — domain randomization per [[2601.16163|Cosmos-Policy]] / [[2511.09515|WMPO]]). **WM sim-to-real is out of scope** — the WM is sim-fit and stays behind at deployment; imagination-based planning on real robots requires a separate real-corpus WM fine-tune (DROID, AgiBot) in a follow-up paper. **Failure-finder + XML perturbation bank are sim-only** — both are training-time scaffolding for active failure-search and have no role at deployment.

**Deployment recipe**: ship Cosmos Policy with $\theta_{\text{base}} + \theta_{\text{lora}}$ fused to the real robot; discard (a) the WM, (b) the failure-finder $\theta_{\text{finder}}$, and (c) the hand-coded XML perturbation bank $B$. The deployed policy is architecturally unchanged from a vanilla Cosmos Policy — fused LoRA adds zero inference overhead, and the failure-finder + perturbation curriculum exist only inside the sim training loop. The WM is a training-time scaffold, consumed by PS-uGRPO (Eq. 8) and all three anchors (Eqs. 10, 11, 12) during sim training only.

## Honest concerns

**V-JEPA 2 surprise as `r^phys` is domain-extrapolated.** WMReward [[2601.10553]] p. 16, App. D: *"VJEPA surprise is not exclusively measuring physics plausibility and entangles other perceptual factors."* The paper validates only on natural-video generation; contact-rich and robotic-manipulation domains are outside its scope.

| Risk | Status |
|---|---|
| Reward-hacking by imagined-frame distortion | Mitigated by SRPO cluster-distance reward (Eq. 2; verified-reference pattern, [[2510.00406\|VLA-RFT]]) |
| `r^phys` gradient corrupting general policy semantics | Mitigated by decoder-restricted gradient routing (Eq. 3; [[2509.20570\|PIRF]]-inspired, ablated `OFF` in §Baselines) |
| V-JEPA 2 surprise misses LIBERO contact violations | **Open.** Defended by `λ_phys = 0` and PIRF `OFF` ablations in §Baselines |

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
| Imagination-based planning at real-robot deployment | Requires the above; deployment recipe here ships Cosmos (base + LoRA fused) only — failure-finder, perturbation bank, and WM are all sim-only |
| Min-max coupling between $\theta_{\text{lora}}$ and $\theta_{\text{finder}}$ on a shared loss | Symmetric zero-sum formulation deferred; alternating updates (ACCEL/PAIRED) are empirically more stable than joint min-max gradient descent |
| Open-ended perturbation generation (XML mutation / generative scene-edit) | The current bank is closed-set (M = 14–19 per task); open-ended self-discovery requires ACCEL-style mutation operators or a generative perturbation model — separate scope |
