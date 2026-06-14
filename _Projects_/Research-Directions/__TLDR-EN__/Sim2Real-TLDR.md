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
> A skimmable TL;DR of [[Sim2Real|Sim-to-Real & Real-to-Sim Transfer]]. Per direction: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[Sim2Real-ELI5|ELI5]].

> [!abstract] Overview
> The reality gap is usually treated as one forward problem (train in sim, lose on hardware) and attacked with more domain randomization. That hides two facts: how faithfully you run reality *backward* into the simulator (real→sim) caps how well it predicts reality *forward*; and whatever residual survives every offline fix is observable only at deploy-time, where an un-handled remainder is a *safety* failure, not just a lost success. The editorial bet: **the realism you optimize is not the transfer you want** — on the load-bearing axes (controller gains, DR marginalization, fidelity proxies) the two are anti-correlated, so the field that *estimates and inverts* beats the field that *randomizes and renders*.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A — Forward Sim-to-Real: Robustness Beyond DR | A1–A3 | DR randomizes appearance, not the *causes* of outcomes — semantics, physics rewards, control structure are what transfer |
| B — Real-to-Sim-to-Real: Grounding the Simulator | B1–B4 | Recovering appearance + dynamics $(\phi^\star, \psi^\star)$ from real data is the new bottleneck — and a *chosen* law caps it |
| C — Reality-Gap Measurement as Inference | C1–C2 | High in-distribution r, untested under deliberate shift, no provable bound |
| D — Deployment-Time Adaptation | D1–D3 | The residual $\delta(t)$ that survives A/B/C is time-varying and observable only at deploy-time |
| E — Risk-Bounded Deployment: Safety Under the Irreducible Gap | E1–E3 | An un-handled residual is a *safety* failure, not just a performance one |

## A — Forward Sim-to-Real: Robustness Beyond Domain Randomization
*Attack the forward gap directly — transfer what is invariant (object semantics, physics-grounded rewards, control structure) rather than randomizing what is not (pixels around an unchanged cause).*

### A1 — Hybrid Neural-Rendering + Physics Simulators for Semantic Sim-to-Real
> [!abstract] The bet
> A 3DGS-in-the-loop simulator that re-samples affordance and material *semantics per episode* (not once at asset time, and not appearance) lifts affordance-task real SR **>20 pp over AffordSim's ~24% appearance-only ceiling** *and* beats Digital-Cousins-style fixed-cousin asset randomization at matched render budget — pushing mug-hang-class tasks toward HyperSim's 95%-with-few-real regime at GS-Playground-class throughput (10,000 FPS).

**Why** — DR perturbs lighting/texture/pose, but a mug's handle-affordance is a *semantic* property that survives every appearance change, so the nuisance axis DR covers and the task axis the policy needs are orthogonal. First principle: task success depends on appearance-invariant causes (affordance, material response); randomizing the downstream effect can't cover variation in the cause. The live assumption it challenges is *not* "randomize the cause not the effect" (Digital Cousins already proved that, 90% vs 25% asset-level), but that the cause is best varied *offline at asset-generation time* — leaving appearance the only thing randomized in the loop.

**First-principles** — *Principle:* affordances/mass/material are the causes of manipulation outcomes; pixels are downstream effects. *Challenged:* the offline-asset-time-only assumption behind RoboTwin 2.0 / ViserDex / Digital Cousins; AffordSim's affordance-aware data hits 98/79/64% collection yet zero-shot real SR caps at ~24%. *Wager:* re-sampling the cause *per episode inside a physics loop* covers it continuously rather than via a discrete cousin set, and GS-Playground's 10,000 FPS shows it fits the budget.

**Sharpest questions** — 1) Does affordance/material randomization add real-SR *on top of* the fidelity-helps finding (Grounding Study) — i.e. does the semantic main-effect survive at high PBR, or get absorbed by rendering? 2) Does per-episode in-loop re-sampling beat fixed-cousin asset randomization at matched diversity budget? 3) Can AffordSim's VoxAfford auto-label generated assets well enough to remove the hand-annotation bottleneck?

> [!warning] Risks
> - Neural rendering in the loop is compute-heavy → GS-Playground point-pruning + batch rendering (10,000 FPS shows tractable); discard auxiliary heads at deploy.
> - Semantic ground truth is scarce → bootstrap from VoxAfford auto-labeling on generated assets, not hand annotation.
> - Gains may be confounded with realism → semantics-vs-appearance ablation at fixed PBR is the go/no-go; report the semantic main-effect separately.

### A2 — Reward-Signal Sim-to-Real: Transferring PINN-Estimated Physics Rewards, Not Actions
> [!abstract] The bet
> A physics-law-grounded reward (GRF, contact wrench) retains its objective across *contact-dynamics* shifts where a *learned* transferable reward drifts — holding QuietWalk's **R²=0.99 sensor-free** accuracy and the **−7.17 dBA** objective across **4 footwear types** and outdoor terrains, while a Video-Language-Critic-style learned reward and a VIRAL-style DR action policy both lose retention under the same shift.

