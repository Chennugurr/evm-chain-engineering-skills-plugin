# CLAUDE-AUTH-401

## Classification

- Severity: blocker
- Status: open
- Release impact: blocks `v0.3.0-beta` strict release and tag creation
- Opened: 2026-06-25

## Summary

Claude Code plugin discovery works far enough to validate the plugin manifest and report plugin skills in the live-run init event, but noninteractive Claude agent execution fails with `401 authentication_failed`.

This is currently classified as an auth/session blocker, not a plugin-specific failure.

## Evidence

- Existing live-run package: `dogfood/live-runs/claude/01-op-stack-public-testnet/`
- Redacted stream: `dogfood/live-runs/claude/01-op-stack-public-testnet/CLAUDE_STREAM_REDACTED.jsonl`
- Triage doc: `docs/claude-auth-blocker-triage.md`

## Reproduction Summary

- `claude auth status`: reports logged in via first-party Claude auth, with account identifiers redacted from committed evidence.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict`: passes.
- `claude --print --verbose --output-format stream-json "Reply with the single word ok."`: fails with `401 authentication_failed`.
- The same login status is visible from a clean shell with `HOME`, `PATH`, and `SHELL` only.

## Required Resolution

Before strict v0.3 can continue:

1. Resolve Claude Code noninteractive authentication for this environment or switch to another authenticated environment.
2. Rerun Claude plugin discovery without `--bare`.
3. Rerun the Claude OP Stack smoke package and generate `GENERATED_ARTIFACTS/`.
4. Capture Claude hook evidence or a documented managed-settings/platform limitation.
5. Move this issue to `dogfood/issues/closed/CLAUDE-AUTH-401.md` with the successful evidence paths.
