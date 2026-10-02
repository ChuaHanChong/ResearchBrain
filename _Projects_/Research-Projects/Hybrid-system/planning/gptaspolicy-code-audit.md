# GPT-as-Policy code completeness audit

Repo: `https://github.com/anonymous-report-421/GPT-as-Policy`
Clone: `repo/GPTasPolicy_reference`, commit `8f3d362` "Initial public release", 2026-09-14
Audited: 2026-09-19

## Verdict

**Complete as released, not runnable standalone.**
Every file the authors say they shipped is present and hash-verified.
The harness is whole; the simulator, the policy weights and the model backend are deliberately external.

## Evidence

### 1. Self-certified manifest: 851/851 exact

`release-manifest.json` lists every file with `bytes` + `sha256`.

| Check | Result |
|---|---|
| Files listed | 851 |
| Present on disk | 851 |
| SHA-256 match | 851 |
| Missing | 0 |
| Mismatched | 0 |
| Tracked but unlisted | 1 (`release-manifest.json` itself) |

No truncation, no stripped file, no silent redaction.

### 2. Test suite: 597 pass, 5 fail, all 5 environmental

Ran on Python 3.13 with `requirements-tools.txt` only.

```
597 passed, 5 failed, 10 skipped, 13 subtests passed in 51.13s
```

| Failure | Root cause | Code defect? |
|---|---|---|
| `test_batch.py` x3 | `batch.py:31 enable_subreaper()` calls `prctl(PR_SET_CHILD_SUBREAPER)`, Linux-only. macOS: `dlsym(RTLD_DEFAULT, prctl): symbol not found` | No, Linux-only feature |
| `test_publication.py` | macOS `/var` to `/private/var` symlink makes two equal paths compare unequal | No, macOS path artifact |
| `test_annotation_dashboard.py` | Binds `0.0.0.0` then connects to `127.0.0.2`. Linux routes all of `127.0.0.0/8` to loopback; macOS does not | No, Linux-only networking assumption |

Zero `TODO`, `FIXME`, `NotImplementedError` across 188 Python files / 24,953 LOC.
The only "placeholder" hits are a report-site UI string `existing_debug_placeholder`, not stubbed logic.

### 3. What the code does NOT contain

Stated in `README.md`, verified by import scan. The path name decodes under XPolicyLab's public convention `<bench>-<ckpt_name>-<env_cfg_type>-<action_type>-<seed>`, so `RoboDojo-sim-arx_x5-joint-0` is bench `RoboDojo`, run nickname `sim`, robot `arx_x5`, joint-space actions, seed 0.

| Missing | Referenced at | Where to obtain |
|---|---|---|
| Isaac Sim 5.1 / Isaac Lab | `robodojo_server/server.py` `from isaaclab.app import AppLauncher` | NVIDIA |
| RoboDojo source + assets | `from env.global_configs import ROOT_DIR, BENCHMARK`, `task.{BENCHMARK}.task_registry` | `RoboDojo-Benchmark/RoboDojo`, commit `ee67a14` pinned in `SOURCE.json`. Eval-only; policies live in the `XPolicyLab` submodule |
| OpenPI / JAX | `pi05_server/server.py` `from openpi.policies.policy_config import create_trained_policy` | Vendored inside `XPolicyLab/policy/Pi_05/openpi/`, upstream `Physical-Intelligence/openpi`. Pinned `432f82b` is not a branch head or tag upstream, so it is a specific commit or the vendored fork |
| pi05 **weights** | `SOURCE.json` path `/mnt/rollout/.../RoboDojo-sim-arx_x5-joint-0/59999` | Not in this release. **Reproducible**: the training config `pi05_base_aloha_full_sim_arx-x5_seed_0` is the public default of `OPENPI_TRAIN_CONFIG_NAME` in `XPolicyLab/policy/Pi_05`, run via its `process_data.sh` + `train.sh`. Recipe from RoboDojo paper: init `gs://openpi-assets/checkpoints/pi05_base`, batch 256, 60K steps, matching the `59999` step dir |
| Model backend | `codex_backend/config.toml` `base_url = "https://gateway.example.invalid"` | own LiteLLM gateway + `OPENAI_API_KEY` |
| Codex CLI | `cluster_entrypoint.sh` | OpenAI |
| `cv2`, `pxr` (USD), `torch` | sim-side modules | upstream sim env |

Cluster paths are hardcoded to `/mnt/rollout/robodojo_mixed_control` in several operational scripts, so those need editing for any other host.

### 4. What IS fully readable

- Gate prompt verbatim, sha256-pinned in `SOURCE.json`: `skill/gate_prompt.md`
- Full decision loop: `robodojo_server/client.py`, `session.py`, `protocol.py`, `rpc.py`
- Correction kinematics and clamps: `action_edit_kinematics.py`, `kinematics.py`
- Diagnostics passed to the model: `proposal_diagnostics.py`
- Response validation and takeover rules: `validation.py`, `gate_assessment.py`
- 60 test files covering the contract
- Published results: `public_results/` (`data.json`, `evaluation_cases.json`, `scores.csv`, `provenance.json`)

### 5. Can the release reproduce the published numbers?

Partly. `public_results/provenance.json` has `"scope": "article-clips-only"`, records `results_sha256` and an `official_sha256` against robodojo-benchmark.com, and states `raw_annotations_included: false`, `full_rollout_videos_included: false`.
It carries no code hash and no run date, so the published rows cannot be tied to commit `8f3d362`.
`SOURCE.json` also reports `status: "native_integration_verified_company_backend_not_yet_run"`, meaning this released integration path had not itself been run end to end at release time.
Treat `public_results/` as reported outcomes, not as artifacts this code is proven to regenerate.

## Implication for the gated System-2 plan

The harness is reusable as-is for the coupling and request-type axes.
The real blockers are Isaac Sim 5.1 plus a GPU host, not the orchestration code.
The pi05 checkpoint is a cost problem rather than an availability problem: config and training entrypoint are public, so it is a 60K-step retrain.

`accel` and ActProbe cannot be computed from anything this repo exposes.
`actions.npz` is post-clipping policy output only; denoising velocities live inside OpenPI.
A Phase 0 detector needs a hook in `pi05_server/`, not in the harness.

No latency instrumentation exists anywhere in `hybrid_rollout/`, confirming the missing-latency-number finding in the design plan.
