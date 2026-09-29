# Study Bench · Robot Learning: primary method-paper reading list

**Status:** v1, 2026-09-29. Companion to `study-bench-robot-learning-plan.md` (v1.3).
**What this is:** the method papers that the 16 corpus surveys name as important, grouped by site topic. The build reads each one directly through alphaXiv. Each paper is shown on the site as "Primary source, cited by Pxx".

## How "important" was decided
A paper is **Tier 1 (deep read: full text)** if at least one of these holds:
- it is a node on a lineage lane;
- a survey discusses it in depth (its own figure, equation, table row with details, or a paragraph);
- two or more surveys cite it as a representative method.

A paper is **Tier 2 (targeted read: a fact card)** if a survey's taxonomy figure or table lists it as a representative method. The fact card records:
- problem and key idea
- architecture and inputs / outputs
- action representation
- training data and scale
- headline result
- parent method

Anything a survey mentions only in passing stays **survey-level** and is labeled that way on the site.

A paper listed under an earlier topic appears again as "(→ topic)" and is counted once.
Papers that are not on arXiv (e.g. GAT, Dex-Net in Science Robotics) are read through Semantic Scholar where alphaXiv supports it. If neither works, the entry falls back to survey-level and says so.

## Totals
| Topic | Tier 1 | Tier 2 |
|---|---|---|
| A1 The robot-learning problem | 0 | 0 |
| A2 Control the policy sits on | 0 | 0 |
| A3 Reinforcement learning for robots | 10 | 13 |
| A4 Sim-to-real | 8 | 11 |
| B1 Behavior cloning and why it breaks | 2 | 5 |
| B2 Generative policy heads | 7 | 25 |
| B3 Action representations and inference timing | 7 | 4 |
| B4 Vision-language-action models | 17 | 26 |
| B5 High-level planning with LLMs and VLMs (new) | 9 | 8 |
| C1 World models | 11 | 16 |
| C2 World action models | 21 | 39 |
| C3 World models as simulator, evaluator and data engine | 8 | 19 |
| D1 The data pyramid | 6 | 18 |
| D2 Learning from human videos | 12 | 22 |
| E1 Grasping: analytic grasps to grasp-anything models | 17 | 25 |
| E2 Dexterous and in-hand manipulation | 7 | 15 |
| E3 Deformable, bimanual, mobile and soft manipulation | 6 | 30 |
| E4 Humanoid whole-body manipulation | 6 | 15 |
| E5 Touch and force | 12 | 31 |
| E6 Physics priors | 10 | 16 |
| F1 Verifiers and failure detection | 12 | 36 |
| F2 Safety of embodied AI | 12 | 25 |
| F3 Benchmarks and what they miss | 9 | 19 |
| **Total (unique)** | **209** | **418** |

### A1 · The robot-learning problem
*Surveys that cite them:* P01, X2. Framework topic: taught from the surveys; its methods live in later topics.

### A2 · Control the policy sits on
*Surveys that cite them:* P09, P10, P11. Framework topic: textbook forms (.sb-prov); learned controllers live in E4–E6.

### A3 · Reinforcement learning for robots
*Surveys that cite them:* X2, P07, P09, P01 Table 8.

- **Tier 1 (10 new):** DQN; DDPG; SAC; PPO; QT-Opt; RLPD; SERL; HIL-SERL; Residual RL (Johannink); DayDreamer
- **Tier 2 (13 new):** A Walk in the Park; Q-Transformer; MT-Opt; Eureka; DrEureka; DPPO; SimpleVLA-RL; RIPT-VLA; ConRFT; iRe-VLA; VLA-RL; Pinto & Gupta (50K grasps); Zeng push-grasp synergies

### A4 · Sim-to-real
*Surveys that cite them:* P08, P07, P09.

