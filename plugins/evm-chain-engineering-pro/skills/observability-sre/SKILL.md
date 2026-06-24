---
name: observability-sre
description: "Design observability and SRE systems for EVM chains, rollups, RPC gateways, sequencers, batchers, proposers, provers, validators, bridges, explorers, Prometheus, Grafana, Alertmanager, Loki, OpenTelemetry, health checks, SLOs, SLAs, status pages, and incident signals. Use for monitoring and reliability work. Do not use as a replacement for security review or infrastructure planning."
---

# Observability and SRE

## Purpose

Plan chain observability, SLOs, alerts, dashboards, log pipelines, tracing, and status processes.

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

- metrics catalog
- alert plan
- dashboard plan
- runbook links

## References To Load

- `references/monitoring.md`
- `references/metrics-catalog.md`
- `references/prometheus-alerts.md`
- `references/grafana-dashboards.md`
- `references/grafana-dashboard-design.md`
- `references/logs-and-loki.md`
- `references/logs-and-tracing.md`
- `references/tracing.md`
- `references/rpc-health-checks.md`
- `references/rollup-health-checks.md`
- `references/status-pages.md`
- `references/slo-and-sla-models.md`

## Scripts and Templates To Use

- Use `scripts/scan_secrets.py` before shipping generated files.
- Use `scripts/dry_run_deploy_plan.py` before any deployment plan.
- Use stack-specific validators such as `validate_genesis.py`, `validate_rollup_config.py`, `validate_firewall_policy.py`, and `validate_chain_metadata.py` when inputs exist.
- Use templates only with placeholder values and external secret references.

## Acceptance Criteria

- The output states assumptions, trust model, validation steps, and unresolved `VERIFY_CURRENT_DOCS` items.
- Production-like outputs include security review triggers and launch blockers.
- Generated configs can be validated without real secrets or network side effects.
