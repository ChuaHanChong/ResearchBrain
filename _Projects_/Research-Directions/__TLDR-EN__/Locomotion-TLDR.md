---
title: "TL;DR: Promising Research Directions: Locomotion, Bipedal & Quadruped"
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

# TL;DR: Promising Research Directions: Locomotion, Bipedal & Quadruped

> [!info] What this is
> A quick TL;DR of [[Locomotion|Promising Research Directions: Locomotion, Bipedal & Quadruped]]. For each direction: **the bet**, the reasoning, the sharpest open questions, and the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[__ELI5-EN__/Locomotion-ELI5|ELI5]].

> [!abstract] Overview
> A legged robot must act on things it cannot sense. Terrain friction, ground height ahead of the swing foot, payload, contact, and model error exist in sim but not on hardware. So a deployable policy must recover or bound that hidden state, from proprioception, exteroception, or a learned model. 9 directions in 2 clusters. The non-consensus bet: the lever is the *mechanism that extracts more from each step*. Feasible references over more demos. Looking ahead over reacting. Off-policy reuse and world-model imagination over PPO throwing away each rollout. Not more data, scale, or domain randomization.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Bipedal Locomotion & Dynamic Skills | A1–A6 | High-DoF whole-body balance with only partial observation. Flat RL fails here, and the reference/constraint structure is the lever |
| B: Quadruped Locomotion & Real-World Adaptation | B1–B3 | Recovering or bounding the hidden physical state (μ, h, payload, model error) so the policy is deployable |

## A: Bipedal Locomotion & Dynamic Skills
*The humanoid's legs: whole-body balance and walking under partial observation, plus the agile skills (terrain traversal, parkour, dance, fall-recovery) that make a humanoid more than a slow walker. Flat RL fails; the reference/constraint structure is the lever.*

### A1: Perceptive Terrain Traversal & Vertical Mobility
> [!abstract] The bet
> Mix online reference generation (G1 WBC-Gen+Track-style) with learned active gaze (TAGA-style, sensor pointing under limited field of view, not the map-attention that reads a full passive scan more selectively). The mix beats gaze alone and generation alone, biggest where the height-scan is sparse. On stepping-stone / wide-gap tasks (≥70 cm spacing), it holds ≥0.95 SR at ≤40% full-scan *training* compute, a number that must be re-baselined on onboard wall-clock inference latency and elevation-map-noise robustness, the cost the robot actually feels at deploy; on dense rough terrain it ties full-scan within 2 pp. There is also an *interior-optimal reference horizon*: SR is non-monotone in horizon under ~0.5 m perturbation (PHP-class).

**Why**: A humanoid clearing a 75 cm box picks its swing path before the foot lands, and the deciding ground shape is *sparse*, a few load-bearing footholds matter. Perceptive-beats-blind is over (PRIOR-Loco 100% traversal, G1 WBC-Gen+Track's 0.962-vs-0.230 box-climb, Deep WB Parkour 100% on a 1.2 m OOD range). Open: *what to look at, over what horizon*. Consensus pays for a full fixed-horizon scan, but TAGA matches it at 65.2% lower cost.

**First-principles**: *Principle:* a full scan goes stale and wastes effort, yet only a few footholds matter. *Challenged:* that a full receding-horizon height-scan is the right way to perceive. *Wager:* online generation plus learned where-to-look concentrates compute on the footholds that matter; the horizon curve is non-monotone.

**Sharpest questions**: 1) A 2×2 test (fixed full scan vs learned camera-gaze) × (no reference vs online-generated reference) on sparse stepping-stones, with the gaze-by-generation interaction term as the pre-registered primary result: ≥0.95 SR at ≤40% full-scan training compute *and* at matched inference latency? 2) Sweep the 0.5 s horizon against ~0.5 m perturbation: interior-optimal horizon (non-monotone SR)? 3) Does gaze close the most cost gap on sparse footholds and tie full-scan on dense terrain?

