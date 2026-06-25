# Validation

## Commands And Results

- `python3 scripts/render_artifact_bundle.py --workflow arbitrum-orbit-l3-anytrust --stack arbitrum-orbit --chain-type l3 --environment public-testnet --settlement arbitrum-style-l2-parent --data-availability anytrust-dac --proof-model anytrust --chain-name 'Example Orbit L3 AnyTrust' --output dogfood/live-runs/codex/02-arbitrum-orbit-l3-anytrust/GENERATED_ARTIFACTS --overwrite --json-out dogfood/live-runs/codex/02-arbitrum-orbit-l3-anytrust/artifact-render-report.json`
  - Result: pass
- `python3 scripts/validate_artifact_bundle.py --strict --path dogfood/live-runs/codex/02-arbitrum-orbit-l3-anytrust/GENERATED_ARTIFACTS`
  - Result: pass
- `python3 scripts/validate_generated_configs.py --strict --path dogfood/live-runs/codex/02-arbitrum-orbit-l3-anytrust/GENERATED_ARTIFACTS`
  - Result: pass
- `python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs/codex/02-arbitrum-orbit-l3-anytrust/GENERATED_ARTIFACTS --strict`
  - Result: pass
- `python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path dogfood/live-runs/codex/02-arbitrum-orbit-l3-anytrust/GENERATED_ARTIFACTS --strict --json`
  - Result: pass

## Remaining Blockers

- None for this prompt package.
