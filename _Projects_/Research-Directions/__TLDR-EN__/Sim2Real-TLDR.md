---
title: "TL;DR: Sim-to-Real & Real-to-Sim Transfer"
aliases:
  - "Sim2Real TL;DR"
  - "Sim2Real skim"
tags:
  - tldr
  - sim-to-real
  - real-to-sim
  - embodied-AI
---

# TL;DR: Sim-to-Real & Real-to-Sim Transfer

> [!info] What this is
> A skimmable TL;DR of [[Sim2Real|Sim-to-Real & Real-to-Sim Transfer]]. Each direction gives **the bet**, the reasoning, the sharpest open questions, and the risks. Full detail stays in the source. Plain-language version: [[__ELI5-EN__/Sim2Real-ELI5|ELI5]].

> [!abstract] Overview
> People treat the reality gap as one forward problem: train in sim, lose on real hardware, fix with more domain randomization. That hides two facts. First: how well you run reality *backward* into the simulator (real→sim) limits how well it predicts reality *forward*. Second: whatever gap survives every offline fix shows up only at deploy-time, where an un-handled remainder is a *safety* failure, not a lost success. The bet: **the realism you optimize is not the transfer you want**: on the load-bearing axes (controller gains, DR marginalization, fidelity proxies) the two are anti-correlated. So the field that *estimates and inverts* beats the one that *randomizes and renders*.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Forward Sim-to-Real: Robustness Beyond DR | A1–A3 | DR randomizes appearance, not the *causes* of outcomes, semantics, physics rewards, control structure are what transfer |
| B: Real-to-Sim-to-Real: Grounding the Simulator | B1–B4 | Recovering appearance + dynamics $(\phi^\star, \psi^\star)$ from real data is the new bottleneck, and a *chosen* law caps it |
| C: Reality-Gap Measurement as Inference | C1–C2 | High in-distribution r, untested under deliberate shift, no provable bound |
| D: Deployment-Time Adaptation | D1–D3 | The residual $\delta(t)$ that survives A/B/C is time-varying and observable only at deploy-time |
| E: Risk-Bounded Deployment: Safety Under the Irreducible Gap | E1–E3 | An un-handled residual is a *safety* failure, not just a performance one |

## A: Forward Sim-to-Real: Robustness Beyond Domain Randomization
*Attack the forward gap directly. Transfer what stays the same, object semantics, physics-grounded rewards, control structure, not pixels around an unchanged cause.*

### A1: Hybrid Neural-Rendering + Physics Simulators for Semantic Sim-to-Real
> [!abstract] The bet
> Build a 3DGS-in-the-loop simulator that re-samples affordance and material *semantics per episode*, in the loop, not once at asset time. This lifts affordance-task real SR **>20 pp over AffordSim's ~24% appearance-only ceiling**, beats Digital-Cousins-style fixed-cousin randomization at matched render budget, and pushes mug-hang-class tasks toward HyperSim's 95%-with-few-real regime at GS-Playground throughput (10,000 FPS).

**Why**: DR perturbs lighting, texture, and pose, but a mug's handle-affordance survives every appearance change, DR's axis and the policy's are orthogonal.

**First-principles**: *Principle:* affordances, mass, and material cause outcomes; pixels are downstream. *Challenged:* not "randomize the cause not the effect" (Digital Cousins, 90% vs 25%) but the offline-asset-time-only assumption behind RoboTwin 2.0 / ViserDex / Digital Cousins, AffordSim hits 98/79/64% collection yet caps ~24% zero-shot. *Wager:* re-sample the cause per episode, in-loop.

**Sharpest questions**: 1) Does affordance/material randomization add real-SR on top of fidelity (semantic main-effect survives at high PBR)? 2) Does per-episode in-loop re-sampling beat fixed-cousin at matched diversity? 3) Can VoxAfford auto-label assets well enough to drop hand annotation?

> [!warning] Risks
> - In-loop rendering is compute-heavy → GS-Playground point-pruning + batch rendering; drop auxiliary heads at deploy.
> - Semantic ground truth is scarce → bootstrap from VoxAfford auto-labeling.
> - Gains may confound with realism → ablate semantics-vs-appearance at fixed PBR.

