---
title: "Focus-Direction Paper-Code Index"
aliases:
  - "Focus-Direction Paper-Code Index"
  - "Paper-Code Index"
tags:
  - embodied-AI
  - index
---
# Focus-Direction Paper-Code Index: Papers ↔ Code Repositories

> [!abstract] What this is
> One row per paper: it links each of the **581 papers** across [[Focus-Direction]]'s 18 core directions (Whole-Body A+B, WAM·A, Sim2Real·B, Embodied-AI·B) plus Whole-Body Cluster C (Force-Adaptive Coordination Under Load), 20 directions across the 6 clusters in all, to its KnowledgeHub note, local PDF, and official code repo. **352** papers have a confirmed official repo; **347** of those are cloned-and-catalogued in `data/.repositories/` (the live folder now holds **358** directories in all, the extra being later or uncatalogued clones; the in-program figure of 358 is that live folder count). The other **229** released no public code (of which 11 are the newest additions whose code is not yet released).
>
> **Indexing:** all **567** papers are indexed in a graphify concept graph at `data/papers/graphify-out/` (1,918 nodes, cross-paper semantic + citation links, community clusters); **343** of the **347** cloned repos are indexed in GitNexus code-graphs (`.gitnexus/`, queryable via the gitnexus MCP for call-graphs / impact analysis / symbol context) — the 4 exceptions are in Known gaps.
>
> Repos were resolved per-paper (full-PDF read → web search `<title> github` → alphaxiv `read_files_from_github_repository` confirm) and read-verified as the paper's own release; dependency, baseline, third-party-reimplementation, and different-paper repos were rejected. A few authors' official repos that are still empty ("code coming soon") are kept. KnowledgeHub notes carry no code links.

> [!info] Columns
> **Cluster(s)** = which source clusters cite the paper · **KH** = KnowledgeHub note · **PDF** = local file in `data/papers/` · **Repo** = official GitHub (clickable) · **Cloned** = ✓ in `data/.repositories/` · ✗ repo found but clone failed · — no public code · **Size** = on-disk size of the full clone (complete history; Git-LFS blobs skipped) · **Indexed** = ✓ has a gitnexus code-graph index (`.gitnexus/`, queryable via the gitnexus MCP) · ✗ cloned but not indexed · **Remarks** = repo-completeness note from studying the paper + repo (blank = complete; e.g. README-only, partial, survey-list, website, data-only).

**Totals** — papers 581 · with repo 352 · cloned 347 · clone-failed 2 · no public code 229 · cloned size 154.6 GB · gitnexus-indexed 343. The 14 newest (rows 568-581, added 2026-07-12) are cataloged but not yet cloned or graph-indexed: 11 have no released code yet, and 3 have identified repos (MuSe, IMPACT, FAWAM) not yet cloned.

**Repo completeness** (studied paper + repo across 347 cloned) — complete **242** · partial **41** · README-only/placeholder **33** · survey-list **15** · project-website-only **12** · benchmark-data-only **4**. Non-complete repos are flagged in the **Remarks** column.

