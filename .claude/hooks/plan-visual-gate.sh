#!/bin/sh
# PostToolUse:ExitPlanMode - flag a missing or stale plan visual after approval.
# PreToolUse deadlocks: plan mode forbids writing the HTML the gate demands.
# The slug comes from the plan's H1, so the exact filename is not computable
# here; compare mtimes against the newest docs/visuals/plan-*.html instead.
# Hole: re-rendering an unrelated visual after writing a plan satisfies it.

plan=$(ls -t "$HOME/.claude/plans"/*.md 2>/dev/null | head -1)
[ -n "$plan" ] || exit 0

visual=$(ls -t "${CLAUDE_PROJECT_DIR:-.}"/docs/visuals/plan-*.html 2>/dev/null | head -1)

if [ -z "$visual" ]; then
  echo "No plan visual found. Render $plan to docs/visuals/plan-{slug}.html with the visualize skill (Implementation-plan form) before exiting plan mode." >&2
  exit 2
fi

if [ "$plan" -nt "$visual" ]; then
  echo "Plan visual $visual is older than $plan. Re-render it with the visualize skill before exiting plan mode." >&2
  exit 2
fi

exit 0
