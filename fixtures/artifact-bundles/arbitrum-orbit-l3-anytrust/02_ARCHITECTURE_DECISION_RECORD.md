# Architecture Decision Record: Example Orbit L3 AnyTrust

## Status

Planning-only fixture. Not approved for production or mainnet.

## Context

The workflow targets `public-testnet` using Arbitrum Orbit.

## Decision

Use `arbitrum-orbit` for a `l3` planning bundle with roles: sequencer, validator-or-staker, batch-poster, rpc-node, explorer, monitoring.

## Alternatives Considered

| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| Arbitrum Orbit | Best fit for this fixture | selected for workflow acceptance |
| OP Stack | Common optimistic-rollup baseline | rejected unless this fixture uses OP Stack |
| Arbitrum Orbit | L3 and AnyTrust-capable path | rejected unless this fixture uses Orbit |
| Polygon CDK | Validity/validium-focused path | rejected unless this fixture uses CDK |

## Security Model

Generated artifacts are not audits. Security depends on signer custody, bridge assumptions, DA assumptions, admin-key governance, and upstream release choices.

## Settlement Model

Settlement layer: `arbitrum-style-l2-parent`. Verify finality and bridge conditions against current docs.

## Data Availability Model

DA mode: `anytrust-dac`. DA failures must be modeled before real deployment.

## Sequencing Model

Sequencing model: `centralized-sequencer-for-alpha-fixture`. Censorship, downtime, and centralization risks require review.

## Governance and Upgrade Model

Admin keys must move to multisig plus timelock or documented external custody before production/mainnet.

## Operational Model

Operators run isolated roles for public RPC, internal admin surfaces, monitoring, and signer integrations.

## Consequences

This creates a repeatable planning bundle, not a launch approval.

## Human Decisions Required

- Select exact upstream release versions.
- Assign a unique chain ID after collision checks.
- Approve signer custody and external review scope.
