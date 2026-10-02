# Hybrid System V2 pseudocode

This file is the source of truth for the pseudocode in `hybrid-system-architecture-v2.html`; review changes here with `git diff`.
Each `## ` section below is one box or one arrow: clicking it in the diagram shows this pseudocode in the right panel. The panel's picture shows the box's IN and OUT, built from the diagram's arrows; this file only holds what you need to build each part.
The `<!-- box: id -->` line under a heading names the diagram box it belongs to; the build fails if a box has no section.
Step numbers match the diagram's step squares: 1 to 8 at runtime, T1 to T6 offline.

Tags in comments:

- `BUILT: name (file)` means the code exists on hpc today, as named in `_build/notes/`.
- `NOT BUILT` means the design has it and the code does not.
- `PROPOSED: <decision>` means the line follows a pick that is still open in the Decide register.

# Shared

## Constants

```python
# Built values, with their source.
GATE_STRIDE = {"LIBERO": 10, "RoboDojo": 15}       # BUILT: LiberoTools.gate_stride; RoboDojo run setting
CUSUM_THRESHOLD_ROBODOJO = 0.555                   # BUILT: RoboDojo calibration; LIBERO is re-fit (T6)
MAX_CORRECTION = (0.05, 0.35)                      # metres, radians. BUILT: validate_response (validation.py)
CHUNK_STEP_MAX_ROWS = 15                           # BUILT: chunk_step (libero/session.py)

# Unset counts: named, never guessed. Each is measured before it is used.
N_CANDIDATES = TO_MEASURE                          # candidate chunks per VLA step; today the VLA returns one
MAX_UNSURE_CALLS_PER_SUBTASK = TO_MEASURE          # PROPOSED: How many unsure calls per subtask?
MAX_RECOVERY_TRIES = TO_MEASURE                    # PROPOSED: How many tries before asking a human?
MAX_CODE_ERRORS = TO_MEASURE                       # the code error retry limit (≤N in the diagram)
MIN_REPEAT_EPISODES = TO_MEASURE                   # PROPOSED: What counts as a repeat?
TREE_BRANCHES = TO_MEASURE                         # fixes tried per failure state in tree search
```

## How the boxes connect (one episode)

```python
def run_episode(task, scene_set, seed):
    """One task in one OOD scene: the VLA drives, the advisor helps on demand."""
    task, obs = start_episode(task, scene_set, seed)                         # 1
    subtasks = deque(advisor(Call.PLAN, Context(task, obs)))                  # call 1
    trace, recoveries = [], 0
    while subtasks:
        gate, pending = UncertaintyGate(), []                                 # gate state is per subtask
        while True:
            if pending:
                chunks, pending = pending, []
            else:
                candidates, signal = vla_step(obs, subtasks[0])               # 2
                if not gate.fires(signal):                                    # 3
                    chunks = [pick_chunk(candidates)]                         # 4a
                else:
                    if gate.calls > MAX_UNSURE_CALLS_PER_SUBTASK:
                        return ask_human(trace, "too many unsure calls")      # 8b
                    answer = advisor(Call.UNSURE, Context(obs, candidates, subtasks[0], trace))   # call 2, 4b
                    gate.reset()
                    if answer.kind == "subtask":
                        subtasks[0] = answer.subtask
                        continue
                    chunks = answer.chunks                                    # 4c to 4f
            verdict, obs = run_chunks(chunks, obs, subtasks[0], trace)        # 5, 6, 7
            if verdict is Verdict.TASK_DONE:
                return end_success(trace)                                     # 8a: verified stop
            if verdict is Verdict.SUBTASK_DONE:
                subtasks.popleft()
                break
            if verdict is Verdict.FAILED:
                recoveries += 1
                if recoveries > MAX_RECOVERY_TRIES:
                    return ask_human(trace, "too many failed recoveries")     # 8b
                answer = advisor(Call.FAILED, Context(obs, subtasks[0], trace))   # call 3
                if answer.kind == "subtask":
                    subtasks[0] = answer.subtask
                else:
                    pending = answer.chunks
    return end_success(trace)                                                 # 8a: all subtasks done

def run_chunks(chunks, obs, subtask, trace):
    """Steps 5 to 7 for each chunk until a verdict other than continue; returns (verdict, latest obs)."""
    for chunk in chunks:
        if not safety_check(chunk):                                           # 5
            trace.append(Step(obs, chunk, Verdict.FAILED, refused=True))
            return Verdict.FAILED, obs                                        # refused = failed
        obs = robot_follow(chunk)                                             # 6
        verdict = failure_gate(obs, subtask, is_stop=chunk.is_stop)           # 7
        trace.append(Step(obs, chunk, verdict))                               # T1: every step and verdict saved
        if verdict is not Verdict.CONTINUE:
            return verdict, obs
    return Verdict.CONTINUE, obs
```

# Runtime

## 1 · Task + OOD scene
<!-- box: task -->


```python
def start_episode(task, scene_set, seed):
    """Start one run in a scene the VLA was not trained on."""
    scene = scene_set.sample(seed)          # OOD scene set: NOT BUILT (gap ood-set)
    obs = scene.reset(seed)                 # BUILT: LIBERO resets by seed
    return task, obs
```

## 2 · VLA (π0.5)
<!-- box: vla -->


```python
def vla_step(obs, subtask, noise_policy=None):
    """Sample candidate chunks from the frozen VLA and score its own uncertainty."""
    # PROPOSED: Should the VLA get subtasks? -> send them, in pi0.5's subtask wording
    if noise_policy:                        # after training: steer the frozen VLA through its noise
        noises = noise_policy(obs, subtask, n=N_CANDIDATES)
    else:
        noises = gaussian_noise(n=N_CANDIDATES)
    candidates = [pi05.denoise(obs, subtask, z) for z in noises]   # BUILT: pi05_infer (weights frozen)
    signal = score_denoise_path(candidates)                          # BUILT: score_denoise_path (scoring.py)
    return candidates, signal
```

