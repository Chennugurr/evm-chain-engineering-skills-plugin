# Live Hook Verification

v0.3 keeps the existing plugin hook layout at `plugins/evm-chain-engineering-pro/hooks/hooks.json` and continues omitting a Codex manifest `hooks` field.

Strict validation requires each platform to provide either:

- a passing hook observation with evidence paths, or
- a documented `not-supported` platform limitation with evidence.

Bootstrap mode keeps `dogfood/hooks/*/observed-hooks.json` at `pending` and records release readiness as false.

## Strict Evidence Pass Status

- Codex smoke run: no explicit hook lifecycle event appeared in `dogfood/live-runs/codex/01-op-stack-public-testnet/CODEX_STREAM_REDACTED.jsonl`.
- Claude discovery run: `dogfood/live-runs/claude/00-plugin-discovery/CLAUDE_STREAM_REDACTED.jsonl` recorded `PreToolUse:Bash` hook lifecycle events and policy guard allow decisions.
- Claude OP Stack artifact run: `dogfood/live-runs/claude/01-op-stack-public-testnet/CLAUDE_STREAM_REDACTED.jsonl` recorded `PreToolUse:Bash` hook lifecycle events and policy guard allow decisions.
- Claude central observation file: `dogfood/hooks/claude/observed-hooks.json` is now `pass`.
- Codex central observation file: `dogfood/hooks/codex/observed-hooks.json` remains `pending`.
- Release impact: strict v0.3 is not release-ready until Codex hook evidence or a documented platform limitation is captured.

## Official Docs Refreshed

Retrieval date: 2026-06-25

- Codex hooks, plugin build, config reference, advanced config, skills, and subagents docs were refreshed from `developers.openai.com` and the current Codex manual helper before strict evidence capture.
- Claude hooks reference, hooks guide, plugins, plugin reference, skills, subagents, and settings docs were refreshed from `code.claude.com`.
- Live hook support still requires observed platform evidence; docs freshness alone is not hook verification.