**Why** — Most pipelines harden the *action* mapping, so the thing crossing the gap inherits the simulated dynamics it was hardened on. Transferring the *reward* is already mature (XIRL, DARL, Video-Language Critic, DrEureka), but each reward is *learned* from data, so it drifts under the dynamics shift it was meant to survive. First principle: a reward grounded in a physical law is a function of physical *state*, not training distribution, so it scores any trajectory correctly on unseen hardware.

**First-principles** — *Principle:* actions are distribution-bound; physics-grounded rewards are distribution-free. *Challenged:* the learned-reward orthodoxy (XIRL/DARL/Video-Language-Critic/DrEureka) — the novelty is *distribution-free*, not "reward-instead-of-action" (which is consensus). *Wager:* QuietWalk's inverse-dynamics *constraint* — not the network — drives the 82–86% GRF-error reduction and R²=0.99, so the reward is invariant precisely because the constraint is.

**Sharpest questions** — 1) Does the physics-law reward beat a *learned* reward (and action transfer) on cross-condition retention, widest under the hardest contact shift (high heels)? 2) Is the inverse-dynamics constraint the lever — does removing it collapse R² toward 0.39/0.67 and break off-distribution retention? 3) Does the advantage hold only on conservation/inverse-dynamics tasks and vanish on semantic tasks (bounding the claim)?

> [!warning] Risks
> - PINN rewards exist for few physical quantities → bound the claim to contact/force-dominated tasks where a conservation law actually exists; don't over-claim to semantic tasks.
> - Reward transfer ≠ policy transfer → pair with Self-Adapting RL's online fine-tune so the transferable reward drives fast real adaptation.
> - PINN degrades off-manifold → measure the trust envelope (H4); gate reward use on residual magnitude, fall back where R² drops below threshold.

### A3 — Controller-Gain-Aware Sim-to-Real: Co-Optimizing Dynamics and Control
> [!abstract] The bet
> Co-optimizing $(K_p, K_d)$ *jointly with* the dynamics distribution captures a non-empty **gain×dynamics interaction term** — joint beats (gain-only + dynamics-only) by **more than their sum** on AutoMate-class contact tasks, *and* the co-optimized DR variable beats a DexCtrl/TAM-style runtime gain residual at matched SR (preventing the mismatch beats patching it).

**Why** — The field treats gains as a fixed robot property or tunes them for low tracking error during sysID — but the gain is really an unrecognized sim-to-real hyperparameter, setting the training dynamics distribution, action smoothness, and deployment oscillation spectrum at once. Tune-to-Learn is the under-internalized result: the gains with the *lowest* sysID error (stiff) give the *worst* transfer; RL reaches 99%+ across regimes only with per-gain tuning.

**First-principles** — *Principle:* the controller is part of the plant the policy controls — gains set closed-loop dynamics, so they belong in the transfer distribution, not a separate pre-tuning step. *Challenged:* not "gains belong in randomization" (routine DR; runtime adaptive gains DexCtrl/Dynamic-Compliance/Watch-Less already beat fixed) but that gain and dynamics randomization are *separable* — Tune-to-Learn's sysID-vs-transfer inversion implies the closed-loop couples them. *Wager:* a sequential or runtime-residual recipe leaves a joint term on the table that only co-optimization captures.

**Sharpest questions** — 1) Is there a super-additive gain×dynamics term — does joint beat gain-only + dynamics-only? 2) (Front-line falsifier) Do co-optimized DR-variable gains beat a *runtime* adaptive-gain predictor / torque residual at matched SR? 3) Is the effect contact-specific (concentrated on contact-rich tasks, ~null on free-space reaches)?

> [!warning] Risks
> - Gain co-optimization explodes the search space → seed a narrow compliant/overdamped prior from Tune-to-Learn rather than searching the full grid.
> - Hardware gain limits may make co-optimized values infeasible → constrain to the hardware's admissible gain box and validate on the real controller.
> - Effect may be task-specific → scope to contact-rich tasks (AutoMate/NIST) and report the free-space null honestly.

## B — Real-to-Sim-to-Real: Grounding the Simulator in Deployment
*Invert reality into the simulator first — recover appearance and dynamics from real data — then forward transfer comes nearly for free, because a simulator predicts reality forward no better than it captured reality backward.*

### B1 — Closing the Real-to-Sim Gap: Reconstruction Fidelity as the New Bottleneck
> [!abstract] The bet
> Across rigid/articulated/deformable object classes there is a **monotone, measurable fidelity→r law** — degrading reconstruction error in controlled steps predicts forward r per class — and the joint-inversion advantage is **widest on deformables** (Real-to-Sim GS 0.901 vs Isaac Lab 0.237 on rope, vs 0.915 vs 0.649 push-T), the regime the navigation counter-example does *not* cover.

