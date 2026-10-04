# Hybrid System V2 pseudocode

This file is the source of truth for the pseudocode in `hybrid-system-architecture-v2.html`; review changes here with `git diff`.
Each `## ` section below is one box or one arrow: clicking it in the diagram shows this pseudocode in the right panel.
The panel's picture shows the box's IN and OUT, built from the diagram's arrows; this file only holds what you need to build each part.
The `<!-- box: id -->` line under a heading names the diagram box it belongs to; the build fails if a box has no section.
Step codes match the diagram's step squares: A = VLA lane, B = advisor lane, C = offline; numbers follow reading order.

Tags in comments:

- `BUILT: name (file)` means the code exists on hpc today, as named in `_build/notes/`.
- `NOT BUILT` means the design has it and the code does not.
- `PROPOSED: <decision>` means the line follows a pick that is still open in the Decide register.
- `DECIDED: <decision>` means the line follows a decision already made in the Decide register.

# Shared

## Constants

```python
from __future__ import annotations                 # forward type names resolve lazily
from dataclasses import dataclass, field, replace
from enum import Enum, auto
from collections import deque
from contextlib import contextmanager
import itertools, random
from typing import Iterable, Iterator, Literal, Protocol
from math import ceil, log
from statistics import median

# Built values, with their source.
MAX_CORRECTION = (0.05, 0.35)                      # metres, radians. BUILT: validate_response (validation.py)
CHUNK_STEP_MAX_ROWS = 15                           # BUILT: chunk_step (libero/session.py)
EXEC_STEPS = {"LIBERO": 10, "RoboDojo": 15}        # rows per decision. BUILT: LiberoTools.gate_stride; RoboDojo setting
SCORED_ROWS = EXEC_STEPS                           # ACCEL+ scores the planned executed rows (accel_plus.py fix #1)
N_CANDIDATES = 1                                   # candidate chunks per VLA step; improvement plan 9 raises it

# ACCEL+ settings, from the method file (accel_plus.py Cfg); not built.
ALPHA = 0.1                                        # false-alarm rate per part on successes (accel_plus.py)
CUSUM_C = 0.5                                      # CUSUM slack k = CUSUM_C * scale (accel_plus.py)
SHORT_STEPS = 2                                    # rows run when unsure but typical (accel_plus.py)
HIST_WINDOW = 24                                   # executed rows kept for part 5 (accel_plus.py)
EPS = 1e-4                                         # keeps the stall ratio finite (accel_plus.py)
MIN_CHECK_RUNS = ceil(1 / ALPHA) - 1               # fewest check-set runs for the conformal rank

# Evaluation split of LIBERO-Plus factor-levels: disjoint, defined before any training.
TRAIN_LEVELS = TO_MEASURE                          # factor-levels whose runs give fixes; plain LIBERO: own-success noise
EVAL_LEVELS = TO_MEASURE                           # scored by checks() each round; picks ablation arms
FINAL_LEVELS = TO_MEASURE                          # scored once at the end, never by checks()
EVAL_EPISODES = TO_MEASURE                         # episodes per check, same seeds for old and new
MARGIN = PRESET                                    # pre-registered margin of both paired tests
TEST_LEVEL = PRESET                                # pre-registered significance level of both paired tests

# Limits from the robot's spec (to be read), never tuned.
X5_JOINT_STEP = FROM_ROBOT_SPEC                    # X5 URDF velocity limit x 0.04 s; unset: no URDF
STEP_LIMIT = {"LIBERO": (0.05, 0.5), "RoboDojo": X5_JOINT_STEP}   # per row: LIBERO m, rad per axis; RoboDojo per joint
GRIPPER_LIMIT = {"LIBERO": (-1, 1), "RoboDojo": FROM_ROBOT_SPEC}   # (low, high) gripper command per robot
WORKSPACE = FROM_ROBOT_SPEC                        # reachable, allowed box
CONTACT_LIMIT = FROM_ROBOT_SPEC                    # largest predicted contact force
GRIPPER_CLOSED_WIDTH = FROM_ROBOT_SPEC             # at or below it a closed gripper holds nothing

# Flags and unset counts: named, never guessed. Each is measured before it is used; main() refuses an unset one.
STAGE2_ON = False                                  # improvement plan 2: ACCEL+ calibration in main()
PFD_AND_SCENES_ON = False                          # improvement plan 3: PFD root filter, nearby scenes
PFD_EPISTEMIC_CUT = TO_MEASURE                     # PFD score above it counts as epistemic (our use)
SIM_RESET_BUILT = False                            # gap reset: LIBERO restore built; variant rebuild not
LORA_ON = False                                    # improvement plan 7: LoRA fallback allowed
MAX_UNSURE_CALLS_PER_SUBTASK = TO_MEASURE          # unsure calls per subtask before a hand-off
MAX_RECOVERY_TRIES = TO_MEASURE                    # failed recoveries per run before a hand-off
MAX_CODE_ERRORS = TO_MEASURE                       # code-error retries per program; tries = retries + 1 (≤N)
MIN_REPEAT_EPISODES = TO_MEASURE                   # distinct runtime episodes a repair needs to train
LESSONS_PER_CALL = TO_MEASURE                      # repair lessons offered to one advisor call
TREE_BRANCHES = TO_MEASURE                         # fixes tried per gate-fire state
ROOTS_PER_ROUND = TO_MEASURE                       # tree roots searched per offline round, oldest first
SCENES_PER_ROOT = TO_MEASURE                       # nearby start scenes per epistemic root
VERIFY_EVERY = {"LIBERO": 30, "RoboDojo": 45}      # executed VLA rows between verifier calls: three chunks' worth
STALL_ROUNDS = PRESET                              # pre-registered: failed redeploy rounds before fine-tuning
PROGRESS_THRESHOLD = FITTED                        # self-check cut-off, fit in calibrate_gate, never hand-set
AUDIT_DISAGREE_MAX = TO_MEASURE                    # largest verifier-vs-sim disagreement before a round stops
AUDIT_MIN_CALLS = TO_MEASURE                       # fewest audited calls before the rate can stop
AUDIT_RATE = TO_MEASURE                            # share of saved-fix verifier calls audited (our suggestion)
TASK_MEMORY_ON = False                             # improvement plan 11: task memory on
# PROPOSED: How does memory reach the VLA? -> staging
MEMORY_TO_VLA = "staging"                          # a VLA_ROUTES key: hover_over stages the arm
PAIRED_LCB_ON = False                              # improvement plan 12: paired LCB admission, needs SIM_RESET_BUILT
GRASP_MEMORY_ON = False                            # improvement plan 13: grasp memory ranks grasps
SELF_CORRECT_ON = False                            # improvement plan 14: latent monitor watches VLA chunks
SELF_CORRECT_TRIES = TO_MEASURE                    # self-corrections per subtask before call 3
SC_WINDOW = TO_MEASURE                             # MAD window of the mismatch E_t (VLA-Corrector)
SC_LAMBDA_ON = TO_MEASURE                          # T_on = median + SC_LAMBDA_ON * MAD
SC_LAMBDA_OFF = TO_MEASURE                         # T_off = median + SC_LAMBDA_OFF * MAD
SC_CONSECUTIVE = TO_MEASURE                        # steps in a row over T_on before a trigger
SC_COOLDOWN = TO_MEASURE                           # steps after a trigger with no new trigger
LVM_K = TO_MEASURE                                 # steps between the latents the monitor compares
MONITOR_ROBOTS = ("LIBERO",)                       # robots with a trained latent monitor
SC_ACTIVE = SELF_CORRECT_ON and robot.name in MONITOR_ROBOTS   # self-correction runs only here
LCB_PAIRS = TO_MEASURE                             # M: shared-randomness pairs per admission event (RE-0)
LCB_BUDGET = TO_MEASURE                            # most paired suffix rollouts per offline round
CELL_EPISODES = TO_MEASURE                         # episodes per (task, level) cell, per-cell arm
CELL_TOLERANCE = PRESET                            # pre-registered: largest allowed per-cell drop, Holm-tested
LCB_LEVEL = PRESET                                 # pre-registered: confidence level of the paired LCB (RE-0)
GRASP_NEIGHBOURS = TO_MEASURE                      # k nearest past grasps in the Beta posterior
GRASP_PRIOR = TO_MEASURE                           # (a, b): grasp memory's Beta prior
MIN_LESSON_SUPPORT = TO_MEASURE                    # agreeing repairs before a new lesson (Optimus-R)
INVERT_ERROR_CUT = TO_MEASURE                      # inversion error under it: the VLA can make it
ALIAS_VIEW_CUT = TO_MEASURE                        # view distance below it: the same view (gap aliasing)
IN_CONTEXT_K = TO_MEASURE                          # successes in an in-context policy's prompt (ContextFlow, Zero-WAM: 1)
HOVER_TARGET = {"LIBERO": "demo_pregrasp", "RoboDojo": "fixed_clearance"}   # Phase 2: RoboDojo demos carry no object poses
FIXED_CLEARANCE = {"RoboDojo": 0.12, "LIBERO": 0.14}   # metres above the object; LIBERO only as a fallback
```

## Shared types

```python
# Types and helpers the boxes name, one line each; NOT BUILT unless tagged. Every class is a @dataclass. Shapes: an action chunk is 50 rows × action_dim (7 LIBERO, 14 RoboDojo); the denoise path is 11 × 50 × 32, cut to action_dim after.
Decision = Enum("Decision", "RUN RUN_SHORT STOP_AND_ASK")       # the gate's call, before rows run
Verdict = Enum("Verdict", "CONTINUE SUBTASK_DONE TASK_DONE FAILED")   # the failure gate's call, after
VerifierVerdict = Enum("VerifierVerdict", "PASS FAIL UNVERIFIED")   # tri-state; UNVERIFIED: cannot tell, look again
Call = Enum("Call", "PLAN UNSURE FAILED")                        # advisor calls ① ② ③
class RunOutcome(Enum): SUCCESS = auto(); ASKED_HUMAN = auto(); TIMED_OUT = auto(); REFUSED = auto(); SIM_SUCCESS_UNCONFIRMED = auto(); VERIFIER_SUCCESS_SIM_FAIL = auto()   # how a run ends
class Subtask: verb: str; object: str; text: str = field(compare=False)   # frozen; == on (verb, object); Subtask.of(task) wraps text
class RunnerStep: op: Literal["perceive", "hover", "nudge"]; object_name: str | None = None; payload: Pose | None = None   # one program step
Program, Segment = list[RunnerStep], RunnerStep   # a program is runner steps; a segment is one step
class SimState: scene_variant: SceneVariant; physics: ndarray; objects: dict; robot: ndarray; changes: list = field(default_factory=list)   # changes: LIBERO-MAX events still due
class Chunk: rows: ndarray; source: str; planned: ndarray | None = None; noise: ndarray | None = None; trace: ndarray | None = None; is_stop: bool = False; last_pose: Pose | None = None; grasp: tuple | None = None   # rows [rows, A]
class Fix: program: Program; subtask: Subtask; failure_pattern: str; program_segment: Segment; path: list[Step]; last_pose: Pose; repair_key: tuple = (); episode_ids: set[str] = field(default_factory=set); verified: bool = False; verifier_calls: list[VerifierCall] = field(default_factory=list); root: GateFireState | None = None; on_sim: bool = True; vla_version: int = 0; needs_memory: bool = False   # path: the fix's own steps; fix.root.root_id keys it
class Repair: subtask: Subtask; failure_pattern: str; program_segment: Segment; program: Program; path: list[Step]; last_pose: Pose; verifier_calls: list[VerifierCall]; root_event: int = 0   # ②: the gate-fire step; ③: call ③'s start
class VerifierCall: kind: str; subtask: Subtask | None; said: VerifierVerdict; sim: bool | None; step: int; reason: str | None = None; early: bool = False   # beside the same-step sim predicate
class PreferencePair: obs_before: Observation; task: str; better: Chunk; worse: Chunk; vla_version: int; root_id: tuple = ()   # sim-labelled candidate pair
class AdvisorAnswer: call: Call; subtask: Subtask; program: Program | None; failure_pattern: str; program_segment: Segment | None; kind: str = "advisor_answer"   # every answer but a hand-off
class SafetyNote: step: int; overshoot: ndarray; skipped: set[str]; kind: str = "safety"   # overshoot [A] past the controller's range; unset limits
class DenoiseSignal: traces: list[ndarray]; chunks: ndarray; noises: ndarray   # traces [11, 50, 32]; chunks, noises [N, 50, A]
class Window: obs: Observation; task: str; actions: ndarray   # actions [50, A], tail in-painted (FRS); the VLA's task text
class GateFire: step: int; kind: str = "gate_fire"                 # shadow-run gate fire, logged only
class SelfCheckFire: step: int; kind: str = "self_check_fire"      # shadow-run self-check miss, logged only
class SelfCorrectFire: step: int; kind: str = "self_correct_fire"  # shadow-run monitor trigger, logged only
class GateFireState: sim_state: SimState; obs_before: Observation; task: str; subtask: Subtask; episode_ids: set[str] = field(default_factory=set); root_id: tuple = ()   # GateFireState.of(run, index): None without sim_state
class Step: obs: Observation; chunk: Chunk; verdict: Verdict; source: str; gate_fired: bool; refused: bool; sim_state: SimState | None; obs_before: Observation; task: str; subtask: Subtask; reason: str | None = None; kind: str = "step"   # one trace entry
class Answer: kind: str; reason: str | None = None; subtask: Subtask | None = None; subtasks: list[Subtask] = field(default_factory=list); code: Program | None = None; payload: Pose | None = None; failure_pattern: str | None = None; program_segment: Segment | None = None; program: Program | None = None; chunks: Iterable[Chunk] = ()   # chunks: a list, or code_runner's
class Context: obs: Observation; subtask: Subtask | None; task: str = ""; trace: list[Step] = field(default_factory=list); candidates: ndarray | None = None; signal: float | None = None; gate_calls: int = 0; recoveries: int = 0; steps_left: int | None = None; code_errors: list[CodeError] = field(default_factory=list); memory: MemoryRead | None = None; target: PerceiveResult | None = None   # one advisor call's input
class AccelPlusCalibration: reference: Reference; level: float; scale: float; short_level: float; threshold: float; den_floor: ndarray; prefix_p: int; progress_threshold: float   # reference, fit and check set fits
class HandoffConditions: take_over_at: Pose; stop_when: Verdict    # when the VLA takes over a skill
class SkillCard: handoff: HandoffConditions; training_range: list; checks: DryRunResult   # what the advisor reads per skill
class Skill: program: Program; subtask: Subtask; tag: str; repair_key: tuple; card: SkillCard; success_rate: float   # one per repair_key; tag POS, NEG or BLOCKED
class MemoryEvent: step: int; state: dict; kind: str = "task_memory"   # one committed task-memory write, in the run log
class GraspOutcome: embedding: ndarray; lifted: bool; state: RobotState | None   # one past grasp and whether it held
class FixGenConfig: root_filter: str = "pfd" if PFD_AND_SCENES_ON else "all"; nearby_scenes: bool = PFD_AND_SCENES_ON; fix_source: str = "tree_search"; labeller: str = "advisor"   # C2 plug-ins by name
class WorkingMemory: ...    # WorkingMemory(task, start, scene_level): rng seeded; subtasks deque; summary()
class TooManyCodeErrors(Exception): ...   # code_runner gave up; run_chunks fails the step "code errors"
def on_code_error(error, program, context) -> Program: ...   # log_code_error; past MAX_CODE_ERRORS raise TooManyCodeErrors(context.trace); else claude.fix
class FixSource(Protocol): ...   # propose(root, budget, label) -> Iterator[Fix]; RootFilter, Labeller: plain callables
class OneFix(FixSource): ...   # one labelled fix per failure (test-time DAgger)
Start = tuple[str, str | None, int]   # (task, level, seed); level None: plain LIBERO
# disjoint splits, each TO_MEASURE: held_out_starts, anchor_starts, final_held_out_starts, shadow_starts, skill_dry_run_split, ablation_starts, demo_states
# externals, defined outside this file: env (step, success, observe, steps, step_limit, out_of_steps, is_sim, can_restore; stopped() = success or at the step limit), sim, robot, claude, code_agent (the advisor's offline code agent), pi05, sam3_1 (track), depth_anything_3, grasp_model, latent_monitor, grasp_encoder, OggGuide, CusumGate, Cusum, load_calibration; markers TO_MEASURE, FROM_ROBOT_SPEC, FITTED, PRESET
# external types: ndarray, Pose, Grasp, Motion, RobotState, SceneVariant, Network, Event, Reference, DryRunResult, StateSpec, Subgoal, GateCalibration, Calibration, Moved; vla.invert(obs, task, actions) -> (noise, error); robot.hold_row(state), robot.clip_rows(rows) -> (rows clipped to the controller's input range, overshoot [A]), robot.arm_dims, robot.gripper_dims, robot.controller_scale
def accel_blind_signals(new_chunk) -> dict: ...   # ACCEL+ part 5: overlap, executed-action stats, stall
def vla_self_check(obs, subtask, chunk, shadow) -> bool: ...   # part 5 vs progress_threshold; True in stage 1; shadow logs
VERSION_IDS = itertools.count(1)   # one id per Trained; reseeded on load
# vla offline state, saved and loaded: preference_pairs, searched_fixes, pending_roots, audit_pool ([]); quarantined, lcb_verdicts; last_trained, last_rooted, last_audited (None); version, run_version, rounds_without_ood_gain, lcb_budget_left, lcb_untested (0)
# ACCEL+ gate: accel_only(cal) stage 1, a BUILT GateCalibration; accel_score(trace, cal) BUILT score_denoise_path on trace[:, :n_exec]; accel_plus_score(trace, chunk, state, cal) parts 1 to 5 per phase, max -log p; ACCEL+ fits: calibrate_accel_plus(previous, trained, first_pass) two shadow passes, else previous; calibrate_gate(successful_runs) reference / fit / check split, conformal at ALPHA
def gate_score(gate, signal, obs, picked) -> float: ...   # stage 1 accel_score, else accel_plus_score, picked chunk
def vla_trial(trained=None, calibration=None): ...   # context manager: temporary load, restored after
# A7, the rest: after_code() clears guide_next, ogg and recent, never tries (tries reset per subtask); mad_trigger(error) puts E_t into the window, True on SC_CONSECUTIVE over T_on out of cooldown; used_up() is tries > SELF_CORRECT_TRIES, then the failure gate fails the chunk
def follow_watched(chunk, obs, shadow=False) -> tuple[Observation, int, bool]: ...   # row by row; robot_follow's step-limit check and A8 update
def past_a_cap(context) -> str | None: ...   # failure_gate.reason step limit or code errors; unsure calls; recoveries
def finished_run(working, outcome) -> FinishedRun: ...   # adds sim_success, vla.run_version, accel-only flag, VLM call counts
def lesson_fixes(train_log, last_written) -> list[Fix]: ...   # saved fixes since last_written, verified, unquarantined, passes_gates
def vlm_state_spec(task) -> StateSpec: ...   # SimpleARM: variables and read ops, no values
# A8, the rest: end_run() deactivates; seed(name) returns a tracked object's prompt while active; count_stage(stage, step, last) +1 on a counted done; evidence_gate(proposal, state): identity anchor matches, no motion veto, and a verified achievement (AGM) or several agreeing views (SG-Nav); B8, the rest: drop() logs a staged grasp the VLA ran but never closed as a miss; only TRAIN_LEVELS runs stage, so write
def hover_over(recalled) -> Program: ...   # [perceive, hover] runner steps for the recalled object (B5)
def name_in_subtask(recalled) -> Subtask: ...   # NOT BUILT: needs π0.5 base
def coordinate_subgoal(recalled) -> Subgoal: ...   # NOT BUILT: needs a GroundSG checkpoint
VLA_ROUTES = {"staging": hover_over, "subtask": name_in_subtask, "grounded": coordinate_subgoal}   # memory to VLA, by MEMORY_TO_VLA
def lift_odds(outcomes, grasp, points) -> float: ...   # Beta posterior mean of a lift over the GRASP_NEIGHBOURS nearest
# PROPOSED: What does the verifier look at? -> images + robot state, plus force where the robot has it (none on LIBERO or RoboDojo today)
class LoggedVerifier: ...   # check(obs, subtask), task_done(obs, task, goal): tri-state, each logged
# verifier, the rest: check and task_done re-observe once on UNVERIFIED (one re-look per check), and each VerifierCall keeps the VLM's reason; FailureGate, the rest: failed(reason) sets failure_gate.reason, returns Verdict.FAILED; verifier_due(chunk) adds len(chunk.rows), due at VERIFY_EVERY[robot.name], then resets; task_verdict(obs, why_not) asks verifier.task_done on goal_in_words, TASK_DONE on PASS, else failed("cannot tell" on UNVERIFIED, else why_not)
def goal_in_words(start, state) -> str: ...   # LIBERO: BDDL predicates; RoboDojo: end pose, arms-back from joint state
def begin_run(task, start, obs) -> deque[Subtask]: ...   # call ①'s plan into memory.working.subtasks, returned; gate reset
def begin_subtask(subtasks, shadow) -> UncertaintyGate: ...   # A7 tries, B8 drop; a fresh gate
def ask(call, gate, obs, subtasks, trace, recoveries, candidates=None) -> Answer: ...   # call ② or ③; gate.reset(); reword
def ended_unverified(trace, shadow) -> tuple | None: ...   # end_shadow, or end_unconfirmed: sim success, task verdict not PASS
# ends: end_shadow(trace) into shadow_log, never run_log; end_unconfirmed(trace) SIM_SUCCESS_UNCONFIRMED with failure_gate.reason ("verifier: not done" or "cannot tell"), no hand-off
def move_and_judge(chunk, obs, last, shadow, refused) -> Moved: ...   # 6, 7: Moved(chunk, obs, verdict, reason); refused: no move
def save_root(saves) -> SimState | None: ...   # sim.save_state() if saves and env.can_restore (RoboDojo: never)
def staged(obs, chunk) -> bool: ...   # ◎: no last_pose, or move_to_hover's arrival check passes there
def after_code_ran() -> None: ...   # once per code run: VLA queue, part 5, A7 reset
def nudge_chunks(answer, obs) -> list[Chunk]: ...   # stop: hold_chunk(is_stop=True); edit or eef: bounded(payload)
def verifier_audit(train_log) -> bool: ...   # misses and false passes past AUDIT_DISAGREE_MAX quarantine runs
# verifier audit: a verifier FAIL at sim success is a "verifier miss" only when the task's truth file sides with the sim; when it sides with the verifier the case is "sim lenient" and counts against nothing; VERIFIER_SUCCESS_SIM_FAIL counts as a false pass
def refit_gate(vla, trained, old_held) -> Calibration: ...   # drift report, then stage 2 or ACCEL+ re-fit
def training_key(approved, pairs, version, lora_due, own) -> tuple: ...   # learn skips a round on the same data
def current_pairs(vla) -> list[PreferencePair]: ...   # this VLA version's pairs, roots not quarantined
def stage2_calibration(trained=None) -> Calibration: ...   # ACCEL+ once enough accel-only successes exist
def final_eval(vla) -> tuple: ...   # FINAL_LEVELS + final_held_out_starts, once, by hand (gap final-split)
def nearby_roots(epistemic) -> list[GateFireState]: ...   # nearby TRAIN_LEVELS scenes until the gate fires; parent's ids kept
def pfd_roots(roots) -> list[GateFireState]: ...   # keeps roots whose obs_before pfd_is_epistemic
def repair_key(subtask, failure_pattern, program_segment) -> tuple: ...   # fixed classes: (verb, object), RoboFAC type, runner step
def aliased(fix, candidates) -> bool: ...   # another candidate's fix.path[0].obs_before within ALIAS_VIEW_CUT, another repair_key
def unmeasured_constants() -> list[str]: ...   # TO_MEASURE or PRESET names an enabled path still reads
# paired LCB (RE-0): paired_lcb(fix, root_state) suffix rollouts, None once the budget is spent; paired_lcb_wins(fix) cached per lcb_key(fix) = (fix.root.root_id, repair_key, program_hash, vla.version), real-robot fix True; lcb_order(candidates) untested first, then most votes, round-robin by key
# shadow and paired checks: record_shadow_runs(starts, calibration, trained), record_successful_runs(calibration, trained), vla_alone_runs(vla, starts, trained, calibration) -> {Start: env.success}, eval_starts(levels); paired tests at TEST_LEVEL: redeploy_test(old, new) (McNemar, gain past MARGIN), non_inferiority_test(old, new), false_alarm_rate(calibration, trained, starts)
# sim truth: sim_predicate(kind, subtask); rollout(fix) -> (path, after) in a fresh begin_run scope: the fix, then the VLA alone, no advisor call, logged to shadow_log only, no episode vote; vla_alone_reached_goal(after): env.success at its end and no FAILED verdict; sim_goal_check(end_obs) = env.success()
# offline data: extract_repairs(run) from ② code answers and ③ answers, candidate_pairs(roots, n), own_success_noise(vla), stage2_trigger(runs), to_vla_windows(fix) over the fix's own rows only, dry_run(fix, split) -> DryRunResult, sim-labelled per start; vla_alone_after(run, repair): no advisor call and no FAILED verdict after the repair's last step
# trainers (C6): train_noise_policy(examples) on (obs, task, noise), inverted or own success; train_scorer(pairs) pairwise on sim-labelled candidate pairs, this VLA only; train_lora(fixes) -> LoRA | None, an adapter on fixes the VLA cannot make
def validate_response(answer, skill) -> bool: ...   # BUILT: validation.py; the extra kinds NOT BUILT
def bounded(payload, max_correction) -> Chunk: ...   # BUILT: edited_targets; nudge clipped to max_correction
def hover_pose(task, target) -> Pose: ...   # HOVER_TARGET[robot.name]; no target: raises CodeError
def bounded_steps(start_pose, end_pose) -> Motion: ...   # BUILT: move_to_hover (hover.py)
# safety geometry from the robot spec: within_step(chunk, state, limit) per axis on LIBERO, per joint on RoboDojo; within(values, (low, high)); inside(chunk, state, box); predicted_contact(chunk, state); part 5 inputs: commanded_displacement(rows, state), reached_displacement(before, after), phase_of(state, chunk)
# grasp memory: nearest(outcomes, embedding, k), grasp_attempted(rows, before), lifted_since_close(state), gripper_holding(state), close_axis(state); task memory: history_dependent(subtask), change_point(obs) (gripper changes; arm-motion change points once on), frozen_tools(spec, obs), commit(state, proposal), reground(state, images)
# lessons and skills: Lesson.of(fix), Skill.of(fix, tag, results), passes_gates(fix), check_against_scene(lesson, images), inside_range(images, training_range), scenes_of(episode_ids); retrieve_successes(run_log, subtask, k) the k verified successes of that subtask, nearest scene first; start states for tree search: pfd_is_epistemic(obs), libero_plus_factor(state), sample_nearby_scenes(task, factor, levels, n), rank_scenes(scenes), rollout_until_gate_fires(scene), push_off(path, obs)
# small: random_sample, disagreement_rate, program_hash, robofac_failure_type, scene_set, subtask_starts, split_disjoint, episode_peak_part5_suspicion, cosine, mad, best, gaussian_noise, new_episode_id, log_code_error(error, program, context) into context.code_errors and the run log; reports for a person: report, report_aliasing, report_drift, report_verifier_drift, report_small_audit, report_untested, report_kept_calibration, notify_person (NOT BUILT); state on disk: save_state_of_system() and load_state_of_system() (reseeds VERSION_IDS); advisor_calls, vla_step_share rank redeploys
```

