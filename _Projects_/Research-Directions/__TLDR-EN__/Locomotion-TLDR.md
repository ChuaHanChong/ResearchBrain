---
title: "TL;DR: Promising Research Directions: Locomotion — Bipedal & Quadruped"
aliases:
  - "Locomotion TL;DR"
  - "Locomotion skim"
tags:
  - tldr
  - locomotion
  - humanoid
  - quadruped
  - sim-to-real
---

# TL;DR: Promising Research Directions: Locomotion — Bipedal & Quadruped

> [!info] What this is
> A skimmable TL;DR of [[Locomotion|Promising Research Directions: Locomotion — Bipedal & Quadruped]]. Per direction: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[Locomotion-ELI5|ELI5]].

> [!abstract] Overview
> A legged robot must act on what it cannot directly sense: terrain friction, ground height ahead of the swing foot, payload, contact, and model error are available in sim but absent on hardware, so a deployable policy must recover or bound that privileged state from proprioception, exteroception, or a learned model. Across 8 directions in 2 clusters, the non-consensus bet is that the lever is the *mechanism that extracts more from each step* — feasible references over more demonstrations, anticipatory perception over reactive recovery, off-policy reuse and world-model imagination over PPO rollout-discard — not more data, more scale, or more domain randomization.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A — Bipedal Locomotion & Dynamic Skills | A1–A5 | High-DoF whole-body balance under partial observation, where flat RL fails and the reference/constraint structure is the lever |
| B — Quadruped Locomotion & Real-World Adaptation | B1–B3 | Recovering or bounding the unobserved physical state (μ, h, payload, model error) for deployable locomotion |

## A — Bipedal Locomotion & Dynamic Skills
*The humanoid's legs — whole-body balance and locomotion under partial observation, plus the dynamic agile skills (terrain traversal, parkour, dance, fall-recovery) that make a humanoid more than a slow walker. Where flat RL fails and the reference/constraint structure is the lever.*

### A1 — Perceptive Terrain Traversal & Vertical Mobility
> [!abstract] The bet
> A policy that *fuses* online reference generation (G1 WBC-Gen+Track-style) with learned active gaze (TAGA-style) beats both gaze-alone and generation-alone, and concentrates its win where the height-scan is sparse: on stepping-stone / wide-gap tasks (≥70 cm spacing) the fused policy holds ≥0.95 SR at ≤40% of the full-scan compute, while on dense rough terrain it ties full-scan within 2 pp; and there is an *interior-optimal reference horizon* — SR is non-monotone in horizon under ~0.5 m perturbation (PHP-class).

**Why** — A humanoid clearing a 75 cm box must commit its swing trajectory before the foot touches, so it needs the local geometry ahead — but the geometry is *sparse*: a few load-bearing footholds carry the decision while most of the height-scan is irrelevant. First principle: feasible foot-placement depends on local geometry ahead of the swing foot, and that signal must be *perceived*, not felt. The perceptive-beats-blind battle is settled (PRIOR-Loco 100% traversal, G1 WBC-Gen+Track's 0.962-vs-0.230 box-climb, Deep WB Parkour 100% on a 1.2 m OOD range); the unsettled question is *what to look at, over what horizon* — every consensus policy pays for a full fixed-horizon scan, and TAGA shows learned gaze matches that at 65.2% lower cost.

**First-principles** — *Principle:* a fixed full scan over a fixed horizon spends equal capacity everywhere and equal staleness under disturbance, but only a few footholds matter. *Challenged:* the consensus that a fixed full height-scan over a fixed receding horizon is the right perceptive interface (PRIOR-Loco, G1 WBC-Gen+Track's 0.5 s fixed horizon, Deep WB Parkour) — all won against blind trackers but consume the whole scan; TAGA proves the attention half cheap. *Wager:* fusing online reference generation with learned where-to-look concentrates compute on sparse footholds, and there is a non-monotone horizon curve (anticipation helps, stale references hurt under disturbance).

**Sharpest questions** — 1) Four-arm comparison (blind / gaze-alone / generation-alone / gaze+generation) at matched compute on sparse stepping-stones — does fusion hold ≥0.95 SR at ≤40% full-scan compute? 2) Sweep the 0.5 s generation horizon against ~0.5 m perturbation — is there an interior-optimal horizon (non-monotone SR), or does SR rise monotonically? 3) Does TAGA's gaze close the most cost gap precisely on distant/sparse footholds and tie full-scan on dense terrain?