**Why** — The field invests in *forward* realism, but once you name a real-to-sim gap distinct from the forward one (REALM), the causal arrow flips: forward correlation is capped by inversion fidelity, and no forward training lifts a lossy inversion. The joint-inversion *engine* is now consensus (Splatting Physical Scenes, One-Shot Real-to-Sim, TwinAligner, D-REX all jointly invert geometry+appearance+physics), so the bottleneck is the *law* mapping reconstruction fidelity to forward r.

**First-principles** — *Principle:* a simulator predicts reality forward no better than it captured reality backward — $\text{Gap}_{\text{S2R}}$ is lower-bounded by $\text{Gap}_{\text{R2S}}$. *Challenged:* not "invert jointly" (consensus) but that reconstruction fidelity *monotonically* predicts forward transfer — Lower-Fidelity Sim2Real broke it head-on (lower fidelity gave *higher* transfer in navigation). *Wager:* Real-to-Sim GS's ablation (removing color *or* physics collapses correlation) shows the bound is joint-reconstruction-bound, and the fidelity→r map must be *measured* per class, not assumed.

**Sharpest questions** — 1) Is the fidelity→r law monotone on contact manipulation (where the navigation counter-example doesn't reach) — and can the regression *rank* twins offline before any forward rollout? 2) Is the inversion advantage widest on deformables, requiring the r>0.9 bet to be reported per object-class? 3) Does control-dynamics misalignment (REALM) cap correlation even at r>0.9 — a residual term only control-alignment (links A3) closes?

> [!warning] Risks
> - Reconstruction is per-scene expensive → amortize with generative reconstruction priors (WorldComposer) and reuse twins across tasks.
> - The gap to Isaac Lab is widest on deformables → scope the >0.9 bet across rigid and deformable, reporting per-class delta separately rather than assuming one number generalizes.
> - Inversion fidelity may not be the *only* bound → co-optimize control alignment (links A3) alongside appearance+physics.

### B2 — Amortized Differentiable System-ID: Zero-Per-Object Gradient sysID in Clutter
> [!abstract] The bet
> An amortized observation→parameter network, trained on differentiable-sim rollouts, recovers constitutive parameters for **unseen objects in clutter at zero per-object demos** and reproduces the gradient-sysID-vs-DR-on-OOD advantage (D-REX 9–10/10 vs DR 4–9/10 below the DR support) **on objects it never saw** — the falsifiable measurement being the *SR-vs-parameter-distance frontier* for {amortized} vs {per-object gradient} vs {DR}.

**Why** — Gradient sysID through a differentiable simulator is solved (D-REX recovers mass to 4.8–12.0% error and beats DR off-support), but every such loop runs *per object*, re-optimizing from interaction demos (≥20 demos/object, mass only) — so it can't identify a novel object in clutter. First principle: the observation→parameter map is itself a learnable *function*, amortizable to a single forward pass.

**First-principles** — *Principle:* a function can be amortized — trained once on diff-sim rollouts, it infers parameters for a novel object in one forward pass. *Challenged:* that per-object gradient recovery is the unit of sysID (D-REX/DOT-Sim/PhysTwin/One-Shot re-optimize per object). *Wager:* Offline Domain Randomization proves DR *is* MLE of a parameter distribution from offline data — so the same corpus can train the inverse map, not just average over it; the diff-sim that recovers params per object is exactly the data generator for the net's supervision.

**Sharpest questions** — 1) Does amortized inference match D-REX's per-object recovery at zero per-object demos, and beat DR off the prior support on the SR-vs-distance frontier? 2) Does it scale to clutter (one pass for N objects) where per-object loops cost N optimizations? 3) Does a full constitutive *vector* (mass+friction+stiffness) amortize, not just mass?

> [!warning] Risks
> - Amortized inference may not transfer past its training distribution of objects → train on a wide diff-sim corpus, report recovery error vs distance, fall back to a per-object D-REX loop when low-confidence.
> - Differentiable sims exist for few physics regimes → generate the corpus in DOT-Sim/PhysTwin's deformable/soft-contact regime; expand to rigid contact cautiously.
> - Clutter breaks the observation→parameter map → condition on segmented per-object observations, report recovery error vs occlusion, gate on segmentation confidence.

### B3 — Bidirectional Sim↔Real Co-Training: The Twin as a Data Engine, Not a Sandbox
> [!abstract] The bet
> A per-task object-grounded fold-back loop **gated on a B1 reconstruction-fidelity check** improves *monotonically across N rounds* on unseen-object generalization, where the same loop *ungated* drifts — and the per-round gain *scales with the reconstruction-fidelity exchange rate* (Real-is-Sim 30 sim ≈ 30 real, 57%→80%, rising with twin fidelity). Reproduce RialTo's 90%-vs-10% grounding advantage and HyperSim 75%→95% per round, beating Arcadia's single feedback-on/off lifecycle delta (LIBERO 88.5 vs 86.9) over successive rounds.