## How the boxes connect (one episode)

```python
def run_episode(start, shadow=False):
    """One task in one OOD scene; shadow: the VLA alone, every fire and verdict only logged."""
    task, obs = start_episode(*start)                         # 1; start = (task, level, seed)
    subtasks = begin_run(task, start, obs)                    # call ①: the plan, kept as memory.working.subtasks
    trace, recoveries = [], 0
    while subtasks:
        gate, fired = begin_subtask(subtasks, shadow), False  # gate, A7, B8 per subtask
        call = None
        while True:
            after_failed = call is Call.FAILED
            if call:
                answer = ask(call, gate, obs, subtasks, trace, recoveries, candidates)   # B1; rewords subtasks[0]
                if answer.kind == "human":
                    return ask_human(trace, answer.reason, obs.images)   # B3
                chunks, call = answer.chunks, None            # B7, B6, B5, B4; code runs step by step
            else:
                guided = SC_ACTIVE and self_corrector.guide_next   # an A7 re-call is not gate-scored
                candidates, signal = vla.step(obs, task)      # 2; the VLA keeps the task text
                picked = pick_index(candidates, obs, task)    # A6
                decision = Decision.RUN if guided else gate.decide(signal, obs, picked)   # 3
                if decision is Decision.STOP_AND_ASK:
                    fired, call = True, Call.UNSURE           # call ②; the robot pauses
                    continue
                rows = SHORT_STEPS if decision is Decision.RUN_SHORT else EXEC_STEPS[robot.name]
                chunks = [pick_chunk(candidates, rows, picked, signal)]
            last = len(subtasks) == 1                         # judge turns a last SUBTASK_DONE into the task verdict
            verdict, obs = run_chunks(chunks, obs, task, subtasks[0], trace, fired, last, shadow, after_failed)
            fired = fired and not chunks                      # no chunk ran: the fire is still to mark
            if verdict is Verdict.TASK_DONE and not shadow:
                return end_success(trace)                     # A12: in sim, the sim's goal check must agree
            if ended := ended_unverified(trace, shadow):      # shadow end, or sim success the verifier did not pass
                return ended
            if verdict is Verdict.SUBTASK_DONE:
                subtasks.popleft()                            # never the last subtask: judge decides that one
                break
            if not shadow and verdict is Verdict.FAILED:
                # PROPOSED: What does call ③ try first? -> ask the advisor (arm: a VLA retry, then ask, as a setting)
                recoveries, call = recoveries + 1, Call.FAILED   # call ③; past_a_cap hands off on step limit, code errors
    return ask_human(trace, "no subtasks left", obs.images)   # never reached: judge ends the last subtask
def run_chunks(chunks, obs, task, subtask, trace, fired, last, shadow=False, after_failed=False):
    """Steps A9 to A11 per chunk until a verdict other than CONTINUE; returns (verdict, latest obs)."""
    verdict, chunk = Verdict.CONTINUE, None                   # chunk: the last one that ran
    try:
        for i, chunk in enumerate(chunks):                    # code chunks arrive one runner step at a time
            before, first = obs, fired and i == 0
            saved = save_root(first or (i == 0 and PAIRED_LCB_ON and after_failed))   # a tree root, or call ③'s start
            refused = not safety_check(chunk, obs.state)      # 5; rows clipped to the controller's range first
            moved = move_and_judge(chunk, obs, last, shadow, refused)   # 6, 7; refused: failed, no move
            chunk, obs = moved.chunk, moved.obs
            verdict, reason = moved.verdict, moved.reason     # reason: failure_gate.reason, e.g. "step limit"
            step = Step(obs, chunk, verdict, chunk.source, first, refused, saved, before, task, subtask, reason)
            trace.append(step)
            memory.record(step)                               # every step + verdict, refused too
            if verdict is not Verdict.CONTINUE:
                break
    except TooManyCodeErrors:
        verdict = failure_gate.failed("code errors")          # call ③ next; past_a_cap hands off
    if chunk and chunk.source == "code":
        after_code_ran()                                      # once, when the code run ends: VLA queue cleared
    return verdict, obs
```

# Runtime

## A1 · Task + OOD scene
<!-- box: task -->
Based on: LIBERO [2306.03310]: the base **task suites**; LIBERO-Plus [2510.13626]: **OOD** perturbation splits; LIBERO-MAX [2609.36518]: one **mid-task change** per episode
Related: THE-COLOSSEUM [2402.08191]; REALM [2512.19562]; LIBERO-X [2602.06556]


```python
def start_episode(task, level, seed):   # NOT BUILT: RoboDojo OOD scenes (gap ood-set)
    """Start one run in a scene the VLA was not trained on."""
    # PROPOSED: Which OOD suite? -> LIBERO-Plus, plus LIBERO-MAX Lite for mid-task changes
    # BUILT: LIBERO resets by seed
    scene = scene_set(level, robot.name).sample(seed)         # plain LIBERO when level is None
    obs = scene.reset(seed)
    return task, obs
```

## A2 · VLA
<!-- box: vla -->
Based on: π0.5 [2504.16054]: the **frozen VLA**, trained with subtask-level language; ACCEL+: project method, its last part is the **self-check**; ACT [2304.13705]: **overlapping chunks**, compared here for the self-check
Related: ProbeAct [2606.09740]; OpenVLA-EarlyWarning [2606.29699]; FineART [2609.36416]


```python
class VLA:   # NOT BUILT: load, trial; BUILT: Pi05 (policy/methods.py, frozen, task-text prompt), score_denoise_path, load_calibration; the self-check is built, off
    """The frozen VLA: candidate chunks plus its own denoise trace; holds the trained parts it reads."""
    # PROPOSED: Which policy? -> π0.5, LIBERO-finetuned checkpoint (settings: base or GroundSG checkpoint, TempoFit attention-cache reuse off; WAM arm: Cosmos Policy; in-context arm: ContextFlow on LIBERO, Zero-WAM on RoboDojo)
    # PROPOSED: Should the VLA get subtasks? -> keep the task text until the Phase 4 probe; subtasks go to the advisor and verifier
    # PROPOSED: Should the VLA get a success-memory prior? -> later, once the verifier exists (no prior here yet)
    # PROPOSED: What does the VLA get in context? -> nothing: π0.5 has no demo slot (in-context arm: retrieve_successes(run_log, subtask, IN_CONTEXT_K))
    # PROPOSED: How does the VLA check its own progress? -> ACCEL+ (5): progress stall + chunk overlap + executed-action statistics (vla_self_check)
    def __init__(self, policy):
        self.policy, self.version = policy, 0                 # version: the deployed Trained's id
        self.noise_policy, self.scorer = None, None           # trained parts, set by load after a passed round
        self.lora, self.preference_pairs = None, []           # LoRA after a stall; the scorer's training pairs
        self.gate_calibration = load_calibration(robot.name)  # stage 1 runs accel only
        self.self_check, self.trial = vla_self_check, vla_trial   # read by FailureGate; trial: a temporary load
    def step(self, obs, task):
        n = N_CANDIDATES
        noises = self.noise_policy.sample(obs, task, n) if self.noise_policy else gaussian_noise(n=n)   # the noise policy steers
        guide = None
        if SC_ACTIVE and self_corrector.guide_next:           # A7: one OGG-guided re-call after a truncation
            self_corrector.guide_next = False
            guide = OggGuide(latent_monitor, *self_corrector.ogg)   # the monitor's gradient steers the flow
        candidates, traces = zip(*(self.policy.denoise_with_trace(obs, task, z, guide) for z in noises))
        return list(candidates), DenoiseSignal(traces, chunks=candidates, noises=noises)   # candidates [N, 50, A]
    def request_plan(self, task, obs) -> list[Subtask]: ...   # call 1: advisor(Call.PLAN, ...).subtasks or [Subtask.of(task)]
    def load(self, noise_policy, scorer, gate_calibration, version, lora=None): ...   # redeploy, prune pairs; lora None keeps the deployed one
vla = VLA(pi05)                                               # the one deployed VLA
```

## A3 · Noise policy + scorer
<!-- box: noise -->
Based on: FlowDAgger [2607.08877]: a **noise policy** steers a **frozen** flow VLA; V-GPS [2410.13816]: **rerank** a frozen policy's samples


```python
class NoisePolicy:   # NOT BUILT (gap noise-policy)
    """Picks each candidate's starting noise for the frozen VLA; VLA.step (A2) samples it."""
    # PROPOSED: What learns first? -> noise policy + reranking scorer; DSRL, guidance and residual are the arms
    def __init__(self, network):
        self.network = network                                # fit by train_noise_policy (C6)
    def sample(self, obs, task, n) -> ndarray:
        return self.network(obs, task, n)                  # noises [n, 50, A]; the VLA's weights untouched
class Scorer:
    """Reranks the VLA's candidate chunks; pick_index (A6) reads it."""
    def __init__(self, network):
        self.network = network                                # fit by train_scorer (C6) on this VLA's pairs
    def score(self, obs, task, chunk) -> float:
        return self.network(obs, task, chunk)              # higher: more likely to succeed
```

## A4 · Fine-tuning (last resort)
<!-- box: lora -->
Based on: LoRA [2106.09685]: a small **LoRA adapter** beside the frozen weights
Related: FailBank [2609.39820]


```python
class LoRA:   # NOT BUILT (gap lora-stall); the default fine-tuning plug-in
    """Low-rank weights beside the frozen VLA: the last resort, loaded only after passed checks."""
    # DECIDED: May the VLA's weights change? -> frozen first, LoRA as fallback
    def __init__(self, weights):
        self.weights = weights                                # fit by train_lora (C6); the stall count lives in C7
    def load(self, vla):
        vla.lora = self                                       # VLA.load calls it; every VLA step reads it
```

## A5 · Uncertainty gate
<!-- box: unc -->
Based on: ACCEL+: project method, a **per-dimension accel** gate; ACCEL [2607.27933]: the **denoise-path score** it extends; CUSUM: Page's test, **sums the excess** over time; AEGIS [2606.06660]: a **per-episode escalation cap** on a frozen VLA
Related: GeoAAC [2609.20776]; Diffusion Uncertainty HitL [2503.01876]; VLA Help-Trigger Introspection [2510.01389]; VLA-ATTC [2605.01194]


```python
class UncertaintyGate:
    """Fires when the VLA is unsure; read as a likely OOD scene."""
    # PROPOSED: What tells the VLA it is unsure? -> ACCEL+: per-dimension accel, phase reference, bend shape, conformal p-values + CUSUM
    # PROPOSED: Which ACCEL+ parts are on? -> all parts (1 to 5); each is knocked out later (accel_plus.py ABLATIONS)
    # PROPOSED: What happens when the VLA is unsure but typical? -> unsure but typical: run SHORT_STEPS (2) rows, then look again; ACCEL+ only, the accel + CUSUM gate has no RUN_SHORT branch
    # DECIDED: What happens to the gate when the VLA takes over again? -> reset to zero
    # BUILT (option A, stage 1): CusumGate (cusum.py), EscalationGate.observe (gate.py), score_denoise_path (scoring.py)
    def __init__(self, cal, shadow=False):
        self.cal, self.shadow = cal, shadow
        self.calls, self.score = 0, 0.0
        self.accel_only = accel_only(cal)                     # stage 1: the built gate as it is
        self.cusum = CusumGate(cal) if self.accel_only else Cusum(cal.level, cal.scale, CUSUM_C)
    def decide(self, signal, obs, picked) -> Decision:
        fused = gate_score(self, signal, obs, picked)         # scores the chunk that will run
        self.score = self.cusum.update(fused)                 # the CUSUM statistic
        if self.score > self.cal.threshold and self.fire():
            return Decision.STOP_AND_ASK                      # call 2
        return Decision.RUN_SHORT if not self.accel_only and fused > self.cal.short_level else Decision.RUN
    def fire(self) -> bool:
        if self.shadow:
            memory.record_event(GateFire(step=env.steps))     # shadow: logged, never asks
        self.calls += not self.shadow                         # the advisor checks the cap
        return not self.shadow
    def reset(self):
        self.cusum.reset()                                    # calls kept: the cap counts the subtask
```

