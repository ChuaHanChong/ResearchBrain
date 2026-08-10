# Transcript: alphaxiv search for GRPO-style RL fine-tuning of VLA models for robotics

## 1. Tool calls

### Call 1

Tool: `mcp__alphaxiv__discover_papers`

Parameters (exact JSON):
```json
{
  "keywords": ["GRPO", "vision-language-action", "reinforcement learning", "robotics"],
  "question": "recent papers on using GRPO-style reinforcement learning to fine-tune vision-language-action models for robotics",
  "difficulty": 6,
  "prioritize": "recency"
}
```

Result (no error):
```
1. [ID=2606.31846] Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models (https://www.alphaxiv.org/abs/2606.31846). Published 2026-06-30 · 15 votes · 148 views: Vision-Language-Action (VLA) models offer a promising framework for robotic manipulation by connecting language instructions, visual observations, and continuous control. However, most existing polici...
2. [ID=2607.01658] Teaching Vision-Language-Action Models What to See and Where to Look (https://www.alphaxiv.org/abs/2607.01658). Published 2026-07-02 · 12 votes · 101 views: Vision-Language-Action (VLA) models have emerged as a promising paradigm for end-to-end autonomous driving. However, existing VLAs' training relies heavily on text-centric visual question answering an...
3. [ID=2607.04637] PixelPilot: Scalable Vision-Language-Action Models for End-to-End Autonomous Driving (https://www.alphaxiv.org/abs/2607.04637). Published 2026-07-06 · 16 votes · 67 views: Vision-Language-Action Models (VLAs), which leverage the advanced reasoning capabilities of Vision-Language Models (VLMs), show promising generalization in complex autonomous driving scenarios. Existi...
4. [ID=2606.23531] BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation (https://www.alphaxiv.org/abs/2606.23531). Published 2026-06-22 · 3 votes · 10 views: Endoscopic retrograde cholangiopancreatography (ERCP) demands precise endoscopic navigation and stable biliary cannulation within a narrow monocular field characterized by specular reflections, partia...
5. [ID=2606.20698] SafeDojo: Safe Reinforcement Learning for VLA via Interactive World Model (https://www.alphaxiv.org/abs/2606.20698). Published 2026-06-15 · 5 votes · 72 views: Safe control is a prerequisite for real-world embodied intelligence, for which safe reinforcement learning has emerged as a promising paradigm. However, existing safe reinforcement learning methods ei...
6. [ID=2607.12640] A Learning-Rate-Gated Failure of GRPO in a Small Language and Vision-Language Model Web Agent: A Controlled Null and Its Mechanism (https://www.alphaxiv.org/abs/2607.12640). Published 2026-07-14 by Monash University, Chinese Academy of Sciences, Pusan National University, Shenzhen University of Advanced Technology · 0 votes · 4 views: Reinforcement learning with verifiable rewards, and Group Relative Policy Optimization (GRPO) in particular, is now run routinely on a supervised checkpoint in the hope of producing a stronger agent. ...
```

No error returned.

### Call 2

Tool: `mcp__alphaxiv__discover_papers`

Parameters (exact JSON):
```json
{
  "keywords": ["GRPO", "VLA", "robot manipulation", "fine-tuning", "reward"],
  "question": "GRPO reinforcement learning fine-tuning of vision-language-action models for robot manipulation policies",
  "difficulty": 6,
  "prioritize": "default"
}
```

