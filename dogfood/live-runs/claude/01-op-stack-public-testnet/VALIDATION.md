# Claude Smoke Validation

## Commands And Results

- `claude plugin validate plugins/evm-chain-engineering-pro --strict`
  - Result: pass.
- `claude --print --verbose --output-format stream-json --include-hook-events --plugin-dir plugins/evm-chain-engineering-pro --permission-mode acceptEdits --max-budget-usd 0.80 < PROMPT.md`
  - Result: pass.
- `python3 scripts/validate_artifact_bundle.py --strict --path dogfood/live-runs/claude/01-op-stack-public-testnet/GENERATED_ARTIFACTS`
  - Result: pass, zero findings.
- `python3 scripts/validate_generated_configs.py --strict --path dogfood/live-runs/claude/01-op-stack-public-testnet/GENERATED_ARTIFACTS`
  - Result: pass, zero findings.
- `python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs/claude/01-op-stack-public-testnet/GENERATED_ARTIFACTS --strict`
  - Result: pass, zero findings.
- `python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path dogfood/live-runs/claude/01-op-stack-public-testnet/GENERATED_ARTIFACTS --strict --json`
  - Result: pass, zero findings.

## Evidence Files

- `CLAUDE_STREAM_REDACTED.jsonl`
- `GENERATED_ARTIFACTS/`
- `GENERATED_ARTIFACTS/evidence/artifact-validation-report.json`
- `GENERATED_ARTIFACTS/evidence/generated-config-validation-report.json`
- `GENERATED_ARTIFACTS/evidence/bad-output-patterns-report.json`

## Remaining Blockers

- The remaining required strict prompt matrix still needs live evidence on Codex and Claude.
- Codex live hook observations and subagent dogfood evidence remain pending.
