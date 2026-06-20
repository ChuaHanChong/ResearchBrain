---
title: "Focus-Direction Repo Map: Papers ↔ Code Repositories"
aliases:
  - "Focus-Direction Repo Map"
  - "Paper-Repo Map"
tags:
  - embodied-AI
  - index
---
# Focus-Direction Repo Map: Papers ↔ Code Repositories

> [!abstract] What this is
> A KnowledgeHub ↔ PDF ↔ GitHub map for the **344 papers** across the **18 core directions** of [[Focus-Direction]] (5 source clusters: Whole-Body A+B, WAM·A, Sim2Real·B, Embodied-AI·B). **226** papers have a confirmed official repo; **224** are cloned into `data/.repositories/`. The remaining **118** released no public code.
>
> Repos were resolved per-paper (PDF page-1 footnote → alphaxiv paper-content → web), each validated to exist and filtered to reject dependency/baseline repos. KnowledgeHub notes themselves carry no code links.

> [!info] Columns
> **Cluster(s)** = which source clusters cite the paper · **KH** = KnowledgeHub note · **PDF** = local file in `data/papers/` · **Repo** = official GitHub (clickable) · **Cloned** = ✓ in `data/.repositories/` · ✗ resolve-OK-but-clone-failed · — no public code · **Size** = on-disk size of the full clone (complete history; Git-LFS blobs skipped) · **Indexed** = ✓ has a gitnexus code-graph index (`.gitnexus/`, queryable via the gitnexus MCP) · ✗ cloned but not indexed.

**Totals** — papers 344 · with repo 226 · cloned 224 · clone-failed 2 · no public code 118 · cloned size 95.3 GB · gitnexus-indexed 220. Resolution confidence: high 216 · medium 10 · none 118.

