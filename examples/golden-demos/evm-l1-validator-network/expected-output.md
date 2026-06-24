# Evm L1 Validator Network

## Architecture Decision Record

### Context

The user asked for a dry-run architecture and operations plan. No deployment, broadcast, signing, or secret generation is permitted.

### Decision

Use a staged, review-first plan centered on consensus, validator set, genesis, native token, chain ID, bootnodes, RPC, explorer, monitoring, economics, governance, launch gates. Exact stack commands and server requirements remain `VERIFY_CURRENT_DOCS` before production use.

### Alternatives considered

Keep the chosen stack, a different rollup stack, an EVM L1/appchain, and managed RaaS as alternatives where applicable.

### Consequences

The plan prioritizes explicit trust assumptions, role separation, validation, and launch gates over speed.

### Assumptions

- This is a dry-run planning exercise.
- No real users, funds, production secrets, or live deployment are involved.
- Human review is required before public infrastructure or mainnet-like actions.

### Non-goals

- No deploy commands that broadcast transactions.
- No private keys, mnemonics, or signer credentials.
- No claim that upstream docs are permanently stable.

## Recommended Stack or Stack Shortlist

Recommended path depends on verified upstream docs and target environment. Shortlist must include the requested stack and at least one fallback when the prompt is comparative.

## Stack-specific Architecture

Cover these required concepts: consensus, validator set, genesis, native token, chain ID, bootnodes, RPC, explorer, monitoring, economics, governance, launch gates.

## Server Topology

| Role | Purpose | Suggested environment | Notes |
|---|---|---|---|
| control plane | coordination and runbooks | private admin network | no public admin RPC |
| public RPC | user and indexer access | public edge with rate limits | no debug/personal APIs |
| operations | monitoring and logs | private network | alerts and runbooks required |
| bridge/explorer/faucet | ecosystem services | segmented hosts | external secrets only |

## Data Flow

Document settlement, DA, sequencing, bridge, RPC, indexing, and monitoring flow with explicit finality and failure assumptions.

## Security and Trust Assumptions

- Bridge, DA, sequencer, prover/validator, governance, and admin-key trust assumptions must be stated.
- Production-like work requires `chain-security-reviewer` findings and go/no-go criteria.

## Secrets and Key Management

Use hardware wallets, multisig, timelock, KMS/HSM, signer service, or runtime secret injection. Do not commit secrets or use key-shaped placeholders.

## Governance and Upgrades

Use owner inventory, multisig/timelock policy, emergency pause policy, rollback constraints, release gates, and communication plan.

## Monitoring and Alerts

Track liveness, RPC latency, block production, batch/proof submission, bridge health, DA publication, disk growth, and error budgets.

## Backups, Snapshots, and Recovery

Define snapshot cadence, checksums, restore drills, retention, and isolated restore validation.

## Validation Plan

Run local validators, behavior evals, hook validation, secret scan, firewall policy checks, metadata checks, and dry-run plans only.

## Launch Gates

- Current docs verified.
- Security review accepted.
- Incident runbook ready.
- Backups and restore drills complete.
- Human approval recorded for any production-like action.

## Known Limitations

Stack commands, hardware profiles, contract addresses, and deployment modes are version-sensitive and require current official docs.

## Human Review Checklist

- [ ] Correct skills routed.
- [ ] Required concepts present.
- [ ] Trust assumptions clear.
- [ ] No live deployment.
- [ ] No real or fake key-shaped secrets.
- [ ] `VERIFY_CURRENT_DOCS` items identified.
