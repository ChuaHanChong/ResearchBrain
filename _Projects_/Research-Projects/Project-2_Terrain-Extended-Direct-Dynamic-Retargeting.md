---
title: Terrain-Extended Direct Dynamic Retargeting for Closed-Loop Real2Sim2Real
tags:
  - project
  - active
  - robotics
  - humanoid
  - sim-to-real
  - imitation-learning
  - optimal-control
aliases:
  - Terrain-Extended DDR
  - Closing the Loop on VideoMimic
---

# Terrain-Extended Direct Dynamic Retargeting for Closed-Loop Real2Sim2Real

> [!abstract] Thesis
> Terrain-aware real2sim2real has the irreducible truth that reconstruction fidelity and retargeting dynamics are two independent, compounding bottlenecks — a noisy terrain mesh caps whatever the retargeting stage can achieve on top of it, no matter how it's solved — which breaks the field's assumption (MeshMimic, current SOTA) that fixing reconstruction alone closes the sim2real gap, and I bet that grafting MeshMimic's published reconstruction loss-terms plus DDR's terrain-extended dynamic retargeting onto VideoMimic's own running pipeline, closed with a fold-back loop, pushes terrain tasks matching MeshMimic's two hardest (CB1/JCD1-style, published ceiling today 40%/30%) to ≥60% real SR within 3 rounds.

**Anchor:** [[2505.03729|VideoMimic]] — real2sim2real base pipeline; code public and already reproduced end-to-end in this vault (gpu1, [[VideoMimic-Reproduction-Steps]]), so Phase 1 starts from a working substrate, not a reimplementation. **Mechanism sources:** [[2605.23762|Direct Dynamic Retargeting (DDR)]] — single-stage dynamically-feasible retargeting, proven only flat-ground self-contact, extended here to terrain; [[2602.15733|MeshMimic]] — published reconstruction loss-term equations (no code/dataset release) grafted onto VideoMimic's own optimization stage, plus the numeric ceiling (Table 3) this project's own terrain tasks are measured against.

---

## Background — what the source papers already show

Verified directly against all three papers' full text (alphaXiv PDF) and this vault's own VideoMimic reproduction, not abstracts.