> [!warning] Risks
> - Perception failure is catastrophic, not graceful (a depth dropout mid-vault can be fatal) → require a DWL-class proprioceptive safety mode underneath (couples to A3); report fall rate under induced dropout.
> - Generated references can be infeasible → use G1 WBC-Gen+Track-style RL fine-tuning to filter; report the tracker's reject/clamp rate, not just headline SR.
> - Parkour-class skills (1.25 m walls, 3.41 m/s vaults) risk hardware damage → bound claims to validated platforms; report contact-force and motor-temperature (couples to A4).

### A2 — Dynamic Agile Skills via Physically-Feasible Motion Imitation
> [!abstract] The bet
> On extreme agile-bipedal skills (flips, martial-arts), KungfuBot-style *rejection* + an *adaptive tracking tolerance* (Adaptive Motion Tracking-style) beats a scaled projection-then-track pipeline (SPIDER/Opt2Skill-style) that tracks every projected clip — cutting tracking error to KungfuBot's 53.25 mm (vs >233 mm OmniH2O/ExBody2) and lifting downstream RL to ReActor's 97.45% (G1) at zero penetration, with the gain concentrated on the high-rejection (>30% episode-collapse) tail where a project-everything pipeline silently chases infeasible targets.

**Why** — A human backflip breaks the robot's torque limits, contact timing, and balance margins, so a policy imitating raw mocap optimizes toward a target it physically cannot reach — yet the reflexive recipe is "imitate more human motion." First principle: tracking is only well-posed if the reference lies on the robot's dynamically-feasible manifold, so the first operation is projection $\xi \mapsto \Pi_{\mathcal F}(\xi)$. Feasibility-projection at scale is now the norm (SPIDER projects 2.4 M frames across 9 embodiments at 100% task SR); what is unsettled is whether *rejection* + adaptive tolerance on the untrackable residue beats simply projecting-then-tracking everything.

**First-principles** — *Principle:* asking a policy to track a reference only makes sense if that reference is physically executable; KungfuBot shows *filtering* (not adding data) delivers the 233→53 mm cut. *Challenged:* not that feasibility beats scale (SPIDER, Implicit Kinodynamic Retargeting prove projection scales — they are complements) but the narrower claim that *projecting-then-tracking everything* is enough; SPIDER/Opt2Skill/KDMR project-and-track with no rejection gate. *Wager:* an explicit accept/reject decision plus a tolerance schedule is the lever on the high-rejection extreme-skill tail, and EFGCL's force curriculum can even *grow* the manifold to reach flips PPO cannot learn.

**Sharpest questions** — 1) Three-arm comparison (track-raw / scaled-projection-then-track / rejection+adaptive-tolerance) at fixed FLOPs, split by KungfuBot's rejection ratio — is the win tail-concentrated (>30% episode-collapse), or does scaled projection match it there? 2) Does an adaptive (early-loose/late-tight) tracking factor learn dynamic skills a fixed tolerance cannot? 3) Does EFGCL's force curriculum *recover* skills KungfuBot's filter would reject, so the two compose (filter the trackable, expand the rest)?

> [!warning] Risks
> - Physics-filtering needs an accurate robot model (correction is only as good as the URDF/dynamics) → validate the feasibility manifold against hardware; report the sim-vs-real tracking-error gap.
> - Filtering discards expressive motions → couple with EFGCL-style force-guidance that *expands* feasibility; report the recovered-skill fraction, not just rejection rate.
> - Downstream-RL gains may be task-specific (+15.22 pp may not transfer) → test the feasibility→trainability curve across skill classes, not a single average.

### A3 — Autonomous Fall Recovery as Non-Periodic Whole-Body Control
> [!abstract] The bet
> Injecting a phase-clock / periodic foot-contact prior into a prior-free recovery policy *lowers* arbitrary-config getting-up SR by a measurable margin (≥10 pp) versus the prior-free HUMANUP / HoST formulations; and HUMANUP's two-stage discover/refine and HoST's single-stage multi-critic reach *parity* (within 5 pp) on a matched posture/terrain distribution — confirming the lever is curriculum-shaped exploration, not a specific decomposition, and that gait structure actively hurts.