> [!warning] Risks
> - Depth dropout mid-vault can be fatal. → Keep a DWL-class proprioceptive safety mode underneath (A3); report fall rate under forced dropout.
> - Generated references can be infeasible. → Filter via G1 WBC-Gen+Track RL fine-tuning; report the tracker's reject/clamp rate.
> - Parkour-class skills (1.25 m walls, 3.41 m/s vaults) damage hardware. → Limit claims to tested platforms; report contact-force and motor-temperature (A4).
> - Three networks (generator, gaze predictor, tracker) compete for one 50 Hz control budget, and the ≤40% figure is a training cost, not deploy latency. → Gate every headline SR on a composed onboard deployment-latency budget, and treat the gaze-generation deadlock (gaze looking away from where the generator then swings into) as a second go/no-go alongside the main test.

### A2: Dynamic Agile Skills via Physically-Feasible Motion Imitation
> [!abstract] The bet
> On extreme agile skills (flips, martial-arts), lead with an *adaptive tracking-tolerance schedule* (Adaptive Motion Tracking/KungfuBot-style), not with rejection. It cuts tracking error to KungfuBot's 53.25 mm (vs >233 mm OmniH2O/ExBody2) and lifts downstream RL to ReActor's 97.45% (G1) at zero penetration. Clip-level *rejection* is a two-sided diagnostic now, not a categorical winner: it adds ≥5 pp only where episode-collapse exceeds 30%, and less than 1 pp on the sub-30% strata. The honest baseline is OmniXtreme's actuation-aware project-everything, which reaches 91.08% overall real-world SR across 24 high-dynamic motions (96.36% on the flips subset) with no clip-level reject gate at all, and even KungfuBot's own lab swapped rejection for relaxed tracking in its own follow-up, KungfuBot2 (92.68% SR).

**Why**: A human backflip breaks the robot's torque, contact, and balance limits, so raw mocap is a target it cannot hit. First step: projection onto the dynamically-feasible manifold, $\xi \mapsto \Pi_{\mathcal F}(\xi)$, now standard at scale (SPIDER projects 2.4 M frames across 9 embodiments at 100% task SR). Open: what to do with the leftovers that stay untrackable, and whether an explicit clip-level accept/reject gate buys anything over projecting-then-tracking everything at scale.

**First-principles**: *Principle:* tracking makes sense only if the robot can do it; KungfuBot's *filtering* gives the 233→53 mm cut. *Challenged:* not that feasibility beats scale, SPIDER and friends prove projection scales just fine. The narrower claim is that *projecting-then-tracking everything* is enough on its own. *Wager:* an adaptive tolerance schedule is the lever on the extreme tail, and clip-level rejection helps only where episode-collapse is already high, not everywhere.

**Sharpest questions**: 1) Five-arm test (track-raw / OmniXtreme-style actuation-aware project-everything / LIMMT-style upstream data-curation filter / Extreme-RGMT-style continual consolidation / rejection+adaptive-tolerance), split by rejection ratio on a shared cross-controller protocol: is rejection's gain concentrated on the tail (>30% episode-collapse) and near-zero below it? 2) Does an adaptive (early-loose/late-tight) tolerance learn skills a fixed tolerance cannot? 3) Does a reference-free policy (GaitSpan/WARL-style, no mocap clip to filter or reject at all) match either arm on the extreme-skill tail, sidestepping the whole projection/rejection/tolerance question?

> [!warning] Risks
> - Physics-filtering is only as good as the URDF/dynamics model. → Check the manifold against hardware; report the sim-vs-real tracking-error gap.
> - Filtering throws away expressive motions. → Pair with EFGCL-style force-guidance that *expands* feasibility; report the recovered-skill fraction.
> - The +15.22 pp downstream-RL gain may not transfer. → Test the feasibility→trainability curve across skill classes, not one average.

### A3: Autonomous Fall Recovery as Non-Periodic Whole-Body Control
> [!abstract] The bet
> Add a phase-clock / periodic foot-contact prior to a prior-free recovery policy, and the getting-up SR from any starting pose *drops* ≥10 pp versus prior-free HUMANUP / HoST. Also, HUMANUP's two-stage discover/refine and HoST's single-stage multi-critic reach *parity* (within 5 pp) on a matched posture/terrain set. So the lever is curriculum-shaped exploration, not one specific breakdown, and gait structure actively hurts.

