---
title: "Focus Direction: The Explicit-Coupling Whole-Body Research Program"
aliases:
  - "Focus Direction"
  - "Explicit-Coupling Direction"
tags:
  - humanoid
  - embodied-AI
  - robotics
---
# Focus Direction: The Explicit-Coupling Whole-Body Research Program

> [!abstract] The reduced direction
> Of ~77 directions across [[Embodied-AI|umbrella]] + six mechanism/capability docs: **six clusters** reduce to **one thesis** — *explicit coupling of jointly-controlled subsystems* — carried by **three anchor channels**, composed by **three mechanism roles**. Two physically coupled subsystems controlled together: joint value doesn't factor. Cross-term is low-dimensional, structured quantity to **predict**, not data to collect.
>
> Whole-body control instantiates along two axes. Two channels on **force-transmission** axis — two *dominant* ways an arm's forces reach support legs: **arm↔leg** (reach = self-induced *inertial* reaction) and **force-under-load** (external contact *wrench* propagates to support polygon). Gravity/CoM folded into grounded model; arm-velocity-induced Coriolis cross-term predicted inside channel A (not separate channel). Third, **base↔arm**, *kinematic* coupling on separate axis — base velocity itself a manipulation DoF. Two force channels (A, C) share *output* machinery (feedforward wrench legs compensate); B factors the action.
>
> Field's proof-of-life sits on arm↔leg channel (only channel with published number): making coupling *count at all* already widens out-of-distribution margin from ~41% (GR00T N1.5) / 44% (pi0.5), monolithic generalist VLAs, to ~62% (HEX's *implicit* MoE-coupled policy, 79.8% in-distribution on the same seven tasks). Field's borrowed proof-of-life on scene-generalization axis, not the disturbance/coupling-OOD axis this program targets — counts as precedent, not this program's own claim. Bet here: next increment. Making coupling an *explicit predicted term* adds further explicit-over-implicit margin the falsifier must measure, pre-registered to count only at >= 5 pp ($\delta_{1A}$), concentrated where cross-term largest. **Not** a head start for A over B and C: same explicit *move* runs across all three channels **in parallel**; for B and C, stage one (coupling counts at all) is co-equal bet each tests, not a number already measured. Three co-equal in *that bet*, not in mechanism *depth*: A deepest (carries own reactive-observer + analytic-residual baselines), C rides A's shared wrench head (different prediction problem, same output machinery), B thinner *factoring-only* claim, no reactive-observer comparator. Co-equal billing on explicit-coupling move, not depth of mechanism.
>
> | Role | Cluster | The bet |
> |---|---|---|
> | **Anchor — arm↔leg** (inertial) | [[Whole-Body\|WB · A]] | make arm→leg coupling *explicit predicted term*, not residual legs absorb |
> | **Anchor — base↔arm** (kinematic) | [[Whole-Body\|WB · B]] | make base a *manipulation DoF*, factored base→torso→arm not flat-concatenated |
> | **Anchor — force-under-load** (external) | [[Whole-Body\|WB · C]] | *anticipate* external hand wrench + base/leg reaction it induces, not stiff-reject it |
> | **Predict** | [[WAM\|WAM · A]] | imagine cross-term wrench as modeled *output*, sensor-free at deploy |
> | **Ground** | [[Sim2Real\|S2R · B]] | recover real physics by differentiable system-ID so term grounded, not guessed |
> | **Verify** | [[Embodied-AI\|EAI · B]] | causal-consistency metric (today imagination↔action) extended to bind predicted↔realized coupling across all three channels |

## The loop