**Why** — A humanoid that cannot stand up after a fall is not autonomous. Getting-up has no gait cycle, an arbitrary post-fall configuration, and a single binary reward at the end, so the locomotion playbook's inductive biases work *against* it. First principle: fall-recovery has no phase clock and no nominal contact schedule, so the phase-clocked, foot-contact priors that make locomotion well-shaped bias the policy away from the contact-rich ground transitions recovery needs. That learned curriculum-shaped recovery beats a script is consensus (HoST 100% standing, VIGOR beats HoST/FIRM up to 5×); two independent decompositions (HUMANUP's discover/refine over 20,000 postures, HoST's multi-critic that is 0% without it) reach parity, so the open question is *which* structural prior is load-bearing — and whether a gait-like prior actively hurts.

**First-principles** — *Principle:* the sparse-reward landscape needs *some* structural scaffold (HUMANUP single-stage fails to converge; HoST 0% without multi-critic) but a *gait-like* one is the wrong kind. *Challenged:* not that learned curriculum recovery beats a script (HoST, VIGOR, HiFAR, FRASA settle that) but the finer assumption that imposing the locomotion phase-clock/foot-contact prior is neutral — Classical Balance RL already ran the ablation showing the balance-metric structure is needed (93.4% with it, fails to lift off without). *Wager:* the periodic prior should bias against non-periodic ground-up transitions and lower SR; no recovery paper has injected and measured it.

**Sharpest questions** — 1) Inject a phase-clock / foot-contact prior into a prior-free recovery policy — does SR drop ≥10 pp vs prior-free HUMANUP (the untested sharp claim), or is the prior neutral/helpful? 2) Do HUMANUP's two-stage discovery and HoST's multi-critic reach parity (within 5 pp) at matched data, while an unstructured single-stage baseline fails to converge? 3) Wired as A1's fallback when the perceptive policy loses balance, does a unified locomotion+recovery stack complete a multi-obstacle course *including* falls without human intervention?

> [!warning] Risks
> - Recovery motions stress hardware (flailing limbs, ground impacts) → use HUMANUP-style strong regularization (lowers arm-motor temperature); report contact-force and temperature, treat smoothness as a first-class objective (couples to A4).
> - Discovery may find unsafe trajectories → refine discovery into a deployable policy; report the discovery→deployment safety-margin gap.
> - Real falls exceed simulation coverage (20,000 postures may miss adversarial real falls) → report the coverage curve and failure modes by initial-configuration class, not a single average.

