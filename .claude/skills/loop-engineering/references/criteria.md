# Writing criteria, and the gate that checks them

Two things make or break a convergence loop: criteria strict enough to fail, and a gate that does not trust the author's own grade. This file covers both, then works one example end to end.

## Part 1: criteria that can fail

A criterion is worth writing only if a stranger who did not do the work could read it, apply it to the artifact, and return a clear verdict. Everything else is a wish.

Three tests to apply to every candidate criterion:

1. **The stranger test.** Could someone with no memory of your reasoning judge it from the artifact alone? If judging it requires your intent, rewrite it until it does not. "The plan is well motivated" fails this. "Section 2 states the problem, why it is unsolved, and what changes if it is solved" passes it.
2. **Measurable or taste.** Decide which kind it is, because they are judged differently. A measurable criterion has a metric or check that returns the same answer for anyone: a threshold to clear, a test to pass, a search that must come back empty; put the number or the procedure in the criterion. A taste criterion turns on judgement no metric captures, so it needs a rubric: a short scale that says what a weak, a middling, and a strong result look like, and the score that clears. Prefer measurable and convert toward it where you can, since "clear prose" partly cashes out as a check ("every acronym defined on first use, no sentence over N words"); write a rubric only for the judgement that genuinely resists a metric, rather than dressing taste up as objective.
3. **One claim per criterion.** A criterion that bundles three requirements hides which one failed and points at no single fix. Split it. The loop attacks the weakest criterion each round, so each criterion must name one thing.

Turning a vague ask into a set: the user rarely hands you criteria, they hand you "make it solid". Discover what "solid" means for this artifact by reading the standard it is judged against (a rubric, a prior review, the conventions of the genre), then decompose that standard into single-claim criteria, each tagged measurable or taste. The decomposition is the real work of the Plan stage.

## Part 2: soft criteria and their strict rewrites

Each pair below shows a criterion that always passes (useless) and the rewrite that can fail (useful). The first four are measurable, the fifth is taste; the move differs, as the closing note says.

**Research plan**
- Soft: "The hypotheses are rigorous and testable."
- Strict: "Every hypothesis names a falsifier and a pre-registered decision threshold with the statistical test that decides it, so a reader can state in advance what result would kill it."

**Specification**
- Soft: "The API is clearly specified."
- Strict: "Every endpoint states its required and optional inputs, the type of each, the error returned when a required input is missing, and one worked request-and-response example; no behavior is described only in prose."

**Code change**
- Soft: "The change is well tested."
- Strict: "Every new branch has a test that fails on the pre-change code and passes on the new code, and the test names the exact input and expected output rather than asserting no-throw."

**Prose document**
- Soft: "The argument is well supported."
- Strict: "Every load-bearing claim cites a primary source, and each citation has been checked against that source rather than against a summary of it, with contested claims marked as contested."

**Prose quality (taste)**
- Soft: "The writing is engaging."
- Rubric: "Score 1-10 for whether a first-time reader stays oriented, where a 3 loses the thread by the second section, a 6 reads clearly but forgettably, and a 9 makes the structure feel inevitable. Clears at 7." No check captures this, so independent judges score it and the loop clears on their aggregate.

The move differs by kind. In the four measurable rows, replace an adjective the author grades with a check a stranger runs. In the taste row, you cannot remove the judgement, so you discipline it: name the scale and the bar, then hand it to judges who never saw your reasoning.

## Part 3: the independent-verifier gate

The gate is the stop condition. It runs only after the self-check says every criterion is met, and it exists because a model grading its own work checks its intent, not its artifact, and so passes claims that are false. A measurable criterion and a taste criterion clear by different rules, because they fail differently.

Rules for a measurable criterion:

- The default is one verifier per criterion (or per finding, when the criteria produced a finding list). Each sees the real artifact and the one criterion it owns, never your account of the work.
- Each verifier is told to refute, and to default to refuted when the evidence is not airtight. The burden is on the work to survive, not on the verifier to justify killing it.
- A criterion with a single verifier clears if that verifier cannot refute it. A criterion that can fail in more than one way gets several verifiers with distinct lenses, one per failure mode, and any single refutation fails it, since each lens checks a different property the criterion needs and a real flaw found by one lens is not cancelled by another lens finding none. The escalation buys coverage, not a vote: more lenses catch more real flaws, and any real flaw is disqualifying. Reporting that nothing survived is the goal, not a failure to be useful, and a verifier that manufactures a finding to look productive has broken the gate.
- Every verdict quotes the artifact. A verdict grounded in a paraphrase is not a verdict.

Rules for a taste criterion:

- No verifier can refute it, because there is no metric to fail. Instead, several independent judges score it against its rubric, each seeing the artifact and the rubric but not your reasoning or each other's scores.
- The criterion clears when the aggregate score, the median, meets the rubric's bar. A lone low score does not sink it and a lone high score does not save it, because each judge is a noisy estimate of one quality and the panel exists to average the noise out.
- This is the opposite of the multi-lens rule above, and deliberately so. Distinct lenses on a measurable criterion check separate necessary properties, so any one failure is disqualifying (AND). Redundant judges on a taste criterion estimate the same quality, so you take their central tendency (median). Match the aggregation to the kind, and never let a taste panel vote a measurable property alive or a lens panel average a real flaw away.
- Every score cites the artifact for its reasoning. A score with no artifact-grounded justification is noise, not a judgement.