## 3 · Uncertainty gate
<!-- box: unc -->


```python
class UncertaintyGate:
    """Fires when the VLA is unsure; read as a likely OOD scene."""
    # PROPOSED: What tells the VLA it is unsure? -> A: score on its own denoise path + CUSUM
    # BUILT: CusumGate (cusum.py), EscalationGate.observe (gate.py), threshold from GateCalibration
    # Unsure is not OOD: several valid grasps also raise the score. False-alarm rate: to be measured.
    def fires(self, signal) -> bool:
        self.step += 1
        if self.step % GATE_STRIDE[robot.name]:
            return False                                     # scored every stride steps only
        fired = self.cusum.observe(signal) > self.threshold
        self.calls += fired
        return fired

    def reset(self):
        """After a hand-back. PROPOSED: What happens to the gate after a hand-back? -> reset to zero."""
        self.cusum.reset()                                   # BUILT: CusumGate.reset(), called in gated_infer
        # self.calls is kept on purpose: the cap counts every call in this subtask
```

## 4a · Action chunk (VLA)
<!-- box: vlachunk -->


```python
def pick_chunk(candidates, scorer=None):
    """The reranking scorer picks one candidate; random until it is trained."""
    if scorer is None:                      # today: one chunk only (BUILT: runs the only chunk)
        return random.choice(candidates)
    return max(candidates, key=scorer)      # NOT BUILT: trained offline (T5)
```

## 4b · Advisor
<!-- box: adv -->


```python
def advisor(call, context, skills=skill_library):
    """Answer one call; the VLA stays the main policy."""
    robot.pause()                                            # the robot holds while the advisor is asked
    if call is Call.PLAN:
        return claude.plan(context.task, context.images)     # NOT BUILT: call 1
    skill = skills.match(context.subtask, context.images)    # 4c: a checked skill is tried first
    answer = claude.answer(call, context, skill)             # BUILT: ClaudePolicy (skill/claude_policy.py)
    validate_response(answer)                                # BUILT: validation.py
    match answer.kind:
        case "subtask":
            return answer                                    # reworded or replanned subtask
        case "code":
            answer.chunks = code_runner(answer.code or skill, context)   # 4e
        case "stop":
            answer.chunks = [hold_chunk(context.obs, is_stop=True)]       # 4f; the verifier must confirm it
        case "edit" | "eef":                                 # nudge: ablation only
            answer.chunks = [bounded(answer.correction, MAX_CORRECTION)]  # BUILT: edited_targets
        case _:
            raise ValueError(f"unknown answer kind: {answer.kind}")
    return answer
```

## 4c · Skill library
<!-- box: skills -->


```python
class SkillLibrary:
    """Checked code + VLA skills, tried before new code."""   # NOT BUILT
    def match(self, subtask, images):
        fits = [s for s in self.skills if s.tag == "POS" and s.applies(subtask, images)]
        return max(fits, key=lambda s: s.success_rate, default=None)

    def admit(self, skill):
        """Only called by checks() after a held-out dry run (decided)."""
        self.skills.append(skill)
```

## 4d · Vision tools
<!-- box: vision -->


```python
def perceive(images, object_name):
    """Find the object, its centre and its best grasp."""
    mask = sam3_1.track(images, object_name)                 # mask + frame-to-frame tracking. Tracking: NOT BUILT
    points = depth_anything_3(images) & mask                 # object points; the centre is the hover target
    grasps = grasp_model(points)                             # PROPOSED: Which grasp model? -> Contact-GraspNet, top-down first
                                                             # BUILT: cgn_server; HarnessPerception.find/locate/holding/grasps
    return Target(mask, points.centre(), best(grasps, prefer="top_down"))   # top-down lifted 4 of 4 on LIBERO
```

## 4e · Code runner
<!-- box: runner -->


```python
def code_runner(program, context):
    """Code stages the arm at a pose the VLA knows; the VLA then does the contact."""
    for attempt in range(MAX_CODE_ERRORS):
        try:
            target = perceive(context.images, program.object_name)            # 4d
            pose = pre_grasp_pose(program.task, target)       # PROPOSED: Where does the hover stop? -> the demos' pre-grasp pose
            motion = bounded_steps(context.obs.eef, pose)     # PROPOSED: May code moves use a motion planner? -> bounded steps only
                                                              # BUILT: move_to_hover (hover.py)
            vla.clear_queue()                                 # the VLA resumes with its queued chunk cleared
            return to_chunks(motion)                          # 4f
        except CodeError as error:                            # a code error, not a physical failure
            context.trace.append(error)
            program = claude.fix(program, error, context.trace)
    raise AskHuman(context.trace)                             # 8b
    # Risk, the core bet: a familiar arm pose may not be enough when new objects stay in view (experiment A).
```

## 4f · Final action chunks
<!-- box: codechunks -->


```python
def to_chunks(motion):
    """Cut a motion into chunks the robot follows like the VLA's own."""
    rows = motion.as_action_rows()                            # the VLA's action format
    return [Chunk(rows[i:i + CHUNK_STEP_MAX_ROWS]) for i in range(0, len(rows), CHUNK_STEP_MAX_ROWS)]

def hold_chunk(obs, is_stop):
    """A stop: hold the arm; the failure gate's verifier decides if the task is done."""
    return Chunk([obs.current_pose], is_stop=is_stop)
```

