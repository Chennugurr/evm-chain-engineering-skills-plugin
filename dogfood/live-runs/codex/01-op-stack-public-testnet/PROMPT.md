# Codex Smoke Prompt

You are running the v0.3.0-beta strict live evidence smoke test for the installed Codex plugin evm-chain-engineering-pro.

Use the installed plugin skills if they are available for this task. If the platform does not expose skill telemetry, state the selected skills in your final answer as observed-by-output/inferred, not as hidden telemetry.

Work only inside dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS for generated planning artifacts. Do not deploy, broadcast transactions, publish, create real secrets, write the production-network approval marker, edit plugin manifests, or touch unrelated files.

Create a safe planning-only artifact bundle for the following checked-in dogfood prompt by using the repository tooling where appropriate. A suitable command is:

python3 scripts/render_artifact_bundle.py --workflow op-stack-public-testnet --stack op-stack --chain-type l2 --environment public-testnet --settlement sepolia --data-availability ethereum-blobs --chain-name smoke-op-stack-public-testnet --output dogfood/live-runs/codex/01-op-stack-public-testnet/GENERATED_ARTIFACTS --overwrite --json-out dogfood/live-runs/codex/01-op-stack-public-testnet/artifact-render-report.json

Then run strict validation for that generated bundle if possible and include a concise final summary with selected skills, validation commands/results, security stance, and limitations.

Checked-in prompt:

# 01 OP Stack Public Testnet

## Objective

Use the installed EVM Chain Engineering Pro plugin to design a safe OP Stack public testnet plan for an internal team.

## Stack or Task

Plan a public testnet L2 using OP Stack with Ethereum Sepolia settlement, a separated sequencer, batcher, proposer, RPC, explorer, and monitoring roles.

## Safety

Do not deploy, broadcast, publish, create secrets, or write approval markers. Use dry-run language and require human security review before production-like actions.

## Required Output

Produce an artifact bundle or equivalent structured answer with an architecture decision record, chain spec, infrastructure plan, security review, launch gates, selected skills, and validation notes.
