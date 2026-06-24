# Claude Smoke Validation

## Commands And Results

- `claude plugin validate plugins/evm-chain-engineering-pro --strict`
  - Result: pass
- `claude --print --verbose --output-format stream-json --include-hook-events --plugin-dir plugins/evm-chain-engineering-pro ...`
  - Result: fail, `401 authentication_failed`

## Evidence Files

- `CLAUDE_STREAM_REDACTED.jsonl`

## Remaining Blockers

- Authenticated Claude Code live session required.
- Claude artifact generation, transcript validation, hook observation, and skill-routing evidence remain pending.