## 5 · Safety limits
<!-- box: safety -->


```python
def safety_check(chunk) -> bool:
    """Hard limits on every chunk before the robot moves."""   # NOT BUILT: no single limit layer today
    return (max_step(chunk) <= step_limit
            and inside(chunk, workspace)
            and predicted_contact(chunk) <= contact_limit)    # limits from the robot's spec, not tuned
```

## 6 · Robot moves
<!-- box: robot -->


```python
def robot_follow(chunk):
    """The low-level controller follows the chunk; it holds while the advisor is asked."""
    for row in chunk.rows:
        env.step(row)                                         # BUILT: chunk_step, execute_joint_actions
    return env.observe()
```

## 7 · Failure detection gate
<!-- box: fail -->


```python
def failure_gate(obs, subtask, is_stop=False) -> Verdict:
    """The VLA's self-check plus an independent verifier."""
    # PROPOSED: What does the verifier look at? -> images + robot state + force
    if is_stop:                                               # the advisor said the task is done
        return Verdict.TASK_DONE if verifier.task_done(obs) else Verdict.FAILED
    if not vla.self_check(obs) or not verifier.check(obs.images, obs.state, obs.force):
        return Verdict.FAILED                                 # verifier: NOT BUILT
    return Verdict.SUBTASK_DONE if verifier.subtask_done(obs, subtask) else Verdict.CONTINUE
```

## 8a · End: task succeeded
<!-- box: endok -->


```python
def end_success(trace):
    """Close the run as a verified success."""
    return Outcome.SUCCESS, trace
```

## 8b · End: ask a human for help
<!-- box: endhuman -->


```python
def ask_human(trace, reason):
    """Stop and ask a person; the failed run still feeds offline training."""
    # PROPOSED: How many tries before asking a human? -> few (MAX_RECOVERY_TRIES, to be measured)
    notify_person(reason, trace)                              # NOT BUILT
    return Outcome.ASKED_HUMAN, trace
```

# Offline

## How the offline boxes connect (one round)

```python
# PROPOSED: Where does offline training run first? -> LIBERO with OOD splits (free resets).
def offline_round(saved_runs, vla, skills):
    """Between runs: turn saved runs into more data, then train small parts of the frozen VLA."""
    roots = failure_states(saved_runs)                        # T1
    fixes = tree_search(roots)                                # T2
    candidates = fixes + push_off_and_recover(fixes)          # T3
    approved = [c for c in candidates if should_train(c)]     # T4
    trained = learn(vla, approved)                            # T5
    checks(vla, trained, skills)                              # T6, then redeploy
```

## T1 · Saved runs
<!-- box: buf -->


```python
def failure_states(saved_runs):
    """Sort what was saved and pick the tree roots."""
    buffers = sort_by_kind(saved_runs)    # fixes, advisor picks, verdicts, VLA-alone successes. NOT BUILT (today: one log)
    return [step.state for step in buffers.all_steps if step.gate_fired]
```

## Sim reset
<!-- box: reset -->


```python
def sim_reset(state):
    """Put the sim back into a saved moment; this is why T2 and T3 are sim-only."""
    sim.set_state(state.physics, state.objects, state.robot)  # NOT BUILT: LIBERO resets by seed only today
```

## T2 · Tree search
<!-- box: expand -->


```python
def tree_search(roots):
    """Several fixes per failure; keep only those the verifier accepts."""
    # PROPOSED: How do we get many fixes per failure? -> tree search from where the gate fired
    # PROPOSED: Who labels the fix? -> the code agent (code + VLA)
    fixes = []
    for state in roots:
        for branch in range(TREE_BRANCHES):
            sim_reset(state)
            fix = code_agent.fix(state)
            if verifier.accepts(rollout(fix)):
                fixes.append(fix)
    return fixes
```

## T3 · Push off + recover
<!-- box: multiply -->


```python
def push_off_and_recover(fixes):
    """Push the arm off a verified path and label the way back."""
    # PROPOSED: How are recoveries labelled? -> ask the code agent again from the pushed-off state
    recoveries = []
    for fix in fixes:
        sim_reset(fix.state)
        pushed = push_off(fix.path)                           # physics renders the images: no world model in sim
        recovery = code_agent.recover(pushed)
        if verifier.accepts(rollout(recovery)):
            recoveries.append(recovery)
    return recoveries
```

## T4 · Advisor: train on this?
<!-- box: trigger -->


```python
def should_train(candidate) -> bool:
    """Nothing trains on its own; the advisor starts training."""
    # PROPOSED: What makes the advisor start training? -> verified and repeats across trials
    # PROPOSED: What counts as a repeat? -> only distinct runtime episodes vote; search copies add data
    return candidate.verified and candidate.distinct_runtime_episodes >= MIN_REPEAT_EPISODES
```

## T5 · Learn, VLA frozen
<!-- box: learn -->


```python
def learn(vla, approved):
    """Fixes become labels; small parts learn while the VLA stays frozen."""
    labels, skill_candidates = [], []
    for fix in approved:
        noise, error = vla.invert(fix.actions)               # PROPOSED: How does a fix become a label? -> run the VLA backwards
        if error.small:                                       # the reconstruction error is the router
            labels.append((fix.obs, fix.subtask, noise))
        else:
            skill_candidates.append(fix)                      # the VLA cannot make it: keep as a skill
    noise_policy, scorer = train(labels)                      # PROPOSED: What learns first? -> noise policy + reranking scorer
    # VLA weights stay frozen; LoRA only after the frozen path stalls and checks pass (decided)
    return Trained(noise_policy, scorer, skill_candidates)
```

## T6 · Check + re-tune
<!-- box: checks -->