### A2: Reward-Signal Sim-to-Real: Transferring PINN-Estimated Physics Rewards, Not Actions
> [!abstract] The bet
> A physics-law-grounded reward (GRF, contact wrench) keeps its objective across *contact-dynamics* shifts where a *learned* reward drifts. It holds QuietWalk's **R²=0.99 sensor-free** accuracy and the **−7.17 dBA** objective across **4 footwear types** and outdoor terrains, where a Video-Language-Critic-style reward and a VIRAL-style DR action policy both lose it.

**Why**: Most pipelines harden the *action* mapping, inheriting the dynamics they were hardened on. Reward transfer is mature (XIRL, DARL, Video-Language Critic, DrEureka), but each is *learned*, drifting under the shift it should survive.

**First-principles**: *Principle:* actions are distribution-bound; physics-grounded rewards are distribution-free. *Challenged:* the learned-reward orthodoxy, the novelty is *distribution-free*. *Wager:* QuietWalk's inverse-dynamics *constraint* drives the 82–86% GRF-error reduction and R²=0.99.

**Sharpest questions**: 1) Does the physics-law reward beat a learned reward (and action transfer) on cross-condition retention, widest under the hardest shift (high heels)? 2) Does removing the inverse-dynamics constraint collapse R² toward 0.39/0.67? 3) Does the advantage vanish on semantic tasks?

> [!warning] Risks
> - PINN rewards exist for few quantities → bound to contact/force-dominated tasks with a conservation law.
> - Reward transfer ≠ policy transfer → pair with Self-Adapting RL's online fine-tune.
> - PINN degrades off-manifold → measure the trust envelope (H4); gate on residual, fall back where R² drops.

### A3: Controller-Gain-Aware Sim-to-Real: Co-Optimizing Dynamics and Control
> [!abstract] The bet
> Co-optimize $(K_p, K_d)$ *jointly with* the dynamics distribution, capturing a non-empty **gain×dynamics interaction term**: joint beats (gain-only + dynamics-only) by **more than their sum** on AutoMate-class contact tasks. The co-optimized DR variable also beats a DexCtrl/TAM-style runtime gain residual at matched SR.

**Why**: The field treats gains as a fixed property, or tunes them for low sysID error. But the gain is an unrecognized sim-to-real hyperparameter, setting training dynamics, smoothness, and oscillation at once. Tune-to-Learn shows the *lowest*-sysID-error (stiff) gains give the *worst* transfer; RL reaches 99%+ only with per-gain tuning.

**First-principles**: *Principle:* the controller is part of the plant; gains set closed-loop dynamics, so they belong in the transfer distribution. *Challenged:* not "gains belong in randomization" (routine DR) but that gain and dynamics randomization are *separable*, Tune-to-Learn's sysID-vs-transfer inversion implies coupling. *Wager:* sequential or residual recipes leave a joint term only co-optimization captures.

**Sharpest questions**: 1) Does joint beat gain-only + dynamics-only (a super-additive gain×dynamics term)? 2) (Falsifier) Do co-optimized DR-variable gains beat a runtime adaptive-gain predictor / torque residual at matched SR? 3) Is the effect contact-specific (~null on free-space)?

> [!warning] Risks
> - Co-optimization explodes the search space → seed a narrow compliant/overdamped prior from Tune-to-Learn.
> - Co-optimized values may be infeasible → constrain to the hardware's admissible gain box.
> - Effect may be task-specific → scope to contact-rich tasks (AutoMate/NIST); report the free-space null.

## B: Real-to-Sim-to-Real: Grounding the Simulator in Deployment
*Invert reality into the simulator first. Recover appearance and dynamics from real data, and forward transfer comes nearly for free, a simulator predicts reality forward no better than it captured it backward.*

### B1: Closing the Real-to-Sim Gap: Reconstruction Fidelity as the New Bottleneck
> [!abstract] The bet
> The headline is a *within-object causal* test, not a cross-object correlation: degrading *the same object's* reconstruction in controlled steps **monotonically lowers that object's forward r** (a cross-object regression conflates fidelity with per-object difficulty). The commit gate is **H5**: even at r>0.9 from joint appearance+physics inversion, REALM's control-dynamics misalignment caps the rest, and only co-optimizing control alignment (links A3) recovers that residual, if the within-object slope holds *and* the control term closes a measurable residual, the "reconstruction fidelity is the new bottleneck" thesis commits; if either fails, the direction de-risks to the observational law. The joint-inversion advantage is **widest on deformables** (Real-to-Sim GS 0.901 vs Isaac Lab 0.237 on rope, 0.915 vs 0.649 push-T), the regime the navigation counter-example skips.