## A6 · Action chunk (VLA)
<!-- box: vlachunk -->
Based on: Diffusion Policy [2303.04137]: run a chunk's first rows, then **predict again**; ACT [2304.13705]: **action chunking** for a policy
Related: VLA-Corrector [2607.01804]; AutoHorizon [2602.21445]; Q-Planning [2608.21204]; VERITAS [2606.18247]; Pre-VLA [2605.22446]


```python
def pick_index(candidates, obs, task) -> int:   # NOT BUILT: scorer(obs, task, chunk)
    """The reranking scorer picks one candidate; random until it is trained."""
    # PROPOSED: How is one candidate chunk picked? -> our reranking scorer (arms: random; a value function, V-GPS or SVA; a learned success scorer, RoboMonkey or eVTA0; until the scorer is trained, the nearest of retrieve_successes(run_log, subtask, k), SAIL)
    # BUILT: runs the only chunk (N_CANDIDATES = 1)
    if vla.scorer is None:
        return memory.working.rng.randrange(len(candidates))  # per-run rng, seeded from the start's seed
    return max(range(len(candidates)), key=lambda i: vla.scorer.score(obs, task, candidates[i]))
def pick_chunk(candidates, rows, picked, signal) -> Chunk:
    """Cut the picked candidate to rows: EXEC_STEPS, or SHORT_STEPS when unsure but typical."""
    planned = candidates[picked]                              # [50, A], kept whole for part 5
    noise, trace = signal.noises[picked], signal.traces[picked]
    return Chunk(planned[:rows], source="vla", planned=planned, noise=noise, trace=trace)
```

## A7 · Self-correction
<!-- box: selfcorrect -->
Based on: VLA-Corrector [2607.01804]: a **latent-dynamics monitor** truncates the chunk, then **re-calls**
Related: CoRe [2608.14822]; CheckVLA [2607.26789]; DREAM-Chunk [2606.18589]; SV-VLA [2604.02965]; BCP [2608.03483]


```python
class SelfCorrector:   # NOT BUILT (gap selfcorrect)
    """Watch each executed VLA row; a sustained latent mismatch truncates, then one OGG re-call."""
    # PROPOSED: Who decides: VLA corrects itself, or the advisor helps? -> self-correct first, the advisor after SELF_CORRECT_TRIES failed self-corrections (arm: the advisor decides, each time or always)
    # PROPOSED: How does the VLA self-correct? -> truncate + a re-call, OGG monitor-guided (a plain re-call is its setting)
    def __init__(self):
        self.new_subtask()                                    # all of its state is per subtask
    def new_subtask(self, subtask=None):
        self.errors, self.recent = deque(maxlen=SC_WINDOW), deque(maxlen=LVM_K)
        self.ogg, self.guide_next = None, False
        self.over, self.cooldown = 0, 0
        self.tries = 0                                        # reset here only: tries count per subtask
    def watch(self, latent_before, row, latent_after) -> bool:
        self.recent.append((latent_before, row))
        if len(self.recent) < LVM_K:
            return False                                      # no E_t yet
        old_latent, old_row = self.recent[0]                  # step t - k
        expected = latent_monitor(old_latent, old_row)        # residual latent change over k steps
        drift = latent_after - old_latent
        if not self.mad_trigger(1 - cosine(expected, drift)):   # E_t through the MAD hysteresis
            return False
        self.tries, self.guide_next = self.tries + 1, True
        self.ogg = (latent_after, expected - drift)           # corrective direction for OGG
        return True
self_corrector = SelfCorrector()                              # read only when SC_ACTIVE
```

## B1 · Advisor
<!-- box: adv -->
Based on: Hi Robot [2502.19417]: a high-level model **plans subtasks** for a VLA; RoboHarness [2603.24060]: a **harness** that keeps the frozen VLA as policy
Related: AdaHVLA [2609.29204]; VoLoAgent [2606.07723]; Pigey [2607.21725]; RoboBRIDGE [2607.27881]; VLAs-as-Tools [2605.13119]


```python
def advisor(call, context):
    """Answer one call; the VLA stays the main policy."""
    # PROPOSED: Which advisor model? -> Claude Code (Codex is the arm)
    # PROPOSED: How many unsure calls per subtask? -> a cap per subtask, then ask a human
    # BUILT: ClaudeAdvisor plan, answer, fix (advisor/claude.py); advisor() (runtime/episode.py)
    robot.pause()                                             # the robot holds while asked
    if call is Call.PLAN:
        return Answer(kind="plan", subtasks=claude.plan(context.task, context.obs.images))   # call ①
    if reason := past_a_cap(context):
        return Answer(kind="human", reason=reason)            # B3: the advisor hands off
    context.memory = memory.read(context.subtask, context.obs.images)   # B2: this run, lessons, task memory once
    found = skill_library.match(call, context)               # B7: checked skill first
    answer = claude.answer(call, context, found.skill, avoid=found.avoid)
    if answer.kind == "code":                                 # a use-it skill first, else new code, else A8 staging
        answer.program = found.program or answer.code or task_memory.to_vla(context.memory.task)
    if not validate_response(answer, skill=found.skill):     # a code answer needs a program
        return Answer(kind="human", reason="invalid answer")
    if answer.kind in ("stop", "edit", "eef"):                # B4: a stop, or a nudge
        answer.chunks = nudge_chunks(answer, context.obs)
    elif answer.kind == "code":
        answer.chunks = code_runner(answer.program, context)  # B5: lazy, one runner step at a time
    memory.record_event(AdvisorAnswer.of(call, context.subtask, answer))   # every answer but a hand-off
    return answer
```

## B2 · Advisor memory
<!-- box: mem -->
Based on: RACaP [2609.29394]: **typed working memory** plus reusable lessons; Mimir [2608.04933]: memory **re-grounded** in the current scene; Living-Harness [2607.26598]: **gated lesson** extraction; Optimus-R [2609.39794]: a new lesson only with **enough support**; MemHarness [2607.28272]: each lesson **checked against the scene**, then adapted
Related: RoboMemory [2508.01415]; AGP [2609.12541]; PhysMem [2602.20323]; GeneralVLA-2 [2606.17480]; Pragmatist-Robot-Plan-Tasks [2507.16713]

```python
class AdvisorMemory:   # NOT BUILT: lessons
    """In-episode working memory plus cross-episode repair lessons, written offline from the run log."""
    # PROPOSED: What does the advisor remember within a run? -> typed working memory
    # PROPOSED: What history does the advisor see? -> anchor frames + the latest step (RoboICL)
    # PROPOSED: What examples does the advisor get in context? -> matching lessons only (arms: + retrieve_successes(run_log, subtask, 1) and the nearest failure at ② and ③, RoboHarness; + 1-3 successful code programs for code answers, RoboICL or AOR)
    # PROPOSED: What carries over when the advisor's context resets? -> structured handover (NavHarness)
    # BUILT: TypedWorkingMemory (memory/methods.py), lessons empty
    def __init__(self):
        self.working = None                                   # WorkingMemory, set by begin_run
    def record(self, step):
        self.working.update(step)                             # counts, and the step joins the events
    def record_event(self, event):
        self.working.events.append(event)                     # e.g. a VerifierCall, reaches the run log
    def read(self, subtask, images) -> MemoryRead:
        view = task_memory.read(subtask, images) if TASK_MEMORY_ON else None
        return MemoryRead(self.working.summary(), lesson_store.read(subtask, images), task=view)   # lessons
    def end_run(self, log, outcome):
        if TASK_MEMORY_ON:
            task_memory.end_run()                             # A8: no seed outside a run
        if GRASP_MEMORY_ON:
            grasp_memory.drop()                               # B8: a staging never closed is a miss
        log.append(finished_run(self.working, outcome))       # run_log, or shadow_log for shadow runs
memory = AdvisorMemory()                                      # one memory for run_episode, advisor, verifier
```

**Lessons, kept across runs** (written each offline round from the run log, read on calls ② and ③):

```python
class LessonStore:   # NOT BUILT (gap repair-mem)
    """Repair lessons across runs; offline_round writes, AdvisorMemory.read reads."""
    # PROPOSED: How are lessons written across runs? -> each offline round, after the verifier audit, behind gates, from training runs only (setting: RoboHarn-Evo support and oppose counts)
    # PROPOSED: How does the advisor use a retrieved lesson? -> check it against the scene, then adapt or reject (setting: SimpleARM read gate, only when history matters)
    def __init__(self):
        self.by_key = {}                                      # repair_key -> Lesson: one lesson per repair
        self.last_written = None                              # None: the first write reads every run
    def write(self, train_log):
        for fix in lesson_fixes(train_log, self.last_written):   # verified, unquarantined, passes_gates
            self.add_or_merge(Lesson.of(fix))
        self.last_written = train_log.runs[-1].episode_id if train_log.runs else self.last_written
    def add_or_merge(self, lesson):
        kept = self.by_key.setdefault(lesson.repair_key, lesson)
        kept.supporters |= lesson.supporters                  # a repeat adds support (Optimus-R)
    def drop_supporters(self, quarantined):
        for lesson in self.by_key.values():
            lesson.supporters -= quarantined                  # a quarantined run takes its support back
    def match(self, subtask, images) -> list[Lesson]:
        live = [l for l in self.by_key.values() if len(l.supporters) >= MIN_LESSON_SUPPORT]
        fits = [l for l in live if l.trigger == subtask]      # check_against_scene judges the scene
        return sorted(fits, key=lambda l: len(l.supporters), reverse=True)[:LESSONS_PER_CALL]
    def read(self, subtask, images) -> list[Lesson]:
        return [c for l in self.match(subtask, images) if (c := check_against_scene(l, images))]   # None: rejected
lesson_store = LessonStore()                                  # built after its class; AdvisorMemory reads it at call time
```

## A8 · Task memory
<!-- box: ledger -->
Based on: SimpleARM [2609.36595]: the **state a task needs**, written only with proof; AGM [2608.29537]: commit only a **verified achievement**; SG-Nav [2410.08189]: accept a change once **several views** agree
Related: ACM [2606.29774]; T²Mem [2609.36720]; VLMM [2607.23797]; Divide-and-Remember [2610.00982]

```python
class TaskMemory:   # NOT BUILT (gap ledger)
    """Within-run task state, from SimpleARM's code (simplearm.github.io)."""
    # PROPOSED: What does task memory track? -> SimpleARM task-chosen state (kinds: OCC4M tracks + containment, RoboStream event log, ECoMEM concepts)
    # PROPOSED: When is task memory read? -> only for a history-dependent subgoal (settings: the advisor decides, NavHarness; old entries down-weighted, DART-VLN)
    # PROPOSED: How does memory reach the VLA? -> arm staging via the code runner (subtask text may use TOWN-VLA's fixed template)
    # PROPOSED: What triggers a memory write? -> change points in gripper and arm motion (ProTracer); the gripper part (AGM) first
    def __init__(self):
        self.spec, self.state = None, {}                      # set per run by spec_from_task
    def spec_from_task(self, task):
        self.spec = vlm_state_spec(task)                      # relations, counts, step order; no values
        self.state = {v: None for v in self.spec.variables}
    def update(self, obs):
        proposal = frozen_tools(self.spec, obs) if change_point(obs) else None   # the write trigger
        if proposal and evidence_gate(proposal, self.state):  # update rule: anchor, motion veto, then verified or views agree
            self.state = commit(self.state, proposal)
            memory.record_event(MemoryEvent(env.steps, dict(self.state)))
    def read(self, subtask, images) -> TaskState | None:
        if history_dependent(subtask):                        # SimpleARM read gate
            return reground(self.state, images)               # recalled objects, in the current view
        return None
    def to_vla(self, recalled) -> Program | None:            # advisor() passes the state read once
        return VLA_ROUTES[MEMORY_TO_VLA](recalled) if recalled else None   # staging: π0.5 unchanged
task_memory = TaskMemory()                                    # read only when TASK_MEMORY_ON
```

## B7 · Skill library
<!-- box: skills -->
Based on: Voyager [2305.16291]: the **skill library** idea; ASPIRE [2607.00272]: skills discovered, **checked** and kept; ENPIRE [2606.19980]: recipes and tools **evolved between runs**; RACaP [2609.29394]: code evolved offline into **typed APIs**; Zetta [2608.16590]: **validation-gated** skill updates around a frozen VLA
Related: HarnessPAI [2609.29166]; TGL [2608.17209]; RATS [2606.19419]; SHAPER (Skill-Harness Evolution) [2608.11350]


```python
class SkillLibrary:   # NOT BUILT: dry_run and the scene check; the store, match and admit are built
    """Checked code + VLA skills: dry-run, tag and admit each; match the one tried first."""
    # DECIDED: What may enter the skill library? -> checked fixes only
    # DECIDED: Must a new skill pass the checks? -> yes: a dry run on its own split first
    # BUILT: CheckedSkillLibrary.match (skills/methods.py), subtask only
    def __init__(self):
        self.skills = []                                      # admitted only: POS, NEG or BLOCKED
    def dry_run(self, candidates):                            # the only writer, called by checks (C7)
        for fix in candidates:
            results = dry_run(fix, skill_dry_run_split)       # sim-labelled, one row per start
            self.admit(Skill.of(fix, self.tag(fix, results), results))
    def tag(self, fix, results) -> str:                       # POS passed, NEG failed, BLOCKED failed twice
        failed_before = any(s.repair_key == fix.repair_key and s.tag == "NEG" for s in self.skills)
        return "POS" if results.passed else ("BLOCKED" if failed_before else "NEG")
    def admit(self, skill):
        self.skills = [s for s in self.skills if s.repair_key != skill.repair_key] + [skill]   # one per repair
    def match(self, call, context) -> SkillMatch:             # call ② or ③, before new code
        subtask, images = context.subtask, context.obs.images
        fits = [s for s in self.skills if s.subtask == subtask]   # (verb, object) match
        fits = [s for s in fits if inside_range(images, s.card.training_range)]   # the scene inside its range
        best = max((s for s in fits if s.tag == "POS"), key=lambda s: s.success_rate, default=None)
        avoid = [s for s in fits if s.tag in ("NEG", "BLOCKED")]
        return SkillMatch(skill=best, program=best.program if best else None, avoid=avoid)
skill_library = SkillLibrary()                                # the advisor's skills; the Advisor calls match (B7)
```

## B6 · Vision tools
<!-- box: vision -->
Based on: SAM 3 [2511.16719]: **concept masks** and a video tracker; Depth Anything 3 [2511.10647]: **depth** from images; Contact-GraspNet [2103.14127]: **grasp poses** from points
Related: K1 [2609.29389]; SpaceTools [2512.04069]; Instruct2Act [2305.11176]; VoLoAgent [2606.07723]


```python
def perceive(images, object_name):   # NOT BUILT: tracking
    """Find the object, its centre and its best grasp."""
    # PROPOSED: Track the object or re-detect it? -> track the mask
    # PROPOSED: Where does depth come from? -> Depth Anything 3
    # PROPOSED: Which grasp model? -> Contact-GraspNet, top-down first
    # BUILT: Sam3Segmenter, DepthAnything3, ContactGraspNet, TopDownRanker (perception/methods.py)
    seed = task_memory.seed(object_name) if TASK_MEMORY_ON else None   # A8: one identity
    mask = sam3_1.track(images, object_name, seed)            # seed None: a concept prompt
    if mask is None:
        raise CodeError(error=f"{object_name} not found")     # code_runner retries
    points = depth_anything_3(images) & mask                  # the object's points
    grasps = grasp_model(points)
    grasp = grasp_memory.rank(grasps, points)[0] if GRASP_MEMORY_ON else best(grasps, prefer="top_down")
    return PerceiveResult(mask, points, points.centre(), grasp)
```

## B8 · Grasp memory
<!-- box: graspmem -->
Based on: CL-Grasp [2610.01301]: a **success-odds** scorer, updated by each **outcome**
Related: GTP-FA [2606.03385]


```python
class GraspMemory:   # NOT BUILT (gap graspmem)
    """Grasp outcomes across episodes, from TRAIN_LEVELS runs; a Beta posterior ranks candidates."""
    # PROPOSED: How are grasp candidates ranked? -> Beta-posterior kNN over approach axes, labelled by the VLA's grasp
    def __init__(self):
        self.outcomes, self.pending = [], None                # a cross-run store, written at runtime
        self.ran, self.closed = False, False
        self.last_command = None
    def rank(self, grasps, points) -> list[Grasp]:
        return sorted(grasps, key=lambda g: lift_odds(self.outcomes, g, points), reverse=True)
    def stage(self, grasp, points, state):
        self.drop()                                           # the last staging never closed: a miss
        if not gripper_holding(state) and memory.working.scene_level in TRAIN_LEVELS:   # eval runs never write
            self.pending, self.ran = (grasp, points), False
            self.closed, self.last_command = False, None
    def record(self, state, chunk):
        gripper = chunk.rows[:, robot.gripper_dims]           # the executed gripper commands
        if chunk.source == "vla":                             # only the VLA's chunk is a grasp try
            self.ran = True
            self.closed = self.closed or grasp_attempted(gripper, self.last_command)
        self.last_command = gripper[-1] if len(gripper) else self.last_command
        if self.pending is not None and self.closed and lifted_since_close(state):
            embedding = grasp_encoder(close_axis(state), self.pending[1])   # the axis the VLA closed along
            self.outcomes.append(GraspOutcome(embedding, lifted=gripper_holding(state), state=state))
            self.pending = None
grasp_memory = GraspMemory()                                  # read only when GRASP_MEMORY_ON
```

## B5 · Code runner
<!-- box: runner -->
Based on: ENPIRE [2606.19980]: tools **hover the arm**, then the VLA grasps; Harness VLA [2607.08448]: the frozen VLA as a **retryable primitive**
Related: HarnessPAI [2609.29166]; AGP [2609.12541]; LiLo [2602.21531]; BATON [2608.16889]; VLCP [2608.16978]


```python
def code_runner(program, context) -> Iterator[Chunk]:   # NOT BUILT: multi-step programs; CodeVla runs one find + hover
    """Run the advisor's program one step at a time: each move runs before the next step looks."""
    # PROPOSED: Where does the hover stop? -> the demos' pre-grasp pose
    # PROPOSED: May code moves use a motion planner? -> bounded steps only
    i = 0
    while i < len(program):
        try:
            yield from run_step(program[i], context)          # run_chunks runs each chunk before pulling the next
            i += 1
        except CodeError as error:
            program = on_code_error(error, program, context)  # logs it; claude.fix rewrites only the step that raised
def run_step(step, context) -> list[Chunk]:
    """One step on a fresh view: perceive finds the target, hover stages the arm, nudge edits."""
    context.obs = env.observe()                               # the scene after the last move
    if step.op == "perceive":
        context.target = perceive(context.obs.images, step.object_name)   # B6
        return []
    if step.op == "nudge":
        return [bounded(step.payload, MAX_CORRECTION)]        # ≤ 5 cm, ≤ 0.35 rad
    pose = hover_pose(context.task, context.target)           # LIBERO: demo offset; RoboDojo: fixed clearance
    chunks = to_chunks(bounded_steps(context.obs.state.eef_pose, pose), target=context.target)   # B4
    if GRASP_MEMORY_ON and chunks:
        grasp_memory.stage(*chunks[0].grasp, context.obs.state)   # B8: the chosen grasp, on the first chunk
    return chunks
    # Risk: a familiar arm pose may not suffice with new objects in view (experiment A).
```

