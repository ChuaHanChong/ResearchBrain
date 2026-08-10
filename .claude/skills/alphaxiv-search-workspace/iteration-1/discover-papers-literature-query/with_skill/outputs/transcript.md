# Transcript: alphaxiv-search skill eval

Task: search alphaxiv for recent papers on using GRPO-style reinforcement learning to fine-tune vision-language-action models for robotics

Skill followed: `/Users/chuahanchong/Documents/Projects/ResearchBrain/.claude/skills/alphaxiv-search/SKILL.md` (Literature Review use case: run `discover_papers`, re-run with varied keywords/higher difficulty to fill gaps, then synthesize).

## 1. Tool calls

### Call 1

Tool: `mcp__alphaxiv__discover_papers`

Parameters (exact JSON):
```json
{
  "keywords": ["GRPO", "vision-language-action", "reinforcement learning"],
  "question": "Recent papers using GRPO-style (group relative policy optimization) reinforcement learning to fine-tune vision-language-action (VLA) models for robotics, covering RL post-training of robot manipulation and control policies.",
  "difficulty": 6,
  "prioritize": "recency"
}
```

Error: none.

Result (verbatim):
```
1. [ID=2606.31846] **Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models** (https://www.alphaxiv.org/abs/2606.31846). Published 2026-06-30 · 15 votes · 148 views: Vision-Language-Action (VLA) models offer a promising framework for robotic manipulation by connecting language instructions, visual observations, and continuous control. However, most existing polici...
2. [ID=2607.08409] **When Synthetic Speech Is All You Have: Better Call GRPO** (https://www.alphaxiv.org/abs/2607.08409). Published 2026-07-09 · 6 votes · 20 views: LLM-based ASR adapted to regulated domains such as banking is bottlenecked by privacy: real speech is costly and legally constrained to collect, making synthetic text-to-speech (TTS) an attractive sub...
3. [ID=2606.23531] **BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation** (https://www.alphaxiv.org/abs/2606.23531). Published 2026-06-22 · 3 votes · 10 views: Endoscopic retrograde cholangiopancreatography (ERCP) demands precise endoscopic navigation and stable biliary cannulation within a narrow monocular field characterized by specular reflections, partia...
4. [ID=2607.04637] **PixelPilot: Scalable Vision-Language-Action Models for End-to-End Autonomous Driving** (https://www.alphaxiv.org/abs/2607.04637). Published 2026-07-06 · 16 votes · 67 views: Vision-Language-Action Models (VLAs), which leverage the advanced reasoning capabilities of Vision-Language Models (VLMs), show promising generalization in complex autonomous driving scenarios. Existi...
5. [ID=2606.18594] **Benchmarking Action Spaces in Reinforcement Learning for Vision-based Robotic Manipulation** (https://www.alphaxiv.org/abs/2606.18594). Published 2026-06-17 · 6 votes · 49 views: In real-world reinforcement learning (RL), the choice of action space can play a key role in shaping motion smoothness, safety, and overall task performance. In this study, we evaluate pose increment,...
6. [ID=2605.15964] **WorldVLN: Autoregressive World Action Model for Aerial Vision-Language Navigation** (https://www.alphaxiv.org/abs/2605.15964). Published 2026-05-15 · 24 votes · 425 views: Aerial vision-language navigation (VLN) requires agents to follow natural-language instructions through closed-loop perception and action in 3D environments. We argue that aerial VLN can be formulated...
```

### Call 2

Tool: `mcp__alphaxiv__discover_papers`

Parameters (exact JSON):
```json
{
  "keywords": ["VLA", "GRPO", "robot manipulation"],
  "question": "RL post-training methods that apply group relative policy optimization (GRPO) or GRPO-style reward-based fine-tuning directly to vision-language-action policies for robotic manipulation and control, as an alternative to supervised imitation learning.",
  "difficulty": 7,
  "prioritize": "recency"
}
```

Error: none.