**Why**: Getting up has no gait cycle, starts from any pose, and gives one binary end reward, so locomotion biases work *against* it: phase-clocked, foot-contact priors push the policy away from the contact-rich ground moves recovery needs (HoST 100% standing, VIGOR beats HoST/FIRM up to 5×). HUMANUP's discover/refine over 20,000 postures and HoST's multi-critic reach parity by different routes.

**First-principles**: *Principle:* the sparse-reward setting needs *some* scaffold (HUMANUP single-stage fails to converge; HoST scores 0% without multi-critic), but a *gait-like* one is wrong. *Challenged:* that adding the locomotion phase-clock/foot-contact prior is harmless; Classical Balance RL needs balance-metric structure (93.4% with it, cannot lift off without). *Wager:* the periodic prior fights the non-periodic ground-up moves and lowers SR.

**Sharpest questions**: 1) Add a phase-clock / foot-contact prior to a prior-free policy: SR drop ≥10 pp vs prior-free HUMANUP? 2) Do HUMANUP's two-stage and HoST's multi-critic reach parity (within 5 pp) at matched data, while an unstructured single-stage fails? 3) Can a combined locomotion+recovery stack finish a multi-obstacle course *including* falls with no human help?

> [!warning] Risks
> - Recovery motions stress hardware (flailing limbs, impacts). → Use HUMANUP-style regularization; report contact-force and temperature, treat smoothness as first-class (A4).
> - Discovery may find unsafe trajectories. → Refine into a deployable policy; report the discovery→deployment safety-margin gap.
> - The 20,000 postures may miss hard real falls. → Report the coverage curve and failure modes by initial-configuration class.

### A4: Embodiment-Grounded Locomotion Constraints (Force, Acoustic, Thermal)
> [!abstract] The bet
> Two things ride together here but answer different questions: the thermal/latency cost gates the whole A1+A2+A3 spine (any parkour or recovery move that overheats a motor is a deployment failure regardless of task SR), while the acoustic/GRF Pareto is a separate cross-cutting substrate bet. Lead with *amortization*: one *threshold-conditioned* cost-head (QuietPaw-style CNCP), fed heat + noise + GRF (predicted at QuietWalk's R²≈0.99), obtains the whole deployment cost-front at **1× training** where N fixed-weight specialist policies need **N× retrainings** to sweep the same operating points. Its two unowned assets: the heat∧noise∧**force** triple in one head (the FORCE axis, predicted GRF, no prior cost policy carries), and the *measured* thermal-vs-acoustic curve as the moat, pushing noise down ≥3 dBA provably raises peak motor temperature. (Not the refuted claim that conditioning is *necessary* to map the front, a swept fixed-weight composite traces it pointwise, and not a claim that the single-head-sweeps-a-Pareto mechanism itself is novel either, QuietPaw and PCHC already run it.)

**Why**: Sim rewards task success and ignores physical cost: motors overheat, gaits are loud, forces spike, deployment-fatal. A gait is bounded by hard embodiment limits (motor-temperature ceilings, force limits, noise budgets) that live *off* the reward surface and *compete*. Single-cost fixes exist (Thermal-Aware Residual drops overheating 70%→<10%, QuietWalk cuts noise 7.17 dBA; IMF couples energy + impact, 35% peak-power cut), and Olaf even co-regulates heat **and** noise in one policy, but with *fixed* weights, no force axis, and no swept trade-off. QuietPaw and, on a humanoid, PCHC already run a single conditional cost-head, and AMOR runs the same weight-conditioned mechanism on character-motion trade-offs, so the head-sweeps-a-Pareto mechanism itself is not new either. None amortize the heat∧noise∧force triple or map the curve.

**First-principles**: *Principle:* a policy optimizing only task success pushes embodiment limits until hardware fails, Thermal-Aware Residual's 70% overheating is the evidence. *Challenged:* not that conditioning is *necessary* (a swept fixed-weight composite maps the same front) and not that the head mechanism is novel (QuietPaw, PCHC, AMOR already run it), but that paying **N× retrainings** for a deployment cost-front is acceptable when thermal costs are hour-scale slow integrators. *Wager:* a threshold-conditioned head amortizes the whole front into 1× training and carries the FORCE axis QuietPaw/IMF/Olaf all lack, and the thermal-vs-acoustic trade-off is real and measurable.

**Sharpest questions**: 1) Does the conditional joint head obtain the cost-front at 1× training where an Olaf-style fixed-weight composite *swept* over ~8 weight vectors needs N×, holding overheating <10% and noise within +1 dBA at ≤5% SR loss? 2) Does pushing noise down ≥3 dBA provably raise peak motor temperature (downward-sloping front), first past a measurement-repeatability check confirming the signal clears the cross-surface/cross-ambient noise floor of the dBA/temperature metrics? 3) Does QuietWalk's GRF predictor work on unseen surfaces (ice, soft ground) with R² dropping gracefully?