| # | Cluster(s) | KH | PDF | Repo | Cloned | Size | Indexed |
|---:|---|---|---|---|:--:|--:|:--:|
| 1 | WB·A | [[2403.10506\|HumanoidBench]] | [[2403.10506v2.pdf]] | [`carlosferrazza/humanoid-bench`](https://github.com/carlosferrazza/humanoid-bench) | ✓ | 464 MB | ✓ |
| 2 | WB·A | [[2405.18418\|Puppeteer]] | [[2405.18418v3.pdf]] | [`nicklashansen/puppeteer`](https://github.com/nicklashansen/puppeteer) | ✓ | 29 MB | ✓ |
| 3 | WB·A | [[2407.10353\|UMI-on-Legs]] | [[2407.10353v1.pdf]] | [`real-stanford/umi-on-legs`](https://github.com/real-stanford/umi-on-legs) | ✓ | 178 MB | ✓ |
| 4 | WB·A | [[2408.00342\|MuJoCo MPC HumanoidBench]] | [[2408.00342v1.pdf]] | [`google-deepmind/mujoco_mpc`](https://github.com/google-deepmind/mujoco_mpc) | ✓ | 106 MB | ✓ |
| 5 | WB·A | [[2409.16048\|WB-EE Pose Tracking]] | [[2409.16048v2.pdf]] | — *(no public code)* | — | — | — |
| 6 | WB·A | [[2412.03012\|Omni WBLM]] | [[2412.03012v2.pdf]] | — *(no public code)* | — | — | — |
| 7 | WB·A | [[2502.14795\|Humanoid-VLA]] | [[2502.14795v2.pdf]] | — *(no public code)* | — | — | — |
| 8 | WB·A WB·B | [[2503.05652\|BRS]] | [[2503.05652v2.pdf]] | [`behavior-robot-suite/brs-algo`](https://github.com/behavior-robot-suite/brs-algo) | ✓ | 138 MB | ✓ |
| 9 | WB·A | [[2504.11054\|Meta Motivo]] | [[2504.11054v1.pdf]] | [`facebookresearch/metamotivo`](https://github.com/facebookresearch/metamotivo) | ✓ | 27 MB | ✓ |
| 10 | WB·A WB·B | [[2504.16054\|π0.5]] | [[2504.16054v1.pdf]] | [`Physical-Intelligence/openpi`](https://github.com/Physical-Intelligence/openpi) | ✓ | 79 MB | ✓ |
| 11 | WB·A | [[2505.06776\|FALCON (Loco-Manipulation)]] | [[2505.06776v2.pdf]] | [`LeCAR-Lab/FALCON`](https://github.com/LeCAR-Lab/FALCON) | ✓ | 363 MB | ✓ |
| 12 | WB·A | [[2506.09366\|SkillBlender]] | [[2506.09366v1.pdf]] | [`Humanoid-SkillBlender/SkillBlender`](https://github.com/Humanoid-SkillBlender/SkillBlender) | ✓ | 274 MB | ✓ |
| 13 | WB·A | [[2506.12779\|Experts-to-Generalist]] | [[2506.12779v3.pdf]] | [`BeingBeyond/BumbleBee`](https://github.com/BeingBeyond/BumbleBee) | ✓ | 381 MB | ✓ |
| 14 | WB·A | [[2506.12851\|KungfuBot]] | [[2506.12851v2.pdf]] | [`TeleHuman/PBHC`](https://github.com/TeleHuman/PBHC) | ✓ | 257 MB | ✓ |
| 15 | WB·A | [[2506.13751\|LeVERB]] | [[2506.13751v3.pdf]] | — *(no public code)* | — | — | — |
| 16 | WB·A | [[2507.04140\|Centroidal Arm Motion]] | [[2507.04140v1.pdf]] | [`hojae-io/LearningHumanoidArmMotion-RAL2025-Code`](https://github.com/hojae-io/LearningHumanoidArmMotion-RAL2025-Code) | ✓ | 216 MB | ✓ |
| 17 | WB·A | [[2507.06905\|ULC]] | [[2507.06905v2.pdf]] | [`Hellod035/ULC`](https://github.com/Hellod035/ULC) | ✓ | 272 MB | ✓ |
| 18 | WB·A | [[2507.08656\|Multi-Critic Twist Tracking]] | [[2507.08656v2.pdf]] | — *(no public code)* | — | — | — |
| 19 | WB·A | [[2508.16943\|LHM-Humanoid]] | [[2508.16943v2.pdf]] | — *(no public code)* | — | — | — |
| 20 | WB·A | [[2509.21231\|SEEC]] | [[2509.21231v1.pdf]] | — *(no public code)* | — | — | — |
| 21 | WB·A | [[2511.05936\|10 VLA Challenges]] | [[2511.05936v1.pdf]] | — *(no public code)* | — | — | — |
| 22 | WB·A | [[2511.15200\|VIRAL]] | [[2511.15200v2.pdf]] | [`NVlabs/GR00T-VisualSim2Real`](https://github.com/NVlabs/GR00T-VisualSim2Real) | ✓ | 75 MB | ✓ |
| 23 | WB·A | [[2511.21169\|Kinematics-Aware Multi-Policy]] | [[2511.21169v1.pdf]] | — *(no public code)* | — | — | — |
| 24 | WB·A | [[2512.11047\|WholeBodyVLA]] | [[2512.11047v2.pdf]] | [`opendrivelab/WholeBodyVLA`](https://github.com/opendrivelab/WholeBodyVLA) | ✓ | 78 MB | ✓ |
| 25 | WB·A | [[2512.13093\|PvP]] | [[2512.13093v2.pdf]] | [`myismyname/SRL4Humanoid`](https://github.com/myismyname/SRL4Humanoid) | ✓ | 66 MB | ✓ |
| 26 | WB·A EAI·B | [[2512.20188\|Fast-Slow WB VLA]] | [[2512.20188v1.pdf]] | — *(no public code)* | — | — | — |
| 27 | WB·A | [[2601.17440\|PILOT]] | [[2601.17440v1.pdf]] | — *(no public code)* | — | — | — |
| 28 | WB·A | [[2602.06341\|HiWET]] | [[2602.06341v1.pdf]] | — *(no public code)* | — | — | — |
| 29 | WB·A | [[2602.13850\|Humanoid Hanoi]] | [[2602.13850v3.pdf]] | [`osudrl/Humanoid_Hanoi`](https://github.com/osudrl/Humanoid_Hanoi) | ✓ | 591 MB | ✓ |
| 30 | WB·A | [[2602.16705\|HERO (Humanoid EE Control)]] | [[2602.16705v3.pdf]] | — *(no public code)* | — | — | — |
| 31 | WB·A | [[2603.02443\|Safe WBLM]] | [[2603.02443v1.pdf]] | — *(no public code)* | — | — | — |
| 32 | WB·A | [[2603.03279\|ULTRA]] | [[2603.03279v1.pdf]] | — *(no public code)* | — | — | — |
| 33 | WB·A | [[2603.05410\|PhysiFlow]] | [[2603.05410v1.pdf]] | — *(no public code)* | — | — | — |
| 34 | WB·A | [[2603.08572\|MetaWorld-X]] | [[2603.08572v1.pdf]] | — *(no public code)* | — | — | — |
| 35 | WB·A | [[2603.08961\|FAME]] | [[2603.08961v1.pdf]] | [`correlllab/h12_adaptive_policy`](https://github.com/correlllab/h12_adaptive_policy) | ✓ | 260 MB | ✓ |
| 36 | WB·A | [[2603.10675\|Cybo-Waiter]] | [[2603.10675v1.pdf]] | — *(no public code)* | — | — | — |
| 37 | WB·A | [[2603.12263\|Psi0]] | [[2603.12263v1.pdf]] | [`physical-superintelligence-lab/Psi0`](https://github.com/physical-superintelligence-lab/Psi0) | ✓ | 643 MB | ✓ |
| 38 | WB·A | [[2603.20147\|AGILE]] | [[2603.20147v1.pdf]] | [`nvidia-isaac/WBC-AGILE`](https://github.com/nvidia-isaac/WBC-AGILE) | ✓ | 84 MB | ✓ |
| 39 | WB·A | [[2604.00202\|DreamControl-v2]] | [[2604.00202v1.pdf]] | — *(no public code)* | — | — | — |
| 40 | WB·A | [[2604.01158\|SMASH]] | [[2604.01158v1.pdf]] | — *(no public code)* | — | — | — |
| 41 | WB·A | [[2604.07457\|CMP]] | [[2604.07457v1.pdf]] | [`Shepherd1226/CMP`](https://github.com/Shepherd1226/CMP) | ✓ | 3.2 MB | ✓ |
| 42 | WB·A | [[2604.07993\|HEX]] | [[2604.07993v2.pdf]] | [`Open-X-Humanoid/HEX`](https://github.com/Open-X-Humanoid/HEX) | ✓ | 73 MB | ✓ |
| 43 | WB·A | [[2604.11251\|CLAW]] | [[2604.11251v3.pdf]] | [`JianuoCao/CLAW`](https://github.com/JianuoCao/CLAW) | ✓ | 334 MB | ✓ |
| 44 | WB·A | [[2604.24833\|MotionBricks]] | [[2604.24833v1.pdf]] | [`NVlabs/GR00T-WholeBodyControl`](https://github.com/NVlabs/GR00T-WholeBodyControl) | ✓ | 1.2 GB | ✓ |
| 45 | WB·A | [[2605.14417\|DAJI]] | [[2605.14417v2.pdf]] | [`Hxxxz0/DAJI`](https://github.com/Hxxxz0/DAJI) | ✓ | 3.2 MB | ✓ |
| 46 | WB·A WB·B | [[2605.21133\|Spatial Brain Cerebellum]] | [[2605.21133v1.pdf]] | — *(no public code)* | — | — | — |
| 47 | WB·A | [[2606.03536\|Bionic Whole-Body Control]] | [[2606.03536v1.pdf]] | — *(no public code)* | — | — | — |
| 48 | WB·A | [[2606.06139\|MotionDisco]] | [[2606.06139v1.pdf]] | — *(no public code)* | — | — | — |
| 49 | WB·A | [[2606.06493\|HANDOFF]] | [[2606.06493v3.pdf]] | [`lzyang2000/HANDOFF`](https://github.com/lzyang2000/HANDOFF) | ✓ | 221 MB | ✓ |
| 50 | WB·A | [[2606.09215\|MotionWAM]] | [[2606.09215v1.pdf]] | — *(no public code)* | — | — | — |
| 51 | WB·A | [[2606.10340\|OMG]] | [[2606.10340v1.pdf]] | [`Tsinghua-MARS-Lab/OMG`](https://github.com/Tsinghua-MARS-Lab/OMG) | ✓ | 106 MB | ✓ |
| 52 | WB·B | [[2305.04866\|Causal WBMM]] | [[2305.04866v4.pdf]] | [`JiahengHu/CausalMoMa`](https://github.com/JiahengHu/CausalMoMa) | ✓ | 25 MB | ✓ |
| 53 | WB·B | [[2306.11565\|HomeRobot]] | [[2306.11565v2.pdf]] | [`facebookresearch/home-robot`](https://github.com/facebookresearch/home-robot) | ✓ | 460 MB | ✓ |
| 54 | WB·B | [[2310.00433\|ActPerMoMa]] | [[2310.00433v2.pdf]] | [`pearl-robot-lab/ActPerMoMa`](https://github.com/pearl-robot-lab/ActPerMoMa) | ✓ | 146 MB | ✓ |
| 55 | WB·B | [[2401.02117\|Mobile ALOHA]] | [[2401.02117v1.pdf]] | [`MarkFzp/mobile-aloha`](https://github.com/MarkFzp/mobile-aloha) | ✓ | 28 MB | ✓ |
| 56 | WB·B | [[2407.07788\|BiGym]] | [[2407.07788v2.pdf]] | [`chernyadev/bigym`](https://github.com/chernyadev/bigym) | ✓ | 275 MB | ✓ |
| 57 | WB·B | [[2410.11989\|DovSG]] | [[2410.11989v6.pdf]] | [`BJHYZJ/DovSG`](https://github.com/BJHYZJ/DovSG) | ✓ | 124 MB | ✓ |
| 58 | WB·B | [[2410.18964\|DISaM]] | [[2410.18964v1.pdf]] | [`UT-Austin-RobIn/l2l`](https://github.com/UT-Austin-RobIn/l2l) | ✓ | 61 MB | ✓ |
| 59 | WB·B | [[2411.04999\|DynaMem]] | [[2411.04999v2.pdf]] | [`hello-robot/stretch_ai`](https://github.com/hello-robot/stretch_ai) | ✓ | 134 MB | ✓ |
| 60 | WB·B | [[2412.13211\|MS-HAB]] | [[2412.13211v3.pdf]] | [`arth-shukla/mshab`](https://github.com/arth-shukla/mshab) | ✓ | 220 MB | ✓ |
| 61 | WB·B | [[2506.01185\|HoMeR]] | [[2506.01185v2.pdf]] | [`priyasundaresan/homer`](https://github.com/priyasundaresan/homer) | ✓ | 373 MB | ✓ |
| 62 | WB·B | [[2506.15666\|Vision-in-Action]] | [[2506.15666v1.pdf]] | [`haoyu-x/vision-in-action`](https://github.com/haoyu-x/vision-in-action) | ✓ | 745 MB | ✓ |
| 63 | WB·B | [[2507.01961\|AC-DiT]] | [[2507.01961v3.pdf]] | [`PKU-HMI-Lab/AC-DiT`](https://github.com/PKU-HMI-Lab/AC-DiT) | ✓ | 636 MB | ✓ |
| 64 | WB·B | [[2509.20297\|mindmap]] | [[2509.20297v3.pdf]] | [`nvidia-isaac/nvblox_mindmap`](https://github.com/nvidia-isaac/nvblox_mindmap) | ✓ | 119 MB | ✓ |
| 65 | WB·B | [[2510.01607\|ActiveUMI]] | [[2510.01607v1.pdf]] | — *(no public code)* | — | — | — |
| 66 | WB·B | [[2510.03885\|3D Latent Mapping]] | [[2510.03885v3.pdf]] | [`ExistentialRobotics/SBP`](https://github.com/ExistentialRobotics/SBP) | ✓ | 408 MB | ✓ |
| 67 | WB·B | [[2511.00153\|EgoMI]] | [[2511.00153v2.pdf]] | — *(no public code)* | — | — | — |
| 68 | WB·B | [[2511.18112\|EchoVLA]] | [[2511.18112v2.pdf]] | — *(no public code)* | — | — | — |
| 69 | WB·B | [[2512.24653\|RoboMIND 2.0]] | [[2512.24653v3.pdf]] | [`Open-X-Humanoid/RoboMIND-Sim`](https://github.com/Open-X-Humanoid/RoboMIND-Sim) | ✓ | 120 MB | ✓ |
| 70 | WB·B | [[2602.01939\|EFM-10]] | [[2602.01939v3.pdf]] | — *(no public code)* | — | — | — |
| 71 | WB·B | [[2602.04600\|Act-Sense-Act]] | [[2602.04600v1.pdf]] | — *(no public code)* | — | — | — |
| 72 | WB·B | [[2602.22461\|EgoAVFlow]] | [[2602.22461v1.pdf]] | — *(no public code)* | — | — | — |
| 73 | WB·B | [[2602.23024\|InCoM]] | [[2602.23024v4.pdf]] | — *(no public code)* | — | — | — |
| 74 | WB·B | [[2603.03243\|HoMMI]] | [[2603.03243v2.pdf]] | [`xxm19/hommi`](https://github.com/xxm19/hommi) | ✓ | 64 MB | ✓ |
| 75 | WB·B EAI·B | [[2603.04639\|RoboMME]] | [[2603.04639v3.pdf]] | [`RoboMME/robomme_policy_learning`](https://github.com/RoboMME/robomme_policy_learning) | ✓ | 71 MB | ✓ |
| 76 | WB·B | [[2603.18494\|MemoAct]] | [[2603.18494v1.pdf]] | — *(no public code)* | — | — | — |
| 77 | WB·B | [[2604.08534\|ActiveGlasses]] | [[2604.08534v1.pdf]] | — *(no public code)* | — | — | — |
| 78 | WB·B | [[2605.02487\|Visibility-Aware Mobile Grasping]] | [[2605.02487v3.pdf]] | [`AdaCompNUS/Visibility-Awared-Mobile-Grasping`](https://github.com/AdaCompNUS/Visibility-Awared-Mobile-Grasping) | ✓ | 303 MB | ✓ |
| 79 | WB·B | [[2605.07943\|TAVIS]] | [[2605.07943v1.pdf]] | [`spiglerg/tavis`](https://github.com/spiglerg/tavis) | ✓ | 44 MB | ✓ |
| 80 | WB·B | [[2606.12956\|SERF]] | [[2606.12956v1.pdf]] | — *(no public code)* | — | — | — |
| 81 | WAM·A S2R·B EAI·B | [[2304.07193\|DINOv2]] | [[2304.07193v2.pdf]] | [`facebookresearch/dinov2`](https://github.com/facebookresearch/dinov2) | ✓ | 62 MB | ✓ |
| 82 | WAM·A EAI·B | [[2306.03310\|LIBERO]] | [[2306.03310v2.pdf]] | [`Lifelong-Robot-Learning/LIBERO`](https://github.com/Lifelong-Robot-Learning/LIBERO) | ✓ | 795 MB | ✓ |
| 83 | WAM·A S2R·B | [[2402.08191\|THE COLOSSEUM]] | [[2402.08191v2.pdf]] | [`robot-colosseum/robot-colosseum`](https://github.com/robot-colosseum/robot-colosseum) | ✓ | 670 MB | ✓ |
| 84 | WAM·A | [[2409.18330\|DMC-VB]] | [[2409.18330v1.pdf]] | [`google-deepmind/dmc_vision_benchmark`](https://github.com/google-deepmind/dmc_vision_benchmark) | ✓ | 613 MB | ✓ |
| 85 | WAM·A | [[2410.24090\|Sparsh]] | [[2410.24090v1.pdf]] | [`facebookresearch/sparsh`](https://github.com/facebookresearch/sparsh) | ✓ | 151 MB | ✓ |
| 86 | WAM·A EAI·B | [[2411.04983\|DINO-WM]] | [[2411.04983v2.pdf]] | [`gaoyuezhou/dino_wm`](https://github.com/gaoyuezhou/dino_wm) | ✓ | 50 MB | ✓ |
| 87 | WAM·A | [[2411.12503\|ManiSkill-ViTac 2025]] | [[2411.12503v1.pdf]] | [`cyliizyz/ManiSkill-ViTac2025`](https://github.com/cyliizyz/ManiSkill-ViTac2025) | ✓ | 77 MB | ✓ |
| 88 | WAM·A | [[2412.14803\|VPP]] | [[2412.14803v2.pdf]] | [`roboterax/video-prediction-policy`](https://github.com/roboterax/video-prediction-policy) | ✓ | 76 MB | ✓ |
| 89 | WAM·A | [[2412.15109\|Seer]] | [[2412.15109v1.pdf]] | [`OpenRobotLab/Seer`](https://github.com/OpenRobotLab/Seer) | ✓ | 61 MB | ✓ |
| 90 | WAM·A | [[2503.00200\|UVA]] | [[2503.00200v3.pdf]] | [`ShuangLI59/unified_video_action`](https://github.com/ShuangLI59/unified_video_action) | ✓ | 301 MB | ✓ |
| 91 | WAM·A | [[2504.02792\|UWM]] | [[2504.02792v3.pdf]] | [`WEIRDLabUW/unified-world-model`](https://github.com/WEIRDLabUW/unified-world-model) | ✓ | 33 MB | ✓ |
| 92 | WAM·A EAI·B | [[2504.13059\|RoboTwin]] | [[2504.13059v1.pdf]] | [`agilexrobotics/RoboTwin`](https://github.com/agilexrobotics/RoboTwin) | ✓ | 43 MB | ✓ |
| 93 | WAM·A | [[2505.11528\|LaDi-WM]] | [[2505.11528v6.pdf]] | [`GuHuangAI/LaDiWM`](https://github.com/GuHuangAI/LaDiWM) | ✓ | 1.5 GB | ✓ |
| 94 | WAM·A | [[2505.18472\|ManiFeel]] | [[2505.18472v2.pdf]] | [`purdue-mars/manifeel`](https://github.com/purdue-mars/manifeel) | ✓ | 238 MB | ✓ |
| 95 | WAM·A | [[2505.19386\|Force Prompting]] | [[2505.19386v2.pdf]] | [`brown-palm/force-prompting`](https://github.com/brown-palm/force-prompting) | ✓ | 409 MB | ✓ |
| 96 | WAM·A | [[2506.14754\|Sparsh-X]] | [[2506.14754v1.pdf]] | [`facebookresearch/sparsh-multisensory-touch`](https://github.com/facebookresearch/sparsh-multisensory-touch) | ✓ | 149 MB | ✓ |
| 97 | WAM·A | [[2508.10104\|DINOv3]] | [[2508.10104v1.pdf]] | [`facebookresearch/dinov3`](https://github.com/facebookresearch/dinov3) | ✓ | 96 MB | ✓ |
| 98 | WAM·A | [[2508.17600\|GWM]] | [[2508.17600v2.pdf]] | [`Gaussian-World-Model/gaussianwm`](https://github.com/Gaussian-World-Model/gaussianwm) | ✓ | 41 MB | ✓ |
| 99 | WAM·A | [[2509.07962\|TA-VLA]] | [[2509.07962v1.pdf]] | [`ZZongzheng0918/TA-VLA`](https://github.com/ZZongzheng0918/TA-VLA) | ✓ | 44 MB | ✓ |
| 100 | WAM·A | [[2509.21797\|MoWM]] | [[2509.21797v3.pdf]] | [`tsinghua-fib-lab/MoWM`](https://github.com/tsinghua-fib-lab/MoWM) | ✓ | 15 MB | ✓ |
| 101 | WAM·A EAI·B | [[2510.13626\|LIBERO-Plus]] | [[2510.13626v3.pdf]] | [`sylvestf/LIBERO-plus`](https://github.com/sylvestf/LIBERO-plus) | ✓ | 594 MB | ✓ |
| 102 | WAM·A | [[2510.16732\|World Models for Embodied AI Survey]] | [[2510.16732v2.pdf]] | [`Li-Zn-H/AwesomeWorldModels`](https://github.com/Li-Zn-H/AwesomeWorldModels) | ✓ | 16 MB | ✓ |
| 103 | WAM·A | [[2511.02097\|WM Manipulation Survey]] | [[2511.02097v2.pdf]] | — *(no public code)* | — | — | — |
| 104 | WAM·A | [[2511.08544\|LeJEPA]] | [[2511.08544v3.pdf]] | [`rbalestr-lab/lejepa`](https://github.com/rbalestr-lab/lejepa) | ✓ | 42 MB | ✓ |
| 105 | WAM·A | [[2512.15692\|mimic-video]] | [[2512.15692v2.pdf]] | [`mimic-video/mimic-video`](https://github.com/mimic-video/mimic-video) | ✓ | 779 MB | ✓ |
| 106 | WAM·A | [[2512.23864\|DreamTacVLA]] | [[2512.23864v3.pdf]] | [`michaelyeah7/learning-to-feel-the-future`](https://github.com/michaelyeah7/learning-to-feel-the-future) | ✓ | 264 MB | ✓ |
| 107 | WAM·A | [[2601.14354\|VJEPA-Probabilistic]] | [[2601.14354v1.pdf]] | [`yongchaohuang/vjepa`](https://github.com/yongchaohuang/vjepa) | ✓ | 16 MB | ✓ |
| 108 | WAM·A | [[2601.20321\|TaF-VLA]] | [[2601.20321v2.pdf]] | — *(no public code)* | — | — | — |
| 109 | WAM·A | [[2602.01153\|UniForce]] | [[2602.01153v1.pdf]] | — *(no public code)* | — | — | — |
| 110 | WAM·A | [[2602.02142\|FD-VLA]] | [[2602.02142v2.pdf]] | — *(no public code)* | — | — | — |
| 111 | WAM·A | [[2602.06001\|VT-WM]] | [[2602.06001v1.pdf]] | — *(no public code)* | — | — | — |
| 112 | WAM·A | [[2602.10098\|VLA-JEPA]] | [[2602.10098v2.pdf]] | [`ginwind/VLA-JEPA`](https://github.com/ginwind/VLA-JEPA) | ✓ | 58 MB | ✓ |
| 113 | WAM·A | [[2602.10102\|VideoWorld 2]] | [[2602.10102v1.pdf]] | [`ByteDance-Seed/VideoWorld`](https://github.com/ByteDance-Seed/VideoWorld) | ✓ | 219 MB | ✓ |
| 114 | WAM·A | [[2602.11832\|JEPA-VLA]] | [[2602.11832v1.pdf]] | — *(no public code)* | — | — | — |
| 115 | WAM·A | [[2602.16086\|LGQ]] | [[2602.16086v2.pdf]] | [`KurbanIntelligenceLab/LGQ`](https://github.com/KurbanIntelligenceLab/LGQ) | ✓ | 38 MB | ✓ |
| 116 | WAM·A | [[2602.18639\|Bisimulation JEPA Planning]] | [[2602.18639v1.pdf]] | — *(no public code)* | — | — | — |
| 117 | WAM·A | [[2603.05438\|CompACT]] | [[2603.05438v1.pdf]] | [`kdwonn/CompACT`](https://github.com/kdwonn/CompACT) | ✓ | 127 MB | ✓ |
| 118 | WAM·A | [[2603.14482\|V-JEPA 2.1]] | [[2603.14482v3.pdf]] | [`facebookresearch/vjepa2`](https://github.com/facebookresearch/vjepa2) | ✓ | 58 MB | ✓ |
| 119 | WAM·A | [[2603.15169\|ForceVLA2]] | [[2603.15169v1.pdf]] | — *(no public code)* | — | — | — |
| 120 | WAM·A | [[2603.15257\|HapticVLA]] | [[2603.15257v1.pdf]] | [`Advanced-Robotic-Manipulation/crab`](https://github.com/Advanced-Robotic-Manipulation/crab) | ✓ | 165 MB | ✓ |
| 121 | WAM·A | [[2603.16666\|Fast-WAM]] | [[2603.16666v2.pdf]] | [`yuantianyuan01/FastWAM`](https://github.com/yuantianyuan01/FastWAM) | ✓ | 56 MB | ✓ |
| 122 | WAM·A | [[2603.17240\|GigaWorld-Policy]] | [[2603.17240v2.pdf]] | [`open-gigaai/giga-world-policy`](https://github.com/open-gigaai/giga-world-policy) | ✓ | 43 MB | ✓ |
| 123 | WAM·A | [[2603.17851\|DexViTac]] | [[2603.17851v1.pdf]] | [`xitong-c/DexViTac`](https://github.com/xitong-c/DexViTac) | ✓ | 238 MB | ✓ |
| 124 | WAM·A | [[2603.19201\|OmniVTA]] | [[2603.19201v2.pdf]] | [`mrsecant/OmniVTA`](https://github.com/mrsecant/OmniVTA) | ✓ | 2.1 GB | ✓ |
| 125 | WAM·A EAI·B | [[2603.22078\|WAM vs VLA Robustness]] | [[2603.22078v3.pdf]] | — *(no public code)* | — | — | — |
| 126 | WAM·A | [[2603.29409\|CLaD]] | [[2603.29409v1.pdf]] | — *(no public code)* | — | — | — |
| 127 | WAM·A | [[2604.02029\|Latent Space Survey]] | [[2604.02029v2.pdf]] | [`YU-deep/Awesome-Latent-Space`](https://github.com/YU-deep/Awesome-Latent-Space) | ✓ | 78 MB | ✓ |
| 128 | WAM·A | [[2604.07335\|TAMEn]] | [[2604.07335v1.pdf]] | [`OpenDriveLab/TAMEn`](https://github.com/OpenDriveLab/TAMEn) | ✓ | 219 MB | ✓ |
| 129 | WAM·A | [[2604.13015\|Touch Dreaming]] | [[2604.13015v2.pdf]] | [`chrisyrniu/humanoid-touch-dream`](https://github.com/chrisyrniu/humanoid-touch-dream) | ✓ | 72 MB | ✓ |
| 130 | WAM·A | [[2604.16484\|DexWorldModel]] | [[2604.16484v1.pdf]] | — *(no public code)* | — | — | — |
| 131 | WAM·A EAI·B | [[2604.16592\|Cognition WM Survey]] | [[2604.16592v2.pdf]] | — *(no public code)* | — | — | — |
| 132 | WAM·A | [[2604.19092\|RoboWM-Bench]] | [[2604.19092v2.pdf]] | [`fffstrong/RoboWM-Bench`](https://github.com/fffstrong/RoboWM-Bench) | ✓ | 1.3 GB | ✓ |
| 133 | WAM·A | [[2604.20444\|VTouch++]] | [[2604.20444v1.pdf]] | — *(no public code)* | — | — | — |
| 134 | WAM·A | [[2605.00078\|Being-H0.7]] | [[2605.00078v1.pdf]] | [`BeingBeyond/Being-H`](https://github.com/BeingBeyond/Being-H) | ✓ | 135 MB | ✓ |
| 135 | WAM·A | [[2605.06388\|Semantic-LDM-WM]] | [[2605.06388v1.pdf]] | [`chandar-lab/semantic-wm`](https://github.com/chandar-lab/semantic-wm) | ✓ | 33 MB | ✓ |
| 136 | WAM·A | [[2605.10942\|HarmoWAM]] | [[2605.10942v1.pdf]] | — *(no public code)* | — | — | — |
| 137 | WAM·A EAI·B | [[2605.12090\|WAM Survey]] | [[2605.12090v1.pdf]] | [`OpenMOSS/Awesome-WAM`](https://github.com/OpenMOSS/Awesome-WAM) | ✓ | 3.5 GB | ✓ |
| 138 | WAM·A | [[2605.13083\|TouchAnything]] | [[2605.13083v1.pdf]] | [`Jianyi2004/TouchAnything`](https://github.com/Jianyi2004/TouchAnything) | ✓ | 242 MB | ✓ |
| 139 | WAM·A | [[2605.15153\|Pelican-Unified]] | [[2605.15153v2.pdf]] | — *(no public code)* | — | — | — |
| 140 | WAM·A | [[2605.15725\|DiLA]] | [[2605.15725v1.pdf]] | [`senngadaisuki/disentangled-latent-action-world-models`](https://github.com/senngadaisuki/disentangled-latent-action-world-models) | ✓ | 75 MB | ✓ |
| 141 | WAM·A | [[2605.19986\|MetaFine]] | [[2605.19986v1.pdf]] | [`Hiangx-robotics/MetaFine`](https://github.com/Hiangx-robotics/MetaFine) | ✓ | 599 MB | ✓ |
| 142 | WAM·A | [[2605.20752\|GaussianDream]] | [[2605.20752v2.pdf]] | [`TuojingAI/GaussianDream`](https://github.com/TuojingAI/GaussianDream) | ✓ | 72 MB | ✓ |
| 143 | WAM·A | [[2605.21862\|EvoScene-VLA]] | [[2605.21862v1.pdf]] | — *(no public code)* | — | — | — |
| 144 | WAM·A EAI·B | [[2605.26379\|LeJEPA World Model]] | [[2605.26379v1.pdf]] | [`klindtlab/lejepa-identifiability`](https://github.com/klindtlab/lejepa-identifiability) | ✓ | 61 MB | ✓ |
| 145 | WAM·A | [[2605.28816\|Gamma-World]] | [[2605.28816v1.pdf]] | [`nv-tlabs/Gamma-World`](https://github.com/nv-tlabs/Gamma-World) | ✓ | 247 MB | ✓ |
| 146 | WAM·A | [[2606.01955\|WALL-WM]] | [[2606.01955v1.pdf]] | [`X-Square-Robot/wall-x`](https://github.com/X-Square-Robot/wall-x) | ✓ | 73 MB | ✓ |
| 147 | WAM·A | [[2606.02800\|Cosmos 3]] | [[2606.02800v3.pdf]] | [`nvidia/cosmos`](https://github.com/nvidia/cosmos) | ✓ | 230 MB | ✓ |
| 148 | WAM·A | [[2606.03188\|GeoSem-WAM]] | [[2606.03188v1.pdf]] | — *(no public code)* | — | — | — |
| 149 | WAM·A | [[2606.04130\|CLAW (Latent Action WM)]] | [[2606.04130v1.pdf]] | — *(no public code)* | — | — | — |
| 150 | WAM·A EAI·B | [[2606.05254\|Flash-WAM]] | [[2606.05254v1.pdf]] | [`NU-World-Model-Embodied-AI/Flash-WAM`](https://github.com/NU-World-Model-Embodied-AI/Flash-WAM) | ✓ | 62 MB | ✓ |
| 151 | WAM·A | [[2606.05979\|WLA]] | [[2606.05979v1.pdf]] | [`SJTU-DENG-Lab/WLA`](https://github.com/SJTU-DENG-Lab/WLA) | ✓ | 32 MB | ✓ |
| 152 | WAM·A | [[2606.08737\|Dream-Tac]] | [[2606.08737v1.pdf]] | [`LYFCLOUDFAN/Dream-Tac`](https://github.com/LYFCLOUDFAN/Dream-Tac) | ✓ | 160 MB | ✓ |
| 153 | WAM·A | [[2606.10040\|Efficient-WAM]] | [[2606.10040v2.pdf]] | [`jiajun613/Efficient-WAM`](https://github.com/jiajun613/Efficient-WAM) | ✓ | 49 MB | ✓ |
| 154 | WAM·A | [[2606.11184\|TacForeSight]] | [[2606.11184v1.pdf]] | — *(no public code)* | — | — | — |
| 155 | WAM·A | [[2606.12217\|AGRA]] | [[2606.12217v1.pdf]] | — *(no public code)* | — | — | — |
| 156 | WAM·A | [[2606.12406\|FACTR 2]] | [[2606.12406v1.pdf]] | — *(no public code)* | — | — | — |
| 157 | S2R·B | [[2104.02646\|gradSim]] | [[2104.02646v1.pdf]] | [`gradsim/gradsim`](https://github.com/gradsim/gradsim) | ✓ | 63 MB | ✓ |
| 158 | S2R·B | [[2204.03139\|DiffCloud]] | [[2204.03139v2.pdf]] | [`priyasundaresan/diffcloud_real2sim`](https://github.com/priyasundaresan/diffcloud_real2sim) | ✓ | 430 MB | ✗ |
| 159 | S2R·B | [[2207.10821\|Lower-Fidelity Sim2Real]] | [[2207.10821v2.pdf]] | [`joannetruong/robot-nav`](https://github.com/joannetruong/robot-nav) | ✓ | 17 MB | ✓ |
| 160 | S2R·B | [[2304.14369\|NCLaw]] | [[2304.14369v2.pdf]] | [`PingchuanMa/NCLaw`](https://github.com/PingchuanMa/NCLaw) | ✓ | 84 MB | ✓ |
| 161 | S2R·B | [[2306.15668\|Physion++]] | [[2306.15668v2.pdf]] | — *(no public code)* | — | — | — |
| 162 | S2R·B | [[2403.03949\|RialTo]] | [[2403.03949v3.pdf]] | [`real-to-sim-to-real/RialTo`](https://github.com/real-to-sim-to-real/RialTo) | ✓ | 889 MB | ✓ |
| 163 | S2R·B | [[2403.12945\|DROID]] | [[2403.12945v2.pdf]] | [`droid-dataset/droid`](https://github.com/droid-dataset/droid) | ✓ | 118 MB | ✓ |
| 164 | S2R·B | [[2404.09833\|Video2Game]] | [[2404.09833v1.pdf]] | [`video2game/video2game`](https://github.com/video2game/video2game) | ✓ | 212 MB | ✓ |
| 165 | S2R·B | [[2404.12308\|ASID]] | [[2404.12308v2.pdf]] | [`WEIRDLabUW/asid`](https://github.com/WEIRDLabUW/asid) | ✓ | 98 MB | ✓ |
| 166 | S2R·B | [[2406.04155\|Lagrangian Particle Optimization]] | [[2406.04155v1.pdf]] | — *(no public code)* | — | — | — |
| 167 | S2R·B | [[2406.10788\|Embodied Gaussians]] | [[2406.10788v1.pdf]] | [`bdaiinstitute/embodied_gaussians`](https://github.com/bdaiinstitute/embodied_gaussians) | ✓ | 89 MB | ✓ |
| 168 | S2R·B | [[2407.07889\|AdaptiGraph]] | [[2407.07889v1.pdf]] | [`Boey-li/AdaptiGraph`](https://github.com/Boey-li/AdaptiGraph) | ✓ | 358 MB | ✗ |
| 169 | S2R·B | [[2411.00554\|DPSI]] | [[2411.00554v3.pdf]] | [`IanYangChina/SI4RP-data`](https://github.com/IanYangChina/SI4RP-data) | ✓ | 6.8 GB | ✓ |
| 170 | S2R·B | [[2412.00259\|One-Shot Real-to-Sim]] | [[2412.00259v4.pdf]] | [`yifanzhu95/RigidWorldModel`](https://github.com/yifanzhu95/RigidWorldModel) | ✓ | 45 MB | ✓ |
| 171 | S2R·B | [[2501.12202\|Hunyuan3D]] | [[2501.12202v5.pdf]] | [`Tencent/Hunyuan3D-2`](https://github.com/Tencent/Hunyuan3D-2) | ✓ | 202 MB | ✓ |
| 172 | S2R·B | [[2503.10118\|RSR Loop]] | [[2503.10118v2.pdf]] | [`sunnyshi0310/RSR-MJX`](https://github.com/sunnyshi0310/RSR-MJX) | ✓ | 66 MB | ✓ |
| 173 | S2R·B | [[2503.17973\|PhysTwin]] | [[2503.17973v1.pdf]] | [`Jianghanxiao/PhysTwin`](https://github.com/Jianghanxiao/PhysTwin) | ✓ | 143 MB | ✓ |
| 174 | S2R·B | [[2504.03597\|Real-is-Sim]] | [[2504.03597v2.pdf]] | — *(no public code)* | — | — | — |
| 175 | S2R·B | [[2505.16971\|UniPhy]] | [[2505.16971v1.pdf]] | [`HimangiM/UniPhy_CVPR2025`](https://github.com/HimangiM/UniPhy_CVPR2025) | ✓ | 97 MB | ✓ |
| 176 | S2R·B | [[2505.17966\|Single-View Mesh for Robotics]] | [[2505.17966v2.pdf]] | — *(no public code)* | — | — | — |
| 177 | S2R·B | [[2506.02794\|PhysGaia]] | [[2506.02794v3.pdf]] | [`mjmjeong/PhysGaia`](https://github.com/mjmjeong/PhysGaia) | ✓ | 243 MB | ✓ |
| 178 | S2R·B | [[2506.04120\|Splatting Physical Scenes]] | [[2506.04120v2.pdf]] | — *(no public code)* | — | — | — |
| 179 | S2R·B | [[2506.10133\|Offline Domain Randomization]] | [[2506.10133v2.pdf]] | — *(no public code)* | — | — | — |
| 180 | S2R·B | [[2506.15680\|Particle-Grid Neural Dynamics]] | [[2506.15680v2.pdf]] | [`kywind/pgnd`](https://github.com/kywind/pgnd) | ✓ | 63 MB | ✓ |
| 181 | S2R·B EAI·B | [[2506.18088\|RoboTwin 2.0]] | [[2506.18088v2.pdf]] | [`RoboTwin-Platform/RoboTwin`](https://github.com/RoboTwin-Platform/RoboTwin) | ✓ | 203 MB | ✓ |
| 182 | S2R·B | [[2508.01112\|MASIV]] | [[2508.01112v1.pdf]] | [`Skaldak/MASIV`](https://github.com/Skaldak/MASIV) | ✓ | 56 MB | ✓ |
| 183 | S2R·B | [[2509.18631\|Sim-Real OT Co-Training]] | [[2509.18631v3.pdf]] | [`TTimelord/ot-sim2real`](https://github.com/TTimelord/ot-sim2real) | ✓ | 268 MB | ✓ |
| 184 | S2R·B | [[2509.24948\|RehearseVLA]] | [[2509.24948v6.pdf]] | [`amap-cvlab/world-env`](https://github.com/amap-cvlab/world-env) | ✓ | 100 MB | ✓ |
| 185 | S2R·B | [[2510.11689\|Phys2Real]] | [[2510.11689v2.pdf]] | [`phys2real/phys2real`](https://github.com/phys2real/phys2real) | ✓ | 6.7 MB | ✓ |
| 186 | S2R·B | [[2510.17950\|RoboChallenge]] | [[2510.17950v1.pdf]] | — *(no public code)* | — | — | — |
| 187 | S2R·B | [[2510.20813\|GSWorld]] | [[2510.20813v1.pdf]] | [`3dgsworld/gsworld`](https://github.com/3dgsworld/gsworld) | ✓ | 314 MB | ✓ |
| 188 | S2R·B | [[2510.22975\|VoMP]] | [[2510.22975v2.pdf]] | [`nv-tlabs/VoMP`](https://github.com/nv-tlabs/VoMP) | ✓ | 416 MB | ✓ |
| 189 | S2R·B | [[2511.04665\|Real-to-Sim GS]] | [[2511.04665v2.pdf]] | [`kywind/real2sim-eval`](https://github.com/kywind/real2sim-eval) | ✓ | 55 MB | ✓ |
| 190 | S2R·B | [[2511.04831\|Isaac Lab]] | [[2511.04831v1.pdf]] | [`isaac-sim/IsaacLab`](https://github.com/isaac-sim/IsaacLab) | ✓ | 782 MB | ✓ |
| 191 | S2R·B | [[2511.06299\|Physics-Informed Deformable GS]] | [[2511.06299v3.pdf]] | [`SCAILab-USTC/Physics-Informed-Deformable-Gaussian-Splatting`](https://github.com/SCAILab-USTC/Physics-Informed-Deformable-Gaussian-Splatting) | ✓ | 343 MB | ✓ |
| 192 | S2R·B | [[2511.07416\|PhysWorld]] | [[2511.07416v1.pdf]] | — *(no public code)* | — | — | — |
| 193 | S2R·B | [[2512.00076\|Arcadia]] | [[2512.00076v1.pdf]] | [`Embodied-Arcadia/EmbodiedKit`](https://github.com/Embodied-Arcadia/EmbodiedKit) | ✓ | 123 MB | ✓ |
| 194 | S2R·B | [[2512.13214\|Differentiable MPM Control]] | [[2512.13214v1.pdf]] | — *(no public code)* | — | — | — |
| 195 | S2R·B | [[2512.14696\|CRISP]] | [[2512.14696v3.pdf]] | [`crisp-real2sim/CRISP-Real2Sim`](https://github.com/crisp-real2sim/CRISP-Real2Sim) | ✓ | 200 MB | ✓ |
| 196 | S2R·B | [[2512.16881\|PolaRiS]] | [[2512.16881v2.pdf]] | [`arhanjain/polaris`](https://github.com/arhanjain/polaris) | ✓ | 35 MB | ✓ |
| 197 | S2R·B | [[2512.19390\|TwinAligner]] | [[2512.19390v1.pdf]] | [`TwinAligner/TwinAligner`](https://github.com/TwinAligner/TwinAligner) | ✓ | 348 MB | ✓ |
| 198 | S2R·B | [[2512.19562\|REALM]] | [[2512.19562v1.pdf]] | [`martin-sedlacek/REALM`](https://github.com/martin-sedlacek/REALM) | ✓ | 437 MB | ✓ |
| 199 | S2R·B | [[2601.02078\|Genie Sim 3.0]] | [[2601.02078v2.pdf]] | [`AgibotTech/genie_sim`](https://github.com/AgibotTech/genie_sim) | ✓ | 592 MB | ✓ |
| 200 | S2R·B | [[2601.17251\|EMPM]] | [[2601.17251v1.pdf]] | — *(no public code)* | — | — | — |
| 201 | S2R·B | [[2602.12628\|RL-Co]] | [[2602.12628v4.pdf]] | [`RLinf/RLinf`](https://github.com/RLinf/RLinf) | ✓ | 253 MB | ✓ |
| 202 | S2R·B | [[2603.01151\|D-REX]] | [[2603.01151v1.pdf]] | — *(no public code)* | — | — | — |
| 203 | S2R·B | [[2603.04531\|PTLD]] | [[2603.04531v2.pdf]] | — *(no public code)* | — | — | — |
| 204 | S2R·B | [[2603.13825\|Explicit-WM Manipulation]] | [[2603.13825v1.pdf]] | — *(no public code)* | — | — | — |
| 205 | S2R·B | [[2604.04974\|Video-to-Control Survey]] | [[2604.04974v3.pdf]] | — *(no public code)* | — | — | — |
| 206 | S2R·B | [[2604.08544\|SIM1]] | [[2604.08544v2.pdf]] | [`InternRobotics/SIM1`](https://github.com/InternRobotics/SIM1) | ✓ | 175 MB | ✓ |
| 207 | S2R·B | [[2604.10856\|BridgeSim]] | [[2604.10856v1.pdf]] | [`vail-ucla/BridgeSim`](https://github.com/vail-ucla/BridgeSim) | ✓ | 525 MB | ✓ |
| 208 | S2R·B | [[2604.11386\|ComSim]] | [[2604.11386v1.pdf]] | [`faceong/ComSim`](https://github.com/faceong/ComSim) | ✓ | 167 MB | ✓ |
| 209 | S2R·B | [[2604.15805\|WorldComposer]] | [[2604.15805v1.pdf]] | [`jaber628/WorldComposer`](https://github.com/jaber628/WorldComposer) | ✓ | 68 MB | ✓ |
| 210 | S2R·B | [[2604.26509\|3D Generation for Embodied AI Survey]] | [[2604.26509v3.pdf]] | [`hitcslj/3DGen4Robot`](https://github.com/hitcslj/3DGen4Robot) | ✓ | 6.5 MB | ✓ |
| 211 | S2R·B | [[2604.27367\|DOT-Sim]] | [[2604.27367v1.pdf]] | — *(no public code)* | — | — | — |
| 212 | S2R·B | [[2605.00080\|WM Robot Learning Survey]] | [[2605.00080v1.pdf]] | [`NTUMARS/Awesome-World-Model-for-Robotics-Policy`](https://github.com/NTUMARS/Awesome-World-Model-for-Robotics-Policy) | ✓ | 6.9 MB | ✓ |
| 213 | S2R·B | [[2605.09538\|PhysHanDI]] | [[2605.09538v1.pdf]] | — *(no public code)* | — | — | — |
| 214 | S2R·B | [[2605.26638\|HyperSim]] | [[2605.26638v1.pdf]] | — *(no public code)* | — | — | — |
| 215 | S2R·B | [[2605.28812\|CoP Tactile]] | [[2605.28812v1.pdf]] | — *(no public code)* | — | — | — |
| 216 | S2R·B | [[2606.08828\|Video2Sim2Real]] | [[2606.08828v1.pdf]] | [`video2sim2real/video2sim2real`](https://github.com/video2sim2real/video2sim2real) | ✓ | 1.1 GB | ✓ |
| 217 | S2R·B | [[2606.12604\|EgoEngine]] | [[2606.12604v1.pdf]] | — *(no public code)* | — | — | — |
| 218 | EAI·B | [[1612.00796\|EWC]] | [[1612.00796v2.pdf]] | — *(no public code)* | — | — | — |
| 219 | EAI·B | [[2105.10919\|Continual World]] | [[2105.10919v3.pdf]] | [`awarelab/continual_world`](https://github.com/awarelab/continual_world) | ✓ | 36 MB | ✓ |
| 220 | EAI·B | [[2109.00137\|IBC]] | [[2109.00137v1.pdf]] | [`google-research/ibc`](https://github.com/google-research/ibc) | ✓ | 112 MB | ✓ |
| 221 | EAI·B | [[2109.08238\|HM3D]] | [[2109.08238v1.pdf]] | [`facebookresearch/habitat-matterport3d-dataset`](https://github.com/facebookresearch/habitat-matterport3d-dataset) | ✓ | 16 MB | ✓ |
| 222 | EAI·B | [[2109.13202\|MiniHack]] | [[2109.13202v2.pdf]] | [`facebookresearch/minihack`](https://github.com/facebookresearch/minihack) | ✓ | 99 MB | ✓ |
| 223 | EAI·B | [[2211.15944\|Continual-Dreamer]] | [[2211.15944v2.pdf]] | [`skezle/continual-dreamer`](https://github.com/skezle/continual-dreamer) | ✓ | 38 MB | ✓ |
| 224 | EAI·B | [[2306.13394\|MME]] | [[2306.13394v5.pdf]] | [`BradyFU/Awesome-Multimodal-Large-Language-Models`](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) | ✓ | 131 MB | ✓ |
| 225 | EAI·B | [[2307.06281\|MMBench]] | [[2307.06281v5.pdf]] | [`open-compass/MMBench`](https://github.com/open-compass/MMBench) | ✓ | 9.2 MB | ✓ |
| 226 | EAI·B | [[2310.06253\|Objective Mismatch MBRL Survey]] | [[2310.06253v2.pdf]] | [`ran-weii/objective_mismatch_papers`](https://github.com/ran-weii/objective_mismatch_papers) | ✓ | 8.3 MB | ✓ |
| 227 | EAI·B | [[2311.16502\|MMMU]] | [[2311.16502v4.pdf]] | [`MMMU-Benchmark/MMMU`](https://github.com/MMMU-Benchmark/MMMU) | ✓ | 251 MB | ✓ |
| 228 | EAI·B | [[2404.14387\|LLM Self-Evolution Survey]] | [[2404.14387v2.pdf]] | [`AlibabaResearch/DAMO-ConvAI`](https://github.com/AlibabaResearch/DAMO-ConvAI) | ✓ | 1.0 GB | ✓ |
| 229 | EAI·B | [[2405.09673\|LoRA-Learns-Less]] | [[2405.09673v2.pdf]] | [`danbider/lora-tradeoffs`](https://github.com/danbider/lora-tradeoffs) | ✓ | 8.8 MB | ✓ |
| 230 | EAI·B | [[2406.04339\|RoboMamba]] | [[2406.04339v2.pdf]] | [`lmzpai/roboMamba`](https://github.com/lmzpai/roboMamba) | ✓ | 27 MB | ✓ |
| 231 | EAI·B | [[2408.07666\|Model Merging in LLMs/MLLMs]] | [[2408.07666v5.pdf]] | [`EnnengYang/Awesome-Model-Merging-Methods-Theories-Applications`](https://github.com/EnnengYang/Awesome-Model-Merging-Methods-Theories-Applications) | ✓ | 14 MB | ✓ |
| 232 | EAI·B | [[2410.00371\|AHA]] | [[2410.00371v1.pdf]] | [`NVlabs/AHA`](https://github.com/NVlabs/AHA) | ✓ | 68 MB | ✓ |
| 233 | EAI·B | [[2502.19645\|OpenVLA-OFT]] | [[2502.19645v2.pdf]] | [`moojink/openvla-oft`](https://github.com/moojink/openvla-oft) | ✓ | 49 MB | ✓ |
| 234 | EAI·B | [[2503.02310\|PD-VLA]] | [[2503.02310v2.pdf]] | — *(no public code)* | — | — | — |
| 235 | EAI·B | [[2503.08558\|FAIL-Detect]] | [[2503.08558v3.pdf]] | [`CXU-TRI/FAIL-Detect`](https://github.com/CXU-TRI/FAIL-Detect) | ✓ | 99 MB | ✓ |
| 236 | EAI·B | [[2503.18684\|OMLA]] | [[2503.18684v2.pdf]] | — *(no public code)* | — | — | — |
| 237 | EAI·B | [[2505.04769\|VLA Concepts Survey]] | [[2505.04769v2.pdf]] | [`Applied-AI-Research-Lab/Vision-Language-Action-Models-Concepts-Progress-Applications-and-Challenges`](https://github.com/Applied-AI-Research-Lab/Vision-Language-Action-Models-Concepts-Progress-Applications-and-Challenges) | ✓ | 22 MB | ✓ |
| 238 | EAI·B | [[2505.12224\|RoboFAC]] | [[2505.12224v4.pdf]] | [`MINT-SJTU/RoboFAC`](https://github.com/MINT-SJTU/RoboFAC) | ✓ | 57 MB | ✓ |
| 239 | EAI·B | [[2505.23705\|Knowledge Insulation VLA]] | [[2505.23705v1.pdf]] | [`Physical-Intelligence/openpi`](https://github.com/Physical-Intelligence/openpi) | ✓ | 79 MB | ✓ |
| 240 | EAI·B | [[2506.00613\|WorldGym]] | [[2506.00613v3.pdf]] | [`world-model-eval/world-model-eval`](https://github.com/world-model-eval/world-model-eval) | ✓ | 41 MB | ✓ |
| 241 | EAI·B | [[2506.06677\|RoboCerebra]] | [[2506.06677v2.pdf]] | [`qiuboxiang/RoboCerebra`](https://github.com/qiuboxiang/RoboCerebra) | ✓ | 696 MB | ✓ |
| 242 | EAI·B | [[2506.09937\|SAFE]] | [[2506.09937v2.pdf]] | [`vla-safe/SAFE`](https://github.com/vla-safe/SAFE) | ✓ | 31 MB | ✓ |
| 243 | EAI·B | [[2506.09985\|V-JEPA 2]] | [[2506.09985v1.pdf]] | [`facebookresearch/vjepa2`](https://github.com/facebookresearch/vjepa2) | ✓ | 58 MB | ✓ |
| 244 | EAI·B | [[2506.12723\|SP-VLA]] | [[2506.12723v3.pdf]] | [`ChildTang/SP-VLA`](https://github.com/ChildTang/SP-VLA) | ✓ | 127 MB | ✓ |
| 245 | EAI·B | [[2506.18123\|RoboArena]] | [[2506.18123v2.pdf]] | [`robo-arena/roboarena`](https://github.com/robo-arena/roboarena) | ✓ | 14 MB | ✓ |
| 246 | EAI·B | [[2506.21669\|SEEA-R1]] | [[2506.21669v2.pdf]] | [`AurumTian/seea-r1`](https://github.com/AurumTian/seea-r1) | ✓ | 192 MB | ✓ |
| 247 | EAI·B | [[2506.21872\|Continual RL Survey]] | [[2506.21872v2.pdf]] | — *(no public code)* | — | — | — |
| 248 | EAI·B | [[2507.05116\|VOTE]] | [[2507.05116v4.pdf]] | [`LukeLIN-web/VOTE`](https://github.com/LukeLIN-web/VOTE) | ✓ | 51 MB | ✓ |
| 249 | EAI·B | [[2508.07407\|Self-Evolving AI Agents Survey]] | [[2508.07407v2.pdf]] | [`EvoAgentX/Awesome-Self-Evolving-Agents`](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents) | ✓ | 11 MB | ✓ |
| 250 | EAI·B | [[2508.19236\|MemoryVLA]] | [[2508.19236v2.pdf]] | [`shihao1895/MemoryVLA`](https://github.com/shihao1895/MemoryVLA) | ✓ | 208 MB | ✓ |
| 251 | EAI·B | [[2509.04018\|FPC-VLA]] | [[2509.04018v2.pdf]] | — *(no public code)* | — | — | — |
| 252 | EAI·B | [[2509.09372\|VLA-Adapter]] | [[2509.09372v2.pdf]] | [`OpenHelix-Team/VLA-Adapter`](https://github.com/OpenHelix-Team/VLA-Adapter) | ✓ | 172 MB | ✓ |
| 253 | EAI·B | [[2509.11480\|VLA Cross-Platform Scaling]] | [[2509.11480v2.pdf]] | — *(no public code)* | — | — | — |
| 254 | EAI·B | [[2509.18953\|Eva-VLA]] | [[2509.18953v2.pdf]] | — *(no public code)* | — | — | — |
| 255 | EAI·B | [[2509.22195\|Actions as Language]] | [[2509.22195v1.pdf]] | — *(no public code)* | — | — | — |
| 256 | EAI·B | [[2510.01642\|FailSafe]] | [[2510.01642v2.pdf]] | [`jimntu/FailSafe_code`](https://github.com/jimntu/FailSafe_code) | ✓ | 703 MB | ✓ |
| 257 | EAI·B | [[2510.02298\|ARMADA]] | [[2510.02298v1.pdf]] | [`Virlus/armada`](https://github.com/Virlus/armada) | ✓ | 180 MB | ✓ |
| 258 | EAI·B | [[2510.03827\|LIBERO-PRO]] | [[2510.03827v2.pdf]] | [`Zxy-MLlab/LIBERO-PRO`](https://github.com/Zxy-MLlab/LIBERO-PRO) | ✓ | 1.1 GB | ✓ |
| 259 | EAI·B | [[2510.04354\|SureSim]] | [[2510.04354v1.pdf]] | [`irom-princeton/rapid-policy-evaluation`](https://github.com/irom-princeton/rapid-policy-evaluation) | ✓ | 268 MB | ✓ |
| 260 | EAI·B | [[2510.07077\|VLA Robotics Real-World Review]] | [[2510.07077v1.pdf]] | — *(no public code)* | — | — | — |
| 261 | EAI·B | [[2510.09459\|FIPER]] | [[2510.09459v2.pdf]] | [`utiasDSL/fiper`](https://github.com/utiasDSL/fiper) | ✓ | 47 MB | ✓ |
| 262 | EAI·B | [[2510.10125\|CTRL-WORLD]] | [[2510.10125v3.pdf]] | [`Robert-gyj/Ctrl-World`](https://github.com/Robert-gyj/Ctrl-World) | ✓ | 190 MB | ✓ |
| 263 | EAI·B | [[2510.20685\|C-Nav]] | [[2510.20685v4.pdf]] | [`BigTree765/C-Nav`](https://github.com/BigTree765/C-Nav) | ✓ | 3.0 MB | ✓ |
| 264 | EAI·B | [[2510.24795\|Efficient VLA Survey]] | [[2510.24795v2.pdf]] | [`YuZhaoshu/Efficient-VLAs-Survey`](https://github.com/YuZhaoshu/Efficient-VLAs-Survey) | ✓ | 19 MB | ✓ |
| 265 | EAI·B | [[2511.04555\|Evo-1]] | [[2511.04555v2.pdf]] | [`MINT-SJTU/Evo-1`](https://github.com/MINT-SJTU/Evo-1) | ✓ | 131 MB | ✓ |
| 266 | EAI·B | [[2511.15605\|SRPO]] | [[2511.15605v2.pdf]] | [`sii-research/siiRL`](https://github.com/sii-research/siiRL) | ✓ | 124 MB | ✓ |
| 267 | EAI·B | [[2511.16166\|EvoVLA]] | [[2511.16166v1.pdf]] | [`AIGeeksGroup/EvoVLA`](https://github.com/AIGeeksGroup/EvoVLA) | ✓ | 447 MB | ✓ |
| 268 | EAI·B | [[2511.18810\|MergeVLA]] | [[2511.18810v2.pdf]] | [`MergeVLA/MergeVLA`](https://github.com/MergeVLA/MergeVLA) | ✓ | 253 MB | ✓ |
| 269 | EAI·B | [[2512.00836\|Counterfactual Model Error]] | [[2512.00836v1.pdf]] | [`uncidd/scenario-eval-theory`](https://github.com/uncidd/scenario-eval-theory) | ✓ | 479 MB | ✓ |
| 270 | EAI·B | [[2601.02295\|CycleVLA]] | [[2601.02295v1.pdf]] | — *(no public code)* | — | — | — |
| 271 | EAI·B | [[2601.04137\|WoW-World-Eval]] | [[2601.04137v1.pdf]] | — *(no public code)* | — | — | — |
| 272 | EAI·B | [[2601.09512\|CLARE]] | [[2601.09512v2.pdf]] | [`tum-lsy/clare`](https://github.com/tum-lsy/clare) | ✓ | 274 MB | ✓ |
| 273 | EAI·B | [[2601.17067\|Video Generation as World Models Survey]] | [[2601.17067v1.pdf]] | [`hit-perfect/Awesome-Video-World-Models`](https://github.com/hit-perfect/Awesome-Video-World-Models) | ✓ | 15 MB | ✓ |
| 274 | EAI·B | [[2602.03445\|CRL-VLA]] | [[2602.03445v1.pdf]] | — *(no public code)* | — | — | — |
| 275 | EAI·B | [[2602.03782\|QVLA]] | [[2602.03782v1.pdf]] | [`AutoLab-SAI-SJTU/QVLA`](https://github.com/AutoLab-SAI-SJTU/QVLA) | ✓ | 130 MB | ✓ |
| 276 | EAI·B | [[2602.04411\|Self-evolving Embodied AI]] | [[2602.04411v1.pdf]] | — *(no public code)* | — | — | — |
| 277 | EAI·B | [[2602.06043\|Share]] | [[2602.06043v1.pdf]] | [`ankit-vaidya19/Share`](https://github.com/ankit-vaidya19/Share) | ✓ | 1.1 GB | ✓ |
| 278 | EAI·B | [[2602.08025\|MIND-Bench]] | [[2602.08025v2.pdf]] | [`CSU-JPG/MIND`](https://github.com/CSU-JPG/MIND) | ✓ | 46 MB | ✓ |
| 279 | EAI·B | [[2602.08971\|WorldArena]] | [[2602.08971v2.pdf]] | [`tsinghua-fib-lab/WorldArena`](https://github.com/tsinghua-fib-lab/WorldArena) | ✓ | 283 MB | ✓ |
| 280 | EAI·B | [[2602.10503\|Long-Lived Robots]] | [[2602.10503v2.pdf]] | — *(no public code)* | — | — | — |
| 281 | EAI·B | [[2602.13086\|UniManip]] | [[2602.13086v1.pdf]] | — *(no public code)* | — | — | — |
| 282 | EAI·B | [[2602.16710\|EgoScale]] | [[2602.16710v1.pdf]] | — *(no public code)* | — | — | — |
| 283 | EAI·B | [[2602.18397\|VLA-Perf]] | [[2602.18397v1.pdf]] | [`NVlabs/vla-perf`](https://github.com/NVlabs/vla-perf) | ✓ | 49 MB | ✓ |
| 284 | EAI·B | [[2602.20057\|AdaWorldPolicy]] | [[2602.20057v1.pdf]] | — *(no public code)* | — | — | — |
| 285 | EAI·B | [[2602.20309\|QuantVLA]] | [[2602.20309v4.pdf]] | [`AIoT-MLSys-Lab/QuantVLA`](https://github.com/AIoT-MLSys-Lab/QuantVLA) | ✓ | 92 MB | ✓ |
| 286 | EAI·B | [[2602.21531\|LiLo]] | [[2602.21531v1.pdf]] | [`yy-gx/LiLo-VLA`](https://github.com/yy-gx/LiLo-VLA) | ✓ | 79 MB | ✓ |
| 287 | EAI·B | [[2602.21633\|SC-VLA]] | [[2602.21633v1.pdf]] | [`Kisaragi0/SC-VLA`](https://github.com/Kisaragi0/SC-VLA) | ✓ | 63 MB | ✓ |
| 288 | EAI·B | [[2602.22579\|VLA Metamorphic Testing]] | [[2602.22579v2.pdf]] | [`pablovalle/MT_of_VLAs`](https://github.com/pablovalle/MT_of_VLAs) | ✓ | 35.0 GB | ✓ |
| 289 | EAI·B | [[2603.02224\|Subspace Geometry Forgetting]] | [[2603.02224v1.pdf]] | — *(no public code)* | — | — | — |
| 290 | EAI·B | [[2603.03818\|VLA Continual Learning]] | [[2603.03818v2.pdf]] | [`UT-Austin-RPL/continual-vla`](https://github.com/UT-Austin-RPL/continual-vla) | ✓ | 15 MB | ✓ |
| 291 | EAI·B | [[2603.07648\|AtomicVLA]] | [[2603.07648v1.pdf]] | [`zhanglk9/AtomicVLA`](https://github.com/zhanglk9/AtomicVLA) | ✓ | 64 MB | ✓ |
| 292 | EAI·B | [[2603.09030\|PlayWorld]] | [[2603.09030v3.pdf]] | — *(no public code)* | — | — | — |
| 293 | EAI·B | [[2603.09298\|CORAL (LoRA Experts)]] | [[2603.09298v1.pdf]] | [`LUOyk1999/CORAL`](https://github.com/LUOyk1999/CORAL) | ✓ | 26 MB | ✓ |
| 294 | EAI·B | [[2603.11653\|VLA RL Continual Learning]] | [[2603.11653v2.pdf]] | [`UT-Austin-RobIn/continual-vla-rl`](https://github.com/UT-Austin-RobIn/continual-vla-rl) | ✓ | 2.1 GB | ✓ |
| 295 | EAI·B | [[2603.12942\|ReMem-VLA]] | [[2603.12942v1.pdf]] | — *(no public code)* | — | — | — |
| 296 | EAI·B | [[2603.13528\|Counterfactual Failure Synthesis]] | [[2603.13528v1.pdf]] | — *(no public code)* | — | — | — |
| 297 | EAI·B | [[2603.13966\|vla-eval]] | [[2603.13966v2.pdf]] | [`allenai/vla-evaluation-harness`](https://github.com/allenai/vla-evaluation-harness) | ✓ | 80 MB | ✓ |
| 298 | EAI·B | [[2603.16195\|S-VAM]] | [[2603.16195v2.pdf]] | [`haodong-yan/S-VAM`](https://github.com/haodong-yan/S-VAM) | ✓ | 81 MB | ✓ |
| 299 | EAI·B | [[2603.19312\|LeWM]] | [[2603.19312v3.pdf]] | [`lucas-maes/le-wm`](https://github.com/lucas-maes/le-wm) | ✓ | 27 MB | ✓ |
| 300 | EAI·B | [[2603.22212\|Omni-WorldBench]] | [[2603.22212v1.pdf]] | [`AMAP-ML/Omni-WorldBench`](https://github.com/AMAP-ML/Omni-WorldBench) | ✓ | 33 MB | ✓ |
| 301 | EAI·B | [[2603.23376\|ABot-PhysWorld]] | [[2603.23376v2.pdf]] | [`amap-cvlab/ABot-PhysWorld`](https://github.com/amap-cvlab/ABot-PhysWorld) | ✓ | 305 MB | ✓ |
| 302 | EAI·B | [[2603.23497\|WildWorld]] | [[2603.23497v1.pdf]] | [`ShandaAI/WildWorld`](https://github.com/ShandaAI/WildWorld) | ✓ | 9.9 MB | ✓ |
| 303 | EAI·B | [[2603.24350\|Emergent Self]] | [[2603.24350v3.pdf]] | [`adidevj7/emergentrobotself`](https://github.com/adidevj7/emergentrobotself) | ✓ | 665 MB | ✓ |
| 304 | EAI·B | [[2603.28301\|LIBERO-Para]] | [[2603.28301v1.pdf]] | [`cau-hai-lab/LIBERO-Para`](https://github.com/cau-hai-lab/LIBERO-Para) | ✓ | 814 MB | ✓ |
| 305 | EAI·B | [[2603.28489\|Video Gen as WM Survey]] | [[2603.28489v2.pdf]] | — *(no public code)* | — | — | — |
| 306 | EAI·B | [[2604.05498\|JailWAM]] | [[2604.05498v1.pdf]] | — *(no public code)* | — | — | — |
| 307 | EAI·B | [[2604.18791\|HELM]] | [[2604.18791v1.pdf]] | — *(no public code)* | — | — | — |
| 308 | EAI·B | [[2604.21686\|WorldMark]] | [[2604.21686v1.pdf]] | — *(no public code)* | — | — | — |
| 309 | EAI·B | [[2604.22152\|dWorldEval]] | [[2604.22152v1.pdf]] | — *(no public code)* | — | — | — |
| 310 | EAI·B | [[2604.22748\|Agentic World Modeling Survey]] | [[2604.22748v3.pdf]] | [`matrix-agent/awesome-agentic-world-modeling`](https://github.com/matrix-agent/awesome-agentic-world-modeling) | ✓ | 50 MB | ✓ |
| 311 | EAI·B | [[2604.23775\|VLA Safety Survey]] | [[2604.23775v1.pdf]] | [`LiQiiiii/Awesome-VLA-Safety`](https://github.com/LiQiiiii/Awesome-VLA-Safety) | ✓ | 18 MB | ✓ |
| 312 | EAI·B | [[2605.02900\|Safety in Embodied AI Survey]] | [[2605.02900v2.pdf]] | [`x-zheng16/Awesome-Embodied-AI-Safety`](https://github.com/x-zheng16/Awesome-Embodied-AI-Safety) | ✓ | 61 MB | ✓ |
| 313 | EAI·B | [[2605.06311\|VISER]] | [[2605.06311v1.pdf]] | — *(no public code)* | — | — | — |
| 314 | EAI·B | [[2605.08799\|ElasticFlow]] | [[2605.08799v1.pdf]] | — *(no public code)* | — | — | — |
| 315 | EAI·B | [[2605.08879\|ConSFT]] | [[2605.08879v2.pdf]] | [`tyzhang2907/ConservativeSFT`](https://github.com/tyzhang2907/ConservativeSFT) | ✓ | 66 MB | ✓ |
| 316 | EAI·B | [[2605.10921\|RoboMemArena]] | [[2605.10921v1.pdf]] | [`OpenHelix-Team/RoboMemArena`](https://github.com/OpenHelix-Team/RoboMemArena) | ✓ | 716 MB | ✓ |
| 317 | EAI·B | [[2605.10993\|ECHO-VLA]] | [[2605.10993v1.pdf]] | — *(no public code)* | — | — | — |
| 318 | EAI·B | [[2605.13778\|Realtime-VLA FLASH]] | [[2605.13778v1.pdf]] | [`dexmal/realtime-vla-flash`](https://github.com/dexmal/realtime-vla-flash) | ✓ | 84 MB | ✓ |
| 319 | EAI·B | [[2605.14598\|DSSP]] | [[2605.14598v2.pdf]] | — *(no public code)* | — | — | — |
| 320 | EAI·B | [[2605.15735\|UAM]] | [[2605.15735v2.pdf]] | [`CladernyJorn/Unified-Action-Model`](https://github.com/CladernyJorn/Unified-Action-Model) | ✓ | 54 MB | ✓ |
| 321 | EAI·B | [[2605.20774\|VLA-REPLICA]] | [[2605.20774v1.pdf]] | [`IRVLUTD/VLAReplica`](https://github.com/IRVLUTD/VLAReplica) | ✓ | 29 MB | ✓ |
| 322 | EAI·B | [[2605.21800\|stable-worldmodel]] | [[2605.21800v1.pdf]] | [`galilai-group/stable-worldmodel`](https://github.com/galilai-group/stable-worldmodel) | ✓ | 564 MB | ✓ |
| 323 | EAI·B | [[2605.25874\|WBench]] | [[2605.25874v1.pdf]] | [`meituan-longcat/WBench`](https://github.com/meituan-longcat/WBench) | ✓ | 123 MB | ✓ |
| 324 | EAI·B | [[2605.26820\|VLA Continual Forgetting]] | [[2605.26820v1.pdf]] | [`Agentic-Intelligence-Lab/ContinualVLA`](https://github.com/Agentic-Intelligence-Lab/ContinualVLA) | ✓ | 74 MB | ✓ |
| 325 | EAI·B | [[2605.27589\|What-If World]] | [[2605.27589v1.pdf]] | — *(no public code)* | — | — | — |
| 326 | EAI·B | [[2605.28527\|VLA Value Probing]] | [[2605.28527v1.pdf]] | — *(no public code)* | — | — | — |
| 327 | EAI·B | [[2605.28634\|PrimitiveVLA]] | [[2605.28634v1.pdf]] | — *(no public code)* | — | — | — |
| 328 | EAI·B | [[2605.29360\|MiraBench]] | [[2605.29360v1.pdf]] | — *(no public code)* | — | — | — |
| 329 | EAI·B | [[2605.29438\|ElegantVLA]] | [[2605.29438v1.pdf]] | — *(no public code)* | — | — | — |
| 330 | EAI·B | [[2605.29548\|Capacity Interference Retention]] | [[2605.29548v2.pdf]] | — *(no public code)* | — | — | — |
| 331 | EAI·B | [[2605.29562\|VLA-Pro]] | [[2605.29562v1.pdf]] | [`ketchup45/VLA-Pro`](https://github.com/ketchup45/VLA-Pro) | ✓ | 64 MB | ✓ |
| 332 | EAI·B | [[2605.29710\|PhAIL]] | [[2605.29710v1.pdf]] | [`positronic-robotics/positronic`](https://github.com/positronic-robotics/positronic) | ✓ | 272 MB | ✓ |
| 333 | EAI·B | [[2605.30834\|Hide-and-Seek]] | [[2605.30834v1.pdf]] | — *(no public code)* | — | — | — |
| 334 | EAI·B | [[2606.02307\|FATE-VLA]] | [[2606.02307v1.pdf]] | [`pablovalle/fate-vla`](https://github.com/pablovalle/fate-vla) | ✗ | — | — |
| 335 | EAI·B | [[2606.03374\|eMEM]] | [[2606.03374v1.pdf]] | [`automatikarobotics/emem`](https://github.com/automatikarobotics/emem) | ✗ | — | — |
| 336 | EAI·B | [[2606.03385\|GTP-FA]] | [[2606.03385v1.pdf]] | — *(no public code)* | — | — | — |
| 337 | EAI·B | [[2606.03556\|VLA Patch Attack]] | [[2606.03556v1.pdf]] | — *(no public code)* | — | — | — |
| 338 | EAI·B | [[2606.03598\|PHASER]] | [[2606.03598v2.pdf]] | — *(no public code)* | — | — | — |
| 339 | EAI·B | [[2606.04233\|Manipulation Benchmark Audit]] | [[2606.04233v1.pdf]] | [`ripl/manipulation_benchmark_audit`](https://github.com/ripl/manipulation_benchmark_audit) | ✓ | 7.3 MB | ✓ |
| 340 | EAI·B | [[2606.04463\|OSCAR]] | [[2606.04463v2.pdf]] | [`wuzy2115/oscar-public`](https://github.com/wuzy2115/oscar-public) | ✓ | 102 MB | ✓ |
| 341 | EAI·B | [[2606.05159\|X4Val]] | [[2606.05159v1.pdf]] | — *(no public code)* | — | — | — |
| 342 | EAI·B | [[2606.05395\|VASO]] | [[2606.05395v1.pdf]] | — *(no public code)* | — | — | — |
| 343 | EAI·B | [[2606.05737\|One-Step VLA]] | [[2606.05737v1.pdf]] | — *(no public code)* | — | — | — |
| 344 | EAI·B | [[2606.05773\|PiL-World]] | [[2606.05773v1.pdf]] | — *(no public code)* | — | — | — |

## Resolve-OK but clone failed

These have a confirmed repo URL but the clone did not complete (timeout / size / access). Re-clone manually if needed.

- [[2606.02307]] — [`pablovalle/fate-vla`](https://github.com/pablovalle/fate-vla)
- [[2606.03374]] — [`automatikarobotics/emem`](https://github.com/automatikarobotics/emem)

## Cross-references

- [[Focus-Direction]] — the research program these papers serve.
- Source clusters: [[Whole-Body]] · [[WAM]] · [[Sim2Real]] · [[Embodied-AI]].
- PDFs: `data/papers/` · Repos: `data/.repositories/`.
