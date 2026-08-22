# ACEMemBench

## TODOs

### 260820

- [x] Study RMBench, RoboMemArena, MIKASA-Robo-VLA, RoboCasa365, BEHAVIOR-1K
- [x] Study ACEDojo

### 260821

- [x] Understand the RoboCasa365 data format and identify the inputs and ground truth
- [x] How RoboCasa365 uses MimicGen to generate data

### 260822

- [ ] How to generate data using MimicGen, DexMimicGen
- [ ] Study the three robot memory research directions
- [ ] Study the differences between the 8 memory methods in the papers below
- [ ] Deep dive into robot memory

### Questions

- [ ] QKV relationships
- [ ] cross-attention vs self-attention and their sequence

## Concepts

### Problem

1. Data collection for long-horizon manipulation - demo count scales with horizon, demo-warping (MimicGen) only covers short single-skill tasks, teleop doesn't scale.
2. Simulation subtask connection - generators produce one atomic subtask per rollout, no native stitching into multi-stage episodes; and parallel/vectorized rollout is hard when the renderer isn't built for batching.

### Long-Horizon vs Memory

RMBench's related work makes two separate dismissals:

> "LIBERO-Long and RoboCerebra features long-horizon tasks, but task-relevant information remains observable throughout execution and therefore does not explicitly require memory."

> "RoboCasa, ManiSkill3, ..., BEHAVIOR-1K, and SIMPLER provide diverse manipulation tasks, yet most scenarios emphasize short-horizon interactions or can be solved without relying on historical observations."

Both dismissals conflate two separate axes:

1. **Horizon** - steps to goal. Scalar.
2. **Task Memory Complexity (TMC)** - does the optimal action at t depend on something before t no longer visible in o_t?

RMBench POMDP: history h_t = (o_1:t, a_1:t-1). π*(a_t|h_t) = π*(a_t|o_t) → M(0), memory-free regardless of length. Needs m past obs no longer visible → M(m).

Examples:
- Cabinet→pick→place→close: state stays visible each step. M(0).
- `put_back_block`: block moved off 1-of-4 identical pads, now symmetric, unsolvable from o_t alone. M(1).
- Press Button / Blocks Ranking: count/rank accumulates, no visual trace. M(n).

Long + fully Markovian is possible (BEHAVIOR-1K, RoboCasa365 (built on RoboCasa), LIBERO-Long) - the gap RMBench/MIKASA/RoboMemArena fill by engineering occlusion/symmetry/removal.

### Memory Taxonomy

One task, four memory types in play: robot told "put block back" after moving it itself same episode.

- **Contextual** (working memory) - "3 steps ago, block A→B." Lost at episode end. Without it: sees block in B, no idea it's from A → fails (observation-aliasing).
- **Episodic** (cross-episode) - "Task #47, block A→B, succeeded returning to A." Stored trace, retrievable a different session.
- **Semantic** (abstracted, no instance) - "Blocks go in marked slots, fixed layout." Distilled across episodes.
- **Long-term** (stable, cross-task) - grasp force, layout stability. Backbone across all sessions.

Compression path: contextual → episodic → semantic → long-term.

RMBench's M(m) mostly tests contextual memory only (within-episode) - episodic/semantic/long-term stay untested by current benchmarks (RMBench/RoboMemArena/MIKASA all M(m) = within-episode). Open gap.

## Reading List

### From Prof

- https://scholar.google.com/citations?hl=zh-CN&user=u76xfogAAAAJ&view_op=list_works, https://shenyujun.github.io/
- https://arxiv.org/pdf/2602.15922  # World Action Models are Zero-shot Policies
- https://arxiv.org/pdf/2603.16666  # Fast-WAM: Do World Action Models Need Test-time Future Imagination?
- https://arxiv.org/pdf/2604.15483  # π0.7: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities
- https://arxiv.org/pdf/2603.01229  # RMBench: Memory-Dependent Robotic Manipulation Benchmark with Insights into Policy Design
- https://arxiv.org/pdf/2406.02523  # RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots

### Surveys

