---
name: loop-engineering
description: Drive one deliverable to an explicit quality bar through a converge-until-good-enough loop with discover, plan, execute, verify, and iterate stages. Each success criterion is either measurable, decided by a metric or check that returns the same answer for anyone, or taste, decided by a rubric score from independent judges; the loop closes a round only when a fresh gate confirms every measurable criterion passes and every taste criterion clears its bar, which is what stops a self-graded loop from declaring victory early. Use this when someone hands you a research plan, spec, document, dataset, or code change and wants it iterated until it meets a bar rather than answered in one pass, or says "loop until", "iterate until it is solid", "keep improving until it meets the criteria", "make this bulletproof", or "converge on". This is the methodology layer only. For running something on a schedule or interval defer to the built-in loop and schedule skills. Explicit invocation only, run it as /loop-engineering.
argument-hint: "[the deliverable to drive to a bar]"
disable-model-invocation: true
---

# Loop engineering

Take one deliverable and improve it across rounds until it clears an explicit bar, then stop. The value is not the repetition, which any agent can do, but two things a single pass skips: criteria strict enough that they can actually fail, and a verification step that does not trust the author's own grade. Without both, a loop just circles until the model talks itself into "good enough".

This skill is the methodology, not the runner. It does not schedule anything. A recurring or timed task belongs to the built-in `loop` and `schedule` skills; hand those off and do not reimplement them here.

## When it earns its cost

Reach for the loop when the deliverable has a checkable bar and is worth more than one pass: a research plan that has to survive scrutiny, a spec that must be unambiguous, a document that has to be right rather than merely written. Skip it when one pass fully answers the request, and route anything about intervals, polling, or "every N minutes" to the scheduler skills instead.

## The loop

Run the five stages in order. State the loop out loud as you go, so the user can see where it is: end each round by printing `ITERATING` (with the weakest criterion you are about to fix) or `FINAL` (only after the gate passes clean).

### 1. Discover

Read the real, current state of the deliverable and the standard it will be judged against. Open the actual file, the actual data, the actual prior review. Do not start from this template or from memory, because the bar for a research plan is not the bar for a config file, and you cannot write criteria for a thing you have not looked at.

### 2. Plan

Write the success criteria. This is the stage that decides whether the loop converges on something real or on the model's own approval, so give it the most care.

A criterion earns its place only if it can fail. The test is whether a stranger who did not do the work could check it and come back with a clear verdict. "The methodology is solid" cannot fail, so it is not a criterion. "Every hypothesis states a falsifier and a pre-registered decision threshold" can fail, so it is. Keep one claim per criterion so a single failure points at a single fix.

Criteria come in two kinds, and each is judged differently. A measurable criterion is decided by a metric or check that returns the same answer for anyone: a test passes, a number clears a threshold, a search returns nothing. A taste criterion turns on judgement that no metric captures (is this prose clear, is this framing non-obvious, is this design coherent); it is decided by a rubric that says what a weak, a middling, and a strong result look like, plus the score that clears. Prefer measurable and convert toward it where you can, since "clear prose" partly cashes out as "every acronym defined on first use, no sentence over N words"; write a rubric only for the residue of judgement that genuinely resists a metric, rather than dressing taste up as objective. `references/criteria.md` holds the craft in full, with a library of both kinds across deliverable types; read it before writing criteria for anything unfamiliar.

Then state the single next step, not the whole remaining plan, the one move that most raises the weakest criterion. Set a round budget at the same time: the number of rounds after which you stop and report the remaining gaps even if the gate has not passed, so the loop cannot run forever.

### 3. Execute

Produce or improve the work, always attacking the weakest criterion first. When the step fans out over many independent units (sections to rewrite, claims to ground, files to touch), use the Workflow tool so the units run in parallel; keep steps that need the user, or that are inherently serial, in the main conversation. Scale the fan-out to the workload rather than to a fixed number.

### 4. Verify

Two tiers, and the distinction is the point of the whole skill.

Between gates, check each criterion yourself as triage: run the metric on a measurable one, score a taste one against its rubric, and say exactly what is weakest. This only picks the next round's target; it never ends the loop.

At the gate, reached only once every measurable criterion passes its check and every taste criterion self-scores at its bar, hand the work to fresh agents through a Workflow, each grounded in the real artifact rather than your account of it. The two kinds clear differently, because they fail differently:

- A measurable criterion is decided by re-running its check independently. One verifier per criterion is the default, and it clears if that verifier cannot refute it; when the criterion has several necessary properties, give it a verifier per property and let any single failure fail it, since each checks something the criterion needs.
- A taste criterion is decided by independent judges scoring it against the rubric. It clears when their aggregate meets the bar, not on any one score, because a taste score is a noisy estimate of one quality and several judges exist to average out the noise, not to let a lone judge decide.

Match the aggregation to the kind: AND across the distinct necessary properties of a measurable criterion, median across the redundant judges of a taste one. Report what actually cleared, raise nothing to reach the exit, and treat a clean gate as the goal, not a failure to be productive. The gate skeleton is in `references/criteria.md`.

The reason for the split is on record: a model grading its own work will pass claims that are false, because it is checking its intent rather than the artifact. Fresh eyes, running the check or scoring the rubric, judge the artifact.

### 5. Iterate

If the gate knocks anything down, fix the weakest survivor and run the loop again. Stop on one of two conditions: the gate passes clean, print `FINAL`; or a round budget you stated up front is spent, in which case print the honest remaining gaps rather than declaring `FINAL`. A loop that hides an unmet bar to reach the exit is the failure this skill exists to prevent.

## Working rules

- Do not stall on questions. When something is ambiguous, make a sensible assumption, note it in the round, and keep going. Surface a genuinely load-bearing ambiguity once, then proceed on your best reading.
- The self-score is a triage tool. The gate is the stop condition. Never let the first stand in for the second.
- Converge, do not perfect. The bar you wrote in Plan is the finish line; clear it and stop rather than polishing past it.
- Two places call for the Workflow tool: the execute fan-out, when a step splits into many independent units, and the verify gate. A serial single-unit step stays inline.
- Scheduling is not yours. Intervals, cron, wakeups, and durable runs belong to the built-in `loop` and `schedule` skills.