- **Tier 1 (8 new):** Domain randomization (Tobin); Dynamics randomization (Peng); ADR / Solving Rubik's Cube; RMA; Teacher–student terrain (Lee 2020); Asymmetric actor-critic; GAT (grounded action transformation); ASAP
- **Tier 2 (11 new):** Sim-to-real agile locomotion (Tan 2018); ANYmal actuator net (Hwangbo 2019); Perceptive locomotion (Miki 2022); RL-CycleGAN; Active DR; DROPO; IndustReal; Bi-directional DA; Walk These Ways; DCAC (random delay); Local Policies (Dalal)

### B1 · Behavior cloning and why it breaks
*Surveys that cite them:* X2, P01 Fig. 15.

- **Tier 1 (2 new):** DAgger; BC-Z
- **Tier 2 (5 new):** HG-DAgger; ThriftyDAgger; One-shot imitation (Duan); End-to-end visuomotor policies (Levine); Behavior Transformers (BeT)

### B2 · Generative policy heads
*Surveys that cite them:* X2, P01 §6.4.

- **Tier 1 (7 new):** ACT; Diffusion Policy; DP3; 3D Diffuser Actor; Consistency Policy; VQ-BeT; AdaFlow
- **Tier 2 (25 new):** iDP3; ScaleDP; MoDE; SDP; OneDP; ManiCM; FLOWER; Streaming Flow Policy; ManiFlow; MP1; FlowPolicy; PointFlowMatch; MaIL; RoboMamba; FreqPolicy; Wavelet Policy; DBPO; Implicit Drifting Policy; Chain-of-Action; Bi-ACT; ALOHA Unleashed; Dense Policy; CARP; EquiBot; EquiDiff

### B3 · Action representations and inference timing
*Surveys that cite them:* P02 §IV, X2, P01 §6.4.8, P05 §7.2.2.

- **Tier 1 (7 new):** FAST; OpenVLA-OFT; Real-Time Chunking (RTC); UMI; CrossFormer; UniAct; SpatialVLA
- **Tier 2 (4 new):** BEAST; ABPolicy; Q-chunking; Qwen-RobotManip (semantic action slots)

### B4 · Vision-language-action models
*Surveys that cite them:* P02, P01 Fig. 17, X2, P09 §VIII.

- **Tier 1 (17 new):** Gato; VIMA; RT-1; RT-2; Open X-Embodiment / RT-X; Octo; OpenVLA; RDT-1B; π0; π0.5; Knowledge Insulation; GR00T N1; SmolVLA; π0.7; CogACT; RT-H; Hi Robot
- **Tier 2 (26 new):** RoboFlamingo; HybridVLA; DexVLA; DiffusionVLA; TinyVLA; ECoT; GR-3; X-VLA; Magma; RoboDual; HiRT; Fast-in-Slow; Hume; OpenHelix; 3D-VLA; BridgeVLA; PointVLA; AgiBot World / GO-1; Gemini Robotics; Large Behavior Models (TRI LBM); MDT; Dita; BitVLA; VLA-Cache; DeeR-VLA; GR00T N1.5 / N1.6

### B5 · High-level planning with LLMs and VLMs (new)
*Surveys that cite them:* P01 §5, P09 §VIII, P02 §IV-C. Final list confirmed against P01 §5.1–5.7 in Phase 0.

- **Tier 1 (9 new):** SayCan; Inner Monologue; Code as Policies; PaLM-E; VoxPoser; ReKep; MOKA; RoboPoint; CLIPort
- **Tier 2 (8 new):** ProgPrompt; Text2Motion; CoPa; RT-Trajectory; RT-Sketch; VRB (affordances from human video); SpatialVLM; Where2Act

### C1 · World models
*Surveys that cite them:* X3, P03, X1 §3.