**Why** — Most of the corpus uses twins as sandboxes (cheap evaluators), discarding the twin's generative capacity. The highest-leverage results use twins as *data engines* (RialTo, HyperSim, RoboTwin 2.0). The closed loop is now *claimed* (Arcadia operationalizes a real→sim→real lifecycle and states B3's falsifier verbatim) — but its evidence is a *single* feedback-on/off pass at *scene/lifecycle* scale, not a per-task object twin run over *successive* rounds.

**First-principles** — *Principle:* a twin grounded in real reconstruction generates data from the *correct* distribution, so its samples are training-valid, not just test-valid (RialTo's 90% target-twin vs 10% generic proves only grounded twins produce target-distribution data). *Challenged:* not "closed loop beats one-shot" (Arcadia claims it) but that fold-back is *unconditionally* self-improving — each fold re-reconstructs from imperfect deployment data, so an ungated loop can drift. *Wager:* gating each fold on a B1 fidelity check (reject folds that lower sim-real r) keeps the loop monotone.

**Sharpest questions** — 1) On a *per-task object* twin, does fold-back beat one-shot over *successive* rounds (gap widening each round), where Arcadia only showed it once at lifecycle scale? 2) Does twin-data value (the sim:real exchange rate) scale with reconstruction fidelity? 3) Does a per-fold fidelity gate keep the loop monotone where the ungated loop drifts?

> [!warning] Risks
> - Closed-loop can drift → gate each fold on a B1 fidelity check; reject folds that lower sim-real r.
> - Co-training balance is delicate → tune the sim:real ratio per Real-is-Sim's 1:1 and HyperSim's 35-demo regime; treat the ratio as a hyperparameter.
> - Grounding cost per object → amortize via B2's differentiable sysID + generative priors; reuse twins across tasks.

### B4 — Generalizable Constitutive-Law Inversion: Learning the Physics, Not Just the Parameters
> [!abstract] The bet
> A learned constitutive law beats a parameter-only fit (e.g. PhysTwin) **on held-out geometry up to 1M particles** — reproducing NCLaw's order-of-magnitude extrapolation advantage and <1e-3 loss — *and* survives a **closed robot real→sim→real loop**: dropped into Real-to-Sim GS's pipeline in place of the fixed soft-body model, it holds forward correlation across material variation a single parameter fit cannot cover.

**Why** — B2 recovers the *parameters* of a law the engineer chose, capping generalization at the functional form. NCLaw shows the move (embed a *neural* constitutive law inside a differentiable MPM, let the simulator enforce conservation structurally), and MASIV makes learn-the-form-from-video *consensus* — so "learn the functional form" is no longer the frontier. The two unattacked deltas: isolating the learned-law-vs-parameter-fit advantage *on held-out geometry* (which MASIV never does), and the *closed robot loop* (which neither NCLaw nor MASIV supplies).

**First-principles** — *Principle:* the cause of a material's motion is its constitutive law (the stress-strain map), not the scalars of any one parameterization — conservation laws are universal and belong in the simulator, the constitutive law is the only material-specific degree of freedom. *Challenged:* not "learn the form from video" (MASIV/UniPhy/Physics-Informed-Deformable-GS do it) but that learning the form is *itself* the contribution — leaving geometry-extrapolation and robot-loop untested. *Wager:* NCLaw's orders-of-magnitude generalization shows the functional form, not the parameters, is the binding constraint on extrapolation.

**Sharpest questions** — 1) (Front line) Does learned-law extrapolation beat a parameter fit on held-out geometry up to 1M particles — the delta MASIV's material-type recovery skips? 2) Does a learned law survive the full real→sim→real loop, holding forward correlation across materials a single parameter fit can't cover? 3) Are NCLaw's structural priors (rotation-equivariance, undeformed-equilibrium) load-bearing for off-distribution physicality?

> [!warning] Risks
> - Recovery is solved; the robot loop is not → treat 1M-particle generalization as transfer-of-recovery evidence; the learned-law-into-loop test (H2) is the go/no-go supplying the missing proof.
> - Learned laws can violate physics off-distribution despite priors → keep NCLaw's structural priors as hard constraints; gate on conservation-law residuals, not just reconstruction loss.
> - Differentiable MPM is mature for soft bodies, not rich contact → scope the 1M-particle bet to elastoplastic/fluid materials; treat rigid-contact laws as a separate, harder problem.

## C — Reality-Gap Measurement as Statistical Inference
*Stop asking "is the sim accurate?" Ask "what can I provably infer about real performance from imperfect, possibly-adversarial sims?" — treating a correlation number as a validity claim and a portfolio of biased sims as a variance-reduction estimator.*