**Why**: Name a real-to-sim gap separate from the forward one (REALM) and the arrow flips: forward correlation is capped by inversion fidelity. The joint-inversion *engine* is consensus (Splatting Physical Scenes, One-Shot Real-to-Sim, TwinAligner, D-REX); the bottleneck is the *law* mapping fidelity to r, and whether that law is a within-object *cause* or a confounded cross-object correlation.

**First-principles**: *Principle:* a simulator predicts reality forward no better than it captured it backward, $\text{Gap}_{\text{S2R}}$ is lower-bounded by $\text{Gap}_{\text{R2S}}$. *Challenged:* not "invert jointly" (consensus) but that fidelity *monotonically* and *causally* predicts forward transfer; Lower-Fidelity Sim2Real broke it (lower fidelity gave *higher* transfer in navigation). *Wager:* the bound is joint-reconstruction-bound (Real-to-Sim GS), so the within-object fidelity→r slope must be *measured*, not inferred from a cross-object fit.

**Sharpest questions**: 1) (Headline) Does degrading *one object's* reconstruction in controlled steps monotonically lower *that object's* forward r, the within-object causal slope a cross-object regression cannot give? 2) (Commit gate) Does control-dynamics misalignment (REALM) cap correlation even at r>0.9, and does co-optimizing control alignment (A3) close a measurable residual, the go/no-go for the causal-ceiling thesis? 3) Is the inversion advantage widest on deformables (the r>0.9 bet per class), and can the law rank twins offline before any rollout?

> [!warning] Risks
> - Reconstruction is per-scene expensive → amortize with generative priors (WorldComposer); reuse twins.
> - Gap to Isaac Lab is widest on deformables → scope the >0.9 bet across rigid and deformable; report per-class delta.
> - The >20 pp / per-cell-r margins sit near the real-robot noise floor → at REALM-class N~50 a 20 pp difference is only ~2–3 binomial SE, so pre-register a bootstrap-CI / minimum-detectable-effect power check before the ablations, or report underpowered rather than positive.

### B2: Amortized Differentiable System-ID: Zero-Per-Object Gradient sysID in Clutter
> [!abstract] The bet
> Train an amortized observation→parameter network on differentiable-sim rollouts. It recovers constitutive parameters for **unseen objects in clutter at zero per-object demos**, reproducing the gradient-sysID-vs-DR-on-OOD advantage (D-REX 9–10/10 vs DR 4–9/10 below DR support) **on objects it never saw**. The falsifier is the *SR-vs-parameter-distance frontier*.

**Why**: Gradient sysID through a differentiable simulator is solved (D-REX recovers mass to 4.8–12.0% error, beats DR off-support). But every loop runs *per object* from demos (≥20/object, mass only), so it can't identify a novel object in clutter.

**First-principles**: *Principle:* the inverse map can be amortized, trained once on diff-sim rollouts, it infers a novel object's parameters in one forward pass. *Challenged:* that per-object gradient recovery is the unit of sysID (D-REX/DOT-Sim/PhysTwin/One-Shot re-optimize per object). *Wager:* Offline Domain Randomization proves DR *is* MLE of a parameter distribution, so one corpus trains the inverse map.

**Sharpest questions**: 1) Does amortized inference match D-REX's per-object recovery at zero demos, and beat DR off the prior support on the SR-vs-distance frontier? 2) Does it scale to clutter (one pass for N objects) where per-object loops cost N? 3) Does a full vector (mass+friction+stiffness) amortize, not just mass?

> [!warning] Risks
> - Amortized inference may not transfer past training → train on a wide diff-sim corpus; fall back to per-object D-REX when low-confidence.
> - Differentiable sims exist for few regimes → generate the corpus in DOT-Sim/PhysTwin's deformable/soft-contact regime.
> - Clutter breaks the observation→parameter map → condition on segmented per-object observations; gate on segmentation confidence.