- https://arxiv.org/pdf/2510.10903  # Towards a Unified Understanding of Robot Manipulation: A Comprehensive Survey
- https://arxiv.org/pdf/2605.00080  # World Model for Robot Learning: A Comprehensive Survey
- https://arxiv.org/pdf/2512.13564  # Memory in the Age of AI Agents: A Survey
- https://arxiv.org/pdf/2512.22983  # Embodied Robot Manipulation in the Era of Foundation Models: Planning and Learning Perspectives
- https://arxiv.org/pdf/2606.05660  # Safe Embodied AI for Long-horizon Tasks: A Cross-layer Analysis of Robotic Manipulation

### Benchmarks

- https://arxiv.org/pdf/2506.06677  # RoboCerebra: A Large-scale Benchmark for Long-horizon Robotic Manipulation Evaluation
- https://arxiv.org/pdf/2604.16788  # LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks
- https://arxiv.org/pdf/2603.04639  # RoboMME: Benchmarking and Understanding Permanence Memory for Robotic Generalist Policies
- https://arxiv.org/abs/2506.18088  # RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation
- https://arxiv.org/abs/2406.02523  # RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots

Studied, all have KH notes. Direct robot-memory trio (non-Markovian manipulation → explicit memory module → graded task complexity):

- **RMBench** (2603.01229) - 9-task memory-dependent benchmark, graded Task Memory Complexity + Mem-0 modular policy. Field's current reference framing (per General/11 star callout).
- **RoboMemArena** (2605.10921) - 26 long-horizon tasks (1000+ steps, 68.9% memory-dependent), keyframe annotations, real-world eval + PrediMem dual-system VLM.
- **MIKASA** (2502.10550) - RL-focused memory-task taxonomy; MIKASA-Base (general) + MIKASA-Robo (32 tabletop tasks, partial observability).

Scale comparators only, not memory-native:

- **BEHAVIOR-1K** (2403.09227) - 1000 everyday activities, OMNIGIBSON sim, long-horizon but not memory-specific.
- **RoboCasa365** (2603.04356) - 365 kitchen tasks × 2500 scenes, 600h human + 1600h synthetic demos, generalist-robot benchmark.

### Methods

- https://arxiv.org/abs/2608.05042  # BridgeVLA++: A Data-Efficient, Generalizable, and Memory-Augmented Vision-Language-Action Framework for 3D Manipulation
- https://arxiv.org/abs/2603.24576  # Chameleon: Control-Indexed Prospective Memory for Visuomotor Manipulation
- https://arxiv.org/abs/2606.20562  # MemoryWAM: Efficient World Action Modeling with Persistent Memory
- https://arxiv.org/abs/2606.30318  # Chronos: A Physics-Informed Full-History Framework for Non-Markovian Long-Horizon Manipulation
- https://arxiv.org/abs/2608.16885  # τ0-VLA: a Hierarchical Robot Foundation Model with World-Model-Guided Test-Time Computation
- https://arxiv.org/abs/2601.21998  # Causal World Modeling for Robot Control
- https://arxiv.org/abs/2604.15483  # π0.7: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities
- https://arxiv.org/abs/2608.06729  # AtlasVLA: Persistent World-Ego State Modeling for Vision-Language-Action Models

## RoboCasa Data Format

LeRobot format, official Box release (not the newer v3.0 HF-mirror repacks, which use different filenames). Version differs by source: human-collected = v2.1, MimicGen-generated = v2.0.

**3 data types:**

| Type | Tasks | Demos/task |
|---|---|---|
| pretrain-human | 300 | 100 |
| pretrain-mimicgen | 60 | ~10,000 |
| target-human | 50 | 500 |

**Folder layout** (one `lerobot/` per task):

```
lerobot/
├── meta/
│   ├── tasks.jsonl          # task_index -> instruction text
│   ├── episodes.jsonl       # episode_index -> length, tasks
│   ├── info.json            # field dtypes/shapes
│   └── stats.json           # dataset mean/std
├── data/chunk-NNN/
│   └── episode_NNNNNN.parquet   # low-dim, 1 row per timestep
├── videos/chunk-NNN/{camera}/
│   └── episode_NNNNNN.mp4       # real H.264 video, not raw arrays
└── extras/episode_NNNNNN/    # human-collected only, MimicGen has no extras/
    ├── states.npz            # raw MuJoCo state (sim replay only)
    ├── model.xml.gz          # scene description
    └── ep_meta.json          # layout/style/fixtures
```