### C1 — Per-Factor Correlation Validity as a Deployment Gate: Stress-Test, Then Route
> [!abstract] The bet
> A per-(sim, factor) trust map — the *correlation* re-measured under each COLOSSEUM factor, ingesting REALM's validated rows — used as a deployment *router* lifts Sim2Real Betting's **70–100% win rate** over its single-global-edge baseline on shift-mixed deployment, and recovers SureSim's **20–25%** real-trial reduction by skipping do-not-trust cells, with the gain largest where r collapses hardest.

**Why** — Two questions share one mechanism: is a benchmark's high r a real property or an artifact of nominal conditions, and once you have a per-factor table can you *route* which sim to trust per shift? Today's correlations (SIMPLER r≥0.85, VISER 0.92, WorldMark ρ>0.9) are all *in-distribution*; COLOSSEUM shows single perturbations cause 30–50% SR drops differently per factor. MolmoSpaces runs controlled per-factor variation but reports per-factor *SR sensitivities*, not per-factor *correlation*, and nobody builds a router.

**First-principles** — *Principle:* a correlation number only vouches for the sim under the exact conditions measured; trustworthiness is one number *per perturbation factor* (different physics shortcuts break under different shifts). *Challenged:* not "one in-distribution r proves the sim usable" (conceded; MolmoSpaces/Predictivity/Quantile-Curves) but that the diagnosis ends at *success-drop sensitivities* and a *global* edge — nobody re-measures the *correlation* per factor or routes on it. *Wager:* a per-factor validity map can route deployment where one global r cannot.

**Sharpest questions** — 1) Does per-factor *correlation* (not SR sensitivity) fall below r<0.7 for the worst factors (distractors/color/lighting) even where global r is high? 2) Does a per-(sim, factor) routing gate beat single-global-edge selection? 3) Under some perturbation, does sim r go *negative* (ranks policies backward — the strongest case for the gate)?

> [!warning] Risks
> - Stress-test and gate both need paired sim+real OOD data (combinatorially expensive) → reuse REALM's 15-perturbation validated pairs and RoboChallenge's real fleet; populate the gate incrementally on Embodied Arena.
> - A null result (r survives shift) is still informative → pre-register the r<0.7 bet; if r holds, "high-r sims are robust to shift X" is publishable and the gate routes on validated-robust cells.
> - Routing on a stale gate mis-deploys the portfolio → tie gate refresh to Embodied Arena's evolving-eval cadence; expire trust cells past a staleness window.

### C2 — Sim-to-Real as Provable Statistical Inference: Banks of Biased Simulators
> [!abstract] The bet
> (i) Diversifying simulator bias tightens SureSim's PPI bound / widens Sim2Val's variance reduction **more than adding copies of the same biased sim** at matched bank size — a measurable CI-width gap Δ from diversity at fixed count. (ii) There is a compute-budget **crossover** below which one accurate sim gives tighter CIs and above which the biased portfolio wins. Reproduce Sim2Real Betting's **70–100% win** and Sim2Val's fewer-real-samples result *only as the regime where diversity is present*.

**Why** — Real-performance estimation is variance reduction, and a bank of cheap biased sims beating a single accurate one is no longer the open question — Sim2Val does control-variates over biased sources with a provable variance bound on quadruped robotics; PERRY, SureSim, Sim2Real Betting are the PPI/betting instances. The open question is *bank composition*: which property (diversity vs count) tightens the bound, and when the portfolio is worth it.

**First-principles** — *Principle:* estimating real performance is a statistics problem on few real trials — what matters is estimator jitter and CI trustworthiness, not any single sim's accuracy; a biased sim is fine if the bias carries signal and you correct for it. *Challenged:* not "the goal is one high-fidelity sim" (the inference camp won that) but that the portfolio *result* is the contribution — nobody asks what *property of the bank* drives the bound. *Wager:* bias *diversity* (different physics approximations), not bias *count*, is the lever, with a compute crossover below which one accurate sim still wins.

**Sharpest questions** — 1) Does bias-diversity tighten the bound more than bias-count at matched count? 2) Is there a compute-budget crossover (below it one accurate sim wins, above it the portfolio wins)? 3) Does *informative* bias beat adversarial bias — does C1's gate selecting informative-bias sims recover more of the 70–100% win than an unfiltered bank?

> [!warning] Risks
> - PPI/betting need a few paired real outcomes → pair with RoboChallenge's remote fleet to keep real-sample cost minimal while preserving validity.
> - Bias must be informative, not adversarial → use C1's per-factor trust map to select informative-bias sims and exclude those failing under the relevant shift.
> - Portfolio overhead (managing many sims) → quantify the compute-allocation frontier so the portfolio is used only where it provably beats the single-sim baseline.

## D — Deployment-Time Adaptation: Closing the Residual Gap Online
*Close the residual $\delta(t)$ at deploy-time — a time-varying disturbance observable only on hardware that survives every train-, reconstruct-, and measure-time fix. The three directions split by which model is on hand: privileged extrinsics, an analytical model, or only a learned one.*

