# Live Hook Verification

v0.3 keeps the existing plugin hook layout at `plugins/evm-chain-engineering-pro/hooks/hooks.json` and continues omitting a Codex manifest `hooks` field.

Strict validation requires each platform to provide either:

- a passing hook observation with evidence paths, or
- a documented `not-supported` platform limitation with evidence.

Bootstrap mode keeps `dogfood/hooks/*/observed-hooks.json` at `pending` and records release readiness as false.

## Strict Evidence Pass Status

- Codex hook closure run: `dogfood/hooks/codex/CODEX_HOOK_STREAM_REDACTED.jsonl` and `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl` recorded `PreToolUse:Bash` allow and deny decisions.
- Codex central observation file: `dogfood/hooks/codex/observed-hooks.json` is now `pass`.
- Claude discovery run: `dogfood/live-runs/claude/00-plugin-discovery/CLAUDE_STREAM_REDACTED.jsonl` recorded `PreToolUse:Bash` hook lifecycle events and policy guard allow decisions.
- Claude OP Stack artifact run: `dogfood/live-runs/claude/01-op-stack-public-testnet/CLAUDE_STREAM_REDACTED.jsonl` recorded `PreToolUse:Bash` hook lifecycle events and policy guard allow decisions.
- Claude central observation file: `dogfood/hooks/claude/observed-hooks.json` is now `pass`.
- Release impact: the live hook observation blocker is resolved for smoke scope. Strict v0.3 remains not release-ready until the remaining prompt matrix and subagent evidence pass.

## Codex Hook Closure Notes

- Codex plugin installed/enabled version observed: `0.1.0+codex.v03-codex-hook-enforce-20260625`.
- Trust state: noninteractive automation used `--dangerously-bypass-hook-trust`; no persisted `/hooks` trust is claimed.
- Safe command allowed: `python3 scripts/validate_live_hook_observations.py --help`.
- Fake secret sentinel write blocked: `secret-output` and `unsafe-env`.
- Mainnet-like broadcast blocked: `mainnet-broadcast`.
- Hook command is portable and contains no absolute `<HOME>` dependency.

## Official Docs Refreshed

Retrieval date: 2026-06-25

- Codex hooks, plugin build, config reference, advanced config, skills, and subagents docs were refreshed from `developers.openai.com` and the current Codex manual helper before strict evidence capture.
- Claude hooks reference, hooks guide, plugins, plugin reference, skills, subagents, and settings docs were refreshed from `code.claude.com`.
- Live hook support still requires observed platform evidence; docs freshness alone is not hook verification.