Result (no error):
```
1. [ID=2606.31846] Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models (https://www.alphaxiv.org/abs/2606.31846). Published 2026-06-30 · 15 votes · 148 views: Vision-Language-Action (VLA) models offer a promising framework for robotic manipulation by connecting language instructions, visual observations, and continuous control. However, most existing polici...
2. [ID=2606.02313] Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO (https://www.alphaxiv.org/abs/2606.02313). Published 2026-06-01 · 6 votes · 55 views: Vision-Language-Action (VLA) models offer a promising end-to-end paradigm for unmanned aerial vehicles (UAVs) to accomplish complex tasks specified by fine-grained instructions. However, standard supe...
3. [ID=2608.01013] RL Bootstrapping of OpenVLA-OFT for a Novel Robot Embodiment (https://www.alphaxiv.org/abs/2608.01013). Published 2026-08-02 · 3 votes · 10 views: Adapting a pretrained vision-language-action (VLA) policy to a new robot usually assumes embodiment-specific demonstrations. This assumption is especially restrictive for custom robots whose morpholog...
4. [ID=2606.26006] FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation (https://www.alphaxiv.org/abs/2606.26006). Published 2026-06-24 · 3 votes · 41 views: Vision-Language-Action (VLA) models are often constrained by the imitation ceiling imposed by sub-optimal data. While Reinforcement Learning (RL) fine-tuning can surpass this limit, it is notoriously ...
5. [ID=2607.12931] ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning (https://www.alphaxiv.org/abs/2607.12931). Published 2026-07-14 by Sun Yat-Sen University, Zhejiang University, Nanyang Technological University, ACE Robotics · 14 votes · 108 views: Reinforcement Learning (RL) has demonstrated significant potential for improving Vision-Language-Action (VLA) models on complex manipulation tasks. However, its practical scalability remains severely ...
6. [ID=2605.19580] PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models (https://www.alphaxiv.org/abs/2605.19580). Published 2026-05-19 · 12 votes · 41 views: Vision-Language-Action (VLA) models show promising ability in language-guided robotic tasks. However, making VLA policies reliable remains challenging, because a manipulation task is completed through...
7. [ID=2605.16154] Learn Where Outcomes Diverge: Efficient VLA RL via Probabilistic Chunk Masking (https://www.alphaxiv.org/abs/2605.16154). Published 2026-05-15 · 10 votes · 49 views: Reinforcement learning (RL) allows vision-language-action (VLA) policies to generalize beyond their training distribution by optimizing directly for task success, but post-training is computationally ...
8. [ID=2606.14375] Elastic Queries Reinforcement Learning: Self-Aware Policy Execution for VLA Models (https://www.alphaxiv.org/abs/2606.14375). Published 2026-06-12 · 14 votes · 75 views: Vision-language-action (VLA) models are powerful action generators for robot manipulation, but they are typically executed with fixed inference and replanning schedules. This rigidity ignores the unev...
9. [ID=2606.09337] TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation (https://www.alphaxiv.org/abs/2606.09337). Published 2026-06-08 · 16 votes · 151 views: Vision-Language-Action (VLA) models have become a powerful framework for robotic manipulation, and recent studies have introduced tactile or force feedback into VLAs to address contact-rich tasks. How...
10. [ID=2608.05600] LC-GRPO: Bridging Train-Inference Gap for Flow-Based GRPO with Langevin Correction (https://www.alphaxiv.org/abs/2608.05600). Published 2026-08-06 · 1 votes · 3 views: Flow-based generative models are typically sampled by solving a deterministic ordinary differential equation (ODE), whereas online reinforcement learning requires stochastic rollouts for policy explor...
11. [ID=2606.24051] DriveStack-VLA: Render-Teacher Alignment for BEV-Based DeepStack Vision-Language-Action Model (https://www.alphaxiv.org/abs/2606.24051). Published 2026-06-23 · 8 votes · 44 views: Vision-Language-Action driving models convert a pretrained Vision-Language Model into a driving policy, allowing them to use world knowledge and follow language guidances. However, existing VLA drivin...
12. [ID=2603.01928] LaST-VLA: Thinking in Latent Spatio-Temporal Space for Vision-Language-Action in Autonomous Driving (https://www.alphaxiv.org/abs/2603.01928). Published 2026-03-02 by Tsinghua University, University of Macau, Xiaomi · 39 votes · 669 views: While Vision-Language-Action (VLA) models have revolutionized autonomous driving by unifying perception and planning, their reliance on explicit textual Chain-of-Thought (CoT) leads to semantic-percep...
```

No error returned.

## 2. Errors

No tool call errored. Both `mcp__alphaxiv__discover_papers` calls returned results successfully.

## 3. Final answer

Recent papers on GRPO-style RL fine-tuning of VLA models for robotics, found via alphaxiv `discover_papers` (two queries, one recency-prioritized on broad VLA+RL+GRPO terms, one default-prioritized on manipulation/fine-tuning/reward terms):

Most directly on-topic (GRPO/RL fine-tuning of VLA for manipulation or other robot control):

- **Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models** (2606.31846, 2026-06-30) - RL framework for VLA robotic manipulation, addresses inefficiency of existing RL-for-VLA approaches.
- **FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation** (2606.26006, 2026-06-24) - RL fine-tuning to push VLA past the imitation-learning ceiling, tackles RL fine-tuning inefficiency.
- **ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning** (2607.12931, 2026-07-14) - structured exploration to make VLA RL fine-tuning scalable for manipulation.
- **PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models** (2605.19580, 2026-05-19) - policy-optimization variant aimed at VLA reliability in manipulation tasks.
- **Learn Where Outcomes Diverge: Efficient VLA RL via Probabilistic Chunk Masking** (2605.16154, 2026-05-15) - efficient RL post-training for VLA generalization.
- **Elastic Queries Reinforcement Learning: Self-Aware Policy Execution for VLA Models** (2606.14375, 2026-06-12) - RL for adaptive inference/replanning in VLA manipulation policies.
- **TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation** (2606.09337, 2026-06-08) - online RL with tactile/force feedback for contact-rich VLA manipulation.
- **RL Bootstrapping of OpenVLA-OFT for a Novel Robot Embodiment** (2608.01013, 2026-08-02) - RL used to adapt a pretrained VLA (OpenVLA-OFT) to a new robot embodiment without embodiment-specific demos.
- **Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO** (2606.02313, 2026-06-01) - explicitly uses GRPO to fine-tune a VLA model, applied to UAV/aerial navigation rather than manipulation.
- **SafeDojo: Safe Reinforcement Learning for VLA via Interactive World Model** (2606.20698, 2026-06-15) - safe RL for VLA using a world model.

Adjacent / less directly on-topic (surfaced by the queries but not GRPO+VLA+robotics manipulation specifically):

- **A Learning-Rate-Gated Failure of GRPO in a Small Language and Vision-Language Model Web Agent** (2607.12640) - GRPO applied to a web agent, not a robotics VLA.
- **LC-GRPO: Bridging Train-Inference Gap for Flow-Based GRPO with Langevin Correction** (2608.05600) - general flow-based GRPO method, not robotics-specific in the abstract snippet.
- Several autonomous-driving VLA papers (2607.01658, 2607.04637, 2606.24051, 2603.01928) and one medical-navigation paper (2606.23531, BiliVLA) - these are VLA+RL but for driving/endoscopy domains, not general robot manipulation.

Caveat: these are the papers alphaxiv's `discover_papers` tool surfaced for this query; I have not opened any of the papers' full content (no `get_paper_content` calls were made), so descriptions above are based only on the abstract snippets returned by the search tool itself. All listed publication dates (2026-03 through 2026-08) are as returned by the tool.