### B3: Bidirectional Sim↔Real Co-Training: The Twin as a Data Engine, Not a Sandbox
> [!abstract] The bet
> The *primary* endpoint is **gate-metric validity**: does sim-real reconstruction-fidelity r actually predict per-fold SR gain? Log (Δr, ΔSR) per fold and report their Spearman rank-correlation with a bootstrap CI, with the **null pre-registered** (Δr and ΔSR rank-uncorrelated, so the fidelity gate is arbitrary). Only conditional on a positive correlation does the secondary claim carry: a per-task object-grounded fold-back loop **gated on that B1 fidelity check** improves *monotonically across N rounds* where the same loop *ungated* drifts, the per-round gain *scaling with the reconstruction-fidelity exchange rate* (Real-is-Sim 30 sim ≈ 30 real, 57%→80%). Reproduce RialTo's 90%-vs-10% grounding advantage and HyperSim 75%→95% per round, beating Arcadia's single feedback-on/off delta (LIBERO 88.5 vs 86.9).

**Why**: Most of the corpus uses twins as sandboxes; the highest-leverage results use them as *data engines* (RialTo, HyperSim, RoboTwin 2.0). The closed loop is now *claimed* (Arcadia states B3's falsifier verbatim), but its evidence is a single feedback-on/off pass at scene/lifecycle scale, not a per-task object twin over *successive* rounds, and nobody has checked the unmeasured premise the whole gate rests on: that the fidelity score tracks downstream value.

**First-principles**: *Principle:* a twin grounded in real reconstruction generates data from the *correct* distribution, so its samples are training-valid, not just test-valid (RialTo's 90% target-twin vs 10% generic). *Challenged:* not "closed loop beats one-shot" (Arcadia claims it) but that fold-back is *unconditionally* self-improving, each fold re-reconstructs from imperfect data and can drift. *Wager:* gating each fold on a B1 check keeps the loop monotone, but only if Δr actually predicts ΔSR, so that gate-validity is the result to settle first.

**Sharpest questions**: 1) (Primary endpoint) Does per-fold Δr (reconstruction-fidelity change) rank-predict per-fold ΔSR, against a pre-registered null, so the fidelity gate is well-posed at all? 2) Conditional on that, does a per-fold fidelity gate keep the loop monotone over successive rounds where the ungated one drifts, the gap widening each round (Arcadia showed it once, at lifecycle scale)? 3) Does the sim:real exchange rate scale with reconstruction fidelity?

> [!warning] Risks
> - The per-round monotone trend sits below the real-robot noise floor → at REALM-class N~50 per round, a small per-fold ΔSR cannot be resolved from binomial sampling noise (SE ≈ 7 pp at 50% SR), so pre-register the per-round ΔSR MDE and the Δr–ΔSR rank-correlation gate before claiming monotonicity, or report the trajectory as power-limited.
> - Closed-loop can drift → gate each fold on a B1 fidelity check; reject folds that lower sim-real r.
> - Co-training balance is delicate → tune the sim:real ratio per Real-is-Sim's 1:1 and HyperSim's 35-demo regime.

### B4: Generalizable Constitutive-Law Inversion: Learning the Physics, Not Just the Parameters
> [!abstract] The bet
> A learned constitutive law beats a parameter-only fit (e.g. PhysTwin) **on held-out geometry up to 1M particles**, reproducing NCLaw's order-of-magnitude extrapolation advantage and <1e-3 loss. It also survives a **closed robot real→sim→real loop**: dropped into Real-to-Sim GS's pipeline in place of the fixed soft-body model, it holds forward correlation across material variation a parameter fit cannot cover.

**Why**: B2 recovers the *parameters* of a law the engineer chose, capping generalization at the functional form. NCLaw embeds a *neural* constitutive law in a differentiable MPM; MASIV makes learn-the-form-from-video *consensus*. Two deltas stay unattacked: the learned-law-vs-parameter-fit advantage *on held-out geometry* (MASIV never isolates it), and the *closed robot loop* (neither supplies it).

**First-principles**: *Principle:* a material's motion is caused by its constitutive law (the stress-strain map), not the scalars of any parameterization; conservation laws are universal, the constitutive law the only material-specific DOF. *Challenged:* not "learn the form from video" (MASIV/UniPhy/Physics-Informed-Deformable-GS do it) but that learning the form is *itself* the contribution, leaving geometry-extrapolation and robot-loop untested. *Wager:* the form, not the parameters, binds extrapolation (NCLaw).

**Sharpest questions**: 1) (Front line) Does learned-law extrapolation beat a parameter fit on held-out geometry up to 1M particles, the delta MASIV skips? 2) Does a learned law survive the full real→sim→real loop across materials a parameter fit can't? 3) Are NCLaw's structural priors (rotation-equivariance, undeformed-equilibrium) load-bearing off-manifold?