### A4 — Embodiment-Grounded Locomotion Constraints (Force, Acoustic, Thermal)
> [!abstract] The bet
> A *single* conditional cost-head (QuietPaw-style CNCP) fed heat + noise + GRF (predicted at QuietWalk's R²≈0.99) *jointly* holds overheating below Thermal-Aware Residual's <10% **and** noise within +1 dBA of QuietWalk's quiet-policy mean at ≤5% task-SR loss; **and** it traces a non-trivial *thermal-vs-acoustic* Pareto front — pushing noise down by ≥3 dBA provably raises peak motor temperature by a measurable margin — that two single-cost heads run independently cannot map.

**Why** — Simulation rewards task success (reach the velocity, climb the box) and silently omits the physical cost the real robot pays: motors overheat, gaits are loud, contact forces spike — deployment-fatal, not cosmetic. First principle: a gait is bounded by hard embodiment limits (motor-temperature ceilings, force limits, noise budgets) that exist *off* the sim reward surface and that *compete* — a quieter gait runs hotter. Single-cost solutions exist (Thermal-Aware Residual drops overheating 70%→<10%, QuietWalk cuts noise 7.17 dBA) and IMF couples one pair (energy + impact, 35% peak-power cut), but nobody regulates the heat∧noise∧force triple jointly or maps the cross-cost trade-off.

**First-principles** — *Principle:* a policy optimizing only task success saturates embodiment limits because nothing penalizes them, until the hardware fails (Thermal-Aware Residual's 70% overheating under standard policies is the direct evidence). *Challenged:* not that embodiment cost is a distinct lever (settled by QuietWalk, Thermal-Aware Residual, QuietPaw, IMF) but that costs are regulated *one-at-a-time* — QuietPaw's single conditional head sweeps noise-vs-agility but never touches heat; IMF couples energy+impact but never noise. *Wager:* the costs are jointly regulable under one head (QuietPaw proves one head can sweep a Pareto front, hypervolume 10.416×10⁻²) and their cross-trade-off (thermal vs acoustic) is real and measurable.

**Sharpest questions** — 1) Extend QuietPaw's single conditional head to take heat + acoustic + force thresholds — does it dominate QuietPaw-on-noise + Thermal-Aware Residual-on-heat run independently, holding both bounds at ≤5% SR loss? 2) Under the joint head, does pushing noise down ≥3 dBA provably raise peak motor temperature (a downward-sloping thermal-vs-acoustic front), or is the front flat? 3) Does QuietWalk's GRF predictor (trained barefoot→high-heels) generalize to unseen interfaces (ice, soft ground) with R² degrading gracefully?

> [!warning] Risks
> - Cost-regulation can degrade task performance (a quiet/cool gait may be slower) → use Thermal-Aware Residual's residual structure to preserve performance; report the cost-vs-task Pareto front, not a single number.
> - GRF/thermal models are platform-specific (R²≈0.99 on one robot may not transfer) → treat cost predictors as per-platform-calibrated and report the transfer gap.
> - Acoustic metrics are environment-dependent (dBA depends on surface/room) → report noise per surface (QuietWalk reports across 4), not a single average.

### A5 — Sample-Efficient Off-Policy & Flow Locomotion Learning
> [!abstract] The bet
> A flow policy (FPO++/PolicyFlow-style) beats a matched Gaussian off-policy learner on gait quality and sim-to-real SR *specifically* on multimodal-contact skills (agile transitions, motion tracking) by a measurable margin, while tying on smooth walking where a Gaussian suffices; **and** at fixed total wall-clock, N fast Humanoid Loco 15min-style (15-min) iterations of reward/curriculum search converge to a better final gait than one AGILE-style (6–25 hr) PPO run.

**Why** — Off-policy-beats-PPO-on-wall-clock is now established (Parallel Q-Learning 2023, SAC Legged Locomotion *closes the gap entirely*, FastTD3 solves HumanoidBench <3 hrs), so the live questions move downstream. First principle: sample efficiency is governed by how often each step informs a gradient update — off-policy replay reuses every transition, PPO discards each rollout after one update, and with locomotion's dense reward and parallel sim the advantage compounds. The two genuinely-open edges are the *flow* axis (does a richer action distribution help on multimodal contact?) and the *iteration* axis (do N fast runs beat one slow run?).

**First-principles** — *Principle:* off-policy reuse compounds where transitions are cheap and individually informative; FastTD3 shows large-batch off-policy + a distributional critic (no complex stabilizers) beats PPO, DreamerV3, and TDMPC2 on wall-clock. *Challenged:* not that off-policy beats PPO (settled background) but the *Gaussian* policy default — a unimodal Gaussian under-fits multimodal contact (which foot, which transition), and PolicyFlow's anti-mode-collapse result + FPO++'s sim-to-real flow gait bet that flow's expressive distribution is the next lever. *Wager:* flow wins concentrate on multimodal contact (not uniformly), and sub-hour training (15-min loop) enables reward/curriculum search PPO's hours-long run cannot afford.

**Sharpest questions** — 1) Flow vs matched Gaussian at matched compute, stratified by contact multimodality — does flow win on agile-contact and tie on smooth walking, or tie everywhere (richer distribution adds nothing)? 2) At fixed total wall-clock, do N fast 15-min iterations of reward/curriculum search converge to a better gait than one PPO run, or does the single run match the iterated search? 3) Does the off-policy wall-clock win *narrow or reverse* on sparse-reward locomotion sub-tasks (fall-recovery-like, A3), bounding the bet to the dense-reward regime?

> [!warning] Risks
> - Off-policy instability on sparse-reward skills (dense-reward advantage may not hold for fall-recovery, A3) → bound the bet to dense-reward locomotion; report where off-policy degrades vs PPO on sparse tasks.
> - Fast-trained policies may be brittle (15-min policies may overfit sim) → both Humanoid Loco 15min and FastTD3 deploy real; report the sim-to-real SR gap, not just sim wall-clock.
> - Consumer-GPU results may not scale to perception (vision policies, A1, cost more) → report wall-clock separately for state-based vs vision-based; the 15-min number is state-based.

## B — Quadruped Locomotion & Real-World Adaptation
*Recovering or bounding the unobserved physical state — terrain friction, ground height, payload, model error — that separates a sim-trained quadruped policy from a deployable one. Proprioceptive robustness, world-model dreaming for few-shot adaptation, and perceptive mapless mobility-to-goal.*

### B1 — Proprioceptive-Only Robustness under Disturbance & Payload
> [!abstract] The bet
> Under a controlled backbone swap (TCN / contrastive-IMC / Transformer / Transformer-XL) at *identical* privileged supervision, *no single backbone* simultaneously matches RMA's 12 kg (80% body weight) payload *and* HIM/TERT's discontinuous-terrain ceiling (≥60% stairs where TCN scores 0%) — there is a measurable payload-vs-terrain trade-off curve, and only an attention/long-context backbone with allocated capacity holds the conjunction at 100 Hz control / 10 Hz adaptation, zero fine-tuning.

