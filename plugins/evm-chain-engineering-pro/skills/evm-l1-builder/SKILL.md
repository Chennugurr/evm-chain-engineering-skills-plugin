---
name: evm-l1-builder
description: "Build and review EVM L1 chains including Ethereum-like execution plus consensus clients, BNB-style PoSA, Cosmos EVM, Avalanche L1/Subnet-EVM, and Polkadot Frontier. Use for genesis, chain IDs, validators, fork schedules, precompiles, RPC, gas token, staking, slashing, and L1 launch planning. Do not use for OP Stack, Orbit, CDK, or ZK Stack rollups."
---

# EVM L1 Builder

## Purpose

Guide Ethereum-like, BNB-style, Cosmos EVM, Avalanche L1, and Frontier-based EVM L1 designs.

## Default Workflow

1. Classify the request, target environment, and chain stack before proposing commands or configs.
2. Identify whether the request touches production, mainnet, public testnet, bridges, admin keys, validators, sequencers, provers, relayers, custom precompiles, or public RPC.
3. If any security trigger is present, invoke or require `chain-security-reviewer` before go/no-go or deployment planning.
4. Load only the references needed for the selected stack or subsystem.
5. Produce dry-run, validation, and review outputs before any state-changing action.
6. Mark exact commands, versions, addresses, server specs, and stack-specific defaults as `VERIFY_CURRENT_DOCS` unless freshly verified from official docs.

## Mandatory Safety Checks

- Never generate, print, store, or commit real private keys or mnemonics.
- Never embed secrets in `.env.example`, templates, docs, systemd units, Docker Compose, Terraform, logs, or examples.
- Never expose admin/debug RPC publicly.
- Never auto-deploy to mainnet, sign transactions, or move funds.
- Keep deployer, admin, sequencer, batcher, proposer, validator, prover, relayer, faucet, explorer, and monitoring roles separate.

## Required Outputs

- genesis plan
- validator topology
- fork schedule
- L1 launch checklist

## References To Load

- `references/ethereum-like-l1.md`
- `references/bnb-style-posa-l1.md`
- `references/cosmos-evm-l1.md`
- `references/avalanche-l1-subnet-evm.md`
- `references/polkadot-frontier-evm.md`
- `references/genesis-config.md`
- `references/validator-economics.md`
- `references/fork-schedule-and-upgrades.md`
- `references/precompiles.md`
- `references/consensus-and-finality.md`

## Scripts and Templates To Use

- Use `scripts/scan_secrets.py` before shipping generated files.
- Use `scripts/dry_run_deploy_plan.py` before any deployment plan.
- Use stack-specific validators such as `validate_genesis.py`, `validate_rollup_config.py`, `validate_firewall_policy.py`, and `validate_chain_metadata.py` when inputs exist.
- Use templates only with placeholder values and external secret references.

## Acceptance Criteria

- The output states assumptions, trust model, validation steps, and unresolved `VERIFY_CURRENT_DOCS` items.
- Production-like outputs include security review triggers and launch blockers.
- Generated configs can be validated without real secrets or network side effects.