## B4 · Final action chunks
<!-- box: codechunks -->
Based on: ACT [2304.13705]: actions come in **short runs**; π0.5 [2504.16054]: its **row format**, so code chunks run alike


```python
def to_chunks(motion, target=None):
    """Cut a motion into chunks the robot follows like the VLA's own; target: what perceive found."""
    rows = motion.as_action_rows()                            # the VLA's action format, [rows, A]
    if len(rows) == 0:
        return []                                             # already there: nothing runs
    step = CHUNK_STEP_MAX_ROWS
    chunks = [Chunk(rows[i:i + step], source="code") for i in range(0, len(rows), step)]
    chunks[-1].last_pose = motion.end_pose                    # ◎: where the VLA takes over
    if GRASP_MEMORY_ON and target:
        chunks[0].grasp = (target.grasp, target.points)         # B8: run_step stages it at the hover
    return chunks
def hold_chunk(obs, is_stop):
    """A stop: hold the arm; the failure gate's verifier decides if the task is done."""
    return Chunk(robot.hold_row(obs.state)[None], source="code", is_stop=is_stop)   # [1, A]
```

## A9 · Safety limits
<!-- box: safety -->
Based on: ENPIRE [2606.19980]: **hard safety limits**, a violation fails the task; Safe RFM [2503.07404]: a **safety layer** last, after the pretrained policy
Related: SafeHarness [2609.20822]; VLSA [2512.11891]; RAIL [2409.19190]


```python
def safety_check(chunk, state) -> bool:   # NOT BUILT: workspace and contact checks
    """Hard limits on every chunk before the robot moves; state: where the chunk starts."""
    # BUILT: SpecLimits (safety/methods.py); clip_rows (robots/methods.py)
    chunk.rows, overshoot = robot.clip_rows(chunk.rows)       # the controller clips anyway; overshoot [A] per dimension
    limits = dict(step=STEP_LIMIT[robot.name], gripper=GRIPPER_LIMIT[robot.name])   # per robot
    limits.update(workspace=WORKSPACE, contact=CONTACT_LIMIT)
    unset = {name for name, value in limits.items() if value is FROM_ROBOT_SPEC}   # skipped, not guessed
    memory.record_event(SafetyNote(env.steps, overshoot, unset))   # overshoot per dimension; skipped limits
    step_ok = "step" in unset or within_step(chunk, state, limits["step"])   # LIBERO per axis; RoboDojo per joint
    grip_ok = "gripper" in unset or within(chunk.rows[:, robot.gripper_dims], limits["gripper"])
    room_ok = "workspace" in unset or inside(chunk, state, WORKSPACE)
    touch_ok = "contact" in unset or predicted_contact(chunk, state) <= CONTACT_LIMIT
    return step_ok and grip_ok and room_ok and touch_ok       # robot spec limits, not tuned
```

## A10 · Robot moves
<!-- box: robot -->
Based on: robosuite [2009.12293]: the **operational-space controller** LIBERO runs on


```python
def robot_follow(chunk):
    """The low-level controller follows the chunk, stopping early on success or at the step limit."""
    # BUILT: chunk_step (early stop), execute_joint_actions
    for row in chunk.rows:
        if env.steps >= env.step_limit:
            break                                             # checked before stepping: no row past the limit
        env.step(row)
        if env.success():
            break                                             # the failure gate then forces verifier.task_done
    obs = env.observe()                                       # images + state + force
    if TASK_MEMORY_ON:
        task_memory.update(obs)                               # A8: every step's view
    if GRASP_MEMORY_ON:
        grasp_memory.record(obs.state, chunk)                 # B8: writes once a pending grasp closed and lifted
    return obs
```

## A11 · Failure gate
<!-- box: fail -->
Based on: Sentinel [2410.04640]: a **VLM checks progress**, not every step; ACCEL+: project method, the **self-check**; RegenHarness [2609.27612]: the controller saying **done is not success**
Related: AGM [2608.29537]; Agentic-Robot [2505.23450]; DoReMi [2307.00329]; MotorMind [2609.38078]


```python
class FailureGate:   # NOT BUILT: force; the self-check is built, off
    """The VLA's self-check plus an independent verifier; in shadow the self-check only logs."""
    # PROPOSED: How is the verifier built? -> a VLM progress check (Sentinel), tri-state verdict
    # DECIDED: How is a code move checked? -> at ◎, by its pose; the verifier counts executed VLA rows
    def __init__(self):
        self.rows_since_verify, self.reason = 0, None         # VLA rows since a check; last FAILED's why
    def judge(self, obs, chunk, last, shadow=False, truncated=False) -> Verdict:   # subtask: working memory's
        if chunk.is_stop or env.stopped():                    # a stop, sim success or the step limit
            return self.task_verdict(obs, "step limit" if env.out_of_steps() else "verifier: not done")
        if chunk.source == "code":                            # ◎: staged at last_pose? VLA chunks judge progress
            return Verdict.CONTINUE if staged(obs, chunk) else self.failed("not at the known pose")
        if truncated and self_corrector.used_up():
            return self.failed("self-correction tries used up")
        if not (truncated or vla.self_check(obs, memory.working.subtasks[0], chunk, shadow)):
            return self.failed("stalled")                     # in shadow only logged
        if not self.verifier_due(chunk):
            return Verdict.CONTINUE                           # the self-check covers chunks between
        verdict, subtask_done = verifier.check(obs, memory.working.subtasks[0])   # one VLM call, two records
        if verdict is not VerifierVerdict.PASS or not subtask_done:   # UNVERIFIED twice: wait for the next check
            return self.failed("no progress") if verdict is VerifierVerdict.FAIL else Verdict.CONTINUE
        return self.task_verdict(obs, "verifier: not done") if last else Verdict.SUBTASK_DONE
failure_gate, verifier = FailureGate(), LoggedVerifier()      # the verifier logs each verdict beside the sim predicate
```

## A12 · End: task succeeded
<!-- box: endok -->
Based on: RegenHarness [2609.27612]: only a **verified goal** counts as success
Related: SuccessVQA [2303.07280]


```python
def end_success(trace):
    """Close the run as a verified success; in sim, the sim's goal check must agree."""
    sim_not = env.is_sim and not env.success()                # the verifier passed, the sim did not
    outcome = RunOutcome.VERIFIER_SUCCESS_SIM_FAIL if sim_not else RunOutcome.SUCCESS   # a false pass for the audit
    memory.end_run(run_log, outcome)                          # the run, appended to the run log
    return outcome, trace
```

## B3 · End: ask a human for help
<!-- box: endhuman -->
Based on: RegenHarness [2609.27612]: a spent **recovery budget** ends in escalation
Related: AEGIS-Reflex [2606.06660]; ARMADA [2510.02298]; Sirius-Runtime [2310.17552]


```python
def ask_human(trace, reason, images):
    """Stop and ask a person; the failed run still feeds offline training."""
    # PROPOSED: How many tries before asking a human? -> few (MAX_RECOVERY_TRIES, to be measured)
    notify_person(reason, images, trace)                      # reason: a cap or invalid answer
    memory.end_run(run_log, RunOutcome.ASKED_HUMAN)           # the run, appended to the run log
    return RunOutcome.ASKED_HUMAN, trace
```

# Offline

## How the offline boxes connect (one round)

```python
def offline_round(run_log, vla):
    """Between runs: turn saved runs into more data, then train small parts of the frozen VLA."""
    # PROPOSED: Where does offline training run first? -> LIBERO with OOD splits (free resets).
    try:
        vla.lcb_budget_left, vla.lcb_untested = LCB_BUDGET, 0   # a fresh paired-LCB budget each round
        train_log = run_log.only_levels(TRAIN_LEVELS)         # fixes come from TRAIN_LEVELS runs only
        audit_ok = verifier_audit(train_log)                  # C7 guardrail: misses and false passes only
        lesson_store.drop_supporters(vla.quarantined)         # quarantined runs take their support back
        vla.pending_roots = [g for g in vla.pending_roots if not g.episode_ids & vla.quarantined]
        if not audit_ok:
            return                                            # quarantined: no roots, training or lessons
        trusted = RunLog.of([r for r in train_log.runs if r.episode_id not in vla.quarantined])
        lesson_store.write(train_log)                         # lessons, only after the audit passes
        if SIM_RESET_BUILT:                                   # C1 roots; none until gap reset closes
            fresh = [r for r in train_log.runs_after(vla.last_rooted) if r.episode_id not in vla.quarantined]
            vla.pending_roots += RunLog.of(fresh).gate_fire_states()
            vla.last_rooted = train_log.runs[-1].episode_id if train_log.runs else vla.last_rooted
        roots, vla.pending_roots = vla.pending_roots[:ROOTS_PER_ROUND], vla.pending_roots[ROOTS_PER_ROUND:]   # oldest first
        fixes = generate_fixes(roots)                         # C2
        vla.searched_fixes += fixes + push_off_and_recover(fixes)   # C4, kept across rounds
        searched = [f for f in vla.searched_fixes if not f.episode_ids & vla.quarantined]
        candidates = saved_runtime_fixes(trusted) + searched  # C5 reads the saved runtime fixes
        ordered = lcb_order(candidates) if PAIRED_LCB_ON else candidates
        approved = [c for c in ordered if should_train(c, candidates)]   # C5; flags aliased fixes
        report_aliasing(candidates)                           # share flagged needs_memory, per run and overall
        if PAIRED_LCB_ON:
            report_untested(vla.lcb_untested)                 # starved fixes show
        if approved and not own_success_noise(vla):           # plain LIBERO trains only here: FlowDAgger's own-success buffer
            record_shadow_runs([s for s in shadow_starts if s[1] is None], vla.gate_calibration, trained=None)
        trained = learn(vla, approved)                        # C6
        count_stall(vla, trained is not None and checks(vla, trained))   # C7; a round with no OOD gain counts
    finally:
        save_state_of_system()                                # every exit survives a restart
```

## C1 · Run log (event store)
<!-- box: buf -->
Based on: RegenHarness [2609.27612]: an **event-sourced log** progress is rebuilt from
Related: PhyAgentOS [2607.16636]; REVOLVE [2609.14633]

```python
class RunLog:   # NOT BUILT: offline readers; append is built, one event file per run
    """One append-only log of every run; training data and repair lessons are read from it."""
    def __init__(self, runs=()):
        self.runs, self.events = [], []                       # FinishedRuns; (episode_id, event) pairs
        for run in runs:
            self.append(run)
    @classmethod
    def of(cls, runs):
        return cls(runs)
    def append(self, run):
        self.runs.append(run)
        self.events += [(run.episode_id, e) for e in run.events]   # never edited; corrections are new events
    def gate_fire_states(self) -> list[GateFireState]:
        steps = [(r, i, e) for r in self.runs for i, e in enumerate(r.events) if e.kind == "step"]
        fires = [(r, i) for r, i, e in steps if e.gate_fired and e.verdict is not Verdict.TASK_DONE]
        roots = [GateFireState.of(r, i) for r, i in fires]    # a finished fire repairs nothing
        return [g for g in roots if g is not None]            # no saved sim_state: not a root
    def only_levels(self, levels):
        return RunLog.of([r for r in self.runs if r.scene_level in levels])
    def runs_after(self, last_id):
        ids = [r.episode_id for r in self.runs]
        return self.runs if last_id is None else self.runs[ids.index(last_id) + 1:]
    def scored_runs_since(self, last_id):
        return [r for r in self.runs_after(last_id) if r.final_verdict is not None]
run_log, shadow_log = RunLog(), RunLog()                      # shadow_log is never read by offline_round
```

## C3 · Sim reset
<!-- box: reset -->
Based on: ENPIRE [2606.19980]: **reset straight** to the hardest phase, by analogy
Related: OmniReset [2603.15789]; Reverse-Curriculum-Generation [1707.05300]


```python
def sim_reset(state: SimState) -> Observation:   # NOT BUILT: variant rebuild, change schedule
    """Put the sim back into a saved state for tree search and push-off; why C2 and C4 are sim-only."""
    # BUILT: LIBERO save_state and restore (SimRobot), restore error 1.8e-5
    sim.build_scene(state.scene_variant)                      # the LIBERO-Plus variant first
    sim.set_state(state.physics, state.objects, state.robot)
    sim.schedule(state.changes)                               # LIBERO-MAX mid-task changes still due
    return env.observe()
```

## C2 · Try fixes + verify
<!-- box: expand -->
Based on: VLAPS [2508.12211]: the **tree-search** idea, branches are code-agent fixes; PFD [2606.20754]: **weight-perturbation disagreement** picks states to explore; LIBERO-Plus [2510.13626]: the **perturbation factor** each root is tagged with; FATE-VLA [2606.02307]: **rank start scenes** by likely failure; RoboMD [2412.02818]: **search scenes** where the policy fails
Related: Plan2Explore [2005.05960]; V-VLAPS [2601.00969]; SkillWeaver-Robot [2609.36171]; RoboART [2502.06575]; SAIL-ICIL [2603.08269]


```python
def generate_fixes(roots, cfg=None):   # NOT BUILT, nor the unbuilt arms listed by each table
    """More verified fixes per failure; each stage is a plug-in picked by config."""
    # PROPOSED: Which gate-fire states are worth exploring? -> PFD: weight-perturbation disagreement (epistemic)
    # PROPOSED: How do we get many fixes per failure? -> tree search from where the gate fired
    # PROPOSED: Who labels the fix? -> the advisor, writing code + VLA fixes
    cfg = cfg or FixGenConfig()                               # no shared mutable default
    roots = ROOT_FILTERS[cfg.root_filter](roots)              # a dropped root is consumed
    if cfg.nearby_scenes:
        roots = roots + nearby_roots(roots)                   # TRAIN_LEVELS scenes; parents' ids kept
    vla.preference_pairs += candidate_pairs(roots, n=N_CANDIDATES) if N_CANDIDATES > 1 else []   # scorer pairs
    source, label = FIX_SOURCES[cfg.fix_source], LABELLERS[cfg.labeller]
    fixes = [f for root in roots for f in source.propose(root, budget=TREE_BRANCHES, label=label)]
    for fix in fixes:
        fix.episode_ids, fix.vla_version = fix.root.episode_ids, vla.version   # copies add data, not votes
        fix.repair_key = repair_key(fix.root.subtask, fix.failure_pattern, fix.program_segment)
        fix.path, after = rollout(fix)                        # path: the fix's own steps; after: the VLA alone
        fix.verified = vla_alone_reached_goal(after)          # env.success, no FAILED; never the VLM verifier
    return [f for f in fixes if f.verified]
class TreeSearch(FixSource):                                  # Protocol + registry plug-in: branches from one root
    def propose(self, root, budget, label) -> Iterator[Fix]:
        for _ in range(budget):
            yield replace(label(root, sim_reset(root.sim_state)), root=root)   # every branch starts at the root
ROOT_FILTERS = {"pfd": pfd_roots, "all": lambda roots: roots}   # unbuilt arms: bend_shape, repr_distance
FIX_SOURCES = {"tree_search": TreeSearch(), "one_fix": OneFix()}   # unbuilt arms: program_search, vla_guided
LABELLERS = {"advisor": lambda root, obs: code_agent.fix(root, obs)}   # unbuilt arms: advisor_best_of_n, human, rpg
```

## C4 · Push off + recover
<!-- box: multiply -->
Related: FLARE [2608.26645]; PARS [2609.33049]; ADC [2503.11646]; FailSafe [2510.01642]


```python
def push_off_and_recover(fixes):
    """Push the arm off a verified path and label the way back; keep recoveries that reach the goal."""
    # PROPOSED: How are recoveries labelled? -> ask the advisor again, from the pushed-off state
    recoveries = []
    for fix in fixes:
        pushed = push_off(fix.path, sim_reset(fix.root.sim_state))   # physics renders the images
        root_id = (*fix.root.root_id, "pushed", program_hash(fix.program))
        pushed_root = replace(fix.root, sim_state=sim.save_state(), obs_before=pushed, root_id=root_id)
        recovery = code_agent.recover(pushed)
        recovery.repair_key = repair_key(fix.subtask, recovery.failure_pattern, recovery.program_segment)
        recovery.episode_ids, recovery.root = fix.episode_ids, pushed_root   # data, not votes
        recovery.path, after = rollout(recovery)              # path: the recovery's own steps; after: the VLA alone
        recovery.verified, recovery.vla_version = vla_alone_reached_goal(after), vla.version   # env.success only
        recoveries += [recovery] if recovery.verified else []
    return recoveries
```

## C5 · Count + decide
<!-- box: trigger -->
Based on: ASPIRE [2607.00272]: distil **recurring validated repairs** into skills; RoboFAC [2505.12224]: a fixed **failure taxonomy**, so repeats match; RE-0 [2609.32416]: admit a fix only if it **beats a resample**
Related: Reuse-Before-Retrieve [2608.17484]; DARC [2608.11772]


```python
def should_train(candidate, candidates) -> bool:
    """Nothing trains on its own; the advisor starts it. Runtime fixes pass the same check."""
    # PROPOSED: What makes the advisor start training? -> verified, repeats, and a paired LCB win from the same root (RE-0), from improvement plan 12 (PAIRED_LCB_ON); before it, verified and repeats
    # PROPOSED: What counts as a repeat? -> only distinct runtime episodes vote; search copies add data
    same = [c for c in candidates if c.repair_key == candidate.repair_key]   # the same repair, any source
    votes = set().union(*(c.episode_ids for c in same))       # copies carry their root's ids
    repeats = candidate.verified and len(votes) >= MIN_REPEAT_EPISODES
    candidate.needs_memory = aliased(candidate, candidates)   # same first view, another repair: no noise label, no fine-tuning
    return repeats and (not PAIRED_LCB_ON or paired_lcb_wins(candidate))
def saved_runtime_fixes(run_log) -> list[Fix]:
    """The advisor's runtime repairs: each votes for its own episode, never pushed off."""
    fixes = []
    for run in run_log.runs:
        for repair in extract_repairs(run):                   # ② code answers and ③ answers
            key = repair_key(repair.subtask, repair.failure_pattern, repair.program_segment)
            root = GateFireState.of(run, repair.root_event)   # ②: the gate-fire step; ③: call ③'s start
            fix = Fix.from_repair(repair, key, run, root)     # ids, on_sim, vla_version from run; path: its steps
            fix.verified = run.sim_success is True and vla_alone_after(run, repair)   # then the VLA alone, no FAILED
            fixes.append(fix)
    return fixes
```

## C6 · Learn + keep VLA frozen
<!-- box: learn -->
Based on: FlowDAgger [2607.08877]: **invert fixes to noise**, train a noise policy, VLA frozen
Related: RL2-VLA [2607.26991]; Imagine-RL [2609.24033]; QPILOTS [2606.14801]


