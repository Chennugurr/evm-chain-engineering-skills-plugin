# CLAUDE-AUTH-401

## Classification

- Severity: blocker while open
- Status: resolved for discovery
- Opened: 2026-06-25
- Resolved: 2026-06-25
- Release impact: no longer the first blocker for Claude plugin discovery or the OP Stack smoke run; strict `v0.3.0-beta` remains blocked by the remaining live prompt matrix and Codex hook evidence

## Summary

Claude Code noninteractive execution previously returned `401 authentication_failed` even though `claude auth status` reported logged in and `claude plugin validate plugins/evm-chain-engineering-pro --strict` passed.

A later retry proved noninteractive Claude execution, local plugin discovery, hook observation, and the `01-op-stack-public-testnet` Claude artifact smoke run now work. The old auth-only blocker is closed.

## Resolution Evidence

- Discovery package: `dogfood/live-runs/claude/00-plugin-discovery/`
- OP Stack smoke package: `dogfood/live-runs/claude/01-op-stack-public-testnet/`
- Redacted event stream: `dogfood/live-runs/claude/00-plugin-discovery/CLAUDE_STREAM_REDACTED.jsonl`
- Hook evidence: `dogfood/live-runs/claude/00-plugin-discovery/HOOK_EVENTS.json`
- Triage doc: `docs/claude-auth-blocker-triage.md`

## Resolution Summary

- `claude auth status`: reports logged in, with account identifiers redacted from committed evidence.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict`: passes.
- No-plugin `claude --print` smoke: returned assistant text `ok`; the command ended as an error only because the budget cap was too low.
- Plugin discovery: passed with `--plugin-dir plugins/evm-chain-engineering-pro` and without `--bare`.
- Skill discovery: 14 plugin skills visible.
- Direct skill invocation: `evm-chain-engineering-pro:blockchain-architect`.
- Hook observation: `PreToolUse:Bash` lifecycle events were recorded and allowed by policy guard.

## Remaining Work

1. Continue the remaining six-prompt strict matrix for Codex and Claude.
2. Capture Codex live hook evidence or a documented platform limitation.
3. Capture subagent dogfood evidence.
4. Run `make validate-v03` and create `v0.3.0-beta` only if it passes.