**Why** — A quadruped's deployable policy must act on proprioception alone (joint angles, IMU, contact) because sim's privileged context (friction μ, payload m, ground compliance) is unavailable on hardware, and the field's escape routes (a camera, or on-robot fine-tuning) both add cost. First principle: the privileged context shapes how joints and IMU respond, so it leaves a recoverable fingerprint in recent proprioceptive history that a supervised module can regress out. Proprioceptive inference is now mature and *backbone-diverse* (RMA's TCN at 12 kg, DreamWaQ's Beta-VAE, HIM's contrastive embedding, LoadAdapt's explicit estimator); the mechanism is settled — what each backbone *trades* is not, and the payload line and discontinuous-terrain line are studied separately.

**First-principles** — *Principle:* a supervised module can regress proprioceptive history into a context estimate without ever sensing the privileged state (RMA's 10 Hz module sustains 12 kg, zero fine-tuning). *Challenged:* not that proprioceptive inference works (DreamWaQ, HIM, LoadAdapt settle that) but that a *single backbone* holds both heavy payload *and* discontinuous terrain — TERT's 60%-vs-0% stair result proves backbone choice (not signal availability) sets discontinuous-terrain context, yet LoadAdapt caps near 8 kg without the stair contrast. *Wager:* the two axes *trade* — a backbone tuned for one pays on the other unless capacity is allocated for the conjunction.

**Sharpest questions** — 1) Hold supervision fixed, swap TCN ↔ contrastive-IMC ↔ Transformer ↔ Transformer-XL, sweep payload (0→80% body weight) × terrain (flat→stairs) — is there a payload-vs-terrain Pareto, or does one off-the-shelf backbone hold both with no trade-off? 2) Does proprioception match exteroception on *dynamics* context (friction, payload) and only lose on *anticipatory geometry* (gaps, steps), drawing a clean boundary? 3) Does LocoFormer's long-context in-context adaptation match RMA's supervised extrinsics inference *without* a privileged target (trading supervision for context length)?