> [!warning] Risks
> - A quiet or cool gait may be slower. → Use Thermal-Aware Residual's residual structure; report the cost-vs-task Pareto front, not one number.
> - GRF/thermal models are platform-specific, R²≈0.99 may not transfer. → Calibrate per platform; report the transfer gap.
> - Acoustic metrics depend on surface and room. → Report noise per surface (QuietWalk reports across 4).
> - The thermal/latency axis gates the whole A1+A2+A3 spine, not just a wing of this direction. Parkour (A1) and recovery (A3) already stress motors, and stacking cost estimators competes for the same onboard compute and thermal budget. → Carry the thermal budget as one composed deployment-latency-plus-heat gate on every A1/A2/A3 headline number; keep the acoustic/GRF Pareto as the separate bet.

### A5: Sample-Efficient Off-Policy & Flow Locomotion Learning
> [!abstract] The bet
> Lead with the *safe core*, the fast-iteration axis: at fixed total wall-clock, N fast Humanoid Loco 15min-style (15-min) rounds of reward/curriculum search reach a better final gait than one slow AGILE-style (6–25 hr) PPO run. *Demote* the flow-vs-Gaussian claim to a conditioning-matched sub-study: a flow policy (FPO++/PolicyFlow-style) tested against a Gaussian off-policy learner with *matched mode/phase conditioning* on multimodal contact, the higher-variance bet, where a clean null (conditioning ties flow) is publishable and the question is likely absorbed into a unified architecture within ~a year.

**Why**: Off-policy beating PPO on wall-clock is settled (Parallel Q-Learning 2023, SAC Legged Locomotion *closes the gap entirely*, FastTD3 solves HumanoidBench <3 hrs): replay reuses every transition while PPO discards each rollout, and with dense reward and parallel sim that edge adds up. The fast-iteration axis is the defensible core, sub-hour training makes a reward/curriculum search PPO cannot afford. The flow axis is the contested half, a parallel Gaussian-plus-structure literature (per-gait AMP, MoE) already deploys multi-gait humanoids, so each mode is locally unimodal and a Gaussian may suffice.

**First-principles**: *Principle:* off-policy reuse pays off where transitions are cheap and informative, FastTD3 beats PPO, DreamerV3, and TDMPC2 on wall-clock. *Challenged:* the safe lever is iteration, locomotion's cheap sub-hour training makes the reward/curriculum search a single long PPO run forgoes the genuinely-open, less-crowded edge. *Wager:* N fast runs beat one slow run; flow-vs-Gaussian is a sub-study whose most valuable outcome may be a clean null, since expressive *conditioning* (per-gait AMP, MoE) already handles multi-gait humanoids.

**Sharpest questions**: 1) At fixed wall-clock, do N fast 15-min reward/curriculum rounds beat one PPO run? 2) Flow vs a *conditioning-matched* Gaussian at matched compute, split by contact multimodality: does flow win on agile-contact, or tie (a clean null)? 3) Does the off-policy win *narrow or flip* on sparse-reward sub-tasks (A3)?

> [!warning] Risks
> - The dense-reward edge may not hold for fall-recovery (A3). → Limit the bet to dense-reward locomotion; report where off-policy trails PPO on sparse tasks.
> - Fast-trained policies may overfit sim. → Both Humanoid Loco 15min and FastTD3 deploy on real robots; report the sim-to-real SR gap.
> - Vision policies (A1) cost more on consumer GPUs. → Report wall-clock for state-based and vision-based separately; the 15-min number is state-based.
> - Flow's real cost is onboard *inference* latency, not the training-time figure. → A flow/CNF policy needs multi-step integration every control step; gate the flow sub-study on a composed onboard inference-latency budget against the 50–200 Hz control period, not the <50%-extra training number.

