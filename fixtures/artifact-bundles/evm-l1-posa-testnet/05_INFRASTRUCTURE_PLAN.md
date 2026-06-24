# Infrastructure Plan: Example EVM L1 PoSA Testnet

## Scope

Planning-only. No real deployment.

## Node Roles

validator, rpc-node, bootnode, explorer, monitoring, governance-operator

## Server Topology

Separate public RPC, internal sequencer/validator/prover roles, monitoring, and signer integrations. Sizing is `VERIFY_CURRENT_DOCS`.

## Network Boundaries

Public ingress only through rate-limited RPC/explorer endpoints. Admin/debug RPC binds to localhost or private networks only.

## Firewall Policy

Allow public RPC only where intended; deny admin/debug APIs externally; restrict signer and database access to private networks.

## Storage Policy

Use dedicated volumes, snapshot/restore checks, and archive/pruning decisions recorded per role.

## Runtime Approach

Docker Compose, systemd, Kubernetes, and Terraform samples are planning templates only.

## Observability

Prometheus, Grafana, logs, RPC health, disk alerts, and role-specific alerts are required before launch.

## Backup/Restore

Backups must be restore-tested before public testnet, staging, production, or mainnet.

## Upgrade Process

Stage upgrades, pin versions, verify upstream docs, and maintain rollback plans.

## Incident Response

Triage node down, RPC unavailable, sequencer lag, bridge incident, DA failure, and signer access incidents.

## Genesis Planning

Genesis configuration, validator allocation, bootnodes, fork schedule, and chain ID collision checks must be reviewed before any real network launch.