**`data/` parquet columns** (1 row = 1 timestep):

| Field | dtype | shape | meaning |
|---|---|---|---|
| `action` | float64 | 12 | commanded action |
| `observation.state` | float64 | 16 | proprioception (EE pose + gripper + base) |
| `next.reward`, `next.done` | float32, bool | 1 | reward, episode-end flag |
| `timestamp`, `frame_index`, `episode_index`, `task_index` | - | 1 | bookkeeping |

**Key facts:**

- Videos = 3 cameras (eye-in-hand, agentview-left/right), 256×256, 20fps. Frame index = parquet row index.
- `extras/` is for sim replay only, not training.
- `chunk-NNN` = shard of up to 1000 episodes (`episode_chunk = episode_index // 1000`).
- 1 episode = 1 full task attempt (many frames), not 1 frame.
- Verified sample downloaded to `~/Documents/Projects/ACEMemBench/robocasa/datasets/v1.0/`.

**Training (per-timestep sample, both video + parquet fused by `LeRobotDataset`):**
- Input: 3 camera images + `observation.state` (16-d) + instruction (via `task_index`)
- Label: `action` (12-d) - ground truth, what human/MimicGen actually did that step (imitation learning / BC)
- RoboCasa's BC-Transformer: past 10 timesteps in, next 10 actions out

Pretrain vs fine-tune: same mechanics (same `LeRobotDataset` fuse, same input/label). Only difference - dataset used (`dataset_soup`: pretrain = 300 human + 60 mimicgen tasks; fine-tune = 50 target tasks) and starting weights (fine-tune inits from `--base_model_path` pretrained checkpoint, not random).

**target-human vs eval - same kitchens, different jobs:**
- `target-human` demos = fine-tune training input.
- Eval = live policy rollout in same kitchens, no demo file replayed.

### MimicGen: Input Requirements

Verified against `NVlabs/mimicgen` source. 4 needs:

| # | Requirement | What | Note |
|---|---|---|---|
| 1 | Seed hdf5 | `data/demo_N/{states,actions}` + attrs `model_file`, `env_args` (plain robomimic teleop format) | No `obs` needed - MimicGen replays `states` itself; `obs` only appears in output. ~10 demos/task convention, configurable (`experiment.source.n`) |
| 2 | Working sim env | reconstructed from `env_args`/`model_file`, actually stepped | data without a runnable env is inert |
| 3 | `datagen_info` | added by `prepare_src_dataset.py`, replaying each seed demo | see field table below |
| 4 | Task-specific code | `MG_EnvInterface` subclass (`get_object_poses()` + `get_subtask_term_signals()`) + real `_check_success()` | not derivable from data, hand-written per task. Missing `_check_success` (e.g. RoboCasa `Kitchen` stub = hardwired `False`) blocks the generation loop outright |

**`datagen_info` fields** (per timestep):

| Field | Shape | Meaning |
|---|---|---|
| `eef_pose` | (T,4,4) | end-effector pose |
| `gripper_action` | (T,1) | gripper command |
| `object_poses/<obj>` | (T,4,4) | one per object of interest |
| `subtask_term_signals/<name>` | (T,) | binary; first 0→1 = subtask split point |
| `target_pose` | (T,4,4) | |

### MimicGen: How Synthetic Data Is Generated

Not a learned generator - trajectory stitching + replay, gated by sim success/failure. Verified against MimicGen paper (2310.17596) + source in cloned repo.

| # | Step | What happens |
|---|---|---|
| 1 | Seed | small set of human teleop demos (paper: ~10-50/task) |
| 2 | Parse | each demo auto-split into object-centric subtask segments (e.g. pick-and-place = [grasp, place]); automated success-detection metrics per subtask, not manual labeling |
| 3 | Transform for new scene | pick a reference segment, rigidly transform its target poses to the new object pose: `T'_t = T_O · (T_O')⁻¹ · T_t` (preserves relative gripper-target/object pose per timestep) |
| 4 | Interpolate + stitch | linear (position) + slerp (rotation) bridge from current end-effector pose to the transformed segment's start; segments chained subtask-by-subtask |
| 5 | Execute + reject | robot runs the new trajectory in sim; kept only if task succeeds ("data generation rate" = success/attempts); failed attempts discarded, not fixed |

