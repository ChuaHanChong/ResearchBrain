---
title: "Self-Discovering Failure in Diffusion-WAMs — Literature Scan"
tags:
  - self-evolving
  - WAM
  - diffusion
  - failure-detection
  - failure-attribution
  - imagination-error
  - action-error
  - literature
aliases:
  - "Self-Discovering Diffusion-WAM Lit Scan"
  - "Diffusion-WAM Attribution Lit"
---

# Self-Discovering Failure in Diffusion-WAMs — Literature Scan

> [!abstract] Scope
> A literature scan for a first-publication **failure-discovery method for diffusion-based World Action Models** — a per-episode diagnostic that decomposes an episode's failure into ==imagination failure== (the WM's next-frame prediction diverged from reality) vs. ==action failure== (the WM's prediction was correct but the action head picked a poor action). The paper delivers the **diagnostic gate** only; what to *do* with a diagnosis — targeted retraining, residual RL, data collection — is **out of scope / future work**. Scope restricted to diffusion-WAM architectures across two sub-variants: **AR-video-diffusion** ([[2602.15922|DreamZero]]) and **FM-video-diffusion** (Fast-WAM, Cosmos-Predict2).

> [!info] How this scan was assembled
> Vault search across `_KnowledgeHub_/` (2247 paper notes) plus targeted alphaxiv + web queries for 2024–2026 work on (a) uncertainty / OOD detection in diffusion world models, (b) failure prediction in VLA policies, (c) verifier / process-reward models applicable to generative rollouts, (d) the "why diffusion, not latent" motivation (imagination-error well-posedness), and (e) per-episode attribution precedents. Organized as: (§Why Diffusion) motivation, (§Landscape) canonical diffusion WAMs, then three buckets — **(A) imagination-failure detection**, **(B) action-failure detection**, **(C) attribution & verification systems** — plus §The Gap and §Out-of-Scope Future Work.

---

## Why Diffusion-Based WAMs (and not Dreamer / JEPA)

Self-failure-discovery requires a measurable imagination-residual — a signal that says *"my world model's prediction was wrong here, regardless of what the policy did."* **The family of world models determines whether such a signal is well-defined in the first place.**

| WM family | Imagination-residual shape | Problem |
|---|---|---|
| **Dreamer-line** (latent reconstruction; e.g., DreamerV3) | Ensemble variance over $k$ latent-dynamics heads | Compute scales with $k$; infeasible for large WMs. |
| **JEPA-line** (joint-embedding, no reconstruction; e.g., V-JEPA2) | KL divergence between learned posterior and prior in latent space | **Self-referential**: the target encoder is an EMA of the student; low prediction error can mean "target agreed with student," not "model is right." Representation collapse, scale uninterpretability, non-stationary latent space. |
| **Diffusion-video-WAM** ([[2602.15922\|DreamZero]], Fast-WAM, Cosmos) | **Pixel-level prediction error** against the *observed* next frame; optional **semantic generative uncertainty** via CLIP / Bayesian last-layer | Grounded in the observation; interpretable in natural units (pixel MSE, PSNR, LPIPS); no self-reference; no collapse risk. |

**Diffusion WAMs are the only family whose imagination-residual has external ground truth at the per-step level** — the observation $o_{t+1}$ itself. Every rollout produces a pair $(\hat{o}_{t+1}, o_{t+1})$ that can be compared directly. Latent-WM families compute error in a learned, drifting, self-referential space; their signals require elaborate calibration and are brittle to architectural choices.

> [!tip] The paper's framing consequence
> The "why diffusion?" question is a *methodological contribution*, not a budget decision. We argue diffusion WAMs are the architecture class in which **per-episode failure attribution becomes well-posed** — and then deliver a principled diagnostic gate.

---

## Diffusion-WAM Landscape (2024–2026)

Within diffusion-based WAMs, two sub-variants span the design space of action-head structure:

| Sub-variant | Exemplar | Action head | Native action-side uncertainty | Native imagination-side uncertainty |
|---|---|---|---|---|
| **AR-video-diffusion** | [[2602.15922\|DreamZero]] (NVIDIA, 14 B) | Autoregressive over action tokens | Next-token entropy over the AR head's softmax | Pixel MSE at frame boundaries + multi-seed frame-variance + [[2502.20946\|generative uncertainty]] (Laplace + CLIP) |
| **FM-video-diffusion** | Fast-WAM / Cosmos-Predict2 ([[2602.20057\|AdaWorldPolicy]]'s backbone) / [[2603.07799\|MWM]] | Flow-matching action chunk | [[2510.25889\|Flow-SDE]] sample variance or multi-sample spread | Pixel MSE + CFG-disagreement / multi-seed denoising variance + [[2502.20946\|generative uncertainty]] |

Additional in-scope diffusion WAMs (cited but not used as experimental backbones):

- [[2412.14957|DREMA]] — Gaussian-Splatting + physics engine; hybrid-diffusion with explicit physics referee.
- [[2512.06628|MIND-V]] — Hierarchical diffusion WM with physical-alignment coherence reward.
- [[2603.07799|MWM]] — Mobile world models; demonstrates visually-faithful rollouts can be action-conditioned inconsistent.
- [[2502.00622|GPC]] — Generative Predictive Control; uses a diffusion WM for inference-time planning.
- [[2603.12639|RoboStereo]] — Dual-tower 4D EWM with **Test-Time Policy Augmentation (TTPA)** — a pre-execution verification step.

Out of scope: generic video-diffusion without an action interface.

---

## Problem Setup

A diffusion-WAM executes an episode by rolling out in imagination (denoising future frames + predicting actions) and acting in reality. When the episode fails, the failure has two possible blame targets:

| | Imagination failure | Action failure |
|---|---|---|
| **What's wrong** | Predicted frame $\hat{o}_{t+1}$ diverges from observed $o_{t+1}$ in pixel space | WM's frame prediction was correct, but the action-head choice is poor |
| **Signal (diffusion-specific)** | Pixel MSE / LPIPS; multi-seed denoising variance; [[2502.20946\|generative uncertainty]] (Laplace + CLIP); CFG-disagreement for CFG-enabled samplers | FM-head: [[2510.25889\|Flow-SDE]] sample variance; AR-head: token entropy; [[2604.01985\|WAV]] sparse inverse-dynamics as a verifier-independent check |
| **Meaning for future work (out of scope)** | The WM's physics / visual dynamics are wrong here → retrain the WM predictor on this region | The WM is fine; the action head picks bad actions on a correct dream → residual RL on the action head |

**Prior work on diffusion-WAM failure conflates these signals.** Existing *detection* systems ([[2510.09459|FIPER]], [[2506.09937|SAFE]], [[2503.08558|FAIL-Detect]]) fire a single "failure likely" flag. Existing *closed-loop* systems ([[2602.20057|AdaWorldPolicy]], [[2603.13528|Dream2Fix]]) fire on a single prediction-error signal and update everything. **No prior paper computes the two residuals as separately-interpretable per-episode signals and reports their joint distribution as a diagnosis.**

---

## Bucket A — Imagination-Failure Detection

Signals that tell the diffusion WAM *"my next-frame prediction is wrong about this region."*

### A.1 Pixel-Level Prediction Error

- **Post-rollout pixel MSE / LPIPS** — the core diffusion-WAM-native signal. Cheap, grounded, interpretable. No single vault paper proposes it as a *per-episode attribution signal*; we adopt it as the primary $r_{\text{imag}}$.
- [[2603.07799|MWM]] — pixel-level prediction error (LPIPS, DreamSim) is meaningful for action-conditioned video WMs; **action-consistency** metric is exactly this signal averaged over a rollout. **Borrowable**: confirmation that LPIPS / DreamSim are sensitive to WM failure.

### A.2 Multi-Seed / Bayesian Uncertainty (Self-Discovery)

- [[2502.20946|Generative Uncertainty in Diffusion Models]] — Bayesian **last-layer Laplace** + **semantic likelihood in CLIP feature space**; quantifies sample-quality uncertainty at ~10× lower cost than Monte Carlo seed variance. Directly validated on diffusion and flow-matching models. **Borrowable**: the principled epistemic channel — diffusion-native, computationally tractable.
- [[2511.04670|Cambrian-S]] — "surprise"-driven latent video-prediction error used for memory management; high latent divergence = WM breakdown. **Pure intrinsic**; stacks with pixel-MSE as a latent-side companion channel on $r_{\text{imag}}$.
- [[2512.01119|WM Surprise Robustness]] — Bayesian surprise as a principled detection signal. *Historical*: originally JEPA-only; the multi-hypothesis pattern transfers but not the math.
- [[1705.05363|ICM]] — forward-model prediction error as curiosity. *Historical*: canonical motivation; noisy-TV problem mitigated in diffusion by pixel-ground-truth.

### A.3 Physical-Plausibility Violation

- [[2603.19312|LeWM]]'s **Violation-of-Expectation** — prediction error is higher on physically implausible events than merely novel visual conditions. **Borrowable**: typed surprise signal (physics vs. appearance).
- [[2603.23376|ABot-PhysWorld]] — Diffusion-DPO to suppress physically implausible predictions (diffusion-native). **Borrowable**: as a data-side future-work remedy (out of scope for this paper).
- [[2412.14957|DREMA]] — compositional WM with explicit PyBullet physics engine. **Borrowable**: physics-verified rollout as a ground-truth channel when geometry is known.
- [[2512.06628|MIND-V]] — Physical Foresight Coherence reward with frozen V-JEPA2 as physics referee. **Borrowable**: PFC as a *model-checker-style* imagination-residual component.

### A.4 Conformal / Distributional OOD

- [[2602.16182|WM Failure Classifier]] — hybrid framework: success / known-failure / OOD via latent prediction error + conformal prediction. **Borrowable**: the three-way classifier — extend to four-way (imagination-OOD × action-OOD) via our 4-cell gate. **Critical baseline for the detection task** (purely detection, no updates — exactly the scope of this paper).

### A.5 Historical / Latent-WM Precedents (Context Only)

These are retained as cited prior work to motivate *why diffusion's pixel-ground-truth is preferable*:

- [[2005.05960|Plan2Explore]] — $k$-ensemble of latent dynamics (Dreamer-family). *Historical.*
- [[2504.16680|RWM-U / MOPO-PPO]] — ensemble epistemic uncertainty validated on physical quadrupeds (Dreamer-family). *Historical*: gold-standard validation of latent ensemble variance, but relies on architectural property (multi-head dynamics) unavailable in large diffusion WMs.
- [[2603.04029|Self-Adapting RL (Domberg)]] — OPR + RPR residual decomposition (Dreamer-family). *Closest prior decomposition concept* — but OR-gated and Dreamer-only.

---

## Bucket B — Action-Failure Detection

Signals that tell the agent *"the diffusion WM was right, but the action head failed."*

### B.1 Action-Uncertainty / Stochastic-Sample Spread (Self-Discovery)

- [[2510.09459|FIPER]] — OOD-observation score AND action-chunk entropy; ACE via dimension-wise binning. **Borrowable**: ACE is family-agnostic — works identically for FM continuous actions and AR discrete tokens via binning/softmax entropy. **Critical detection-only baseline**.
- [[2510.25889|πRL]]'s Flow-SDE — ODE→SDE conversion for flow-matching VLAs enables stochastic sampling and action-variance measurement. **Borrowable**: the FM sub-variant action-residual signal.
- [[2509.19292|SOE]] — VIB perturbation maps action-level behavioral boundaries. **Borrowable**: architecture-agnostic probing — transfers to both FM and AR action heads via latent perturbation (pre-action-head embedding).
- [[2604.04161|AAC]] (Adaptive Action Chunking) — Gaussian differential entropy on continuous action components as an inference-time signal for action quality; high entropy → smaller chunk / replan. **Pure intrinsic**; no failure labels. Stacks with Flow-SDE on the action side.
- [[2603.18091|ADV]] (Action Draft and Verify) — VLM perplexity over generated action candidates filters suboptimal actions before execution. **Pure intrinsic** (uses pretrained VLM perplexity, no failure-specific training). Action-side only.
- **Token entropy for AR diffusion** — native signal of AR-video-diffusion WAMs; cheap, no additional forward passes.

### B.2 Hidden-State / Internal-Feature Probes

- [[2506.09937|SAFE]] — probes VLA hidden states with a small MLP + conformal prediction. **Borrowable**: conformal calibration scheme; orthogonal internal-feature detector. **Note**: exchangeability assumption holds in our scope (no updates), so SAFE's statistical guarantees are preserved.
- [[2503.08558|FAIL-Detect]] — `logpZO` flow-based density + conformal prediction; **label-free calibration**. **Borrowable**: calibrate without access to failure labels. Complements the synthetic-injected-failure protocol.
- [[2310.17552|Sirius-Runtime]] — cVAE dynamics model + human-intervention-informed failure classifier. *Historical cousin of SAFE* (same probe-based paradigm, earlier).
- [[2603.11106|RC-NF]] — Robot-Conditioned Normalizing Flow; unsupervised density-based anomaly scoring (<100 ms). **Borrowable**: nominal-only training precedent — we use the same success-only calibration principle.
- [[2603.06987|Foundational WM]] — Cosmos-latent probabilistic WM + predicted std dev + residual calibrated via Conformal Prediction; 3.8% higher detection on real bimanual tasks. **Closest detection-scope competitor in the vault** — same conformal machinery, latent WM though (not diffusion).
- [[2510.02298|ARMADA]] — Online Optimal Transport on policy embeddings vs. expert trajectories; dynamic threshold adaptation. **Borrowable as baseline**; ~95% embedding-space detection accuracy.
- [[2410.14868|Diff-DAgger]] — repurposes diffusion policy's training loss as deployment uncertainty; +39% F1 over ensembles. **Diffusion-policy-native** — a direct comparator in the FM sub-variant since Fast-WAM has a diffusion action head.

### B.3 Sim-to-Real / Policy-Specific Diagnosis

- [[2602.01515|RAPT]] — reconstruction-likelihood OOD + integrated gradients + multi-modal LLM for zero-shot root-cause classification (75% Top-1). **Borrowable**: end-to-end diagnostic pipeline; a *competitor paradigm* for this paper (LLM-as-classifier vs. our structured gate) — should be compared head-to-head on attribution accuracy.
- [[2412.02818|RoboMD]] — RL adversary searches semantic embedding space for failure-inducing environments. **Borrowable**: active probing to construct the injected-failure test suite.
- [[2603.02115|Robometer]] — VLM reward model trained on absolute progress + pairwise preferences; F1 $= 0.81$ for zero-shot failure detection via **reward inversion**. **Borrowable as reward-model-detector baseline**; reward-based signal is global (no component decomposition).
- [[2407.08735|AESOP]] — dual-stage LLM runtime monitor (fast embedding-retrieval + slow generative reasoning); 100% recovery in simulation via MPC fallback. **Borrowable**: foundation-model-grounded detection layer; complementary to intrinsic signals.

### B.4 Multi-Detector Ensembles

- [[2410.04640|Sentinel]] — STAC + VLM judge in parallel. **Borrowable**: ensemble philosophy for the baseline comparison.
- [[2410.14868|Diff-DAgger]] — repurposes diffusion policy's training loss as uncertainty; +39% F1 over ensembles. **Borrowable**: *diffusion-native* uncertainty signal — direct precedent for using training loss at deployment.

---

## Bucket C — Attribution & Verification Systems

Systems that combine multiple signals or verify rollouts before / during / after — most directly comparable to our contribution.

### C.1 Verifiers for World-Model Rollouts

- [[2604.01985|WAV (World Action Verifier)]] — **closest prior work**. Decomposes WM verification into (state plausibility via a **subgoal generator**) and (action reachability via **sparse inverse dynamics**). Forward-inverse asymmetry. **Borrowable**: the sparse-IDM is a verifier-independent action-side signal that stacks with Flow-SDE / token entropy. **How we differ**: WAV routes disagreement to *data acquisition*; we route it to *per-episode diagnosis*. WAV assumes latent-WM; we target diffusion-video. WAV's contribution overlaps ours at the decomposition concept but not at the signal form, scope, or downstream use.
- [[2603.12639|RoboStereo]] — dual-tower 4D EWM with **Test-Time Policy Augmentation (TTPA)** for pre-execution verification. **Borrowable**: TTPA is a pre-execution verification stage that can catch would-be imagination failures before they happen — a *complementary* timing axis to our post-episode diagnostic gate.
- [[2504.16828|Process Reward Models That Think]] — step-level verifier that attributes failure to specific generation stages. **Borrowable**: step-level attribution as an additional granularity axis.
- [[2602.08971|WorldArena]] — 2×2 benchmark decomposition at the *model-evaluation* level: perceptual quality vs. functional utility across 14 WMs. **Structural precedent** for the imagination-vs-action decomposition, at benchmark granularity rather than per-episode. Empirical evidence: correlation between the two axes is only **r ≈ 0.36** — the decomposition is not trivial.

### C.1b VLM-Based Failure Attribution (Attribution Competitors — supervised)

These are the *attribution-task* competitors — all produce a structured cause label but all require labeled failure data:

- [[2512.01946|Guardian / FailCoT]] — VLM (InternVL3-8B) fine-tuned on **30K+ failure examples with CoT reasoning**; decomposes failures into **planning vs. execution** — the taxonomy most closely aligned with our imagination-vs-action-head axes. Beats GPT-4o on RoboFail. **Most direct taxonomy competitor**; requires extensive labeled failure data (we do not).
- [[2410.00371|AHA]] — VLM with procedurally generated failure dataset for free-form reasoning over robot failures. **Borrowable as baseline** (free-form output vs. our structured label).
- [[2505.12224|RoboFAC]] — comprehensive framework for robotic failure analysis and correction. **Borrowable as baseline** — broader scope than just detection, overlaps with future-work correction.
- [[2510.01642|FailSafe]] — VLM fine-tuned on synthetic failure-action pairs; outputs 7-DoF recovery actions; +22.6% success boost on OpenVLA. **Borrowable**: action-centric cause taxonomy (the recovery action implies the failure type); conflates diagnosis with correction.
- [[2409.03966|VLM Failure Recovery]] — GPT-4o prompt engineering for failure detection and recovery. *Earlier precedent*; simpler but shows the VLM-as-judge pattern was viable before task-specific fine-tunes.

### C.1c Counterfactual / Sim-Based Attribution

- [[2503.00761|TRACE]] — Tree-of-Thought + counterfactual critic; the critic perturbs VLM-predicted trajectories and the world model (sim access) validates feasibility. **Borrowable as both side**: counterfactual divergence provides evidence for both imagination and action failure. **Caveat**: requires oracle sim-rollouts per counterfactual — expensive; borderline self-discovery (oracle actions are a form of supervision). We keep it as a *baseline* for attribution comparison, not as a stacked component.

### C.2 Multi-Signal Detection Frameworks

- [[2602.16182|WM Failure Classifier]] — three-way success / known-failure / OOD classifier via conformal prediction. *Critical baseline* — the closest prior detection system for our benchmark.
- [[2603.22078|WAM-vs-VLA Robustness]] — WM-based vs. direct-policy robustness ablation across OOD axes. *Provides the injected-failure protocol* we adopt for the attribution-accuracy benchmark.
- [[2511.16166|EvoVLA]] — stage-aligned reward reduces stage hallucination by 23.7 pp. **Borrowable**: the stage-hallucination framing maps cleanly to our imagination-failure class.

### C.3 Decision-Aware MBRL Context

- [[2505.13709|Policy-Driven WM Adaptation]] — Stackelberg maximin joint adaptation. *Historical context*: motivates that likelihood-optimal WMs are not policy-optimal — hence the need for *policy-referenced* diagnosis. Not a direct competitor (it's an update method).
- [[2310.06253|Objective Mismatch MBRL Survey]] — taxonomy of decision-aware MBRL. **Borrowable**: places our contribution as a *per-episode* diagnostic tool that any decision-aware MBRL pipeline can consume.
- [[1911.10601|Scaling Active Inference]] — free-energy framework unifying prediction error and policy value. *Theoretical grounding* for why observation- and action-residuals should be compared, not summed.

---

## The Gap

> [!question] What no prior paper does
> No existing work **computes pixel-ground-truth imagination-residual and action-head-native action-residual in a diffusion-WAM system, reports their joint distribution as a per-episode diagnostic, and validates attribution accuracy on synthetic injected failures across both AR and FM diffusion sub-variants** — independent of any self-improvement loop.

**Closest prior approaches and why they fall short**:

| Paper | What it does | Why it's not the same |
|-------|-------------|----------------------|
| [[2510.09459\|FIPER]] | OOD-score ∧ action-entropy for failure *prediction* | AND-gated for detection; collapses the two signals into a single flag; no attribution |
| [[2604.01985\|WAV]] | Forward-inverse asymmetry on latent WMs, routed to data acquisition | Latent-WM; scope is self-improvement data loop; not per-episode diagnostic; no diffusion validation |
| [[2602.16182\|WM Failure Classifier]] | 3-way success / known-failure / OOD classification with conformal | Single signal; no WM-vs-action-head decomposition |
| [[2506.09937\|SAFE]] | Hidden-state probe + conformal | Single signal; predicts failure but doesn't localize to a component |
| [[2602.01515\|RAPT]] | LLM root-cause classification | Environmental cause (friction, actuator), not WM-vs-action-head |
| [[2603.04029\|Self-Adapting RL]] | OPR + RPR residuals, OR-gated | Dreamer-family only (excluded from scope); never treats the two residuals as a joint diagnostic |
| [[2602.08971\|WorldArena]] | 2×2 perceptual × functional *benchmark* | Benchmark-level decomposition of WMs; not per-episode; no per-trajectory signal definition |

**Evidence the dichotomy is empirically necessary in the diffusion family**:

1. [[2603.07799|MWM]] shows visually-faithful diffusion rollouts can be action-conditioned inconsistent — pixel MSE can be low while the action head still fails. Motivates a separate action-residual channel.
2. [[2602.08971|WorldArena]] finds a **"perception–functionality gap"** across 14 embodied WMs: correlation between perceptual quality and action-planning utility is only **r ≈ 0.36**.
3. [[2603.22078|WAM-vs-VLA Robustness]]: robustness gaps between WAM-based and direct-policy agents depend on the OOD axis — some failures stem from the WAM, others from the policy.
4. [[2604.01985|WAV]]: forward-inverse asymmetry holds empirically on real robots (latent WM); we claim the analogous decomposition is *more principled* in diffusion WMs because pixel-ground-truth removes the self-referential concern.

**The contribution**: a 4-cell *diagnostic* matrix from the joint of `(imagination-residual, action-residual)`, computed natively for each diffusion sub-variant. Each cell is a labeled diagnosis:

| | low action residual | high action residual |
|---|---|---|
| **low imag. residual** | **Success** — episode succeeded | **Action failure** — the WM was right; the action head chose poorly |
| **high imag. residual** | **Imagination failure** — the WM's prediction was wrong; action head was operating on a wrong dream | **Joint failure** — both signals fire; likely compounding cause |

The paper reports per-cell accuracy on a synthetic injected-failure benchmark, baseline comparison against single-signal detectors, and signal-correlation analysis — **nothing else**.

---

## Out-of-Scope / Future Work

These are explicitly deferred. The diagnostic gate produces a *label*; acting on the label is future work that builds on this paper's foundation.

- **Self-improvement loops** — targeted retraining, residual RL, LoRA updates. Relevant literature: [[2511.00091|PLD]], [[2507.21053|FPO]], [[2602.04879|DPPO]], [[2602.20057|AdaWorldPolicy]], [[2502.00622|GPC]], [[2603.13528|Dream2Fix]].
- **Failure-conditioned data synthesis** — generating recovery trajectories. Relevant: [[2603.13528|Dream2Fix]], [[2603.23376|ABot-PhysWorld]].
- **Closed-loop curriculum** — adaptive task-difficulty based on diagnosed failures. Relevant: [[2604.14144|SpatialEvo]], [[2602.16444|RoboGene]].
- **Reflection / memory over diagnoses** — learning from diagnosis history. Relevant: [[2603.08561|RetroAgent]], [[2502.05907|EvoAgent]].

The paper will include a one-paragraph "Applications" section pointing to these directions without instantiating them.

---

## Cross-References

- [[02_Self-Discovering-WAM-Roadmap]] — companion roadmap operationalizing this scan's §The Gap across AR and FM diffusion-WAM sub-variants.

---

*Companion to [[02_Self-Discovering-WAM-Roadmap]].*