> [!warning] Risks
> - Recovery is solved; the robot loop is not → the learned-law-into-loop test (H2) is the go/no-go.
> - Learned laws can violate physics off-distribution → keep NCLaw's structural priors as hard constraints; gate on conservation-law residuals.
> - Differentiable MPM is mature for soft bodies, not rich contact → scope the 1M-particle bet to elastoplastic/fluid materials.

## C: Reality-Gap Measurement as Statistical Inference
*Stop asking "is the sim accurate?" Ask "what can I provably infer about real performance from imperfect sims?" A correlation is a validity claim; a portfolio of biased sims is a variance-reduction estimator.*

### C1: Per-Factor Correlation Validity as a Deployment Gate: Stress-Test, Then Route
> [!abstract] The bet
> Build a per-(sim, factor) trust map, the *correlation* re-measured under each COLOSSEUM factor, ingesting REALM's validated rows, as a deployment *router*. This lifts Sim2Real Betting's **70–100% win rate** over its single-global-edge baseline on shift-mixed deployment, and recovers SureSim's **20–25%** real-trial reduction by skipping untrusted cells.

**Why**: Today's correlations (SIMPLER r≥0.85, VISER 0.92, WorldMark ρ>0.9) are all *in-distribution*. COLOSSEUM shows single perturbations cause 30–50% SR drops per factor; MolmoSpaces reports per-factor *SR sensitivities*, not *correlation*. Nobody builds a router.

**First-principles**: *Principle:* a correlation only vouches for the sim under the conditions measured; trustworthiness is one number *per perturbation factor*. *Challenged:* not "one in-distribution r proves the sim usable" (conceded) but that diagnosis ends at *success-drop sensitivities* and a *global* edge. *Wager:* a per-factor map routes deployment where one global r cannot.

**Sharpest questions**: 1) Does per-factor correlation (not SR sensitivity) fall below r<0.7 for the worst factors (distractors/color/lighting) even where global r is high? 2) Does a per-(sim, factor) gate beat single-global-edge selection? 3) Under some perturbation, does sim r flip negative?

> [!warning] Risks
> - Stress-test and gate need paired sim+real OOD data → reuse REALM's 15-perturbation validated pairs and RoboChallenge's real fleet; populate the gate on Embodied Arena.
> - A null result (r survives shift) is still informative → pre-register the r<0.7 bet; "high-r sims are robust to shift X" is publishable.
> - A stale gate mis-deploys → tie refresh to Embodied Arena's eval cadence; expire trust cells past a staleness window.

### C2: Sim-to-Real as Provable Statistical Inference: Banks of Biased Simulators
> [!abstract] The bet
> (i) Diversifying simulator bias tightens SureSim's PPI bound / widens Sim2Val's variance reduction **more than copies of the same biased sim** at matched bank size, a measurable CI-width gap Δ from diversity at fixed count. (ii) There is a compute-budget **crossover**: below it one accurate sim gives tighter CIs, above it the biased portfolio wins. Reproduce Sim2Real Betting's **70–100% win** and Sim2Val's fewer-real-samples result *only where diversity exists*.

**Why**: A bank of cheap biased sims beating a single accurate one is no longer the open question: Sim2Val does control-variates over biased sources with a provable variance bound on quadruped robotics; PERRY, SureSim, Sim2Real Betting are the PPI/betting instances. The open question is *bank composition*.

**First-principles**: *Principle:* estimating real performance is a statistics problem on few real trials; what matters is estimator jitter and CI trustworthiness, not any single sim's accuracy, a biased sim is fine if the bias carries signal and you correct for it. *Challenged:* not "the goal is one high-fidelity sim" but that the portfolio *result* is the contribution. *Wager:* bias *diversity*, not *count*, is the lever, with a compute crossover below which one sim wins.

**Sharpest questions**: 1) Does bias-diversity tighten the bound more than bias-count at matched count? 2) Is there a compute-budget crossover (below it one accurate sim wins, above it the portfolio)? 3) Does informative bias beat adversarial, does C1's gate recover more of the 70–100% win than an unfiltered bank?

> [!warning] Risks
> - PPI/betting need a few paired real outcomes → pair with RoboChallenge's remote fleet.
> - Bias must be informative, not adversarial → use C1's per-factor trust map to select informative-bias sims.
> - Portfolio overhead → quantify the compute-allocation frontier so the portfolio is used only where it provably beats the single-sim baseline.

