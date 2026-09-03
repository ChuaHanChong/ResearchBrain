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
3. **Red pass.** Work the Checks table. Then read the limitations section and mark every weakness that is *not* in it.
4. **Mark each weakness** `material` and `undisclosed` where they apply, then read the verdict off the rule in Materiality.
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
| | Leakage | hyperparameters or checkpoints chosen on the evaluation set, or evaluation data seen in training | `leakage` |
| | Reporting | part of the suite shown, a claim no table isolates, a metric that does not measure the claim, or accuracy without its cost | `selective-reporting` |
| generalization | Breadth | one domain, embodiment or setup, or simulation standing in for reality | `narrow-eval` |
| reproducibility | Code | no link, a dead link, or a repository without training code or an accessible backbone | `no-code` |
| | Hyperparameters | optimizer, learning rate, schedule or compute budget missing | `no-hyperparameters` |

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

- **`material`** - correcting it could plausibly change the headline claim.
- **`undisclosed`** - you looked and the paper states it nowhere. When a weakness *is* disclosed, cite the section instead of marking it.

```
weak        a weakness marked both material and undisclosed
borderline  any material weakness
solid       no material weakness
```

Materiality depends on the effect size, not the weakness:

- `no-variance` on a 67-point gap is immaterial. No seed variance closes that.
- `no-variance` on a 3-point gap is material. That is noise.
- `narrow-eval` is immaterial when the claim is scoped to what was tested, material when the paper claims generality it did not evaluate.

`solid` means **the claims are correctly sized to the evidence**, not that the paper is flawless. Without materiality that verdict would be unreachable, since almost no real-robot paper reports multiple runs.

Strengths never upgrade a verdict. A pre-declared protocol does not buy off a result inside the noise.

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
- `no-variance` **undisclosed** - one training run, never mentioned; immaterial against a 67-point gap.

**Strengths**
- `novel-mechanism` - the RL critic scoring predicted wrench; joint prediction alone is TA-VLA [[2509.07962]] (CoRL'25).
- `pre-declared-protocol` - 20 trials per cell, fixed before running, no re-runs. (Sec 6.1)
```

Weaknesses come first, here and in the note, because that is where the verdict is decided. Marks go inline after the tag.

**One line per finding, 20 words maximum for the explanation after the tag**, naming the table, figure or section that decided it. A finding that will not fit is not sharp enough yet.

**Record every `material` and `undisclosed` weakness, then stop.** Add a non-marked weakness only when it is genuinely surprising, and at most two strengths. Four to six lines is the usual length. A note long enough to scroll defeats the point of having one.

## Failure modes

**Do not soften a material weakness because the paper was candid about it.** Disclosure is not evidence. This skill's first run gave a well-written paper `solid` over five weaknesses; step 6 exists to catch that.

**Do not manufacture concerns to look thorough.** If nothing is material, `solid` is the honest answer. Invented objections train the reader to ignore the flags.

**Do not judge novelty from summaries.** Its own development got this wrong twice - from the related-work, then from a KH note - before the prior work's full text settled it.

When the full text will not load, say so and give no verdict - a missing assessment beats a guessed one.
