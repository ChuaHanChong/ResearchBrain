# Research Direction Update - Long-Horizon Memory and Failure Recovery (2026-09-01)

Ongoing update. Three slides, plus three backup.

**Direction**: on a non-Markovian long-horizon task the robot must remember what it already did, and when it errs it must fix that error and carry on from there.

## Slide 1 - Why a mid-episode anchor

Header: On a non-Markovian task, the observation that decides a later action can occur anywhere. A fixed-index rule cannot find it.

```
  ONE EPISODE, NON-MARKOVIAN TASK

  step 0 --------------------------------- k -------------------- T
                                           |
                                           o_k : transient or occluded,
                                                 absent from o_T, yet a
                                                 later action depends on it

  WHAT TO KEEP
     keep all        full-history WAMs are feasible, and do not win
     keep by index   MemoryWAM
     keep by use     what the task needs

                            anchor                     recent
                            |--|                       |--------|
  MemoryWAM  by index       F  F  g  g  g  g  g  g  g  F  F  F  F
                                           ^ reduced to gist tokens by a
                                             rule that never reads content

  needed     by action      g  g  g  g  g  F  g  g  g  F  F  F  F
                                           ^ kept whole, wherever it falls

     human memory encodes by goal relevance, not by position in time

  SECOND FAILURE : stored, but no longer readable

     example: context length 6 frames, episode 125 frames

     BEFORE   position = when the frame happened
                                                |----- window -----|
        f3 .....................................|  f120 .... f125  |
        |--------------- gap 122 ---------------|                  |
        ^ distance never trained. attention cannot reliably retrieve it

     AFTER    position = slot counted back from now
                                                |----- window -----|
        f3 becomes s0 ------------------------->|s0  s1  s2  recent|
                                                |----- gap 5 ------|
        ^ inside the window at any episode length

  F = full visual tokens   g = gist tokens
  scope: within-episode
```

## Slide 2 - Where full visual tokens go

Header: The fix changes what earns a slot, and where that slot sits.

```
BEFORE - MemoryWAM          rule : by index
F = full visual tokens   g = gist tokens   a = action chunk   . = masked

  K>    f0 g0 a0 | f1 g1 a1 | f2 g2 a2 | f3 g3 a3 | f4 g4 a4
 Q v
 f0     F  g  .  | .  .  .  | .  .  .  | .  .  .  | .  .  .
 g0     F  g  .  | .  .  .  | .  .  .  | .  .  .  | .  .  .
 a0     F  g  a  | .  .  .  | .  .  .  | .  .  .  | .  .  .
 f1     F  g  .  | F  g  .  | .  .  .  | .  .  .  | .  .  .
 g1     F  g  .  | F  g  .  | .  .  .  | .  .  .  | .  .  .
 a1     F  g  .  | F  g  a  | .  .  .  | .  .  .  | .  .  .
 f2     F  g  .  | F  g  .  | F  g  .  | .  .  .  | .  .  .
 g2     F  g  .  | F  g  .  | F  g  .  | .  .  .  | .  .  .
 a2     F  g  .  | F  g  .  | F  g  a  | .  .  .  | .  .  .
 f3     F  g  .  | F  g  .  | .  g  .  | F  g  .  | .  .  .
 g3     F  g  .  | F  g  .  | .  g  .  | F  g  .  | .  .  .
 a3     F  g  .  | F  g  .  | .  g  .  | F  g  a  | .  .  .
 f4     F  g  .  | F  g  .  | .  g  .  | .  g  .  | F  g  .
 g4     F  g  .  | F  g  .  | .  g  .  | .  g  .  | F  g  .
 a4     F  g  .  | F  g  .  | .  g  .  | .  g  .  | F  g  a
        |anchor|   |anchor|   evicted    evicted    |recent|
```

```
AFTER - WorldTrace + learned gate   rule : by action utility, by slot rank

  K>    f0 g0 a0 | f1 g1 a1 | f2 g2 a2 | f3 g3 a3 | f4 g4 a4
 Q v
 f0     F  g  .  | .  .  .  | .  .  .  | .  .  .  | .  .  .
 g0     F  g  .  | .  .  .  | .  .  .  | .  .  .  | .  .  .
 a0     F  g  a  | .  .  .  | .  .  .  | .  .  .  | .  .  .
 f1     .  g  .  | F  g  .  | .  .  .  | .  .  .  | .  .  .
 g1     .  g  .  | F  g  .  | .  .  .  | .  .  .  | .  .  .
 a1     .  g  .  | F  g  a  | .  .  .  | .  .  .  | .  .  .
 f2     .  g  .  | .  g  .  | F  g  .  | .  .  .  | .  .  .
 g2     .  g  .  | .  g  .  | F  g  .  | .  .  .  | .  .  .
 a2     .  g  .  | .  g  .  | F  g  a  | .  .  .  | .  .  .
 f3     .  g  .  | .  g  .  | F  g  .  | F  g  .  | .  .  .
 g3     .  g  .  | .  g  .  | F  g  .  | F  g  .  | .  .  .
 a3     .  g  .  | .  g  .  | F  g  .  | F  g  a  | .  .  .
 f4     .  g  .  | .  g  .  | F  g  .  | .  g  .  | F  g  .
 g4     .  g  .  | .  g  .  | F  g  .  | .  g  .  | F  g  .
 a4     .  g  .  | .  g  .  | F  g  .  | .  g  .  | F  g  a
           |-- FIELD -|       LANDMARK      GIST    |--|
           q-3                q-2           q-1     recent

  GIST      one frame, MemoryWAM's compressor
  FIELD     contiguous gists merged in canonical space
  LANDMARK  one frame verbatim, picked by a gate scored on action loss

  all stored canonically, so a slot re-rotates them to a fixed distance
  from now, at any episode length. a landmark blocks a merge across it.
```