```python
def checks(vla, trained, skills):
    """Gate everything that goes back to runtime."""
    for skill in trained.skill_candidates:                    # decided: a new skill must pass the checks
        if dry_run(skill, held_out_scenes):
            skills.admit(skill)
    if held_out_success(vla, trained) < held_out_success(vla):
        return rollback(trained)                              # held-out tasks must not drop
    report(ood_split_success(vla, trained))                   # ranked: VLA-alone OOD success first, advisor calls second
    refit_gate_calibration(vla, trained)                      # PROPOSED: How is the gate re-tuned after training? -> re-fit
                                                              # BUILT: fit_calibration.py (fit once today)
    redeploy(vla, trained)
```

# Arrows

Each `## ` section below is one arrow: it only says what passes between two boxes (the message, its fields, when, who builds it, who reads it); each box's own logic stays in its box section.
Shapes come from `_build/notes/`: an action chunk is 50 rows × action_dim (7 on LIBERO, 14 on RoboDojo); the denoise path is 11 steps × 50 × 32 before it is cut to action_dim.

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
    """Task + OOD scene to VLA (π0.5)."""
    task: str                       # text: the instruction
    images: Any                     # camera frames: the first view of the OOD scene

# when: once, at the start of a run
message = TaskStart(task=…, images=…)
# built by: Task + OOD scene (start_episode)
vla_step(message)
# read by: VLA (π0.5)
```

## e_plan_ask · ① ask for a plan
<!-- box: e_plan_ask -->

- **When:** once, before the VLA's first step.

| Field | Type / shape | Meaning |
|---|---|---|
| task | text | the instruction |
| images | camera frames | the first view |

```python
@dataclass
class PlanRequest:
    """VLA (π0.5) to Advisor."""
    task: str                       # text: the instruction
    images: Any                     # camera frames: the first view

# when: once, before the VLA's first step
message = PlanRequest(task=…, images=…)
# built by: VLA (π0.5) (vla_step)
advisor(Call.PLAN, message)
# read by: Advisor
```

## e_plan_back · subtasks
<!-- box: e_plan_back -->

- **When:** once per run, and again when a call answers with a reworded subtask.

| Field | Type / shape | Meaning |
|---|---|---|
| subtasks | list of text | in pi0.5's subtask wording (PROPOSED: send subtasks) |

```python
@dataclass
class Plan:
    """Advisor to VLA (π0.5)."""
    subtasks: Any                   # list of text: in pi0.5's subtask wording (PROPOSED: send subtasks)

# when: once per run, and again when a call answers with a reworded subtask
message = Plan(subtasks=…)
# built by: Advisor (advisor)
vla_step(message)
# read by: VLA (π0.5)
```

## e_chunk_gate · candidate chunks + signal
<!-- box: e_chunk_gate -->

- **When:** every VLA step; the gate scores every stride steps.

| Field | Type / shape | Meaning |
|---|---|---|
| candidates | N × 50 × action size | N candidate chunks (today N = 1) |
| denoise path | 11 × 50 × 32 | the flow steps the score reads |
| signal | float | the VLA's doubt score (built) |

```python
@dataclass
class CandidatesWithSignal:
    """VLA (π0.5) to Uncertainty gate."""
    candidates: Any                 # N × 50 × action_dim: N_CANDIDATES chunks (today N = 1)
    denoise_path: Any               # 11 × 50 × 32: the flow steps the score reads
    signal: float                   # float: score_denoise_path (BUILT)

# when: every VLA step; the gate scores every stride steps
message = CandidatesWithSignal(candidates=…, denoise_path=…, signal=…)
# built by: VLA (π0.5) (vla_step)
UncertaintyGate.fires(message)
# read by: Uncertainty gate
```

## e_no · no: the scorer picks one
<!-- box: e_no -->

- **When:** every step the gate does not fire.

| Field | Type / shape | Meaning |
|---|---|---|
| candidates | N × 50 × action size | all candidate chunks |

```python
@dataclass
class CandidatesToPick:
    """Uncertainty gate to Action chunk (VLA)."""
    candidates: Any                 # N × 50 × action_dim: all candidate chunks

# when: every step the gate does not fire
message = CandidatesToPick(candidates=…)
# built by: Uncertainty gate (UncertaintyGate.fires)
pick_chunk(message)
# read by: Action chunk (VLA)
```

## e_ask · ② unsure: likely OOD
<!-- box: e_ask -->

- **When:** the gate fires; the robot pauses; at most the per-subtask cap of calls.

| Field | Type / shape | Meaning |
|---|---|---|
| images | camera frames | fresh views |
| chunk | 50 × action size | the unsure candidate |
| subtask | text | the current subtask |
| trace | list of steps | what happened so far |

```python
@dataclass
class UnsureCall:
    """Uncertainty gate to Advisor."""
    images: Any                     # camera frames: fresh views
    chunk: Any                      # 50 × action_dim: the unsure candidate
    subtask: str                    # text: the current subtask
    trace: Any                      # list of steps: what happened so far

# when: the gate fires; the robot pauses; at most the per-subtask cap of calls
message = UnsureCall(images=…, chunk=…, subtask=…, trace=…)
# built by: Uncertainty gate (UncertaintyGate.fires)
advisor(Call.UNSURE, message)
# read by: Advisor
```

## e_vla_chunk · action chunk
<!-- box: e_vla_chunk -->

- **When:** every step the VLA acts alone.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | 50 × action size | the picked chunk; its first rows run |

```python
@dataclass
class VLAChunk:
    """Action chunk (VLA) to Safety limits."""
    chunk: Any                      # 50 × action_dim: the picked chunk; its first rows run

