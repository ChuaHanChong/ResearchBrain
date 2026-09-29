# Study Bench · Robot Learning: structure and content plan

**Status:** plan v1.2, 2026-09-29. Manipulation focus; navigation dropped; grasping topic added. Nothing is implemented yet.
**Target:** `studies/playground/study-bench-robot-learning.html` plus a published artifact. It follows Study Bench design system v2.7 exactly: the same eight pages, PageShell, TopicPage order, EquationKey, faceted filters, demos and QA harness.
**Sources:** 16 of the 17 papers in the Robot-Learning project (P12, navigation, is out of scope), all read through alphaXiv. Together they are the site's "book". Two additions are allowed, and both are labeled: standard textbook forms (`.sb-prov`), and a small set of **primary papers that the corpus cites** for the grasping topic (see §1.1), marked "Primary source, cited by P01 / P05".
**Focus:** manipulation. Locomotion and navigation appear only where they serve manipulation (loco-manipulation, mobile manipulation).

---

## 1. The corpus ("the book")

Short IDs follow the project filenames. They are used in `.sb-ref` tags, e.g. `[P04 §4]`.

| ID | Paper | Main role on the site |
|---|---|---|
| P01 | Towards a Unified Understanding of Robot Manipulation (2510.10903, v2) | Spine of the site: three-layer stack, X→Z→A pipeline, the policy-head family tree, the VLA tree |
| P02 | VLA Models for Robotics: Toward Real-World Applications (2510.07077) | The **seven VLA architectures**, the design timeline, data and hardware |
| P03 | World Model for Robot Learning (2605.00080) | WM–policy coupling (IDM, single-backbone, MoT, unified, latent); WM as simulator; **LIBERO / CALVIN / RoboTwin / SIMPLER tables** |
| P04 | World Action Models: A Survey, "Dream Less, Act More" (2606.20781) | **3 philosophies** + **(Φ, F, B, D) anatomy**; census of about 110 WAMs; deployment-cost equations |
| P05 | Data Pyramid for Embodied Manipulation (2607.24744) | Five-layer pyramid, collection paradigms, data recipes, cross-embodiment alignment |
| P06 | Robot Learning from Human Videos (2604.27621) | Task / observation / action bridges, latent actions, retargeting, 50-dataset atlas |
| P07 | Deep RL for Robotics: Real-World Successes (2408.03539) | Four-axis taxonomy, **L0–L5 maturity levels**, why locomotion succeeded |
| P08 | Sim-to-Real Methods in RL with Foundation Models (2502.13187) | Sim-to-real techniques grouped by the MDP element they act on (O / A / T / R), gap definition G(π) |
| P09 | Humanoid Locomotion and Manipulation (2501.02116) | Contact planning → MPC → WBC → learning → foundation models |
| P10 | Tactile- and Force-aware Robot Learning (2608.07558) | TF-ART phases 0–3, fusion operators, compliant controllers |
| P11 | Embedding Physics Priors in Robot Learning (2609.22319) | Guided / encoded / informed; DeLaN, HNN, NODE, PINN, SINDy, Koopman |
| ~~P12~~ | Vision-and-Language Navigation survey (2607.09792) | **Not used.** Out of scope for the manipulation focus; stays in the project |
| P13 | Safety in Embodied AI (2605.02900) | Five capability–risk layers, attacks and defenses (FlowHijack, SilentDrift, VLSA) |
| P14 | No Free Checker: Verifiers for Robot Policies (2609.09250) | Four judge sources, the availability–credibility trade-off, **failure detectors**, validating the verifier |
| X1 | World Action Models: The Next Frontier (2605.12090) | Cascaded vs Joint (AR / diffusion / multi-stream); the second WAM taxonomy |
| X2 | Robot Learning: A Tutorial (LeRobot, 2510.12403) | Pedagogical spine: classical → RL → BC (ACT, DP, FM) → π0 / SmolVLA, with equations and async inference |
| X3 | World Models for Robotic Manipulation (2606.00113) | Representation spectrum, prediction–action interface, PRIOR → REFINE → ADAPT lifecycle, WM metrics |

### 1.1 Primary grasping papers (read during the build)
P01 §4.1 and P05 §6.8 name the key grasp models only in a line each. To teach them properly, the build reads these cited primary papers through alphaXiv. Each is labeled as a primary source and linked to the survey that cites it:
- **Datasets and benchmarks:** GraspNet-1Billion, Grasp-Anything / Grasp-Anything++ / Grasp-Anything-6D, DexGraspNet, Dex1B
- **Detectors and generators:** GG-CNN, GR-ConvNet, 6-DoF GraspNet, Contact-GraspNet, AnyGrasp, EquiGraspFlow
- **Language-driven and foundation models:** LGD (language-driven grasp detection), GraspGPT, ThinkGrasp, RT-Grasp, VCoT-Grasp, GraspMolmo, GraspVLA (SynGrasp-1B)
- **Dexterous:** DexDiffuser, Grasp as You Say, D(R,O) Grasp