A compact Workflow skeleton for the gate, structure only, agent counts left to the runtime. Numbers here are illustrative shape, not a required fan-out.

```
export const meta = {
  name: 'converge-gate',
  description: 'Independent-verifier gate for a convergence loop',
  phases: [{ title: 'Verify' }],
}

const VERDICT = {
  type: 'object',
  required: ['refuted', 'reasoning'],
  properties: {
    refuted: { type: 'boolean' },
    reasoning: { type: 'string', description: 'quote the artifact; default refuted when not airtight' },
  },
}

// `args` carries the artifact path and the criteria list, passed in by the caller.
const results = await parallel(
  args.criteria.map((c) => () =>
    agent(
      `Refute this criterion against the real artifact at ${args.path}.
       CRITERION: ${c}
       Read the artifact, quote it, and default to refuted=true unless the evidence is airtight.`,
      { label: `verify:${c.slice(0, 40)}`, phase: 'Verify', schema: VERDICT },
    ),
  ),
)

const cleared = args.criteria.filter((c, i) => results[i] && !results[i].refuted)
return { total: args.criteria.length, cleared: cleared.length, failed: args.criteria.filter((c, i) => !results[i] || results[i].refuted) }
```

This skeleton is the measurable path: one verifier per criterion, cleared only when its verifier does not refute it. For a criterion that can fail in more than one way, map it instead to several agents with distinct lenses (correctness, completeness, and does-the-check-actually-decide-it) and fail the criterion if any lens refutes it, the same filter extended so one refutation among the lenses is enough.

For a taste criterion, swap the schema and the aggregation. Each judge returns `{ score, reasoning }` with `score` a 1-10 integer, and the criterion clears when the median score meets its bar:

```
const TASTE = {
  type: 'object',
  required: ['score', 'reasoning'],
  properties: {
    score: { type: 'integer', minimum: 1, maximum: 10 },
    reasoning: { type: 'string', description: 'cite the artifact against the rubric' },
  },
}
const median = (xs) => xs.slice().sort((a, b) => a - b)[Math.floor(xs.length / 2)]
// spawn an odd number of judges per taste criterion, then:
const passed = median(scores) >= criterion.bar
```

## Part 4: worked example, a research plan's methodology

This walks the loop over one deliverable to show the *shape* of each stage. It is not an answer key. When you run the loop on this same plan, derive the criteria from the artifact as it stands that day, since the plan and the literature move; do not lift the set below.

The ask: "make this research plan's methodology solid."

**Discover.** The plan lives in two files, a lean plan and a detailed plan, and its section 7 already carries pre-registered quantitative gates (margins in percentage points, named statistical tests, void conditions). Its abstract records that one adversarial review was already folded in. So the bar is not "add rigor from nothing", it is "does every part of the methodology meet the standard the strongest parts already set". That reading only comes from opening the files, which is why Discover precedes Plan.

**Plan.** A strict criteria set for "solid methodology", each single-claim and stranger-checkable:

- Every hypothesis in section 4 names a falsifier and a pre-registered decision threshold with the test that decides it.
- Every gate in section 7 is decidable from numbers stated in the plan, with no gate resting on an adjective.
- Every novelty claim survives a check against live literature, with any partial pre-emption named rather than omitted.
- Every benchmark named maps to a specific gate it discharges, and no gate lacks a benchmark.

All four are measurable: each is decided by a check (does this hypothesis name a threshold, does this gate cite numbers, does a pre-empting paper exist, does this benchmark map to a gate) that lands the same way for any reader. A taste criterion could belong here too, for instance "the central framing reads as non-obvious rather than a repackaging of known work", which no check settles; that one would carry a rubric and be scored by independent judges instead. Every criterion above is still about the plan, checkable by quoting it. Rules about how the loop runs, such as "no criterion is self-scored at the gate", are conduct of this skill, not criteria of the deliverable, so they never enter the set; a criterion you cannot judge the artifact against is a process rule in disguise. The single next step is the one that most raises the weakest of these, found by the self-check, not the first in the list.

**Execute.** Grounding every novelty claim against live literature is a fan-out over many independent claims, so it goes to a Workflow, one claim per agent. Rewriting a single section's gate to be number-decidable is serial and stays inline.

**Verify.** Run each of the four checks yourself to pick the weakest, then, once all four pass, run the gate: one verifier per criterion, each reading the actual plan files, each told to refute and to default to refuted, each quoting the section it judges. The novelty criterion's verifier checks the literature itself rather than trusting the Execute agent's grounding, because the whole reason for the gate is that the author's own grounding is what needs checking. Were a taste criterion in the set, it would go to a panel of judges scoring its rubric instead, clearing on the median.

**Iterate.** Whatever the gate refutes becomes the next round's weakest point. Print `ITERATING` with that point named, or `FINAL` once the gate refutes nothing, or the honest remaining gaps if a stated round budget runs out first.