Result (verbatim):
```
1. [ID=2607.27782] **RedFlow: Redirect Failure into Action-Level Corrections for Flow-matching VLA Policy** (https://www.alphaxiv.org/abs/2607.27782). Published 2026-07-30 · 21 votes · 93 views: Flow-matching Vision-Language-Action (VLA) policies have shown strong potential for robotic manipulation but often suffer from compounding errors caused by distribution shifts during deployment. While...
2. [ID=2606.02313] **Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO** (https://www.alphaxiv.org/abs/2606.02313). Published 2026-06-01 · 6 votes · 55 views: Vision-Language-Action (VLA) models offer a promising end-to-end paradigm for unmanned aerial vehicles (UAVs) to accomplish complex tasks specified by fine-grained instructions. However, standard supe...
3. [ID=2605.19580] **PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models** (https://www.alphaxiv.org/abs/2605.19580). Published 2026-05-19 · 12 votes · 41 views: Vision-Language-Action (VLA) models show promising ability in language-guided robotic tasks. However, making VLA policies reliable remains challenging, because a manipulation task is completed through...
4. [ID=2606.24051] **DriveStack-VLA: Render-Teacher Alignment for BEV-Based DeepStack Vision-Language-Action Model** (https://www.alphaxiv.org/abs/2606.24051). Published 2026-06-23 · 8 votes · 44 views: Vision-Language-Action driving models convert a pretrained Vision-Language Model into a driving policy, allowing them to use world knowledge and follow language guidances. However, existing VLA drivin...
5. [ID=2608.01013] **RL Bootstrapping of OpenVLA-OFT for a Novel Robot Embodiment** (https://www.alphaxiv.org/abs/2608.01013). Published 2026-08-02 · 3 votes · 10 views: Adapting a pretrained vision-language-action (VLA) policy to a new robot usually assumes embodiment-specific demonstrations. This assumption is especially restrictive for custom robots whose morpholog...
6. [ID=2607.06564] **Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation** (https://www.alphaxiv.org/abs/2607.06564). Published 2026-07-07 · 25 votes · 165 views: Recently, Vision-Language-Action (VLA) models have demonstrated strong generalization across diverse tasks. However, effective robotic manipulation in physical environments fundamentally requires geom...
7. [ID=2607.08448] **Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents** (https://www.alphaxiv.org/abs/2607.08448). Published 2026-07-09 by Chinese Academy of Sciences, Tsinghua University, Purdue University, HKUST, Infinigence-AI, Zhongguancun Academy, Striding AI · 70 votes · 1302 views: Language-conditioned manipulation requires both precise contact-rich control and robust reasoning over language, scenes, and long horizons. End-to-end Vision-Language-Action (VLA) models provide stron...
8. [ID=2606.25800] **ROAD-VLA: Robust Online Adaptation via Self-Distillation for Vision-Language-Action Models** (https://www.alphaxiv.org/abs/2606.25800). Published 2026-06-24 · 10 votes · 102 views: Effective online adaptation of vision-language-action (VLA) models remains challenging, as sparse rewards provide weak supervision for high-dimensional autoregressive action policies. Although self-di...
9. [ID=2606.10184] **Dropout-GRPO: Variational Stochasticity for Continuous Latent Reasoning** (https://www.alphaxiv.org/abs/2606.10184). Published 2026-06-08 · 6 votes · 35 views: Group Relative Policy Optimization (GRPO) relies on the diversity of $K$ rollouts within each group; otherwise, the group-mean advantage $A^{(k)} = r^{(k)} - \mu_r$ collapses to zero. This presents a ...
```

No other `mcp__alphaxiv__*` tools were called. `get_paper_content` and `answer_pdf_queries` were not needed since the task asked for a paper search/discovery, not a deep read of a specific paper's content.

## 2. Errors

No errors were returned by either call.

## 3. Final answer to the user

Searched alphaxiv (2 `discover_papers` calls, prioritized by recency) for GRPO-style RL fine-tuning of VLA models for robotics. Most directly on-topic hits:

- **Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models** ([2606.31846](https://www.alphaxiv.org/abs/2606.31846), 2026-06-30) - RL framework aimed squarely at VLA robotic manipulation policies.
- **PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models** ([2605.19580](https://www.alphaxiv.org/abs/2605.19580), 2026-05-19) - policy-optimization RL fine-tuning for VLA manipulation reliability.
- **RL Bootstrapping of OpenVLA-OFT for a Novel Robot Embodiment** ([2608.01013](https://www.alphaxiv.org/abs/2608.01013), 2026-08-02, most recent) - RL post-training of OpenVLA-OFT to adapt to a new robot embodiment without embodiment-specific demos.
- **Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO** ([2606.02313](https://www.alphaxiv.org/abs/2606.02313), 2026-06-01) - explicitly GRPO-based RL fine-tuning of a VLA policy, though for aerial UAV navigation rather than manipulation.
- **Benchmarking Action Spaces in Reinforcement Learning for Vision-based Robotic Manipulation** ([2606.18594](https://www.alphaxiv.org/abs/2606.18594), 2026-06-17) - relevant context on RL action-space choices for robotic manipulation (not GRPO/VLA-specific but adjacent).

Weaker/tangential matches surfaced by the searches: Dropout-GRPO (2606.10184, GRPO mechanics for latent reasoning, not robotics), RedFlow (2607.27782), Lift3D-VLA (2607.06564), Harness VLA (2607.08448), ROAD-VLA (2606.25800), DriveStack-VLA (2606.24051) - all VLA-for-robotics papers but none confirmed to use GRPO specifically in the abstract preview. Off-topic hits (ASR speech synthesis, endoscopic navigation, autonomous-driving VLA, aerial world-action-model) were also returned by the broad keyword match and excluded.

Caveat: rankings/abstracts are from `discover_papers` previews only; no `get_paper_content`/`answer_pdf_queries` calls were made to confirm GRPO usage inside the ambiguous ones - would need a follow-up read of PAPO-VLA, Z-1, and the OpenVLA-OFT RL paper to verify their RL algorithm is specifically GRPO (vs. PPO or another group-relative variant) before citing them as GRPO-confirmed.
