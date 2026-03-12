# paper-visual-explainer Agent — Design Spec

**Date:** 2026-03-12
**Status:** Implemented

## Problem

Researchers want to quickly understand arxiv papers visually, but neither the `alphaxiv-paper-lookup` skill (text-only summary) nor the `excalidraw` skill (requires manual concept input) alone provides a complete end-to-end visual explanation workflow.

## Solution

A Claude Code custom agent (`paper-visual-explainer`) that orchestrates both skills into a single invocation:
1. Fetches machine-readable paper summary via alphaxiv API
2. Invokes the `excalidraw` skill to generate a diagram
3. Saves output to `Artefacts/` in the vault

## Design Decisions

### Agent vs. Skill
Implemented as a **custom agent** (`.claude/agents/`), not a skill (`.claude/skills/`). Reason: this is a multi-step orchestration workflow that runs to completion, with its own persona, process, and tool permissions. Skills are passive knowledge modules; agents are autonomous task performers.

### Two Modes
- **Single paper**: comprehensive technical multi-zoom diagram
- **Comparison (2+ papers)**: side-by-side comparison diagram showing differences and shared ideas

### Output Location
`Artefacts/` folder in the vault root. Naming: `{PAPER_ID}.excalidraw` for single; `compare-{ID1}-{ID2}.excalidraw` for comparison.

### Sub-skills Used
- **alphaxiv API** directly (`https://alphaxiv.org/overview/{ID}.md`) — same endpoint as `alphaxiv-paper-lookup` skill
- **`excalidraw` skill** — invoked via Skill tool for diagram generation

### Trigger
Explicit invocation only (not auto-triggered like skills). Fires when user expresses visual understanding intent: "diagram", "understand visually", "compare", "show me how X and Y differ".

## Files

| File | Purpose |
|------|---------|
| `.claude/agents/paper-visual-explainer.md` | Agent definition |
| `Artefacts/` | Output folder for generated diagrams |
