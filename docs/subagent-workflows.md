# Subagent Workflows

Use subagents to review a full chain launch plan without leaking expected answers.

1. Main agent receives the user prompt.
2. `chain-architect` creates the ADR and candidate stack shortlist.
3. `infra-ops-reviewer` reviews server topology and operations.
4. `protocol-security-reviewer` reviews threat model and launch blockers.
5. `docs-maintainer` checks references, docs, and limitations.
6. `release-manager` checks validation and release gates.
7. Main agent merges results into the final user-facing answer.

## Handoff Template

# Subagent Handoff

## Original user request

## Current draft

## Assumptions

## Files changed

## Questions for reviewer

## Required output

Return:
- blockers
- warnings
- suggested edits
- final approval: yes/no