```python
def learn(vla, approved):
    """Fixes become labels; small parts learn while the VLA stays frozen."""
    # PROPOSED: How does a fix become a label? -> run the VLA backwards
    current = current_pairs(vla)                              # this VLA's pairs, unquarantined
    due, own = lora_due(vla), own_success_noise(vla)          # fine-tuning's stall rule; FlowDAgger's second buffer
    if vla.last_trained == (trained_on := training_key(approved, current, vla.version, due, bool(own))):
        return None                                           # the same data: nothing trains
    vla.last_trained = trained_on
    admitted = {s.repair_key for s in skill_library.skills if s.tag != "NEG"}   # a NEG repair is tried again
    labels, cannot = [], []
    for fix in approved:
        inverted = [(w, *vla.invert(w.obs, w.task, w.actions)) for w in to_vla_windows(fix)]   # its own rows; FlowDAgger's backwards run
        if all(error < INVERT_ERROR_CUT for _w, _noise, error in inverted) and not fix.needs_memory:
            labels += [(w.obs, w.task, noise) for w, noise, _error in inverted]   # the error is the router
        else:
            cannot.append(fix)                                # the VLA cannot make it, or it needs memory
    skill_candidates = [f for f in cannot if f.repair_key not in admitted]
    noise_policy = train_noise_policy(labels + own) if labels and own else vla.noise_policy
    scorer = train_scorer(current) if current else vla.scorer
    lora = train_lora([f for f in cannot if not f.needs_memory]) if due else None   # apart from the skills
    same = (noise_policy, scorer, lora) == (vla.noise_policy, vla.scorer, None) and not skill_candidates
    return None if same else Trained(noise_policy, scorer, skill_candidates, lora)   # same: skip the checks
def lora_due(vla) -> bool:                                    # fine-tuning's write rule
    return LORA_ON and vla.rounds_without_ood_gain >= STALL_ROUNDS
```

## C7 · Check + re-fit
<!-- box: checks -->
Based on: FlowDAgger [2607.08877]: **held-out success** shows old skills are kept; ENPIRE [2606.19980]: verification and reset as **fixed APIs**; Calibration under policy updates [2606.15366]: a policy update **shifts** the gate's **calibration**; RegenHarness [2609.27612]: done is not success, so fixes are **audited**
Related: Scale and Selection [2609.39304]; RoboFoundry [2609.32862]


```python
def checks(vla, trained) -> bool:
    """Gate everything that goes back to runtime; True only when an OOD gain was redeployed."""
    # PROPOSED: How is the gate re-fit after training? -> re-fit, every round after stage 2; a pass with too few check-set runs keeps the old one (logged)
    # PROPOSED: What must a round pass to redeploy? -> held-out non-inferiority + OOD McNemar above MARGIN; DynaHarness's per-cell constraints are the stricter arm
    # BUILT: fit_calibration.py (fit once today)
    same_parts = trained.noise_policy is vla.noise_policy and trained.scorer is vla.scorer
    gained = not (same_parts and trained.lora is None) and redeploy_if_passed(vla, trained)   # skill-only: VLA as is
    skill_library.dry_run(trained.skill_candidates)           # after any vla.load: on the deployed VLA
    return gained
def redeploy_if_passed(vla, trained) -> bool:
    """Held-out non-inferiority, then the OOD redeploy test; vla.load only after both pass."""
    old_held = vla_alone_runs(vla, held_out_starts)           # VLA alone, sim goal check, same seeds
    calibration = refit_gate(vla, trained, old_held)          # drift report, then re-fit before the tests
    held_ok = non_inferiority_test(old_held, vla_alone_runs(vla, held_out_starts, trained, calibration))
    if not held_ok:
        return False                                          # a held-out drop: not redeployed
    ood = eval_starts(EVAL_LEVELS)
    old_ood, new_ood = vla_alone_runs(vla, ood), vla_alone_runs(vla, ood, trained, calibration)
    if not redeploy_test(old_ood, new_ood):
        return False                                          # no OOD gain past MARGIN
    report(new_ood, advisor_calls(vla, trained, calibration), vla_step_share(vla, trained, calibration))
    vla.load(trained.noise_policy, trained.scorer, calibration, trained.version, trained.lora)   # trained parts: only here
    return True
def count_stall(vla, gained) -> None:                         # every round without an OOD gain counts
    vla.rounds_without_ood_gain = 0 if gained else vla.rounds_without_ood_gain + 1
```

# Arrows

Each `## ` section below is one arrow: it only says what passes between two boxes (the message, its fields, when, who builds it, who reads it); each box's own logic stays in its box section.
Each arrow's dataclass is real code; the footer lines under it are illustrative, so they are commented out and never run.

## e_task · task + first view
<!-- box: e_task -->

- **When:** once, at the start of a run.

| Field | Type / shape | Meaning |
|---|---|---|
| task | text | the instruction |
| images | camera frames | the first view of the OOD scene |

```python
@dataclass
class TaskStart:
    """Task + OOD scene to VLA."""
    task: str                       # text: the instruction
    images: list[ndarray]           # [H, W, 3] per camera: the first OOD view
# when: once, at the start of a run
# built by: Task + OOD scene (start_episode)
# vla.request_plan(message.task, obs)        # obs from start_episode carries message.images
# read by: VLA
```

## e_plan_ask · ① at start: ask for a plan
<!-- box: e_plan_ask -->
Based on: Hi Robot [2502.19417]: a high-level **plan call**

- **When:** once, before the VLA's first step.

| Field | Type / shape | Meaning |
|---|---|---|
| task | text | the instruction |
| images | camera frames | the first view |

```python
@dataclass
class PlanRequest:
    """VLA to Advisor."""
    task: str                       # text: the instruction
    images: list[ndarray]           # [H, W, 3] per camera: the first view
# when: once, before the VLA's first step
# built by: VLA (VLA.request_plan)
# advisor(Call.PLAN, Context(obs, None, task=message.task))   # obs carries message.images, the first view
# read by: Advisor
```

## e_plan_back · plan: subtasks
<!-- box: e_plan_back -->
Based on: Hi Robot [2502.19417]: a high-level model **plans subtasks**

- **When:** once per run, at the start.
- **If it fails:** empty or unparseable plan: run the task text as one subtask (PROPOSED fallback).

| Field | Type / shape | Meaning |
|---|---|---|
| subtasks | list of (verb, object, text) | what the verifier checks and the advisor plans with; the VLA keeps the task text |

```python
@dataclass
class Plan:
    """Advisor to Advisor memory: the subtasks the verifier and advisor read."""
    subtasks: list[Subtask]         # (verb, object, text): never sent to the VLA
# when: once per run, at the start
# built by: Advisor (the plan answer, call ①)
# memory.working.subtasks = deque(message.subtasks or [Subtask.of(task)])   # begin_run
# read by: the failure gate's verifier and the advisor, via working memory
```

## e_chunk_gate · candidates + unsure score
<!-- box: e_chunk_gate -->
Based on: ACCEL [2607.27933]: the VLA scores its own **denoise path**; ACCEL+: project method, the gate reads the **whole trace**

- **When:** every VLA step, before its rows run.

| Field | Type / shape | Meaning |
|---|---|---|
| candidates | N × 50 × action size | N candidate chunks (today N = 1) |
| signal | denoise traces + chunks + noises | each candidate's denoise path and noise, scored by the gate; built today: one float |

```python
@dataclass
class CandidatesWithSignal:
    """VLA to Uncertainty gate."""
    candidates: ndarray             # [N, 50, A]: N_CANDIDATES chunks (today N = 1)
    signal: DenoiseSignal           # per candidate: trace [11, 50, 32], chunk, noise
# when: every VLA step, one per decision
# built by: VLA (VLA.step)
# UncertaintyGate.decide(message.signal, obs, picked)   # picked = pick_index(...): the chunk that runs
# read by: Uncertainty gate
```

## e_no · no: run the chunk, or a few rows
<!-- box: e_no -->

- **When:** every step the gate does not fire.

| Field | Type / shape | Meaning |
|---|---|---|
| candidates | N × 50 × action size | all candidate chunks |
| picked | int | the reranking scorer's pick, scorer(obs, task, chunk), then scored by the gate |
| rows | int | the normal rows, or a few when unsure but typical |

```python
@dataclass
class CandidatesToPick:
    """Uncertainty gate to Action chunk (VLA)."""
    candidates: ndarray             # [N, 50, A]: all candidate chunks
    picked: int                     # the reranking scorer's pick
    rows: int                       # EXEC_STEPS, or SHORT_STEPS on Decision.RUN_SHORT
# when: every step the gate does not fire
# built by: Uncertainty gate (UncertaintyGate.decide: Decision.RUN or RUN_SHORT)
# pick_chunk(message.candidates, message.rows, message.picked, signal)   # the picked z and its denoise path
# read by: Action chunk (VLA)
```

## e_ask · ② unsure: likely OOD
<!-- box: e_ask -->
Based on: ACCEL [2607.27933]: a firing gate flags a **likely failure**, read as OOD

- **When:** the gate fires.

| Field | Type / shape | Meaning |
|---|---|---|
| images | camera frames | fresh views |
| candidates | N × 50 × action size | all candidate chunks, the unsure ones |
| signal | float | the gate's unsure score |
| subtask | (verb, object, text) | the current subtask |
| trace | list of steps | what happened so far |
| gate calls | int | unsure calls in this subtask, for the advisor's cap |
| recoveries | int | failed tries in this run, for the advisor's cap |

```python
@dataclass
class UnsureCall:
    """Uncertainty gate to Advisor."""
    images: list[ndarray]           # [H, W, 3] per camera: fresh views
    candidates: ndarray             # [N, 50, A]: all candidate chunks
    signal: float                   # the gate's unsure score: its CUSUM value (gate.score)
    subtask: Subtask                # the current subtask
    trace: list[Step]               # what happened so far
    gate_calls: int                 # unsure calls in this subtask
    recoveries: int                 # failed tries in this run
# when: the gate fires; the robot pauses
# built by: the gate sends it (UncertaintyGate.decide returns Decision.STOP_AND_ASK, in run_episode)
# advisor(Call.UNSURE, Context(obs, message.subtask, task, message.trace, candidates=message.candidates, signal=message.signal, gate_calls=message.gate_calls, recoveries=message.recoveries))   # advisor() adds memory
# read by: Advisor
```

## e_sc_watch · chunk + executed row
<!-- box: e_sc_watch -->
Based on: VLA-Corrector [2607.01804]: the monitor reads the **executed action**

- **When:** every executed row of a VLA chunk, once self-correction is on.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | rows × A | the picked VLA chunk as it runs |
| row | A | the row just executed |

```python
@dataclass
class WatchedRow:
    """Action chunk (VLA) to Self-correction."""
    chunk: Chunk                    # [rows, A]: the picked VLA chunk as it runs
    row: ndarray                    # [A]: the row just executed
# when: every executed row of a VLA chunk, SELF_CORRECT_ON
# built by: run_chunks (follow_watched), for the chunk pick_chunk made
# self_corrector.watch(latent.before, message.row, latent.after)   # latent: e_sc_latent
# read by: Self-correction
```

## e_sc_replan · truncate · re-call
<!-- box: e_sc_replan -->
Based on: VLA-Corrector [2607.01804]: **truncate** the remaining rows, then one **guided re-call**

- **When:** the monitor triggers: several steps in a row over its threshold, out of cooldown.
- **If it fails:** past SELF_CORRECT_TRIES in one subtask the chunk is judged failed, so call ③ asks the advisor.

| Field | Type / shape | Meaning |
|---|---|---|
| rows run | int | the chunk's rows that ran; the rest are dropped |
| guide next | bool | the next VLA step is one monitor-guided re-call (False for a plain re-call) |

```python
@dataclass
class Truncation:
    """Self-correction to Action chunk (VLA)."""
    rows_run: int                   # the chunk's rows that ran; the rest are dropped
    guide_next: bool                # True: the next VLA step is one OGG-guided re-call
# when: the monitor triggers (SC_CONSECUTIVE steps over T_on, out of cooldown)
# built by: Self-correction (follow_watched, SelfCorrector.watch)
# chunk = replace(chunk, rows=chunk.rows[:message.rows_run])   # inside follow_watched; VLA.step reads guide_next
# read by: Action chunk (VLA), through move_and_judge and the next VLA.step
```

## e_sc_latent · latents of each executed row
<!-- box: e_sc_latent -->
Based on: VLA-Corrector [2607.01804]: the monitor reads **encoder latents** around each row

- **When:** every executed row of a VLA chunk, once self-correction is on.

| Field | Type / shape | Meaning |
|---|---|---|
| latent before | encoder latent | the frozen π0.5 visual-encoder latent before the row |
| latent after | encoder latent | the same latent after the row |

```python
@dataclass
class RowLatents:
    """Robot moves to Self-correction."""
    latent_before: ndarray          # the frozen π0.5 visual-encoder latent before the row
    latent_after: ndarray           # and after it
# when: every executed row of a VLA chunk, SELF_CORRECT_ON
# built by: Robot moves (follow_watched, row by row)
# self_corrector.watch(message.latent_before, row, message.latent_after)
# read by: Self-correction (SelfCorrector.watch)
```

## e_sc_fail · tries used up: judged failed
<!-- box: e_sc_fail -->

- **When:** a trigger past the tries cap in one subtask.

| Field | Type / shape | Meaning |
|---|---|---|
| tries | int | self-corrections made in this subtask, past the cap |

```python
@dataclass
class TriesUsedUp:
    """Self-correction to Failure gate."""
    tries: int                      # past SELF_CORRECT_TRIES in this subtask
# when: a trigger past SELF_CORRECT_TRIES in one subtask
# built by: Self-correction (used_up: tries > SELF_CORRECT_TRIES)
# self_corrector.used_up()   # in failure_gate.judge, after a truncation
# read by: Failure gate (failed), then call ③
```

## e_vla_chunk · action chunk
<!-- box: e_vla_chunk -->

- **When:** every step the VLA acts alone.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | EXEC_STEPS (or SHORT_STEPS) × action size | the picked chunk, already cut to its rows: fewer when unsure but typical |

```python
@dataclass
class VLAChunk:
    """Action chunk (VLA) to Safety limits."""
    chunk: Chunk                    # [EXEC_STEPS or SHORT_STEPS, A], source "vla": already cut by pick_chunk
# when: every step the VLA acts alone
# built by: Action chunk (VLA) (pick_chunk)
# safety_check(message.chunk, obs.state)     # obs.state: where the chunk starts
# read by: Safety limits
```

## e_saved · skills, tried first
<!-- box: e_saved -->
Based on: Voyager [2305.16291]: **retrieve a stored skill** before writing new code

- **When:** every call ② or ③, before the advisor writes new code.

| Field | Type / shape | Meaning |
|---|---|---|
| skill | code + tag | best use-it match among admitted, dry-run-tagged skills, by success rate, or none |
| program | runner steps | the best match's program, or none |
| avoid | list of skills | matches known to fail or blocked |

```python
@dataclass
class SkillMatch:
    """Skill library to Advisor."""
    skill: Skill | None             # code + tag: the best POS match
    program: Program | None         # the best match's program, or None
    avoid: list[Skill]              # NEG and BLOCKED matches: known to fail / not allowed
# when: every call ② or ③
# built by: Skill library (SkillLibrary.match)
# claude.answer(call, context, message.skill, avoid=message.avoid)
# read by: Advisor
```

## e_code · code to help the VLA
<!-- box: e_code -->
Based on: Code as Policies [2209.07753]: the advisor answers with **robot code**

- **When:** after call ② or ③, when the answer is code + VLA.

| Field | Type / shape | Meaning |
|---|---|---|
| program | runner steps | perceive, hover, nudge: new code, task-memory staging, or a verified skill's |
| context | Context | the call's Context: images, subtask, trace, code errors |

```python
@dataclass
class CodeAnswer:
    """Advisor to Code runner."""
    program: Program                # runner steps: perceive names the object, hover stages
    context: Context                # the call's Context, plus the program
# when: after call ② or ③
# built by: Advisor (advisor)
# code_runner(message.program, message.context)
# read by: Code runner
```

## e_objname · object name
<!-- box: e_objname -->
Based on: SAM 3 [2511.16719]: a **text prompt** names the object to segment

- **When:** each time the code perceives.

| Field | Type / shape | Meaning |
|---|---|---|
| object name | text | the object to find |
| images | camera frames | the current views |

```python
@dataclass
class PerceiveRequest:
    """Code runner to Vision tools."""
    object_name: str                # the object to find
    images: list[ndarray]           # [H, W, 3] per camera: the current views
# when: each time the code perceives
# built by: Code runner (run_step, a perceive step)
# perceive(message.images, message.object_name)
# read by: Vision tools
```

## e_mask · mask · points · grasps
<!-- box: e_mask -->
Based on: SAM 3 [2511.16719]: a **mask** per instance; Depth Anything 3 [2511.10647]: **depth** for the points

- **When:** the answer to each find step.
- **If it fails:** perceive raises CodeError when the object is not found.

| Field | Type / shape | Meaning |
|---|---|---|
| mask | H × W bool | the object, tracked frame to frame |
| points | M × 3 | object points from depth ∩ mask |
| centre | xyz | locates the object; the hover pose starts from it |
| grasp | pose (xyz + axis) | best grasp, top-down first; its approach axis orients the gripper at the pre-grasp pose |

```python
@dataclass
class PerceiveResult:
    """Vision tools to Code runner."""
    mask: ndarray                   # [H, W] bool: the object, tracked frame to frame
    points: ndarray                 # [M, 3]: object points from depth ∩ mask
    centre: ndarray                 # [3] xyz: locates the object
    grasp: Pose                     # xyz + approach axis: best grasp, top-down first
# when: the answer to each find step
# built by: Vision tools (perceive)
# hover_pose(context.task, message)          # in run_step: demo offset (LIBERO) or fixed clearance (RoboDojo)
# read by: Code runner
```

## e_grasps · grasp candidates
<!-- box: e_grasps -->
Based on: CL-Grasp [2610.01301]: a learned **grasp embedding** feeds the scorer

- **When:** each find step, once grasp memory is on.

| Field | Type / shape | Meaning |
|---|---|---|
| grasps | list of poses | the grasp model's candidates |
| points | M × 3 | the object's points, for the grasp embedding |

```python
@dataclass
class GraspCandidates:
    """Vision tools to Grasp memory."""
    grasps: list[Grasp]             # the grasp model's candidates
    points: ndarray                 # [M, 3]: the object's points, for the grasp embedding
# when: each find step, GRASP_MEMORY_ON
# built by: Vision tools (perceive, after grasp_model)
# grasp_memory.rank(message.grasps, message.points)
# read by: Grasp memory
```

## e_ranked · ranked grasps
<!-- box: e_ranked -->
Based on: CL-Grasp [2610.01301]: **success odds** from the nearest past outcomes

- **When:** the answer to each rank call.

| Field | Type / shape | Meaning |
|---|---|---|
| grasps | list of poses | best first by success odds over the nearest past outcomes |

```python
@dataclass
class RankedGrasps:
    """Grasp memory to Vision tools."""
    grasps: list[Grasp]             # best first by the Beta posterior
# when: the answer to each rank call
# built by: Grasp memory (rank)
# grasp = grasp_memory.rank(grasps, points)[0]   # inside perceive; staged when the hover runs
# read by: Vision tools; Code runner (run_step's hover stages it)
```

## e_gm_write · gripper width after close + lift
<!-- box: e_gm_write -->
Based on: CL-Grasp [2610.01301]: each grasp **outcome** updates the scorer

- **When:** after the VLA closes on a staged grasp and lifts, on training-level runs only.

| Field | Type / shape | Meaning |
|---|---|---|
| state | robot state | gripper width and holding, after the lift |
| chunk | rows × A | the executed chunk, for its gripper commands |

```python
@dataclass
class GripAfterLift:
    """Robot moves to Grasp memory."""
    state: RobotState               # gripper width after the close and lift
    chunk: Chunk                    # [rows, A]: the executed gripper commands
# when: after a close and lift, TRAIN_LEVELS runs, GRASP_MEMORY_ON
# built by: Robot moves (robot_follow's obs.state)
# grasp_memory.record(message.state, message.chunk)   # in robot_follow, after each chunk
# read by: Grasp memory (GraspMemory.record)
```