## D: Deployment-Time Adaptation: Closing the Residual Gap Online
*Close the residual $\delta(t)$ at deploy-time, a time-varying disturbance, observable only on hardware, surviving every offline fix. The directions split by which model is on hand: privileged extrinsics, an analytical model, or only a learned one.*

### D1: Latent-Extrinsics Online Adaptation
> [!abstract] The bet
> Outside the train-time randomization range, a proprioception-only latent-extrinsics estimator **beats a GRAM-style robust-fallback** head-to-head, the real-SR gap *grows* with distance past the range and vanishes inside it. It reproduces RMA's zero-real-fine-tune adaptation (sand/mud/12 kg) and FLaRe's 50%→80.7% (+30.7%) *as the in-range baseline*.

**Why**: Hardware reveals dynamics that don't exist at train-time. RMA infers a privileged extrinsics vector online from proprioceptive history (zero real fine-tuning across terrains + 12 kg payload); FLaRe makes the manipulation case. GRAM builds the same architecture but *concedes* inference becomes unreliable OOD, falling back to a robust latent, D1 bets the inverse.

**First-principles**: *Principle:* deployment dynamics are a latent revealed only by the robot's proprioceptive history; the estimable quantity is the posterior over extrinsics given that history. *Challenged:* not "infer-then-condition beats robustify in-range" (settled by RMA/FLaRe) but GRAM's claim that inference becomes *unreliable* outside the range. *Wager:* the estimate *extends accurately* past the range (LDG's outcome-centric latents give headroom).

**Sharpest questions**: 1) (Front line) Does continued inference beat GRAM's robust-fallback outside the range, the SR gap growing with distance? 2) Over what envelope does the estimate stay accurate past the DR range? 3) Does an outcome-centric latent (LDG) beat parameter-centric (RMA) on unmodeled shifts (disabled actuator, time-varying disturbance)?

> [!warning] Risks
> - Proprioception under-determines extrinsics for vision-dominant manipulation → augment with force/tactile history (links A2's GRF reward).
> - Online adaptation can chase noise → use RMA's slow-module (10 Hz) / fast-policy (100 Hz) separation; gate on Self-Adapting RL's residual magnitude.
> - Unsafe adaptation during exploration → hand off to E1's safety-constrained continual adaptation.

### D2: Differentiable-Sim Test-Time Adaptation
> [!abstract] The bet
> BPTT through a *learned-residual hybrid* differentiable model, adapting a *learned neural* policy, corrects an OOD disturbance **in ≤3 steps / 4.5 s with 81% hover-error reduction** (vs L1-MPC; 55% vs DATT). It recovers SR on a disturbance the residual captures but M-GAPS's analytical-only model cannot represent.

**Why**: A quadrotor hitting unmodeled wind or added mass must correct *now* (seconds), but RL fine-tuning of a learned world model is slow. Learning on the Fly's differentiable hybrid (analytical core + learned residual MLP) lets policy gradients flow by BPTT, making adaptation first-order. M-GAPS settles online-gradient-beats-RL for a *purely analytical* controller, but is robust-*to* model error, not learning it.

**First-principles**: *Principle:* if the dynamics model is differentiable, adapting the policy is gradient descent on a known loss, so a few steps suffice. *Challenged:* not "online gradient adaptation is unavoidably slow" (GAPS/DiffTune+/M-GAPS settle it for analytical) but that the *analytical-model* route settles the whole question. *Wager:* a learned-residual hybrid *captures* a disturbance the analytical controller can only *tolerate*; BPTT adapts a *learned neural* policy where no analytical form exists.

**Sharpest questions**: 1) (Front line) Does learned-residual BPTT capture a disturbance off the nominal model that M-GAPS cannot, both still beating sampled RL on wall-clock? 2) Does residual expressiveness trade adaptation speed against disturbance range? 3) Does the 3-step correction degrade on contact-rich manipulation?

> [!warning] Risks
> - Differentiable dynamics may not exist for rich contact/friction transients → start in the aerial/analytical-core regime; expand via B2/B4's differentiable-MPM cautiously.
> - Fast overfitting to transient noise → gate on Self-Adapting RL's residual-magnitude trigger; decay the residual when the disturbance clears.
> - Adaptation during flight is safety-critical → bound the per-step update; hand execution-safety to E2's reachability shield.