- **VideoMimic's own reconstruction is the weaker of the two, by a wide margin, and MeshMimic quantifies exactly how much that costs.** Table 1: WA-MPJPE 112.13 vs MeshMimic's 94.32, Chamfer distance 0.75 vs 0.61. More important than the numbers: MeshMimic's own ablation (Fig. 6b) shows plain VideoMimic reconstruction (VMM+VMT) **fails sim2sim validation on 7 of 8 terrain tasks** — quote: "With VMT, sim2sim failures become more severe (JB1, JB2, SV1, SV2, CB1, CB2, JCD1), again preventing deployment except in Walk1, where terrain interaction is minimal." Even VideoMimic-motion-on-MeshMimic-terrain (VMM+MMT) fails on 4/8. This means reconstruction quality isn't a side concern for this project — on VideoMimic's own reconstruction, most terrain tasks never even reach a sim2sim-valid state, retargeting stage notwithstanding.
- **MeshMimic's own retargeting stage is still kinematic.** `MeshRetargeting` (Sec 3.3) is an SQP-style optimizer minimizing Laplacian deformation energy of an interaction mesh (following [[2509.26633|OmniRetarget]]), under hard constraints for collision avoidance and joint limits — solved per-frame, kinematically. Dynamic feasibility is left entirely to the downstream RL stage. This is structurally the same two-stage pattern DDR calls "Indirect Dynamic Retargeting" (IDR) and proves is biased.
- **DDR's own math: the bias is provable, not hypothesized.** For Geometric Retargeting $x_{GR}$, Indirect Dynamic Retargeting $x_{IDR}$ (tracks $x_{GR}$ inside a simulator), and Direct Dynamic Retargeting $x_{DDR}$ (tracks $x_{ref}$ directly, within the feasible set from the outset): $d(x_{DDR}, x_{ref}) \le d(x_{IDR}, x_{ref})$ by construction — DDR provides a strict lower bound on tracking error versus any two-stage pipeline, because IDR's search is constrained to stay near the (already-biased) $x_{GR}$ reference.
- **DDR's measured gains from removing the bias (5 flat-ground self-motions, Unitree H1-2):** feasibility 21.74–28.38% broken (GR) → 0–3.36% (DDR); contact-sequence error e.g. one-foot-balance 21.37% (GR) → 13.71% (DDR); RL convergence 37% faster + 12% higher final reward on pistol squat versus IDR; success rate (5 seeds) e.g. balancing stick 0% (IDR) → 66.67% (DDR); zero-shot real hardware transfer on all 5 motions.
- **DDR has never touched terrain/scene contact.** All 5 evaluated motions are flat-ground, self-contact only (foot-ground). No environment mesh, no obstacle, no scene geometry anywhere in the rollout function $S_{q_0}$.
- **DDR reports no wall-clock number.** The paper tabulates RL environment-steps but never CEM/MPC solve time. "Cheap per fold-back round" is an inference, not a cited figure — the primary open risk, checked at Gate B.
- **DDR's solver is built on a public framework even though DDR's own code isn't released yet.** DDR states "source code will be made publicly available" (future tense) but its CEM-MPC runs "within the framework introduced in [24]" — **Hydrax** (`github.com/vincekurtz/hydrax`), a public GPU sampling-MPC library (JAX + MuJoCo MJX). Concrete bootstrap path for Gate 0, independent of DDR's own release timeline. DDR's own reference implementation already builds on "part of the VideoMimic framework" for keypoint extraction — VideoMimic is a natural substrate for DDR's retargeting stage, not a foreign one.
- **MeshMimic's real SR ceiling on its two hardest tasks is already known and low.** Table 3 (global-torso-position ablation on the best configuration, MMM+MMT): CB1 (climb 50cm box, walk to edge, descend single-hand) **40%**; JCD1 (jump 20cm box → climb 60cm box → descend single-hand) **30%**.
- **Neither MeshMimic nor its benchmark scenes are public.** Confirmed against the paper's full text (no code/GitHub/project-page statement anywhere, including Conclusion) and a web search (no repo found). What's usable regardless: MeshMimic's loss-term *equations* (Eq. 1–5 — contact $L_c$, TSDF penetration $L_p$, trajectory smoothness $L_{sm}$, foot-snapping $L_{fs}$) are fully specified in the paper and can be grafted onto any optimizer, including VideoMimic's own. What isn't reproducible directly: Table 3's CB1/JCD1 numbers are a published ceiling to compare against on *comparable* self-constructed tasks, not a same-data reproduction.
- **VideoMimic's own pipeline is already running in this vault** — gpu1, [[VideoMimic-Reproduction-Steps]], zero bootstrap cost for the real2sim substrate this project builds on. This is the practical reason Anchor is VideoMimic rather than MeshMimic.
- **Simulation-framework mismatch, not previously flagged.** VideoMimic trains in **Isaac Gym Preview 4** via `rsl_rl` (legged_gym-based — confirmed live on gpu1). MeshMimic trains in **IsaacLab** (paper text: "We train the policy in IsaacLab"), a different, newer NVIDIA framework. This project's RL stage follows VideoMimic's running substrate (Isaac Gym Preview 4/`rsl_rl`), not MeshMimic's IsaacLab.
- **[[2604.04539|FlashSAC]] is a plausible PPO drop-in for the *algorithm*, but its shipped wrapper targets the wrong simulator.** Verified directly against its repo (`data/.repositories/FlashSAC`, also the anchor of [[Project-1_Curvature-Conditioned-Exploration|Project-1]]): natively supports `asymmetric_observation` (agent.py:36, 350-353 — actor gets a truncated obs slice, critic gets the full one), a fit for MeshMimic-style asymmetric-PPO actor/critic splits. Ships a native **IsaacLab** wrapper (`flash_rl/envs/isaaclab.py`, `play_isaaclab.py`) — not an Isaac Gym Preview 4/legged_gym one, so it does not drop into VideoMimic's actual training substrate unmodified. FlashSAC's critic is a fixed-support `[-5,5]` 101-bin categorical, small enough to plausibly fit a DeepMimic-style bounded reward without rescaling. **Unverified:** no Isaac-Gym-Preview-4/legged_gym wrapper exists for FlashSAC; no precedent for off-policy SAC-family on phase-conditioned reference-tracking with reference-state-initialization + early-termination-on-deviation.