**Integrity rules specific to this site**
- Every number carries a `[Pxx §/Table]` ref. Results tables are labeled "As reported in P03; conditions not matched".
- Equations the papers describe only in words (RSSM ELBO, CEM/MPPI, CBF, PPO, DR objective, conformal quantile) are `.sb-prov` "standard form".
- **Where the papers disagree** is a first-class feature (see §6), not a footnote.
- The site is a study resource for the corpus only; it carries no framing from outside research projects.

---

## 2. Site identity

- **Name:** Study Bench · Robot Learning. **Monogram:** `RB` (confirmed; `RL` is taken by the RL site). **Accent:** petrol, as on the other sites.
- **Hero lede (≤40 words):** "How robots learn to act, from control loops and reward to VLAs, world action models and verifiers. Sixteen surveys, one map: follow each method's lineage, open its architecture and run it on a bench."
- **Color roles** (aliases of `data-1..7`):
  - `mod-vision`, `mod-lang`, `mod-action`, `mod-future` (predicted observation), `mod-touch`, `mod-latent`
  - `layer-plan` / `layer-policy` / `layer-control` for P01's three layers

---

## 3. Page structure (the standard eight)

### 3.1 Overview `#overview`
1. **Hero** + PageGuide.
2. **Robot learning in one picture.** A FlowDiagram of the full stack:
   - data pyramid → pretraining (VLM / video / human video) → policy (VLA or WAM) → post-training (RL, verifier rewards) → deployment loop (chunk → controller → robot → observation)
   - with a verifier / safety monitor on the side.
   Every node jumps to its topic.
3. **The three layers (P01 Fig. 12).** Planning → action modeling → actuation. Click a layer to see the artifacts that pass between layers (plan, code, affordance, video → target pose / latent → torques).
4. **Course map.** Topic DAG with progress, built from each topic's "Builds on" list.
5. **Manipulation task map.** P01 §4's task families: grasping, basic, dexterous, deformable, bimanual, mobile, humanoid. Each tile shows its topic, key methods and benchmarks.
6. **Paper shelf.** 17 cards, each with scope, taxonomy thumbnail, year, and "used in topics …". Filterable.
7. **Chapter summaries.** One card per Part, each with a key equation + EquationKey.
8. **Where the field is going.** A frontier map clustering the open problems from all 17 papers: latency ("dream less"), contact and touch, failure data, evaluation, safety, data recipes. Each cluster lists the papers that raise it.

### 3.2 Topic Explorer `#explorer` — 22 topics in 6 Parts
Every topic uses the TopicPage order:
- Orientation / Before you start
- Why this exists
- Key concepts (term cards)
- Methods in this topic (method cards → Compare)
- Worked example or Algorithm box
- FlowDiagram
- Inline mini-demo
- What to remember
- Quiz + flashcards
- Previous / Next pager

**Part A — Foundations**

| # | Topic | Sources | Core content | Diagram / visual | Mini-demo |
|---|---|---|---|---|---|
| A1 | The robot-learning problem | P01 §2, §5–6, X2 ch.1–2, P07 (POMDP) | POMDP; classical vs learned; the three layers; X→Z→A; why classical pipelines are brittle | Three-layer stack; X→Z→A pipeline | Toggle an input / latent / decoder cell and see which methods live there |
| A2 | Control the policy sits on | P09 §V–VI, P10 §6, P11 §2 | Rigid-body dynamics $M\ddot q+C\dot q+G=\tau+J^\top\lambda$; PD / impedance / admittance / hybrid; MPC model fidelity; WBC (HQP vs WQP) | Four control loops (P10 Fig. 6); MPC → WBC stack | 1-D wall contact: PD vs impedance vs admittance |
| A3 | Reinforcement learning for robots | X2 ch.3, P07, P09 §VII-A | DQN → DDPG → SAC; PPO (the dominant sim algorithm); RLPD → SERL → HIL-SERL; reward classifiers; L0–L5 maturity | HIL-SERL actor–learner loop; competency × level heatmap | Maturity map filter: "zero-shot + dense reward + PPO" pattern |
| A4 | Sim-to-real | P08, P07, P09 (ASAP) | G(π) gap; DR / ADR; domain adaptation; GAT grounding; action delay MDPs; teacher–student / RMA; asymmetric actor-critic | MDP ring with the four gap sources; teacher → student distillation | DR range slider on a cart-pole, tested against a hidden "real" parameter |

