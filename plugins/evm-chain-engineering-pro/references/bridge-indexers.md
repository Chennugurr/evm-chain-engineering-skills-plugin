# Bridge Indexers

## Purpose

Provide focused guidance for `bridge-indexers.md` within the EVM Chain Engineering Plugin.

## Applies To

Use when the task involves bridge, indexers or adjacent architecture, configuration, operations, or safety decisions.

## Does Not Apply To

Do not use as a shortcut around stack-specific docs, security review, human approval, or current upstream verification.

## Current-Docs Verification Notes

VERIFY_CURRENT_DOCS before using exact commands, ports, contract addresses, server requirements, supported modes, version numbers, or upgrade procedures.

## Core Concepts

For bridge work, model canonical routes, parent-chain constraints, token mapping, relayer trust, replay protection, withdrawal delays, and TVL limits.

## Decisions

Capture environment, stack, settlement, DA, proof or consensus model, sequencing, gas token, governance, key custody, and rollback assumptions.

## Configuration Considerations

Prefer placeholders, pinned versions, explicit role names, separated keys, documented ports, and config validation before any dry-run deployment plan.

## Server / Infrastructure Considerations

Define node roles, host sizing, disks, firewall rules, TLS, backups, observability, restore drills, and operator access boundaries.

## Security Considerations

Route production-like work through `chain-security-reviewer`; check admin powers, bridges, DA trust, replay protection, exposed RPC, and incident response.

## Monitoring Considerations

Define liveness, finality, batch/proof submission, bridge health, RPC latency, disk growth, logs, alerts, and runbook links.

## Common Mistakes

Avoid tutorial defaults in public networks, unpinned images, real secrets in templates, role key reuse, public debug RPC, and unstated trust assumptions.

## Checklist

- [ ] Architecture decision recorded.
- [ ] Current docs checked.
- [ ] Config validated.
- [ ] Security review triggered when needed.
- [ ] Dry-run plan produced before changes.

## TODO / Verify Against Current Docs

VERIFY_CURRENT_DOCS: replace generic guidance with stack-version-specific commands and requirements when a concrete target version is selected.

## Version Sensitivity

Treat this reference as stable workflow guidance, not a frozen command source. Refresh before releases or production-like use.