### A6: Regime-Contingent MPC-Learning Coupling for Legged Control
> [!abstract] The bet
> Run the head-to-head nobody has: hold platform, task, and compute fixed, and swap only the coupling type, RL-as-contact-scheduler, RL-residual, learned-differentiable-surrogate, in-loop generative sampler, MPC-as-teacher, plus the pure-RL and pure-MPC endpoints, across a contact-richness × observability × horizon regime grid. No single coupling wins by more than 5 pp of success rate in every cell, and in at least one wide regime the better of pure-RL or pure-MPC ties the best hybrid within 2 pp, so the integration overhead isn't always worth paying.

**Why**: Every hybrid-control paper validates its own coupling against the same two baselines, pure RL and pure MPC, and reports a win, but nobody holds platform and task fixed and swaps only the coupling type against the *other* hybrids. The one paper that runs both pure endpoints on a shared harness already shows they split the axes: RL wins on energy and one disturbance direction, MPC wins the other and lateral stability, neither dominates, exactly the pattern that makes a coupling-level bake-off worth running rather than assuming one architecture is best.

**First-principles**: *Principle:* MPC enforces a dynamics model and hard constraints by construction, so it's reliable where the model is right and the horizon is short; a learned policy compiles experience into a reactive map, so it's fast and robust where the model is wrong or the state is unobserved. Which one matters is regime-indexed (contact-richness, observability, horizon), not universal. *Challenged:* that each lab's chosen coupling is *the* right integration, provable by beating the two pure endpoints; a win over the floor is not a win over a sibling coupling. *Wager:* the best coupling changes with the regime, and the integration overhead is sometimes unjustified.

**Sharpest questions**: 1) Across the regime grid, does the per-cell winner change coupling to coupling, with no coupling's margin over the second-best exceeding 5 pp in every cell? 2) On a well-modelled regime (contact-sparse, full-state, short-horizon), does a pure method tie the best hybrid within 2 pp SR? 3) Under payload/friction shift and partial observability, do the online-adaptive-surrogate and MPC-teacher couplings win the cell while offline-fixed couplings and pure-MPC degrade fastest?

> [!warning] Risks
> - Re-implementing four couplings faithfully is a large engineering surface, and a weak arm fakes a regime-contingent result for implementation reasons, not architectural ones. → Reproduce each coupling against its own paper's reported number on its own platform first, as a validity gate before the cross-coupling grid.
> - The endpoints and couplings don't share a platform today (MIT Humanoid, Centauro, Go1/Go2 are all different). → Port every arm onto one shared platform and metric contract; treat any result that needs a different platform as out of scope.
> - Matched compute is ambiguous between training and inference, a coupling can win on training-sample efficiency yet lose on onboard latency once an MPC solve is in the loop. → Fix both a training wall-clock budget and an onboard inference-latency budget; report success under each separately.

## B: Quadruped Locomotion & Real-World Adaptation
*Recovering or bounding the hidden physical state, friction, ground height, payload, model error, between a sim-trained quadruped policy and a deployable one. Covers proprioceptive robustness, world-model dreaming for few-shot adaptation, and perceptive mapless mobility-to-goal.*

### B1: Proprioceptive-Only Robustness under Disturbance & Payload
> [!abstract] The bet
> Make the durable contribution the **diagnostic**: a stratified payload(0→80% body weight) × discontinuous-terrain protocol that maps the payload-vs-terrain trade-off *curve*, not the verdict on which backbone wins. Under a controlled backbone swap (TCN / contrastive-IMC / Transformer / Transformer-XL) at *identical* privileged supervision, the curve shows *where* each backbone trades RMA's 12 kg (80% body weight) payload against HIM/TERT's discontinuous-terrain ceiling (≥60% stairs where TCN scores 0%), with the 80%-payload stratum as the unowned cell. (The which-backbone-wins verdict is fragile, TAR already holds both axes in one zero-shot demo.)