> [!warning] Risks
> - Proprioception cannot anticipate geometry (a step/gap is invisible until contact) → bound B1 to dynamics-context inference; anticipatory geometry is A1's job — complementary, not competing.
> - Adaptation supervision needs privileged sim → standard for the RMA family; cross-ref [[Sim2Real|Sim2Real]] for the privileged-to-proprioceptive distillation.
> - TCN-vs-Transformer gap may be task-specific (TERT's stair win may not generalize) → run the backbone ablation per-terrain, not a single average.

### B2 — World-Model Dreaming for Few-Shot Real-World Adaptation
> [!abstract] The bet
> At a matched ≤5-trajectory / 15–30-min real budget, a *bounded latent dreamer* (DreamTIP + RWM-U's epistemic penalty, 0.91 ANYmal D) reaches DreamTIP's 100%-vs-10% on a 52 cm climb *and beats reconstruct-then-retrain* (LoopSR's 100% Stair-Up via digital-twin) on held-out terrain by a measurable margin, because dreaming generalizes across the latent where a reconstructed sim overfits the rebuilt geometry.

**Why** — Deep RL needs millions of interactions (impractical on hardware), and the field's two answers (exhaustive domain randomization, extensive on-robot RL) are both inefficient ways to close the sim-to-real dynamics gap. First principle: a learned dynamics model is a *multiplier* on real data — each real transition updates the model, and through imagination generates thousands of synthetic ones, so 5 trajectories become worth thousands (DreamTIP: ~5 trajectories → 100% on a 52 cm climb where a non-dreaming baseline gets 10%). Anti-DR few-shot adaptation is consensus via *two* mechanisms (reconstruct-then-retrain: LoopSR; latent-dreaming: DreamTIP, DayDreamer) — but nobody has run them head-to-head, and neither carries an epistemic bound.

**First-principles** — *Principle:* sample efficiency is governed by model accuracy per real interaction, not raw count. *Challenged:* not that few-shot beats DR (LoopSR, Simulator Adaptation settled that via reconstruction) but that *reconstructing a digital-twin sim and retraining* is the way to spend those few trajectories — reconstruct-then-retrain needs a faithful sim rebuild and carries no uncertainty estimate. *Wager:* latent dreaming extracts more per trajectory, and an epistemic bound (which LoopSR and Simulator Adaptation both lack, supplied by RWM-U) is what makes the tiny budget safe.

**Sharpest questions** — 1) Three-arm comparison at fixed real-data budget (DR-blind / reconstruct-then-retrain / latent-dreaming), adapt on terrain A and evaluate held-out terrain B — does the bounded dreamer beat reconstruct-then-retrain, or do they tie (latent dreaming adds no multiplier)? 2) Does RWM-U's epistemic penalty β have an interior optimum where the discount matches measured long-horizon prediction error? 3) Does DreamTIP's 5-trajectory adaptation overfit the adapted terrain (held-out SR drops measurably), and does the epistemic penalty fix it?

> [!warning] Risks
> - Model error compounds over horizon (long imagined rollouts drift) → use RWM-U's epistemic penalty; report prediction error vs horizon and cap rollout length where uncertainty spikes.
> - 5-trajectory adaptation may overfit the test terrain → report held-out-terrain SR, not just the adapted terrain.
> - Dreaming needs a good simulator for pretraining (garbage-in poisons the model) → stress diverse large-scale pretraining (SimDist); cross-ref [[WAM|WAM]] for substrate quality and [[Sim2Real|Sim2Real]] for the sim side.

### B3 — Perceptive Mapless Locomotion-to-Goal & Traversability
> [!abstract] The bet
> The mapless-memory advantage is *graded by map-friendliness* — the SRU-style mapless-minus-mapped SR gap is near-zero on feature-rich static courses (where Wheeled-Legged NavLoco's map→plan→track is at its best) and *widens monotonically* to ≥20 pp as feature density drops, dynamics rise, and drift accumulates; with SwarmDiffusion-style joint traversability+trajectory and COTRATE cross-platform perception holding the advantage across embodiments.

**Why** — Long-range goal-reaching is the locomotion-to-goal problem (distinct from VLN goal *reasoning* and from manipulation), and the classical map-build → plan → track pipeline is brittle on unstructured terrain (drift, dynamic obstacles, no GPS) — yet that brittleness is *asserted*, not measured against a graded map-friendliness axis. First principle: long-range locomotion-to-goal needs a spatial state that persists across hundreds of control steps *and* a coupling to the gait; an explicit metric map is one lossy realization, and the map→plan→track factoring severs the perception-gait coupling. SRU's learned recurrent spatial state lifts mapless SR 23.5% over LSTM/GRU and transfers zero-shot 100+ m; HiPAN hits 94.7% SR / 83.6 SPL in dead-ends.

**First-principles** — *Principle:* a learned recurrent spatial state ("where have I been, where is the goal relative to me") coupled to the gait beats a lossy metric map under drift and dynamics. *Challenged:* the assumption that goal-reaching factors cleanly into map-build → plan → track, held strongest by map-using stacks like Wheeled-Legged NavLoco (kilometer-scale urban nav, 0 collisions) — SRU's 23.5% mapless gain and HiPAN's dead-end SR bet learned memory beats the factored pipeline where the map breaks first. *Wager:* the advantage is a *function of map-friendliness*, not a constant — near-zero where the map is at its best, widening as terrain degrades.

**Sharpest questions** — 1) Grade courses by map-friendliness (feature density, dynamics, drift) — is the SRU-minus-NavLoco gap near-zero on feature-rich courses and ≥20 pp as terrain degrades (graded), or constant/shrinking (map isn't the weakest link)? 2) Does a SwarmDiffusion-style head that *jointly* infers traversability and generates the trajectory beat a perception-only substrate (COTRATE) plugged into the mapless policy for cross-embodiment goal-reaching (Spot→Husky)? 3) Does SPL drop below SR more on loop-prone courses (exposing mapless looping the SR number hides), and does path conditioning narrow the SPL–SR gap?

> [!warning] Risks
> - Mapless policies can loop or get stuck (revisiting dead-ends without a map) → report SPL alongside SR, not SR alone (HiPAN's SPL catches this).
> - Overlap with the umbrella's VLN direction (high-level goal *reasoning* is VLN territory) → scope this to low-level mapless control + traversability; cross-reference language-instruction goal-reasoning to [[Embodied-AI|Embodied-AI]].
> - Traversability self-supervision needs experience (COTRATE learns from rollouts) → report where cross-platform transfer (Spot→Husky) holds zero-shot vs needs continual learning.
