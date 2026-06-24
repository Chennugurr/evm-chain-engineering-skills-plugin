# Runbook: Example OP Stack Public Testnet

## Preflight Checklist

- Run validators in dry-run mode.
- Confirm no secrets are committed.
- Verify upstream docs and versions.

## Start/Stop Service Examples

Use local dry-run or staging-only service manager commands after human review. Do not use this fixture for mainnet deployment.

## Monitoring Checks

Check node availability, RPC health, disk, logs, and role-specific lag.

## Backup Checks

Confirm snapshots exist and restore into an isolated environment.

## Rollback Checklist

Record version pins, config backups, and rollback owners before changes.

## Incident Triage

Classify RPC outage, sequencer/validator/prover issue, bridge risk, DA failure, or signer incident.