Known limitations (paper's own): filters on task-success only, not motion quality - linear interpolation has no collision guarantee, kept trajectories can still be jerky/collide. Doesn't handle mobile-nav tasks (excluded from RoboCasa's generated set).

RoboCasa-specific: 8 core skills → subtask sequence template reused across all atomic tasks (minimal per-task human effort). Pipeline in cloned repo: `prepare_src_dataset.py` (extract subtask metadata) → `generate_dataset.py` (generation, per-task JSON config) → separate image/video render pass. Note: `generate_dataset_multicore.py` does not exist in this repo (checked `mimicgen/scripts/` directly) - corrected from an earlier, unverified note.

## Vault Notes

### Deep Dives

- `10_Manipulation-Skill-Learning.md` § 4 - long-horizon task & memory.
  - Core problem: Markov assumption breaks once task spans >1 contact - enemy is visual aliasing.
  - Covers: episodic/retrieval memory (NativeMEM, CAMP, MemER, SAM2Act) + object-permanence/keyframe-history (Out-of-Sight-Still-in-Mind, BPP).
  - Key papers: SAM2Act (architecture+benchmark pair), MemER (minutes-scale VLM retrieval).
  - ELI5 4.1: diary/logbook - robot logs events as they happen, flips back to the relevant page instead of replaying everything. Example: told "grab the scoop you used earlier," recalls "3 steps ago, near the sink" (MemER) instead of rescanning the room.
  - ELI5 4.2: two flavors. Object-permanence - like a baby knowing a toy still exists under a blanket: cup placed in a closed cabinet, robot still "knows" it's there (Out-of-Sight-Still-in-Mind). Keyframe-history - sticky notes instead of full video: remembers "added flour," "cracked egg," not every frame (BPP).
  - One-liner: 4.1 = what happened. 4.2 = what's true now, even unseen.

- `02_Dataset-Benchmark-Environment.md` § 5.2/§5.3 - memory benchmark.
  - §5.3 (5 papers, split from §5.2): RMBench (Task Memory Complexity + Mem-0, field's reference), RoboMemArena (68.9% subtasks memory-dependent), RoboMME, MIKASA, VQ-Memory.
  - §5.2 keeps 7 general capability-diagnostic papers (RoboGraph, ERR@HRI 3.0, etc) - not memory-specific.

- `02_Dataset-Benchmark-Environment.md` § 10 - long-horizon benchmark.
  - Not memory-specific - tests planning/compositionality/error-accumulation instead.
  - Key papers: RoboCerebra (2,972 avg steps), FurnitureBench (hardest published), CALVIN (compositionality), LIBERO family (4 perturbation-axis variants).

### Research Directions

**Decision: no new Manipulation.md direction.** `Embodied-AI.md` B2 already covers manipulation long-horizon-memory (anchors HELM/GTP-FA/RoboFAC/RoboMemArena, LIBERO-Long/Recovery/tabletop) - a new `Manipulation.md` direction on the same axis would be a re-slice, banned by the doc's own rule.

Where the work actually lives:
- Embodied-AI-B2 (Long-Horizon Memory + Failure Recovery Loops) = manipulation long-horizon-memory, filed cross-cutting - bet: cross-episode memory + cause-attributed recovery beats HELM's episode-local uniform rollback.
- Whole-Body-B2 (Large-Workspace Memory for Mobile Manipulation) = mobile/large-workspace-memory (moving-base occlusion, not tabletop) - persistent spatio-semantic memory for objects/state outside the current FOV as the robot moves between rooms.
- Spatial-4D-C3 (Persistent Geometric Memory) = geometric memory, substrate-agnostic - one world-frame memory reused as a persistence layer across occupancy/latent-4D/pointmap representations, tests whether geometric + episodic memory compound.

**Memory-type axis across the three** (event / scene / geometric):
- Embodied-AI-B2 = *event* memory - "what happened." Not spatial.
- Whole-Body-B2 = *scene* memory - "what's out there." Spatial, occlusion-driven.
- Spatial-4D-C3 = *geometric* memory - "what the world looks like." Lower-level, feeds the other two.

## Access

home/zyang/AceDojo

登录账户：zyang
密码：sgres12345