## e_fixable · code error: retry
<!-- box: e_fixable -->
Based on: Voyager [2305.16291]: **execution errors** go back to the code writer

- **When:** the code raises an error.

| Field | Type / shape | Meaning |
|---|---|---|
| program | code | the program that failed |
| error | text | the exception, not a physical failure |
| trace | list of steps | what the code did |
| kind | "code_error" | the event kind in the run log |

```python
@dataclass
class CodeError(Exception):
    """Code runner to Advisor."""
    error: str                      # the exception, not a physical failure
    program: Program | None = None  # the program that failed; code_runner fills it in
    trace: list[Step] | None = None # what the code did
    kind: str = "code_error"        # event kind in the run log
# when: the code raises an error, inside code_runner's retry loop
# built by: Code runner
# claude.fix(message.program, message)       # rewrites only the step that raised; also logged
# read by: Advisor: its fix call inside code_runner's retry loop
```

## e_split · motion split into chunks
<!-- box: e_split -->

- **When:** the code has a motion to a known pose.

| Field | Type / shape | Meaning |
|---|---|---|
| motion | waypoints | bounded steps to the hover pose |

```python
@dataclass
class StagingMotion:
    """Code runner to Final action chunks."""
    motion: Motion                  # [K, A] waypoints + end_pose to the hover pose
# when: the code has a motion to a known pose
# built by: Code runner (run_step, a hover step)
# to_chunks(message.motion, target=context.target)
# read by: Final action chunks
```

## e_codechunk · code chunks (◎ known pose)
<!-- box: e_codechunk -->
Based on: ENPIRE [2606.19980]: **hover first**, then hand the grasp to the VLA

- **When:** after the code, a stop or a nudge produced chunks.

| Field | Type / shape | Meaning |
|---|---|---|
| chunks | K × (≤15 × action size) | at most 15 rows each |
| chunk.last_pose | pose, on the last chunk | where the VLA takes over (◎); its queue clears once, when the code run ends |
| chunk.is_stop | bool, on each chunk | true for a stop's hold chunk; failure_gate reads it |

```python
@dataclass
class CodeChunks:
    """Final action chunks to Safety limits."""
    chunks: list[Chunk]             # .is_stop (a stop's hold chunk, read by failure_gate)
# when: after the code, a stop or a nudge produced chunks
# built by: Final action chunks (to_chunks, hold_chunk, bounded)
# safety_check(chunk, obs.state) for chunk in message.chunks   # inside run_chunks
# read by: Safety limits
```

## e_nudge · ■ stop, or ↔ nudge
<!-- box: e_nudge -->
Based on: ENPIRE [2606.19980]: its RoboCasa API lists a **nudge tool**

- **When:** the answer is a stop or a nudge (edit or hand pose).

| Field | Type / shape | Meaning |
|---|---|---|
| kind | stop, edit or hand pose | which answer it is |
| payload | none, or ≤ 5 cm and ≤ 0.35 rad | none for a stop (the verifier must confirm it); the bounded correction for a nudge |

```python
@dataclass
class StopOrNudge:
    """Advisor to Final action chunks."""
    kind: Literal["stop", "edit", "eef"]
    payload: Pose | None            # None for a stop
# when: the answer is a stop or a nudge
# built by: Advisor (advisor)
# hold_chunk(context.obs, is_stop=True) if message.kind == "stop" else bounded(message.payload, MAX_CORRECTION)
# read by: Final action chunks, inside advisor()
```

## e_safe_robot · within limits
<!-- box: e_safe_robot -->
Based on: ENPIRE [2606.19980]: only motion **inside the hard limits** reaches the robot

- **When:** every chunk that passes the hard limits.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | rows × action size | the checked chunk |

```python
@dataclass
class CheckedChunk:
    """Safety limits to Robot moves."""
    chunk: Chunk                    # [rows, A]: the checked chunk
# when: every chunk that passes the hard limits
# built by: Safety limits (safety_check)
# robot_follow(message.chunk)
# read by: Robot moves
```

## e_refuse · refused = failed
<!-- box: e_refuse -->
Based on: ENPIRE [2606.19980]: crossing a **hard limit** ends the attempt as failure

- **When:** a chunk breaks a hard limit.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | rows × action size | the refused chunk, saved in the trace |
| refused | true | the failure gate returns failed |

```python
@dataclass
class RefusedChunk:
    """Safety limits to Failure gate."""
    chunk: Chunk                    # [rows, A]: the refused chunk, saved in the trace
    refused: bool = True            # the failure gate returns FAILED
# when: a chunk breaks a hard limit; the robot never moves
# built by: Safety limits (safety_check, in run_chunks)
# move_and_judge(message.chunk, obs, last, shadow, refused=True)   # no move; failed("refused")
# read by: Failure gate
```

## e_obs · new observation
<!-- box: e_obs -->

- **When:** after every chunk that ran.

| Field | Type / shape | Meaning |
|---|---|---|
| images | camera frames | the new views |
| state | robot state | joints, end effector, gripper |
| force | contact readings | for the verifier; none on LIBERO |

```python
@dataclass
class Observation:
    """Robot moves to Failure gate."""
    images: list[ndarray]           # [H, W, 3] per camera: the new views
    state: RobotState               # joints, end effector, gripper
    force: ndarray                  # contact readings for the verifier; none on LIBERO
# when: after every chunk that ran
# built by: Robot moves (robot_follow)
# failure_gate.judge(message, chunk, last)   # from the episode loop; chunk.source picks the check
# read by: Failure gate
```

## e_next · next chunk / next subtask
<!-- box: e_next -->

- **When:** the verdict is continue or subtask done.

| Field | Type / shape | Meaning |
|---|---|---|
| verdict | continue, or subtask done | what the gate decided |
| obs | images + state | the VLA's next input |

```python
@dataclass
class Continue:
    """Failure gate to VLA."""
    verdict: Verdict                # CONTINUE or SUBTASK_DONE: what the gate decided
    obs: Observation                # images + state: the VLA's next input
# when: the verdict is continue or subtask done
# built by: run_episode, after failure_gate's verdict
# vla.step(message.obs, task)                # the VLA keeps the task text
# read by: VLA
```

## e_failed · ③ failed: ask how to recover
<!-- box: e_failed -->
Based on: RegenHarness [2609.27612]: a failed check goes to a **separate recovery role**

- **When:** the verdict is failed; past a cap, the advisor hands off to a human.

| Field | Type / shape | Meaning |
|---|---|---|
| images | camera frames | fresh views |
| subtask | (verb, object, text) | the current subtask |
| trace | list of steps | including the failed step |
| recoveries | int | failed tries in this run, for the advisor's cap |
| gate calls | int | unsure calls in this subtask, for the advisor's cap |

```python
@dataclass
class RecoverCall:
    """Failure gate to Advisor."""
    images: list[ndarray]           # [H, W, 3] per camera: fresh views
    subtask: Subtask                # the current subtask
    trace: list[Step]               # including the failed step
    recoveries: int                 # failed tries in this run
    gate_calls: int                 # unsure calls in this subtask
# when: the verdict is failed
# built by: the failure gate sends it (failure_gate, in run_episode)
# advisor(Call.FAILED, Context(obs, message.subtask, task, message.trace, gate_calls=message.gate_calls, recoveries=message.recoveries))   # advisor() adds memory
# read by: Advisor
```

## e_done · all subtasks done, or stop verified
<!-- box: e_done -->
Based on: RegenHarness [2609.27612]: completion is the **original goal re-checked**

- **When:** verifier passes the task: last subtask, a stop, or the sim's goal check ends it.

| Field | Type / shape | Meaning |
|---|---|---|
| verdict | task done | the task-done check passes on the task text and the benchmark goal |
| trace | list of steps | the whole run |

```python
@dataclass
class Success:
    """Failure gate to End: task succeeded."""
    verdict: Verdict                # TASK_DONE: task_done(obs, task, goal) said PASS
    trace: list[Step]               # the whole run
# when: task_done passes; FAIL or cannot tell at sim success: SIM_SUCCESS_UNCONFIRMED
# built by: run_episode, after failure_gate's verdict
# end_success(message.trace)
# read by: End: task succeeded
```

## e_human · a cap passed: hand off
<!-- box: e_human -->
Based on: RegenHarness [2609.27612]: a spent **recovery budget** ends in escalation

- **When:** the advisor finds a cap passed.

| Field | Type / shape | Meaning |
|---|---|---|
| reason | text | which limit was hit |
| images | camera frames | the last views |
| trace | list of steps | what was tried |

```python
@dataclass
class HumanHandoff:
    """Advisor to End: ask a human for help."""
    reason: str                     # which limit was hit
    images: list[ndarray]           # [H, W, 3] per camera: the last views
    trace: list[Step]               # what was tried
# when: the advisor answers kind "human": a cap passed
# built by: the advisor gives the reason (advisor, past_a_cap)
# ask_human(message.trace, message.reason, message.images)   # called by run_episode on a "human" answer
# read by: End: ask a human for help
```

## e_save · every step + verdict
<!-- box: e_save -->
Based on: RegenHarness [2609.27612]: each attempt and its **verdict are recorded** first

- **When:** after every chunk, also a refused one.

| Field | Type / shape | Meaning |
|---|---|---|
| obs | images + state + force | what was seen |
| chunk | rows × action size | what was done, or refused |
| verdict | continue, subtask done, task done, or failed | the failure gate's call, also for a refused chunk |
| source | "vla" or "code" | who produced the chunk |
| gate fired | bool | first chunk after a fire only: marks the tree roots later |
| refused | bool | the safety limits refused it |
| sim state | scene variant + physics + objects + robot, or none | saved when the gate fired: a tree root |
| obs before | images + state | the observation the gate saw, re-scored by the disagreement filter (C2) |
| task | text | the run's task, read for the tree roots |
| subtask | text | the subtask the chunk served, read for the tree roots |
| reason | text or none | why a failed verdict was given, e.g. "step limit" |
| kind | "step" | the event kind in the run log |

```python
@dataclass
class StepRecord:
    """Failure gate to Advisor memory; the same fields as run_chunks' Step."""
    obs: Observation                # images + state + force: what was seen
    chunk: Chunk                    # [rows, A]: what was done, or refused
    verdict: Verdict                # continue, subtask done, task done, or failed
    source: str                     # "vla" or "code"
    gate_fired: bool                # marks the tree roots later
    refused: bool                   # the safety limits refused it
    sim_state: SimState | None      # saved when gate_fired (first chunk after a fire)
    obs_before: Observation         # the observation the gate saw
    task: str                       # the run's task: RunLog.gate_fire_states reads it
    subtask: Subtask                # the subtask the chunk served: RunLog.gate_fire_states reads it
    reason: str | None = None       # why a FAILED verdict was given, e.g. "step limit"
    kind: str = "step"              # event kind: RunLog.gate_fire_states keeps kind == "step"
# when: after every chunk, also a refused one
# built by: run_chunks (verdict from failure_gate)
# memory.record(message)                     # in run_chunks, after each step
# read by: Advisor memory
```

## e_log · the run, appended
<!-- box: e_log -->
Based on: RegenHarness [2609.27612]: every record is **appended**, never overwritten

- **When:** once, when the run ends.

| Field | Type / shape | Meaning |
|---|---|---|
| events | list of events | steps, verdicts, verifier calls with their same-step sim predicate, advisor calls, code and its errors |
| final verdict | run outcome | success, a hand-off, or a verifier and sim disagreement |
| episode id | id | the runtime episode: its fixes vote once in should_train |
| scene level | LIBERO-Plus factor-level, or none | only training-level runs feed training; none for plain LIBERO |
| start | (task, level, seed) | the run's Start: own_success_noise keeps the in-distribution shadow_starts runs |
| sim success | bool, or none | the sim's goal check at run end, the training label; none on a real robot |
| vla version | int | the VLA version during the run; a trial of trained parts logs the trial's version |
| recorded accel only | bool | the run was recorded under the accel-only gate; stage2_calibration reuses only these runs |
| vlm calls | counts | verifier and advisor calls this run, logged for the per-episode budget (gap vlm-budget) |

```python
@dataclass
class FinishedRun:
    """Advisor memory to Run log (event store)."""
    events: list[Event]             # steps, verdicts, VerifierCalls
    final_verdict: RunOutcome       # SUCCESS, ASKED_HUMAN, SIM_SUCCESS_UNCONFIRMED, VERIFIER_SUCCESS_SIM_FAIL
    episode_id: str                 # the runtime episode: one vote in should_train
    scene_level: str | None         # LIBERO-Plus factor-level: in TRAIN_LEVELS, EVAL_LEVELS or FINAL_LEVELS
    start: Start                    # (task, level, seed)
    sim_success: bool | None = None # env.success() at the run's end, in sim
    vla_version: int = 0            # vla.run_version during the run: own_success_noise keeps the current version's runs
    recorded_accel_only: bool = False # accel_only(vla.gate_calibration) during the run: stage2_calibration reuses only these runs
    vlm_calls: dict = field(default_factory=dict)   # verifier and advisor calls this run
# when: once, when the run ends
# built by: Advisor memory (end_run, called by end_success and ask_human)
# run_log.append(message)                    # keeps the run (with final_verdict) and appends its events
# read by: Run log (event store)
```

## e_lessons · lessons, after the gates
<!-- box: e_lessons -->
Based on: Living-Harness [2607.26598]: lessons pass **commit gates** before they are written

- **When:** each offline round, after the verifier audit, behind gates, from training runs only.