**Part B — Imitation and policy architectures (evolution, part 1)**

| # | Topic | Sources | Core content | Diagram | Mini-demo |
|---|---|---|---|---|---|
| B1 | Behavior cloning and why it breaks | X2 ch.4, P01 §6.1.2 (IL tree) | BC objective; compounding error; multimodality (mean collapse); DAgger family | Covariate-shift picture | MSE-BC collapses on a bimodal "left or right" task |
| B2 | Generative policy heads | X2 (ACT, DP, FM), P01 §6.4 | ACT (β-CVAE + chunking + temporal ensembling); Diffusion Policy (DDPM / DDIM); flow matching; consistency and one-step; SSM, frequency and drift heads | ACT, DP and FM architecture figures; P01 policy-family tree | Denoising steps: curved diffusion paths vs straight flow paths |
| B3 | Action representations and inference timing | P02 §IV, X2 (async), P01 §6.4.8, P05 §7.2.2, P04 §4.4 | Binning (256 bins); FAST (DCT + BPE); continuous L1; latent actions; chunking; RTC; async inference and its threshold g; semantic action slots; UMI relative trajectories | Async client–server queue (X2 Fig. 32) | Queue-size plot for g = 0 … 1 |
| B4 | Vision-language-action models | P02, P01 VLA tree, X2 ch.5, P09 §VIII | Definition; **seven architectures**; RT-1 → RT-2 → OXE → Octo → OpenVLA → RDT-1B → π0 → FAST / OFT → π0.5 → GR00T N1 → SmolVLA → π0.7; knowledge insulation; dual-system; freeze vs LoRA vs full fine-tune | Seven mini-stacks (P02 Fig. 4); π0 vs SmolVLA block diagrams + attention masks | Architecture builder: backbone × head → cell |

**Part C — Predictive models (evolution, part 2)**

| # | Topic | Sources | Core content | Diagram | Mini-demo |
|---|---|---|---|---|---|
| C1 | World models | X3 §II–IV, P03 §1–3, X1 §3 | Definition (predictive, world-grounded, intervention-aware); lineage Dyna → PILCO → Ha & Schmidhuber → PlaNet → Dreamer / V3 → DayDreamer → TD-MPC2 → V-JEPA 2 / DINO-WM → video foundation WMs; the five representations (pixel → latent → flow → 3D / 4D → physics) | RSSM imagination loop; representation spectrum (X3 Fig. 2) | CEM planning in a toy latent model |
| C2 | World action models | P04, X1, P03 §3 | VLA vs WM vs WAM; three routes (cascade / score / joint); P04's three philosophies; the (Φ, F, B, D) anatomy; X1's cascaded vs joint (AR / unified / multi-stream / MoT); "video at train time, optional at test time" (Fast-WAM, UVA, UWM) | P04 Figs. 1–2, 4–6; X1 Figs. 5–6 | "One joint distribution, four queries" |
| C3 | World models as simulator, evaluator and data engine | P03 §4, X3 §V–VI, P05 §5.5, X1 §3.3 | RL in imagination (WMPO, World-Env, VLA-RFT); co-evolution; candidate ranking (GPC); MCTS; DreamGen pseudo-actions; the PRIOR / REFINE / ADAPT lifecycle; WM metrics (PSNR, FVD, rank correlation, hallucination rate) | P03 Fig. 5 (RL loop and validation); X3 Figs. 4–5 | Imagined vs real success as the policy exploits simulator artifacts |

**Part D — Data**

| # | Topic | Sources | Core content | Diagram | Mini-demo |
|---|---|---|---|---|---|
| D1 | The data pyramid | P05, P02 §VI, P01 §7.1 | Five layers × scalability vs alignment; collection paradigms (script, teleop, HITL); UMI; sim data (MimicGen, InternData); data recipes π0 → π0.7, GR00T, Qwen-RobotManip | Pyramid with two axes; UMI pipeline | Data-recipe mixer (Illustrative) |
| D2 | Learning from human videos | P06, P05 §4 | Three gaps; six bridges; TCN / R3M / VIP / MVP / VC-1; Phantom-style embodiment transform; affordances; LAPA latent actions; retargeting as optimization | P06 Fig. 3; LAPA three-stage pipeline | Route-selection wizard (P06 Table 9) |

**Part E — Manipulation skills and embodiments**

