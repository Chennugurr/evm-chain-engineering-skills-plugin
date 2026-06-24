---
name: bridge-interop-engineer
description: "Engineer bridges, canonical bridges, native bridges, L2/L3 bridging, cross-chain messaging, relayers, token mapping, chain metadata, wallet onboarding, bridge monitoring, and bridge security assumptions. Use when moving assets or messages between chains, exposing a bridge UI, or mapping tokens. Do not use without also invoking security review for production, public testnet, or TVL-bearing bridge work."
---

# Bridge and Interoperability Engineer

## Purpose

Plan bridges, canonical routes, relayers, token mappings, and wallet/explorer metadata with explicit trust assumptions.

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

- bridge model
- token map
- relayer plan
- security review inputs

## References To Load

- `references/bridge-and-interoperability.md`
- `references/native-bridges.md`
- `references/canonical-bridges.md`
- `references/cross-chain-messaging.md`
- `references/relayers.md`
- `references/token-mapping.md`
- `references/bridge-security.md`
- `references/bridge-monitoring.md`
- `references/l2-l3-bridging.md`
- `references/chainlist-and-wallets.md`

## Scripts and Templates To Use

- Use `scripts/scan_secrets.py` before shipping generated files.
- Use `scripts/dry_run_deploy_plan.py` before any deployment plan.
- Use stack-specific validators such as `validate_genesis.py`, `validate_rollup_config.py`, `validate_firewall_policy.py`, and `validate_chain_metadata.py` when inputs exist.
- Use templates only with placeholder values and external secret references.

## Acceptance Criteria

- The output states assumptions, trust model, validation steps, and unresolved `VERIFY_CURRENT_DOCS` items.
- Production-like outputs include security review triggers and launch blockers.
- Generated configs can be validated without real secrets or network side effects.