# when: every step the VLA acts alone
message = VLAChunk(chunk=…)
# built by: Action chunk (VLA) (pick_chunk)
safety_check(message)
# read by: Safety limits
```

## e_saved · skills, tried first
<!-- box: e_saved -->

- **When:** every call 2 or 3, before the advisor writes new code.

| Field | Type / shape | Meaning |
|---|---|---|
| skill | code + tag | best POS match for the subtask and scene, or none |

```python
@dataclass
class SkillMatch:
    """Skill library to Advisor."""
    skill: Any                      # code + tag: best POS match for the subtask and scene, or none

# when: every call 2 or 3, before the advisor writes new code
message = SkillMatch(skill=…)
# built by: Skill library (SkillLibrary.match)
advisor(call, context, skills=message)
# read by: Advisor
```

## e_code · code to help the VLA
<!-- box: e_code -->

- **When:** the answer is code + VLA.

| Field | Type / shape | Meaning |
|---|---|---|
| program | code | a checked skill or new code |
| object name | text | what perceive should find |

```python
@dataclass
class CodeAnswer:
    """Advisor to Code runner."""
    program: Any                    # code: a checked skill or new code
    object_name: str                # text: what perceive should find

# when: the answer is code + VLA
message = CodeAnswer(program=…, object_name=…)
# built by: Advisor (advisor)
code_runner(message)
# read by: Code runner
```

## e_objname · object name
<!-- box: e_objname -->

- **When:** each time the code perceives.

| Field | Type / shape | Meaning |
|---|---|---|
| object name | text | the object to find |
| images | camera frames | the current views |

```python
@dataclass
class PerceiveRequest:
    """Code runner to Vision tools."""
    object_name: str                # text: the object to find
    images: Any                     # camera frames: the current views

# when: each time the code perceives
message = PerceiveRequest(object_name=…, images=…)
# built by: Code runner (code_runner)
perceive(message)
# read by: Vision tools
```

## e_mask · mask · depth · grasps
<!-- box: e_mask -->

- **When:** the answer to each perceive call.

| Field | Type / shape | Meaning |
|---|---|---|
| mask | H × W bool | the object, tracked frame to frame |
| points | M × 3 | object points from depth ∩ mask |
| centre | xyz | the hover target |
| grasp | pose (xyz + axis) | best grasp, top-down first |

```python
@dataclass
class PerceiveResult:
    """Vision tools to Code runner."""
    mask: Any                       # H × W bool: the object, tracked frame to frame
    points: Any                     # M × 3: object points from depth ∩ mask
    centre: Any                     # xyz: the hover target
    grasp: Any                      # pose (xyz + axis): best grasp, top-down first

# when: the answer to each perceive call
message = PerceiveResult(mask=…, points=…, centre=…, grasp=…)
# built by: Vision tools (perceive)
code_runner(message)
# read by: Code runner
```

## e_fixable · code error: retry
<!-- box: e_fixable -->

- **When:** the code raises an error; at most the cap of code errors.

| Field | Type / shape | Meaning |
|---|---|---|
| error | text | the exception, not a physical failure |
| trace | list of steps | what the code did |

```python
@dataclass
class CodeError:
    """Code runner to Advisor."""
    error: str                      # text: the exception, not a physical failure
    trace: Any                      # list of steps: what the code did

# when: the code raises an error; at most the cap of code errors
message = CodeError(error=…, trace=…)
# built by: Code runner (code_runner)
advisor(message)
# read by: Advisor
```

## e_split · motion split into chunks
<!-- box: e_split -->

- **When:** the code has a motion to a known pose.

| Field | Type / shape | Meaning |
|---|---|---|
| motion | waypoints | bounded steps to the pre-grasp pose |

```python
@dataclass
class StagingMotion:
    """Code runner to Final action chunks."""
    motion: Any                     # waypoints: bounded steps to the pre-grasp pose

# when: the code has a motion to a known pose
message = StagingMotion(motion=…)
# built by: Code runner (code_runner)
to_chunks(message)
# read by: Final action chunks
```

## e_codechunk · known pose
<!-- box: e_codechunk -->

- **When:** after the code (or a stop or a nudge) produced chunks.

| Field | Type / shape | Meaning |
|---|---|---|
| chunks | K × (≤15 × action size) | cut to the 15-row chunk limit rows |
| last pose | pose | where the VLA takes over (◎) |
| is stop | bool | true for a stop's hold chunk |

```python
@dataclass
class CodeChunks:
    """Final action chunks to Safety limits."""
    chunks: Any                     # K × (≤15 × action_dim): cut to CHUNK_STEP_MAX_ROWS rows
    last_pose: Any                  # pose: where the VLA takes over (◎)
    is_stop: bool                   # bool: true for a stop's hold chunk

# when: after the code (or a stop or a nudge) produced chunks
message = CodeChunks(chunks=…, last_pose=…, is_stop=…)
# built by: Final action chunks (to_chunks)
safety_check(message)
# read by: Safety limits
```

## e_nudge · ■ stop, or ↔ nudge (edit/eef, ablation)
<!-- box: e_nudge -->

- **When:** the answer is a stop or an edit / eef nudge.

| Field | Type / shape | Meaning |
|---|---|---|
| stop | hold chunk | the verifier must confirm the task is done |
| correction | ≤ 5 cm, ≤ 0.35 rad | the nudge, bounded by the response check |

```python
@dataclass
class StopOrNudge:
    """Advisor to Final action chunks."""
    stop: Any                       # hold chunk: the verifier must confirm the task is done
    correction: Any                 # ≤ 5 cm, ≤ 0.35 rad: the nudge, bounded by validate_response

