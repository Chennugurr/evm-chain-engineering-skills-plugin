# Platform Compatibility Matrix

Generated from v0.3 local evidence on 2026-06-25.

Allowed statuses: `verified`, `blocked`, `not-supported`, `not-tested`, `partial`.

Official platform docs were refreshed on 2026-06-25. Docs freshness is not release evidence; every row below is tied to committed local evidence.

| Capability | Codex Status | Codex Evidence | Claude Status | Claude Evidence |
|---|---|---|---|---|
| Plugin install | verified | `codex plugin add evm-chain-engineering-pro@evm-chain-engineering`; `dogfood/live-runs/codex/01-op-stack-public-testnet/MANUAL_NOTES.md` | partial | `claude plugin validate plugins/evm-chain-engineering-pro --strict`; `dogfood/live-runs/claude/01-op-stack-public-testnet/MANUAL_NOTES.md` |
| Skill discovery | verified | `dogfood/live-runs/codex/01-op-stack-public-testnet/CODEX_STREAM_REDACTED.jsonl` | partial | `dogfood/live-runs/claude/01-op-stack-public-testnet/CLAUDE_STREAM_REDACTED.jsonl` |
| Direct skill invocation | not-tested | Not captured yet | blocked | `docs/claude-auth-blocker-triage.md` |
| Automatic skill triggering | partial | OP Stack smoke skill selection in `dogfood/live-runs/codex/01-op-stack-public-testnet/SKILL_OBSERVATIONS.md` | blocked | `dogfood/issues/open/CLAUDE-AUTH-401.md` |
| Command prompt files | partial | `commands/`; smoke prompt captured in `dogfood/live-runs/codex/01-op-stack-public-testnet/PROMPT.md` | blocked | `dogfood/live-runs/claude/01-op-stack-public-testnet/PROMPT.md` plus auth blocker |
| Subagents | not-tested | No live prompt 11 evidence yet | blocked | `docs/claude-auth-blocker-triage.md` |
| Plugin hooks discovered | not-tested | No explicit hook lifecycle event in Codex smoke stream | blocked | `dogfood/live-runs/claude/01-op-stack-public-testnet/HOOK_EVENTS.json` |
| Plugin hooks trusted/enabled | not-tested | `dogfood/hooks/codex/observed-hooks.json` remains pending | blocked | Auth fails before hook execution; no managed-settings blocker found |
| Safe command allowed | not-tested | Hook fixture tests pass, but live hook observation pending | blocked | Auth fails before live hook test |
| Unsafe command blocked | not-tested | Hook fixture tests pass, but live hook observation pending | blocked | Auth fails before live hook test |
| Artifact generation | verified for OP Stack smoke | `dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS/` | blocked | No Claude artifacts generated because of `401 authentication_failed` |
| Artifact validation | verified for OP Stack smoke | `dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json` | blocked | `dogfood/live-runs/claude/01-op-stack-public-testnet/VALIDATION.json` |
| Clean install | verified | `release/evidence/v0.3.0-beta/clean-install-report.json` | verified for plugin package validation only | `claude plugin validate` passed; live Claude execution blocked |
| Strict release evidence | blocked | Missing full prompt matrix and live hook observations | blocked | `dogfood/issues/open/CLAUDE-AUTH-401.md` |

## Release Impact

Strict v0.3 remains not release-ready. The current first blocker is Claude Code noninteractive execution returning `401 authentication_failed` despite redacted auth status reporting logged in.

Do not create `v0.3.0-beta` until:

- `dogfood/issues/open/CLAUDE-AUTH-401.md` is moved to closed with evidence,
- Claude `00-plugin-discovery` and `01-op-stack-public-testnet` packages pass,
- live hook observations are captured for Codex and Claude or formally classified as release-blocking limitations,
- the required prompt matrix passes on both platforms,
- `make validate-v03` passes.
