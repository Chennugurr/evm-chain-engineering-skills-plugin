# Claude Discovery Validation

## Commands And Results

- `claude auth status`
  - Result: pass, account identifiers redacted from committed evidence.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict`
  - Result: pass.
- `claude --print --verbose --output-format stream-json --max-budget-usd 0.05 'Reply with the single word ok.'`
  - Result: partial. The assistant returned `ok`; the command ended with a budget-cap error, not an auth error.
- `claude --print --verbose --output-format stream-json --include-hook-events --plugin-dir plugins/evm-chain-engineering-pro --permission-mode acceptEdits --allowedTools Read --max-budget-usd 0.40 ...`
  - Result: pass.

## Evidence Files

- `CLAUDE_STREAM_REDACTED.jsonl`
- `HOOK_EVENTS.json`
- `POLICY_EVENTS.json`

## Remaining Blockers

- Claude `01-op-stack-public-testnet` still needs to be rerun to generate and validate artifacts.
- Strict v0.3 still needs the remaining required prompt matrix on Codex and Claude.