# when: the answer is a stop or an edit / eef nudge
message = StopOrNudge(stop=…, correction=…)
# built by: Advisor (advisor)
to_chunks(message)
# read by: Final action chunks
```

## e_safe_robot · within limits
<!-- box: e_safe_robot -->

- **When:** every chunk that passes the hard limits.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | rows × action size | the checked chunk |

```python
@dataclass
class CheckedChunk:
    """Safety limits to Robot moves."""
    chunk: Any                      # rows × action_dim: the checked chunk

# when: every chunk that passes the hard limits
message = CheckedChunk(chunk=…)
# built by: Safety limits (safety_check)
robot_follow(message)
# read by: Robot moves
```

## e_refuse · refused = failed
<!-- box: e_refuse -->

- **When:** a chunk breaks a hard limit; the robot never moves.

| Field | Type / shape | Meaning |
|---|---|---|
| chunk | rows × action size | the refused chunk, saved in the trace |
| verdict | FAILED | counts as a failure |

```python
@dataclass
class RefusedChunk:
    """Safety limits to Failure detection gate."""
    chunk: Any                      # rows × action_dim: the refused chunk, saved in the trace
    verdict: Any                    # FAILED: counts as a failure

# when: a chunk breaks a hard limit; the robot never moves
message = RefusedChunk(chunk=…, verdict=…)
# built by: Safety limits (safety_check)
failure_gate(message)
# read by: Failure detection gate
```

## e_obs · new observation
<!-- box: e_obs -->

- **When:** after every chunk.

| Field | Type / shape | Meaning |
|---|---|---|
| images | camera frames | the new views |
| state | robot state | joints, end effector, gripper |
| force | contact readings | for the verifier (PROPOSED) |

```python
@dataclass
class Observation:
    """Robot moves to Failure detection gate."""
    images: Any                     # camera frames: the new views
    state: Any                      # robot state: joints, end effector, gripper
    force: Any                      # contact readings: for the verifier (PROPOSED)

# when: after every chunk
message = Observation(images=…, state=…, force=…)
# built by: Robot moves (robot_follow)
failure_gate(message)
# read by: Failure detection gate
```

## e_next · no: next chunk, resume after code; done: next subtask
<!-- box: e_next -->

- **When:** the verdict is continue or subtask done.

| Field | Type / shape | Meaning |
|---|---|---|
| verdict | continue, or subtask done | what the gate decided |
| obs | images + state | the VLA's next input |

```python
@dataclass
class Continue:
    """Failure detection gate to VLA (π0.5)."""
    verdict: Any                    # CONTINUE or SUBTASK_DONE: what the gate decided
    obs: Any                        # images + state: the VLA's next input

# when: the verdict is continue or subtask done
message = Continue(verdict=…, obs=…)
# built by: Failure detection gate (failure_gate)
vla_step(message.obs, subtask)
# read by: VLA (π0.5)
```

## e_failed · ③ failed: ask how to recover
<!-- box: e_failed -->

- **When:** the verdict is failed; at most the per-run cap of recoveries.

| Field | Type / shape | Meaning |
|---|---|---|
| images | camera frames | fresh views |
| subtask | text | the current subtask |
| trace | list of steps | including the failed step |

```python
@dataclass
class RecoverCall:
    """Failure detection gate to Advisor."""
    images: Any                     # camera frames: fresh views
    subtask: str                    # text: the current subtask
    trace: Any                      # list of steps: including the failed step

# when: the verdict is failed; at most the per-run cap of recoveries
message = RecoverCall(images=…, subtask=…, trace=…)
# built by: Failure detection gate (failure_gate)
advisor(Call.FAILED, message)
# read by: Advisor
```

## e_done · all subtasks done, or stop verified
<!-- box: e_done -->

- **When:** the last subtask is done, or a stop is confirmed.

| Field | Type / shape | Meaning |
|---|---|---|
| verdict | task done, or the last subtask done | verified by the verifier |
| trace | list of steps | the whole run |

```python
@dataclass
class Success:
    """Failure detection gate to End: task succeeded."""
    verdict: Any                    # TASK_DONE or last SUBTASK_DONE: verified by the verifier
    trace: Any                      # list of steps: the whole run

# when: the last subtask is done, or a stop is confirmed
message = Success(verdict=…, trace=…)
# built by: Failure detection gate (failure_gate)
end_success(message)
# read by: End: task succeeded
```

## e_human · too many tries
<!-- box: e_human -->

- **When:** too many failed tries, unsure calls in one subtask, or code errors.

| Field | Type / shape | Meaning |
|---|---|---|
| reason | text | which limit was hit |
| images | camera frames | the last views |
| trace | list of steps | what was tried |

```python
@dataclass
class HumanHandoff:
    """Advisor to End: ask a human for help."""
    reason: str                     # text: which limit was hit
    images: Any                     # camera frames: the last views
    trace: Any                      # list of steps: what was tried

# when: too many failed tries, unsure calls in one subtask, or code errors
message = HumanHandoff(reason=…, images=…, trace=…)
# built by: Advisor (advisor)
ask_human(message)
# read by: End: ask a human for help
```

## e_save · every step and verdict saved
<!-- box: e_save -->

- **When:** after every chunk, from runtime into offline storage.

| Field | Type / shape | Meaning |
|---|---|---|
| step | obs + chunk | what was seen and done |
| verdict | continue, subtask done, task done, or failed | the failure gate's call |
| source | VLA alone or advised | who produced the chunk |
| gate fired | bool | marks the tree roots |

```python
@dataclass
class SavedStep:
    """Failure detection gate to Saved runs."""
    step: Any                       # obs + chunk: what was seen and done
    verdict: Any                    # CONTINUE, SUBTASK_DONE, TASK_DONE, FAILED: the failure gate's call
    source: Any                     # VLA alone or advised: who produced the chunk
    gate_fired: bool                # bool: marks the tree roots

