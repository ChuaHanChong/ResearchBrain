---
title: VideoMimic End-to-End Reproduction - Steps & Paper Mapping
tags:
  - project
  - active
  - robotics
  - humanoid
  - sim-to-real
  - imitation-learning
aliases:
  - VideoMimic Reproduction
  - VideoMimic Repro Steps
---

# VideoMimic End-to-End Reproduction - Steps & Paper Mapping

> [!abstract] Scope
> Running [[2505.03729|VideoMimic]]'s full pipeline (real2sim → simulation training → inference → real deployment) end-to-end, no steps skipped, to understand the paper via the actual running code. Phases 0-4 run on `hpc-slab-gpu1`; Phase 5 (sim2real) pending robot access. Full plan/risks/open-questions: `docs/visuals/plan-2026-08-12-videomimic-end-to-end-on-hpc-slab-gpu1.html` (predates Phase 5). This doc is the live per-phase checklist + paper↔code grounding, updated as phases run - not a proposal doc like [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]].

Paper section references below are pulled directly from arxiv 2505.03729 (read via local PDF, not paraphrased from the repo READMEs).

---

## Phase 0 - Bootstrap `hpc-slab-gpu1`

Everything under `/data/hanchong/VideoMimic`, using pre-existing `/data/hanchong/miniconda3`.