| Field | Type / shape | Meaning |
|---|---|---|
| trigger | text | when the lesson applies (subtask, failure sign) |
| failure pattern | text | what went wrong |
| repair | text or skill name | what fixed it, verified by the sim's goal check |
| source scene | images + state | where it was learned (the repair's first observation), so it can be checked later |
| repair key, supporters | key + episode ids | supporters merge per key; a new key needs enough agreeing fixes |

```python
@dataclass
class Lesson:
    """Run log (event store) to Advisor memory: its lessons."""
    trigger: Subtask                # (verb, object): when the lesson applies
    failure_pattern: str            # what went wrong
    repair: str                     # text or skill name: what fixed it
    source_scene: Observation       # images + state: the repair's first obs_before
    repair_key: tuple = ()          # the merge gate keys on it
    supporters: set[str] = field(default_factory=set) # episode ids of the supporting repairs
# when: each offline round
# built by: Advisor memory (LessonStore.write), reading the run log (lesson_fixes)
# lesson_store.add_or_merge(message)          # inside LessonStore.write, after the audit
# read by: Advisor memory (LessonStore)
```

## e_mem_read · this run + matching lessons
<!-- box: e_mem_read -->
Based on: MemHarness [2607.28272]: each lesson is **checked against the scene** before use

- **When:** every call ② or ③.

| Field | Type / shape | Meaning |
|---|---|---|
| working memory | summary | this run's subtask status, attempts, failed tries, gate calls |
| lessons | list of lessons | the top matches by subtask and scene, each checked against the current scene |
| task | task state or none | task memory's state, re-grounded, only for a history-dependent subtask |

```python
@dataclass
class MemoryRead:
    """Advisor memory to Advisor."""
    working_memory: str             # summary: this run so far
    lessons: list[Lesson]           # matching lessons, checked against this scene
    task: TaskState | None = None   # task memory's state, read-gated
# when: every call ② or ③
# built by: Advisor memory (read)
# context.memory = message                   # inside advisor(), after the cap check: memory.read(subtask, images) returns it
# read by: Advisor
```

## e_ledger_obs · every step's view
<!-- box: e_ledger_obs -->
Based on: AGM [2608.29537]: a write is checked at **gripper events**

- **When:** after every chunk that ran, once task memory is on; writes need a change point.

| Field | Type / shape | Meaning |
|---|---|---|
| obs | Observation | the new view, robot state and force |

```python
@dataclass
class MemoryUpdate:
    """Robot moves to Task memory."""
    obs: Observation                # the new view after a chunk
# when: after every chunk that ran, TASK_MEMORY_ON
# built by: Robot moves (robot_follow)
# task_memory.update(message.obs)
# read by: Task memory
```

## e_ledger_read · history for the advisor, when needed
<!-- box: e_ledger_read -->
Based on: SimpleARM [2609.36595]: memory is read **only for history-dependent** subtasks

- **When:** every call ② or ③ whose subtask has a history-dependent field.

| Field | Type / shape | Meaning |
|---|---|---|
| variables | name → value | the task-chosen relations, counts and step order |
| now | object → position | recalled objects, re-grounded in the current images |

```python
@dataclass
class TaskState:
    """Task memory to Advisor memory."""
    variables: dict                 # relations, counts, step order, as the VLM chose
    now: dict                       # recalled objects re-grounded in the current images
# when: call ② or ③ on a history-dependent subtask
# built by: Task memory (read)
# MemoryRead(working_memory, lessons, task=message)   # inside memory.read
# read by: Advisor memory
```

## e_tm_vla · resolved target, for staging
<!-- box: e_tm_vla -->
Based on: SimpleARM [2609.36595]: recalled objects are **re-grounded** before the VLA acts

- **When:** a code answer on a history-dependent subtask, before the VLA's next step.

| Field | Type / shape | Meaning |
|---|---|---|
| target | object → position | the recalled object, re-grounded now |
| route | str | staging now; subtask text and coordinate target each need a checkpoint |

```python
@dataclass
class MemoryToVla:
    """Task memory to Code runner."""
    target: dict                    # the recalled object, re-grounded now
    route: str                      # MEMORY_TO_VLA: staging; subtask, grounded NOT BUILT
# when: a code answer on a history-dependent subtask
# built by: Task memory (to_vla), via the advisor's code answer
# answer.program = found.program or answer.code or task_memory.to_vla(context.memory.task)   # in advisor(): staging last
# read by: Code runner, which hovers over it; then the VLA
```

## e_noise_vla · starting noise + chunk pick
<!-- box: e_noise_vla -->

- **When:** every VLA step, once the noise policy and scorer are trained.

| Field | Type / shape | Meaning |
|---|---|---|
| noises | [N, 50, A] | each candidate's starting noise; plain Gaussian until trained |
| scorer | small network, or none | keeps one candidate; random until trained |

```python
@dataclass
class NoiseAndPick:
    """Noise policy + scorer to VLA."""
    noises: ndarray                 # [N, 50, A] starting noises
    scorer: Scorer | None           # None: pick at random
# when: every VLA step
# built by: Noise policy + scorer (NoisePolicy.sample)
# vla.step(obs, task)   # samples message.noises; pick_index reads message.scorer
# read by: VLA (VLA.step), then Action chunk (VLA) picks
```

## e_lora_vla · weight change
<!-- box: e_lora_vla -->

- **When:** once per redeploy that carries fine-tuned weights.

| Field | Type / shape | Meaning |
|---|---|---|
| lora | low-rank weights | an adapter beside the frozen weights; every VLA step reads it |

```python
@dataclass
class WeightChange:
    """Fine-tuning to VLA."""
    lora: LoRA                      # low-rank weights beside the frozen ones
# when: once per redeploy that carries fine-tuned weights
# built by: Fine-tuning (LoRA.load)
# message.lora.load(vla)   # sets vla.lora
# read by: VLA, on every step
```

## e_tm_seed · track seed
<!-- box: e_tm_seed -->
Based on: SAM 3 [2511.16719]: a **video tracker** keeps one object identity

- **When:** each find step, once task memory is on.

| Field | Type / shape | Meaning |
|---|---|---|
| seed | prompt, or none | a tracked object's prompt while the run is active; none: a concept prompt |

```python
@dataclass
class TrackSeed:
    """Task memory to Vision tools."""
    seed: object | None             # a tracked object's prompt; None outside a run
# when: each find step, TASK_MEMORY_ON
# built by: Task memory (TaskMemory.seed)
# mask = sam3_1.track(images, object_name, message.seed)   # inside perceive
# read by: Vision tools (perceive)
```

## e_tm_log · memory events
<!-- box: e_tm_log -->
Based on: RegenHarness [2609.27612]: every record is **appended**, never overwritten

- **When:** each committed task-memory write.

| Field | Type / shape | Meaning |
|---|---|---|
| step | int | the env step of the write |
| state | dict | the task state after the write |

```python
@dataclass
class MemoryEventOut:
    """Task memory to Advisor memory."""
    step: int                       # env.steps at the write
    state: dict                     # the committed task state
# when: each committed write, TASK_MEMORY_ON
# built by: Task memory (TaskMemory.update)
# memory.record_event(MemoryEvent(message.step, message.state))
# read by: Advisor memory (record_event); the run log via e_log
```

## e_buf_exp · gate-fire states
<!-- box: e_buf_exp -->

- **When:** each offline round.

| Field | Type / shape | Meaning |
|---|---|---|
| states | list of gate-fire states | each: saved sim state, the observation the gate saw, task and subtask |

```python
@dataclass
class TreeRoots:
    """Run log (event store) to Try fixes + verify."""
    states: list[GateFireState]     # saved states where the gate fired
# when: each offline round
# built by: Run log (event store) (RunLog.gate_fire_states, from Step.sim_state)
# generate_fixes(message.states)
# read by: Try fixes + verify
```

## e_reset_exp · same state
<!-- box: e_reset_exp -->
Based on: RE-0 [2609.32416]: **restore a saved snapshot**, then run from it

- **When:** before every tree-search branch.

| Field | Type / shape | Meaning |
|---|---|---|
| state | scene variant + physics + objects + robot | the saved state, given by tree search: root.sim_state |
| obs | images + state + force | the restored observation |

```python
@dataclass
class ResetToState:
    """Sim reset to Try fixes + verify."""
    state: SimState                 # one saved moment: scene variant, physics, objects, robot
    obs: Observation                # the restored observation
# when: before every tree-search branch
# built by: Sim reset (sim_reset)
# code_agent.fix(root, message.obs)          # inside generate_fixes (tree_search plug-in): obs = sim_reset(root.sim_state), then the branch
# read by: Try fixes + verify
```

## e_exp_mul · verified paths
<!-- box: e_exp_mul -->
Based on: DART [1703.09327]: **perturb around good paths** to collect recoveries

- **When:** after tree search.

| Field | Type / shape | Meaning |
|---|---|---|
| fixes | code + VLA paths | only those the sim's goal check accepted |

```python
@dataclass
class VerifiedFixes:
    """Try fixes + verify to Push off + recover."""
    fixes: list[Fix]                # code + VLA paths the sim's goal check accepted
# when: after tree search
# built by: Try fixes + verify (generate_fixes)
# push_off_and_recover(message.fixes)
# read by: Push off + recover
```

## e_reset_mul · same path
<!-- box: e_reset_mul -->
Based on: RE-0 [2609.32416]: **restore a saved snapshot**, then run from it

- **When:** before every push-off.

| Field | Type / shape | Meaning |
|---|---|---|
| state | scene variant + physics + objects + robot | the fix's saved root state, where the verified path replays from |
| obs | images + state + force | the restored observation |

```python
@dataclass
class ResetToPath:
    """Sim reset to Push off + recover."""
    state: SimState                 # the fix's root state
    obs: Observation                # the restored observation
# when: before every push-off
# built by: Sim reset (sim_reset)
# push_off(fix.path, message.obs)            # inside push_off_and_recover: obs = sim_reset(fix.root.sim_state)
# read by: Push off + recover
```

## e_pairs · sim-labelled pairs
<!-- box: e_pairs -->

- **When:** once the VLA proposes several candidates, after the roots are chosen.

| Field | Type / shape | Meaning |
|---|---|---|
| pairs | list of better + worse chunk | one success and one failure from the same root, sim-labelled |
| vla_version | int | the VLA the candidates came from; other versions are pruned |

```python
@dataclass
class ScorerPairs:
    """Try fixes + verify to Learn + keep VLA frozen."""
    pairs: list[PreferencePair]     # better and worse candidates from one root
    vla_version: int                # pairs from this VLA only
# when: N_CANDIDATES > 1, in generate_fixes
# built by: Try fixes + verify (candidate_pairs)
# train_scorer(current_pairs(vla))           # in learn: this VLA's pairs, roots not quarantined
# read by: Learn + keep VLA frozen
```

## e_mul_trig · fixes + recoveries
<!-- box: e_mul_trig -->

- **When:** each offline round.

| Field | Type / shape | Meaning |
|---|---|---|
| candidates | list of fixes | tree-search fixes, recoveries and saved runtime fixes, each with its verified flag and episodes |

```python
@dataclass
class TrainCandidates:
    """Push off + recover to Count + decide."""
    candidates: list[Fix]           # tree-search fixes and recoveries
# when: each offline round
# built by: offline_round (saved_runtime_fixes + generate_fixes + push_off_and_recover)
# [c for c in lcb_order(message.candidates) if should_train(c, message.candidates)]   # lcb_order once PAIRED_LCB_ON: untested on this VLA version first
# read by: Count + decide
```

## e_buf_trig · saved runtime fixes
<!-- box: e_buf_trig -->
Based on: ASPIRE [2607.00272]: **validated repairs** from real runs are what recurs

- **When:** each offline round, before the count.

| Field | Type / shape | Meaning |
|---|---|---|
| fixes | list of fixes | the advisor's runtime repairs, each voting for its own episode |

```python
@dataclass
class SavedRuntimeFixes:
    """Run log (event store) to Count + decide."""
    fixes: list[Fix]                # ② code answers and ③ answers, from trusted runs
# when: each offline round, after the verifier audit
# built by: saved_runtime_fixes(trusted), reading the run log
# candidates = message.fixes + searched   # inside offline_round
# read by: Count + decide
```

## e_trig_learn · yes: train
<!-- box: e_trig_learn -->

- **When:** a candidate is verified and seen in enough separate runtime episodes.

| Field | Type / shape | Meaning |
|---|---|---|
| approved | fixes | verified, repeating over distinct runtime episodes |

```python
@dataclass
class ApprovedFixes:
    """Count + decide to Learn + keep VLA frozen."""
    approved: list[Fix]             # verified, repeating over distinct runtime episodes
# when: verified and seen in enough runtime episodes
# built by: Count + decide (should_train)
# learn(vla, message.approved)
# read by: Learn + keep VLA frozen
```

## e_learn_chk · trained parts
<!-- box: e_learn_chk -->
Based on: FlowDAgger [2607.08877]: check **held-out tasks** after training a noise policy

- **When:** after training.

| Field | Type / shape | Meaning |
|---|---|---|
| noise policy | small network | picks the VLA's noise |
| scorer | small network | reranks the VLA's candidate chunks |
| skill candidates | fixes | the VLA cannot make these; they get the skill dry run |
| lora | low-rank weights, or none | only after a stall; checked held-out |

```python
@dataclass
class Trained:
    """Learn + keep VLA frozen to Check + re-fit."""
    noise_policy: NoisePolicy | None = None # small network: picks the VLA's noise
    scorer: Scorer | None = None    # small network: reranks candidates
    skill_candidates: list[Fix] = field(default_factory=list) # the VLA cannot make these
    lora: LoRA | None = None        # only after a stall
    version: int = field(default_factory=lambda: next(VERSION_IDS)) # unique per Trained (VERSION_IDS = itertools.count(1)); vla.load adopts it
# when: after training
# built by: Learn + keep VLA frozen (learn)
# checks(vla, message)
# read by: Check + re-fit
```

## e_admit · admit as a skill
<!-- box: e_admit -->
Based on: ASPIRE [2607.00272]: only **validated repairs** enter the skill library

- **When:** a skill candidate has had its skill dry run.

| Field | Type / shape | Meaning |
|---|---|---|
| skill | code + tag | verified code + VLA skill: use it, known to fail, or blocked (failed twice) |

```python
@dataclass
class AdmittedSkill:
    """Check + re-fit to Skill library."""
    skill: Skill                    # code + tag: POS, NEG or BLOCKED
# when: a skill candidate has had its skill dry run
# built by: Check + re-fit
# skill_library.admit(message.skill)        # inside SkillLibrary.dry_run
# read by: Skill library
```

## e_redeploy · redeploy: noise policy + scorer
<!-- box: e_redeploy -->
Based on: DAgger [1011.0686]: deploy the improved policy, then **collect where it fails**

- **When:** once the trained parts pass Check + re-fit; every VLA step then reads them.

| Field | Type / shape | Meaning |
|---|---|---|
| noise policy | small network | picks each candidate's starting noise; trained on noise labels plus own successes |
| scorer | small network | reranks the VLA's candidates; trained on sim-labelled pairs from Try fixes + verify |
| calibration | gate threshold + scale | re-fit on the new VLA's runs; unchanged while the gate is accel only |
| version | int | the trained parts' version number |

```python
@dataclass
class Redeploy:
    """Check + re-fit to Noise policy + scorer: the trained parts."""
    noise_policy: NoisePolicy | None    # picks each candidate's starting noise
    scorer: Scorer | None               # reranks the VLA's candidates
    calibration: GateCalibration | AccelPlusCalibration # threshold + scale, re-fit on the new VLA's runs
    version: int                    # the Trained.version it came from: vla.load sets vla.version to it
# when: after passed checks; then read on every VLA step
# built by: Check + re-fit (checks), after passed held-out and OOD checks
# vla.load(message.noise_policy, message.scorer, message.calibration, message.version)
# read by: Noise policy + scorer, then VLA.step and pick_index
```

## e_redeploy_lora · redeploy: fine-tuning
<!-- box: e_redeploy_lora -->

- **When:** after a stall, once the fine-tuned weights pass Check + re-fit.

| Field | Type / shape | Meaning |
|---|---|---|
| lora | low-rank weights | trained on fixes the VLA cannot make; kept only if held-out is no worse |
| version | int | the trained parts' version number |

```python
@dataclass
class RedeployLora:
    """Check + re-fit to Fine-tuning (last resort): the last-resort weights."""
    lora: LoRA                      # only after a stall and passed checks
    version: int                    # the Trained.version it came from
# when: after a stall and passed checks
# built by: Check + re-fit (checks), when trained.lora is set
# vla.load(vla.noise_policy, vla.scorer, vla.gate_calibration, message.version, lora=message.lora)
# read by: Fine-tuning (last resort), then the VLA on every step
```

# Entry

## Entry point

The program's last line: every def and class above, the Arrows dataclasses included, exists before main() runs; the Arrows message and call lines are comments, so nothing there runs.

```python
def main():
    """The module's entry: refuse unset constants, restore saved state, then stage 2 once STAGE2_ON."""
    if unset := unmeasured_constants():                       # every TO_MEASURE or PRESET an enabled path reads
        raise ValueError(f"measure or pre-register these first: {unset}")
    load_state_of_system()
    if STAGE2_ON and accel_only(vla.gate_calibration):        # a restored ACCEL+ calibration stays
        vla.gate_calibration = stage2_calibration()
        save_state_of_system()
main()                                                        # called last: every class and def it reaches is above
```

# Integration tests

Unit tests check one box on its own; an integration test runs real neighbouring boxes together and checks the messages on the arrows between them.
Each row names the boxes it crosses (diagram ids), so a box's panel lists every integration test that runs through it.
Status is what the notes in `_build/notes/` show; nothing here has been run for this guide.

| Test | Boxes | Proves | Status |
|---|---|---|---|
| IT1 VLA to gate | vla, unc | the gate scores real π0.5 denoise paths; the scan sampler matches the original bit for bit | partial: tests/integration/test_sampler_parity.py exists (needs ≥14 GB GPU); not run here |
| IT2 gate to advisor and back | unc, adv | a fired gate pauses the robot, calls the advisor, and the hand-back resets the gate | built: tests/integration/test_gate_to_advisor.py with fakes; live in the e2e runs L1 and K1 |
| IT3 code assists the VLA | adv, skills, runner, vision, codechunks, safety, robot | code stages the arm at the pre-grasp pose and the VLA then grasps (experiment A) | partial: one live LIBERO run (K1) recovered a missed grasp; experiment A not run |
| IT4 failure and recovery | robot, fail, adv | a failed verdict reaches call ③ and the recovery chunks run | built: the e2e run R2 ran call ③ to a verified success |
| IT5 one full LIBERO episode | task, vla, unc, vlachunk, adv, safety, robot, fail, endok, endhuman | a run ends as a verified success or a hand-off, with every step saved | built: the e2e runs L1 and L2 ended as verified successes (scripts/run_episode.py) |
| IT6 runtime to offline data | fail, buf, reset, expand, multiply | saved gate-fire states reload in sim and tree search finds verified fixes | not built: no mid-episode sim reset |
| IT7 one offline round | buf, trigger, learn, checks, vla | trained parts pass held-out checks and redeploy with a re-fit gate | not built |
| IT8 skill admission | checks, skills, adv | a dry-run-checked skill is admitted and tried first at runtime | not built: the library exists, nothing admits a skill |
| IT9 a lesson carries a repair | fail, mem, buf, adv | a repair verified in one run is written as a lesson and changes the advisor's answer the next time the same failure appears | not built: working memory exists, no lessons |
| IT10 task memory | vision, ledger, mem, adv | an evidence-gated write keeps one identity per task object across chunks, and a history-dependent subtask reads it, re-grounded | not built: no task memory |
| IT11 self-correction | vlachunk, selfcorrect, robot, fail, adv | a triggered monitor truncates a VLA chunk, the next VLA step is one guided re-call, and past a few tries call ③ runs | not built: no monitor |

# Ablation plan

Rule: build the pipeline on every ★ main option, then knock out one choice at a time; which rows run is decided later.
One row per decision whose alternatives are compared later.
Episodes per arm: TO_MEASURE.
Every gate arm is scored on the same shadow recordings: the VLA alone, RUN_SHORT off, each run labelled by the sim's goal check (env.success), so no arm changes what was recorded.
These scoring runs are recorded on ablation_starts, a split disjoint from every other split, so never in the reference, fit or check calibration sets.
After stage 2 they still run RUN_SHORT off: record_shadow_runs(ablation_starts, calibration=load_calibration(robot.name)) passes the stage-1 accel-only calibration explicitly.
Every gate arm, ACCEL+ included, is calibrated on the stage-2 first pass, recorded under the accel-only previous calibration (RUN_SHORT off), never on ACCEL+'s second pass, whose RUN_SHORT rows would favour ACCEL+.
Arms that need labels (SAFE, FAIL-Detect) train on labelled shadow_log runs on shadow_starts (successes and failures, by env.success), never on ablation_starts.
False-alarm rates on in-distribution successes carry the conformal guarantee; OOD false-alarm and detection rates are measured, not guaranteed.
Arms are compared and chosen on EVAL_LEVELS only; FINAL_LEVELS and final_held_out_starts score, once, only the arms pre-registered before that run.
VFD is the exception: it runs its own M = 2 fine-tuned SmolVLA models, so it is scored on the same tasks and seeds, not on the same recordings.
The RUN_SHORT row and the self-correction rows change what runs, so they need live runs, each arm with its own calibration.
Detection lead counts chunks before the episode ends, the only failure time the sim gives.
Memory rows also run on RoboMME [2603.04639], the memory benchmark: 16 history-dependent manipulation tasks; every RoboMME row needs a RoboMME-trained checkpoint, none exists yet (NOT BUILT).
Pre-registered headline metric for every row: the share of steps under the VLA, reported next to the row's own metric (DynaHarness: 570 of 770 episodes never call π0.5, at 96.7% success, while episodes that call π0.5 succeed 6.0%, so success alone can hide a VLA that barely acts).

| Decision | Main (★) | Arms compared | Metric | Benchmark |
|---|---|---|---|---|
| What tells the VLA it is unsure? | ACCEL+ | accel + CUSUM (A, built), learned ask (B), UPS (C), a learned probe (D; settings: SAFE own features, ActProbe actions, FailPatch action-hidden probe on labelled shadow failures), distance from the training data (E; settings: FAIL-Detect scene density, VLA-FAIL fixed-noise Mahalanobis distance or chunk consistency), disagreement across model variants (study; PFD weight perturbation, VFD fine-tuned ensemble), dynamics mismatch (study, logged only; VLA-Corrector latent, ActionGround residual), in-context WAM prediction error (study, logged only; Zero-WAM with a retrieved success vs LingBot-VA without, success-only conformal score plus a motion check) | AUROC of episode-peak S; TPR/TNR at eta; realized false-alarm rate on successes; detection lead in chunks before the episode ends; false alarms at contact phases; latency per chunk | LIBERO-Plus + LIBERO-MAX Lite |
| Which ACCEL+ parts are on? | All parts (1 to 5) | per-dimension accel only (1), + label-free prefix choice (2), + phase reference (3), + bend shape (4), + part 5 (chunk overlap, executed-action stats, stall), covariance probe (study arm), + 4-phase reference (ActionGround detector); the ACCEL+ rows below follow accel_plus.py ABLATIONS order | AUROC of episode-peak S; TPR/TNR at eta; realized false-alarm rate on successes; detection lead in chunks before the episode ends; false alarms at contact phases; latency per chunk | LIBERO-Plus + LIBERO-MAX Lite |
| What happens when the VLA is unsure but typical? | Unsure but typical: run SHORT_STEPS (2) rows, then look again | run the normal EXEC_STEPS rows | live runs: task success with adaptive horizon; advisor calls per episode; latency per chunk | LIBERO-Plus + LIBERO-MAX Lite |
| How are lessons written across runs? | Each offline round, after the verifier audit, behind gates, from training runs only | every run's reflection (flat reflection), code-skill lessons (RoboSkill), no lessons; support and oppose counts (RoboHarn-Evo) are a setting of the main | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode | LIBERO-Plus + LIBERO-MAX Lite |
| Which gate-fire states are worth exploring? | PFD (epistemic) | ACCEL+ bend shape, representation distance (FIPER), every gate-fire state, most frequent failing subtask first (SEES) | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode | LIBERO-Plus + LIBERO-MAX Lite |
| What learns first? | Noise policy + reranking scorer | noise RL (DSRL, PSS), denoising guidance (PreferenceFlow, PPS), action residual | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode | LIBERO-Plus + LIBERO-MAX Lite |
| Who decides: VLA corrects itself, or the advisor helps? | Self-correct first, the advisor after SELF_CORRECT_TRIES fail | the advisor decides (settings: each time, with retry_vla, or always, the current), self-correct only | live runs: OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA; latency per chunk | LIBERO-Plus + LIBERO-MAX Lite |
| How does the VLA self-correct? | Truncate + OGG replan (plain replan is its setting) | stage-prompt re-call (Stage-Aware VLA-Corrector [2609.06508]), no self-correction | live runs: task success; recoveries per episode; truncations by phase (VLA-Corrector: 83.7% in critical phases); share of steps under the VLA; the RUN_SHORT interaction (gap runshort-truncation) | LIBERO-Plus + LIBERO-MAX Lite |
| What does task memory track? | Task-chosen state: relations, counts, step order (SimpleARM) | fixed fields (positions, anchors, stage counter); kinds of the main: OCC4M world tracks + containment, RoboStream event log, ECoMEM concept writer | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA; success on history-dependent subtasks | LIBERO-MAX Lite + RoboMME (needs checkpoint) |
| When is task memory read? | Only for a history-dependent subgoal (SimpleARM) | every advisor call, never: a fresh find per call (current); settings of the main: the advisor decides (NavHarness), staleness decay (DART-VLN) | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA; null control: the gain on LIBERO-MAX Lite mid-task changes vs on LIBERO-Plus static factors | LIBERO-Plus + LIBERO-MAX Lite + RoboMME (needs checkpoint) |
| How does memory reach the VLA? | Arm staging: the code runner hovers over the recalled object | advisor subtask text (π0.5 base; TOWN-VLA fixed template as a setting), grounded coordinate subgoal (RoboMME GroundSG π0.5, needs a checkpoint); TempoFit KV-cache reuse is now a π0.5 setting; chosen after the Phase 4 probes | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA; latency per chunk | LIBERO-MAX Lite + RoboMME (needs checkpoint) |
| What triggers a memory write? | Change points in gripper and arm motion (ProTracer), gripper part first (AGM) | every step | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA; tool calls per episode; missed changes against the sim's object state | LIBERO-MAX Lite + RoboMME (needs checkpoint) |
| What history does the advisor see? | Fixed anchor frames + the latest step (RoboICL) | first and most recent frames, a summary of the full trace | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA | LIBERO-Plus + LIBERO-MAX Lite + RoboMME (needs checkpoint) |

Rows without a decision in the register: an arm set kept as a gap, and an external baseline.

| Row | Main | Arms compared | Metric | Benchmark |
|---|---|---|---|---|
| nearby_roots scene ranking (gap scene-rank) | FATE-VLA / RoboMD ranking | failure-weighted start sampling (EmbodiRSI [2609.38905]), broad randomization (F4R [2609.35575]'s control) | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA | LIBERO-Plus |
| External baseline: DynaHarness | our pipeline on every ★ option | DynaHarness on the same frozen π0.5 LIBERO checkpoint, re-run multi-seed | OOD success (VLA alone first, advisor calls second); held-out drop; advisor calls per episode; share of steps under the VLA | LIBERO-Plus + LIBERO-MAX Lite |

ACCEL+ rows, in accel_plus.py ABLATIONS order, each adding one part to the row before:

| Row | Adds | Metric |
|---|---|---|
| accel_baseline | ACCEL: one accel over all dimensions, fixed prefix, CUSUM | AUROC of episode-peak S; TPR/TNR at eta; realized false-alarm rate on successes; detection lead in chunks before the episode ends; false alarms at contact phases; latency per chunk |
| +per_dim | part 1: accel per action dimension | same |
| +phase | part 3: phase reference (free, grasped, transition) | same |
| +prefix_select | part 2: label-free prefix choice | same |
| +bend_shape | part 4: direction flips and bend timing | same |
| +accel_blind_signals | part 5: chunk overlap, executed-action statistics, progress stall | same |
| +cov_probe | covariance probe (study arm), latency reported apart | same |

# Improvement plan

Each stage starts only when its trigger holds; each closes a gap or a decision.
Stage numbers are labels, not order: 11 to 14 were added later, and each says where it falls (stage 11 runs after stage 1, before stage 3).

1. Build the main path with the gate in accel-only mode: the built `CusumGate` with its built slack (0.25 sigma) and `fixed_std`, no `RUN_SHORT`, the self-check off (verifier only) until ACCEL+ is calibrated.
   The Sentinel verifier is built here, for runtime only; in sim, every reported success and every offline training label always comes from the sim's goal check (env.success, `BUILT`), and the verifier audit compares the `task_done` verdicts in saved runtime fixes with `env.success` logged at that same step, counting only verifier misses and false passes (the task's truth file tells a verifier miss from a lenient sim); `rollout(fix)` runs the fix, then the VLA alone with no advisor call, in a fresh run scope logged to `shadow_log` only.
   Offline, before learn, when `own_success_noise` is empty, one shadow pass on the in-distribution `shadow_starts` under the current calibration records the VLA's own successful noise; the noise policy trains only once that buffer is non-empty (FlowDAgger's second buffer).
   Trigger: now; its offline part (tree search, push-off) waits for gap reset (mid-episode sim reset), so `offline_round` takes no tree roots until `SIM_RESET_BUILT`.
   Closes: the build gaps on every ★ option.