### D1 — Latent-Extrinsics Online Adaptation
> [!abstract] The bet
> Outside the train-time randomization range, a proprioception-only latent-extrinsics estimator **beats a GRAM-style robust-fallback** head-to-head — the real-SR gap *growing* with distance past the range (and vanishing inside it) — over a measurable envelope, reproducing RMA's zero-real-fine-tune adaptation (sand/mud/12 kg) and FLaRe's 50%→80.7% (+30.7%) *as the in-range baseline*.

**Why** — A fixed domain-randomized policy is one bet placed at train-time, but the dynamics revealed on hardware don't exist until deployment. RMA infers a privileged extrinsics vector online from proprioceptive history (zero real fine-tuning across terrains + 12 kg payload); FLaRe makes the manipulation case. But GRAM builds the same architecture and answers D1's own boundary question — it *concedes* inference becomes unreliable OOD and falls back to a robust latent. D1's surviving edge is the *inverse*: continued inference *beats* robust-fallback outside the range.

**First-principles** — *Principle:* the deployment environment's true dynamics are a latent revealed only by the robot's own proprioceptive history — the estimable quantity is the posterior over extrinsics given on-robot history, a deploy-time object by construction. *Challenged:* not "infer-then-condition beats robustify in-range" (settled by RMA/FLaRe) but GRAM's claim that inference becomes *unreliable* outside the range so you should give up and robustify. *Wager:* the latent-extrinsics estimate *extends accurately* some measurable distance past the range (LDG's outcome-centric latents support the headroom).

**Sharpest questions** — 1) (Front line) Does continued inference beat GRAM's robust-fallback outside the range, the SR gap *growing* with distance (tying inside it)? 2) Over what measurable envelope does the estimate stay accurate past the DR range before it stops? 3) Does an outcome-centric latent (LDG) beat parameter-centric (RMA) on unmodeled shifts (disabled actuator, time-varying disturbance)?

> [!warning] Risks
> - Proprioception under-determines extrinsics for some tasks (vision-dominant manipulation) → augment with force/tactile history (links A2's GRF reward); report the observability boundary.
> - Online adaptation can chase noise → use RMA's slow-module (10 Hz) / fast-policy (100 Hz) separation; gate updates on Self-Adapting RL's residual magnitude.
> - Unsafe adaptation during exploration → hand off to E1's safety-constrained continual adaptation.

### D2 — Differentiable-Sim Test-Time Adaptation
> [!abstract] The bet
> BPTT through a *learned-residual hybrid* differentiable model adapting a *learned neural* policy corrects an OOD disturbance **in ≤3 steps / 4.5 s with 81% hover-error reduction** (vs L1-MPC; 55% vs DATT) — *and* recovers SR on a disturbance the residual captures but M-GAPS's analytical-only model cannot represent, at matched wall-clock.

**Why** — When a quadrotor hits unmodeled wind or added mass, the residual must be corrected *now* (seconds), but RL fine-tuning of a learned world model is slow. Learning on the Fly's differentiable hybrid model (analytical core + learned residual MLP) lets policy gradients flow by BPTT, so adaptation is a first-order step. But M-GAPS already settles online-gradient-beats-RL for an *analytical* controller — it tunes a geometric controller's gains through a *purely analytical* model, so it is robust-*to* model error, not learning it. D2's distinctive regime is what M-GAPS structurally cannot do.

**First-principles** — *Principle:* if the dynamics model is differentiable, adapting the policy is gradient descent on a known loss — the disturbance shows up as an error term the gradient fixes directly, so a few steps suffice. *Challenged:* not "online gradient adaptation is unavoidably slow" (fell to GAPS/DiffTune+; M-GAPS settles it for analytical) but that an *analytical-model* gradient route settles the whole question. *Wager:* a learned-residual hybrid can *capture* a disturbance the analytical controller can only *tolerate*, and BPTT then adapts a *learned neural* policy where no clean analytical form exists.

**Sharpest questions** — 1) (Front line) Does learned-residual BPTT capture a disturbance *off* the nominal model that M-GAPS's analytical-only gain tuning cannot, both still beating sampled RL on wall-clock? 2) Does residual expressiveness trade adaptation speed against disturbance range (a measurable frontier)? 3) Does the 3-step correction degrade on contact-rich ground manipulation, scoping the bet to analytical-core regimes?

> [!warning] Risks
> - Differentiable dynamics may not exist for the regime (rich contact/friction transients) → start in the aerial/analytical-core regime; expand to contact via B2/B4's differentiable-MPM machinery cautiously.
> - Fast overfitting to transient noise → gate adaptation on Self-Adapting RL's residual-magnitude trigger; decay the residual when the disturbance clears.
> - Adaptation during flight is safety-critical → bound the per-step update; hand execution-safety to E2's reachability shield during the adaptation window.

