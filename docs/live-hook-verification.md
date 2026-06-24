# Live Hook Verification

v0.3 keeps the existing plugin hook layout at `plugins/evm-chain-engineering-pro/hooks/hooks.json` and continues omitting a Codex manifest `hooks` field.

Strict validation requires each platform to provide either:

- a passing hook observation with evidence paths, or
- a documented `not-supported` platform limitation with evidence.

Bootstrap mode keeps `dogfood/hooks/*/observed-hooks.json` at `pending` and records release readiness as false.

## Strict Evidence Pass Status

- Codex smoke run: no explicit hook lifecycle event appeared in `dogfood/live-runs/codex/01-op-stack-public-testnet/CODEX_STREAM_REDACTED.jsonl`.
- Claude smoke run: invoked with `--include-hook-events`, but API authentication failed before hook execution.
- Release impact: hook verification remains pending and strict v0.3 is not release-ready.

## Official Docs Refreshed

Retrieval date: 2026-06-25

- Codex hooks, plugin build, config reference, advanced config, skills, and subagents docs were refreshed from `developers.openai.com` and the current Codex manual helper before strict evidence capture.
- Claude hooks reference, hooks guide, plugins, plugin reference, skills, subagents, and settings docs were refreshed from `code.claude.com`.
- Live hook support still requires observed platform evidence; docs freshness alone is not hook verification.
