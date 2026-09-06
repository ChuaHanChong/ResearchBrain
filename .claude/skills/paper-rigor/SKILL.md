---
name: paper-rigor
description: "Judge whether a paper's method and experiments justify its claims, recording a solid/borderline/weak verdict in its KnowledgeHub note. Use when the user passes a paper and asks whether it is any good, whether the experiments hold up, whether it would pass peer review, or whether a recommendation is trustworthy - or doubts its novelty, baselines, ablations, variance or code release. Judges content quality only, never topical relevance."
---

# Paper Rigor

Reads one paper's full text and judges whether its method and experiments justify its claims. Whether it is worth *your* time is a different question, already answered by the graph and the research-direction docs.

One paper per run, and a full-text read is not cheap, so say so before starting on a list.

**Empirical papers only.** A survey, position or theory paper has no measured result to check the claim against, so give no verdict rather than forcing the rubric. Judge a mixed paper, like a method plus its dataset, on the empirical half.

## Procedure

1. **Read the full text** via `mcp__alphaxiv__get_paper_content(fullText=true)`, or `answer_pdf_queries` to target questions. The KH note is context, not evidence: it has no equations, hyperparameters or ablation tables, which is where the failures live.
2. **Blue pass.** Find the headline claim, then the table or figure that supports it. Note the protocol, the effect size, and anything the authors did that they did not have to.
3. **Red pass.** Work the Checks table. Then read the limitations section: a weakness stated there is disclosed, and every weakness it omits is a candidate for `undisclosed`.
4. **Mark each weakness** `material` and `undisclosed` where they apply, then aggregate and read the verdict off the rule in Materiality.
5. **Write** the verdict and assessment.
6. **Re-derive the verdict from the marks alone**, ignoring how the paper read. If that disagrees with what you wrote, the marks are right.

## Checks

How to find each failure, and the tag it is recorded under. Groups are axes, so a note can say a paper is strong on one and weak on another.

| Group | Check | Fails when | Tag |
|---|---|---|---|
| method | Novelty | the contribution is prior work relabelled - use the **Novelty check** below | `derivative` |
| | Soundness | a formulation error, an unstated assumption, a design that does not follow from the problem, or complexity no ablation justifies | `unsound` |
| attribution | Baselines | the obvious comparison is missing, outdated, left untuned, or given less data and compute | `weak-baselines` |
| | Own baselines | the strongest comparison is the authors' own reimplementation | `reimplemented-baselines` |
| | Ablation | several things vary at once, so the mechanism is not isolated | `ablation-confounded` |
| | Supervision | privileged information the baselines do not get, or that is unavailable at deployment | `hidden-supervision` |
| confidence | Variance | one run, no error bars, or too few trials to resolve the gap claimed | `no-variance` |
| | Leakage | hyperparameters or checkpoints chosen on the evaluation set, evaluation data seen in training, or a split not independent of it | `leakage` |
| | Reporting | part of the suite shown, a claim no table isolates, a metric that does not measure the claim, or accuracy without its cost | `selective-reporting` |
| generalization | Breadth | one domain, embodiment or setup, or simulation standing in for reality | `narrow-eval` |
| reproducibility | Code | no link, a dead link, or a repository without training code or an accessible backbone | `no-code` |
| | Hyperparameters | optimizer, learning rate, schedule or compute budget missing | `no-hyperparameters` |

A split is not independent when one episode or recording session is chunked across both sides, temporally ordered data is split at random, normalization statistics are fitted over both, or a scene, object instance or demonstrator recurs on an axis the abstract claims to generalize over.

Fetch the code link rather than trusting it exists; a dead repository is worse than none.

**Do not score lab prestige.** Affiliation is not evidence; venue and citations are context, never overrides.

## Novelty check

A related-work section is the authors' account of their own novelty - usually accurate, always incomplete. Do not judge from it:

1. List the papers related-work distinguishes itself from.
2. Find the real neighbourhood, not just the cited one. The area's `General/` topic file groups it, `Skill(skill="graphify", args="explain '<method>'")` surfaces graph-nearest papers related-work left out, and `Skill(skill="alphaxiv-search")` reaches prior art the vault does not hold. `grep -rl` in `_KnowledgeHub_` settles a specific title.
3. Read the **full text** of the closest one or two, not their KH notes. A note summarises a mechanism; only the paper says whether it is the *same* mechanism.
4. State the delta against what you read, naming the closest prior work as `[[id]] (Venue'YY)`, venue from that note's frontmatter.