- **Tier 1 (11 new):** World Models (Ha & Schmidhuber); PlaNet; Dreamer; DreamerV3; TD-MPC2; V-JEPA 2; DINO-WM; UniSim; Cosmos world foundation models; Genie Envisioner; IRASim
- **Tier 2 (16 new):** TD-MPC; MoDem; Dreamer 4; iVideoGPT; DreamDojo; LeWorldModel; GWM (Gaussian world model); PIN-WM; PointWorld; Robotic World Model (Li, Krause, Hutter); Hierarchical latent world models (Zhang et al.); LaDi-WM; Vid2World; GigaWorld-0; WoW; UnifoLM-WMA-0

### C2 · World action models
*Surveys that cite them:* P04, X1, P03 §3.

- **Tier 1 (21 new):** UniPi; AVDC; SuSIE; GR-1; GR-2; PAD; VPP; Seer; UVA; UWM; FLARE; CoT-VLA; WorldVLA; F1; Motus; Cosmos Policy; LingBot-VA; DreamZero; Fast-WAM; mimic-video; VideoVLA
- **Tier 2 (39 new):** Gen2Act; Im2Flow2Act; Dreamitate; Video Language Planning (VLP); TesserAct; Vidar; VidMan; ARDuP; This&That; GR-MG; 3DFlowAction; NovaFlow; Dream2Flow; RIGVid; LVP; UD-VLA; RynnVLA-002; DreamVLA; UniVLA (Wang et al.); VLA-JEPA; JEPA-VLA; DUST; FRAPPE; LDA-1B; DiT4DiT; GigaWorld-Policy; X-WAM; BagelVLA; CoVAR; AdaWorldPolicy; PhysGen; S-VAM; Video Policy; HMA; 4DGen; TraceGen; VILP; InternVLA-A1; CoWVLA

### C3 · World models as simulator, evaluator and data engine
*Surveys that cite them:* P03 §4, X3 §V–VI, P05 §5.5.

- **Tier 1 (8 new):** DreamGen; World-Env; VLA-RFT; WMPO; Ctrl-World; GPC (generative predictive control); WorldEval; WorldGym
- **Tier 2 (19 new):** World4RL; World-Gymnast; PlayWorld; RISE; RehearseVLA; ProphRL; World-VLA-Loop; WoVR; DiWA; EnerVerse-AC; Veo world simulator (Gemini Robotics); World-in-World; DreamPlan; VLA-Reasoner; WorldPlanner; M³PC; SRPO; NORA-1.5; IRL-VLA

### D1 · The data pyramid
*Surveys that cite them:* P05, P02 §VI, P01 §3.4, §7.1.

- **Tier 1 (6 new):** Open X-Embodiment / RT-X (→B4); DROID; BridgeData V2; AgiBot World / GO-1 (→B4); UMI (→B3); ACT (→B2); Mobile ALOHA; MimicGen; RoboCasa; GELLO
- **Tier 2 (18 new):** RH20T; RoboMIND; DexUMI; FastUMI; UMI on Legs; DexMimicGen; InternData-A1; GenSim / GenSim2; RoboGen; RoboTwin 2.0; EgoScale; Re-Mix; DemInf; DataMIL; Sirius; Open-TeleVision; AnyTeleop; DexCap

### D2 · Learning from human videos
*Surveys that cite them:* P06, P05 §4.

- **Tier 1 (12 new):** Time-Contrastive Networks (TCN); R3M; VIP; MVP; VC-1; LAPA; MimicPlay; ATM (any-point trajectory modeling); EgoMimic; Phantom; Being-H0; villa-X
- **Tier 2 (22 new):** LIV; Voltron; MPI; XIRL; DVD; Vid2Robot; Track2Act; VideoDex; HRP; OKAMI; ZeroMimic; RAM; Masquerade; AVID; Moto; IGOR; UniVLA (Bu et al.); CLAP; EgoVLA; H-RDT; HaMeR; CoTracker

### E1 · Grasping: analytic grasps to grasp-anything models
*Surveys that cite them:* P01 §3.1, §4.1; P05 §6.8; P07; P02.

