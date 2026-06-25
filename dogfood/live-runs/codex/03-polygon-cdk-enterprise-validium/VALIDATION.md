# Validation

## Commands And Results

- `/usr/bin/python3 scripts/render_artifact_bundle.py --workflow polygon-cdk-validium-enterprise --stack polygon-cdk --chain-type validium --environment public-testnet --settlement ethereum-testnet-or-agglayer --data-availability offchain-da-committee --proof-model validity-proof --chain-name Example CDK Enterprise Validium --output /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS --overwrite --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/artifact-render-report.json`
  - Result: pass
- `/usr/bin/python3 scripts/validate_artifact_bundle.py --strict --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS/evidence/artifact-validation-report.json`
  - Result: pass
- `/usr/bin/python3 scripts/validate_generated_configs.py --strict --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS/evidence/generated-config-validation-report.json`
  - Result: pass
- `/usr/bin/python3 scripts/check_bad_output_patterns.py --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS --strict --json-out /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS/evidence/bad-output-patterns-report.json`
  - Result: pass
- `/usr/bin/python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path /home/iljanemesis/blockchain-engineering/dogfood/live-runs/codex/03-polygon-cdk-enterprise-validium/GENERATED_ARTIFACTS --strict --json`
  - Result: pass

## Remaining Blockers

- None for this prompt package.
