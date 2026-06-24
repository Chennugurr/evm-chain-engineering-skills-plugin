---
name: arbitrum-orbit-engineer
description: "Engineer Arbitrum Orbit and Nitro chains, Rollup and AnyTrust modes, L2 or L3 settlement, parent-chain selection, custom gas tokens, validators, batch posting, delayed inbox, sequencer feed, Stylus considerations, and Orbit bridge limits. Use for Arbitrum chain launch, config, or ops. Do not use for OP Stack, Polygon CDK, ZK Stack, or generic L1 builds."
---

# Arbitrum Orbit Engineer

## Purpose

Design and review Arbitrum Orbit/Nitro chains, including parent-chain, AnyTrust, and bridge assumptions.

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

- Orbit architecture record
- parent-chain decision
- bridge assumptions
- validator plan

## References To Load

- `references/orbit-and-nitro-architecture.md`
- `references/rollup-vs-anytrust.md`
- `references/anytrust-and-dacs.md`
- `references/l2-vs-l3-settlement.md`
- `references/parent-chain-selection.md`
- `references/custom-gas-token.md`
- `references/delayed-inbox-and-bridge.md`
- `references/stylus-considerations.md`
- `references/orbit-server-topology.md`
- `references/orbit-troubleshooting.md`

## Scripts and Templates To Use

- Use `scripts/scan_secrets.py` before shipping generated files.
- Use `scripts/dry_run_deploy_plan.py` before any deployment plan.
- Use stack-specific validators such as `validate_genesis.py`, `validate_rollup_config.py`, `validate_firewall_policy.py`, and `validate_chain_metadata.py` when inputs exist.
- Use templates only with placeholder values and external secret references.

## Acceptance Criteria

- The output states assumptions, trust model, validation steps, and unresolved `VERIFY_CURRENT_DOCS` items.
- Production-like outputs include security review triggers and launch blockers.
- Generated configs can be validated without real secrets or network side effects.
