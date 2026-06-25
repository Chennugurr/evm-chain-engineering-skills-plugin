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
| Arbitrum Orbit | L3-capable Orbit/Nitro path with parent-chain settlement, custom gas token planning, sequencer feed, validator/staker review, bridge assumptions, and AnyTrust/DAC review | selected for this workflow |
| Polygon CDK / Agglayer | Validity/validium-focused path | rejected unless validity proofs and Agglayer integration dominate |
| ZK Stack | ZK chain path with prover and proof latency planning | rejected unless that proving model dominates |
| EVM L1/appchain | Native validator-network and consensus path | rejected unless independent consensus and validator economics dominate |

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