**Why**: A deployable quadruped runs on proprioception alone; sim's privileged context (friction μ, payload m, ground compliance) is unavailable on hardware, and the two escapes (a camera, or on-robot fine-tuning) both add cost. Proprioceptive inference is mature across *many backbones* (RMA's TCN at 12 kg, DreamWaQ's Beta-VAE, HIM's contrastive embedding, LoadAdapt's explicit estimator). The mechanism is settled; what each backbone *trades* is not. TAR already holds 12 kg payload, 150 N pushes, and discontinuous steps zero-fine-tune on a real Go2 in one model, but its own backbone swap covers only {contrastive-recurrent, MLP, TCN}, no Transformer or Transformer-XL, so it says nothing about whether attention wins the conjunction.

**First-principles**: *Principle:* a supervised module turns proprioceptive history into a context estimate, RMA's 10 Hz module holds 12 kg with zero fine-tuning. *Challenged:* not that the payload-and-terrain conjunction is unreachable, TAR already holds both in one model. The gap is narrower and about *measurement*: the payload line (RMA/LoadAdapt) and the discontinuous-terrain line (TERT/HIM) are studied separately, and nobody has run a controlled backbone swap under identical supervision to map how the two axes trade. *Wager:* under that controlled swap, the two axes *trade* and an attention/long-context backbone with allocated capacity sits highest on the curve, beating a contrastive-recurrent backbone by ≥5 pp joint SR at the matched 80%-payload/stairs stratum.

**Sharpest questions**: 1) Hold supervision fixed, swap TCN ↔ contrastive-IMC ↔ Transformer ↔ Transformer-XL; sweep payload (0→80% body weight) × terrain (flat→stairs): a payload-vs-terrain Pareto? 2) Does proprioception match exteroception on *dynamics* context and only lose on *anticipatory geometry* (gaps, steps)? 3) Does LocoFormer's in-context adaptation match RMA's supervised inference *without* a privileged target?

> [!warning] Risks
> - Proprioception cannot see geometry ahead, a step or gap is invisible until contact. → Limit B1 to dynamics-context inference; geometry ahead is A1's job.
> - Adaptation supervision needs privileged sim. → Standard for the RMA family. Cross-ref [[Sim2Real|Sim2Real]] for the privileged-to-proprioceptive distillation.
> - The TCN-vs-Transformer gap may be task-specific, TERT's stair win may not transfer. → Run the backbone ablation per-terrain, not as one average.

### B2: World-Model Dreaming for Few-Shot Real-World Adaptation
> [!abstract] The bet
> *Check the bound before trusting it.* An epistemic-uncertainty estimate that looks calibrated in sim can decorrelate from true held-out error once sim-to-real drift sets in, so before committing to dreaming-as-core, confirm the estimate stays calibrated under drift. If that check passes: give it a small budget, ≤5 trajectories / 15–30 min of real data. A *bounded latent dreamer* (DreamTIP + RWM-U's epistemic penalty, 0.91 ANYmal D) reaches DreamTIP's 100%-vs-10% on a 52 cm climb, and *beats reconstruct-then-retrain* (LoopSR's 100% Stair-Up via digital-twin) on held-out terrain: dreaming generalizes across the latent, while a reconstructed sim overfits the rebuilt geometry. If the check fails, dreaming-as-core is premature and reconstruct-then-retrain is the safer default.

**Why**: Deep RL needs millions of interactions; the field's two answers (heavy domain randomization, on-robot RL) both waste them. A learned dynamics model is a *multiplier*: each real transition updates the model, which imagines thousands, so 5 trajectories become worth thousands (DreamTIP: ~5 → 100% on a 52 cm climb where a non-dreaming baseline gets 10%). Anti-DR few-shot adaptation is consensus through *two* mechanisms, reconstruct-then-retrain (LoopSR) and latent-dreaming (DreamTIP, DayDreamer), but nobody has run them head-to-head, and neither has an epistemic bound whose validity has actually been checked.

**First-principles**: *Principle:* sample efficiency depends on model accuracy per interaction, not raw count. *Challenged:* whether *rebuilding a digital-twin sim and retraining* is the right way to spend the trajectories; it needs a faithful rebuild and gives no uncertainty estimate. *Wager:* once instrumented as calibrated, latent dreaming gets more from each trajectory than reconstruct-then-retrain, and the epistemic bound (lacked by LoopSR and Simulator Adaptation, claimed by RWM-U) is what should make the tiny budget safe, conditional on that calibration check, not assumed from it.

**Sharpest questions**: 1) Does the epistemic-uncertainty estimate stay calibrated under sim-to-real drift, tracking measured held-out model error as drift grows, rather than decorrelating from it (an unverified report claims the estimate can decorrelate on this model family)? This gates everything else. 2) Three-arm test at fixed real-data budget (DR-blind / reconstruct-then-retrain / latent-dreaming); adapt on A, test on held-out B: does the bounded dreamer win? 3) Does RWM-U's epistemic penalty β have an interior optimum matched to long-horizon prediction error? 4) Does DreamTIP's 5-trajectory adaptation overfit the adapted terrain, and does the penalty fix it?

