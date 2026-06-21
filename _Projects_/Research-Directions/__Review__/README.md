# Research-Directions Five-Perspective Review

A systematic adversarial review of **every cluster and every research direction** in `_Projects_/Research-Directions/`, generated 2026-06-20. Each unit was put through a fixed 4-prompt lens and graded by an independent peer reviewer.

## How to read

1. Start with **[[00-Master-Review]]** — the whole-corpus synthesis: the COMMIT shortlist (5), the RESHAPE list (13), the full commit/de-risk/reshape ranking over all 78 directions, the global contradiction map, the universal agreements, and the field-wide blind spots. Read sections 4, 5, and 9 first.
2. Then drill into a **per-doc review** below. Each opens with a verdict-summary table + a doc-level synthesis, then the full 4-prompt block for every cluster and direction in that doc.

## Methodology

For each of **103 units** (25 clusters + 77 directions + 1 Focus synthesis), an **analyst** ran:
- **Prompt 1** — five expert perspectives (Practitioner / Academic / Skeptic / Economist / Historian), each with a core position, its strongest evidence, and the one thing only that lens sees.
- **Prompt 2** — a contradiction map (where the perspectives clash, strongest/weakest, the resolving question, the universal agreement, the blind spot none addressed).
- **Prompt 3** — a synthesis briefing for *a researcher deciding whether to commit to the bet* (CEO summary, 5 ranked findings, the hidden connection, the actionable insight, the frontier question).

Then an **independent peer reviewer** ran **Prompt 4** — per-finding confidence 1-10, weakest link, bias check, a missing 6th perspective, and a Stanford-prof letter grade.

Every novelty/whitespace claim was stress-tested against the **live literature via the alphaxiv MCP**. Cited paper IDs are real (88.7% resolve to vault KnowledgeHub notes; the rest are historical references or newly-discovered threats). The full machinery was a set of dynamic multi-agent workflows (~215 agents).

## Headline findings

- **Well-aimed but late.** Of 78 directions, **0 are fully pre-empted** but **56 are partially pre-empted** — the taste is excellent (every direction targets a real gap) but the novelty wedges are narrow and aging.
- **Quality is high and bunched:** grades cluster at B+/A- (62 B+, 26 A-, mean peer confidence 7.03/10); no weak directions, no breakout A's.
- **The durable, fundable asset is the measurement artifact (benchmark / protocol / diagnostic), not the mechanism** — mechanism cells fill in 6-12 months by compute-rich labs while the matched-comparison protocol nobody ran stays open. This recurs in all 8 docs.
- **The biggest systemic blind spot is the Hardware/Sensor-Realist** ("who pays for the sensor / what is the installed base"), flagged in **37 of 103** reviews. Adjacent systemic gaps: statistical power of OOD margins (21×), safety/calibration "what does the policy do when its imagination is confidently wrong" (14+14×), benchmark-validity/metrologist (11×).
- **The deepest contradiction:** open-loop fidelity-correlation vs closed-loop feedback-gain — half the corpus studies sim-real correlation as the object, the other half argues feedback dissolves it.

## Files

| File | Scope | Units |
|---|---|---|
| [[00-Master-Review]] | cross-cutting synthesis + ranking | — |
| [[Embodied-AI-Review]] | umbrella | 3 clusters + 9 directions |
| [[WAM-Review]] | Mechanism | 2 + 7 |
| [[Spatial-4D-Review]] | Mechanism | 4 + 11 |
| [[Sim2Real-Review]] | Mechanism | 5 + 15 |
| [[Manipulation-Review]] | Capability | 5 + 14 |
| [[Locomotion-Review]] | Capability | 2 + 8 |
| [[Whole-Body-Review]] | Capability | 4 + 13 |
| [[Focus-Direction-Review]] | chosen synthesis | 1 holistic |

`Focus-Direction-Repo-Map.md` was excluded (it is a paper↔code infrastructure index, not a research thesis). The per-unit raw analyst/peer blocks were assembled into the per-doc files above and the scaffolding archived outside the vault.
