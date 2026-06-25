# Validation

## Commands And Results

- `/usr/bin/python3 scripts/render_artifact_bundle.py --workflow evm-l1-posa-testnet --stack bnb-style-posa --chain-type l1 --environment public-testnet --settlement native-l1 --data-availability native-chain --proof-model validator-consensus --chain-name Example EVM L1 PoSA Testnet --output /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS --overwrite --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/artifact-render-report.json`
  - Result: pass
- `/usr/bin/python3 scripts/validate_artifact_bundle.py --strict --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json`
  - Result: pass
- `/usr/bin/python3 scripts/validate_generated_configs.py --strict --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS/evidence/generated-config-validation-report.json`
  - Result: pass
- `/usr/bin/python3 scripts/check_bad_output_patterns.py --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS --strict --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS/evidence/bad-output-patterns-report.json`
  - Result: pass
- `/usr/bin/python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/05-evm-l1-validator-network/GENERATED_ARTIFACTS --strict --json`
  - Result: pass

## Remaining Blockers

- None for this prompt package.