- [x] `git clone` VideoMimic → `/data/hanchong/VideoMimic`
- [x] Isaac Gym Preview 4 tarball via direct `curl` - 192MB, no NVIDIA account gate (verified live)
- [x] 3 conda envs created: `vm1rs` (py3.12), `vm1recon` (py3.10), `videomimic` (py3.8)
- [x] `videomimic` env: PyTorch 2.3.1 / CUDA 12.1 (per repo's `simulation/setup.md`, **not** Isaac Gym's stale bundled `torch==1.8.1`/py3.7 env yaml - Isaac Gym's own `setup.py` only requires `torch>=1.8.0`, no upper bound, so the newer stack is safe)
- [x] Isaac Gym `pip install -e .` into `videomimic` env
- [x] Gotcha hit + fixed: `ImportError: libpython3.8.so.1.0` - the prebuilt `gym_38.so` needs `$CONDA_PREFIX/lib` on `LD_LIBRARY_PATH`; persisted via `envs/videomimic/etc/conda/activate.d/env_vars.sh` so it's automatic on every `conda activate videomimic`
- [x] Isaac Gym smoke test: headless `gymapi.create_sim()` on GPU 0 → `sim created: True`, GPU pipeline confirmed
- [x] wandb account created (via cmux browser), API key generated, `wandb login` done on gpu1 (`~/.netrc`) - per Q5, follows the paper's own tooling (`import wandb` baked into checkpoint load/save path in `legged_gym/utils/helpers.py`, `rsl_rl/utils/utils.py`, not just logging)
- [x] `videomimic_rl` (`rsl_rl==1.0.2`) + `videomimic_gym` installed (editable) into `videomimic` env
- [x] `vm1rs` env: main `requirements.txt`, Grounded-SAM-2 (SAM2 + Grounding DINO, latter unused by our pipeline - see gotchas), VIMO, BSTRO, jax[cuda12]+jaxls
- [x] `vm1rs` env: pyroki (robot retargeting), pinned commit `70b30a5`
- [x] `vm1recon` env: rebuilt from MegaSaM's own `environment.yml` (torch 2.0.1/CUDA 11.8), DROID-SLAM base compiled, xformers 0.0.22.post7, NKSR (built from `nv-tlabs/NKSR` source, not the dead `huangjh.tech` index), GeoCalib - all import-verified with working CUDA extensions
- [x] Simulation data downloaded via `gdown` (real Google Drive, no quota wall hit): `checkpoints.zip` (3 dirs, IDs match Phase 1's play scripts exactly), `videomimic_captures.zip` (125 files, ≈ paper's 123 curated videos), `unitree_lafan.zip` (40 motions). Checkpoints auto-copied to `videomimic_gym/logs/g1_deepmimic/`.
- [x] real2sim `assets.zip` downloaded (HuggingFace, 33.9GB), integrity-verified (`unzip -t`, clean), extracted to `real2sim/assets/` (37GB): `body_models/`, `checkpoints/`, `ckpt_raft/`, `ckpt_sam2/`, `configs/`, `robot_asset/`. wget stalled once mid-download (rate dropped to <200KB/s on a long-lived connection); killing and resuming with `wget -c` on a fresh connection recovered full speed.

**Paper grounding for this phase:** none directly - this is pure infra. The two conda-env split (`vm1rs`/`vm1recon`) mirrors real dependency conflicts the authors hit (MegaSaM needs `xformers≤0.0.27` → CUDA 11.8; NKSR also CUDA 11.8), not an artificial repo-hygiene choice.

**Gotchas hit (worth knowing if reproducing this):**
- `chumpy`/`torch-scatter` setup.py break inside pip's isolated build venv (old `pip.main()` API / needs `torch` importable at build time) → `pip install --no-build-isolation`.
- Conda envs weren't isolated from `~/.local` user-site packages (`PYTHONNOUSERSITE` unset) - silently used the wrong torch/CUDA build for a compile. Fixed by persisting `PYTHONNOUSERSITE=1` in every env's `activate.d`.
- `pkg_resources` missing on setuptools≥81 broke a build - pinned `setuptools<81`.
- `pycg.huangjh.tech` / `nksr.huangjh.tech` (the paper-era custom package hosts) are dead (NXDOMAIN). `python-pycg` installs fine from plain PyPI (loses only the GUI-visualizer extras, irrelevant headless); NKSR now lives at `nv-tlabs/NKSR` on GitHub, builds from source with no pin conflict.
- Installing `open3d`/`GeoCalib` silently upgraded `numpy` past MegaSaM's `1.26.3` pin more than once, and one of those upgrades left **duplicate dist-info registrations** (numpy and scipy both showed two installed versions simultaneously) - corrupted scipy's compiled Fortran bindings (`dfitpack_int` `TypeError`) in a way that persisted across 3 different scipy versions until a full purge (`pip uninstall` ×2 + `rm -rf` the package dir) and clean reinstall.

---

## Phase 1 - Inference gate (pretrained checkpoints)

**Purpose:** sanity gate before Phase 3's multi-day training spend - confirms Isaac Gym + checkpoint loading + viser viz work, using the authors' own checkpoints, before we burn compute.

| Script | Checkpoint | Maps to |
|---|---|---|
| `play_mcpt_policy.sh` *(repo typo `playt_` fixed, renamed on gpu1)* | `20250410_063030` | **Stage 1: MoCap Pre-Training** (raw MCPT, full target-joint conditioning) |
| `play_terrain_policy.sh` | `20250502_124756` | **Stage 3: Distillation** (DAgger-distilled, trained w/ human-video terrain data) |
| `play_flat_policy.sh` | `20250414_170842` | **Stage 3: Distillation** (DAgger-distilled, AMASS/flat-only, comparison baseline) |

Both terrain/flat are **Stage 3**, not Stage 2 vs 3 as the README implies - verified via each script's `--task` flag (`_dagger` on both). No shipped checkpoint for raw **Stage 2: Scene-Conditioned Tracking** or **Stage 4: Under-conditioned RL Finetuning**.

- [x] `play_mcpt_policy.sh` - confirmed working, robot rendered + `Clip Playback` panel showing LAFAN clip selection (e.g. `env_25_walk2_subject4_d0`)
- [x] `play_terrain_policy.sh` - confirmed working, robot rendered standing on an actual rough terrain mesh in viser
- [x] `play_flat_policy.sh` - confirmed working, robot rendered on flat ground
- [x] Viser via SSH tunnel - all 3 auto-assigned different ports (8080/8081/8082, no conflict) since 8080 was already taken; tunneled all 3 and visually verified each in a browser

**Gotchas hit:**
- Both `play_mcpt_policy.sh` (typo'd `playt_`) and `play_flat_policy.sh` hardcode `--env.deepmimic.amass_replay_data_path="lafan_single_walk/*.pkl"` - that subfolder doesn't exist in the downloaded `unitree_lafan.zip` (only `lafan_walk_and_dance/` and `lafan_replay_data/` do). Fixed both scripts in place (`lafan_single_walk` → `lafan_walk_and_dance`).
- All 3 runs took an unusually long time between "Loading model from..." and actually rendering in viser - terrain ~8min, flat ~18min, MCPT ~21min - despite active GPU compute (30%+ SM utilization) the whole time, no errors, no deadlock signature (checked via GPU utilization + `/proc` state; `py-spy` stack dump wasn't available - blocked by no sudo). Concluded genuine (if very slow) one-time warmup, not a bug - all 3 eventually rendered correctly. Renamed `playt_mcpt_policy.sh` → `play_mcpt_policy.sh` on gpu1, fixing the repo's own typo.

**Paper grounding:** Stage 1 = Sec 4 "Stage 1: MoCap Pre-Training" (bridges human→robot embodiment gap, LAFAN data). Stage 3 = Sec 4 "Stage 3: Distillation" (DAgger, drops target-joint/root-roll-pitch observation, keeps proprioception+heightmap+root-direction).

---

## Phase 2 - Real2sim on the bundled demo video

Step-by-step (not one-shot `process_video.sh`), matched against **Sec 3** end to end. Real2sim's own code has 5 numbered directories: `stage0_preprocessing`, `stage1_reconstruction`, `stage2_optimization`, `stage3_postprocessing`, `stage4_retargeting` - **unrelated to Phase 3's Stage 1-4 RL training numbering below**, same numerals, two independent pipelines.

- [x] **Stage 0: Preprocessing** (`stage0_preprocessing/` - Human Detection & Pose Estimation) - **Sec 3.1 "Preprocessing"**: actual execution order (per `preprocess_human.sh`) is Grounded-SAM-2 (detection+association across frames) → ViTPose (2D keypoints J₂D) → VIMO (per-frame 3D SMPL pose θ, shape β, joints J₃D) → BSTRO (foot contact regression) - note this differs from the paper's own prose order on p.4 (SAM2 → VIMO → ViTPose → BSTRO, i.e. 2nd/3rd/4th/5th sentence); harmless, VIMO and ViTPose are independent (both only consume SAM2's masks/bboxes, neither reads the other's output). Ran on the bundled `sitting_standing` demo (254 frames), via `preprocess_human.sh`. Output: 764 mask files, 508 pose files, 254 mesh files, 255 contact files - all 4 sub-steps confirmed.
- [x] **Stage 1: World Environment Reconstruction** (`stage1_reconstruction/`) - also **Sec 3.1**, scene half: world point cloud from MegaSaM (per-frame depth Dᵗ, camera pose [R|t]ᵗ, shared intrinsics K) or MonST3R. Also does SLAHMR-style coarse positioning (SfM focal length + 2D/3D limb-length ratio → coarse global trajectory), seeding Stage 2. Ran MegaSaM (Option A) on all 254 frames - Global Bundle Adjustment converged, 1.28GB HDF5 output.
- [x] **Stage 2: MegaHunter Optimization** (`stage2_optimization/` - Human Motion and World Alignment) - **Sec 3.2 "Joint Human–Scene Reconstruction"**: refines Stage 1's coarse trajectory by jointly solving human global translations γ¹:ᵀ, orientations φ¹:ᵀ, local poses θ¹:ᵀ, and scene scale α. Objective `argmin w3D·L3D + w2D·L2D + L_Smooth`, Levenberg-Marquardt solver in JAX. Paper reports **~20ms per 300-frame sequence on an A100 after compilation**. Our run: code pads 254→300 frames (matches documented behavior), converged in 4 iterations, **solved in 8.94s** after JIT warmup (cost 104.2610→104.2608), optimized scale α=4.36. Cost-graph log showed exactly the function names documented in our code comments (`alignment_cost_with_residual_root_rotation`, `local_pose_alignment_cost`, `temporal_smoothness_cost` etc, 2397 costs/901 variables) - real confirmation the paper↔code mapping is accurate.
- [x] **Stage 3: Postprocessing** (`stage3_postprocessing/` - Gravity Calibration & Mesh Generation) - **Sec 3.3 "Generating Simulation-Ready Data"**: GeoCalib (gravity alignment) → NKSR (point-cloud→mesh meshification). Our run: GeoCalib 2.35s (Roll 1.2°, Pitch -7.4°), pointcloud filtering 20.46s (5.5M→18.6K points), two-round NKSR meshification 38.12s - **total 74.27s**, close to the paper's claimed ~60s/300-frame. Outputs: `background_mesh.obj`, 2 pointcloud `.ply` files, `gravity_calibrated_keypoints.h5`, `gravity_calibrated_megahunter.h5`.
- [x] **Step 4: Robot Motion Retargeting** (`stage4_retargeting/`) - note the repo itself calls this "Step 4," not "Stage 4" (0-3 are "Stage," the last one breaks pattern). PyRoKi retargets to G1 under joint-limit/contact/collision constraints, detailed in the paper's Sec A.3 appendix. Our run: 254 timesteps (padded to 300), **optimization finished in 44.53s** - paper claims ~10s/clip on A100, ours ~4.4x slower (noted honestly, not investigated further - could be GPU contention, iteration-count defaults, or hardware differences). Saved `retarget_poses_g1.h5`.
- [x] Visualize via `complete_results_egoview_visualization.py` - ego-view render 8.22s, `depthimg_color_*.png` saved to `output_calib_mesh/.../ego_view/`. Viewed live via viser (SSH tunnel :8081, cmux browser): 254-frame scene loaded and interactive, confirmed via screenshot + clean console (WebGL healthy, no errors).

**Gotchas hit in Stage 0:**
- `vm1rs` had unpinned torch 2.13.0 (too new for the node's CUDA 12.4 driver) - the repo's own `docs/setup.md` specifies `torch==2.5.1+cu124` under "Core Dependencies," a step I'd skipped in Phase 0. Installed it.
- ViTPose (`mmpose`) was never installed in Phase 0 at all - a genuine gap. Installed via `openmim` + `mmcv==1.3.9` + `ViTAE-Transformer/ViTPose` (same `pkg_resources`/`setuptools<81` and `--no-build-isolation` pattern as Phase 0's other fixes).
- ViTPose then hit a real numpy 2.x incompatibility: `topdown_heatmap_base_head.py:71` assigns a reshaped 1-element array into a scalar slot, which numpy<2 silently allowed and numpy≥2 rejects (`ValueError: setting an array element with a sequence`). Downgrading numpy env-wide broke `jax` (needs numpy≥2.1 for `StringDType`) - `vm1rs` serves both, so a blanket downgrade wasn't viable. Patched the one line instead: `.reshape(-1)` → `.reshape(-1)[0]`.

**Gotchas hit in Stage 1:**
- MegaSaM's own `UniDepth` submodule (`third_party/megasam-package/UniDepth/`) imports `huggingface_hub.PyTorchModelHubMixin`, which needs `httpx` - missing in `vm1recon`. Installed it.
- That same import chain then hit a broken `wandb` install: `vm1recon`'s `protobuf 5.29.6` is incompatible with `wandb==0.18.7`'s bundled generated protobuf code (`ImportError: cannot import name 'Deprecated' from wandb.proto.wandb_telemetry_pb2` - a common protobuf-5.x break for older packages). Downgraded to `protobuf<5` (landed on 4.25.9) rather than bumping wandb off its `environment.yml`-pinned version.

**Gotchas hit in Stage 3:** two more missing `vm1recon` deps, same pattern as Stage 1 - `docstring_parser` (needed by `tyro`) and `rtree` (needed by trimesh's ray-triangle intersection, used in NKSR's hole-filling ray-cast step). Both just missing installs, not real bugs.

**Reconstruction baseline to compare against (Sec 5.1, Table 2):** VideoMimic reports WA-MPJPE **112.13**, W-MPJPE **696.62**, Chamfer Distance **0.75** on a SLOPER4D subset, beating WHAM*/TRAM baselines. Not something we can reproduce exactly on the bundled demo video (different clip, no ground truth), but the qualitative pipeline output should look structurally similar.

Sec 3 + Appendix A code mapping now lives as inline comments in the local clone (`data/.repositories/VideoMimic`), not here - per the plan's original approach.

---

## Phase 3 - Full 4-stage RL training

- [x] **Stage 1: MoCap Pre-Training** (`train_stage_1_mcpt.sh`) - **Sec 4 "Stage 1: MoCap Pre-Training"**: MoCap pretrain on LAFAN, full target-joint conditioning, bridges human→robot embodiment gap. **DONE** (2026-08-12 → 2026-08-16, ~3.9 days): `max_iterations=100000` reached, `nproc-per-node=4`, `num_envs=4096`, final checkpoint `model_100000.pt` saved (201 checkpoints total, every 500 iters), wandb run `bp3505ni` synced clean. **Gotcha**: relaunch after an earlier 8192-envs experiment crashed once with `CUDA error: illegal memory access` inside PhysX `env.reset()` - Isaac Gym GPU-pipeline corruption from a stale process (Phase 2's viser viz server, PID left running, holding GPU0 memory) contending with PhysX's GPU context. Fixed by killing the stale process and relaunching on a clean GPU. **Gotcha**: `train_stage_1_mcpt.sh` had a stray trailing backtick (pre-existing, harmless to the completed run since bash had already read past it at launch, but broke any future re-run) - removed, re-synced, `bash -n` verified on all 4 stage scripts.
- [~] **Stage 2: Scene-Conditioned Tracking** (`train_stage_2_terrain_rl.sh`) - **Sec 4 "Stage 2: Scene-Conditioned Tracking"**: init from Stage 1, add heightmap conditioning (residual, weight 0→learned), DeepMimic-style tracking on reconstructed terrains + human-video motions. **RUNNING** (launched 2026-08-16): `LOAD_RUN` changed from the script's default (repo's pretrained `20250410_063030_g1_deepmimic`) to our own Stage 1 run `20260812_142531_g1_deepmimic`, so the pipeline stays self-consistent end-to-end. `--resume` continues the iteration counter (100001→200000, another 100k iters on top of Stage 1's). ~6.6s/iter (slower than Stage 1's 3.3s - heavier scene: 123 human-video-reconstructed terrain meshes loaded per env). tmux session `vm_train_s2`, log `/tmp/stage2_train.log`. **Gotcha**: first launch attempt crashed immediately (`ImportError: libpython3.8.so.1.0`) - conda activation done in the outer `ssh` command doesn't carry into a fresh `tmux new-session -d`, which spawns its own shell; fix is sourcing conda + activating the env *inside* the tmux command string, not before it.
- [ ] **Stage 3: Distillation** (`train_stage_3_distillation.sh`) - **Sec 4 "Stage 3: Distillation"**: DAgger distill to reduced-obs policy: drops target joints/root roll-pitch, keeps proprioception + heightmap + root-direction.
- [ ] **Stage 4: Under-conditioned RL Finetuning** (`train_stage_4_rl_finetune.sh`) - **Sec 4 "Stage 4: Under-conditioned RL Finetuning"**: RL finetune the reduced-obs policy; can now mix in lower-quality reference motions since exact-joint tracking is no longer required.

**Policy learning method:** PPO, Rudin et al.'s implementation (= `rsl_rl`), running in Isaac Gym.

**Observations:** proprioceptive - joint positions/velocities, angular velocity, projected gravity, previous actions (history length 5) - plus target-related: target joint angles, target root roll/pitch, desired root direction (x-y offset + yaw, robot-local frame). Scene-conditioned stages add an 11×11 heightmap patch at 0.1m intervals. Critic gets extra privileged observations the actor doesn't see (paper's Table 3).

**Batched tracking:** Reference State Initialization (RSI, start episodes mid-motion, not just at t=0) + motion load-balancing (upweight motions with lower success rate), per Tessler et al.

**Rewards:** tracking-term-driven - link/joint position, joint velocity, foot-contact matching - plus an action-rate penalty and a few anti-exploit penalty terms. Deliberately minimal hand-tuning (full formulation Sec B.1; matches `g1_deepmimic_config.py`'s `rewards.joint_pos_tracking_k` / `link_pos_tracking_k` / `feet_contact_matching`).

**Data:** paper's 123 curated videos ≈ `videomimic_captures.zip`; LAFAN-on-G1 ≈ `unitree_lafan.zip`.

**Sanity check (Fig. 6):** without MPT, success rate stays near-zero through ~30k iterations; with MPT it jumps to ~0.8+ around 15k. Our Stage 1→2 run should show the same divergence - if not, something's off in data/reward wiring.

---

## Phase 4 - Close the loop

- [ ] Feed Phase 2's own real2sim output (`retarget_poses_g1.h5` + `background_mesh.obj`) into `deepmimic.human_video_folders` for a short Stage-2-style run
- [ ] Play back resulting checkpoint, compare against pretrained/Phase 3 checkpoint

Not covered by a specific paper section (the paper trains on its own 123-video corpus wholesale) - this phase is our own validation that the code path the paper describes for *any* video generalizes to a video we processed ourselves, not just the authors' curated set.

---

## Code annotation - tensor/array shapes

Every tensor/array in `real2sim/` (46/46 files) + `simulation/videomimic_gym/legged_gym/` (33/33 files) + VideoMimic-specific additions in `simulation/videomimic_rl/rsl_rl/` (4 files) + `sim2real/videomimic_real/` (both files) carries a verified `# (shape)` comment, ground-truth checked against real gpu1 h5/pkl artifacts and a live isolated Isaac Gym query. Excluded: `real2sim/third_party/`, `sloper4d_eval_script/`, generic upstream `legged_gym`/`rsl_rl` internals. 13 unresolved `(?, ...)` markers remain where source isn't vendored locally (MegaSam/MonST3R internals, missing SMPL model files) - honestly marked, not guessed. All files compile clean, synced to gpu1, md5-verified.

---

## Phase 5 - sim2real deployment (pending robot access)

Paper Sec 5.2: real deployment on a **23-DoF Unitree G1 at 50Hz onboard**, Kp=75 low joint gains, Fast-LIO2 for LiDAR odometry + real-time height-mapping. Two sim2real tricks made it work: (i) relaxed episode-termination tolerances relative to the reference motion, (ii) injecting realistic physics perturbations during training.

- [ ] Secure a G1 (or compatible humanoid) + onboard Jetson
- [ ] Jetson: ROS 1 Noetic setup
- [ ] Install elevation-mapping code (`ArthurAllshire/elevation_mapping_humanoid`)
- [ ] Checkpoint: our own Phase 3/4 JIT export, or the repo's provided ones - note the repo's default paths (`20250414_170842_g1_deepmimic_dict.pt`, `20250502_124756_g1_deepmimic_dict.pt`) are the **exact same checkpoint IDs** as Phase 1's `play_flat_policy.sh`/`play_terrain_policy.sh` - same trained policies, sim playback vs. real deployment
- [ ] Build `videomimic_inference_real.cpp` against ROS + torch + CUDA (`cmake` with `CMAKE_PREFIX_PATH`, `CMAKE_CUDA_ARCHITECTURES` set to the Jetson's compute capability)
- [ ] Run via `scripts/start_robot.sh` (elevation mapping + inference), passing the network interface (e.g. `eth0`)

---

## Cross-References
- [[2505.03729|VideoMimic]] - the paper itself
- [[2602.15733|MeshMimic]] - improves VideoMimic's reconstruction stage; anchor of [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]]
- [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2: Terrain-Extended DDR]] - this reproduction is groundwork for that research direction