| # | Cluster(s) | KH | PDF | Repo | Cloned | Size | Indexed | Remarks |
|---:|---|---|---|---|:--:|--:|:--:|---|
| 1 | WB·A WB·B | [[2401.02117\|Mobile-ALOHA]] | [[2401.02117v1.pdf]] | [`MarkFzp/mobile-aloha`](https://github.com/MarkFzp/mobile-aloha) | ✓ | 28 MB | ✓ | Teleop/data-collection only; training (ACT) lives in separate repo |
| 2 | WB·A WB·C | [[2403.10506\|HumanoidBench]] | [[2403.10506v2.pdf]] | [`carlosferrazza/humanoid-bench`](https://github.com/carlosferrazza/humanoid-bench) | ✓ | 464 MB | ✓ |  |
| 3 | WB·A | [[2403.17367\|RoboDuet]] | [[2403.17367v5.pdf]] | [`locomanip-duet/RoboDuet`](https://github.com/locomanip-duet/RoboDuet) | ✓ | 331 MB | ✓ |  |
| 4 | WB·A | [[2405.18418\|Puppeteer]] | [[2405.18418v3.pdf]] | [`nicklashansen/puppeteer`](https://github.com/nicklashansen/puppeteer) | ✓ | 28 MB | ✓ |  |
| 5 | WB·A | [[2407.10353\|UMI-on-Legs]] | [[2407.10353v1.pdf]] | [`real-stanford/umi-on-legs`](https://github.com/real-stanford/umi-on-legs) | ✓ | 212 MB | ✓ |  |
| 6 | WB·A | [[2408.00342\|MuJoCo-MPC-HumanoidBench]] | [[2408.00342v1.pdf]] | [`google-deepmind/mujoco_mpc`](https://github.com/google-deepmind/mujoco_mpc) | ✓ | 106 MB | ✓ |  |
| 7 | WB·A | [[2409.16048\|WB-EE-Pose-Tracking]] | [[2409.16048v2.pdf]] | — *(no public code)* | — | — | — |  |
| 8 | WB·A | [[2410.21229\|HOVER]] | [[2410.21229v2.pdf]] | [`NVlabs/HOVER`](https://github.com/NVlabs/HOVER) | ✓ | 261 MB | ✓ |  |
| 9 | WB·A | [[2411.06782\|QuadWBG]] | [[2411.06782v2.pdf]] | — *(no public code)* | — | — | — |  |
| 10 | WB·A | [[2412.03012\|Omni-WBLM]] | [[2412.03012v2.pdf]] | — *(no public code)* | — | — | — |  |
| 11 | WB·A | [[2412.07773\|Mobile-TeleVision]] | [[2412.07773v2.pdf]] | [`OpenTeleVision/TeleVision`](https://github.com/OpenTeleVision/TeleVision) | ✓ | 117 MB | ✓ |  |
| 12 | WB·A | [[2502.03206\|Unified-General-Humanoid-Whole-Body]] | [[2502.03206v3.pdf]] | [`apexrl/HugWBC`](https://github.com/apexrl/HugWBC) | ✓ | 75 MB | ✓ |  |
| 13 | WB·A | [[2502.14795\|Humanoid-VLA]] | [[2502.14795v2.pdf]] | — *(no public code)* | — | — | — |  |
| 14 | WB·A WB·B | [[2503.05652\|BRS]] | [[2503.05652v2.pdf]] | [`behavior-robot-suite/brs-algo`](https://github.com/behavior-robot-suite/brs-algo) | ✓ | 139 MB | ✓ |  |
| 15 | WB·A | [[2503.08564\|MoE-Loco]] | [[2503.08564v2.pdf]] | [`hrh6666/MoE-Loco`](https://github.com/hrh6666/MoE-Loco) | ✓ | 15 MB | ✓ | README only (title/citation) — no code released, 4 files total |
| 16 | WB·A | [[2504.06662\|RAMBO]] | [[2504.06662v4.pdf]] | [`catachiii/rambo`](https://github.com/catachiii/rambo) | ✓ | 188 MB | ✓ |  |
| 17 | WB·A | [[2504.11054\|Meta-Motivo]] | [[2504.11054v1.pdf]] | [`facebookresearch/metamotivo`](https://github.com/facebookresearch/metamotivo) | ✓ | 26 MB | ✓ |  |
| 18 | WB·A WB·B | [[2504.16054\|π0.5]] | [[2504.16054v1.pdf]] | [`Physical-Intelligence/openpi`](https://github.com/Physical-Intelligence/openpi) | ✓ | 858 MB | ✓ |  |
| 19 | WB·A WB·C | [[2505.06776\|FALCON-Loco-Manipulation]] | [[2505.06776v2.pdf]] | [`LeCAR-Lab/FALCON`](https://github.com/LeCAR-Lab/FALCON) | ✓ | 363 MB | ✓ |  |
| 20 | WB·A | [[2505.10918\|Unleashing-Humanoid-Reaching-Potential]] | [[2505.10918v2.pdf]] | [`GalaxyGeneralRobotics/OpenWBT`](https://github.com/GalaxyGeneralRobotics/OpenWBT) | ✓ | 455 MB | ✓ |  |
| 21 | WB·A | [[2505.24198\|Hold-My-Beer]] | [[2505.24198v2.pdf]] | [`LeCAR-Lab/SoFTA`](https://github.com/LeCAR-Lab/SoFTA) | ✓ | 253 MB | ✓ | deploy code not yet released |
| 22 | WB·A | [[2506.09366\|SkillBlender]] | [[2506.09366v1.pdf]] | [`Humanoid-SkillBlender/SkillBlender`](https://github.com/Humanoid-SkillBlender/SkillBlender) | ✓ | 274 MB | ✓ | only H1 ckpts; G1/H1-2 ckpts and sim2real not released |
| 23 | WB·A | [[2506.12779\|Experts-to-Generalist]] | [[2506.12779v3.pdf]] | [`BeingBeyond/BumbleBee`](https://github.com/BeingBeyond/BumbleBee) | ✓ | 381 MB | ✓ | README only — code not yet released |
| 24 | WB·A | [[2506.12851\|KungfuBot]] | [[2506.12851v2.pdf]] | [`TeleHuman/PBHC`](https://github.com/TeleHuman/PBHC) | ✓ | 257 MB | ✓ |  |
| 25 | WB·A | [[2506.13751\|LeVERB]] | [[2506.13751v3.pdf]] | — *(no public code)* | — | — | — |  |
| 26 | WB·A | [[2506.14278\|Heavy-Limbs-WBC]] | [[2506.14278v2.pdf]] | — *(no public code)* | — | — | — |  |
| 27 | WB·A | [[2507.04140\|Centroidal-Arm-Motion]] | [[2507.04140v1.pdf]] | [`hojae-io/LearningHumanoidArmMotion-RAL2025-Code`](https://github.com/hojae-io/LearningHumanoidArmMotion-RAL2025-Code) | ✓ | 347 MB | ✓ |  |
| 28 | WB·A | [[2507.06905\|ULC]] | [[2507.06905v2.pdf]] | [`Hellod035/ULC`](https://github.com/Hellod035/ULC) | ✓ | 272 MB | ✓ | README only — code not yet released |
| 29 | WB·A | [[2507.08656\|Multi-Critic-Twist-Tracking]] | [[2507.08656v2.pdf]] | [`multi-critic-locomanipulation/multi-critic-locomanipulation.github.io`](https://github.com/multi-critic-locomanipulation/multi-critic-locomanipulation.github.io) | ✓ | 684 MB | ✓ | Project website only, no code |
| 30 | WB·A | [[2508.00355\|TOP]] | [[2508.00355v1.pdf]] | — *(no public code)* | — | — | — |  |
| 31 | WB·A | [[2508.10538\|MLM]] | [[2508.10538v2.pdf]] | — *(no public code)* | — | — | — |  |
| 32 | WB·A | [[2508.11275\|Differentiable-Reachability-Maps-Optimization-based]] | [[2508.11275v1.pdf]] | — *(no public code)* | — | — | — |  |
| 33 | WB·A | [[2508.16943\|LHM-Humanoid]] | [[2508.16943v2.pdf]] | — *(no public code)* | — | — | — |  |
| 34 | WB·A | [[2509.13780\|Behavior-Foundation-Model-Humanoid]] | [[2509.13780v1.pdf]] | — *(no public code)* | — | — | — |  |
| 35 | WB·A | [[2509.21231\|SEEC]] | [[2509.21231v1.pdf]] | — *(no public code)* | — | — | — |  |
| 36 | WB·A | [[2509.22442\|Ball-Composing-Policies-Long-Horizon]] | [[2509.22442v1.pdf]] | [`xupei0610/basketball`](https://github.com/xupei0610/basketball) | ✓ | 284 MB | ✓ |  |
| 37 | WB·A | [[2509.26633\|OmniRetarget]] | [[2509.26633v3.pdf]] | [`amazon-far/holosoma`](https://github.com/amazon-far/holosoma) | ✓ | 611 MB | ✓ |  |
| 38 | WB·A | [[2510.05070\|ResMimic]] | [[2510.05070v2.pdf]] | [`amazon-far/ResMimic`](https://github.com/amazon-far/ResMimic) | ✓ | 152 MB | ✓ |  |
| 39 | WB·A | [[2511.05936\|10-VLA-Challenges]] | [[2511.05936v1.pdf]] | — *(no public code)* | — | — | — |  |
| 40 | WB·A | [[2511.06371\|Adaptive-Humanoid-Control-Multi-Behavior]] | [[2511.06371v3.pdf]] | — *(no public code)* | — | — | — |  |
| 41 | WB·A | [[2511.15200\|VIRAL]] | [[2511.15200v2.pdf]] | [`NVlabs/GR00T-VisualSim2Real`](https://github.com/NVlabs/GR00T-VisualSim2Real) | ✓ | 75 MB | ✓ |  |
| 42 | WB·A | [[2511.21169\|Kinematics-Aware-Multi-Policy]] | [[2511.21169v1.pdf]] | — *(no public code)* | — | — | — |  |
| 43 | WB·A | [[2512.04381\|FALCON-LocoMan]] | [[2512.04381v1.pdf]] | — *(no public code)* | — | — | — |  |
| 44 | WB·A | [[2512.11047\|WholeBodyVLA]] | [[2512.11047v2.pdf]] | [`opendrivelab/WholeBodyVLA`](https://github.com/opendrivelab/WholeBodyVLA) | ✓ | 78 MB | ✓ | No open-source timeline; repo is a curated reference list only |
| 45 | WB·A | [[2512.13093\|PvP]] | [[2512.13093v2.pdf]] | [`myismyname/SRL4Humanoid`](https://github.com/myismyname/SRL4Humanoid) | ✓ | 66 MB | ✓ |  |
| 46 | WB·A EAI·B | [[2512.20188\|Fast-Slow-WB-VLA]] | [[2512.20188v1.pdf]] | — *(no public code)* | — | — | — |  |
| 47 | WB·A | [[2601.17440\|PILOT]] | [[2601.17440v1.pdf]] | — *(no public code)* | — | — | — |  |
| 48 | WB·A | [[2602.04515\|EgoActor]] | [[2602.04515v1.pdf]] | — *(no public code)* | — | — | — |  |
| 49 | WB·A WB·C | [[2602.06341\|HiWET]] | [[2602.06341v1.pdf]] | — *(no public code)* | — | — | — |  |
| 50 | WB·A | [[2602.08594\|MOSAIC]] | [[2602.08594v2.pdf]] | [`BAAI-Humanoid/MOSAIC`](https://github.com/BAAI-Humanoid/MOSAIC) | ✓ | 1.3 GB | ✓ |  |
| 51 | WB·A | [[2602.10106\|EgoHumanoid]] | [[2602.10106v2.pdf]] | [`OpenDriveLab/EgoHumanoid`](https://github.com/OpenDriveLab/EgoHumanoid) | ✓ | 72 MB | ✓ |  |
| 52 | WB·A | [[2602.11758\|HAIC]] | [[2602.11758v2.pdf]] | [`ldt29/HAIC`](https://github.com/ldt29/HAIC) | ✓ | 82 MB | ✓ |  |
| 53 | WB·A | [[2602.13850\|Humanoid-Hanoi]] | [[2602.13850v3.pdf]] | [`osudrl/Humanoid_Hanoi`](https://github.com/osudrl/Humanoid_Hanoi) | ✓ | 591 MB | ✓ | Environment only; training code not included |
| 54 | WB·A | [[2602.15060\|CLOT]] | [[2602.15060v2.pdf]] | [`zhutengjie/CLOT`](https://github.com/zhutengjie/CLOT) | ✓ | 2.4 GB | ✓ |  |
| 55 | WB·A | [[2602.16705\|HERO-Humanoid-EE-Control]] | [[2602.16705v3.pdf]] | — *(no public code)* | — | — | — |  |
| 56 | WB·A WB·C | [[2603.02443\|Safe-WBLM]] | [[2603.02443v1.pdf]] | — *(no public code)* | — | — | — |  |
| 57 | WB·A WB·C | [[2603.03279\|ULTRA]] | [[2603.03279v1.pdf]] | — *(no public code)* | — | — | — |  |
| 58 | WB·A | [[2603.05410\|PhysiFlow]] | [[2603.05410v1.pdf]] | — *(no public code)* | — | — | — |  |
| 59 | WB·A | [[2603.08572\|MetaWorld-X]] | [[2603.08572v1.pdf]] | — *(no public code)* | — | — | — |  |
| 60 | WB·A WB·C | [[2603.08961\|FAME]] | [[2603.08961v1.pdf]] | [`correlllab/h12_adaptive_policy`](https://github.com/correlllab/h12_adaptive_policy) | ✓ | 609 MB | ✓ |  |
| 61 | WB·A | [[2603.10306\|SteadyTray]] | [[2603.10306v1.pdf]] | [`AllenHuangGit/SteadyTray`](https://github.com/AllenHuangGit/SteadyTray) | ✓ | 90 MB | ✓ |  |
| 62 | WB·A | [[2603.10675\|Cybo-Waiter]] | [[2603.10675v1.pdf]] | — *(no public code)* | — | — | — |  |
| 63 | WB·A | [[2603.12263\|Psi0]] | [[2603.12263v1.pdf]] | [`physical-superintelligence-lab/Psi0`](https://github.com/physical-superintelligence-lab/Psi0) | ✓ | 1.7 GB | ✓ |  |
| 64 | WB·A | [[2603.13707\|REFINE-DP]] | [[2603.13707v2.pdf]] | — *(no public code)* | — | — | — |  |
| 65 | WB·A | [[2603.20147\|AGILE]] | [[2603.20147v1.pdf]] | [`nvidia-isaac/WBC-AGILE`](https://github.com/nvidia-isaac/WBC-AGILE) | ✓ | 84 MB | ✓ |  |
| 66 | WB·A | [[2604.00202\|DreamControl-v2]] | [[2604.00202v1.pdf]] | — *(no public code)* | — | — | — |  |
| 67 | WB·A | [[2604.01158\|SMASH]] | [[2604.01158v1.pdf]] | — *(no public code)* | — | — | — |  |
| 68 | WB·A WB·C | [[2604.07457\|CMP]] | [[2604.07457v1.pdf]] | [`Shepherd1226/CMP`](https://github.com/Shepherd1226/CMP) | ✓ | 3.2 MB | ✓ | README only — code coming soon |
| 69 | WB·A WB·C | [[2604.07993\|HEX]] | [[2604.07993v2.pdf]] | [`Open-X-Humanoid/HEX`](https://github.com/Open-X-Humanoid/HEX) | ✓ | 73 MB | ✓ | Data collection pipeline not released (commercial restrictions) |
| 70 | WB·A | [[2604.11251\|CLAW]] | [[2604.11251v3.pdf]] | [`JianuoCao/CLAW`](https://github.com/JianuoCao/CLAW) | ✓ | 334 MB | ✓ |  |
| 71 | WB·A | [[2604.24833\|MotionBricks]] | [[2604.24833v1.pdf]] | [`NVlabs/GR00T-WholeBodyControl`](https://github.com/NVlabs/GR00T-WholeBodyControl) | ✓ | 1.2 GB | ✓ |  |
| 72 | WB·A | [[2605.14417\|DAJI]] | [[2605.14417v2.pdf]] | [`Hxxxz0/DAJI`](https://github.com/Hxxxz0/DAJI) | ✓ | 3.2 MB | ✓ | README only — code not yet released |
| 73 | WB·A WB·B | [[2605.21133\|Spatial-Brain-Cerebellum]] | [[2605.21133v1.pdf]] | — *(no public code)* | — | — | — |  |
| 74 | WB·A | [[2605.23733\|Any2Any]] | [[2605.23733v3.pdf]] | — *(no public code)* | — | — | — |  |
| 75 | WB·A | [[2605.27724\|HumanoidMimicGen]] | [[2605.27724v1.pdf]] | — *(no public code)* | — | — | — |  |
| 76 | WB·A | [[2606.03536\|Bionic-Whole-Body-Control]] | [[2606.03536v1.pdf]] | — *(no public code)* | — | — | — |  |
| 77 | WB·A | [[2606.05160\|GRAIL]] | [[2606.05160v1.pdf]] | [`NVlabs/GRAIL`](https://github.com/NVlabs/GRAIL) | ✓ | 3.2 GB | ✓ |  |
| 78 | WB·A | [[2606.06139\|MotionDisco]] | [[2606.06139v1.pdf]] | — *(no public code)* | — | — | — |  |
| 79 | WB·A | [[2606.06493\|HANDOFF]] | [[2606.06493v3.pdf]] | [`lzyang2000/HANDOFF`](https://github.com/lzyang2000/HANDOFF) | ✓ | 323 MB | ✓ |  |
| 80 | WB·A | [[2606.09215\|MotionWAM]] | [[2606.09215v1.pdf]] | — *(no public code)* | — | — | — |  |
| 81 | WB·A | [[2606.10340\|OMG]] | [[2606.10340v1.pdf]] | [`Tsinghua-MARS-Lab/OMG`](https://github.com/Tsinghua-MARS-Lab/OMG) | ✓ | 106 MB | ✓ | OMG-Data, pretrained checkpoints, evaluator checkpoints pending |
| 82 | WB·A | [[2606.16696\|VENOM]] | [[2606.16696v1.pdf]] | — *(no public code)* | — | — | — |  |
| 83 | WB·A | [[2606.17833\|HumanoidArena]] | [[2606.17833v1.pdf]] | — *(no public code)* | — | — | — |  |
| 84 | WB·A WB·B | [[2606.18772\|HALOMI]] | [[2606.18772v1.pdf]] | — *(no public code)* | — | — | — |  |
| 85 | WB·B | [[2305.04866\|Causal-WBMM]] | [[2305.04866v4.pdf]] | [`JiahengHu/CausalMoMa`](https://github.com/JiahengHu/CausalMoMa) | ✓ | 230 MB | ✓ |  |
| 86 | WB·B | [[2306.11565\|HomeRobot]] | [[2306.11565v2.pdf]] | [`facebookresearch/home-robot`](https://github.com/facebookresearch/home-robot) | ✓ | 1.2 GB | ✓ |  |
| 87 | WB·B | [[2310.00433\|ActPerMoMa]] | [[2310.00433v2.pdf]] | [`pearl-robot-lab/ActPerMoMa`](https://github.com/pearl-robot-lab/ActPerMoMa) | ✓ | 146 MB | ✓ |  |
| 88 | WB·B | [[2405.07991\|SPIN-Mobile-Manip]] | [[2405.07991v1.pdf]] | — *(no public code)* | — | — | — |  |
| 89 | WB·B | [[2407.07788\|BiGym]] | [[2407.07788v2.pdf]] | [`chernyadev/bigym`](https://github.com/chernyadev/bigym) | ✓ | 275 MB | ✓ |  |
| 90 | WB·B | [[2410.06237\|BUMBLE]] | [[2410.06237v1.pdf]] | [`UT-Austin-RobIn/BUMBLE`](https://github.com/UT-Austin-RobIn/BUMBLE) | ✓ | 253 MB | ✓ |  |
| 91 | WB·B | [[2410.11989\|DovSG]] | [[2410.11989v6.pdf]] | [`BJHYZJ/DovSG`](https://github.com/BJHYZJ/DovSG) | ✓ | 501 MB | ✓ |  |
| 92 | WB·B | [[2410.18964\|DISaM]] | [[2410.18964v1.pdf]] | [`UT-Austin-RobIn/l2l`](https://github.com/UT-Austin-RobIn/l2l) | ✓ | 66 MB | ✓ |  |
| 93 | WB·B | [[2411.04999\|DynaMem]] | [[2411.04999v2.pdf]] | [`hello-robot/stretch_ai`](https://github.com/hello-robot/stretch_ai) | ✓ | 397 MB | ✓ |  |
| 94 | WB·B | [[2412.13211\|MS-HAB]] | [[2412.13211v3.pdf]] | [`arth-shukla/mshab`](https://github.com/arth-shukla/mshab) | ✓ | 220 MB | ✓ |  |
| 95 | WB·B | [[2501.04595\|MobileH2R]] | [[2501.04595v2.pdf]] | — *(no public code)* | — | — | — |  |
| 96 | WB·B | [[2503.01439\|AVR]] | [[2503.01439v4.pdf]] | — *(no public code)* | — | — | — |  |
| 97 | WB·B | [[2503.12609\|VISO-Grasp]] | [[2503.12609v2.pdf]] | [`YitianShi/vMF-Contact`](https://github.com/YitianShi/vMF-Contact) | ✓ | 91 MB | ✗ |  |
| 98 | WB·B | [[2503.13446\|MoManipVLA]] | [[2503.13446v1.pdf]] | — *(no public code)* | — | — | — |  |
| 99 | WB·B | [[2505.06182\|APPLE-Active-Perception]] | [[2505.06182v6.pdf]] | [`TimSchneider42/apple`](https://github.com/TimSchneider42/apple) | ✓ | 85 MB | ✓ |  |
| 100 | WB·B | [[2505.12278\|Emergent-Active-Perception-Dexterity]] | [[2505.12278v1.pdf]] | — *(no public code)* | — | — | — |  |
| 101 | WB·B | [[2505.23692\|Mobi-Pi]] | [[2505.23692v2.pdf]] | [`yjy0625/mobipi`](https://github.com/yjy0625/mobipi) | ✓ | 227 MB | ✓ |  |
| 102 | WB·B | [[2506.01185\|HoMeR]] | [[2506.01185v2.pdf]] | [`priyasundaresan/homer`](https://github.com/priyasundaresan/homer) | ✓ | 372 MB | ✓ |  |
| 103 | WB·B | [[2506.10968\|EyeRobot]] | [[2506.10968v2.pdf]] | [`kerrj/eyerobot`](https://github.com/kerrj/eyerobot) | ✓ | 1.0 GB | ✓ |  |
| 104 | WB·B | [[2506.15666\|Vision-in-Action]] | [[2506.15666v1.pdf]] | [`haoyu-x/vision-in-action`](https://github.com/haoyu-x/vision-in-action) | ✓ | 745 MB | ✓ |  |
| 105 | WB·B | [[2507.01961\|AC-DiT]] | [[2507.01961v3.pdf]] | [`PKU-HMI-Lab/AC-DiT`](https://github.com/PKU-HMI-Lab/AC-DiT) | ✓ | 636 MB | ✓ |  |
| 106 | WB·B | [[2507.15833\|Look,-Focus,-Act]] | [[2507.15833v2.pdf]] | [`ian-chuang/gaze-av-aloha`](https://github.com/ian-chuang/gaze-av-aloha) | ✓ | 139 MB | ✓ |  |
| 107 | WB·B | [[2508.05186\|TVVE]] | [[2508.05186v5.pdf]] | [`HCPLab-SYSU/TAVP`](https://github.com/HCPLab-SYSU/TAVP) | ✓ | 522 MB | ✓ |  |
| 108 | WB·B EAI·B | [[2508.19236\|MemoryVLA]] | [[2508.19236v2.pdf]] | [`shihao1895/MemoryVLA`](https://github.com/shihao1895/MemoryVLA) | ✓ | 208 MB | ✓ |  |
| 109 | WB·B | [[2509.16063\|DSPv2]] | [[2509.16063v2.pdf]] | [`Selen-Suyue/DSPv2`](https://github.com/Selen-Suyue/DSPv2) | ✓ | 89 MB | ✓ |  |
| 110 | WB·B | [[2509.20297\|mindmap]] | [[2509.20297v3.pdf]] | [`nvidia-isaac/nvblox_mindmap`](https://github.com/nvidia-isaac/nvblox_mindmap) | ✓ | 221 MB | ✓ |  |
| 111 | WB·B | [[2510.01607\|ActiveUMI]] | [[2510.01607v1.pdf]] | — *(no public code)* | — | — | — |  |
| 112 | WB·B | [[2510.03885\|3D-Latent-Mapping]] | [[2510.03885v3.pdf]] | [`ExistentialRobotics/SBP`](https://github.com/ExistentialRobotics/SBP) | ✓ | 408 MB | ✓ |  |
| 113 | WB·B | [[2510.07134\|TrackVLA++]] | [[2510.07134v1.pdf]] | — *(no public code)* | — | — | — |  |
| 114 | WB·B | [[2510.20328\|MemER]] | [[2510.20328v1.pdf]] | [`memer-policy/memer`](https://github.com/memer-policy/memer) | ✓ | 22 MB | ✓ | High-level data-prep/eval only; training deferred to external Qwen3-VL recipe |
| 115 | WB·B | [[2511.00153\|EgoMI]] | [[2511.00153v2.pdf]] | — *(no public code)* | — | — | — |  |
| 116 | WB·B | [[2511.11478\|LIBERO-Mem]] | [[2511.11478v3.pdf]] | [`libero-mem/libero-mem`](https://github.com/libero-mem/libero-mem) | ✓ | 1.7 GB | ✓ |  |
| 117 | WB·B | [[2511.18112\|EchoVLA]] | [[2511.18112v2.pdf]] | [`EchoVLA-project/EchoVLA_web`](https://github.com/EchoVLA-project/EchoVLA_web) | ✓ | 17 MB | ✓ | Project website only, no code |
| 118 | WB·B | [[2512.24653\|RoboMIND-2.0]] | [[2512.24653v3.pdf]] | [`Open-X-Humanoid/RoboMIND-Sim`](https://github.com/Open-X-Humanoid/RoboMIND-Sim) | ✓ | 120 MB | ✓ | Benchmark sim env only; model inference must be implemented by user |
| 119 | WB·B | [[2601.08325\|ActiveVLA]] | [[2601.08325v1.pdf]] | [`ZhenyangLiu/ActiveVLA-Injecting-Active-Perception-into-VLA`](https://github.com/ZhenyangLiu/ActiveVLA-Injecting-Active-Perception-into-VLA) | ✓ | 8.1 MB | ✓ | README only - code/models/eval not yet released |
| 120 | WB·B | [[2602.01939\|EFM-10]] | [[2602.01939v3.pdf]] | [`EFManipulation/EFManipulation.github.io`](https://github.com/EFManipulation/EFManipulation.github.io) | ✓ | 74 MB | ✓ | Project website only, no code |
| 121 | WB·B | [[2602.04600\|Act-Sense-Act]] | [[2602.04600v1.pdf]] | — *(no public code)* | — | — | — |  |
| 122 | WB·B | [[2602.05233\|MobileManiBench]] | [[2602.05233v1.pdf]] | — *(no public code)* | — | — | — |  |
| 123 | WB·B | [[2602.22461\|EgoAVFlow]] | [[2602.22461v1.pdf]] | — *(no public code)* | — | — | — |  |
| 124 | WB·B | [[2602.23024\|InCoM]] | [[2602.23024v4.pdf]] | — *(no public code)* | — | — | — |  |
| 125 | WB·B | [[2603.01229\|RMBench]] | [[2603.01229v2.pdf]] | [`RoboTwin-Platform/RMBench`](https://github.com/RoboTwin-Platform/RMBench) | ✓ | 148 MB | ✓ |  |
| 126 | WB·B | [[2603.03243\|HoMMI]] | [[2603.03243v2.pdf]] | [`xxm19/hommi`](https://github.com/xxm19/hommi) | ✓ | 246 MB | ✓ |  |
| 127 | WB·B EAI·B | [[2603.04639\|RoboMME]] | [[2603.04639v3.pdf]] | [`RoboMME/robomme_policy_learning`](https://github.com/RoboMME/robomme_policy_learning) | ✓ | 77 MB | ✓ |  |
| 128 | WB·B | [[2603.12193\|SaPaVe]] | [[2603.12193v1.pdf]] | — *(no public code)* | — | — | — |  |
| 129 | WB·B | [[2603.18494\|MemoAct]] | [[2603.18494v1.pdf]] | — *(no public code)* | — | — | — |  |
| 130 | WB·B | [[2603.22760\|SG-VLA]] | [[2603.22760v1.pdf]] | — *(no public code)* | — | — | — |  |
| 131 | WB·B | [[2604.08534\|ActiveGlasses]] | [[2604.08534v1.pdf]] | — *(no public code)* | — | — | — |  |
| 132 | WB·B | [[2605.02487\|Visibility-Aware-Mobile-Grasping]] | [[2605.02487v3.pdf]] | [`AdaCompNUS/Visibility-Awared-Mobile-Grasping`](https://github.com/AdaCompNUS/Visibility-Awared-Mobile-Grasping) | ✓ | 317 MB | ✓ |  |
| 133 | WB·B | [[2605.07943\|TAVIS]] | [[2605.07943v1.pdf]] | [`spiglerg/tavis`](https://github.com/spiglerg/tavis) | ✓ | 44 MB | ✓ |  |
| 134 | WB·B | [[2606.12956\|SERF]] | [[2606.12956v1.pdf]] | — *(no public code)* | — | — | — |  |
| 135 | WB·B EAI·B | [[2606.17463\|WeaveLA]] | [[2606.17463v1.pdf]] | — *(no public code)* | — | — | — |  |
| 136 | WB·C | [[2201.03871\|ALMA-Wrench-Prediction]] | [[2201.03871v1.pdf]] | — *(no public code)* | — | — | — | Project page only — no code repo |
| 137 | WB·C | [[2308.14636\|Linear-Impactor]] | [[2308.14636v2.pdf]] | — *(no public code)* | — | — | — | No public code repo |
| 138 | WB·C | [[2310.12567\|Safety-Gymnasium]] | [[2310.12567v3.pdf]] | [`PKU-Alignment/safety-gymnasium`](https://github.com/PKU-Alignment/safety-gymnasium) | ✓ | 1.3 GB | ✓ |  |
| 139 | WB·C | [[2404.19173\|Single-Contact++-RL]] | [[2404.19173v2.pdf]] | — *(no public code)* | — | — | — | Project page only — no code repo |
| 140 | WB·C | [[2502.02858\|p-SSA]] | [[2502.02858v1.pdf]] | [`intelligent-control-lab/spark`](https://github.com/intelligent-control-lab/spark) | ✓ | 488 MB | ✓ |  |
| 141 | WB·C | [[2502.03132\|SPARK]] | [[2502.03132v3.pdf]] | [`intelligent-control-lab/spark`](https://github.com/intelligent-control-lab/spark) | ✓ | 488 MB | ✓ |  |
| 142 | WB·C | [[2502.10894\|UAN]] | [[2502.10894v1.pdf]] | — *(no public code)* | — | — | — | Project page only — no code repo |
| 143 | WB·C | [[2503.00923\|HWC]] | [[2503.00923v3.pdf]] | — *(no public code)* | — | — | — | Project page only — no code repo |
| 144 | WB·C | [[2505.00779\|Uncertainty-Latent-Safety-Filter]] | [[2505.00779v2.pdf]] | [`CMU-IntentLab/UNISafe`](https://github.com/CMU-IntentLab/UNISafe) | ✓ | 130 MB | ✓ |  |
| 145 | WB·C | [[2505.11494\|SHIELD-Humanoid]] | [[2505.11494v3.pdf]] | — *(no public code)* | — | — | — | No public code repo |
| 146 | WB·C | [[2505.17627\|H2-COMPACT]] | [[2505.17627v1.pdf]] | [`bethalageetachandraraju/h2_compact`](https://github.com/bethalageetachandraraju/h2_compact) | ✓ | 53 MB | ✓ |  |
| 147 | WB·C | [[2505.20829\|Unified-Force-Position-Control]] | [[2505.20829v2.pdf]] | — *(no public code)* | — | — | — | Project page only — no code repo |
| 148 | WB·C | [[2506.11033\|Adaptive-Shielding]] | [[2506.11033v2.pdf]] | [`safe-autonomy-lab/AdaptiveShieldingFE`](https://github.com/safe-autonomy-lab/AdaptiveShieldingFE) | ✓ | 959 MB | ✓ |  |
| 149 | WB·C | [[2508.07611\|End-to-End]] | [[2508.07611v1.pdf]] | [`aCodeDog/SafeHumanoidsPolicy`](https://github.com/aCodeDog/SafeHumanoidsPolicy) | ✓ | 133 MB | ✓ | sim2sim eval + policy.jit only; no training code |
| 150 | WB·C | [[2508.11129\|Poisson-CBF-Humanoid]] | [[2508.11129v1.pdf]] | — *(no public code)* | — | — | — | No public code repo |
| 151 | WB·C | [[2510.14293\|Human-Humanoid-Coordination-Collaborative-Object]] | [[2510.14293v1.pdf]] | [`Yushi-Du/COLA_Code`](https://github.com/Yushi-Du/COLA_Code) | ✓ | 37 MB | ✓ | README only — code not yet released |
| 152 | WB·C | [[2510.14959\|CBF-RL]] | [[2510.14959v6.pdf]] | [`lzyang2000/cbf-rl-navigation-demo`](https://github.com/lzyang2000/cbf-rl-navigation-demo) | ✓ | 18 MB | ✓ |  |
| 153 | WB·C | [[2510.17792\|SoftMimic]] | [[2510.17792v1.pdf]] | [`Improbable-AI/softmimic`](https://github.com/Improbable-AI/softmimic) | ✓ | 466 MB | ✓ |  |
| 154 | WB·C | [[2510.26280\|Thor]] | [[2510.26280v2.pdf]] | — *(no public code)* | — | — | — | Code "coming soon" — not released yet |
| 155 | WB·C | [[2511.04679\|GentleHumanoid]] | [[2511.04679v1.pdf]] | [`Axellwppr/gentle-humanoid`](https://github.com/Axellwppr/gentle-humanoid) | ✓ | 138 MB | ✓ | inference/deploy only; training code in a separate repo |
| 156 | WB·C | [[2511.06385\|Path-Consistent-Safety-Filter]] | [[2511.06385v2.pdf]] | [`JulianBalletshofer/pacs-ros2`](https://github.com/JulianBalletshofer/pacs-ros2) | ✓ | 488 MB | ✗ | requires proprietary ruckig pro for trajectory generation |
| 157 | WB·C | [[2511.18509\|SafeFall]] | [[2511.18509v1.pdf]] | — *(no public code)* | — | — | — | Code "coming soon" — not released yet |
| 158 | WB·C | [[2511.20275\|HAFO]] | [[2511.20275v4.pdf]] | — *(no public code)* | — | — | — | Code "coming soon" — not released yet |
| 159 | WB·C | [[2512.01061\|Sim-to-Real-Door]] | [[2512.01061v1.pdf]] | [`NVlabs/GR00T-VisualSim2Real`](https://github.com/NVlabs/GR00T-VisualSim2Real) | ✓ | 75 MB | ✓ | DoorMan code on separate doorman branch |
| 160 | WB·C | [[2601.07821\|FARL]] | [[2601.07821v1.pdf]] | — *(no public code)* | — | — | — | Code "coming soon" — not released yet |
| 161 | WB·C | [[2602.01515\|RAPT]] | [[2602.01515v1.pdf]] | — *(no public code)* | — | — | — | No public code repo |
| 162 | WB·C | [[2603.14308\|Load-Aware-Loco-Manipulation]] | [[2603.14308v1.pdf]] | — *(no public code)* | — | — | — | Project page only — no code repo |
| 163 | WB·C | [[2603.22703\|Safe-Stoppability-Monitor]] | [[2603.22703v1.pdf]] | [`intelligent-control-lab/humanoid_stoppability`](https://github.com/intelligent-control-lab/humanoid_stoppability) | ✓ | 20 MB | ✓ | README only — code not yet released |
| 164 | WB·C | [[2605.10063\|EFGCL]] | [[2605.10063v1.pdf]] | — *(no public code)* | — | — | — | No public code repo |
| 165 | WB·C | [[2605.21935\|MIF]] | [[2605.21935v1.pdf]] | [`Ziya-Jiang/MIF-homepage`](https://github.com/Ziya-Jiang/MIF-homepage) | ✓ | 815 MB | ✓ | Project-page repo with placeholder assets, no code |
| 166 | WB·C | [[2605.25546\|ISSf-CBF-WBC]] | [[2605.25546v1.pdf]] | [`dyroshumanoid/safeWBC`](https://github.com/dyroshumanoid/safeWBC) | ✓ | 897 MB | ✓ |  |
| 167 | WB·C | [[2606.03297\|SplitAdapter]] | [[2606.03297v1.pdf]] | [`splitadapter/splitadapter.github.io`](https://github.com/splitadapter/splitadapter.github.io) | ✓ | 357 MB | ✓ | Project page (HTML, paper PDF, videos), no code |
| 168 | WB·C | [[2606.13232\|WT-UMI]] | [[2606.13232v1.pdf]] | [`wt-umi/WTUMI`](https://github.com/wt-umi/WTUMI) | ✓ | 1.1 GB | ✓ | Project page (HTML, videos, hardware guide), no code |
| 169 | WB·C | [[2606.16542\|ADAPT-Locomotion]] | [[2606.16542v1.pdf]] | [`blyu413/ADAPT`](https://github.com/blyu413/ADAPT) | ✓ | 107 MB | ✓ | README only — code not yet released |
| 170 | WAM·A | [[2112.06442\|Deep-Predictive-Vision-Tactile]] | [[2112.06442v2.pdf]] | — *(no public code)* | — | — | — |  |
| 171 | WAM·A | [[2206.14244\|MWM-Masked-WM]] | [[2206.14244v3.pdf]] | [`younggyoseo/MWM`](https://github.com/younggyoseo/MWM) | ✓ | 25 MB | ✓ |  |
| 172 | WAM·A | [[2211.10831\|JEPA-Slow-Features]] | [[2211.10831v1.pdf]] | [`vladisai/JEPA_SSL_NeurIPS_2022`](https://github.com/vladisai/JEPA_SSL_NeurIPS_2022) | ✓ | 29 MB | ✓ |  |
| 173 | WAM·A S2R·B EAI·B | [[2304.07193\|DINOv2]] | [[2304.07193v2.pdf]] | [`facebookresearch/dinov2`](https://github.com/facebookresearch/dinov2) | ✓ | 62 MB | ✓ |  |
| 174 | WAM·A EAI·B | [[2306.03310\|LIBERO]] | [[2306.03310v2.pdf]] | [`Lifelong-Robot-Learning/LIBERO`](https://github.com/Lifelong-Robot-Learning/LIBERO) | ✓ | 795 MB | ✓ |  |
| 175 | WAM·A S2R·B | [[2402.08191\|THE-COLOSSEUM]] | [[2402.08191v2.pdf]] | [`robot-colosseum/robot-colosseum`](https://github.com/robot-colosseum/robot-colosseum) | ✓ | 670 MB | ✓ |  |
| 176 | WAM·A | [[2407.01570\|Ego-Foresight]] | [[2407.01570v4.pdf]] | [`ego-foresight/efrl`](https://github.com/ego-foresight/efrl) | ✓ | 8.9 MB | ✓ | README only — code not yet released |
| 177 | WAM·A | [[2409.18330\|DMC-VB]] | [[2409.18330v1.pdf]] | [`google-deepmind/dmc_vision_benchmark`](https://github.com/google-deepmind/dmc_vision_benchmark) | ✓ | 613 MB | ✓ |  |
| 178 | WAM·A | [[2410.24090\|Sparsh]] | [[2410.24090v1.pdf]] | [`facebookresearch/sparsh`](https://github.com/facebookresearch/sparsh) | ✓ | 150 MB | ✓ |  |
| 179 | WAM·A EAI·B | [[2411.04983\|DINO-WM]] | [[2411.04983v2.pdf]] | [`gaoyuezhou/dino_wm`](https://github.com/gaoyuezhou/dino_wm) | ✓ | 50 MB | ✓ |  |
| 180 | WAM·A | [[2411.12503\|ManiSkill-ViTac-2025]] | [[2411.12503v1.pdf]] | [`cyliizyz/ManiSkill-ViTac2025`](https://github.com/cyliizyz/ManiSkill-ViTac2025) | ✓ | 77 MB | ✓ |  |
| 181 | WAM·A | [[2412.14803\|VPP]] | [[2412.14803v2.pdf]] | [`roboterax/video-prediction-policy`](https://github.com/roboterax/video-prediction-policy) | ✓ | 76 MB | ✓ |  |
| 182 | WAM·A | [[2412.15109\|Seer]] | [[2412.15109v1.pdf]] | [`OpenRobotLab/Seer`](https://github.com/OpenRobotLab/Seer) | ✓ | 61 MB | ✓ |  |
| 183 | WAM·A | [[2502.02853\|Rethinking-Latent-Redundancy-Behavior]] | [[2502.02853v5.pdf]] | [`BaiShuanghao/BC-IB`](https://github.com/BaiShuanghao/BC-IB) | ✓ | 480 MB | ✓ |  |
| 184 | WAM·A | [[2502.03270\|Temporal-Trap-Entanglement-Pre-Trained]] | [[2502.03270v3.pdf]] | [`tsagkas/pvrobo`](https://github.com/tsagkas/pvrobo) | ✓ | 26 MB | ✓ |  |
| 185 | WAM·A | [[2503.00200\|UVA]] | [[2503.00200v3.pdf]] | [`ShuangLI59/unified_video_action`](https://github.com/ShuangLI59/unified_video_action) | ✓ | 300 MB | ✓ |  |
| 186 | WAM·A | [[2503.00653\|DC-MPC]] | [[2503.00653v1.pdf]] | [`aidanscannell/dcmpc`](https://github.com/aidanscannell/dcmpc) | ✓ | 111 MB | ✓ |  |
| 187 | WAM·A | [[2504.02792\|UWM]] | [[2504.02792v3.pdf]] | [`WEIRDLabUW/unified-world-model`](https://github.com/WEIRDLabUW/unified-world-model) | ✓ | 33 MB | ✓ |  |
| 188 | WAM·A EAI·B | [[2504.13059\|RoboTwin]] | [[2504.13059v1.pdf]] | [`agilexrobotics/RoboTwin`](https://github.com/agilexrobotics/RoboTwin) | ✓ | 43 MB | ✓ | Task info + data-collection pipeline marked 'coming soon'/'released soon' |
| 189 | WAM·A | [[2504.16591\|JEPA-for-RL]] | [[2504.16591v1.pdf]] | — *(no public code)* | — | — | — |  |
| 190 | WAM·A | [[2505.04999\|CLAM]] | [[2505.04999v1.pdf]] | [`clamrobot/clam`](https://github.com/clamrobot/clam) | ✓ | 31 MB | ✓ | Data generation marked TODO |
| 191 | WAM·A | [[2505.11528\|LaDi-WM]] | [[2505.11528v6.pdf]] | [`GuHuangAI/LaDiWM`](https://github.com/GuHuangAI/LaDiWM) | ✓ | 1.5 GB | ✓ |  |
| 192 | WAM·A | [[2505.13982\|AdapTac]] | [[2505.13982v2.pdf]] | [`kingchou007/adaptac-dex`](https://github.com/kingchou007/adaptac-dex) | ✓ | 111 MB | ✓ |  |
| 193 | WAM·A | [[2505.18472\|ManiFeel]] | [[2505.18472v2.pdf]] | [`purdue-mars/manifeel`](https://github.com/purdue-mars/manifeel) | ✓ | 238 MB | ✓ |  |
| 194 | WAM·A | [[2505.19386\|Force-Prompting]] | [[2505.19386v2.pdf]] | [`brown-palm/force-prompting`](https://github.com/brown-palm/force-prompting) | ✓ | 408 MB | ✓ |  |
| 195 | WAM·A | [[2506.14198\|AMPLIFY]] | [[2506.14198v1.pdf]] | [`pairlab/AMPLIFY`](https://github.com/pairlab/AMPLIFY) | ✓ | 37 MB | ✓ |  |
| 196 | WAM·A | [[2506.14754\|Sparsh-X]] | [[2506.14754v1.pdf]] | [`facebookresearch/sparsh-multisensory-touch`](https://github.com/facebookresearch/sparsh-multisensory-touch) | ✓ | 149 MB | ✓ |  |
| 197 | WAM·A | [[2507.19468\|DINO-world]] | [[2507.19468v1.pdf]] | — *(no public code)* | — | — | — |  |
| 198 | WAM·A | [[2508.10104\|DINOv3]] | [[2508.10104v1.pdf]] | [`facebookresearch/dinov3`](https://github.com/facebookresearch/dinov3) | ✓ | 96 MB | ✓ |  |
| 199 | WAM·A | [[2508.17600\|GWM]] | [[2508.17600v2.pdf]] | [`Gaussian-World-Model/gaussianwm`](https://github.com/Gaussian-World-Model/gaussianwm) | ✓ | 40 MB | ✓ | README marks WIP; only pretraining released, more code being sorted out |
| 200 | WAM·A | [[2509.07962\|TA-VLA]] | [[2509.07962v1.pdf]] | [`ZZongzheng0918/TA-VLA`](https://github.com/ZZongzheng0918/TA-VLA) | ✓ | 44 MB | ✓ |  |
| 201 | WAM·A | [[2509.12249\|P-JEPA]] | [[2509.12249v2.pdf]] | [`jasonyu48/concept_discovery`](https://github.com/jasonyu48/concept_discovery) | ✓ | 993 MB | ✓ |  |
| 202 | WAM·A | [[2509.21797\|MoWM]] | [[2509.21797v3.pdf]] | [`tsinghua-fib-lab/MoWM`](https://github.com/tsinghua-fib-lab/MoWM) | ✓ | 15 MB | ✓ |  |
| 203 | WAM·A | [[2510.00739\|TD-JEPA]] | [[2510.00739v1.pdf]] | [`facebookresearch/td_jepa`](https://github.com/facebookresearch/td_jepa) | ✓ | 52 MB | ✓ |  |
| 204 | WAM·A | [[2510.05057\|StaMo]] | [[2510.05057v2.pdf]] | [`aim-uofa/StaMo`](https://github.com/aim-uofa/StaMo) | ✓ | 21 MB | ✓ |  |
| 205 | WAM·A EAI·B | [[2510.13626\|LIBERO-Plus]] | [[2510.13626v3.pdf]] | [`sylvestf/LIBERO-plus`](https://github.com/sylvestf/LIBERO-plus) | ✓ | 594 MB | ✓ |  |
| 206 | WAM·A | [[2510.16732\|World-Models-for-Embodied-AI-Survey]] | [[2510.16732v2.pdf]] | [`Li-Zn-H/AwesomeWorldModels`](https://github.com/Li-Zn-H/AwesomeWorldModels) | ✓ | 16 MB | ✓ | Curated list (survey), no method code |
| 207 | WAM·A | [[2511.02097\|WM-Manipulation-Survey]] | [[2511.02097v2.pdf]] | — *(no public code)* | — | — | — |  |
| 208 | WAM·A | [[2511.08544\|LeJEPA]] | [[2511.08544v3.pdf]] | [`rbalestr-lab/lejepa`](https://github.com/rbalestr-lab/lejepa) | ✓ | 40 MB | ✓ |  |
| 209 | WAM·A | [[2512.15692\|mimic-video]] | [[2512.15692v2.pdf]] | [`mimic-video/mimic-video`](https://github.com/mimic-video/mimic-video) | ✓ | 779 MB | ✓ |  |
| 210 | WAM·A | [[2512.16811\|GeoPredict]] | [[2512.16811v2.pdf]] | [`jingjingqian75/GeoPredict`](https://github.com/jingjingqian75/GeoPredict) | ✓ | 28 MB | ✓ | Inference + checkpoints only; training code coming June 2026 |
| 211 | WAM·A | [[2512.23864\|DreamTacVLA]] | [[2512.23864v3.pdf]] | [`michaelyeah7/learning-to-feel-the-future`](https://github.com/michaelyeah7/learning-to-feel-the-future) | ✓ | 264 MB | ✓ |  |
| 212 | WAM·A | [[2601.05848\|Goal-Force]] | [[2601.05848v2.pdf]] | [`brown-palm/goal-force`](https://github.com/brown-palm/goal-force) | ✓ | 212 MB | ✓ |  |
| 213 | WAM·A | [[2601.14354\|VJEPA-Probabilistic]] | [[2601.14354v1.pdf]] | [`yongchaohuang/vjepa`](https://github.com/yongchaohuang/vjepa) | ✓ | 15 MB | ✓ |  |
| 214 | WAM·A | [[2601.20321\|TaF-VLA]] | [[2601.20321v2.pdf]] | [`mrHuangyz/TaF-VLA`](https://github.com/mrHuangyz/TaF-VLA) | ✓ | 357 MB | ✓ | Benchmark dataset only, no training code |
| 215 | WAM·A | [[2602.01153\|UniForce]] | [[2602.01153v1.pdf]] | — *(no public code)* | — | — | — |  |
| 216 | WAM·A | [[2602.02142\|FD-VLA]] | [[2602.02142v2.pdf]] | — *(no public code)* | — | — | — |  |
| 217 | WAM·A | [[2602.06001\|VT-WM]] | [[2602.06001v1.pdf]] | — *(no public code)* | — | — | — |  |
| 218 | WAM·A | [[2602.10098\|VLA-JEPA]] | [[2602.10098v2.pdf]] | [`ginwind/VLA-JEPA`](https://github.com/ginwind/VLA-JEPA) | ✓ | 58 MB | ✓ |  |
| 219 | WAM·A | [[2602.10102\|VideoWorld-2]] | [[2602.10102v1.pdf]] | [`ByteDance-Seed/VideoWorld`](https://github.com/ByteDance-Seed/VideoWorld) | ✓ | 219 MB | ✓ |  |
| 220 | WAM·A | [[2602.11832\|JEPA-VLA]] | [[2602.11832v1.pdf]] | — *(no public code)* | — | — | — |  |
| 221 | WAM·A | [[2602.14174\|Direction-Matters]] | [[2602.14174v1.pdf]] | — *(no public code)* | — | — | — |  |
| 222 | WAM·A | [[2602.16086\|LGQ]] | [[2602.16086v2.pdf]] | [`KurbanIntelligenceLab/LGQ`](https://github.com/KurbanIntelligenceLab/LGQ) | ✓ | 38 MB | ✓ |  |
| 223 | WAM·A | [[2602.18639\|Bisimulation-JEPA-Planning]] | [[2602.18639v1.pdf]] | — *(no public code)* | — | — | — |  |
| 224 | WAM·A | [[2602.23058\|GeoWorld]] | [[2602.23058v2.pdf]] | — *(no public code)* | — | — | — |  |
| 225 | WAM·A | [[2603.05438\|CompACT]] | [[2603.05438v1.pdf]] | [`kdwonn/CompACT`](https://github.com/kdwonn/CompACT) | ✓ | 155 MB | ✓ |  |
| 226 | WAM·A | [[2603.12553\|Structured-WM-Planner]] | [[2603.12553v1.pdf]] | [`wm-planner/structvla`](https://github.com/wm-planner/structvla) | ✓ | 134 MB | ✓ |  |
| 227 | WAM·A | [[2603.14482\|V-JEPA-2.1]] | [[2603.14482v3.pdf]] | [`facebookresearch/vjepa2`](https://github.com/facebookresearch/vjepa2) | ✓ | 58 MB | ✓ |  |
| 228 | WAM·A | [[2603.15169\|ForceVLA2]] | [[2603.15169v1.pdf]] | — *(no public code)* | — | — | — |  |
| 229 | WAM·A | [[2603.15257\|HapticVLA]] | [[2603.15257v1.pdf]] | [`Advanced-Robotic-Manipulation/crab`](https://github.com/Advanced-Robotic-Manipulation/crab) | ✓ | 157 MB | ✓ |  |
| 230 | WAM·A | [[2603.16666\|Fast-WAM]] | [[2603.16666v2.pdf]] | [`yuantianyuan01/FastWAM`](https://github.com/yuantianyuan01/FastWAM) | ✓ | 56 MB | ✓ |  |
| 231 | WAM·A | [[2603.17240\|GigaWorld-Policy]] | [[2603.17240v2.pdf]] | [`open-gigaai/giga-world-policy`](https://github.com/open-gigaai/giga-world-policy) | ✓ | 43 MB | ✓ |  |
| 232 | WAM·A | [[2603.17851\|DexViTac]] | [[2603.17851v1.pdf]] | [`xitong-c/DexViTac`](https://github.com/xitong-c/DexViTac) | ✓ | 238 MB | ✓ | Project website only, no code |
| 233 | WAM·A | [[2603.19201\|OmniVTA]] | [[2603.19201v2.pdf]] | [`mrsecant/OmniVTA`](https://github.com/mrsecant/OmniVTA) | ✓ | 2.1 GB | ✓ | README only — code not yet released |
| 234 | WAM·A | [[2603.20111\|Var-JEPA]] | [[2603.20111v1.pdf]] | — *(no public code)* | — | — | — |  |
| 235 | WAM·A EAI·B | [[2603.22078\|WAM-vs-VLA-Robustness]] | [[2603.22078v3.pdf]] | — *(no public code)* | — | — | — |  |
| 236 | WAM·A | [[2603.29090\|HCLSM]] | [[2603.29090v1.pdf]] | [`rightnow-ai/hclsm`](https://github.com/rightnow-ai/hclsm) | ✓ | 42 MB | ✓ |  |
| 237 | WAM·A | [[2603.29409\|CLaD]] | [[2603.29409v1.pdf]] | — *(no public code)* | — | — | — |  |
| 238 | WAM·A | [[2604.01414\|Adaptive-Vision-Torque-Fusion]] | [[2604.01414v1.pdf]] | — *(no public code)* | — | — | — |  |
| 239 | WAM·A | [[2604.01985\|WAV]] | [[2604.01985v2.pdf]] | [`world-action-verifier/wav_minigrid`](https://github.com/world-action-verifier/wav_minigrid) | ✓ | 43 MB | ✓ |  |
| 240 | WAM·A | [[2604.02029\|Latent-Space-Survey]] | [[2604.02029v2.pdf]] | [`YU-deep/Awesome-Latent-Space`](https://github.com/YU-deep/Awesome-Latent-Space) | ✓ | 78 MB | ✓ | Curated list (survey), no method code |
| 241 | WAM·A | [[2604.07335\|TAMEn]] | [[2604.07335v1.pdf]] | [`OpenDriveLab/TAMEn`](https://github.com/OpenDriveLab/TAMEn) | ✓ | 219 MB | ✓ | Only tAmeR teleop app; CAD, data, training, inference unreleased |
| 242 | WAM·A | [[2604.13015\|HTD]] | [[2604.13015v2.pdf]] | [`chrisyrniu/humanoid-touch-dream`](https://github.com/chrisyrniu/humanoid-touch-dream) | ✓ | 72 MB | ✓ | README only — code not yet released |
| 243 | WAM·A | [[2604.16484\|DexWorldModel]] | [[2604.16484v1.pdf]] | — *(no public code)* | — | — | — |  |
| 244 | WAM·A EAI·B | [[2604.16592\|Cognition-WM-Survey]] | [[2604.16592v2.pdf]] | — *(no public code)* | — | — | — |  |
| 245 | WAM·A | [[2604.17876\|OFlow]] | [[2604.17876v1.pdf]] | — *(no public code)* | — | — | — |  |
| 246 | WAM·A | [[2604.19092\|RoboWM-Bench]] | [[2604.19092v2.pdf]] | [`fffstrong/RoboWM-Bench`](https://github.com/fffstrong/RoboWM-Bench) | ✓ | 2.5 GB | ✓ |  |
| 247 | WAM·A | [[2604.20444\|VTouch++]] | [[2604.20444v1.pdf]] | — *(no public code)* | — | — | — |  |
| 248 | WAM·A | [[2604.25859\|PFD]] | [[2604.25859v2.pdf]] | [`PengchengFang-cs/PFD`](https://github.com/PengchengFang-cs/PFD) | ✓ | 55 MB | ✓ |  |
| 249 | WAM·A | [[2605.00078\|Being-H0.7]] | [[2605.00078v1.pdf]] | [`BeingBeyond/Being-H`](https://github.com/BeingBeyond/Being-H) | ✓ | 135 MB | ✓ | Being-H0.7 (this paper) code/checkpoints coming soon; only H0.5 released |
| 250 | WAM·A | [[2605.06222\|FFDC-WAM]] | [[2605.06222v2.pdf]] | — *(no public code)* | — | — | — |  |
| 251 | WAM·A | [[2605.06388\|Semantic-LDM-WM]] | [[2605.06388v1.pdf]] | [`chandar-lab/semantic-wm`](https://github.com/chandar-lab/semantic-wm) | ✓ | 33 MB | ✓ |  |
| 252 | WAM·A | [[2605.10942\|HarmoWAM]] | [[2605.10942v1.pdf]] | — *(no public code)* | — | — | — |  |
| 253 | WAM·A EAI·B | [[2605.12090\|WAM-Survey]] | [[2605.12090v1.pdf]] | [`OpenMOSS/Awesome-WAM`](https://github.com/OpenMOSS/Awesome-WAM) | ✓ | 3.5 GB | ✓ | Curated WAM survey list, no method code |
| 254 | WAM·A | [[2605.13083\|TouchAnything]] | [[2605.13083v1.pdf]] | [`Jianyi2004/TouchAnything`](https://github.com/Jianyi2004/TouchAnything) | ✓ | 242 MB | ✓ | Code released but dataset upload in progress, may be incomplete |
| 255 | WAM·A | [[2605.15153\|Pelican-Unified]] | [[2605.15153v2.pdf]] | — *(no public code)* | — | — | — |  |
| 256 | WAM·A | [[2605.15618\|Latent-Video-Prediction-Study]] | [[2605.15618v1.pdf]] | — *(no public code)* | — | — | — |  |
| 257 | WAM·A | [[2605.15725\|DiLA]] | [[2605.15725v1.pdf]] | [`senngadaisuki/disentangled-latent-action-world-models`](https://github.com/senngadaisuki/disentangled-latent-action-world-models) | ✓ | 75 MB | ✓ |  |
| 258 | WAM·A | [[2605.19986\|MetaFine]] | [[2605.19986v1.pdf]] | [`Hiangx-robotics/MetaFine`](https://github.com/Hiangx-robotics/MetaFine) | ✓ | 599 MB | ✓ |  |
| 259 | WAM·A | [[2605.20752\|GaussianDream]] | [[2605.20752v2.pdf]] | [`TuojingAI/GaussianDream`](https://github.com/TuojingAI/GaussianDream) | ✓ | 72 MB | ✓ | checkpoints, datasets, full reproduction instructions not yet released |
| 260 | WAM·A | [[2605.21862\|EvoScene-VLA]] | [[2605.21862v1.pdf]] | — *(no public code)* | — | — | — |  |
| 261 | WAM·A | [[2605.22446\|Pre-VLA]] | [[2605.22446v1.pdf]] | — *(no public code)* | — | — | — |  |
| 262 | WAM·A | [[2605.22882\|GEM-4D]] | [[2605.22882v3.pdf]] | — *(no public code)* | — | — | — |  |
| 263 | WAM·A EAI·B | [[2605.26379\|LeJEPA-World-Model]] | [[2605.26379v1.pdf]] | [`klindtlab/lejepa-identifiability`](https://github.com/klindtlab/lejepa-identifiability) | ✓ | 61 MB | ✓ |  |
| 264 | WAM·A | [[2605.28816\|Gamma-World]] | [[2605.28816v1.pdf]] | [`nv-tlabs/Gamma-World`](https://github.com/nv-tlabs/Gamma-World) | ✓ | 247 MB | ✓ |  |
| 265 | WAM·A | [[2606.01955\|WALL-WM]] | [[2606.01955v1.pdf]] | [`X-Square-Robot/wall-x`](https://github.com/X-Square-Robot/wall-x) | ✓ | 73 MB | ✓ |  |
| 266 | WAM·A | [[2606.02800\|Cosmos-3]] | [[2606.02800v3.pdf]] | [`nvidia/cosmos`](https://github.com/nvidia/cosmos) | ✓ | 230 MB | ✓ |  |
| 267 | WAM·A | [[2606.03188\|GeoSem-WAM]] | [[2606.03188v1.pdf]] | — *(no public code)* | — | — | — |  |
| 268 | WAM·A | [[2606.04130\|CLAW-Latent-Action-WM]] | [[2606.04130v1.pdf]] | — *(no public code)* | — | — | — |  |
| 269 | WAM·A EAI·B | [[2606.05254\|Flash-WAM]] | [[2606.05254v1.pdf]] | [`NU-World-Model-Embodied-AI/Flash-WAM`](https://github.com/NU-World-Model-Embodied-AI/Flash-WAM) | ✓ | 62 MB | ✓ | real-world Unitree G1 deployment setup not released |
| 270 | WAM·A | [[2606.05979\|WLA]] | [[2606.05979v1.pdf]] | [`SJTU-DENG-Lab/WLA`](https://github.com/SJTU-DENG-Lab/WLA) | ✓ | 32 MB | ✓ | Efficient Mode and TTS Mode code not released |
| 271 | WAM·A | [[2606.08737\|Dream-Tac]] | [[2606.08737v1.pdf]] | [`LYFCLOUDFAN/Dream-Tac`](https://github.com/LYFCLOUDFAN/Dream-Tac) | ✓ | 160 MB | ✓ |  |
| 272 | WAM·A | [[2606.09337\|TORL-VLA]] | [[2606.09337v3.pdf]] | — *(no public code)* | — | — | — |  |
| 273 | WAM·A | [[2606.09811\|AHA-WAM]] | [[2606.09811v1.pdf]] | [`serene-sivy/AHA-WAM`](https://github.com/serene-sivy/AHA-WAM) | ✓ | 3.0 MB | ✓ | README only — code not yet released |
| 274 | WAM·A | [[2606.10040\|Efficient-WAM]] | [[2606.10040v2.pdf]] | [`jiajun613/Efficient-WAM`](https://github.com/jiajun613/Efficient-WAM) | ✓ | 49 MB | ✓ |  |
| 275 | WAM·A | [[2606.11184\|TacForeSight]] | [[2606.11184v1.pdf]] | — *(no public code)* | — | — | — |  |
| 276 | WAM·A | [[2606.12217\|AGRA]] | [[2606.12217v1.pdf]] | — *(no public code)* | — | — | — |  |
| 277 | WAM·A | [[2606.12406\|FACTR-2]] | [[2606.12406v1.pdf]] | — *(no public code)* | — | — | — |  |
| 278 | WAM·A | [[2606.13769\|μ0]] | [[2606.13769v2.pdf]] | — *(no public code)* | — | — | — |  |
| 279 | WAM·A | [[2606.13877\|ContactWorld]] | [[2606.13877v1.pdf]] | [`PokuangZhou/ContactWorld`](https://github.com/PokuangZhou/ContactWorld) | ✓ | 402 MB | ✓ |  |
| 280 | WAM·A | [[2606.14048\|WAM4D]] | [[2606.14048v1.pdf]] | — *(no public code)* | — | — | — |  |
| 281 | WAM·A | [[2606.17046\|GAM]] | [[2606.17046v1.pdf]] | [`cvlab-kaist/Geometric-Action-Model`](https://github.com/cvlab-kaist/Geometric-Action-Model) | ✓ | 59 MB | ✓ | README only — code not yet released |
| 282 | S2R·B | [[2104.02646\|gradSim]] | [[2104.02646v1.pdf]] | [`gradsim/gradsim`](https://github.com/gradsim/gradsim) | ✓ | 63 MB | ✓ |  |
| 283 | S2R·B | [[2204.03139\|DiffCloud]] | [[2204.03139v2.pdf]] | [`priyasundaresan/diffcloud_real2sim`](https://github.com/priyasundaresan/diffcloud_real2sim) | ✓ | 430 MB | ✗ |  |
| 284 | S2R·B | [[2207.10821\|Lower-Fidelity-Sim2Real]] | [[2207.10821v2.pdf]] | [`joannetruong/robot-nav`](https://github.com/joannetruong/robot-nav) | ✓ | 17 MB | ✓ |  |
| 285 | S2R·B | [[2304.14369\|NCLaw]] | [[2304.14369v2.pdf]] | [`PingchuanMa/NCLaw`](https://github.com/PingchuanMa/NCLaw) | ✓ | 84 MB | ✓ |  |
| 286 | S2R·B | [[2306.15668\|Physion++]] | [[2306.15668v2.pdf]] | — *(no public code)* | — | — | — |  |
| 287 | S2R·B | [[2403.03949\|RialTo]] | [[2403.03949v3.pdf]] | [`real-to-sim-to-real/RialTo`](https://github.com/real-to-sim-to-real/RialTo) | ✓ | 889 MB | ✓ | Project website only, no code |
| 288 | S2R·B | [[2403.12945\|DROID]] | [[2403.12945v2.pdf]] | [`droid-dataset/droid`](https://github.com/droid-dataset/droid) | ✓ | 879 MB | ✓ |  |
| 289 | S2R·B | [[2404.09833\|Video2Game]] | [[2404.09833v1.pdf]] | [`video2game/video2game`](https://github.com/video2game/video2game) | ✓ | 212 MB | ✓ |  |
| 290 | S2R·B | [[2404.12308\|ASID]] | [[2404.12308v2.pdf]] | [`WEIRDLabUW/asid`](https://github.com/WEIRDLabUW/asid) | ✓ | 98 MB | ✓ |  |
| 291 | S2R·B | [[2406.04155\|Lagrangian-Particle-Optimization]] | [[2406.04155v1.pdf]] | — *(no public code)* | — | — | — |  |
| 292 | S2R·B | [[2406.10788\|Embodied-Gaussians]] | [[2406.10788v1.pdf]] | [`bdaiinstitute/embodied_gaussians`](https://github.com/bdaiinstitute/embodied_gaussians) | ✓ | 88 MB | ✓ | Reference impl: rigid bodies only, shape matching omitted |
| 293 | S2R·B | [[2406.12769\|Latent-Intuitive-Physics]] | [[2406.12769v1.pdf]] | [`xherdan76/LIP`](https://github.com/xherdan76/LIP) | ✓ | 26 MB | ✓ |  |
| 294 | S2R·B | [[2407.07889\|AdaptiGraph]] | [[2407.07889v1.pdf]] | [`Boey-li/AdaptiGraph`](https://github.com/Boey-li/AdaptiGraph) | ✓ | 358 MB | ✗ |  |
| 295 | S2R·B | [[2409.20291\|RL-GSBridge]] | [[2409.20291v2.pdf]] | [`IRMV-Manipulation-Group/RL-GSBridge`](https://github.com/IRMV-Manipulation-Group/RL-GSBridge) | ✓ | 267 MB | ✓ | TODOs: data link, model alignment, run instructions missing |
| 296 | S2R·B | [[2410.20357\|Dynamics-as-Prompts]] | [[2410.20357v2.pdf]] | [`XilunZhangRobo/CAPTURE-Sim2Real`](https://github.com/XilunZhangRobo/CAPTURE-Sim2Real) | ✓ | 839 MB | ✓ |  |
| 297 | S2R·B | [[2411.00554\|DPSI]] | [[2411.00554v3.pdf]] | [`IanYangChina/SI4RP-data`](https://github.com/IanYangChina/SI4RP-data) | ✓ | 6.8 GB | ✓ |  |
| 298 | S2R·B | [[2412.00259\|One-Shot-Real-to-Sim]] | [[2412.00259v4.pdf]] | [`yifanzhu95/RigidWorldModel`](https://github.com/yifanzhu95/RigidWorldModel) | ✓ | 45 MB | ✓ |  |
| 299 | S2R·B | [[2412.01770\|CASHER]] | [[2412.01770v3.pdf]] | — *(no public code)* | — | — | — |  |
| 300 | S2R·B | [[2501.12202\|Hunyuan3D]] | [[2501.12202v5.pdf]] | [`Tencent/Hunyuan3D-2`](https://github.com/Tencent/Hunyuan3D-2) | ✓ | 202 MB | ✓ |  |
| 301 | S2R·B | [[2501.18982\|OmniPhysGS]] | [[2501.18982v1.pdf]] | [`wgsxm/OmniPhysGS`](https://github.com/wgsxm/OmniPhysGS) | ✓ | 282 MB | ✓ |  |
| 302 | S2R·B | [[2502.01536\|VR-Robo]] | [[2502.01536v3.pdf]] | [`zst1406217/VR-Robo`](https://github.com/zst1406217/VR-Robo) | ✓ | 238 MB | ✓ |  |
| 303 | S2R·B | [[2502.08643\|IKER]] | [[2502.08643v2.pdf]] | [`shivanshpatel35/IKER`](https://github.com/shivanshpatel35/IKER) | ✓ | 148 MB | ✓ | only ShoePlace RL task; additional code 'to be released soon' |
| 304 | S2R·B | [[2502.08645\|Re3Sim]] | [[2502.08645v3.pdf]] | [`InternRobotics/Re3Sim`](https://github.com/InternRobotics/Re3Sim) | ✓ | 189 MB | ✓ |  |
| 305 | S2R·B | [[2502.18615\|Distributional-Treatment-Real2Sim2Real-Object-Centric]] | [[2502.18615v4.pdf]] | — *(no public code)* | — | — | — |  |
| 306 | S2R·B | [[2503.10118\|RSR-Loop]] | [[2503.10118v2.pdf]] | [`sunnyshi0310/RSR-MJX`](https://github.com/sunnyshi0310/RSR-MJX) | ✓ | 66 MB | ✓ |  |
| 307 | S2R·B | [[2503.17973\|PhysTwin]] | [[2503.17973v1.pdf]] | [`Jianghanxiao/PhysTwin`](https://github.com/Jianghanxiao/PhysTwin) | ✓ | 143 MB | ✓ |  |
| 308 | S2R·B | [[2503.22634\|Empirical-Analysis-Sim-and-Real-Cotraining]] | [[2503.22634v2.pdf]] | [`sim-and-real-cotraining/diffusion-policy`](https://github.com/sim-and-real-cotraining/diffusion-policy) | ✓ | 117 MB | ✓ |  |
| 309 | S2R·B | [[2504.03597\|Real-is-Sim]] | [[2504.03597v2.pdf]] | — *(no public code)* | — | — | — |  |
| 310 | S2R·B | [[2504.16693\|PIN-WM]] | [[2504.16693v2.pdf]] | [`XuAdventurer/PIN-WM`](https://github.com/XuAdventurer/PIN-WM) | ✓ | 93 MB | ✓ |  |
| 311 | S2R·B | [[2505.14266\|Sampling-Based-SysID]] | [[2505.14266v1.pdf]] | [`LeCAR-Lab/SPI-Active`](https://github.com/LeCAR-Lab/SPI-Active) | ✓ | 524 MB | ✓ | sim2real and dataset replay/visualize code not yet released |
| 312 | S2R·B | [[2505.16971\|UniPhy]] | [[2505.16971v1.pdf]] | [`HimangiM/UniPhy_CVPR2025`](https://github.com/HimangiM/UniPhy_CVPR2025) | ✓ | 97 MB | ✓ |  |
| 313 | S2R·B | [[2505.17966\|Single-View-Mesh-for-Robotics]] | [[2505.17966v2.pdf]] | — *(no public code)* | — | — | — |  |
| 314 | S2R·B | [[2505.24068\|DiffCoTune]] | [[2505.24068v1.pdf]] | — *(no public code)* | — | — | — |  |
| 315 | S2R·B | [[2506.02794\|PhysGaia]] | [[2506.02794v3.pdf]] | [`mjmjeong/PhysGaia`](https://github.com/mjmjeong/PhysGaia) | ✓ | 243 MB | ✓ | Benchmark dataset; method code on separate branches/external repos |
| 316 | S2R·B | [[2506.04120\|Splatting-Physical-Scenes]] | [[2506.04120v2.pdf]] | — *(no public code)* | — | — | — |  |
| 317 | S2R·B | [[2506.10133\|Offline-Domain-Randomization]] | [[2506.10133v2.pdf]] | — *(no public code)* | — | — | — |  |
| 318 | S2R·B | [[2506.15680\|Particle-Grid-Neural-Dynamics]] | [[2506.15680v2.pdf]] | [`kywind/pgnd`](https://github.com/kywind/pgnd) | ✓ | 62 MB | ✓ |  |
| 319 | S2R·B EAI·B | [[2506.18088\|RoboTwin-2.0]] | [[2506.18088v2.pdf]] | [`RoboTwin-Platform/RoboTwin`](https://github.com/RoboTwin-Platform/RoboTwin) | ✓ | 203 MB | ✓ |  |
| 320 | S2R·B | [[2508.01112\|MASIV]] | [[2508.01112v1.pdf]] | [`Skaldak/MASIV`](https://github.com/Skaldak/MASIV) | ✓ | 56 MB | ✓ |  |
| 321 | S2R·B | [[2508.11117\|Robot-Policy-Eval-Sim2Real]] | [[2508.11117v1.pdf]] | — *(no public code)* | — | — | — |  |
| 322 | S2R·B | [[2509.18631\|Sim-Real-OT-Co-Training]] | [[2509.18631v3.pdf]] | [`TTimelord/ot-sim2real`](https://github.com/TTimelord/ot-sim2real) | ✓ | 267 MB | ✓ |  |
| 323 | S2R·B | [[2509.24948\|RehearseVLA]] | [[2509.24948v6.pdf]] | [`amap-cvlab/world-env`](https://github.com/amap-cvlab/world-env) | ✓ | 100 MB | ✓ |  |
| 324 | S2R·B | [[2510.11689\|Phys2Real]] | [[2510.11689v2.pdf]] | [`phys2real/phys2real`](https://github.com/phys2real/phys2real) | ✓ | 895 MB | ✓ |  |
| 325 | S2R·B | [[2510.17950\|RoboChallenge]] | [[2510.17950v1.pdf]] | — *(no public code)* | — | — | — |  |
| 326 | S2R·B | [[2510.20813\|GSWorld]] | [[2510.20813v1.pdf]] | [`3dgsworld/gsworld`](https://github.com/3dgsworld/gsworld) | ✓ | 535 MB | ✓ | build-your-own-scene workflow marked WIP |
| 327 | S2R·B | [[2510.22975\|VoMP]] | [[2510.22975v2.pdf]] | [`nv-tlabs/VoMP`](https://github.com/nv-tlabs/VoMP) | ✓ | 416 MB | ✓ |  |
| 328 | S2R·B | [[2510.24673\|Differentiable-Rheometry]] | [[2510.24673v3.pdf]] | — *(no public code)* | — | — | — |  |
| 329 | S2R·B | [[2511.04665\|Real-to-Sim-GS]] | [[2511.04665v2.pdf]] | [`kywind/real2sim-eval`](https://github.com/kywind/real2sim-eval) | ✓ | 62 MB | ✓ |  |
| 330 | S2R·B | [[2511.04831\|Isaac-Lab]] | [[2511.04831v1.pdf]] | [`isaac-sim/IsaacLab`](https://github.com/isaac-sim/IsaacLab) | ✓ | 808 MB | ✓ |  |
| 331 | S2R·B | [[2511.06299\|Physics-Informed-Deformable-GS]] | [[2511.06299v3.pdf]] | [`SCAILab-USTC/Physics-Informed-Deformable-Gaussian-Splatting`](https://github.com/SCAILab-USTC/Physics-Informed-Deformable-Gaussian-Splatting) | ✓ | 343 MB | ✓ | full dataset withheld pending paper acceptance (double-blind constraints) |
| 332 | S2R·B | [[2511.07416\|PhysWorld]] | [[2511.07416v1.pdf]] | [`PointsCoder/OpenReal2Sim`](https://github.com/PointsCoder/OpenReal2Sim) | ✓ | 3.0 GB | ✓ |  |
| 333 | S2R·B | [[2512.00076\|Arcadia]] | [[2512.00076v1.pdf]] | [`Embodied-Arcadia/EmbodiedKit`](https://github.com/Embodied-Arcadia/EmbodiedKit) | ✓ | 123 MB | ✓ | setup guide and quickstart still TODO; partial scene/VLA-gen code |
| 334 | S2R·B | [[2512.13214\|Differentiable-MPM-Control]] | [[2512.13214v1.pdf]] | — *(no public code)* | — | — | — |  |
| 335 | S2R·B | [[2512.14696\|CRISP]] | [[2512.14696v3.pdf]] | [`crisp-real2sim/CRISP-Real2Sim`](https://github.com/crisp-real2sim/CRISP-Real2Sim) | ✓ | 200 MB | ✓ | main repo is project HTML; method code only in submodules |
| 336 | S2R·B | [[2512.16881\|PolaRiS]] | [[2512.16881v2.pdf]] | [`arhanjain/polaris`](https://github.com/arhanjain/polaris) | ✓ | 846 MB | ✓ |  |
| 337 | S2R·B | [[2512.19390\|TwinAligner]] | [[2512.19390v1.pdf]] | [`TwinAligner/TwinAligner`](https://github.com/TwinAligner/TwinAligner) | ✓ | 1.0 GB | ✓ |  |
| 338 | S2R·B | [[2512.19562\|REALM]] | [[2512.19562v1.pdf]] | [`martin-sedlacek/REALM`](https://github.com/martin-sedlacek/REALM) | ✓ | 437 MB | ✓ |  |
| 339 | S2R·B | [[2601.02078\|Genie-Sim-3.0]] | [[2601.02078v2.pdf]] | [`AgibotTech/genie_sim`](https://github.com/AgibotTech/genie_sim) | ✓ | 579 MB | ✓ |  |
| 340 | S2R·B | [[2601.03200\|3DGS-Digital-Twin]] | [[2601.03200v2.pdf]] | — *(no public code)* | — | — | — |  |
| 341 | S2R·B | [[2601.17251\|EMPM]] | [[2601.17251v1.pdf]] | — *(no public code)* | — | — | — |  |
| 342 | S2R·B | [[2602.02402\|SoMA-Sim]] | [[2602.02402v1.pdf]] | — *(no public code)* | — | — | — |  |
| 343 | S2R·B | [[2602.12628\|RL-Co]] | [[2602.12628v4.pdf]] | [`RLinf/RLinf`](https://github.com/RLinf/RLinf) | ✓ | 253 MB | ✓ |  |
| 344 | S2R·B | [[2603.01151\|D-REX]] | [[2603.01151v1.pdf]] | [`louhz/D-rex`](https://github.com/louhz/D-rex) | ✓ | 2.9 GB | ✓ | README notes unfinished integration, manual scale-alignment, config/path cleanup TODO |
| 345 | S2R·B | [[2603.04531\|PTLD]] | [[2603.04531v2.pdf]] | — *(no public code)* | — | — | — |  |
| 346 | S2R·B | [[2603.13825\|Explicit-WM-Manipulation]] | [[2603.13825v1.pdf]] | — *(no public code)* | — | — | — |  |
| 347 | S2R·B | [[2603.22039\|RAFL]] | [[2603.22039v1.pdf]] | [`generalroboticslab/RAFL`](https://github.com/generalroboticslab/RAFL) | ✓ | 278 MB | ✓ |  |
| 348 | S2R·B | [[2603.23973\|SLAT-Phys]] | [[2603.23973v1.pdf]] | — *(no public code)* | — | — | — |  |
| 349 | S2R·B | [[2603.25725\|SoftMimicGen]] | [[2603.25725v1.pdf]] | [`NVlabs/SoftMimicGen`](https://github.com/NVlabs/SoftMimicGen) | ✓ | 43 MB | ✓ |  |
| 350 | S2R·B | [[2604.04974\|Video-to-Control-Survey]] | [[2604.04974v3.pdf]] | — *(no public code)* | — | — | — |  |
| 351 | S2R·B | [[2604.08544\|SIM1]] | [[2604.08544v2.pdf]] | [`InternRobotics/SIM1`](https://github.com/InternRobotics/SIM1) | ✓ | 237 MB | ✓ |  |
| 352 | S2R·B | [[2604.10856\|BridgeSim]] | [[2604.10856v1.pdf]] | [`vail-ucla/BridgeSim`](https://github.com/vail-ucla/BridgeSim) | ✓ | 525 MB | ✓ |  |
| 353 | S2R·B | [[2604.11386\|ComSim]] | [[2604.11386v1.pdf]] | [`faceong/ComSim`](https://github.com/faceong/ComSim) | ✓ | 167 MB | ✓ | Project website only, no code |
| 354 | S2R·B | [[2604.13645\|CFG-ADDA]] | [[2604.13645v1.pdf]] | — *(no public code)* | — | — | — |  |
| 355 | S2R·B | [[2604.15805\|WorldComposer]] | [[2604.15805v1.pdf]] | [`jaber628/WorldComposer`](https://github.com/jaber628/WorldComposer) | ✓ | 68 MB | ✓ | training/eval, autocollection, full sim env not yet released |
| 356 | S2R·B | [[2604.26509\|3D-Generation-for-Embodied-AI-Survey]] | [[2604.26509v3.pdf]] | [`hitcslj/3DGen4Robot`](https://github.com/hitcslj/3DGen4Robot) | ✓ | 6.5 MB | ✓ | Curated list (survey), no method code |
| 357 | S2R·B | [[2604.27367\|DOT-Sim]] | [[2604.27367v1.pdf]] | — *(no public code)* | — | — | — |  |
| 358 | S2R·B | [[2605.00080\|WM-Robot-Learning-Survey]] | [[2605.00080v1.pdf]] | [`NTUMARS/Awesome-World-Model-for-Robotics-Policy`](https://github.com/NTUMARS/Awesome-World-Model-for-Robotics-Policy) | ✓ | 6.9 MB | ✓ | Curated list (survey), no method code |
| 359 | S2R·B | [[2605.09538\|PhysHanDI]] | [[2605.09538v1.pdf]] | — *(no public code)* | — | — | — |  |
| 360 | S2R·B | [[2605.26638\|HyperSim]] | [[2605.26638v1.pdf]] | — *(no public code)* | — | — | — |  |
| 361 | S2R·B | [[2605.28812\|CoP-Tactile]] | [[2605.28812v1.pdf]] | — *(no public code)* | — | — | — |  |
| 362 | S2R·B | [[2606.08828\|Video2Sim2Real]] | [[2606.08828v1.pdf]] | [`video2sim2real/video2sim2real`](https://github.com/video2sim2real/video2sim2real) | ✓ | 1.1 GB | ✓ | Initial release; further components to be added |
| 363 | S2R·B | [[2606.12604\|EgoEngine]] | [[2606.12604v1.pdf]] | — *(no public code)* | — | — | — |  |
| 364 | S2R·B | [[2606.15338\|SimWeaver]] | [[2606.15338v1.pdf]] | — *(no public code)* | — | — | — |  |
| 365 | S2R·B | [[2606.16202\|EgoPhys]] | [[2606.16202v1.pdf]] | — *(no public code)* | — | — | — |  |
| 366 | S2R·B | [[2606.17520\|GASE]] | [[2606.17520v1.pdf]] | — *(no public code)* | — | — | — |  |
| 367 | EAI·B | [[1612.00796\|EWC]] | [[1612.00796v2.pdf]] | — *(no public code)* | — | — | — |  |
| 368 | EAI·B | [[2105.10919\|Continual-World]] | [[2105.10919v3.pdf]] | [`awarelab/continual_world`](https://github.com/awarelab/continual_world) | ✓ | 36 MB | ✓ |  |
| 369 | EAI·B | [[2109.00137\|IBC]] | [[2109.00137v1.pdf]] | [`google-research/ibc`](https://github.com/google-research/ibc) | ✓ | 112 MB | ✓ |  |
| 370 | EAI·B | [[2109.08238\|HM3D]] | [[2109.08238v1.pdf]] | [`facebookresearch/habitat-matterport3d-dataset`](https://github.com/facebookresearch/habitat-matterport3d-dataset) | ✓ | 16 MB | ✓ | Dataset with experiment-reproduction scripts, no training code |
| 371 | EAI·B | [[2109.13202\|MiniHack]] | [[2109.13202v2.pdf]] | [`facebookresearch/minihack`](https://github.com/facebookresearch/minihack) | ✓ | 99 MB | ✓ |  |
| 372 | EAI·B | [[2211.15944\|Continual-Dreamer]] | [[2211.15944v2.pdf]] | [`skezle/continual-dreamer`](https://github.com/skezle/continual-dreamer) | ✓ | 38 MB | ✓ |  |
| 373 | EAI·B | [[2306.13394\|MME]] | [[2306.13394v5.pdf]] | [`BradyFU/Awesome-Multimodal-Large-Language-Models`](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) | ✓ | 131 MB | ✓ | Curated list (survey), no method code |
| 374 | EAI·B | [[2306.15724\|REFLECT]] | [[2306.15724v4.pdf]] | [`real-stanford/reflect`](https://github.com/real-stanford/reflect) | ✓ | 178 MB | ✓ |  |
| 375 | EAI·B | [[2307.06281\|MMBench]] | [[2307.06281v5.pdf]] | [`open-compass/MMBench`](https://github.com/open-compass/MMBench) | ✓ | 9.2 MB | ✓ | Benchmark data only, eval via external VLMEvalKit |
| 376 | EAI·B | [[2310.06253\|Objective-Mismatch-MBRL-Survey]] | [[2310.06253v2.pdf]] | [`ran-weii/objective_mismatch_papers`](https://github.com/ran-weii/objective_mismatch_papers) | ✓ | 8.3 MB | ✓ | Curated list (survey), no method code |
| 377 | EAI·B | [[2311.16502\|MMMU]] | [[2311.16502v4.pdf]] | [`MMMU-Benchmark/MMMU`](https://github.com/MMMU-Benchmark/MMMU) | ✓ | 251 MB | ✓ | Evaluation/inference code only, no training code |
| 378 | EAI·B | [[2312.01990\|SARA-RT]] | [[2312.01990v1.pdf]] | — *(no public code)* | — | — | — |  |
| 379 | EAI·B | [[2404.00756\|Recover]] | [[2404.00756v1.pdf]] | — *(no public code)* | — | — | — |  |
| 380 | EAI·B | [[2404.14387\|LLM-Self-Evolution-Survey]] | [[2404.14387v2.pdf]] | [`AlibabaResearch/DAMO-ConvAI`](https://github.com/AlibabaResearch/DAMO-ConvAI) | ✓ | 1.0 GB | ✓ |  |
| 381 | EAI·B | [[2405.09673\|LoRA-Learns-Less]] | [[2405.09673v2.pdf]] | [`danbider/lora-tradeoffs`](https://github.com/danbider/lora-tradeoffs) | ✓ | 8.8 MB | ✓ | README + figures only, no code (checkpoints on HF) |
| 382 | EAI·B | [[2406.04339\|RoboMamba]] | [[2406.04339v2.pdf]] | [`lmzpai/roboMamba`](https://github.com/lmzpai/roboMamba) | ✓ | 27 MB | ✓ | Training code not released (email-gated); inference only |
| 383 | EAI·B | [[2407.01531\|Sparse-Diffusion-Policy]] | [[2407.01531v2.pdf]] | [`AnthonyHuo/SDP`](https://github.com/AnthonyHuo/SDP) | ✓ | 57 MB | ✓ |  |
| 384 | EAI·B | [[2408.07666\|Model-Merging-in-LLMs/MLLMs]] | [[2408.07666v5.pdf]] | [`EnnengYang/Awesome-Model-Merging-Methods-Theories-Applications`](https://github.com/EnnengYang/Awesome-Model-Merging-Methods-Theories-Applications) | ✓ | 14 MB | ✓ | Curated list (survey), no method code |
| 385 | EAI·B | [[2410.00371\|AHA]] | [[2410.00371v1.pdf]] | [`NVlabs/AHA`](https://github.com/NVlabs/AHA) | ✓ | 68 MB | ✓ |  |
| 386 | EAI·B | [[2410.08001\|Synergistic-Generalized-Efficient-Dual-System]] | [[2410.08001v3.pdf]] | [`OpenDriveLab/RoboDual`](https://github.com/OpenDriveLab/RoboDual) | ✓ | 52 MB | ✓ |  |
| 387 | EAI·B | [[2412.04455\|Code-as-Monitor]] | [[2412.04455v3.pdf]] | — *(no public code)* | — | — | — |  |
| 388 | EAI·B | [[2501.10395\|t-DGR]] | [[2501.10395v1.pdf]] | [`WilliamYue37/AttentionTuner`](https://github.com/WilliamYue37/AttentionTuner) | ✓ | 16 MB | ✓ |  |
| 389 | EAI·B | [[2502.02175\|VLA-Cache]] | [[2502.02175v2.pdf]] | [`siyuhsu/vla-cache`](https://github.com/siyuhsu/vla-cache) | ✓ | 93 MB | ✓ |  |
| 390 | EAI·B | [[2502.10550\|MIKASA]] | [[2502.10550v3.pdf]] | [`CognitiveAISystems/MIKASA-Robo`](https://github.com/CognitiveAISystems/MIKASA-Robo) | ✓ | 1.2 GB | ✓ |  |
| 391 | EAI·B | [[2502.19645\|OpenVLA-OFT]] | [[2502.19645v2.pdf]] | [`moojink/openvla-oft`](https://github.com/moojink/openvla-oft) | ✓ | 49 MB | ✓ |  |
| 392 | EAI·B | [[2503.02310\|PD-VLA]] | [[2503.02310v2.pdf]] | — *(no public code)* | — | — | — |  |
| 393 | EAI·B | [[2503.07087\|iManip]] | [[2503.07087v1.pdf]] | — *(no public code)* | — | — | — |  |
| 394 | EAI·B | [[2503.08558\|FAIL-Detect]] | [[2503.08558v3.pdf]] | [`CXU-TRI/FAIL-Detect`](https://github.com/CXU-TRI/FAIL-Detect) | ✓ | 99 MB | ✓ |  |
| 395 | EAI·B | [[2503.15202\|VLM-BT-Failure-Handling]] | [[2503.15202v2.pdf]] | — *(no public code)* | — | — | — |  |
| 396 | EAI·B | [[2503.15386\|CCDP]] | [[2503.15386v3.pdf]] | [`HRI-EU/ccdp`](https://github.com/HRI-EU/ccdp) | ✓ | 142 MB | ✓ |  |
| 397 | EAI·B | [[2503.18684\|OMLA]] | [[2503.18684v2.pdf]] | — *(no public code)* | — | — | — |  |
| 398 | EAI·B | [[2504.15517\|Few-Shot-VLA]] | [[2504.15517v1.pdf]] | — *(no public code)* | — | — | — |  |
| 399 | EAI·B | [[2504.15561\|SPECI]] | [[2504.15561v1.pdf]] | [`Triumphant-strain/SPECI`](https://github.com/Triumphant-strain/SPECI) | ✓ | 697 MB | ✓ |  |
| 400 | EAI·B | [[2505.04769\|VLA-Concepts-Survey]] | [[2505.04769v2.pdf]] | [`Applied-AI-Research-Lab/Vision-Language-Action-Models-Concepts-Progress-Applications-and-Challenges`](https://github.com/Applied-AI-Research-Lab/Vision-Language-Action-Models-Concepts-Progress-Applications-and-Challenges) | ✓ | 22 MB | ✓ | Curated paper list (survey), no method code |
| 401 | EAI·B | [[2505.11711\|RL-Sparse-Subnetwork]] | [[2505.11711v2.pdf]] | [`SagnikMukherjee/sparsity_in_rl`](https://github.com/SagnikMukherjee/sparsity_in_rl) | ✓ | 7.7 MB | ✓ | Sparsity-analysis scripts only, no RL finetuning code |
| 402 | EAI·B | [[2505.11816\|CoSO]] | [[2505.11816v2.pdf]] | [`quinn-ch/CoSO`](https://github.com/quinn-ch/CoSO) | ✓ | 110 MB | ✓ |  |
| 403 | EAI·B | [[2505.12224\|RoboFAC]] | [[2505.12224v4.pdf]] | [`MINT-SJTU/RoboFAC`](https://github.com/MINT-SJTU/RoboFAC) | ✓ | 57 MB | ✓ | Eval + data-gen only, no model training code (model on HF) |
| 404 | EAI·B | [[2505.19017\|WorldEval]] | [[2505.19017v1.pdf]] | [`liyaxuanliyaxuan/Worldeval`](https://github.com/liyaxuanliyaxuan/Worldeval) | ✓ | 139 MB | ✓ |  |
| 405 | EAI·B | [[2505.23705\|Knowledge-Insulation-VLA]] | [[2505.23705v1.pdf]] | [`Physical-Intelligence/openpi`](https://github.com/Physical-Intelligence/openpi) | ✓ | 858 MB | ✓ |  |
| 406 | EAI·B | [[2506.00613\|WorldGym]] | [[2506.00613v3.pdf]] | [`world-model-eval/world-model-eval`](https://github.com/world-model-eval/world-model-eval) | ✓ | 41 MB | ✓ |  |
| 407 | EAI·B | [[2506.06677\|RoboCerebra]] | [[2506.06677v2.pdf]] | [`qiuboxiang/RoboCerebra`](https://github.com/qiuboxiang/RoboCerebra) | ✓ | 696 MB | ✓ |  |
| 408 | EAI·B | [[2506.07530\|BitVLA]] | [[2506.07530v2.pdf]] | [`ustcwhy/BitVLA`](https://github.com/ustcwhy/BitVLA) | ✓ | 1.7 GB | ✓ | pre-training code not yet released |
| 409 | EAI·B | [[2506.09937\|SAFE]] | [[2506.09937v2.pdf]] | [`vla-safe/SAFE`](https://github.com/vla-safe/SAFE) | ✓ | 31 MB | ✓ |  |
| 410 | EAI·B | [[2506.09985\|V-JEPA-2]] | [[2506.09985v1.pdf]] | [`facebookresearch/vjepa2`](https://github.com/facebookresearch/vjepa2) | ✓ | 58 MB | ✓ |  |
| 411 | EAI·B | [[2506.10100\|EfficientVLA]] | [[2506.10100v1.pdf]] | [`YantaiYang-05/EfficientVLA`](https://github.com/YantaiYang-05/EfficientVLA) | ✓ | 3.0 MB | ✓ | README only — code coming soon, not released |
| 412 | EAI·B | [[2506.12723\|SP-VLA]] | [[2506.12723v3.pdf]] | [`ChildTang/SP-VLA`](https://github.com/ChildTang/SP-VLA) | ✓ | 127 MB | ✓ |  |
| 413 | EAI·B | [[2506.13725\|CEED-VLA]] | [[2506.13725v1.pdf]] | [`OpenHelix-Team/CEED-VLA`](https://github.com/OpenHelix-Team/CEED-VLA) | ✓ | 48 MB | ✓ | only training-free version; consistency training & Jacobi code release later |
| 414 | EAI·B | [[2506.17639\|RLRC]] | [[2506.17639v2.pdf]] | — *(no public code)* | — | — | — |  |
| 415 | EAI·B | [[2506.18123\|RoboArena]] | [[2506.18123v2.pdf]] | [`robo-arena/roboarena`](https://github.com/robo-arena/roboarena) | ✓ | 14 MB | ✓ |  |
| 416 | EAI·B | [[2506.21669\|SEEA-R1]] | [[2506.21669v2.pdf]] | [`AurumTian/seea-r1`](https://github.com/AurumTian/seea-r1) | ✓ | 176 MB | ✓ |  |
| 417 | EAI·B | [[2506.21872\|Continual-RL-Survey]] | [[2506.21872v2.pdf]] | — *(no public code)* | — | — | — |  |
| 418 | EAI·B | [[2507.05116\|VOTE]] | [[2507.05116v4.pdf]] | [`LukeLIN-web/VOTE`](https://github.com/LukeLIN-web/VOTE) | ✓ | 51 MB | ✓ |  |
| 419 | EAI·B | [[2507.09177\|Online-Agent-OA]] | [[2507.09177v1.pdf]] | [`sail-sg/ContinualBench`](https://github.com/sail-sg/ContinualBench) | ✓ | 36 MB | ✓ |  |
| 420 | EAI·B | [[2507.14049\|EdgeVLA]] | [[2507.14049v1.pdf]] | [`kscalelabs/evla`](https://github.com/kscalelabs/evla) | ✓ | 45 MB | ✓ | TODO: no LoRA support, no HF export, attention hardcoded |
| 421 | EAI·B | [[2508.07407\|Self-Evolving-AI-Agents-Survey]] | [[2508.07407v2.pdf]] | [`EvoAgentX/Awesome-Self-Evolving-Agents`](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents) | ✓ | 11 MB | ✓ | Curated list (survey), no method code |
| 422 | EAI·B | [[2509.04018\|FPC-VLA]] | [[2509.04018v2.pdf]] | — *(no public code)* | — | — | — |  |
| 423 | EAI·B | [[2509.04259\|RL's-Razor]] | [[2509.04259v1.pdf]] | — *(no public code)* | — | — | — |  |
| 424 | EAI·B | [[2509.09090\|SQAP-VLA]] | [[2509.09090v1.pdf]] | — *(no public code)* | — | — | — |  |
| 425 | EAI·B | [[2509.09372\|VLA-Adapter]] | [[2509.09372v2.pdf]] | [`OpenHelix-Team/VLA-Adapter`](https://github.com/OpenHelix-Team/VLA-Adapter) | ✓ | 172 MB | ✓ |  |
| 426 | EAI·B | [[2509.11480\|VLA-Cross-Platform-Scaling]] | [[2509.11480v2.pdf]] | — *(no public code)* | — | — | — |  |
| 427 | EAI·B | [[2509.18953\|Eva-VLA]] | [[2509.18953v2.pdf]] | — *(no public code)* | — | — | — |  |
| 428 | EAI·B | [[2509.22093\|Action-Aware-VLA-Pruning]] | [[2509.22093v1.pdf]] | [`chen7086/VLA-ADP`](https://github.com/chen7086/VLA-ADP) | ✓ | 123 MB | ✓ | Overlay patch; requires separate OpenVLA-OFT install, no standalone setup |
| 429 | EAI·B | [[2509.22195\|Actions-as-Language]] | [[2509.22195v1.pdf]] | — *(no public code)* | — | — | — |  |
| 430 | EAI·B | [[2510.01642\|FailSafe]] | [[2510.01642v2.pdf]] | [`jimntu/FailSafe_code`](https://github.com/jimntu/FailSafe_code) | ✓ | 703 MB | ✓ |  |
| 431 | EAI·B | [[2510.02298\|ARMADA]] | [[2510.02298v1.pdf]] | [`Virlus/armada`](https://github.com/Virlus/armada) | ✓ | 180 MB | ✓ |  |
| 432 | EAI·B | [[2510.03827\|LIBERO-PRO]] | [[2510.03827v2.pdf]] | [`Zxy-MLlab/LIBERO-PRO`](https://github.com/Zxy-MLlab/LIBERO-PRO) | ✓ | 1.1 GB | ✓ |  |
| 433 | EAI·B | [[2510.04354\|SureSim]] | [[2510.04354v1.pdf]] | [`irom-princeton/rapid-policy-evaluation`](https://github.com/irom-princeton/rapid-policy-evaluation) | ✓ | 713 MB | ✓ |  |
| 434 | EAI·B | [[2510.07077\|VLA-Robotics-Real-World-Review]] | [[2510.07077v1.pdf]] | — *(no public code)* | — | — | — |  |
| 435 | EAI·B | [[2510.09459\|FIPER]] | [[2510.09459v2.pdf]] | [`utiasDSL/fiper`](https://github.com/utiasDSL/fiper) | ✓ | 47 MB | ✓ |  |
| 436 | EAI·B | [[2510.10125\|CTRL-WORLD]] | [[2510.10125v3.pdf]] | [`Robert-gyj/Ctrl-World`](https://github.com/Robert-gyj/Ctrl-World) | ✓ | 190 MB | ✓ |  |
| 437 | EAI·B | [[2510.12710\|Reflective-Self-Adaptation]] | [[2510.12710v3.pdf]] | — *(no public code)* | — | — | — |  |
| 438 | EAI·B | [[2510.20685\|C-Nav]] | [[2510.20685v4.pdf]] | [`BigTree765/C-Nav`](https://github.com/BigTree765/C-Nav) | ✓ | 3.0 MB | ✓ | README only — code not yet released |
| 439 | EAI·B | [[2510.24795\|Efficient-VLA-Survey]] | [[2510.24795v2.pdf]] | [`YuZhaoshu/Efficient-VLAs-Survey`](https://github.com/YuZhaoshu/Efficient-VLAs-Survey) | ✓ | 19 MB | ✓ | Curated list (survey), no method code |
| 440 | EAI·B | [[2510.26742\|Running-VLAs-Real-time]] | [[2510.26742v1.pdf]] | [`Dexmal/realtime-vla`](https://github.com/Dexmal/realtime-vla) | ✓ | 36 MB | ✓ |  |
| 441 | EAI·B | [[2511.04555\|Evo-1]] | [[2511.04555v2.pdf]] | [`MINT-SJTU/Evo-1`](https://github.com/MINT-SJTU/Evo-1) | ✓ | 131 MB | ✓ | RoboTwin eval script and results not yet released |
| 442 | EAI·B | [[2511.15605\|SRPO]] | [[2511.15605v2.pdf]] | [`sii-research/siiRL`](https://github.com/sii-research/siiRL) | ✓ | 124 MB | ✓ |  |
| 443 | EAI·B | [[2511.16166\|EvoVLA]] | [[2511.16166v1.pdf]] | [`AIGeeksGroup/EvoVLA`](https://github.com/AIGeeksGroup/EvoVLA) | ✓ | 447 MB | ✓ |  |
| 444 | EAI·B | [[2511.18085\|Stellar-VLA]] | [[2511.18085v4.pdf]] | — *(no public code)* | — | — | — |  |
| 445 | EAI·B | [[2511.18810\|MergeVLA]] | [[2511.18810v2.pdf]] | [`MergeVLA/MergeVLA`](https://github.com/MergeVLA/MergeVLA) | ✓ | 253 MB | ✓ |  |
| 446 | EAI·B | [[2512.00836\|Counterfactual-Model-Error]] | [[2512.00836v1.pdf]] | [`uncidd/scenario-eval-theory`](https://github.com/uncidd/scenario-eval-theory) | ✓ | 479 MB | ✓ |  |
| 447 | EAI·B | [[2512.02787\|ViFailback]] | [[2512.02787v3.pdf]] | [`x1nyuzhou/ViFailback`](https://github.com/x1nyuzhou/ViFailback) | ✓ | 71 MB | ✓ | Rendering and inference utilities only, no training code |
| 448 | EAI·B | [[2512.04952\|FASTer]] | [[2512.04952v2.pdf]] | — *(no public code)* | — | — | — |  |
| 449 | EAI·B | [[2512.08333\|RETAIN]] | [[2512.08333v3.pdf]] | [`yajatyadav/RETAIN_code`](https://github.com/yajatyadav/RETAIN_code) | ✓ | 832 MB | ✓ |  |
| 450 | EAI·B | [[2512.10675\|Veo-Robotics]] | [[2512.10675v2.pdf]] | — *(no public code)* | — | — | — |  |
| 451 | EAI·B | [[2512.20276\|ActionFlow]] | [[2512.20276v1.pdf]] | — *(no public code)* | — | — | — |  |
| 452 | EAI·B | [[2512.23017\|Merge-before-Forget]] | [[2512.23017v1.pdf]] | — *(no public code)* | — | — | — |  |
| 453 | EAI·B | [[2601.02295\|CycleVLA]] | [[2601.02295v1.pdf]] | — *(no public code)* | — | — | — |  |
| 454 | EAI·B | [[2601.04137\|WoW-World-Eval]] | [[2601.04137v1.pdf]] | — *(no public code)* | — | — | — |  |
| 455 | EAI·B | [[2601.09512\|CLARE]] | [[2601.09512v2.pdf]] | [`tum-lsy/clare`](https://github.com/tum-lsy/clare) | ✓ | 274 MB | ✓ | Project website only, no code |
| 456 | EAI·B | [[2601.14133\|TwinBrainVLA]] | [[2601.14133v2.pdf]] | [`ZGC-EmbodyAI/TwinBrainVLA`](https://github.com/ZGC-EmbodyAI/TwinBrainVLA) | ✓ | 11 MB | ✓ | README only — model code lives in external PhysBrain repo |
| 457 | EAI·B | [[2601.17067\|Video-Generation-as-World-Models-Survey]] | [[2601.17067v1.pdf]] | [`hit-perfect/Awesome-Video-World-Models`](https://github.com/hit-perfect/Awesome-Video-World-Models) | ✓ | 15 MB | ✓ | Curated list (survey), no method code |
| 458 | EAI·B | [[2601.17616\|Split-on-Share]] | [[2601.17616v1.pdf]] | — *(no public code)* | — | — | — |  |
| 459 | EAI·B | [[2602.03445\|CRL-VLA]] | [[2602.03445v1.pdf]] | — *(no public code)* | — | — | — |  |
| 460 | EAI·B | [[2602.03782\|QVLA]] | [[2602.03782v1.pdf]] | [`AutoLab-SAI-SJTU/QVLA`](https://github.com/AutoLab-SAI-SJTU/QVLA) | ✓ | 119 MB | ✓ |  |
| 461 | EAI·B | [[2602.04411\|Self-evolving-Embodied-AI]] | [[2602.04411v1.pdf]] | — *(no public code)* | — | — | — |  |
| 462 | EAI·B | [[2602.06043\|Shared-LoRA-Subspaces]] | [[2602.06043v1.pdf]] | [`ankit-vaidya19/Share`](https://github.com/ankit-vaidya19/Share) | ✓ | 1.1 GB | ✓ |  |
| 463 | EAI·B | [[2602.08025\|MIND-Bench]] | [[2602.08025v2.pdf]] | [`CSU-JPG/MIND`](https://github.com/CSU-JPG/MIND) | ✓ | 73 MB | ✓ | MIND-World training/inference code not yet released (TODO) |
| 464 | EAI·B | [[2602.08971\|WorldArena]] | [[2602.08971v2.pdf]] | [`tsinghua-fib-lab/WorldArena`](https://github.com/tsinghua-fib-lab/WorldArena) | ✓ | 283 MB | ✓ |  |
| 465 | EAI·B | [[2602.10503\|Long-Lived-Robots]] | [[2602.10503v2.pdf]] | — *(no public code)* | — | — | — |  |
| 466 | EAI·B | [[2602.12405\|Self-Refining-VLM-Failure]] | [[2602.12405v1.pdf]] | — *(no public code)* | — | — | — |  |
| 467 | EAI·B | [[2602.13086\|UniManip]] | [[2602.13086v1.pdf]] | — *(no public code)* | — | — | — |  |
| 468 | EAI·B | [[2602.13710\|HBVLA]] | [[2602.13710v1.pdf]] | — *(no public code)* | — | — | — |  |
| 469 | EAI·B | [[2602.16710\|EgoScale]] | [[2602.16710v1.pdf]] | — *(no public code)* | — | — | — |  |
| 470 | EAI·B | [[2602.18397\|VLA-Perf]] | [[2602.18397v1.pdf]] | [`NVlabs/vla-perf`](https://github.com/NVlabs/vla-perf) | ✓ | 49 MB | ✓ |  |
| 471 | EAI·B | [[2602.20057\|AdaWorldPolicy]] | [[2602.20057v1.pdf]] | — *(no public code)* | — | — | — |  |
| 472 | EAI·B | [[2602.20309\|QuantVLA]] | [[2602.20309v4.pdf]] | [`AIoT-MLSys-Lab/QuantVLA`](https://github.com/AIoT-MLSys-Lab/QuantVLA) | ✓ | 92 MB | ✓ |  |
| 473 | EAI·B | [[2602.21198\|Reflective-Test-Time-Planning]] | [[2602.21198v3.pdf]] | [`Reflective-Test-Time-Planning/Reflective-Test-Time-Planning`](https://github.com/Reflective-Test-Time-Planning/Reflective-Test-Time-Planning) | ✓ | 2.3 GB | ✓ |  |
| 474 | EAI·B | [[2602.21531\|LiLo]] | [[2602.21531v1.pdf]] | [`yy-gx/LiLo-VLA`](https://github.com/yy-gx/LiLo-VLA) | ✓ | 79 MB | ✓ | Benchmark only — full LiLo-VLA codebase not yet released |
| 475 | EAI·B | [[2602.21633\|SC-VLA]] | [[2602.21633v1.pdf]] | [`Kisaragi0/SC-VLA`](https://github.com/Kisaragi0/SC-VLA) | ✓ | 63 MB | ✓ |  |
| 476 | EAI·B | [[2602.21919\|Learning-in-the-Null-Space]] | [[2602.21919v1.pdf]] | [`pacman-ctm/NESS`](https://github.com/pacman-ctm/NESS) | ✓ | 37 MB | ✓ |  |
| 477 | EAI·B | [[2602.22579\|VLA-Metamorphic-Testing]] | [[2602.22579v2.pdf]] | [`pablovalle/MT_of_VLAs`](https://github.com/pablovalle/MT_of_VLAs) | ✓ | 35.0 GB | ✓ |  |
| 478 | EAI·B | [[2602.22896\|DySL]] | [[2602.22896v3.pdf]] | [`PKU-SEC-Lab/DYSL_VLA`](https://github.com/PKU-SEC-Lab/DYSL_VLA) | ✓ | 136 MB | ✓ |  |
| 479 | EAI·B | [[2603.00903\|Continual-RL-Theory]] | [[2603.00903v1.pdf]] | [`datake/FAME`](https://github.com/datake/FAME) | ✓ | 50 MB | ✓ |  |
| 480 | EAI·B | [[2603.02224\|Subspace-Geometry-Forgetting]] | [[2603.02224v1.pdf]] | — *(no public code)* | — | — | — |  |
| 481 | EAI·B | [[2603.02951\|CGL]] | [[2603.02951v2.pdf]] | — *(no public code)* | — | — | — |  |
| 482 | EAI·B | [[2603.03380\|LiteVLA]] | [[2603.03380v1.pdf]] | — *(no public code)* | — | — | — |  |
| 483 | EAI·B | [[2603.03818\|VLA-Continual-Learning]] | [[2603.03818v2.pdf]] | [`UT-Austin-RPL/continual-vla`](https://github.com/UT-Austin-RPL/continual-vla) | ✓ | 15 MB | ✓ | Project website only, no code |
| 484 | EAI·B | [[2603.05147\|Act,-Think-or-Abstain]] | [[2603.05147v1.pdf]] | [`AIRLab-POLIMI/ActThinkAbstain`](https://github.com/AIRLab-POLIMI/ActThinkAbstain) | ✓ | 5.4 MB | ✓ | README only — code and dataset released after publication |
| 485 | EAI·B | [[2603.07648\|AtomicVLA]] | [[2603.07648v1.pdf]] | [`zhanglk9/AtomicVLA`](https://github.com/zhanglk9/AtomicVLA) | ✓ | 842 MB | ✓ |  |
| 486 | EAI·B | [[2603.07904\|DyQ]] | [[2603.07904v2.pdf]] | — *(no public code)* | — | — | — |  |
| 487 | EAI·B | [[2603.08763\|SPREAD]] | [[2603.08763v1.pdf]] | — *(no public code)* | — | — | — |  |
| 488 | EAI·B | [[2603.09030\|PlayWorld]] | [[2603.09030v3.pdf]] | — *(no public code)* | — | — | — |  |
| 489 | EAI·B | [[2603.09292\|See-Plan-Rewind]] | [[2603.09292v2.pdf]] | [`TingjunDai/SPRVLA`](https://github.com/TingjunDai/SPRVLA) | ✓ | 741 MB | ✓ |  |
| 490 | EAI·B | [[2603.09298\|CORAL-LoRA-Experts]] | [[2603.09298v1.pdf]] | [`LUOyk1999/CORAL`](https://github.com/LUOyk1999/CORAL) | ✓ | 26 MB | ✓ |  |
| 491 | EAI·B | [[2603.11653\|VLA-RL-Continual-Learning]] | [[2603.11653v2.pdf]] | [`UT-Austin-RobIn/continual-vla-rl`](https://github.com/UT-Austin-RobIn/continual-vla-rl) | ✓ | 2.1 GB | ✓ |  |
| 492 | EAI·B | [[2603.12942\|ReMem-VLA]] | [[2603.12942v1.pdf]] | — *(no public code)* | — | — | — |  |
| 493 | EAI·B | [[2603.13528\|Counterfactual-Failure-Synthesis]] | [[2603.13528v1.pdf]] | — *(no public code)* | — | — | — |  |
| 494 | EAI·B | [[2603.13966\|vla-eval]] | [[2603.13966v2.pdf]] | [`allenai/vla-evaluation-harness`](https://github.com/allenai/vla-evaluation-harness) | ✓ | 79 MB | ✓ |  |
| 495 | EAI·B | [[2603.16195\|S-VAM]] | [[2603.16195v2.pdf]] | [`haodong-yan/S-VAM`](https://github.com/haodong-yan/S-VAM) | ✓ | 81 MB | ✓ | Project website only, no code |
| 496 | EAI·B | [[2603.19131\|Embodied-Efficiency]] | [[2603.19131v1.pdf]] | — *(no public code)* | — | — | — |  |
| 497 | EAI·B | [[2603.19312\|LeWM]] | [[2603.19312v3.pdf]] | [`lucas-maes/le-wm`](https://github.com/lucas-maes/le-wm) | ✓ | 27 MB | ✓ |  |
| 498 | EAI·B | [[2603.22212\|Omni-WorldBench]] | [[2603.22212v1.pdf]] | [`AMAP-ML/Omni-WorldBench`](https://github.com/AMAP-ML/Omni-WorldBench) | ✓ | 33 MB | ✓ | README and assets only — benchmark not yet released |
| 499 | EAI·B | [[2603.23376\|ABot-PhysWorld]] | [[2603.23376v2.pdf]] | [`amap-cvlab/ABot-PhysWorld`](https://github.com/amap-cvlab/ABot-PhysWorld) | ✓ | 305 MB | ✓ |  |
| 500 | EAI·B | [[2603.23497\|WildWorld]] | [[2603.23497v1.pdf]] | [`ShandaAI/WildWorld`](https://github.com/ShandaAI/WildWorld) | ✓ | 9.9 MB | ✓ | README only — dataset and WildBench benchmark not yet released |
| 501 | EAI·B | [[2603.24350\|Emergent-Self]] | [[2603.24350v3.pdf]] | [`adidevj7/emergentrobotself`](https://github.com/adidevj7/emergentrobotself) | ✓ | 665 MB | ✓ |  |
| 502 | EAI·B | [[2603.26666\|VLA-OPD]] | [[2603.26666v1.pdf]] | — *(no public code)* | — | — | — |  |
| 503 | EAI·B | [[2603.28301\|LIBERO-Para]] | [[2603.28301v1.pdf]] | [`cau-hai-lab/LIBERO-Para`](https://github.com/cau-hai-lab/LIBERO-Para) | ✓ | 814 MB | ✓ | benchmark + eval scripts; Pi0.5 eval script pending, training not included |
| 504 | EAI·B | [[2603.28489\|Video-Gen-as-WM-Survey]] | [[2603.28489v2.pdf]] | — *(no public code)* | — | — | — |  |
| 505 | EAI·B | [[2603.28565\|StreamingVLA]] | [[2603.28565v1.pdf]] | — *(no public code)* | — | — | — |  |
| 506 | EAI·B | [[2603.28740\|FocusVLA]] | [[2603.28740v1.pdf]] | — *(no public code)* | — | — | — |  |
| 507 | EAI·B | [[2604.02965\|SV-VLA]] | [[2604.02965v1.pdf]] | [`edsad122/SV-VLA`](https://github.com/edsad122/SV-VLA) | ✓ | 57 MB | ✓ |  |
| 508 | EAI·B | [[2604.04161\|AAC]] | [[2604.04161v2.pdf]] | [`Adaptive-Action-Chunking/gr00t-multi-sample`](https://github.com/Adaptive-Action-Chunking/gr00t-multi-sample) | ✓ | 62 MB | ✓ | server only; sim eval clients in separate repos |
| 509 | EAI·B | [[2604.05498\|JailWAM]] | [[2604.05498v1.pdf]] | — *(no public code)* | — | — | — |  |
| 510 | EAI·B | [[2604.05656\|SnapFlow]] | [[2604.05656v1.pdf]] | — *(no public code)* | — | — | — |  |
| 511 | EAI·B | [[2604.05672\|A1]] | [[2604.05672v3.pdf]] | [`ATeam-Research/A1`](https://github.com/ATeam-Research/A1) | ✓ | 343 MB | ✓ |  |
| 512 | EAI·B | [[2604.11306\|Hierarchical-Episodic-Memory]] | [[2604.11306v2.pdf]] | — *(no public code)* | — | — | — |  |
| 513 | EAI·B | [[2604.18791\|HELM]] | [[2604.18791v1.pdf]] | — *(no public code)* | — | — | — |  |
| 514 | EAI·B | [[2604.21232\|ReCAPA]] | [[2604.21232v2.pdf]] | [`SnSnLi/ReCAPA`](https://github.com/SnSnLi/ReCAPA) | ✓ | 29 MB | ✓ |  |
| 515 | EAI·B | [[2604.21686\|WorldMark]] | [[2604.21686v1.pdf]] | — *(no public code)* | — | — | — |  |
| 516 | EAI·B | [[2604.22152\|dWorldEval]] | [[2604.22152v1.pdf]] | — *(no public code)* | — | — | — |  |
| 517 | EAI·B | [[2604.22748\|Agentic-World-Modeling-Survey]] | [[2604.22748v3.pdf]] | [`matrix-agent/awesome-agentic-world-modeling`](https://github.com/matrix-agent/awesome-agentic-world-modeling) | ✓ | 50 MB | ✓ | Curated paper list (survey), no method code |
| 518 | EAI·B | [[2604.23775\|VLA-Safety-Survey]] | [[2604.23775v1.pdf]] | [`LiQiiiii/Awesome-VLA-Safety`](https://github.com/LiQiiiii/Awesome-VLA-Safety) | ✓ | 18 MB | ✓ | Curated paper list (survey), no method code |
| 519 | EAI·B | [[2605.02739\|Latent-Bridge]] | [[2605.02739v1.pdf]] | [`1999Lyd/Latent-Bridge`](https://github.com/1999Lyd/Latent-Bridge) | ✓ | 31 MB | ✓ |  |
| 520 | EAI·B | [[2605.02900\|Safety-in-Embodied-AI-Survey]] | [[2605.02900v2.pdf]] | [`x-zheng16/Awesome-Embodied-AI-Safety`](https://github.com/x-zheng16/Awesome-Embodied-AI-Safety) | ✓ | 61 MB | ✓ | Curated paper list (survey), no method code |
| 521 | EAI·B | [[2605.06175\|VLA-GSE]] | [[2605.06175v2.pdf]] | [`YuhuaJiang2002/VLA-GSE`](https://github.com/YuhuaJiang2002/VLA-GSE) | ✓ | 62 MB | ✓ |  |
| 522 | EAI·B | [[2605.06311\|VISER]] | [[2605.06311v1.pdf]] | — *(no public code)* | — | — | — |  |
| 523 | EAI·B | [[2605.08434\|AFIL]] | [[2605.08434v2.pdf]] | — *(no public code)* | — | — | — |  |
| 524 | EAI·B | [[2605.08799\|ElasticFlow]] | [[2605.08799v1.pdf]] | — *(no public code)* | — | — | — |  |
| 525 | EAI·B | [[2605.08879\|ConSFT]] | [[2605.08879v2.pdf]] | [`tyzhang2907/ConservativeSFT`](https://github.com/tyzhang2907/ConservativeSFT) | ✓ | 66 MB | ✓ | Only the ConSFT loss file released; no training/eval pipeline |
| 526 | EAI·B | [[2605.09410\|RePO-VLA]] | [[2605.09410v1.pdf]] | — *(no public code)* | — | — | — |  |
| 527 | EAI·B | [[2605.09948\|LoopVLA]] | [[2605.09948v1.pdf]] | — *(no public code)* | — | — | — |  |
| 528 | EAI·B | [[2605.10921\|RoboMemArena]] | [[2605.10921v1.pdf]] | [`OpenHelix-Team/RoboMemArena`](https://github.com/OpenHelix-Team/RoboMemArena) | ✓ | 716 MB | ✓ | Benchmark data, BDDL and eval harness; no training code |
| 529 | EAI·B | [[2605.10993\|ECHO-VLA]] | [[2605.10993v1.pdf]] | — *(no public code)* | — | — | — |  |
| 530 | EAI·B | [[2605.13778\|Realtime-VLA-FLASH]] | [[2605.13778v1.pdf]] | [`dexmal/realtime-vla-flash`](https://github.com/dexmal/realtime-vla-flash) | ✓ | 861 MB | ✓ |  |
| 531 | EAI·B | [[2605.14598\|DSSP]] | [[2605.14598v2.pdf]] | — *(no public code)* | — | — | — |  |
| 532 | EAI·B | [[2605.15735\|UAM]] | [[2605.15735v2.pdf]] | [`CladernyJorn/Unified-Action-Model`](https://github.com/CladernyJorn/Unified-Action-Model) | ✓ | 54 MB | ✓ | README only — code planned for early June 2026 |
| 533 | EAI·B | [[2605.20774\|VLA-REPLICA]] | [[2605.20774v1.pdf]] | [`IRVLUTD/VLAReplica`](https://github.com/IRVLUTD/VLAReplica) | ✓ | 29 MB | ✓ |  |
| 534 | EAI·B | [[2605.21800\|stable-worldmodel]] | [[2605.21800v1.pdf]] | [`galilai-group/stable-worldmodel`](https://github.com/galilai-group/stable-worldmodel) | ✓ | 564 MB | ✓ |  |
| 535 | EAI·B | [[2605.24011\|ActQuant]] | [[2605.24011v2.pdf]] | — *(no public code)* | — | — | — |  |
| 536 | EAI·B | [[2605.25874\|WBench]] | [[2605.25874v1.pdf]] | [`meituan-longcat/WBench`](https://github.com/meituan-longcat/WBench) | ✓ | 785 MB | ✓ |  |
| 537 | EAI·B | [[2605.26820\|VLA-Continual-Forgetting]] | [[2605.26820v1.pdf]] | [`Agentic-Intelligence-Lab/ContinualVLA`](https://github.com/Agentic-Intelligence-Lab/ContinualVLA) | ✓ | 74 MB | ✓ |  |
| 538 | EAI·B | [[2605.27589\|What-If-World]] | [[2605.27589v1.pdf]] | — *(no public code)* | — | — | — |  |
| 539 | EAI·B | [[2605.28527\|VLA-Value-Probing]] | [[2605.28527v1.pdf]] | — *(no public code)* | — | — | — |  |
| 540 | EAI·B | [[2605.28634\|PrimitiveVLA]] | [[2605.28634v1.pdf]] | — *(no public code)* | — | — | — |  |
| 541 | EAI·B | [[2605.29341\|WorldMemArena]] | [[2605.29341v2.pdf]] | [`eric-ai-lab/WorldMemArena`](https://github.com/eric-ai-lab/WorldMemArena) | ✓ | 205 MB | ✓ |  |
| 542 | EAI·B | [[2605.29360\|MiraBench]] | [[2605.29360v1.pdf]] | — *(no public code)* | — | — | — |  |
| 543 | EAI·B | [[2605.29438\|ElegantVLA]] | [[2605.29438v1.pdf]] | — *(no public code)* | — | — | — |  |
| 544 | EAI·B | [[2605.29548\|Capacity-Interference-Retention]] | [[2605.29548v2.pdf]] | — *(no public code)* | — | — | — |  |
| 545 | EAI·B | [[2605.29562\|VLA-Pro]] | [[2605.29562v1.pdf]] | [`ketchup45/VLA-Pro`](https://github.com/ketchup45/VLA-Pro) | ✓ | 64 MB | ✓ |  |
| 546 | EAI·B | [[2605.29710\|PhAIL]] | [[2605.29710v1.pdf]] | [`positronic-robotics/positronic`](https://github.com/positronic-robotics/positronic) | ✓ | 274 MB | ✓ |  |
| 547 | EAI·B | [[2605.30834\|Hide-and-Seek]] | [[2605.30834v1.pdf]] | — *(no public code)* | — | — | — |  |
| 548 | EAI·B | [[2606.02307\|FATE-VLA]] | [[2606.02307v1.pdf]] | [`pablovalle/fate-vla`](https://github.com/pablovalle/fate-vla) | ✗ | — | — |  |
| 549 | EAI·B | [[2606.03374\|eMEM]] | [[2606.03374v1.pdf]] | [`automatikarobotics/emem`](https://github.com/automatikarobotics/emem) | ✗ | — | — |  |
| 550 | EAI·B | [[2606.03385\|GTP-FA]] | [[2606.03385v1.pdf]] | — *(no public code)* | — | — | — |  |
| 551 | EAI·B | [[2606.03556\|VLA-Patch-Attack]] | [[2606.03556v1.pdf]] | — *(no public code)* | — | — | — |  |
| 552 | EAI·B | [[2606.03598\|PHASER]] | [[2606.03598v2.pdf]] | — *(no public code)* | — | — | — |  |
| 553 | EAI·B | [[2606.04233\|Manipulation-Benchmark-Audit]] | [[2606.04233v1.pdf]] | [`ripl/manipulation_benchmark_audit`](https://github.com/ripl/manipulation_benchmark_audit) | ✓ | 7.4 MB | ✓ | Project website only, no code |
| 554 | EAI·B | [[2606.04463\|OSCAR]] | [[2606.04463v2.pdf]] | [`wuzy2115/oscar-public`](https://github.com/wuzy2115/oscar-public) | ✓ | 102 MB | ✓ |  |
| 555 | EAI·B | [[2606.05159\|X4Val]] | [[2606.05159v1.pdf]] | — *(no public code)* | — | — | — |  |
| 556 | EAI·B | [[2606.05395\|VASO]] | [[2606.05395v1.pdf]] | — *(no public code)* | — | — | — |  |
| 557 | EAI·B | [[2606.05737\|One-Step-VLA]] | [[2606.05737v1.pdf]] | — *(no public code)* | — | — | — |  |
| 558 | EAI·B | [[2606.05773\|PiL-World]] | [[2606.05773v1.pdf]] | — *(no public code)* | — | — | — |  |
| 559 | EAI·B | [[2606.07383\|RhinoVLA-Technical-Report]] | [[2606.07383v1.pdf]] | [`HuixiAI/RhinoVLA`](https://github.com/HuixiAI/RhinoVLA) | ✓ | 87 MB | ✓ | README only — code/weights/data not yet released |
| 560 | EAI·B | [[2606.09572\|CT-VAM]] | [[2606.09572v1.pdf]] | — *(no public code)* | — | — | — |  |
| 561 | EAI·B | [[2606.09630\|ReCoVLA]] | [[2606.09630v1.pdf]] | — *(no public code)* | — | — | — |  |
| 562 | EAI·B | [[2606.09827\|MemoryVLA++]] | [[2606.09827v1.pdf]] | [`shihao1895/MemoryVLA`](https://github.com/shihao1895/MemoryVLA) | ✓ | 208 MB | ✓ |  |
| 563 | EAI·B | [[2606.12105\|DAM-VLA]] | [[2606.12105v1.pdf]] | — *(no public code)* | — | — | — |  |
| 564 | EAI·B | [[2606.12372\|UniIntervene]] | [[2606.12372v1.pdf]] | — *(no public code)* | — | — | — |  |
| 565 | EAI·B | [[2606.15685\|SCE]] | [[2606.15685v1.pdf]] | — *(no public code)* | — | — | — |  |
| 566 | EAI·B | [[2606.17493\|Sleeping-Robots]] | [[2606.17493v1.pdf]] | — *(no public code)* | — | — | — |  |
| 567 | EAI·B | [[2606.18610\|SC3-Eval]] | [[2606.18610v1.pdf]] | — *(no public code)* | — | — | — |  |
| 568 | WAM·A | [[2605.23856\|JOPAT]] | [[2605.23856v1.pdf]] | — *(no public code)* | — | — | — | added 2026-07-12; WAM·A predict anchor (structured-target beats pixels) |
| 569 | WAM·A | [[2607.08436\|EgoWAM]] | [[2607.08436v1.pdf]] | — *(project page, code coming soon)* | — | — | — | added 2026-07-12; WAM·A predict anchor (auxiliary WM head) |
| 570 | EAI·B | [[2607.05966\|iKCE]] | [[2607.05966v1.pdf]] | — *(no public code)* | — | — | — | added 2026-07-12; dynamics-blindness diagnostic (evidence for the predict bet) |
| 571 | EAI·B | [[2607.02403\|ACID]] | [[2607.02403v1.pdf]] | — *(project page, code coming soon)* | — | — | — | added 2026-07-12; verify build-on (inverse-dynamics consistency) |
| 572 | S2R·B | [[2606.28476\|FADA]] | [[2606.28476v1.pdf]] | — *(project page only)* | — | — | — | added 2026-07-12; ground foil (model-free humanoid dynamics adaptation) |
| 573 | S2R·B | [[2607.02205\|Actuator Reality Shaping]] | [[2607.02205v2.pdf]] | — *(project page only)* | — | — | — | added 2026-07-12; ground foil (actuator counter-philosophy) |
| 574 | WAM·A | [[2607.02503\|VT-WAM]] | [[2607.02503v1.pdf]] | — *(project page, code coming soon)* | — | — | — | added 2026-07-12; contact-WAM anchor for WrenchCast |
| 575 | WAM·A | [[2606.30988\|MuSe]] | [[2606.30988v3.pdf]] | [`jadenvc/multisensory_wm`](https://github.com/jadenvc/multisensory_wm) | ✗ | — | — | placeholder repo, code to be released; added 2026-07-12; anticipatory force-torque prediction |
| 576 | WB·C | [[2607.02332\|HEFT]] | [[2607.02332v1.pdf]] | — *(project page only)* | — | — | — | added 2026-07-12; force-under-load foil (heavy-payload reactive) |
| 577 | WB·C | [[2606.10818\|IMPACT]] | [[2606.10818v1.pdf]] | [`Winston-Gu/IMPACT`](https://github.com/Winston-Gu/IMPACT) | ✗ | — | — | added 2026-07-12; sensorless-feedforward force-under-load foil (WB·C1); not yet cloned |
| 578 | WAM·A | [[2606.08555\|FAWAM]] | [[2606.08555v2.pdf]] | [`HaotianHehaha/FAWAM`](https://github.com/HaotianHehaha/FAWAM) | ✗ | — | — | added 2026-07-12; force-WAM baseline for WrenchCast; not yet cloned (residual-correction code being organized) |
| 579 | S2R·B | [[2606.09640\|Physics-Aware-Sparse-EL]] | [[2606.09640v1.pdf]] | — *(no public code)* | — | — | — | added 2026-07-12; structure-preserving sysID ground anchor |
| 580 | S2R·B | [[2607.06824\|CaLiSym]] | [[2607.06824v1.pdf]] | — *(no public code)* | — | — | — | added 2026-07-12; symplectic-dynamics ground foil |
| 581 | WAM·A | [[2607.05468\|MECo-WAM]] | [[2607.05468v1.pdf]] | — *(no public code)* | — | — | — | added 2026-07-12; discardable-teacher predict precedent |

## Known gaps

**Repo found but clone failed** — the official repo URL was confirmed, but cloning it did not complete (timeout / size / access). Re-clone manually if needed.

- [[2606.02307]] — [`pablovalle/fate-vla`](https://github.com/pablovalle/fate-vla)
- [[2606.03374]] — [`automatikarobotics/emem`](https://github.com/automatikarobotics/emem)

**Cloned but GitNexus-index failed** — GitNexus's native parser crashes on these (`Napi::Error`) — a tool-side bug, not a clone problem; the repos are cloned and usable, just not (fully) graphed. **8 repos** across two cases:

*No index (crashes from scratch):*

- [[2503.12609]] — [`YitianShi/vMF-Contact`](https://github.com/YitianShi/vMF-Contact)
- [[2204.03139]] — [`priyasundaresan/diffcloud_real2sim`](https://github.com/priyasundaresan/diffcloud_real2sim)
- [[2407.07889]] — [`Boey-li/AdaptiGraph`](https://github.com/Boey-li/AdaptiGraph)

*Stale/partial index — indexed fine originally, but re-indexing after the submodule code-pull crashes, so the graph covers only the original (non-submodule) code:*

- [[2305.04866]] — [`JiahengHu/CausalMoMa`](https://github.com/JiahengHu/CausalMoMa)
- [[2606.05160]] — [`NVlabs/GRAIL`](https://github.com/NVlabs/GRAIL)
- [[2507.04140]] — [`hojae-io/LearningHumanoidArmMotion-RAL2025-Code`](https://github.com/hojae-io/LearningHumanoidArmMotion-RAL2025-Code)
- [[2509.20297]] — [`nvidia-isaac/nvblox_mindmap`](https://github.com/nvidia-isaac/nvblox_mindmap)
- [[2603.22039]] — [`generalroboticslab/RAFL`](https://github.com/generalroboticslab/RAFL)

*Parse-timeout — too large/complex for the parser to finish (distinct from the crashes above; cloned and usable, just not graphed):*

- [[2511.06385]] — [`JulianBalletshofer/pacs-ros2`](https://github.com/JulianBalletshofer/pacs-ros2) — 488 MB ROS2 tree, parser idle-timeouts even at 5 min

## Cross-references

- [[Focus-Direction]] — the research program these papers serve.
- Source clusters: [[Whole-Body]] · [[WAM]] · [[Sim2Real]] · [[Embodied-AI]].
- PDFs: `data/papers/` · Repos: `data/.repositories/`.
