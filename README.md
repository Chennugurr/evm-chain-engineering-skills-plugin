# EVM Chain Engineering Pro

## What this plugin is

This repo is a local plugin for Codex and Claude Code called `evm-chain-engineering-pro`.

It gives an agent a set of EVM chain engineering skills: stack selection, rollup planning, L1 design, bridge review, data availability review, infrastructure planning, launch gates, observability, explorer/indexer planning, and security handoff.

Use it when you want an agent to help think through a chain design before anyone touches real infrastructure. The useful output is a clearer plan: what stack fits, what assumptions are risky, what needs current docs, what should be reviewed by a human, and what artifacts should exist before a testnet or launch process moves forward.

## What it is not

This is not a deploy button. It does not run mainnet launches, hold private keys, manage RPC credentials, publish contracts, or make a stack safe just because it produced a checklist.

It is also not a replacement for current stack documentation or an audit. The chain ecosystem moves quickly; use this plugin to structure the work, then verify the exact commands, versions, and production choices against current upstream docs and human reviewers.

## What Is Included

- `plugins/evm-chain-engineering-pro/`: the plugin that Codex and Claude install.
- `.agents/plugins/marketplace.json`: the local Codex marketplace entry.
- `.claude-plugin/marketplace.json`: the local Claude Code marketplace entry.
- `plugins/evm-chain-engineering-pro/skills/`: the 14 skills this plugin adds.
- `plugins/evm-chain-engineering-pro/references/`: supporting notes the skills can use.
- `plugins/evm-chain-engineering-pro/scripts/`: small safe helper scripts shipped with the plugin.
- `scripts/`, `schemas/`, `profiles/`, `fixtures/`, `acceptance/`, and `dogfood/`: maintainer tooling for checking that the plugin behaves the way the repo says it should.

## Contributors

- [Chennugurr](https://github.com/Chennugurr)

## Supported workflows

The plugin is built for planning and review work like:

- choosing between OP Stack, Arbitrum Orbit, Polygon CDK, ZKsync ZK Stack, EVM L1, Cosmos EVM, and modular rollup designs;
- writing chain specs, ADRs, infrastructure plans, launch gates, and runbooks;
- reviewing bridge, admin, sequencer, prover, DA, explorer, faucet, and observability assumptions;
- checking that generated plans stay dry-run, redacted, and review-friendly;
- routing risky work through the security reviewer skill before it looks actionable.

## Install In Codex

From the repo root, validate the plugin first:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/evm-chain-engineering-pro
```

Then refresh Codex plugins and install `evm-chain-engineering-pro` from the local `evm-chain-engineering` marketplace.

## Install In Claude Code

Validate the plugin with Claude Code:

```bash
claude plugin validate plugins/evm-chain-engineering-pro --strict
```

Then install or add the plugin using the local marketplace file at `.claude-plugin/marketplace.json`.

## Use The Skills

Once the plugin is installed, you can just ask for the work you want. The agent should route to the right skill from the topic.

For more control, name the skills directly:

```text
Use blockchain-architect to compare OP Stack and Arbitrum Orbit for a public testnet.
```

```text
Use bridge-interop-engineer and chain-security-reviewer to review this bridge plan.
```

```text
Use chain-launch-manager to draft dry-run launch gates for a testnet.
```

The plugin includes these skills:

- `blockchain-architect`: stack selection, ADRs, trust assumptions, and chain design tradeoffs.
- `evm-l1-builder`: EVM L1 and appchain planning.
- `op-stack-engineer`: OP Stack planning and review.
- `arbitrum-orbit-engineer`: Arbitrum Orbit and L3 planning.
- `polygon-cdk-engineer`: Polygon CDK planning.
- `zksync-zk-stack-engineer`: ZKsync ZK Stack planning.
- `modular-rollup-engineer`: modular rollup and sovereign rollup planning.
- `data-availability-engineer`: DA selection and risk review.
- `bridge-interop-engineer`: bridge, relayer, token mapping, and cross-chain assumptions.
- `chain-infra-ops`: servers, networking, systemd, Kubernetes, Terraform, and runbooks.
- `observability-sre`: metrics, logs, alerts, dashboards, and incident readiness.
- `chain-security-reviewer`: threat modeling, unsafe-pattern review, admin-risk review, and security handoff.
- `chain-launch-manager`: launch gates, testnet phases, release readiness, and post-launch operations.
- `explorer-indexer-engineer`: explorer, indexer, faucet, and public metadata planning.

If the request mentions production, mainnet, bridges, admins, sequencers, provers, or real operators, include `chain-security-reviewer`. That is the skill that slows the answer down in the places where slow is useful.

## Safety model

Treat this plugin like a careful planning partner, not an operator with keys.

Good uses are questions like "what are we missing?", "which stack fits this constraint?", "what should the launch gates be?", and "where are the trust assumptions?" Bad uses are requests to paste secrets, bypass review, broadcast transactions, or turn a draft into a real deployment.

Keep real credentials out of the repo. Keep live deployment work in a separate, human-controlled process. When the answer depends on exact versions, bridge instructions, production settings, or mainnet procedures, verify the current upstream docs before using the plan.

## Release validation

For normal repo changes, run:

```bash
make validate
```

For the full workflow acceptance and live QA checks, maintainers can also run:

```bash
make validate-v02
make validate-v03
```

## Dogfood workflow

`dogfood/` contains prompts and redacted live-run notes used to check whether Codex and Claude actually use the right skills. Most users can ignore it; it is here so maintainers can prove the plugin still behaves like the README claims.

## Behavior evals

Behavior evals check skill routing from fixed prompts:

```bash
python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict
```

## Golden demos

`examples/golden-demos/` contains safe example prompts and expected outputs. They are useful when changing a skill and wanting a quick feel for the shape of a good answer.
