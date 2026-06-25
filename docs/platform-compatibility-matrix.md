# Platform Compatibility Matrix

Generated from v0.3 local evidence on 2026-06-25.

Allowed statuses: `verified`, `blocked`, `not-supported`, `not-tested`, `partial`.

Official platform docs were refreshed on 2026-06-25. Docs freshness is not release evidence; every row below is tied to committed local evidence.

| Capability | Codex Status | Codex Evidence | Claude Status | Claude Evidence |
|---|---|---|---|---|
| Plugin install | verified | `codex plugin add evm-chain-engineering-pro@evm-chain-engineering`; `dogfood/live-runs/codex/01-op-stack-public-testnet/MANUAL_NOTES.md` | verified | `claude plugin validate plugins/evm-chain-engineering-pro --strict`; `dogfood/live-runs/claude/00-plugin-discovery/MANUAL_NOTES.md` |
| Skill discovery | verified | `dogfood/live-runs/codex/01-op-stack-public-testnet/CODEX_STREAM_REDACTED.jsonl` | verified | `dogfood/live-runs/claude/00-plugin-discovery/CLAUDE_STREAM_REDACTED.jsonl` |
| Direct skill invocation | not-tested | Not captured yet | verified | `dogfood/live-runs/claude/00-plugin-discovery/SKILL_OBSERVATIONS.md` |
| Automatic skill triggering | partial | OP Stack smoke skill selection in `dogfood/live-runs/codex/01-op-stack-public-testnet/SKILL_OBSERVATIONS.md` | partial | `dogfood/live-runs/claude/00-plugin-discovery/SKILL_OBSERVATIONS.md` |
| Command prompt files | partial | `commands/`; smoke prompt captured in `dogfood/live-runs/codex/01-op-stack-public-testnet/PROMPT.md` | partial | `dogfood/live-runs/claude/00-plugin-discovery/PROMPT.md` |
| Subagents | not-tested | No live prompt 11 evidence yet | not-tested | No live prompt 11 evidence yet |
| Plugin hooks discovered | verified | `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl`; `dogfood/hooks/codex/observed-hooks.json` | verified | `dogfood/live-runs/claude/00-plugin-discovery/HOOK_EVENTS.json` |
| Plugin hooks trusted/enabled | verified for automation bypass | `dogfood/hooks/codex/CODEX_HOOK_STREAM_REDACTED.jsonl`; `dogfood/hooks/codex/observed-hooks.md` | verified | `dogfood/hooks/claude/observed-hooks.json` |
| Safe command allowed | verified | `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl` | verified | Discovery and OP Stack smoke safe commands allowed by policy guard |
| Unsafe command blocked | verified for Codex smoke | `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl` | not-tested | No live unsafe hook command was run |
| Artifact generation | verified for OP Stack smoke | `dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS/` | verified for OP Stack smoke | `dogfood/live-runs/claude/01-op-stack-public-testnet/GENERATED_ARTIFACTS/` |
| Artifact validation | verified for OP Stack smoke | `dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json` | verified for OP Stack smoke | `dogfood/live-runs/claude/01-op-stack-public-testnet/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json` |
| Clean install | verified | `release/evidence/v0.3.0-beta/clean-install-report.json` | verified for plugin package validation and discovery | `claude plugin validate` and `dogfood/live-runs/claude/00-plugin-discovery/` |
| Strict release evidence | blocked | Missing remaining prompt matrix and subagent evidence | blocked | Missing remaining prompt matrix and subagent evidence |

## Release Impact

Strict v0.3 remains not release-ready. The original Claude Code noninteractive `401 authentication_failed` blocker, the Claude OP Stack artifact smoke, and the Codex live hook observation are resolved for smoke scope. The next blockers are the remaining required prompt matrix and subagent evidence.

Do not create `v0.3.0-beta` until:

- the remaining required prompt matrix passes,
- live hook observations remain captured or formally classified for every required platform/scope,
- the required prompt matrix passes on both platforms,
- `make validate-v03` passes.