---

## First-principles framing

- **First principle.** Dynamic feasibility is a joint constraint over the *whole* trajectory-control-contact space, self *and* environment — but that constraint is only as good as the terrain geometry it's evaluated against. Two independent failure modes compound: a retargeting stage that optimizes kinematics first and patches dynamics later (RL) searches a strictly smaller, provably biased subspace (DDR's inequality); and a noisy or hollow terrain mesh makes even a perfectly-solved retargeting problem infeasible against the wrong geometry (MeshMimic's own VMT ablation, Background).
- **Assumption being challenged.** The field (MeshMimic, Feb 2026, current SOTA) assumes reconstruction fidelity — better human motion + terrain geometry extraction — is *sufficient* for terrain-aware real2sim2real, once achieved. It demonstrates reconstruction fidelity is *necessary* (VMT's 7/8 failure rate) but never tests whether it's *sufficient*, because its own retargeting stage stays kinematic throughout. DDR proves kinematic retargeting is biased on a narrower problem (self-contact only) the same publication cycle; neither paper cites the other.
- **The bet.** Graft MeshMimic's published reconstruction loss-terms (Eq. 1–5) onto VideoMimic's own real2sim optimization stage to close part of the fidelity gap, and extend DDR's single-stage CEM-MPC to include environment-mesh contact as the retargeting stage — both wired into a hybrid closed loop (MPC does the fast per-round correction on fold-back data, RL periodically distills across rounds). On terrain tasks matching MeshMimic's two hardest, longest-horizon, most multi-contact tasks (published ceiling 40%/30%): push real SR to ≥60% within 3 fold-back rounds. Specific numbers in [[#Falsifiable bets]].

---

## Related work — roles, not just citations

| Paper | What it actually does | Role here |
|---|---|---|
| [[2505.03729|VideoMimic]] | Monocular real2sim2real pipeline: dense-mesh terrain reconstruction + kinematic (GR-style) motion retargeting + RL, trained in Isaac Gym Preview 4/`rsl_rl`. | **Anchor.** Code public, already reproduced end-to-end in this vault ([[VideoMimic-Reproduction-Steps]]) — the base pipeline everything else grafts onto. Its own reconstruction+retargeting floor: fails sim2sim on 7/8 of MeshMimic's terrain tasks (VMT config). |
| [[2602.15733|MeshMimic]] | Fixes VideoMimic's *reconstruction* fidelity (planar-polygon scene primitives, SAM3D-Body, TSDF penetration/contact losses) but keeps a *kinematic* retargeting stage (SQP, following OmniRetarget). No code/dataset release; trained in IsaacLab. | **Mechanism source (reconstruction) + numeric ceiling.** Its loss-term equations (Eq. 1–5) are grafted onto VideoMimic's optimizer (Gate 0); its published Table 3 SR numbers are the target this project's own terrain tasks are measured against. Not an implementation dependency. |
| [[2605.23762|Direct Dynamic Retargeting (DDR)]] | Single-stage CEM-MPC retargeting, dynamically feasible from the outset, proven strictly better than kinematic-then-RL — on flat-ground self-contact only. No code release; own reference implementation already builds on VideoMimic's keypoint pipeline. | **Mechanism source (retargeting).** The retargeting stage this project extends to terrain contact. Not a competitor — DDR never attempted scene interaction, so there is no head-to-head, only an extension. |
| [[2509.26633|OmniRetarget]] | Interaction-mesh, Laplacian-deformation-energy retargeting that preserves human-object-terrain spatial relationships — kinematic, not dynamic. | **Ancestor of MeshMimic's retargeting stage**, not this project's. Confirms MeshMimic's retargeting lineage is kinematic even though its perception lineage is not. |
| [[2512.14696|CRISP]] | Contact-guided real2sim via planar scene primitives; 93.1% real2sim success rate, 43% faster RL throughput. | **Different axis (reconstruction/throughput), not retargeting dynamics.** Out of scope — not a foil, not a mechanism source. |
| [[2606.05160|GRAIL]] | Curated simulator-ready 3D asset pipeline (known object/scene/camera/scale) + video interaction priors, sidesteps ambiguous 4D reconstruction. | **Different axis (curated assets vs. in-the-wild reconstruction).** Orthogonal — could in principle supply cleaner terrain meshes, not pursued here to keep the reconstruction fix to MeshMimic's loss-terms alone. |
| [[2512.00076|Arcadia]] | Closed lifecycle loop: deployment feedback re-grounds scene assets + a shared backbone, feedback-on beats off (LIBERO 88.5 vs 86.9). Manipulation domain, not humanoid whole-body video. | **Nearest published loop-closing precedent, different domain.** Only a *single* feedback pass, no monotone-across-rounds claim — the vault's own [[Sim2Real|B2 cluster]]'s H1 gap this project instantiates for humanoid terrain tasks specifically. |
| [[2503.10118|RSR-Loop]] | Closed-loop tuning of *differentiable sim parameters* per round, not assets+policy. | **Adjacent, narrower loop-closing precedent.** Re-grounds parameters only; confirms no prior work closes the loop on asset+policy jointly for this problem class. |

---

## Killed: full MPC replacement of the RL policy

Considered during scoping and rejected, logged per the vault's standing rule to record dead candidates, not just live ones.

1. **Option:** drop RL entirely — every fold-back round is pure CEM-MPC control, deployed online.
2. **Why rejected:** MPC re-solves per scene/video; it does not build a reusable policy that generalizes across future videos without re-running the solve for each new scene. VideoMimic, MeshMimic, and DDR itself all deploy a trained NN policy onboard (Jetson Orin, 50Hz for MeshMimic) precisely because the field's actual deployment constraint is high-frequency onboard reactive control, not online trajectory optimization. Full-replace also inherits the terrain-contact compute-cost risk directly into the real-time control loop, where a solver stall is a fall, not a slow training run.
3. **What stays instead:** MPC is confined to the *offline* per-round reference-generation step (exactly DDR's own existing usage pattern — "because retargeted trajectories are computed offline, we distill them into closed-loop RL policies"). The closed loop's fold-back correction runs there, not online.

No rescue attempted — the hybrid form is not a compromise, it is what DDR itself already does within a single round; this project only extends that pattern across rounds and into terrain.

---

## Proposed method: reconstruction graft + terrain-extended DDR, in a hybrid fold-back loop

**Base substrate:** VideoMimic's own real2sim pipeline and RL training stack (Isaac Gym Preview 4/`rsl_rl`), already running — no reimplementation needed to start.

**What's added — two grafts, one loop:**

0. **Reconstruction graft (one-time, not part of the round-trip).** Add MeshMimic's kinematic consistency optimization losses (contact $L_c$, TSDF penetration $L_p$, trajectory smoothness $L_{sm}$, foot-snapping $L_{fs}$ — Eq. 1–5) to VideoMimic's own human-scene alignment optimization. This is a one-time pipeline upgrade, not a fold-back target: VideoMimic's real2sim reconstruction is a static one-time scan (established in [[Project-3_Dynamics-Fold-Back-Loop-for-VideoMimic|Project-3]]'s own scoping), so there's no natural round-over-round signal to improve it against — get it right once, then leave it alone.
1. Extend DDR's rollout function $S_{q_0}$ (currently self-body-only physics rollout under CEM sampling) to include the (now-upgraded) reconstructed terrain mesh as static collision geometry — the feasibility set $F_{q_0}$ now spans self *and* environment contact.
2. Extend DDR's cost — spatial tracking $E_p$ + Laplacian shape-matching $E_l$ — with MeshMimic's penetration loss $L_p$ and foot-snapping loss $L_{fs}$ (same equations as step 0, reused in the retargeting cost), so the retargeting stage inherits the same terrain-contact priors as the reconstruction stage rather than discovering them from scratch via CEM sampling alone.
3. Run the extended CEM-MPC offline per scene to produce a dynamically-terrain-consistent reference (replacing VideoMimic's kinematic retargeting entirely), then train the RL tracking policy on that reference in VideoMimic's own Isaac Gym Preview 4/`rsl_rl` stack.
4. After real (or sim2sim, if hardware unavailable — see Phase 4) deployment, fold failure trajectories back: re-run the extended CEM-MPC on the failed segment with the observed failure state as a new constraint/warm-start, producing a corrected reference for that segment only.
5. Accumulate corrected references across rounds; periodically (not every round) distill the accumulated set into a re-trained RL policy. Consolidation cadence is an open design choice (see Unresolved Questions). **The distillation algorithm is itself a variable** — see Phase 2.5: swapping PPO for FlashSAC targets Gate B's wall-clock break-even, conditional on porting its wrapper off IsaacLab (Background risk).

---

## Phase 0 — go/no-go gates (mandatory, before any full pipeline build)

**Gate 0 — reproduction bootstrap, two independent legs.**
- *Retargeting leg (DDR):* DDR's own code is not yet public. Build directly on Hydrax (`github.com/vincekurtz/hydrax`, public), the GPU sampling-MPC framework DDR itself is implemented on top of. If Hydrax cannot reproduce DDR's own published flat-ground numbers (Tables II–VII) within a reasonable tolerance, stop — the bootstrap path is broken and this project needs DDR's actual release first.
- *Reconstruction leg (MeshMimic loss-terms):* implement Eq. 1–5 inside VideoMimic's own optimization stage, evaluate on a public dataset both papers already benchmark on (SLOPER4D subset). Decision rule: metrics should move *directionally* from VideoMimic's own baseline (WA-MPJPE 112.13, W-MPJPE 696.62, Chamfer 0.75) toward MeshMimic's published numbers (94.32, 518.98, 0.61) — full parity isn't expected without MeshMimic's full pipeline (SAM3D-Body etc.), only the loss-term contribution is being tested. No directional movement → stop; the graft doesn't transfer onto VideoMimic's reconstruction and Gate A has no realistic chance (Background: VMT already fails 7/8 tasks).
- Both legs must pass before Phase 1 — retargeting supplies the fold-back mechanism, reconstruction supplies a terrain mesh good enough for that mechanism to have something feasible to find.

**Gate A — terrain-contact feasibility, before any RL wiring.** Take the extended rollout (steps 0–2 above) and run CEM-MPC on the project's own captured terrain scenes, built to match MeshMimic's two hardest tasks' difficulty (CB1/JCD1-style — climbing/jumping multi-contact) *without* any RL in the loop yet. Decision rule:
- CEM converges to feasible, contact-consistent trajectories (comparable feasibility/contact-error rates to DDR's flat-ground numbers, Table II/III) within a bounded number of samples → proceed to Phase 1.
- CEM fails to converge or produces high infeasibility/contact-error → the expected failure mode the Risks callout flags; do not proceed to the full loop. Scope down to a single-contact terrain task (e.g. a JB1-style box jump) as a reduced test of the mechanism, and report the terrain-scaling limit as a finding in itself.

**Gate B — wall-clock break-even.** Measure CEM-MPC wall-clock per scene on the terrain-extended rollout (Gate A's converged cases), against VideoMimic's own training cost for the equivalent task. If per-round MPC correction plus periodic RL distillation costs more wall-clock than a one-shot pipeline amortized over the fold-back rounds attempted, the "cheap fold-back" half of the thesis fails **by design**, independent of any final-SR win. Load-bearing premise for Bet 3 — check before Phase 2, don't assume it.

Both gates are pass/fail on the plan's mechanism statement. A Gate A failure changes scope (single-contact fallback, still informative). A Gate B failure is the honest signal to re-scope to a results-only claim (does terrain-extended DDR improve final SR at all, dropping the closed-loop-is-cheap half) before further investment.

---

## Phase 1 — implement and unit-verify

- Harden the reconstruction graft (Gate 0's reconstruction leg) and the extended rollout (terrain mesh + penetration/foot-snapping losses folded into DDR's cost), behind Gate A's decision.
- Regression test 1 (reconstruction): with the graft's loss weights zeroed, confirm VideoMimic's own reconstruction pipeline is bit-reproduced, isolating "did the graft break the baseline" from "does the graft help."
- Regression test 2 (retargeting): with the terrain-contact cost weights zeroed, confirm the extended solver reproduces DDR's own flat-ground numbers (Tables II–VII) on the original 5 self-motions, bit-comparable or within stochastic-seed variance.

## Phase 2 — single-shot comparison (no loop yet)

- On the project's own captured terrain tasks (comparable difficulty to MeshMimic's 8: walk1, JB1, JB2, CB1, CB2, SV1, SV2, JCD1-style), generate terrain-extended-DDR references using the Gate-0-grafted reconstruction, train RL policies in VideoMimic's own Isaac Gym Preview 4/`rsl_rl` stack, and compare training reward + sim2sim validation pass rate against (a) VideoMimic's own ungrafted baseline (this project's true floor, directly reproducible) and (b) MeshMimic's published MMM+MMT numbers (the external ceiling, cited not reproduced).
- Isolates the mechanism contribution (reconstruction graft + dynamic retargeting) from the closed-loop contribution — a single-shot grafted pipeline should already beat VideoMimic's own ungrafted baseline on the same captured scenes, before any fold-back is added.

## Phase 2.5 — RL algorithm ablation (PPO vs FlashSAC)

- Orthogonal to the retargeting-mechanism swap: on Phase 2's fixed references, train the tracking policy twice — VideoMimic's stock PPO (`rsl_rl`), and [[2604.04539|FlashSAC]] with `asymmetric_observation` on. **Precondition, not yet done:** FlashSAC ships an IsaacLab wrapper, not an Isaac Gym Preview 4/`rsl_rl` one (Background) — port or write a compatible wrapper before this phase can run at all; if that port isn't tractable, skip this phase and keep PPO throughout (non-load-bearing, see Falsifiable bets).
- If the port succeeds: confirm FlashSAC's fixed `[-5,5]` categorical critic support actually bounds the reward without saturation (quick check) before a full training run.
- If FlashSAC wins on wall-clock at matched or better final SR, promote it to the Phase 3 distillation step — strengthens Gate B's break-even margin.
- If FlashSAC's off-policy replay degrades under early-termination-heavy episodes, keep PPO and report the negative result — new information either way, nobody has tested SAC-family on this task family before.

## Phase 3 — closed fold-back loop

- On the tasks where Phase 2's single-shot pipeline still fails or underperforms (expected: the CB1/JCD1-style multi-contact long-horizon cases), run the fold-back procedure (Proposed method, steps 4–5) for up to 3 rounds.
- Report real SR (or sim2sim SR if Phase 4's hardware access does not materialize) per round, to test the monotonicity question directly — the vault's existing open [[Sim2Real|B2 cluster's H1]] bet, instantiated here: does fold-back improve monotonically, or drift?
- Track wall-clock per round against Gate B's break-even line throughout, not just at the end.

## Phase 4 — sim-to-real (conditional, not assumed)

- **Hardware access is not assumed for this project** (no Unitree G1 access confirmed at scoping time). If access is available, match MeshMimic's own real-robot protocol (Unitree G1, Jetson Orin onboard, 50Hz) so SR numbers stay comparable to its Table 3 baseline.
- If hardware is unavailable, substitute a sim2sim validation step (Isaac Gym → MuJoCo, matching this project's own training substrate) as the terminal metric throughout Phases 2–3, and report all SR claims as sim2sim, not real, with that caveat explicit in every result.

---

## Falsifiable bets

**Bet 2 is the load-bearing stop-condition.** Bet 1 is directional context only.

1. **Reconstruction graft improves fidelity, directionally (precondition for everything downstream).** VideoMimic + MeshMimic's loss-terms (Gate 0) moves WA-MPJPE/Chamfer distance toward MeshMimic's published numbers on SLOPER4D, without necessarily matching them. Failure here caps Gate A's feasibility ceiling regardless of retargeting quality (Background: VMT fails 7/8 tasks).
2. **Retargeting-quality win, single-shot (directional).** Terrain-extended DDR (Phase 2) should show lower physical-infeasibility and contact-sequence-error rates than VideoMimic's own kinematic retargeting, on the same (grafted) reconstructed scenes — analogous margin to DDR's own flat-ground GR-vs-DDR gap (Table II/III, roughly 20–30 percentage points).
3. **Closed-loop win on the hardest tasks (load-bearing).** CB1/JCD1-style tasks (own captured scenes, comparable difficulty) reach **≥60%** real (or sim2sim) SR within **3** fold-back rounds, up from MeshMimic's published ceiling of 40%/30% and from this project's own Phase-2-measured VideoMimic-ungrafted baseline — a different, not-yet-measured number from MeshMimic's own VMT figure, since VMT runs VideoMimic's reconstruction through MeshMimic's own retargeting/IsaacLab pipeline (Background), not this project's PyRoKi/Isaac-Gym-Preview-4 one; VMT's 7/8 sim2sim-failure rate is directional context for how bad the floor could be, not this project's own measured number. **If this fails, the thesis is wrong and the project stops here.**
4. **Cheap fold-back (hard precondition for Bet 3 to mean what it claims).** Gate B's break-even must hold across all 3 rounds — if closing the loop costs more wall-clock than a one-shot pipeline per unit of SR gained, Bet 3 succeeding would not validate the "closing the loop is now tractable" half of the thesis, only that more compute helps.
5. **No regression on the easy tasks.** Walk1, JB1-style, JB2-style, SV2-style, CB2-style tasks (MeshMimic's already-strong 70–100% SR bracket, Table 3 w/ pos) should not regress below MeshMimic's published numbers as a side effect of either graft.
6. **FlashSAC distillation speedup (Phase 2.5, non-load-bearing, conditional on the IsaacLab→Isaac-Gym port succeeding).** FlashSAC matches or beats PPO's final SR at lower wall-clock — widens Gate B's break-even margin if it holds, reported as a negative result either way if the port fails or the algorithm doesn't fit.

---

> [!warning] Risks
> - **Primary scientific risk:** CEM-MPC's sampling search was proven only on self-contact (foot-ground), 5 flat-ground motions. Adding environment-mesh contact multiplies the contact-mode search space the sampler must cover — this may not converge, or may converge far slower, on exactly the multi-contact long-horizon tasks the thesis targets. Gate A is designed to catch this before any RL wiring is built on top of it.
> - **Reconstruction-floor risk (new, load-bearing):** MeshMimic's own data shows plain VideoMimic reconstruction fails sim2sim on 7/8 terrain tasks (Background). If Gate 0's reconstruction graft doesn't move the needle enough on VideoMimic's own pipeline, Gate A has no realistic chance regardless of retargeting quality — this is now a first-class risk, not a footnote.
> - **Simulation-framework mismatch (new):** VideoMimic trains in Isaac Gym Preview 4/`rsl_rl`; MeshMimic trains in IsaacLab; FlashSAC ships only an IsaacLab wrapper. Phase 2.5 depends on a port that hasn't been attempted — treated as conditional/non-load-bearing precisely because of this.
> - **Wall-clock risk:** "cheap per round" is an inference from DDR's silence on timing (Background), not a citation. Gate B is the first actual measurement of it.
> - **Bootstrap risk (Gate 0, retargeting leg):** DDR's own code isn't public; this project depends on Hydrax reproducing its numbers. If reproduction fails, the whole plan is blocked on DDR's eventual release.
> - **Hardware risk:** Phase 4 is explicitly conditional — real-SR claims degrade to sim2sim-SR claims if no G1 access materializes, and every result must carry that caveat, not silently upgrade sim2sim numbers to read as real ones.
> - **Consolidation-cadence risk:** how many fold-back rounds accumulate before RL re-distills is an unresolved design choice — too frequent negates the "cheap" premise, too infrequent risks the policy tracking stale references.

---

## Unresolved questions

- Fold-back consolidation cadence (distill every round vs. every N rounds) — not fixed in advance, likely resolved empirically in Phase 3 against Gate B's break-even line.
- Whether the terrain-extended cost (DDR's tracking terms + MeshMimic's penetration/foot-snapping losses) needs re-weighting when combined, versus a straight sum — untested, first attempt uses a straight sum, revisited only if Gate A fails on that basis specifically.
- Real G1 hardware access/logistics for Phase 4 — out of scope; assumes MeshMimic's own setup if access materializes.
- Whether CRISP's or GRAIL's cleaner terrain representations (out of scope per Related Work) would raise Gate A's feasibility ceiling beyond what MeshMimic's loss-terms alone deliver — not pursued here, to keep the reconstruction fix to one borrowed mechanism.
- Whether porting FlashSAC's IsaacLab wrapper to Isaac Gym Preview 4/`rsl_rl` is worth the engineering cost versus simply staying on PPO throughout — not decided; Phase 2.5 treats it as conditional.

---

## Cross-References

- [[2505.03729|VideoMimic]] — anchor, base pipeline (code public, already running — [[VideoMimic-Reproduction-Steps]])
- [[2602.15733|MeshMimic]] — mechanism source (reconstruction loss-terms) + numeric ceiling; no code/dataset release
- [[2605.23762|Direct Dynamic Retargeting (DDR)]] — mechanism source (retargeting)
- [[2509.26633|OmniRetarget]] — ancestor of MeshMimic's (kinematic) retargeting stage
- [[2512.14696|CRISP]] — different axis (reconstruction/throughput), out of scope
- [[2606.05160|GRAIL]] — different axis (curated asset generation), out of scope
- [[2512.00076|Arcadia]] — nearest loop-closing precedent, different domain
- [[2503.10118|RSR-Loop]] — adjacent loop-closing precedent, narrower scope (parameters only)
- [[Sim2Real]] B2 cluster's H1 — the vault's existing open closed-loop bet, instantiated here for humanoid terrain tasks specifically
- [[2604.04539|FlashSAC]] / [[Project-1_Curvature-Conditioned-Exploration|Project-1: Curvature-Conditioned Exploration]] — PPO-replacement candidate for Phase 2.5, conditional on an IsaacLab→Isaac-Gym-Preview-4 wrapper port
- [[Project-3_Dynamics-Fold-Back-Loop-for-VideoMimic|Project-3: Dynamics Fold-Back Loop]] — sibling project, closes the sim2real/dynamics loop on VideoMimic's base pipeline instead of the real2sim/retargeting+reconstruction loop this project closes
