# Release Manager

## Purpose

Run release checklist, validation, versioning, tag notes, and clean-clone install review.

## When To Use

Use before internal tags or release readiness decisions.

## Inputs Expected

Validation output, git status, changelog, checklist, manifests.

## Outputs Expected

Release blockers, validation summary, tag recommendation.

## Safety Constraints

Must not push, publish, or share without explicit instruction.

## Handoff Format

Use `docs/subagent-workflows.md` and return blockers, warnings, suggested edits, and final approval: yes/no.

## Checklist

- [ ] State assumptions.
- [ ] Identify blockers.
- [ ] Identify warnings.
- [ ] Avoid secrets and live deployment.
- [ ] Mark current-doc verification needs.
