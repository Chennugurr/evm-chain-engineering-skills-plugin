# Platform Compatibility Matrix

Generated from v0.3 local evidence on 2026-06-25.

Allowed statuses: `verified`, `blocked`, `not-supported`, `not-tested`, `partial`.

Official platform docs were refreshed on 2026-06-25. Docs freshness is not release evidence; every row below is tied to committed local evidence.

| Capability | Codex Status | Codex Evidence | Claude Status | Claude Evidence |
|---|---|---|---|---|
| Plugin install | verified | `codex plugin add evm-chain-engineering-pro@evm-chain-engineering`; `dogfood/live-runs/codex/01-op-stack-public-testnet/MANUAL_NOTES.md` | verified | `claude plugin validate plugins/evm-chain-engineering-pro --strict`; `dogfood/live-runs/claude/00-plugin-discovery/MANUAL_NOTES.md` |
| Skill discovery | verified | `dogfood/live-runs/codex/01-op-stack-public-testnet/CODEX_STREAM_REDACTED.jsonl` | verified | `dogfood/live-runs/claude/00-plugin-discovery/CLAUDE_STREAM_REDACTED.jsonl` |
| Direct skill invocation | not-tested | Not captured in Codex CLI matrix | verified | `dogfood/live-runs/claude/00-plugin-discovery/SKILL_OBSERVATIONS.md` |
| Automatic skill triggering | verified | Required prompts `01`, `02`, `03`, `05`, `06`, and `07` captured under `dogfood/live-runs/codex/` | verified | Required prompts `01`, `02`, `03`, `05`, `06`, and `07` captured under `dogfood/live-runs/claude/` |
| Command prompt files | verified | Prompt captures under `dogfood/live-runs/codex/*/PROMPT.md` | verified | Prompt captures under `dogfood/live-runs/claude/*/PROMPT.md` |
| Subagents | partial | No live subagent execution claimed; limitation recorded in `dogfood/reports/subagent-dogfood-limitation.md` | partial | No live subagent execution claimed; limitation recorded in `dogfood/reports/subagent-dogfood-limitation.md` |
| Plugin hooks discovered | verified | `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl`; `dogfood/hooks/codex/observed-hooks.json` | verified | `dogfood/live-runs/claude/00-plugin-discovery/HOOK_EVENTS.json` |
| Plugin hooks trusted/enabled | verified for noninteractive automation bypass only; persistent interactive `/hooks` trust is not claimed | `dogfood/hooks/codex/CODEX_HOOK_STREAM_REDACTED.jsonl`; `dogfood/hooks/codex/observed-hooks.md` | verified | `dogfood/hooks/claude/observed-hooks.json` |
| Safe command allowed | verified | `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl` | verified | Discovery and OP Stack smoke safe commands allowed by policy guard |
| Unsafe command blocked | verified for Codex smoke | `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl` | not-tested | No live unsafe hook command was run |
| Artifact generation | verified for required artifact prompts | `dogfood/live-runs/codex/{01,02,03,05}-*/GENERATED_ARTIFACTS/` | verified for required artifact prompts | `dogfood/live-runs/claude/{01,02,03,05}-*/GENERATED_ARTIFACTS/` |
| Artifact validation | verified for required artifact prompts | `dogfood/live-runs/codex/*/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json` | verified for required artifact prompts | `dogfood/live-runs/claude/*/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json` |
| Clean install | verified | `release/evidence/v0.3.0-beta/clean-install-report.json` | verified for plugin package validation and discovery | `claude plugin validate` and `dogfood/live-runs/claude/00-plugin-discovery/` |
| Strict release evidence | verified | `make validate-v03`; `release/evidence/v0.3.0-beta/summary.json` reports `release_ready: true` | verified | `make validate-v03`; `release/evidence/v0.3.0-beta/summary.json` reports `release_ready: true` |

## Release Impact

The original Claude Code noninteractive `401 authentication_failed` blocker, the Claude OP Stack artifact smoke, the Codex live hook observation, and the required prompt matrix are resolved for the v0.3.0-beta closure scope.

`v0.3.0-beta` may be created when:

- `make validate-v03` passes,
- release evidence reports `release_ready: true`,
- the subagent limitation remains explicit unless real prompt 11 evidence is captured,
- no blocker appears in the release evidence or dogfood issue reports.
