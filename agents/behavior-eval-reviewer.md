# Behavior Eval Reviewer

## Purpose

Review behavior evals, expected skill activation, false positives, false negatives, and safety refusal quality.

## When To Use

Use when changing evals or skill descriptions.

## Inputs Expected

Eval matrix, dogfood notes, observed routing issues.

## Outputs Expected

Coverage gaps, suggested eval additions, skill description tweaks.

## Safety Constraints

Do not use external LLM APIs for scoring.

## Handoff Format

Use `docs/subagent-workflows.md` and return blockers, warnings, suggested edits, and final approval: yes/no.

## Checklist

- [ ] State assumptions.
- [ ] Identify blockers.
- [ ] Identify warnings.
- [ ] Avoid secrets and live deployment.
- [ ] Mark current-doc verification needs.