| # | Topic | Sources | Core content | Diagram | Mini-demo |
|---|---|---|---|---|---|
| E1 | **Grasping: from analytic grasps to grasp-anything models** | P01 §3.1 (Table 1), §4.1 (Fig. 4); P05 §6.8, Tables 5–6; P07 (Dex-Net, QT-Opt, push-grasp synergies); P02 (GraspVLA, DexGraspVLA); P04 / X1 (AnyGrasp inside RIGVid); primary papers §1.1 | Grasp representations: 5-D rectangle $(x,y,w,h,\theta)$, 6-DoF pose + width + quality, suction, dexterous hand configuration. Analytic grasping (geometry, force closure, GraspIt!). How the datasets evolved: Cornell → Jacquard → GraspNet-1B → ACRONYM → Grasp-Anything (1M images, ~600M grasps) → Dex1B (1B) → RealVLG-11B: manual → automatic labels, rectangles → 6-DoF → dexterous, single object → clutter, vision → language. P01's four families: (a) vision-only (CNN → GR-ConvNet → point-cloud VAE / Contact-GraspNet / AnyGrasp / SE(3)-equivariant flows); (b) language–vision fusion; (c) planner-guided candidates ranked by an LLM / VLM (GraspGPT, ThinkGrasp, OWG); (d) end-to-end grasp foundation models (RT-Grasp, VCoT-Grasp, GraspVLA). Dexterous grasp generation (DexGraspNet → DexDiffuser → Grasp as You Say → Dex1B). Grasping by RL at scale (QT-Opt 580K attempts) | P01 Fig. 4 four families; representation ladder; dataset timeline | Place a rectangle grasp; watch the antipodal / friction-cone check pass or fail |
| E2 | Dexterous and in-hand manipulation | P01 §4 (dexterous), P07 (Dactyl, DeXtreme, Visual Dexterity, in-hand), P10 (C3–C4 reorientation, in-hand), P06 (hand retargeting), P05 (DexUMI, DexMimicGen, Dex1B) | Why hands are hard (DoF, contact, occlusion); sim-to-real with massive DR; visuotactile in-hand; retargeting human hands; dexterous data sources | In-hand RL pipeline; retargeting optimization | Retarget 21 hand keypoints to a 2-finger vs 4-finger hand |
| E3 | Deformable, bimanual and mobile manipulation | P01 §4 (deformable, bimanual, mobile) + Tables 2–3, P07 (mobile manipulation, whole-body control), P02 (ALOHA / Mobile ALOHA), P05 (bimanual data, RoboTwin), P10 (B-tasks: wiping, peeling, cutting) | State representation for cloth and rope; bimanual coordination and leader–follower data; mobile base + arm action spaces; benchmarks (SoftGym, DaXBench, RoboTwin, BEHAVIOR-1K, HomeRobot) | Task-family map with benchmarks | Action-space choice for a mobile manipulator: base + arm vs whole-body |
| E4 | Humanoid whole-body manipulation | P09 (manipulation focus) | Whole-body manipulation vs loco-manipulation (Table I); contact planning; MPC → WBC; teleoperation and mocap data; humanoid foundation models (GR00T N1, Helix) | P09 Fig. 2 roadmap; Fig. 11 teleoperation loop | WBC priority: hierarchical vs weighted QP on a planar body |
| E5 | Touch and force | P10 | TF-ART phases 0–3; FiLM / attention / MoE / gate fusion; AR, MAE, VQ and InfoNCE objectives; predicting reference force and stiffness; slow–fast (RDP) | TF-ART pipeline; slow–fast loop | Gate values across approach → contact → insert |
| E6 | Physics priors | P11 | Guided / encoded / informed; DeLaN, LNN, HNN, port-Hamiltonian, NODE / VIN, residual, SINDy, Koopman, PINN; trade-offs (Table 7) | P11 Figs. 1, 3–5; DeLaN data flow | MLP vs DeLaN energy drift on a pendulum |

**Part F — Trust: verification, safety, evaluation**