2. Calibrate ACCEL+ on successful runs (reference set, fit set for the thresholds, check set for the conformal check), without a circular loop: record them in shadow mode on the in-distribution `shadow_starts` under the previous calibration (the VLA truly alone: ① is kept, the verifier's `SUBTASK_DONE` still advances the subtask as at runtime, and no other verdict acts; no ② or ③, no code; a run ends on env.success, the step limit or a refused chunk, a failure), fit, then record once more under that first fit and re-fit once on the second pass; deployed as `vla.gate_calibration = stage2_calibration()` behind `STAGE2_ON` (`main()`, C7 section), which runs `calibrate_accel_plus` once `stage2_trigger(successes)` holds, no training needed, and `checks()` re-fits it each round after (while the gate is still accel only, `checks()` tries `stage2_calibration` on each new VLA); `successes` reuses the current version's in-distribution shadow successes recorded under the accel-only gate, one per start, when enough exist, else one fresh pass; a pass with fewer than `MIN_CHECK_RUNS` check-set runs keeps the previous calibration (logged).
   Trigger: shadow runs of the VLA alone on in-distribution LIBERO hold enough successes, by the sim's goal check, for three disjoint sets with the check set at least 9 runs (ACCEL used 50; our counts to be measured).
   Closes: gap accel-plus; What tells the VLA it is unsure?
3. Add the PFD filter and scene variation to tree search (`PFD_AND_SCENES_ON`), inside the `ROOTS_PER_ROUND` and `SCENES_PER_ROOT` budgets; until then every gate-fire state is a start state for tree search.
   Trigger: mid-episode sim reset works, including the LIBERO-Plus variant, and PFD's cost is measured (gap pfd-cost).
   Closes: gaps pfd-filter, scene-roots; Which gate-fire states are worth exploring?
4. Train the SAFE probe.
   Trigger: shadow runs of the VLA alone on `shadow_starts` (in-distribution plus `TRAIN_LEVELS`, disjoint from the held-out, anchor and final starts) hold N successes and N failures, labelled by the sim's goal check (`shadow_log` keeps the failures too; SAFE trains on both; N to be measured).
   Closes: gap safe-probe; How does the VLA check its own progress?
5. Add the WAM arm for prediction error, Cosmos Policy first: the prediction-error result was measured on it, while VLA-JEPA's paper does not say it predicts futures at inference.
   Trigger: the π0.5 path passes `IT5`.
   Closes: gap wam-arm; Which policy?
6. Add APPL-style skill cards.
   Trigger: the skill library holds checked skills.
   Closes: gap skill-cards.
7. Turn the LoRA fallback on (`LORA_ON`) and try Finetuning with Sampling for it.
   Trigger: the frozen path stalls (`STALL_ROUNDS`), which needs approved fixes, so repair keys must match across episodes (gap repair-key).
   Closes: gap fws; May the VLA's weights change?
8. Add a trained model checkpoint for the real robot.
   Trigger: before the first real run.
   Closes: gap real-robot.
9. Set `N_CANDIDATES` above 1 and turn the reranking scorer on: `pick_index` then reads `scorer(obs, task, chunk)`, trained on tree-search PreferencePairs tagged with their VLA version.
   Trigger: π0.5's latency per chunk with N > 1 candidates is measured (gap candidates-latency).
   Closes: gaps candidates, scorer; How is one candidate chunk picked?
10. Score `FINAL_LEVELS` and the in-distribution `final_held_out_starts` once, together, with `final_eval` (C7), VLA alone, by the sim's goal check; only the arms pre-registered from `EVAL_LEVELS` results are scored.
    Trigger: after the last offline round.
    Closes: gap final-split.
11. Turn task memory on (`TASK_MEMORY_ON`), reusing SimpleARM's code: at run start a VLM names the task-chosen state; on a gripper change, frozen tools propose an update that commits only with visual proof (the evidence gate); a history-dependent subtask reads the state, re-grounded in the current view; it reaches the VLA by code-runner staging (`MEMORY_TO_VLA`) and the advisor through `memory.read`; the find step seeds its tracker from it during a run; in shadow runs it only logs.
    Phase 4 probes our π0.5 checkpoints on (a) the full instruction vs advisor subtask text and (b) two identical objects, "pick the left one", plus TempoFit's KV-cache reuse, now a π0.5 setting; their results pick later `MEMORY_TO_VLA` routes.
    Runs after stage 1, placed before stage 3 (PFD) only as an order, not a dependency.
    Trigger: SAM 3 tracking works (gap track); `IT10` then tests task memory itself.
    Closes: gaps ledger, ledger-latency, tm-to-vla; What does task memory track?; When is task memory read?; How does memory reach the VLA?
12. Fix admission (`PAIRED_LCB_ON`): `should_train` also needs the fix to beat the VLA's own resample from the same state, with shared seeds, by a paired lower confidence bound (RE-0), on `TRAIN_LEVELS` only.
    Runs after stage 1, once `SIM_RESET_BUILT`, with or after stage 3.
    From this stage ③'s first chunk also saves its `sim_state`, so a ③ saved fix is eligible; runs recorded before it have none and their ③ fixes are never LCB-tested; verdicts are cached per (`root_id`, `repair_key`, `program_hash(program)`, vla.version), so each distinct program gets its own test, a saved fix's `root_id` being (episode id, index of its first Step) and a recovery's root id is its fix's root id plus "pushed" plus its fix's program hash; each event costs 2 x `LCB_PAIRS` rollouts with one fix, at most `LCB_BUDGET` per round (past it a fix waits, untested); no advisor call inside a paired rollout; a real-robot fix (no sim state) falls back to verified + repeats.
    Trigger: `SIM_RESET_BUILT`.
    Closes: gap paired-lcb; What makes the advisor start training?
13. Turn grasp memory on (`GRASP_MEMORY_ON`): the find step ranks the candidates' approach axes by a Beta posterior over the nearest past outcomes, each the VLA's grasp from that hover, embedded by the axis read at its close (a staging the VLA runs on and never closes is a miss), lifted by `GRIPPER_CLOSED_WIDTH` from the robot spec, written on `TRAIN_LEVELS` runs only; the encoder is trained once offline on sim grasps (gap grasp-data).
    Runs after stage 1, whose run log gives the ③ failures.
    Trigger: the run log shows grasp failures are a measurable share (to be measured) of ③ failures (gap grasp-share); top-down lifted 4 of 4 today, so it may never fire.
    Closes: gaps graspmem, grasp-data, grasp-transfer; How are grasp candidates ranked?
14. Turn VLA self-correction on (`SELF_CORRECT_ON`), on LIBERO only until a RoboDojo monitor exists (gap selfcorrect-robodojo): the latent monitor watches each executed VLA row at k = `LVM_K` steps, truncates on a sustained mismatch, makes one OGG-guided re-call, and past `SELF_CORRECT_TRIES` the `FAILED` path asks the advisor; in shadow runs it only logs.
    Runs after stage 2: the gate and self-check are calibrated with it off; the guided re-call is not gate-scored and a truncated chunk's overlap feature is missing, but truncated and guided rows still enter `executed_history` and `stall_inputs`, so their residual effects on part 5 are measured (gap runshort-truncation).
    Trigger: the monitor is trained once on LIBERO demos (π0.5 frozen) and its per-step encoding cost is measured.
    Closes: gaps selfcorrect, selfcorrect-ood, runshort-truncation; Who decides: VLA corrects itself, or the advisor helps?; How does the VLA self-correct?

# Proposed picks for the open decisions

| Decision | Pick | Why |
|---|---|---|
| What tells the VLA it is unsure? | ACCEL+: accel per action dimension, compared per task phase, summed by CUSUM | ACCEL+ keeps accel's single-pass, label-free rule and fixes its averaging and calibration; accel stays the built baseline, and the probes and ensembles are study or labelled-run alternatives. |
| Which ACCEL+ parts are on? | All parts | Build all parts, then knock each out in the method file's own order. |
| How many unsure calls per subtask? | Cap per subtask, then ask a human | The cap counts ② calls per subtask; without it, code-then-unsure loops never end. |
| May code moves use a motion planner? | Bounded steps only | No planner keeps results comparable with planner-free baselines, and the hover move already exists. |
| Where does the hover stop? | The demos' pre-grasp pose | The hand-over back to the VLA must land inside its training data; RoboDojo, whose demos carry no object poses, uses a fixed clearance. |
| Which grasp model? | Contact-GraspNet | It runs today, with top-down grasps first because they lifted 4 of 4 tries. |
| How many tries before asking a human? | Few tries | Each failed try risks the robot while failed runs still feed offline training, so the count stays small and is measured. |
| Should the VLA get subtasks? | Keep the task text | Our LIBERO π0.5 may ignore new wording (LIBERO-Plus: language ignorance), so subtasks go to the advisor and verifier until the Phase 4 wording probe. |
| What does the verifier look at? | Images + robot state, plus force where the robot has it | Images and state are harder to fool than images alone; force joins on a robot that measures it, none on LIBERO or RoboDojo today. |
| Where does offline training run first? | LIBERO, with OOD splits | LIBERO gives free resets and ready OOD splits, once the perception tools lose their RoboDojo names. |
| Who labels the fix? | The advisor, writing code + VLA fixes | The advisor's code covers OOD fixes the VLA cannot reach, while the scorer's pairs come from sim-labelled tree-search candidates. |
| How do we get many fixes per failure? | Tree search from where the gate fired | Labels only help on states the VLA visits, so the search starts there. |
| Which gate-fire states are worth exploring? | Weight-perturbation disagreement: states unsure from too little training | Only those states teach the VLA something new, and PFD beat sampling on 12 LIBERO-PRO suites with π0.5; its score above a measured cut-off is our own use of it. |
| How are recoveries labelled? | Ask the advisor again, from the pushed-off state | In sim, physics renders the images, so only the label matters. |
| What makes the advisor start training? | Verified, repeats, and a paired win over a VLA retry | Repeating failures are worth teaching, and once mid-episode reset works a fix must also beat the VLA's own resample from the same state. |
| How does a fix become a label? | Run the VLA backwards to its noise | The reconstruction error doubles as the router, and FRS in-painting only pads code chunks shorter than 50 rows. |
| What learns first? | Noise policy + reranking scorer | It is the cheapest safe step; the others are the alternatives. |
| What counts as a repeat? | Distinct runtime episodes only | Search turns one fix into many copies, so only real episodes may vote. |
| How is the gate re-fit after training? | Re-fit on new successful runs | A new noise policy changes the spread the gate reads. |
| What does the advisor remember within a run? | Typed working memory | RACaP keeps a task-objective working memory beside its experience memory and Mimir grounds memory in the scene, and a typed schema makes the per-subtask cap simple. |
| How are lessons written across runs? | Each round, after the audit, behind gates, training runs only | Unverified memory hurts (Living-Harness without its commit gates: 73.38 vs 83.09), so only audited, gated fixes from training runs become lessons, merged per repair with a support count. |
| How does the advisor use a retrieved lesson? | Check it against the scene, then adapt or reject | MemHarness's rebuilt memory beat replay (85.9 vs 82.4), though its prompt-only rewriter did not, a risk measured in gap repeat-rate. |
| Should the VLA get a success-memory prior? | Later, once the verifier exists | Retrieve-then-Steer gains with verified memory (92.4% to 94.4%) and loses with unverified memory (87.6%). |
| How does the VLA check its own progress? | ACCEL+'s last part: progress stall, chunk overlap, executed actions | It works from the first calibration, its cut-off set like the gate's, and the SAFE probe is the upgrade once labelled runs exist. |
| What does the VLA get in context? | Nothing: π0.5 has no demo slot | π0.5 takes three cameras, state and the task text only, so retrieved successes need an in-context policy (ContextFlow, Zero-WAM), an alternative to measure. |
| Which policy? | π0.5: LIBERO-finetuned, base or coordinate-target checkpoint | π0.5 stays the main policy on its LIBERO checkpoint, a world-action model adds a future-side signal, and the base and GroundSG checkpoints and TempoFit's cache reuse are settings the Phase 4 probes pick from. |
| How is one candidate chunk picked? | Our reranking scorer | The scorer is what offline training builds, and the other pickers show what it adds. |
| What happens when the VLA is unsure but typical? | Run a few rows, then look again | A short commit sits between running a chunk and asking (two rows, from the method file); it is ACCEL+ only, since the accel + CUSUM gate has no such branch. |
| Which advisor model? | Claude Code | It runs on both robots, with Codex and a lighter advisor as the comparison. |
| How is the verifier built? | A VLM progress check: pass, fail or can't tell | It is independent of the VLA and needs no task training, and a can't-tell verdict looks once more before it counts. |
| What does call ③ try first? | Ask the advisor how to recover | The advisor sees the trace, and a cheap VLA retry, then ask, is the alternative that may make ③ rarer. |
| Where does depth come from? | Depth Anything 3 | It must work on a real robot, and sim ground truth measures what depth errors cost. |
| Track the object or re-detect it? | Track the mask with a video tracker | The moved and held checks need the same object over time. |
| Which OOD suite? | LIBERO-Plus, plus LIBERO-MAX Lite for mid-task changes | Our LIBERO checkpoint runs as is and plain LIBERO stays the in-distribution split, while RoboDojo's split comes second. |
| Who decides: VLA corrects itself, or the advisor helps? | Self-correct first, the advisor after a few failed tries | VLA-Corrector fixes drift inside π0.5's prior without an advisor call, and it stays off until its monitor is trained and timed. |
| How does the VLA self-correct? | Truncate + a re-call, monitor-guided or plain | VLA-Corrector at our horizon (H = 10) rose from 64.50 to 72.40 on π0.5 MetaWorld, guidance adds over a plain re-call, and no self-correction is the baseline. |
| What does task memory track? | Task-chosen state: relations, counts, step order | SimpleARM's VLM names the state from the instruction and frozen tools fill it, training-free, reaching 67.17% on RoboMME vs 44.51% for the strongest baseline; tracks, event logs and concepts are kinds of that state. |
| When is task memory read? | Only for a subtask that depends on history | SimpleARM's VLM-decided reads at every subgoal lost 11.9 points. |
| How does memory reach the VLA? | Arm staging: the code runner hovers over the recalled object | Staging works with today's LIBERO π0.5, whose language following is unmeasured, so subtask text and grounded subgoals wait for the Phase 4 probes. |
| What triggers a memory write? | Change points in gripper and arm motion | Most changes come from grasps and releases, so the gripper part (AGM) runs first, arm change points (tested offline only) next, and every step costs a tool call. |
| What history does the advisor see? | Fixed anchor frames + the latest step | RoboICL's anchored memory beat first plus recent frames, 80.25 vs 73.50, with a frozen VLM. |
| What examples does the advisor get in context? | Matching lessons only | Gated lessons already reach calls ② and ③; RoboHarness's raw success and failure runs (LIBERO-PRO 2.33% to 57.2%) and RoboICL's demos are alternatives to measure. |
| What carries over when the advisor's context resets? | Structured handover: places, ruled-out and untried options, landmark | NavHarness's plain summary of matched length lost 8.3 points of success, an empty handover 8.6. |
| How are grasp candidates ranked? | Success odds of the nearest past VLA grasps | CL-Grasp's past outcomes rerank candidates without training, and it stays off until grasp failures prove common, which may never happen since top-down lifted 4 of 4. |
| What must a round pass to redeploy? | Held-out no worse + a significant paired OOD gain | The two paired tests stay the rule, and per-cell constraints on the evaluation levels are the stricter alternative. |
