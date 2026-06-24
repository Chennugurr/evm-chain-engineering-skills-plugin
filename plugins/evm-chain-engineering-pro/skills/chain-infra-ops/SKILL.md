---
name: chain-infra-ops
description: "Design blockchain infrastructure operations for sequencers, batchers, proposers, validators, provers, RPC nodes, archive nodes, explorers, faucets, bridges, relayers, DA nodes, monitoring, backups, Ubuntu, Docker Compose, systemd, Kubernetes, Terraform, Ansible, Nginx, TLS, firewalls, and incident response. Use for server setup or production topology. Do not use for protocol choice without blockchain-architect."
---

# Chain Infrastructure Operations

## Purpose

Generate infrastructure plans for local devnet, shared devnet, public testnet, production-like staging, and production.

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

- Infrastructure Plan
- host role matrix
- firewall plan
- backup plan

## References To Load

- `references/server-sizing.md`
- `references/ubuntu-server-setup.md`
- `references/bare-metal-vs-cloud.md`
- `references/docker-compose.md`
- `references/systemd.md`
- `references/kubernetes.md`
- `references/terraform.md`
- `references/ansible.md`
- `references/tls-and-nginx.md`
- `references/firewalls-and-networking.md`
- `references/snapshots-and-backups.md`
- `references/disaster-recovery.md`
- `references/load-balancing.md`

## Scripts and Templates To Use

- Use `scripts/scan_secrets.py` before shipping generated files.
- Use `scripts/dry_run_deploy_plan.py` before any deployment plan.
- Use stack-specific validators such as `validate_genesis.py`, `validate_rollup_config.py`, `validate_firewall_policy.py`, and `validate_chain_metadata.py` when inputs exist.
- Use templates only with placeholder values and external secret references.

## Acceptance Criteria

- The output states assumptions, trust model, validation steps, and unresolved `VERIFY_CURRENT_DOCS` items.
- Production-like outputs include security review triggers and launch blockers.
- Generated configs can be validated without real secrets or network side effects.
