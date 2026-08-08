# Research Directions

Synthesis docs that turn the vault's surveys + benchmarks into **promising, first-principles research directions** — each an integrated, non-consensus thesis (Hinton-as-mentor advisory voice) carrying a **measurable, KnowledgeHub-sourced bet**. Generated and maintained by the `/research-directions` command, which embeds the canonical format spec.

## Two axes

The docs are organized on **two orthogonal axes** — the *how* and the *what*:

| Location | Axis | Holds |
|---|---|---|
| **`Embodied-AI.md`** | **Umbrella** — cross-cutting, embodiment-agnostic *mechanism* directions (data / training / evaluation / mobility) that apply to **any** robot body | the entry point |
| **`Mechanism/`** | **The HOW** — embodiment-agnostic mechanisms | `WAM` (world-action-model machinery) · `Spatial-4D` (model-agnostic 3D/4D representation) · `Sim2Real` (the reality gap) |
| **`Capability/`** | **The WHAT** — physical capabilities a body provides, independent of which robot has them | `Manipulation` (arms + hands) · `Locomotion` (legs + wheels) · `Whole-Body` (the coupling) |

## Why by capability, not by robot

Embodiments are **compositions of shared capabilities**: a fixed arm = Manipulation; a quadruped = Locomotion (+ a mounted arm); a humanoid = all three + the coupling. Organizing by *capability* means every research bet sits at exactly one `(capability × mechanism)` coordinate and **nothing duplicates** — whereas one-doc-per-robot would write "legged locomotion" twice (once for the humanoid, once for the quadruped). So the `Capability/` docs are deliberately **cross-embodiment**: `Locomotion` covers bipedal *and* quadruped; `Manipulation` covers humanoid hands *and* fixed-base arms.

## Reading a specific embodiment

A robot is a **path across the capability docs**, not a doc of its own. The humanoid, for example:

> [!example] Humanoid reading path
> A humanoid needs **all three** capabilities at once, so it's a path across the three docs. The humanoid-relevant clusters in each:
>
> - **Legs** → [[Locomotion]] · *Bipedal Locomotion & Dynamic Skills* — gait, terrain, balance, push-recovery, fall-recovery
> - **Arms + hands** → [[Manipulation]] · *Bimanual / Dual-Arm Coordination* + *Dexterous & In-Hand Control* (the Grasping & Contact-Rich clusters also serve humanoid hands)
> - **Whole-body coupling** → [[Whole-Body]] · *Whole-Body Loco-Manipulation* + *Force-Adaptive Coordination Under Load* + *Whole-Body Teleoperation & Retargeting*

Each `Capability/` doc carries this callout in its own Cross-References section.

## Focus-Direction (applied output)

Where the survey docs above narrow into one pitchable proposal:

| File | Holds |
|---|---|
| `Focus-Direction.md` | the thesis — single integrated bet, drawn from across Mechanism/Capability |
| `Focus-Direction-Research-Plan.md` | lean plan — one pass, no branching |
| `Focus-Direction-Research-Plan-detailed.md` | detailed plan — same 12-section spine, full derivations |
| `Focus-Direction-Brief.canvas` | professor-facing pitch — problem, discovery funnel, method foils vs solution refs, mind-map |
| `Focus-Direction-Paper-Code-Index.md` | reference appendix — every cited paper's repo/PDF/clone/index status |

## Conventions

- **Links resolve by basename** (Obsidian shortest-path) — `[[WAM]]`, `[[Manipulation]]`, `[[Embodied-AI]]` — so the folder a doc lives in doesn't matter for linking.
- Every doc follows the canonical **Research-Direction Document Format** (single source of truth: `.claude/commands/research-directions.md`): `[!abstract]` Overview → Methodology → Survey Landscape → Formal Framing → Cluster Overview → Cluster cards (8-section per direction) → Cross-Cutting Themes → Benchmark Gaps → Cross-References.
- **Routing for new docs**: a *mechanism* (embodiment-agnostic) → `Mechanism/`; a *physical capability* → `Capability/`; the cross-cutting umbrella stays at the folder root.

## Index

| Doc | Axis | Directions | Clusters |
|---|---|---|---|
| [[Embodied-AI]] | umbrella | 11 | 4 |
| [[WAM]] | Mechanism | 7 | 2 |
| [[Spatial-4D]] | Mechanism | 11 | 4 |
| [[Sim2Real]] | Mechanism | 15 | 5 |
| [[Manipulation]] | Capability | 14 | 5 |
| [[Locomotion]] | Capability | 9 | 2 |
| [[Whole-Body]] | Capability | 13 | 4 |