# when: after every chunk, from runtime into offline storage
message = SavedStep(step=…, verdict=…, source=…, gate_fired=…)
# built by: Failure detection gate (failure_gate)
failure_states(message)
# read by: Saved runs
```

## e_buf_exp · failure states
<!-- box: e_buf_exp -->

- **When:** each offline round.

| Field | Type / shape | Meaning |
|---|---|---|
| states | saved sim states | where the gate fired |

```python
@dataclass
class TreeRoots:
    """Saved runs to Tree search."""
    states: Any                     # saved sim states: where the gate fired

# when: each offline round
message = TreeRoots(states=…)
# built by: Saved runs (failure_states)
tree_search(message)
# read by: Tree search
```

## e_reset_exp · same state
<!-- box: e_reset_exp -->

- **When:** before every tree-search branch.

| Field | Type / shape | Meaning |
|---|---|---|
| state | physics + objects + robot | one saved moment |

```python
@dataclass
class ResetToState:
    """Sim reset to Tree search."""
    state: Any                      # physics + objects + robot: one saved moment

# when: before every tree-search branch
message = ResetToState(state=…)
# built by: Sim reset (sim_reset)
tree_search(message)
# read by: Tree search
```

## e_exp_mul · verified paths
<!-- box: e_exp_mul -->

- **When:** after tree search.

| Field | Type / shape | Meaning |
|---|---|---|
| fixes | code + VLA paths | only those the verifier accepted |

```python
@dataclass
class VerifiedFixes:
    """Tree search to Push off + recover."""
    fixes: Any                      # code + VLA paths: only those the verifier accepted

# when: after tree search
message = VerifiedFixes(fixes=…)
# built by: Tree search (tree_search)
push_off_and_recover(message)
# read by: Push off + recover
```

## e_reset_mul · same path
<!-- box: e_reset_mul -->

- **When:** before every push-off.

| Field | Type / shape | Meaning |
|---|---|---|
| state | a state on the verified path | where the push starts |

```python
@dataclass
class ResetToPath:
    """Sim reset to Push off + recover."""
    state: Any                      # a state on the verified path: where the push starts

# when: before every push-off
message = ResetToPath(state=…)
# built by: Sim reset (sim_reset)
push_off_and_recover(message)
# read by: Push off + recover
```

## e_mul_trig · all candidates
<!-- box: e_mul_trig -->

- **When:** each offline round.

| Field | Type / shape | Meaning |
|---|---|---|
| candidates | fixes + recoveries | each with verified and its runtime episode ids |

```python
@dataclass
class TrainCandidates:
    """Push off + recover to Advisor: train on this?."""
    candidates: Any                 # fixes + recoveries: each with verified and its runtime episode ids

# when: each offline round
message = TrainCandidates(candidates=…)
# built by: Push off + recover (push_off_and_recover)
should_train(message)
# read by: Advisor: train on this?
```

## e_trig_learn · yes: train
<!-- box: e_trig_learn -->

- **When:** a candidate is verified and seen in enough separate runtime episodes.

| Field | Type / shape | Meaning |
|---|---|---|
| approved | fixes | verified, repeating (PROPOSED: distinct episodes) |

```python
@dataclass
class ApprovedFixes:
    """Advisor: train on this? to Learn, VLA frozen."""
    approved: Any                   # fixes: verified, repeating (PROPOSED: distinct episodes)

# when: a candidate is verified and seen in enough separate runtime episodes
message = ApprovedFixes(approved=…)
# built by: Advisor: train on this? (should_train)
learn(message)
# read by: Learn, VLA frozen
```

## e_learn_chk · trained parts
<!-- box: e_learn_chk -->

- **When:** after training.

| Field | Type / shape | Meaning |
|---|---|---|
| noise policy | small network | picks the VLA's noise |
| scorer | small network | reranks candidates |
| skill candidates | fixes | the VLA cannot make these |

```python
@dataclass
class TrainedParts:
    """Learn, VLA frozen to Check + re-tune."""
    noise_policy: Any               # small network: picks the VLA's noise
    scorer: Any                     # small network: reranks candidates
    skill_candidates: Any           # fixes: the VLA cannot make these

# when: after training
message = TrainedParts(noise_policy=…, scorer=…, skill_candidates=…)
# built by: Learn, VLA frozen (learn)
checks(message)
# read by: Check + re-tune
```

## e_admit · admit as a skill
<!-- box: e_admit -->

- **When:** a skill candidate passes the held-out dry run (decided).

| Field | Type / shape | Meaning |
|---|---|---|
| skill | code + tag POS | checked code + VLA skill |

```python
@dataclass
class AdmittedSkill:
    """Check + re-tune to Skill library."""
    skill: Any                      # code + tag POS: checked code + VLA skill

# when: a skill candidate passes the held-out dry run (decided)
message = AdmittedSkill(skill=…)
# built by: Check + re-tune (checks)
SkillLibrary.admit(message)
# read by: Skill library
```

## e_redeploy · redeploy the better VLA
<!-- box: e_redeploy -->

- **When:** the held-out check does not drop.

| Field | Type / shape | Meaning |
|---|---|---|
| noise policy + scorer | small networks | plug into the frozen VLA |
| calibration | gate threshold + scale | re-fit on the new VLA's runs |

```python
@dataclass
class Redeploy:
    """Check + re-tune to VLA (π0.5)."""
    noise_policy_and_scorer: Any    # small networks: plug into the frozen VLA
    calibration: Any                # gate threshold + scale: re-fit on the new VLA's runs