### D3: World-Model-Supervised Online Policy Correction
> [!abstract] The bet
> An AdaWorldPolicy-style unified WM+force+action loop drives **4 Hz real-robot** online adaptation to unseen dynamics with no real reward. It holds **0.96 LIBERO-10** under OOD where a static policy degrades. Its **force-prediction-error term beats a T3VF-style image-foresight head on contact-rich OOD**.

**Why**: Deploy-time correction is blocked by *no real reward*. AdaWorldPolicy makes the world model an active supervisor, using its *prediction error* to drive test-time LoRA updates at 4 Hz. D3's territory is the *real-robot* 4 Hz regime via a unified WM+force+action DiT.

**First-principles**: *Principle:* physical consistency and task reward optimize *two different things*; prediction error measures policy drift and is visible on hardware where task reward is not. *Challenged:* not "online correction needs reward" (PAD broke it; T3VF made prediction-error-as-reward consensus) but that an image-foresight head is the *whole signal*, it isn't, under *contact* OOD. *Wager:* a force-prediction-error term carries the contact-drift direction visuals miss.

**Sharpest questions**: 1) (Front line) Does force-prediction error beat a T3VF-style image-foresight head on contact-rich OOD? 2) Does prediction-error supervision match a true-reward loop, or a measurably different objective? 3) Does world-model hallucination poison the gradient unless calibration-gated (links E3)?

> [!warning] Risks
> - World-model hallucination poisons the gradient → gate on prediction-error *calibration* (links E3); reject corrections when the world model is itself OOD.
> - Prediction error ≠ task error → measure the consistency-vs-task gap; pair with sparse real success checks.
> - Unsafe correction under no-reward adaptation → hand off to E1's safety-cost-constrained continual adaptation.

## E: Risk-Bounded Sim-to-Real Deployment: Safety Under the Irreducible Gap
*Bound the irreducible residual gap at runtime. Three surfaces: bound the update (E1), bound the action (E2), flag the failure (E3).*

### E1: Zero-Violation Continual Adaptation
> [!abstract] The bet
> SCDA's PCRPO+EWC, **wrapping a Cluster-D engine** (RMA/AdaWorldPolicy), holds the **20%→60% gain at zero violations**, and keeps zero forgetting and zero violations across **N successive domains**: where Safe Continual RL (NSCMDP) shows online-EWC violates and CPO forgets when run alone.

**Why**: Cluster D's online engines share a hazard: an exploratory update on hardware can drive an unsafe action before convergence. SCDA makes safety a *constraint* (PCRPO + EWC with a Fisher matrix from sim pretraining): real grasp SR rises 20%→60% at zero safety cost.

**First-principles**: *Principle:* on hardware an action's safety cost is a hard constraint with no recovery, so adaptation must optimize reward *subject to* it. *Challenged:* not "unconstrained adaptation is unsafe" (measured) but that the safe×continual-RL methods *are the deliverable*, shown alone. *Wager:* the zero-violation constraint *composes* with an arbitrary Cluster-D engine across domains.

**Sharpest questions**: 1) Does the zero-violation result hold when *wrapping* Cluster-D engines (RMA/AdaWorldPolicy), preserving the gain? 2) Does EWC keep both zero forgetting *and* zero violations across successive domains? 3) Do transfer-time (SPiDR) and adaptation-time (SCDA) safety *compose* to fewer violations than either alone?

> [!warning] Risks
> - Tight safety cost can stall adaptation → map the budget/rate frontier; set the limit at the loosest value guaranteeing zero violations.
> - EWC can over-rigidify → tune the EWC weight per SCDA's schedule.
> - Cost-model misspecification permits unsafe actions → pair with E2's reachability shield as a model-free backstop.

### E2: Reachability-Filtered Sim-to-Real Execution
> [!abstract] The bet
> A reachability shield holds the **0%-collision guarantee over a *changing* policy mid-adaptation** (Learning on the Fly/AdaWorldPolicy), at a bounded SR cost during the adaptation window. The static-policy baseline (RAIL 0% vs 5–35%; Path-Consistent Safety Filter +68% over CBF on a real Franka) is the confirmatory floor; an uncertainty-aware occupancy model closes residual-gap hazards a fixed-geometry filter misses.

**Why**: A sim-trained IL policy hitting the residual gap produces compounding errors and OOD actions; usual safety is *soft* (risk bounded in expectation). RAIL makes safety a *hard* guarantee (continuous-time reachability filter + backup planner): 0% collisions vs 5–35% baseline IL, ~10-pp SR cost, 0.42 s/plan on a real Franka. Path-Consistent Safety Filter wins hard-vs-soft on diffusion policies (+68% over CBF). No filter, though, shields a *changing* policy.