| # | Topic | Sources | Core content | Diagram | Mini-demo |
|---|---|---|---|---|---|
| F1 | Verifiers and failure detection | P14, P01 §7 (SAFE, FAIL-Detect), X3 §V-E | Four judge sources; availability vs credibility; uses (curate / rank / reward / gate); best-of-N (RoboMonkey), V-GPS, KnowNo; **intrinsic detectors** (SAFE, FIPER, FAILDetect, Sentinel, Tri-Info, MG-Select, TACO); conformal bands; validating the verifier (nine metrics) | P14 Fig. 4 learned-verifier pipeline; Fig. 5 intrinsic verifiers | Conformal failure band on a toy flow policy |
| F2 | Safety of embodied AI | P13 | Five-layer capability–risk rings; cascade; VLA attacks (FreezeVLA, BadVLA, **FlowHijack**, **SilentDrift**); defenses (BYOVLA, VLSA CBF layer, SafeVLA); benchmarks | Nested rings; cascade pipeline | CBF filter overriding a nominal command |
| F3 | Benchmarks and what they miss | P03 §7, X3 §VII–VIII, P01 §3 (Tables 1–3), X1 §6 | Manipulation benchmarks (LIBERO, CALVIN, SIMPLER, RoboTwin, RoboCasa, RoboArena); grasp benchmarks (GraspNet-1B AP); WM-evaluation tiers; accuracy-at-budget; policy-rank fidelity | Benchmark atlas (year × log demos) | Results board, filtered by suite |

22 topics at up to 900 words each. Every topic lists open problems from its sources in "What to remember".

### 3.3 Evolution `#evolution` — "how the methods evolved" (the core of the request)
Sub-tabs: **Lineage · Story · Equation changes**, then the "What changed?" quiz.

**Lineage map.** Eight swim lanes on a shared time axis (2011 → 2026). Each node has: problem fixed, change from parent, key equation with key, and source ref.

| Lane | Chain (abridged) |
|---|---|
| Policy heads | BC-MLP → ACT (CVAE + chunks) → Diffusion Policy → DP3 / Consistency → flow matching (π0 expert) → one-step FM → drift-based |
| Generalist VLAs | BC-Z / Gato / VIMA → RT-1 → RT-2 → RT-X / OXE → Octo → OpenVLA → RDT-1B → π0 → FAST / OpenVLA-OFT → π0.5 → GR00T N1 → SmolVLA → π0.7 |
| Latent actions and human video | TCN → R3M / VIP / MVP → LAPA → villa-X / UniVLA / GO-1 → DreamDojo |
| World models | Dyna → PILCO → World Models → PlaNet → Dreamer → DreamerV3 / DayDreamer → TD-MPC2 → V-JEPA 2 / DINO-WM → UniSim → Cosmos / Genie Envisioner |
| World action models | UniPi → AVDC / SuSIE → GR-1 → GR-2 / PAD → VPP → UVA / UWM → FLARE → WorldVLA / CoT-VLA → GE-Act → F1 / Motus → Cosmos Policy / LingBot-VA / DreamZero → Fast-WAM → π0.7 |
| RL and sim-to-real | DQN → DDPG → SAC / PPO; QT-Opt; DR → ADR → teacher–student → RMA → ASAP; RLPD → SERL → HIL-SERL; WM-RL (WMPO); VLA-RL (SimpleVLA-RL, RECAP) |
| Verification | SayCan → KnowNo → SAFE / FAIL-Detect → RoboMonkey / V-GPS → FIPER / Sentinel → World Action Verifier |
| Grasping | force closure / GraspIt! → Cornell rectangle CNN → GG-CNN → GR-ConvNet → Dex-Net / QT-Opt → 6-DoF GraspNet (VAE) → GraspNet-1B → Contact-GraspNet → AnyGrasp → Grasp-Anything + LGD → GraspGPT / ThinkGrasp → RT-Grasp → GraspVLA → VCoT-Grasp; dexterous branch DexGraspNet → DexDiffuser → Dex1B |

**Taxonomy lens** (a segmented control) recolors the same map by:
- P02's seven architectures;
- P04's three philosophies;
- X1's cascaded vs joint;
- P03's coupling style (decoupled / shared / MoT / latent).

Nodes the papers classify differently get a ⚑ badge that links to "Where the papers disagree".

**Story (filmstrip), about 14 frames: "From tokens to flows to futures"**
1. Hand-built pipelines are brittle
2. BC averages modes
3. Chunking fights compounding error
4. Diffusion captures multimodality
5. Flow matching makes it cheaper
6. VLMs bring semantics (RT-2)
7. Scale through cross-embodiment data (OXE)
8. Continuous heads beat tokens (π0, OFT)
9. Hierarchy and knowledge insulation (π0.5, GR00T)
10. Human video through latent actions (LAPA)
11. Predict the future before acting (UniPi → GR-1)
12. Joint video–action generation (UWM, Cosmos Policy)
13. "Dream less, act more" (Fast-WAM, latent-only, P04)
14. Checking before acting (verifiers, P14)