### D3 — World-Model-Supervised Online Policy Correction
> [!abstract] The bet
> An AdaWorldPolicy-style unified WM+force+action loop drives **4 Hz real-robot** online adaptation to unseen dynamics with no real reward, holding **0.96 LIBERO-10** under OOD where a static policy degrades, *and* its **force-prediction-error term beats a T3VF-style image-foresight-only head on contact-rich OOD** (the regime image foresight is blind to).

**Why** — The blocker on deploy-time correction is that *real reward is not available*. AdaWorldPolicy makes the world model an active supervisor — uses its *prediction error* as a self-supervised signal to drive test-time LoRA updates at 4 Hz with no reward. But T3VF makes prediction-error-as-reward consensus (per-step VLA updates with an adaptive filter), and PAD broke "needs reward" back in 2021. D3's surviving territory is the *real-robot* 4 Hz regime via a unified WM+force+action DiT, where a *force*-prediction-error term sharpens contact OOD image foresight misses.

**First-principles** — *Principle:* physical consistency and task reward optimize *two different things*; prediction error measures policy drift from the dynamics the model knows, and you can see that error on hardware while you cannot see task reward there. *Challenged:* not "online correction needs reward" (PAD broke it; T3VF made prediction-error-as-reward consensus) but that an image-foresight prediction-error head is the *whole signal* — it isn't under *contact* OOD. *Wager:* a force-prediction-error term (which the unified DiT supplies and T3VF's visual head cannot) carries the contact-drift direction visual prediction misses.

**Sharpest questions** — 1) (Front line) Does force-prediction error beat a T3VF-style image-foresight head on contact-rich OOD? 2) Does prediction-error supervision match a true-reward loop, or correct a measurably *different* (consistency, not task) objective? 3) Does world-model hallucination poison the gradient unless calibration-gated (links E3's conformal detector)?

> [!warning] Risks
> - World-model hallucination poisons the gradient → gate updates on prediction-error *calibration* (links E3); reject corrections when the world model is itself OOD.
> - Prediction error ≠ task error → measure the consistency-vs-task gap; pair with sparse real success checks where available.
> - Unsafe correction under no-reward adaptation → hand off to E1's safety-cost-constrained continual adaptation.

## E — Risk-Bounded Sim-to-Real Deployment: Safety Under the Irreducible Gap
*Bound the irreducible residual gap at runtime — an un-handled gap is a safety failure, not just a performance loss. Three distinct surfaces: bound the update (E1), bound the action (E2), flag the failure (E3).*

### E1 — Zero-Violation Continual Adaptation
> [!abstract] The bet
> SCDA's PCRPO+EWC, **wrapping a Cluster-D engine** (RMA/AdaWorldPolicy), holds the **20%→60% gain at zero violations** *and* keeps both zero forgetting and zero violations across **N successive domains** — where Safe Continual RL (NSCMDP) shows online-EWC violates and CPO forgets when run alone.

**Why** — Cluster D's online engines share a hazard: an exploratory update on real hardware can drive an unsafe action before it converges. SCDA documents reward-only adaptation "led to unsafe behaviors" and makes safety a *constraint* (PCRPO + EWC with a Fisher matrix from sim pretraining): real grasp SR rises 20%→60% at zero safety cost. Safe Continual RL (NSCMDP) makes the two-axis tension a *measured* result (online-EWC violates, CPO catastrophically forgets) — so "is unconstrained adaptation unsafe" is settled, and the front line moves to *composition*.

**First-principles** — *Principle:* on hardware an action's safety cost is a hard constraint with no recovery — adaptation must optimize reward *subject to* a safety-cost bound; safety is a constraint set, not a reward term. *Challenged:* not "unconstrained adaptation is unsafe" (a measured result) but that the safe×continual-RL methods *are the deliverable*, demonstrated in isolation on their own loops. *Wager:* whether the zero-violation constraint *composes* with an arbitrary Cluster-D engine on hardware across successive domains is the open question.

**Sharpest questions** — 1) Does the zero-violation result hold when *wrapping* Cluster-D engines (RMA/AdaWorldPolicy), preserving the adaptation gain? 2) Does EWC keep both zero forgetting *and* zero violations across successive domains, or do they trade off as domains accumulate? 3) Do transfer-time (SPiDR) and adaptation-time (SCDA) safety *compose* to fewer total violations than either alone?

> [!warning] Risks
> - Tight safety cost can stall adaptation → map the budget/rate frontier; set the limit at the loosest value that still guarantees zero violations.
> - EWC protection can over-rigidify → tune the EWC weight per SCDA's schedule; monitor the forgetting/adaptation balance across domains.
> - Cost model misspecification permits unsafe actions it doesn't penalize → pair with E2's reachability shield as a model-free backstop.