*Intended* composition: three coupling channels feed one thesis, three mechanism clusters predict / ground / verify all three. Which hand-offs card-wired vs seams still to build — honest whole picture further down (under [[#How the clusters compose — co-solvable builds and the real sub-pipelines|How the clusters compose]]).

```
   WB · A: arm↔leg     WB · B: base↔arm     WB · C: force-under-load
  self-induced inertial    base as a manip DoF      external contact wrench
   δ_base = M_b,a · q̈_arm    p(a_arm | a_base)         J_ext^T · F_ext
        └──────────────────────┼──────────────────────┘
                   the explicit-coupling thesis
                  (don't factor the joint value:
           predict the cross-wrench A/C, factor the action B)
                                │
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
     WAM · A                Sim2Real · B           Embodied-AI · B
    ── predict ──           ── ground ──            ── verify ──
   imagine the            calibrate the           measure imagination
   cross-term wrench      physics per channel     ↔ realized coupling
   (most literal for C)   (inertia/contact/obj)    (causal consistency)
         └──────────────────────┴──────────────────────┘
              serving ALL THREE coupling channels
          one thesis, three channels, three mechanisms
```

## The thesis — why explicit coupling

Part-wise policy discards a term the physics actually has; same structure shows up three ways. Inertia matrix $M(q)$ non-block-diagonal, so arm acceleration *is* base/leg disturbance — cross-term $\delta_{\text{base}} = M_{\text{base,arm}}\,\ddot q_{\text{arm}}$ (channel **A**, self-induced). Base velocity moves reachable workspace, so right arm action *conditional* on base motion (channel **B**, kinematic). External hand wrench doesn't stay at hand: propagates through $J_{\text{ext}}^{\top}$ to every joint incl. support legs keeping centre of mass over feet — cross-term $J_{\text{ext}}^{\top} F_{\text{ext}}$ (channel **C**, external). Each cross-term low-dimensional, structured, to **predict** (A, C) or **factor** (B), not collect. Bet is **cross-capability**: same cheap explicit coordination term beats far larger data/compute budgets — three channels cover two *dominant* force-transmission pathways (self-induced inertial A, external-contact C) plus separate kinematic axis (B), so program tests *one thesis three ways* not one instance, two-arm coordination as corroborating precedent. Program **bets** coupling term outweighs large-scale pretraining on fixed budget — wager the cluster falsifiers test: if holds, coupling component is single largest contributor, pretraining second-order, architecture the lever, data only buys generalization *breadth*. Honest deliverable: crossover boundary, not declared winner.

**Three coupling anchors — WB·A (arm↔leg), WB·B (base↔arm), WB·C (force-under-load) — co-equal lead improvements to whole-body capability, improved in parallel;** three mechanism clusters predict / ground / verify all three. **A and C are *force* channels:** legs compensate what arms feel — self-induced (A) or external (C) — share *output* machinery (feedforward wrench fed to policy, legs compensating downstream) + WAM imagination-move. Differs in *prediction problem*: A's reaction computable from robot's own commanded $\ddot q_{\text{arm}}$ + inertia model; C's wrench exogenous, must be *anticipated* from context, load, contact state. That pairing — internal reaction a reach induces (A), external reaction a load imposes (C) — is the two-dominant-pathway structure program leans on. Gravity/CoM folded into grounded model; arm-velocity-induced Coriolis cross-term predicted inside channel A (not separate channel). **B is *kinematic* channel:** base velocity itself manipulation DoF; field's navigate-then-fixed-base default freezes base before arm acts, discarding in-task repositioning that extends workspace — same factoring error a layer out. All three: humanoid-distinguishing coupling no part-wise stack keeps. Maximal idea-boundedness × humanoid-distinguishing weight is what a solo team betting ideas, not capital, should hunt.

**Why exactly these six clusters** — each fills role no other can; drop any one, hole opens: no **WB·A** → no self-induced inertial coupling; no **WB·B** → thesis misses kinematic channel; no **WB·C** → misses external-wrench channel, second dominant force pathway; no **WAM·A** (predict) → coupling is dumb regression head, not forecast rolled forward; no **Sim2Real·B** (ground) → wrong physics model collapses explicit term to implicit baseline; no **Embodied-AI·B** (verify) → can't certify bet, imagination drifts from action.

> [!tip] The falsifier — one per cluster, run three in parallel, first
> Run **three falsifiers in parallel, one per coupling cluster** (WB·A, WB·B, WB·C), each *same* cheap sim ablation testing **shared claim every direction in that cluster built on**, so pass validates cluster's **shared load-bearing premise** (necessary, not sufficient) on validated foundation, not single recipe; each direction's marginal mechanism carries own falsifier, must pass independently. **WB·A (arm↔leg):** add explicit predicted base-reaction $\hat\delta_{\text{base}} = \hat M_{\text{base,arm}}\,\ddot q_{\text{arm}}$ as policy input + auxiliary loss (anticipatory interface A1–A4 all build on). **WB·B (base↔arm):** autoregressive base→torso→arm factoring vs flat-concatenation (base-first backbone B1 contributes, B2/B3 compound on). **WB·C (force-under-load):** *anticipated* external wrench vs stiff force-rejecting tracker (load forecast C1 produces, C2 certifies). Each ablates explicit-vs-implicit on same data, same backbone, same tasks, sim, zero new data. For two *force* clusters (A, C), add third arm: reactive observer (ADAPT-style) — explicit-vs-implicit alone can't separate anticipation from reaction (pre-emption note below expands). If explicit ≈ implicit on a cluster — no OOD margin widening, no gain concentration where that cluster's cross-term largest (fast reaches for A, mid-grasp base travel for B, multi-directional load for C) — that cluster's contribution void, learned three ways at once. To keep each test honest not circular — each target defined by very model policy also learns — define each target from *deliberately perturbed* model, report explicit-over-implicit margin *as function of model error*; those margin-vs-error curves are the verify-harness deliverable. All three cheaply proving *themselves* wrong up front = what makes them good problems, not just attractive ones.

**What could pre-empt the bet.** (Two anticipatory-mechanism papers surfaced since section written, [[2603.03751|IO-WBC]] and [[2603.07095|ACLM]], *not* part of threat below — both structurally anticipatory not reactive, corroborate bet's mechanism rather than pre-empt; see WB·C below for what they change.) Reactive momentum-observer estimating *realized* disturbance post-hoc (e.g. ADAPT, 2606.16542 — "Analytical Disturbance-Aware Policy Training", reactive sensor-free whole-body disturbance *observer* estimating realized residual force/torque online, generalizes OOD; abstract verified) may already capture broad "physics-grounded coupling generalizes OOD" claim — threat applies to *both* force channels (A self-induced, C external), observer can react to either. Surviving wedge: *anticipatory feedforward* — predicting reaction *before* arm moves (A) or *before* load fully felt (C) — each force-channel's ablation must run three-way (explicit-feedforward / observer / implicit), stratified by where wrench largest. Two hazards self-test doesn't cover: on real hardware *dominant* unmodeled term may be foot-contact or actuator-bandwidth not inertial/wrench term, so grounding gate can fail for "right model, wrong dominant physics" (this is **H8 pre-gate**: before committing inertial predictor, decompose measured base reaction at worst instant, moment of maximum CoM excursion, into inertial vs foot-contact / support-polygon-transition shares; if contact share dominates, term mis-specified, channel A reframes as contact-constrained hybrid-dynamics prediction, so foot-ground/terrain contact handled as this pre-gate not a separate predicted channel; price force sensing target assumes, rank dominant terms first); and explicit-structure advantage may hold only in low-data, idea-bounded regime while fine-tuned generalist catches up at scale — honest deliverable is crossover boundary, not declared winner.

## The six clusters

Three coupling anchors, then three mechanism roles that predict / ground / verify all three. Detailed per-direction bets/evidence live in each source doc; here — role each cluster plays for coupling.

### The three coupling anchors

**[[Whole-Body\|WB · A]] — arm↔leg (inertial).** Improved as whole: four co-equal layers of one whole-body interface coupling upper-limb intent + lower-body support *before* commands issue. **A1** makes arm→leg coupling *explicit predicted term* not residual legs absorb reactively (explicit reaction head beating implicit mixture on fixed data, gain concentrated on fast-reach regime where reaction torque largest); **A4** couples same intent into command vocabulary as feasible-by-construction loco+manip latent; **A2** secures sim-to-real feasibility (balance substrate coupling needs); **A3** secures workspace feasibility, base as active transport DoF. Each layer targets the one next presumes — cluster advances as one interface no single direction delivers alone.

**[[Whole-Body\|WB · B]] — base↔arm (kinematic).** Same non-separable coupling at mobile-manipulation scale, improved as whole: one perceive-move-update-act loop from three co-equal directions. **B1** makes action single coupled joint, factored base→torso→arm, each link conditioned on upstream rather than flat base+arm vector letting drift accumulate (autoregressive factoring holding large margin over flat baselines on reach-extension tasks, collapsing to flat-concat only on fixed-base reaches); **B2** predicts *where to look* conditioned on base trajectory; **B3** carries what B2 saw out of view as in-policy large-workspace memory. Each closes loop previous opens — three compound into one whole-body controller no single direction delivers alone. One caution on B2 specifically, not B1's core bet: [[2608.02257|PanoVLA]] closes comparable gap (91.3%/73.4% vs local-view 58.6%/30.0%) with *passive* 360° sensing, no gaze action at all — genuine alternative to B2's learned-gaze premise on moving base, untested head-to-head against it, doesn't touch B1's base-first autoregressive-factoring claim.

**[[Whole-Body\|WB · C]] — force-under-load (external wrench).** External-force twin of A: unknown hand wrench propagates through $J_{\text{ext}}^{\top}$ to support polygon, so force adaptation is whole-body equilibrium problem, not arm problem. **C1** *anticipates* external wrench + base/leg reaction it induces, rather than stiff tracker rejecting force late; bet: anticipatory wrench head beats reactive rejection on OOD load, gain concentrated where wrench largest + most multi-directional. C1 shares A1's *output* machinery — feedforward wrench legs compensate — + WAM imagination-move; differs in prediction problem (A's reaction computable from own commanded acceleration, C's external wrench must be anticipated from context/load). **C2** (*certified* safe set — barrier/QP provably keeping balance + collision-freeness under load) deferred to extension layer: *certify* capstone once coupling predicted, grounded, verified.

Until now C1 had no positive anchor of its own — cluster leaned on rebutting ADAPT's reactive-observer threat, not evidence for anticipation. [[2603.03751|IO-WBC]] and [[2603.07095|ACLM]] change that: IO-WBC structurally decouples upper-body interaction execution from lower-body support (proprioceptive-only, no F/T sensor), carries 18 kg load at 80% success where SOTA reactive WBC baseline manages 0%; ACLM extends same anticipatory-wrench move to multi-robot team under ~67% mass-model error. Neither is this program's own result, but now the calibration baseline channel C's OOD-load margin gets measured against — role HEX/GR00T/pi0.5 play for channel A. Full-corpus check confirms C2 stays genuine field-level gap: 39 CBF-adjacent notes checked, zero combine certified safe set with external-wrench context on legged platform.

### The three mechanism roles

**[[WAM\|WAM · A]] — predict.** Coupling term *is* predicted wrench. **A2** imagines internal reaction wrench as modeled world-model *output*, not just policy input, so policy plans against coupling forecast even when force sensors absent at deployment — *external* wrench (channel C) is most literal instance of this tactile/force imagination. Cluster is substrate rollout rides on: **A1** fixes how dense imagined state is (train-dense, deploy-light), **A3** fixes what its latent encodes (control-relevant, not reconstruction). Two independent results now back A3's density-vs-semantics orthogonality claim rather than threatening it: [[2608.05903|Robust-WAM]] shows semantic tokens added atop dense WAM *raise* OOD success rather than washed out, [[2606.30988|MuSe]] shows mirror direction — future-video auxiliary *lowers* force-forecast error — substrate carries both without competing for capacity.

**[[Sim2Real\|S2R · B]] — ground.** Explicit term has zero advantage if physics model wrong, so **B2** recovers real physics from interaction by differentiable system-ID rather than guessing a model — arm-base inertia for A, contact model for C, manipulated object's physics for B. As named it recovers manipulated object's physics, so link to robot's own inertia/contact is a *methodological-transfer bet* (same differentiable-sysID loop pointed at URDF + contact Jacobian). **B1** sets reconstruction-fidelity ceiling recovery sits under, **B4** learns constitutive *law* (not just its parameters), **B3** turns grounded twin into data engine. Pipeline getting sharper tools, not new claim: [[2608.04842|RORA]] recovers kinematic articulation (URDF joints) a contact model needs, [[2608.06164|BendTwin]] upgrades deformable-contact model beyond axial-only spring-mass, [[2605.09954|JODA]] completes RORA's own stated gap by recovering joint-level *dynamics* — friction, damping, detents — RORA explicitly says it lacks. [[2409.17992|LoopSR]] closest existing evidence for round-over-round grounding loop this cluster's own bet depends on: real-hardware reward-vs-loop-round curve (legged locomotion) showing continual improvement across successive sim-real loops, not drift.

**[[Embodied-AI\|EAI · B]] — verify.** **B1** certifies predicted coupling equals realized coupling with causal-consistency metric jointly binding world-model quality + policy success (separately, either alone gameable) — one metric, extended to score all three channels. Cluster carries certified coupling into deployment: **B2** memory + cause-attributed failure recovery, **B3** real-time stability floor, **B4** forgetting-free continual fine-tuning so re-training doesn't erode coupling term. Two 2608-batch results sharpen what B1 must resist / can borrow. [[2607.15207|BadWAM]] is adversarial case for why visual plausibility can't be the metric: imperceptible perturbations desynchronize still-plausible imagined future from executed action, dropping closed-loop success over 50% — exactly the gap causal-consistency metric exists to catch. [[2608.04653|CoCo-WorldModel]] is free machinery toward building one: trains world model for action-counterfactual consistency (inverse/zero-action rollout branches, cycle-consistency loss), ships ARC/DE metric pair for action-response fidelity — training-side complement, candidate off-the-shelf instrument, for exactly the metric B1 must build.

## How the clusters compose — co-solvable builds and the real sub-pipelines

Two questions set build order: which single artifact discharges several directions at once, which directions actually chain output→input.

**Co-solvable builds — one artifact, several directions.**

| Build once | Discharges | Span | Strength |
|---|---|---|---|
| **Whole-body wrench predictor** (one residual head, two input-conditioning paths: $\hat\delta_{\text{base}}$ from own $\ddot q_{\text{arm}}$, $\hat F_{\text{ext}}$ anticipated; ms-latency) | WB·A1 + WB·A3 + WB·B2 + WB·C1 | cross-cluster | **strong** |
| **Differentiable real-to-sim inversion engine** (3DGS + differentiable physics) | Sim2Real·B1 + B2 + B3 + B4 | within Sim2Real·B | **strong** |
| **Dense-train / latent-deploy WAM backbone** (JEPA/DiT) | WAM·A1 + A2 + A3 | within WAM·A | **strong** |
| **Joint loco+manip action head** (unified latent + base→torso→arm factoring) | WB·A4 + B1 | cross-cluster | moderate |
| **Failure-memory + subspace-protected continual update** | Embodied-AI·B2 + B4 | within Embodied-AI·B | moderate |

**Wrench predictor is highest-leverage first build**, three-channel reframe *grows* its leverage: one residual head, two input-conditioning paths, emits both self-induced inertial reaction (A, from commanded $\ddot q_{\text{arm}}$) and anticipated external wrench (C, from context/load) — sharing feedforward output + leg-compensation while inputs differ in kind — so one during-vs-between phase-stratified study validates shared output across A1, A3, B2's balance-compensation slice, *and* C1 at once. (B is kinematic head, separate base→torso→arm factoring.) One *moderate* bundle worth tightening: **joint action head** — make base→torso→arm autoregression (B1) *be* loco/manip latent split (A4), fusing A4 + B1 into one head. (B2 + B4 bundle better left honest-moderate.)

**Sub-pipelines cards actually wire** — three chains card-traceable output→input:

1. **Whole-Body coupling mesh** (critical path): WB·A4 emit joint command → **A1** ground it in coupled dynamics → A3 hold world-frame precision under it → B2 active gaze, balance-compensated by A1 → B3 write to large-workspace memory; **WB·C1** extends mesh on external-load side (same balance compensation, driven by anticipated wrench).
2. **Sim2Real grounding engine:** B4 learn constitutive law → B1 joint real-to-sim inversion ← B3 deployment fold-back, gated on B1 fidelity; B2's amortized sysID shares engine.
3. **Embodied-AI continual-recovery loop:** B2 cross-episode failure memory ↔ B4 subspace-protected continual write.

**Whole picture** — loop up top, now every hand-off marked (solid = card-wired, dashed = seam to build):

```
 ① REPRESENT       WAM·A1 density · A3 encoding · A2 wrench-head  (one WAM backbone, the predict substrate)
       ┊┄ seam to wire: a WAM latent is not the whole-body dynamics state
 ② MAKE EXPLICIT   predict the wrench    WB·A1 → δ_base · WB·C1 → F_ext
                   factor the action     WB·B1 → base→torso→arm
       ┃ solid, card-wired within Whole-Body:
 ③ COMPOSE & ACT   WB·A4 ─► A1 ─► A3 ─► B2 ─► B3   · C1 extends the mesh  ◄── critical path
       ┊┄ seam to wire: S2R·B2 recovers OBJECT physics, not the robot's M_base,arm / J_ext
 ④ GROUND          S2R·B4 ─► B1 ◄─ B3  (B2 shares the engine)     ── solid within Sim2Real
       ┊┄ seam to wire: no card links S2R grounding ─► EAI deployment
 ⑤ DEPLOY & ADAPT  EAI·B2 ◄─► B4  (B3 sets the real-time floor)   ── solid within Embodied-AI
       ┊┄ seam to wire: EAI·B1 verifies a WAM's imagination, not the realized coupling
 ⑥ VERIFY          EAI·B1 causal-consistency metric  (now scores all three channels)
       └┄ loop-back stays LOCAL (S2R·B3 → own twin; EAI·B4 → EAI·B2), not back to ① / ②

  ─►/┃ solid = card-traceable      ┊┄ dashed = the seam IS the research (unwired in the cards)
```

> [!tip] The cross-cluster seams are the research, not plumbing
> Predict→ground→verify loop composes three mechanism clusters onto coupling by **methodological transfer**: applying predict cluster's wrench-imagination *move*, ground cluster's differentiable-sysID *machinery*, verify cluster's consistency *metric* to all three channels. Cards do **not** yet wire those cross-doc hand-offs as literal data pipeline — WAM latent isn't whole-body dynamics state, ground direction recovers object physics not URDF inertia/contact Jacobian, verify metric checks world-model's imagination not realized mechanical coupling. That gap is the point: **wiring the three seams is the contribution.** Build three sub-pipelines first; global loop is research bet this build closes.

## What to build & risks

| Build | Deliverable | Gate |
|---|---|---|
| **Three cluster falsifiers in parallel** | one per coupling cluster, each testing shared claim all its directions build on — **WB·A** inertial reaction (A1–A4), **WB·B** autoregressive-vs-flat (B1 backbone, B2/B3 ride it), **WB·C** anticipated-vs-stiff wrench (C1 forecast, C2 certifies); force clusters A/C add reactive-observer third arm; plot OOD success + balance recovery **vs** where each cross-term largest | per-cluster go / no-go (cluster fails independently; pass advances whole cluster) |
| **Ground the terms** | differentiable system-ID of base-arm inertia (A), contact model (C), manipulated-object physics for mobile-manipulation (B) from few real demos; beat domain randomization on OOD mass/load; show calibrated terms transfer sim→real | explicit terms work on real humanoid |
| **Reframe as a WAM** | coupling heads as wrench-imagining world model; sensor-free reaction *and* external-wrench forecast | forecasts survive without force sensors |
| **Verify harness** | one causal-consistency metric scoring all three channels; ships as missing **3-channel coupling benchmark** | bet is *measured*, not asserted |

All three clusters run this path in parallel: falsifiers are *same* cheap sim ablation with three different cross-terms, each de-risking whole cluster at once, ground/verify machinery shared — program tests one thesis three ways at once, not sequencing A first. Two *force* clusters (A, C) additionally share wrench-predictor artifact, so falsify/ground/reframe builds cheaper for them together than apart.

> [!warning] The one risk the direction absorbs
> Explicit coupling heads need half-decent physics model — wrong URDF or contact model poisons them, then explicit ≈ implicit, that channel's bet void. Exactly why **Sim2Real·B (ground)** is core, not extension: recovers inertia + contact physics from real data so terms grounded, not guessed. If system-ID can't be learned cleanly on a channel, fallback is that channel's implicit baseline — still produces the definitive explicit-vs-implicit ablation, which **Embodied-AI·B (verify)** makes publishable either way. Every branch, every channel, yields a result.
>
> Second, distinct failure mode surfaced by [[2608.05948|GAUGE]]: physics engines given *ground-truth-calibrated* parameters still show order-of-magnitude errors on dynamic contact + deformation, video world models hit near-perfect trajectory fit while inferring free-fall acceleration under 1% of gravity — even a channel clearing Sim2Real·B's grounding gate can still forward-simulate wrong, simulator's own solver has regime-dependent error grounding step doesn't touch. Sharpens H8 pre-gate (foot-contact vs inertial decomposition): GAUGE's worst regime, dynamic contact, is exactly H8's target — H8 should budget for engine-floor error, not only model mis-specification.

## Extensions & cross-references

> [!note] Extension layer — deferred until the core loop closes
> - [[Whole-Body\|WB · C2]] — *certify* the coupling: barrier/QP or learned-manifold projection provably keeping balance + collision-freeness under load (capstone once coupling predicted, grounded, verified).
> - [[Embodied-AI\|EAI · C2]] — port calibrated coupling across humanoids without re-learning (scale-out).
> - [[Sim2Real\|S2R · A3]] — co-optimize low-level controller *with* coupling dynamics (deploy refinement).
> - [[WAM\|WAM · B3]] — know *when* to trust coupling forecast (pairs with verify metric).
> - [[Embodied-AI\|EAI · A1]] — single-loop co-evolution jointly improving coupling + its predictor.

- **Source clusters** (6 clusters / 20 directions): [[Whole-Body]] A (A1–A4) + B (B1–B3) + C (C1–C2) · [[WAM]] A (A1–A3) · [[Sim2Real]] B (B1–B4) · [[Embodied-AI]] B (B1–B4).
- **Geometric substrate:** [[Spatial-4D]] — coupling term itself geometric, Spatial-4D's geometry-native directions a representation layer explicit-coupling head can stand on.
- **Set aside** (same thesis, weaker fit): [[Manipulation]] bimanual coordination (two-arm scale, corroborating precedent, less humanoid-distinguishing); [[Locomotion]] feasibility-corrected motion imitation (excellent, narrower).
- [[README]] — folder guide + full direction index this reduces from.