**Equation changes** (with `sb-new` / `sb-chg` diffs):
- **Chain 1, the policy objective:**
  1. BC MSE
  2. → ACT β-CVAE ELBO
  3. → DDPM ε-loss on an action chunk (DP)
  4. → conditional FM velocity loss
  5. → π0 FM with Beta-τ and VLM conditioning
- **Chain 2, what is modeled:**
  1. $p(a\mid o,l)$ (VLA)
  2. → $p(o'\mid o,a)$ (WM)
  3. → cascade $p(o'\mid o,l)\,q(a\mid o,o',l)$
  4. → scoring $q(a\mid o,l)\,p(o'\mid o,a,l)$
  5. → joint $p(o',a\mid o,l)$
  6. → $\mathcal L_{gen}+\lambda\mathcal L_{act}$
  7. → JEPA latent loss
- **Chain 3, world-model training:** RSSM ELBO (`.sb-prov`) → TD-MPC2 latent consistency → JEPA.

### 3.4 Compare `#compare`
Sub-tabs: **Side by side · Master table · Race · Decision guide**, then "Tell them apart".

- **Side by side.** Any number of methods. Rows:
  - year, org, family
  - backbone, action head, action representation / chunk, params, training data
  - control rate / inference cost, open weights
  - the label each survey gives it (P01 / P02 / P03 / P04 / X1)
  - reported results, key idea, source refs
- **Master table.** About 180 rows (VLAs, WAMs, world models, policy heads, RL / sim-to-real, verifiers). Faceted filters:
  - family, head type
  - P04 Φ / F / B / D
  - X1 cascade vs joint
  - modality (touch, force, 3D)
  - embodiment, has reported LIBERO / CALVIN / RoboTwin results
- **Race** (toy, Illustrative, reproducible):
  - Policy-head race: MSE-BC, CVAE, DDPM, DDIM, flow matching (uniform τ vs Beta τ), one-step, run on a bimodal 2-D reaching task with 20 seeds. Reports success, mode coverage, NFE and latency; mean + 95% band; sortable.
  - Second race: planners (CEM, MPPI, candidate rerank, random shooting) in the world-model sandbox.
- **Reported results board** (inside Master table as a view). P03 Tables 5–6 as-is: LIBERO four suites, CALVIN, RoboTwin, SIMPLER. Warning banner: numbers are self-reported by different papers under different conditions (P03 §7 says results depend on the benchmark).
- **Decision guide.** Seven wizards:
  1. Which policy head?
  2. Which WAM philosophy for my latency budget? (P04 §7.1, deployment cost)
  3. Which data layer to add next? (P05)
  4. Which human-video route? (P06 Table 9)
  5. Which sim-to-real technique for this symptom? (P08 gap diagnoser)
  6. Which verifier for this use? (P14 Table 5)
  7. Which grasp approach? (gripper type × clutter × language target × data; P01 §4.1)

### 3.5 Interactive Lab `#lab` — "Robot Learning Bench"
One `.sb-bench` with a station switcher in `.sb-bench-bar`. All 12 stations are in scope for this build. Every station has Watch / Guide me demos.

| # | Station | What you do | Grounding |
|---|---|---|---|
| 1 | **Policy Head Bench** | Bimodal 2-D task. Pick a head (MSE / CVAE / DDPM / DDIM / FM / one-step), step the denoiser, set chunk size and temporal-ensembling weight, inject noise, watch rollouts compound | X2 eqs. 18, 44–53; ACT 1% → 44% chunking result |
| 2 | **Action Tokenizer** | Draw a 7-DoF-like trajectory; compare 256-bin tokens vs FAST (DCT → quantize → BPE) vs VQ latent. Shows token count, reconstruction error, decode time | P02 §IV-A, X2 |
| 3 | **VLA Dissector** | Backbone × head → the seven cells; π0 vs SmolVLA attention-mask grid; KV-cache highlighter; parameter and memory bars (3.3B vs 450M) | P02 Fig. 4, X2 Figs. 37–39 |
| 4 | **Control-Loop Budget** | Sliders: $N_{fwd}$, chunk K, $f_{ctrl}$, latency, threshold g. Plots the async queue and the four deployment-cost regimes with the feasibility test $N_{fwd}(K)/K<1/f_{ctrl}$. Presets: 50 Hz VLA, DreamZero ~7 Hz, Fast-WAM, π0.7 4 s subgoals, RTC | X2 async; P04 §4.4; X1 §7.5 |
| 5 | **World-Model Sandbox** | Block-push world with an adjustable model bias. Plan with CEM / MPPI / rerank / MCTS; set horizon; see compounding error; "optimize policy in imagination" shows imagined ↑ while real ↓ | P03 §4, X3 §V, eqs. 16–19 |
| 6 | **WAM Coupling Playground** | Discrete joint $p(o',a\mid o,l)$ on a toy push world: marginalize or condition to get policy / passive WM / controllable WM / IDM; switch cascade / score / joint; UWM per-modality noise dials; leakage toggle; IDM Turing test | P03 eqs. 4–8, P04 §2 and §4.2, X1 §4 |
| 7 | **Failure Detector and Verifier Lab** | Toy flow policy with success and failure rollouts. Single-pass uncertainty trace; time-varying conformal band (set α, read detection time and FPR); best-of-N with a noisy VLM verifier vs value vs intrinsic score; proxy-gain / reward hacking; FlowHijack-style trigger injection | P14 §4–6, P13 §5.1 |
| 8 | **Sim-to-Real Station** | Cart-pole / hopper: DR ranges, constant and random action delay, GAT grounding with a learned $f_{real}$, teacher–student latent error | P08, P07 |
| 9 | **Compliance Station** | 1-D / 2-D wall contact: PD / impedance / admittance / hybrid (selection matrix S); TF-ART gate timeline; WBC priority panel | P10 §6, P09 §VI |
| 10 | **Physics-Prior Station** | Pendulum: MLP vs DeLaN vs HNN (energy drift, extrapolation); Euler vs RK4 vs symplectic integrator | P11 §3 |
| 11 | **Data Recipe Mixer** | Pyramid-layer weights → capability coverage; compare with published recipes (π0 → π0.7, Qwen-RobotManip, LingBot-VA 2.0). Labeled Illustrative: the optimum is unknown (P05 §8) | P05 |
| 12 | **Grasp Lab** | Top-down cluttered scene. Place and rotate a 5-D rectangle grasp; antipodal / friction-cone check with a μ slider; grasp-quality heatmap; sample candidates and rank them by geometry, or by a language target ("the mug handle") as in the planner-guided family; 6-DoF view shows approach direction; switch gripper: parallel jaw / suction / 3-finger | P01 §3.1, §4.1; P05 §6.8; primary papers |

Below the bench: `details.sb-demo-list` with one demo card per topic.

### 3.6 Reference `#reference`
Sub-tabs: **Formula sheet · Review cards · Where the papers disagree · Dataset atlas · Paper shelf**

- **Formula sheet.** About 60 equations with EquationKey, faceted by group:
  - Learning (BC, RL, SAC, PPO)
  - Generative heads (CVAE, DDPM, FM, π0)
  - Tokenization
  - World models and WAMs (P04 objectives, deployment cost, JEPA)
  - Sim-to-real (G(π), DR, GAT)
  - Control (impedance, admittance, hybrid, WBC)
  - Physics (Euler–Lagrange, HNN, PINN)
  - Fusion (FiLM, InfoNCE, VQ)
  - Metrics (SR, SPL, nDTW, FVD, Spearman ρ, hallucination rate, STL margin, conformal quantile)
- **Where the papers disagree** (this site's version of "Differences from the book"):
  - Taxonomy conflicts:
    - FLARE / FRAPPE / LDA-1B / DUST are *Joint Diffusion* in X1 but *Video-Generation-Free* in P04.
    - VPP / mimic-video are *Cascaded-Implicit* vs *Latent-Only*.
    - LAPA / villa-X count as WAMs in X1 but not in P04.
  - Definitional conflicts: what counts as a WAM (P04 excludes auxiliary-loss VLAs; X1 requires an "active predictive commitment").
  - Numeric inconsistencies:
    - DROID 18 vs 13 institutions (P02)
    - SmolVLA 6× vs 7× memory (X2)
    - OXE 1.4M (P01, P02) vs 2.4M (P05)
    - GE-Act citation (P03)
    - DexWorldModel vs CLWM (X1)
  - Every `.sb-prov` item on the site.
- **Dataset atlas:**
  - bubble chart (year × log scale, colored by pyramid layer);
  - tables from P01, P02, P05 and P06 (real robot, sim, human video, general).
  - Benchmarks are **not** here: they live in topic F3, which owns the benchmark atlas, metric definitions and the reported-results discussion.

### 3.7 Glossary `#glossary`
Visual · Map · A–Z. About 220 terms in 16 groups:
- learning paradigms, policy heads, action representation, VLA
- world models, WAM, data, human video
- sim-to-real, control, grasping, dexterous / deformable / bimanual, humanoid, touch / force, physics priors
- verification, safety / evaluation

One `TERMS` dictionary feeds autolink, search and the map.

### 3.8 Notation `#notation`
The papers use clashing notation, so the site defines a **house notation** and a **per-paper concordance** (allowed here because every column comes from the site's own corpus). House notation:
- $o_t$, $s_t$, $l$ (instruction), $a_t$, chunk $a_{t:t+H}$, $o'$ (future)
- $z$ (latent), $\Phi$ / $F$ / $B$ / $D$ (P04 axes), $\pi_\theta$, $q_\psi$ (action head), $p_\theta$ (predictor), $V$ / $Q$, $\gamma$
- $\tau\in[0,1]$ = flow / diffusion time, following π0
- $\xi$ = trajectory, to avoid the τ clash
- $M, C, G, J, \lambda$ = dynamics

Symbol anatomy covers the π0 FM loss, the WAM joint loss and the impedance law.

---

## 4. Diagram inventory (FlowDiagram / inline SVG, all theme-aware)

1. Full-stack pipeline (Overview)
2. P01 three layers
3. X→Z→A
4. MDP ring with gap sources (P08)
5. HIL-SERL actor–learner
6. Teacher → student / RMA
7. GAT loop
8. ACT train / infer
9. Diffusion Policy U-Net
10. π0 (VLM + action expert, block mask)
11. SmolVLA
12. Seven VLA stacks
13. Async inference client–server
14. LAPA three stages
15. RSSM / Dreamer imagination loop
16. Representation spectrum
17. WAM three routes
18. Three philosophies
19. (Φ, F, B, D) anatomy
20. Cascade / joint / multi-stream patterns
21. WM-as-simulator RL loop
22. Candidate validation
23. PRIOR → REFINE → ADAPT
24. Data pyramid
25. UMI pipeline
26. Human-video bridges
27. Humanoid roadmap (contact → MPC → WBC)
28. Four control loops
29. TF-ART phases
30. DeLaN data flow
31. Grasp families (P01 Fig. 4) + grasp representation ladder
32. Verifier families
33. Intrinsic failure detection
34. Safety rings + cascade

**Charts** (StudyBench.lineChart / grid spec):
- lineage timelines;
- dataset atlas;
- reported-results board;
- RL maturity heatmap;
- availability–credibility scatter (P14);
- TF-ART sensor and controller counts;
- physics-prior shares;
- grasp-dataset scale (P01 Table 1: grasps × year, log scale);
- human-video dataset bubbles.

## 5. Data model (one inline JS object)

```js
window.SB_SITE = {
  papers: [...],    // 17 entries: id, title, arxiv, date, scope, sections
  methods: [...],   // ~180: id, name, year, org, lane, parents[], labels:{P02,P04,X1,P03},
                    //   head, actionRepr, backbone, params, data, rateHz, results:[{bench, value, ref}],
                    //   keyIdea, problemFixed, eq, refs[]
  terms: {...},     // ~220
  symbols: [...],   // house notation + concordance
  coverage: {...}   // topic ↔ paper ↔ method
}
```

Lineage, Story, Side by side, Master table, Decision guide and search all read from `methods`. Nothing is duplicated.

## 6. Build phases (after you approve this plan)

1. **Scaffold.** Shell with 8 pages, study-bench.css / js inline, the `SB_SITE` data model (papers + methods + terms), Overview.
2. **Parts A–B** + Evolution (policy and VLA lanes) + Lab stations 1–4.
3. **Parts C–D** + WM / WAM / data lanes + Compare (all views) + stations 5–6 and 11.
4. **Parts E–F** (read the §1.1 primary grasping papers first) + stations 7–10 and 12 + Reference / Glossary / Notation.
5. **QA:**
   - qa.js (nav, 400 / 1280 px, both themes, every demo to its last step)
   - `StudyBench.audit()` word limits, axe
   - coverage check: every paper → ≥1 topic; every method → lineage or table
6. **Publish.** Artifact, a local copy in `playground/`, project notes `claude/study-bench-robot-learning.md`.

Expect a single file of roughly 3–4 MB, similar to the RL site.

## 7. Decisions (settled 2026-09-29)
1. **Name and monogram:** Study Bench · Robot Learning, `RB`.
2. **Lab scope:** all 12 stations.
3. **Outside research:** none. Topic F1 and Station 7 present the corpus neutrally; no personal-research framing and no extra sources.
4. **Topics:** 22. Navigation (P12) is dropped; the site focuses on manipulation. F3 (benchmarks) stays a topic in Part F, not a Reference tab.
5. **Grasping:** new topic E1 plus the Grasp Lab station and a Grasping lineage lane, including the grasp-anything family. Dexterous (E2) and deformable / bimanual / mobile (E3) topics added for manipulation depth.