If you cannot name the closest prior work, leave novelty unjudged.

## Strengths

Same groups, plus **candour**, whose weakness counterpart is the `undisclosed` mark rather than a tag of its own.

| Group | Tag |
|---|---|
| method | `novel-mechanism` |
| attribution | `strong-baselines` · `ablation-isolates` |
| confidence | `pre-declared-protocol` |
| generalization | `broad-eval` |
| reproducibility | `fully-released` |
| candour | `states-own-limits` |

Tags name the axis; the explanation line carries the specifics.
Keep the list short - a bigger vocabulary invites near-miss picking, and inconsistent picking destroys the comparability tags exist for.
Add one only for a failure no tag covers even loosely, and only if it is observable: not a missing limitations section (a formatting norm), not cherry-picking (alleged, never observed).
A new weakness tag needs its own Checks row, or nothing will prompt you to look for it.

## Materiality

Every weakness carries up to two marks:

- **`material`** - correcting it could plausibly make the headline claim **false**, not merely smaller. A weakness that shrinks the claim is not material; one that inverts it is. "Shrinks" means the abstract's sentence stays true at a smaller effect: "outperforms X" survives a halved gap, "improves X by 20 points" does not. Apply the per-tag defaults below first; this reaches only what no default discharged.
- **`undisclosed`** - a weakness the reader could not have seen, stated nowhere in the paper. When a weakness *is* disclosed, cite the section instead of marking it.

**The headline claim is the abstract's claim, and nothing else.** A result carried only by an ablation, an appendix or a secondary table is a sub-claim: record the weakness, leave it unmarked. Otherwise a paper thorough enough to ablate itself scores worse than one that never looked. An ablation is a sub-claim when it merely decomposes a result, headline when the abstract rests a causal statement on it. Read the abstract before deciding which.

**A visible omission is never `undisclosed`.** `no-variance`, `no-code` and `no-hyperparameters` are read straight off the figure, the links and the appendix, so the reader already knows. Reserve `undisclosed` for what a careful reader cannot see: a confound, privileged supervision, a contaminated split.

`weak-baselines` and `narrow-eval` are the two tags this rule is most often broken on: an absent comparator and an untested domain are equally visible. Either takes `undisclosed` only for a hidden fact about the comparison: a baseline silently under-resourced, its published number misreported, or an omitted comparator whose published same-benchmark number beats the paper's. Name that number. A merely absent comparator, or an evaluation whose extent the tables show, is visible and takes no mark.

**Each tag carries a default.** Materiality turns on effect size and claim, never the tag alone; argue every mark past it.

| Tag | Immaterial when |
|---|---|
| `no-variance` | the margin is wide relative to the trial count behind it, or the claim only declines to assert superiority ("competitive with") |
| `narrow-eval` | the claim is scoped to what was tested |
| `weak-baselines` | the absent comparator is weaker than one the paper already beats |
| `reimplemented-baselines` | the reimplementation lands on the original paper's reported number |
| `ablation-confounded` | the confound is smaller than the effect it would have to explain |
| `selective-reporting` | the omitted split appears elsewhere, or the claim states its own scope |
| `no-code`, `no-hyperparameters` | always - neither can make a measured result false |
| `leakage`, `hidden-supervision`, `unsound`, `derivative` | never by default - these attack correctness, so judge each on its evidence |

**Not every headline claim is a number.** An abstract makes performance claims ("94.3% on X") and mechanism claims ("X is what enables Y"), and a weakness that leaves every number standing can still falsify the mechanism, so "the success numbers stand regardless" is never on its own a reason to drop a mark. These tags land here:

- `derivative` attacks **novelty**: if the abstract asserts a new mechanism and that mechanism is prior work, the claim is false however good the results are. Drop it only when the abstract claims no novelty for that component, or when the novelty it claims is a compound the component does not carry alone.
- `ablation-confounded` attacks **attribution**: when the abstract names a component as what produces the gain, a confounded ablation leaves that unsupported. Drop it only after checking that the abstract claims an aggregate system result and never names the component.
- `hidden-supervision` attacks **transfer to deployment**. Drop it when the abstract states the privileged input as part of the setting, keep it when the abstract implies the method runs without it.
- `selective-reporting` attacks a **claimed contribution** whose only support is the omitted evidence. Drop it only when the abstract does not list that component as a contribution.

**Variance takes numbers, not a reflex.** `no-variance` **material** must name the margin it threatens **and the trial count behind it** - "3-pt gap over 20 trials, Tab 2".

