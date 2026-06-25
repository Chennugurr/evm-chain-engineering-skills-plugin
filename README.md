# EVM Chain Engineering Pro

## What this plugin is

This repository packages `evm-chain-engineering-pro`, a dual Codex and Claude Code plugin for planning and reviewing EVM chain engineering work.

It is meant for architecture, safety review, dry-run planning, artifact generation, and workflow acceptance around EVM L1s, L2s, L3s, appchains, rollups, bridges, explorers, faucets, and infrastructure.

## What it is not

- It is not an automatic chain deployer.
- It does not manage or store real secrets.
- It does not approve mainnet actions.
- It does not replace current vendor docs, human review, or professional audits.
- It does not make different chain stacks interchangeable.

## What Is Included

- `plugins/evm-chain-engineering-pro/`: the installable plugin bundle.
- `.agents/plugins/marketplace.json`: local Codex marketplace entry.
- `.claude-plugin/marketplace.json`: local Claude Code marketplace entry.
- `plugins/evm-chain-engineering-pro/skills/`: 14 portable skills shared by both agent surfaces.
- `plugins/evm-chain-engineering-pro/references/`: stack notes, safety guidance, and planning references.
- `plugins/evm-chain-engineering-pro/scripts/`: safe plugin-local helper commands.
- `scripts/`: root validation, artifact, release evidence, policy, and dogfood tooling.
- `profiles/`, `schemas/`, `fixtures/`, `acceptance/`, and `dogfood/`: machine-checkable contracts and test evidence.

## Contributors

- [Chennugurr](https://github.com/Chennugurr)

## Supported workflows

- Choosing between OP Stack, Arbitrum Orbit, Polygon CDK, ZKsync ZK Stack, EVM L1, Cosmos EVM, and modular rollup paths.
- Drafting chain specs, infrastructure plans, launch gates, security review templates, and runbooks.
- Reviewing bridge, admin, sequencer, prover, data availability, explorer, faucet, and observability assumptions.
- Running offline validation against checked-in schemas, fixtures, acceptance cases, and safety policies.
- Dogfooding Codex and Claude skill routing with deterministic prompts and redacted transcript evidence.

## Install In Codex

The Codex marketplace file is already checked in at `.agents/plugins/marketplace.json`.

From this repository root, validate the plugin metadata:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/evm-chain-engineering-pro
```

Then restart Codex or refresh local plugins and install `evm-chain-engineering-pro` from the `evm-chain-engineering` marketplace.

## Install In Claude Code

The Claude marketplace file is checked in at `.claude-plugin/marketplace.json`.

Validate the local plugin:

```bash
claude plugin validate plugins/evm-chain-engineering-pro --strict
```

Then add or install the plugin from the local marketplace path, depending on your Claude Code plugin setup.

## Use The Skills

After installation, ask normally. Codex and Claude can route to the relevant skills by topic, or you can name a skill explicitly in your prompt.

Example prompts:

```text
Use blockchain-architect and chain-security-reviewer to compare OP Stack and Arbitrum Orbit for a public testnet.
```

```text
Use bridge-interop-engineer to review the trust assumptions for this bridge plan, then hand off to chain-security-reviewer.
```

```text
Use chain-launch-manager to produce launch gates for a dry-run testnet only.
```

Available skills:

- `blockchain-architect`
- `evm-l1-builder`
- `op-stack-engineer`
- `arbitrum-orbit-engineer`
- `polygon-cdk-engineer`
- `zksync-zk-stack-engineer`
- `modular-rollup-engineer`
- `data-availability-engineer`
- `bridge-interop-engineer`
- `chain-infra-ops`
- `observability-sre`
- `chain-security-reviewer`
- `chain-launch-manager`
- `explorer-indexer-engineer`

For production, mainnet, bridge, admin, sequencer, or prover paths, include `chain-security-reviewer` in the workflow.

## Release validation

Run the standard validation gate before sharing changes:

```bash
make validate
```

Run the v0.2 workflow acceptance layer:

```bash
make validate-v02
```

Run the v0.3 live QA evidence gate:

```bash
make validate-v03
```

Render and validate a planning artifact bundle:

```bash
python3 scripts/render_artifact_bundle.py --workflow op-stack-public-testnet --stack op-stack --chain-type l2 --environment public-testnet --settlement sepolia --output generated/op-stack-public-testnet --overwrite
python3 scripts/validate_artifact_bundle.py --strict --path generated/op-stack-public-testnet
```

Scan for unsafe output patterns:

```bash
python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs --strict
```

Build release evidence:

```bash
python3 scripts/build_release_evidence.py --version v0.3.0-beta --strict
```

## Dogfood workflow

Dogfood prompts and live-run evidence live under `dogfood/`. Use them to check whether Codex and Claude route to the expected skills, refuse unsafe requests, and produce artifact-shaped planning output without using real secrets or live deployment commands.

## Behavior evals

Behavior evals check expected and forbidden skill routing against `evals/skill-trigger-matrix.yaml`:

```bash
python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict
```

## Golden demos

Golden demos live under `examples/golden-demos/`. Each demo gives a safe prompt, expected skills, expected output shape, validation notes, and security review expectations for repeatable plugin QA.

## Safety model

- Keep all outputs planning-only unless a human operator explicitly moves them into a separate deployment process.
- Do not put real private keys, mnemonics, API keys, RPC credentials, or `.env` files in this repository.
- Treat exact stack commands, client versions, bridge procedures, and production launch steps as version-sensitive.
- Use `VERIFY_CURRENT_DOCS` guidance before any production-like action.
- Do not create `.agent-approvals/mainnet-action-approved.json` unless a separate human approval process requires it.

## Development Notes

Root-level scripts are for repository validation and release hardening. Plugin-local scripts under `plugins/evm-chain-engineering-pro/scripts/` are the portable helpers shipped with the plugin.

Generated local outputs belong under `generated/` and should not be committed unless they are intentional fixtures or release evidence.

The current beta evidence is planning-only. The `v0.3.0-beta` tag records live Codex and Claude smoke coverage, hook observations, and release evidence for this repository; it is not a production deployment certification.