# when: the held-out check does not drop
message = Redeploy(noise_policy_and_scorer=…, calibration=…)
# built by: Check + re-tune (checks)
vla_step(obs, subtask, message.noise_policy_and_scorer)
# read by: VLA (π0.5)
```

## bp_e_promote1 · repeats, the VLA can make it
<!-- box: bp_e_promote1 -->

- **When:** a repeating fix inverts with a small error (T5).

| Field | Type / shape | Meaning |
|---|---|---|
| labels | (obs, subtask, noise) | train the noise policy + scorer |

```python
@dataclass
class NoiseLabels:
    """Skill library to Noise policy + scorer."""
    labels: Any                     # (obs, subtask, noise): train the noise policy + scorer

# when: a repeating fix inverts with a small error (T5)
message = NoiseLabels(labels=…)
# built by: Skill library (SkillLibrary)
train(message)
# read by: Noise policy + scorer (train (noise policy + scorer))
```

## bp_e_promote2 · repeats, the VLA cannot make it
<!-- box: bp_e_promote2 -->

- **When:** the frozen path stalls and the checks pass (decided: LoRA only as fallback).

| Field | Type / shape | Meaning |
|---|---|---|
| fixes | actions | the behaviour the VLA cannot produce |

```python
@dataclass
class LoraFixes:
    """Skill library to LoRA."""
    fixes: Any                      # actions: the behaviour the VLA cannot produce

# when: the frozen path stalls and the checks pass (decided: LoRA only as fallback)
message = LoraFixes(fixes=…)
# built by: Skill library (SkillLibrary)
train_lora(message)
# read by: LoRA
```

# Integration tests

Unit tests check one box on its own; an integration test runs real neighbouring boxes together and checks the messages on the arrows between them.
Each row names the boxes it crosses (diagram ids), so a box's panel lists every integration test that runs through it.
Status is what the notes in `_build/notes/` show; nothing here has been run for this guide.

| Test | Boxes | Proves | Status |
|---|---|---|---|
| IT1 VLA to gate | vla, unc | the gate scores real π0.5 denoise paths; the scan sampler matches the original bit for bit | partial: tests/integration/test_sampler_parity.py exists (needs ≥14 GB GPU); not run here |
| IT2 gate to advisor and back | unc, adv, vla | a fired gate pauses the robot, calls the advisor, and the hand-back resets the gate | partial: test_routing uses fakes; one RoboDojo smoke run (claude_smoke_004) |
| IT3 code assists the VLA | adv, skills, runner, vision, codechunks, safety, robot | code stages the arm at the pre-grasp pose and the VLA then grasps (experiment A) | not built: hover_run.py never run |
| IT4 failure and recovery | robot, fail, adv | a failed verdict reaches call 3 and the recovery chunks run | not built: no verifier, no call 3 |
| IT5 one full LIBERO episode | task, vla, unc, vlachunk, adv, safety, robot, fail, endok, endhuman | a run ends as a verified success or a hand-off, with every step saved | not built: no one-shot LIBERO launcher |
| IT6 runtime to offline data | fail, buf, reset, expand, multiply | saved gate-fire states reload in sim and tree search finds verified fixes | not built: no mid-episode sim reset |
| IT7 one offline round | buf, trigger, learn, checks, vla | trained parts pass held-out checks and redeploy with a re-fit gate | not built |
| IT8 skill admission | checks, skills, adv | a dry-run-checked skill is admitted and tried first at runtime | not built: no skill library |

# Proposed picks for the open decisions

| Decision | Pick | Why |
|---|---|---|
| What tells the VLA it is unsure? | A: score on its own denoise path + CUSUM | Built; option B stays available as the re-tune option. |
| How many unsure calls per subtask? | A cap per subtask, then ask a human | Stops the loop where code stages the arm and the VLA is still unsure. |
| What happens to the gate after a hand-back? | Reset it to zero | Built (`CusumGate.reset`); the per-subtask cap covers repeat asks. |
| May code moves use a motion planner? | Bounded steps only | Keeps results comparable with the planner ban; `move_to_hover` exists. |
| Where does the hover stop? | The demos' pre-grasp pose | The hand-back must land inside the VLA's training data, which is the whole point of the hand-back. |
| Which grasp model? | Contact-GraspNet, preferring top-down grasps | Built; top-down lifted 4 of 4; the grasp-model comparison gap stays open. |
| How many tries before asking a human? | Few (count to be measured) | Each failed try risks the robot, and failures still feed offline training. |
| Should the VLA get subtasks? | Send subtasks | π0.5 is trained with subtask-level language. |
| What does the verifier look at? | Images + robot state + force | Harder to fool than images alone. |
| Where does offline training run first? | LIBERO, with OOD splits | Free resets and ready OOD splits. |
| Who labels the fix? | Code agent (code + VLA) | Can fix what the VLA cannot reach; best-of-N picks also feed the scorer. |
| How do we get many fixes per failure? | Tree search from where the gate fired | Labels only help on states the VLA visits. |
| How are recoveries labelled? | Ask the code agent again from the pushed-off state | In sim, physics renders the images, so only the label matters. |
| What makes the advisor start training? | Verified and repeats across trials | Repeating failures are worth teaching; one-offs stay as runtime skills. |
| How does a fix become a label? | Run the VLA backwards to its noise | The reconstruction error doubles as the router. |
| What learns first? | Noise policy + reranking scorer | Cheapest safe step; the base VLA stays untouched. |
| What counts as a repeat? | Distinct runtime episodes only | Search copies add data, not votes. |
| How is the gate re-tuned after training? | Re-fit on new successful runs | The noise policy changes what the gate reads. |