### E2 — Reachability-Filtered Sim-to-Real Execution
> [!abstract] The bet
> A reachability shield holds the **0%-collision guarantee over a *changing* policy mid-adaptation** (Learning on the Fly/AdaWorldPolicy), at a bounded SR cost during the adaptation window — where the static-policy baseline (RAIL 0% vs 5–35%; Path-Consistent Safety Filter +68% over CBF on a real Franka) is the confirmatory floor — *and* an uncertainty-aware occupancy model closes the residual-gap hazards a fixed-geometry filter misses.

**Why** — When a sim-trained IL policy hits the residual gap, it produces compounding errors and OOD actions, and the field's usual safety is *soft* (penalties that bound risk in expectation). RAIL makes safety a *hard* guarantee (continuous-time reachability filter + backup planner): 0% collisions vs 5–35% baseline IL, ~10-pp SR cost, 0.42 s/plan on a real Franka. Path-Consistent Safety Filter wins hard-vs-soft on diffusion policies (+68% over CBF) — so the headline is confirmatory. What no filter does is shield a policy that is *itself changing*.

**First-principles** — *Principle:* collision-freeness is a reachability property of the robot's forward occupancy — verifiable in continuous time independent of the policy, so safety can be a hard runtime filter, not a learned objective. *Challenged:* not "learned soft safety suffices" (Path-Consistent/Uncertainty-Latent won hard-vs-soft) but that the *static-policy* hard-filter result settles safe execution — a Cluster-D online-adapting policy changes its actions mid-deployment, and a fixed-geometry occupancy model provably misses residual-gap hazards. *Wager:* the guarantee must hold over a *moving* policy and *uncertain* geometry.

**Sharpest questions** — 1) Does the 0%-collision guarantee survive an *adapting* policy mid-update, at bounded SR cost? 2) Does the shield *raise* SR for weak policies (by pruning doomed trajectories) and *cost* SR for strong ones — a policy-strength-dependent sign? 3) Does pre-action verification (Pre-VLA) + the reachability shield catch more unsafe actions than either alone?

> [!warning] Risks
> - Reachability filtering adds latency → RAIL runs at 0.42 s/plan on a real Franka (tractable); precompute occupancy, bound the per-step check budget.
> - Conservative shields over-intervene → map the intervention/SR-cost frontier; set the margin at the loosest value preserving 0% collisions.
> - Shield needs a model of obstacles the residual gap may misestimate → ground the occupancy model in B1's reconstruction fidelity; fall back to E3's conformal detector where geometry is uncertain.

### E3 — Conformal Runtime Failure Detection
> [!abstract] The bet
> (i) A detect-then-act loop wiring the conformal flag to RAIL's backup or SCDA's safe-adapt **preserves the FPR guarantee** while cutting user-facing failures (the bound holds *through* the action, not just at the flag). (ii) SAFE's internal-feature detector **does not transfer across architectures**, and pairing it with FAIL-Detect's policy-agnostic density score recovers detection on the architectures the internal features miss. Reproduce FIPER's no-failure-data conformal detection as the settled baseline.

**Why** — Detecting failures from successes alone, via a conformal threshold with an FPR guarantee, zero-shot to unseen tasks, is now consensus (FIPER does it near-verbatim and beats the FAIL-Detect lineage; Sentinel is the success-only root). So a detector *trained on labeled failures* is the wrong-distribution mistake the field already corrected. The open problem is what to *do* with the flag while keeping the guarantee, and whether the strongest internal-feature detectors transfer across policies.

**First-principles** — *Principle:* a failure is an OOD event against the success manifold, so you can spot it from successful runs alone; a conformal threshold caps the false-alarm rate with a guarantee that holds even on a small calibration set. *Challenged:* not "detection needs failure-labeled data" (dropped by Sentinel/FIPER) but that *detection is the deliverable* — closing a detect-then-*act* loop generally *breaks* the FPR bound (the action changes the distribution the calibration assumed), and internal-feature detectors are policy-internal so may not transfer. *Wager:* both structural sub-claims are real and untested.

**Sharpest questions** — 1) Does a detect-then-act loop (flag → RAIL backup / SCDA safe-adapt) *preserve* the conformal FPR guarantee while cutting user-facing failures? 2) Does SAFE's internal-feature detector fail to transfer across architectures, and does a policy-agnostic density backstop (FAIL-Detect/RC-NF) recover it? 3) Do step-level localization (Hide-and-Seek) + root-cause (RAPT) enable a *targeted* response that recovers more SR than binary detect-then-halt?

> [!warning] Risks
> - Conformal validity needs a calibration set of successes → calibrate per FAIL-Detect's success-only protocol on the deployment distribution; re-calibrate on domain shift.
> - Internal-feature detectors are model-specific → pair with FAIL-Detect's/RC-NF's policy-agnostic density score as a model-independent fallback.
> - Detection without response is inert → wire the flag to E2's shield or E1's safe adaptation so detection drives a bounded response.