**First-principles**: *Principle:* collision-freeness is a reachability property of the robot's forward occupancy, verifiable in continuous time independent of the policy. *Challenged:* not "learned soft safety suffices" (Path-Consistent/Uncertainty-Latent won hard-vs-soft) but that the *static-policy* result settles safe execution, a Cluster-D policy changes actions mid-deployment, and fixed geometry misses residual-gap hazards. *Wager:* the guarantee must hold over a *moving* policy and *uncertain* geometry.

**Sharpest questions**: 1) Does the 0%-collision guarantee survive an *adapting* policy mid-update, at bounded SR cost? 2) Does the shield *raise* SR for weak policies and *cost* SR for strong ones? 3) Does pre-action verification (Pre-VLA) + the shield catch more unsafe actions than either alone?

> [!warning] Risks
> - Reachability filtering adds latency → RAIL runs at 0.42 s/plan on a real Franka; precompute occupancy, bound the per-step check.
> - Conservative shields over-intervene → map the intervention/SR-cost frontier; set the margin at the loosest value preserving 0% collisions.
> - Shield needs a model the residual gap may misestimate → ground occupancy in B1's reconstruction fidelity; fall back to E3's conformal detector where geometry is uncertain.

### E3: Conformal Runtime Failure Detection
> [!abstract] The bet
> (i) Robust-Conformal-CBF/CLF's proof that a conformal FPR bound survives *through* a closed CBF/CLF feedback loop **extends to a non-CBF/CLF backup** (RAIL's discrete backup, SCDA's safe-adapt) — preserving FPR within **2 pp** of nominal while cutting user-facing failures by **at least 30%**. (ii) SAFE's internal-feature detector **still does not transfer across architectures**, even though TDQC's calibrated Q-function score already does; pairing SAFE with FAIL-Detect's policy-agnostic density score recovers the detection TDQC's transfer result leaves open. Reproduce FIPER's no-failure-data conformal detection as the settled baseline.

**Why**: Detecting failures from successes alone, via a conformal threshold with an FPR guarantee, zero-shot to unseen tasks, is now consensus (FIPER does it near-verbatim, beating the FAIL-Detect lineage; Sentinel is the success-only root). Two more pieces are now conceded, not open: Robust-Conformal-CBF/CLF already proves the bound survives through a closed CBF/CLF loop under iterative policy updates (100% coverage/safety on inverted pendulum and multi-obstacle maze), and TDQC already runs a cross-architecture transfer test of a calibrated failure score across OpenVLA, UniVLA, π₀, and π₀-FAST. What's left is narrower.

**First-principles**: *Principle:* a failure is an OOD event against the success manifold, spottable from successful runs alone; a conformal threshold caps the false-alarm rate with a guarantee holding even on a small calibration set. *Challenged:* not "detection needs failure-labeled data" (dropped by Sentinel/FIPER) nor "a detect-then-act loop always breaks the FPR bound" (Robust-Conformal-CBF/CLF already shows it can hold, for CBF/CLF backups) — the live assumption is narrower: that bound-preservation is *specific* to CBF/CLF control structure, and that TDQC's cross-architecture transfer also holds for SAFE's internal features. *Wager:* both narrowed sub-claims, bound-preservation beyond CBF/CLF and internal-feature non-transfer, are still untested.

**Sharpest questions**: 1) Does Robust-Conformal-CBF/CLF's bound-preservation theorem extend from CBF/CLF backups to a heterogeneous backup (RAIL/SCDA), holding FPR within 2 pp of nominal while cutting failures by at least 30%? 2) Does SAFE's internal-feature detector fail across architectures where TDQC's Q-function already transfers, and does a policy-agnostic density backstop (FAIL-Detect/RC-NF) recover it? 3) Do step-level localization (Hide-and-Seek) + root-cause (RAPT) enable a *targeted* response recovering more SR than detect-then-halt?

> [!warning] Risks
> - Conformal validity needs a calibration set of successes → calibrate per FAIL-Detect's success-only protocol; re-calibrate on domain shift.
> - Internal-feature detectors are model-specific → pair with FAIL-Detect's/RC-NF's policy-agnostic density score as a fallback.
> - Detection without response is inert → wire the flag to E2's shield or E1's safe adaptation.