---

## Slide 3 - When a step goes wrong

Header: One wrong placement, and nothing in the current observation catches it.

**Example**: three blocks moved off their spots. Put each back, in order.

```
GOAL    block 1 -> spot A    block 2 -> spot B    block 3 -> spot C
        this mapping is in the robot's memory only

ERROR   the robot places block 1 on spot B, which belongs to block 2
        nothing looks wrong in the current observation

        TODAY                            WHAT IS NEEDED
        -----------------------------    -----------------------------
        memory marks block 1 done        memory marks block 1 unverified
        when the placement ends          until the result is checked
                  |                                |
                  v                                v
        robot moves on to block 2        robot moves on to block 2
                  |                                |
                  v                                v
        block 2 fails, spot B taken;     block 2 fails; memory plus
        robot blames block 2             diagnosis point back to block 1
                  |                                |
                  v                                v
        retrying block 2 cannot work     robot moves block 1 to spot A,
                  |                      then places block 2 and 3
                  v                                |
        goal never met, and on a real              v
        robot there is no second try     goal met inside the episode
```

- The **current observation** cannot catch this. Only **memory** can.
- **Memory** must hold what was *verified*, not what was *attempted*.
- **Diagnosis** must name the step that *caused* the failure, not the step that *failed*.

---

# Backup slides

## Backup A - The benchmarks I would measure this on

Header: Four benchmarks, each covering a different part of the problem above.

**RMBench** (2603.01229) - *which tasks the problem applies to*. Grades each task by the minimum past information its optimal action needs, not by step count.

**RoboMemArena** (2605.10921) - *how common it is*. **104 of 151** subtasks (**68.9%**) cannot be decided from the current observation alone, the highest ratio among memory benchmarks. Its transferring category is the example above: objects moved between visually identical containers, where the robot must remember the mapping and which moves are already done.

**RoboGraphBench** (2608.08036) - *the error itself, and what a stale memory costs*. Injects *wrong relocation*, moving an object to a visible but wrong container: only **31.5%** are recovered. GPT-5.4 wastes **47.7%** of its actions repeating work, finishing **23.1%**. Scores planners, not trained policies.

**RoboFAC** (2505.12224) - *whether the fix matches the cause*. **9,440** failure trajectories with a three-level cause taxonomy and corrective annotations, the only one carrying both. Its low-level correction lifts real success **47.5% -> 61.25%**.

## Backup B - What has been built

Header: Two systems cover the two halves. Neither closes the gap.

### HELM (2604.18791) - memory and recovery in one loop

- Adds an episodic memory, a verifier that predicts failure before acting, and a controller that rolls back, all on top of a frozen policy.
- Cuts redundant re-attempts **76%**; **+23.1 pp** on LIBERO-Long.
- Limits: the memory forgets at the episode boundary, and the rollback is the same whatever the cause.
- Its oracle arm is the telling number: injecting *ground-truth* subgoal completion lifts the base policy **58.4% -> 72.4%**, still **9.1 pp** short of HELM. The authors' own reading: memory's contribution is real but not the only factor.

### FLARE-Recovery (2608.26645) - diagnosis routed to a matching fix

- An MLLM diagnoses the error class at runtime and routes to a per-cause recovery adapter. **84.0%** across nine contact-rich RoboMimic tasks, against **72.2%** for its own backbone.
- Limit: the adapters are compiled at training time, so nothing from the running deployment is retained.
- Never runs the comparison that matters: diagnosed routing against generic rollback at equal detection quality and equal recovery budget.

**The gap**: a trained policy that keeps what it has *verified* and routes the fix to the *cause*.

## Backup C - Where the failure data comes from

Header: Two engines manufacture failures at scale. Neither labels what caused them.

### PlayWorld (2603.09030) - the robot fails on its own

- A VLM proposes scene-grounded tasks, a VLA executes them, and safety and reset mechanisms keep it running unsupervised.
- Human-collected data is concentrated on things going right; autonomous play captures the contact-rich events instead - missed grasps, slips.
- Predicted-versus-real policy success correlates at Pearson **0.8766**, and in-model fine-tuning lifts real-world success up to **65%**.

### Dream2Fix (2603.13528) - failures synthesised inside a world model

- Injects targeted action perturbations into a generative world model, starting from successful real demonstrations, then filters with four verifiers (VLM, inverse dynamics, joint pose, point tracking).
- **58.1%** of rollouts survive filtering, giving over **120,000** paired failure-correction samples. Real-world closed-loop recovery reaches **46%**.
- Cheap per sample, so it scales where physical self-play cannot.

**What neither gives**: a labelled *cause*. PlayWorld's failures are whatever happened; Dream2Fix labels the *correction*, not the cause class. Scoring whether a fix matched the cause needs the cause known in advance.