> [!warning] Risks
> - The epistemic estimate may not be calibrated under drift, a bound that looks fine in sim can end up regulating noise once real-world drift sets in. → Run the calibration-under-drift check first and gate the dreaming-vs-reconstruction commit on it; default to reconstruct-then-retrain if it fails.
> - Long imagined rollouts drift. → Use RWM-U's epistemic penalty; report prediction error vs horizon, cap rollout length where uncertainty spikes.
> - 5-trajectory adaptation may overfit. → Report held-out-terrain SR, not the adapted terrain.
> - Dreaming needs a good pretraining simulator. → Push diverse large-scale pretraining (SimDist). Cross-ref [[WAM|WAM]] for substrate quality, [[Sim2Real|Sim2Real]] for the sim side.

### B3: Perceptive Mapless Locomotion-to-Goal & Traversability
> [!abstract] The bet
> The mapless-memory advantage *scales with how map-friendly the course is*. The SRU-style mapless-minus-mapped SR gap is near-zero on feature-rich static courses, where Wheeled-Legged NavLoco's map→plan→track works best. The gap *grows* to ≥20 pp as features get sparse, dynamics rise, and drift builds up. SwarmDiffusion-style joint traversability+trajectory and COTRATE cross-platform perception keep this advantage across embodiments.

**Why**: The classical map-build → plan → track pipeline is brittle on rough terrain (drift, moving obstacles, no GPS) and cuts the link between perception and gait, but that brittleness is *claimed*, not measured against a graded map-friendliness axis. SRU's learned recurrent spatial state lifts mapless SR 23.5% over LSTM/GRU, transfers zero-shot 100+ m; HiPAN hits 94.7% SR / 83.6 SPL in dead-ends.

**First-principles**: *Principle:* a learned recurrent spatial state ("where have I been, where is the goal relative to me"), tied to the gait, beats a lossy metric map under drift and dynamics. *Challenged:* that goal-reaching splits cleanly into map-build → plan → track; Wheeled-Legged NavLoco holds this strongest (kilometer-scale urban nav, 0 collisions), but SRU's 23.5% gain and HiPAN's dead-end SR bet memory wins where the map breaks first. *Wager:* the advantage is a *function of map-friendliness*, not constant.

**Sharpest questions**: 1) Grade courses by map-friendliness (feature density, dynamics, drift): SRU-minus-NavLoco gap near-zero on feature-rich and ≥20 pp as terrain degrades? 2) Does a SwarmDiffusion-style head that *jointly* infers traversability + trajectory beat a perception-only substrate (COTRATE) for cross-embodiment goal-reaching (Spot→Husky)? 3) Does SPL drop below SR more on loop-prone courses, and does path conditioning narrow the gap?

> [!warning] Risks
> - Mapless policies can loop or get stuck. → Report SPL next to SR, not SR alone (HiPAN's SPL catches this).
> - High-level goal *reasoning* is VLN territory. → Scope this to low-level mapless control + traversability; cross-reference language-instruction goal-reasoning to [[Embodied-AI|Embodied-AI]].
> - Traversability self-supervision needs experience, COTRATE learns from rollouts. → Report where cross-platform transfer (Spot→Husky) holds zero-shot vs needs continual learning.