- **Tier 1 (17 new):** Dex-Net (ambidextrous grasping); GG-CNN; GR-ConvNet; 6-DoF GraspNet; Contact-GraspNet; GraspNet-1Billion; AnyGrasp; Grasp-Anything; Grasp-Anything++ / LGD; Grasp-Anything-6D; GraspGPT; ThinkGrasp; RT-Grasp; VCoT-Grasp; GraspVLA; DexGraspNet; Dex1B
- **Tier 2 (25 new):** Real-time grasp detection (Redmon & Angelova); Jacquard; ACRONYM; VGN; EquiGraspFlow; OrbitGrasp; GraspNeRF; LERF-TOGO; GaussianGrasper; GraspSplats; OWG (open-world grasping); VL-Grasp; Reasoning Grasping; AffordGrasp; GraspMolmo; DexDiffuser; Grasp as You Say; D(R,O) Grasp; GenDexGrasp; Dexterous Grasp Transformer; DexGraspVLA; RealVLG-11B; MonoGraspNet; Implicit Grasp Diffusion; GraspClutter6D

### E2 · Dexterous and in-hand manipulation
*Surveys that cite them:* P01 §4.3, Table 7; P07; P10; P06; P05.

- **Tier 1 (7 new):** DAPG (Rajeswaran); PDDM; Learning dexterous in-hand manipulation (Dactyl); DeXtreme; Visual Dexterity; In-hand object rotation (Qi et al.); DexCap (→D1); HATO
- **Tier 2 (15 new):** ViViDex; DexHandDiff; CordViP; REBOOT; Robotic Telekinesis; DexMV; Bunny-VisionPro; DexForce; ViTacFormer; HACMan; DexWild; EgoDex; TriFinger; DexJoCo; DexVerse

### E3 · Deformable, bimanual, mobile and soft manipulation
*Surveys that cite them:* P01 §4.4–4.7, Table 7; P07; P02; P05.

- **Tier 1 (6 new):** ALOHA Unleashed (→B2); DeformerNet; DexDeform; Deep Whole-Body Control (Fu); HOMER; MoManipVLA; RoboTwin 2.0 (→D1); χ0
- **Tier 2 (30 new):** Jan et al. deformable RL; DMfD; DefGoalNet; MPD; DeformGS; Foresightful Affordance; APS-Net; GenDOM; DeformNet; DoughNet; MoMa; MOMA-Force; Skill Transformer; TidyBot++; Waste sorting RL (Herzog); M-EMBER; DribbleBot; VBC; GAMMA; Human2LocoMan; WildLMa; QUAR-VLA; GeRM; Soft DAgger; KineSoft; SS-ILKC; BiGym; SoftGym; DaXBench; ODYSSEY

### E4 · Humanoid whole-body manipulation
*Surveys that cite them:* P09, P01 §4.8.

- **Tier 1 (6 new):** H2O / OmniH2O; HumanPlus; ExBody2; Open-TeleVision (→D1); OKAMI (→D2); WoCoCo; Real-world humanoid locomotion (Radosavovic); FLAM
- **Tier 2 (15 new):** ExBody; Mobile-TeleVision; DiffuseLoco; AMP; PhysHOI; SFV; Agile soccer (Haarnoja); CooHOI; HumanVLA; Humanoid-VLA; HumanoidBench; SIMPLE; HumanoidArena; OASIS; GRAIL

### E5 · Touch and force
*Surveys that cite them:* P10 (53 core papers), P01 §6.2.3. P10 tabulates all 53; every one gets at least a fact card.

