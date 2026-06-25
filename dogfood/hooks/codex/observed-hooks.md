# Codex Hook Observation

Status: pass

Observation date: 2026-06-25

Installed plugin: `evm-chain-engineering-pro@evm-chain-engineering`

Installed version: `0.1.0+codex.v03-codex-hook-enforce-20260625`

Codex CLI: `codex-cli 0.142.0-alpha.6`

## Result

Codex discovered the plugin-bundled hook manifest at `plugins/evm-chain-engineering-pro/hooks/hooks.json` and emitted `PreToolUse:Bash` decisions during a nested live smoke run.

Observed decisions:

- Safe help command: allowed and executed.
- Fake secret write sentinel: denied by `secret-output` and `unsafe-env`; sentinel file remained absent.
- Mainnet-like broadcast: denied by `mainnet-broadcast`; no deploy/network command executed.
- Final sentinel absence check: allowed and executed.

Evidence:

- `dogfood/hooks/codex/CODEX_HOOK_STREAM_REDACTED.jsonl`
- `dogfood/hooks/codex/HOOK_POLICY_DECISIONS.jsonl`
- `dogfood/hooks/codex/observed-hooks.json`

## Trust State

The smoke run used `--dangerously-bypass-hook-trust` for noninteractive automation. The evidence records the corresponding Codex startup warnings. This proves the hook source was vetted for the run, but it does not claim persisted interactive `/hooks` trust.

## Portability

The hook command uses plugin-root environment variables when present and a repo-relative fallback for local marketplace development:

```txt
python3 "${PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-plugins/evm-chain-engineering-pro}}/scripts/policy_guard.py" --stdin --json --strict --hook-output
```

No absolute `<HOME>` path is required in the hook manifest or committed evidence.

## Fixes Applied During Closure

- Removed unsupported top-level metadata from `hooks/hooks.json`; policy metadata now lives in `hooks/policy-metadata.json`.
- Changed the PreToolUse matcher to `*` so Codex can match supported hook tool names consistently.
- Made `policy_guard.py` hook output return explicit Codex `permissionDecision` JSON with exit `0`, while keeping strict nonzero exits for normal CLI scans.
- Made the plugin-local policy guard self-contained for installed plugin cache execution.