A stated count is the input that computes an interval, not a pass through the check: at an 80% success rate the 95% Clopper-Pearson interval spans about 38 points at 20 trials, 24 at 50, 17 at 100. Treat those as an anchor, never a test: a one-arm interval is not the interval on a between-method gap, so a single-number rule misreads it by a wide factor either way.

A pre-declared protocol makes an interval trustworthy, not narrower. Trials of one trained policy bound rollout noise, not training noise, so the count says nothing about seed variance between two separately trained systems.

With no stated count, judge the margin on its face: material only when ordinary run-to-run noise could invert the gap, not merely shrink it.

**An equivalence-shaped claim needs a tighter bound than a superiority claim, not a looser one.** "Matches", "on par with" and "comparable to" assert the gap is negligible, and failing to detect a difference is not evidence of equivalence: the margin at stake is that negligible gap, material when the benchmark's known spread exceeds it. Only "competitive with", which declines to assert superiority, is discharged by modest sizing.

**Aggregate before reading the verdict off.** Ask once whether weaknesses left immaterial **by magnitude** - a narrow margin, a small confound, a reimplementation slightly off the original - attack the same headline claim and together could invert it where none could alone. If so, mark the largest `material` and name the others it carries. Aggregation confers `material` only, never `undisclosed`. A default discharged for a logical reason (claim scoped, comparator dominated, split appears elsewhere) has nothing to add.

```
weak        a weakness marked both material and undisclosed
borderline  any material weakness
solid       no material weakness
```

`weak` means material **and** hidden. A disclosed or visible material weakness caps at `borderline` however severe, and that split is safe because every material weakness is recorded inline in both buckets, so the frontmatter filters rather than hides.

`solid` means **the claims are correctly sized to the evidence**, not that the paper is flawless. Without materiality that verdict would be unreachable.

Strengths never upgrade a verdict, but evidence about protocol is not a strength - it is input to materiality, as the trial count above is. The `pre-declared-protocol` tag itself buys nothing once a mark survives the table.

## Output

Verdict in frontmatter, where Bases can filter on it. Insert before the closing `---`; do not anchor on `citations:` or the venue fields, which come from `venue-sync` and may not exist yet.

```yaml
rigor: "borderline"
```

Everything else under `## Assessment` in the `%%` block, which reads BibTeX, then Assessment, then Publication. Anchor above `## Publication` when `venue-sync` has written one, otherwise above the closing `%%`.

```
## Assessment

- rigor_checked: YYYY-MM-DD

**Weaknesses**
- `reimplemented-baselines` **material** - the two strongest are the authors' own, so the floor is unverified. (Sec 6.1)
- `no-variance` - one training run, no seeds; immaterial against a 67-point gap.

**Strengths**
- `novel-mechanism` - the RL critic scoring predicted wrench; joint prediction alone is TA-VLA [[2509.07962]] (CoRL'25).
- `pre-declared-protocol` - 20 trials per cell, fixed before running, no re-runs. (Sec 6.1)
```

Weaknesses come first, here and in the note, because that is where the verdict is decided. Marks go inline after the tag.

**One line per finding, 20 words maximum for the explanation after the tag**, naming the table, figure or section that decided it. A finding that will not fit is not sharp enough yet.

**Record every `material` and `undisclosed` weakness, then stop.** Record a discharged `leakage`, `hidden-supervision`, `unsound` or `derivative` finding too, unmarked, naming the evidence that discharged it: it departs from its default and nothing else shows it was weighed. Otherwise add a non-marked weakness only when it is genuinely surprising, and at most two strengths. Four to six lines is the usual length; a note long enough to scroll defeats the point.

## Failure modes

**Do not soften a material weakness because the paper was candid about it.** Disclosure is not evidence. This skill's first run gave a well-written paper `solid` over five weaknesses; step 6 exists to catch that.

**Watch the distribution.** These marks exist to separate papers, so if nearly everything you judge lands in one bucket the marks have drifted rather than the field having collapsed.

**Do not mark a sub-claim.** The verdict answers whether the abstract is true. An ablation row that sits inside noise is worth a line, not a mark.

**Do not manufacture concerns to look thorough.** If nothing is material, `solid` is the honest answer. Invented objections train the reader to ignore the flags.

**Do not judge novelty from summaries.** Its own development got this wrong twice - from the related-work, then from a KH note - before the prior work's full text settled it.

When the full text will not load, say so and give no verdict - a missing assessment beats a guessed one.
