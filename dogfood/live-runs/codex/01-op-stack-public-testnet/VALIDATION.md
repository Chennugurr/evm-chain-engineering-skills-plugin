# Codex Smoke Validation

## Commands And Results

- `python3 scripts/render_artifact_bundle.py --workflow op-stack-public-testnet --stack op-stack --chain-type l2 --environment public-testnet --settlement sepolia --data-availability ethereum-blobs --chain-name smoke-op-stack-public-testnet --output dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS --overwrite --json-out dogfood/live-runs/codex/01-op-stack-public-testnet/artifact-render-report.json`
  - Result: pass
- `python3 scripts/validate_artifact_bundle.py --strict --path dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS`
  - Result: pass
- `python3 scripts/validate_generated_configs.py --strict --path dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS`
  - Result: pass
- `python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS --strict`
  - Result: pass
- `python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS --strict --json`
  - Result: pass

## Evidence Files

- `GENERATED_ARTIFACTS/evidence/artifact-validation-report.json`
- `GENERATED_ARTIFACTS/evidence/generated-config-validation-report.json`
- `GENERATED_ARTIFACTS/evidence/bad-output-patterns-report.json`
- `artifact-render-report.json`

## Remaining Blockers

- Full strict v0.3 remains blocked until all required prompts are captured on both Codex and Claude and live hook observation is resolved.
