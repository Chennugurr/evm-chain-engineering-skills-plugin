---
name: chain-security-reviewer
description: "Review blockchain and rollup security for mainnet, production, public testnet, bridges, admin keys, validators, sequencers, provers, relayers, custom precompiles, upgrade controls, DA trust, fraud or validity proofs, exposed RPC, key custody, and launch readiness. Use whenever the request involves real users, value, public infrastructure, or unsafe shortcuts. Do not use to bless production without findings and go/no-go criteria."
---

# Chain Security Reviewer

## Purpose

Review protocol, bridge, admin, key, infra, and agent/plugin safety risks before production-like actions.

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

- Security Review
- launch blockers
- required fixes
- accepted risks

## References To Load

- `references/threat-model.md`
- `references/key-management.md`
- `references/upgrade-admin.md`
- `references/precompile-review.md`
- `references/bridge-security.md`
- `references/supply-chain-security.md`
- `references/plugin-agent-security.md`
- `references/audit-preparation.md`
- `references/governance-and-upgrades.md`
- `references/validator-security.md`
- `references/rpc-security.md`
- `references/genesis-review.md`
- `references/mainnet-readiness.md`

## Scripts and Templates To Use

- Use `scripts/scan_secrets.py` before shipping generated files.
- Use `scripts/dry_run_deploy_plan.py` before any deployment plan.
- Use stack-specific validators such as `validate_genesis.py`, `validate_rollup_config.py`, `validate_firewall_policy.py`, and `validate_chain_metadata.py` when inputs exist.
- Use templates only with placeholder values and external secret references.

## Acceptance Criteria

- The output states assumptions, trust model, validation steps, and unresolved `VERIFY_CURRENT_DOCS` items.
- Production-like outputs include security review triggers and launch blockers.
- Generated configs can be validated without real secrets or network side effects.