- **Tier 1 (12 new):** Reactive Diffusion Policy (RDP); ForceVLA; FoAR; Adaptive Compliance Policy (ACP); 3D-ViTac; UniT; FuSe; Tactile-VLA; TacDiffusion; M3L; ViTaL; TA-VLA
- **Tier 2 (31 new):** FCLM; UPPFC; FORGE; AdmitDiff; DexForce (→E2); ForceMimic; DIPCOM / Comp-ACT; FARM; TLA; FILIC; ManipForce; TACT; TaF-VLA; Force Policy; FACTR; ForceSight; CRAFT; EquiContact; MoDE-VLA; ForceVLA2; ReTac-ACT; TacVLA; KineDex; OmniVTA; OmniVTLA; ViTaS; VLA-Touch; 3DTacDex; VTAO-BiManip; VTLA; ARCH; TouchGuide

### E6 · Physics priors
*Surveys that cite them:* P11.

- **Tier 1 (10 new):** DeLaN; Hamiltonian Neural Networks; Lagrangian Neural Networks; Neural ODE; Variational Integrator Networks; PINN (Raissi); SINDy; Port-Hamiltonian on SE(3) (Duong & Atanasov); Neural SDE (Djeumou); PI-TCN
- **Tier 2 (16 new):** Context-aware DeLaN; FeLaN; Controlled HNN; Forced VIN; Lagrangian-SINDy; EQLN; Neural time fields; Coupled oscillator networks (CONs); MixNet; Morphological symmetry (Ordoñez-Apraez); GP-MPC racing (Kabzan); PhysDiff; Riemannian flow matching; Reachable-set projection diffusion; Hamiltonian video world model; Deep Koopman with physics lifting

### F1 · Verifiers and failure detection
*Surveys that cite them:* P14, P01 §7, X3 §V-E.

- **Tier 1 (12 new):** KnowNo; RoboMonkey; V-GPS; SAFE; FAIL-Detect; FIPER; Sentinel; GVL; RECAP (π*0.6); RoboArena; AutoEval; World Action Verifier
- **Tier 2 (36 new):** Deep RL from human preferences (Christiano); PEBBLE; ConformalSTL (Lindemann); TGPO; RINSE; Code-as-Monitor; Robometer; VLAC; Robo-Dopamine; VLM-RM; RoboCLIP; TOPReward; SuccessVQA; REFLECT; AHA; RoboFAC; RoVer; AHEAD; FOREWARN; Foresight; GRAPE; Demo-SCORE; SCIZOR; Tri-Info; HideAndSeek; MG-Select; TACO; VIPER; Diffusion Reward; MOPO; MOReL; Ward et al. (world-model uncertainty); Latent reachability (Nakamura); PNCBF; RoboReward; OpenGVL

### F2 · Safety of embodied AI
*Surveys that cite them:* P13.

- **Tier 1 (12 new):** BadVLA; FlowHijack; SilentDrift; FreezeVLA; RoboPAIR; BADROBOT; POEX; BYOVLA; VLSA; SafeVLA; SafeDreamer; LIBERO-Plus
- **Tier 2 (25 new):** DP-Attacker; UADA / UPA / TMA; Tex3D; VLA-Fool; JailWAM; RedVLA; DropVLA; GoBA; BEAT; PolicyCleanse; RoboSafe; SafePlan; TRAP; PhysCond-WMA; CtrlAttack; HomeGuard; Surprise Recognition; AFM; STRONG-VLA; AgentPoison; ERT; CBA; Robo-Troj; J-DAPT; LIBERO-X

### F3 · Benchmarks and what they miss
*Surveys that cite them:* P03 §7, X3 §VII–VIII, P01 §3, X1 §6.

- **Tier 1 (9 new):** LIBERO; CALVIN; SIMPLER; RLBench; Meta-World; robomimic; ManiSkill3; RoboCasa (→D1); WorldSimBench; EWMBench
- **Tier 2 (19 new):** VIMA-Bench; COLOSSEUM; VLABench; GemBench; AGNOSTOS; GenManip; BEHAVIOR-1K; HomeRobot; Franka Kitchen; RoboVerse; TacSL; ManiFeel; WorldArena; WoW-World-Eval; RoboWM-Bench; Dream.exe; RoboChallenge; PolaRiS; RoboMME
