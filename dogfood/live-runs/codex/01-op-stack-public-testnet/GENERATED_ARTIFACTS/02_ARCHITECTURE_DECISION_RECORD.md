# Architecture Decision Record: smoke-op-stack-public-testnet

## Status

Planning-only fixture. Not approved for production or mainnet.

## Context

The workflow targets `public-testnet` using OP Stack.

## Decision

Use `op-stack` for a `l2` planning bundle with roles: sequencer, execution-client, op-node, batcher, proposer, rpc-node, explorer, monitoring.

## Alternatives Considered

| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| OP Stack | Best fit for this fixture with separated batcher and proposer roles | selected for workflow acceptance |
| OP Stack | Common optimistic-rollup baseline with explicit batcher and proposer separation | rejected unless this fixture uses OP Stack batcher/proposer role separation |
| Arbitrum Orbit | L3 and AnyTrust-capable path | rejected unless this fixture uses Orbit |
| Polygon CDK / Agglayer | Validity/validium-focused path | rejected unless this fixture uses CDK/Agglayer |

OP Stack planning in this bundle explicitly includes separated batcher and proposer roles.

## Security Model

Generated artifacts are not audits. Security depends on signer custody, bridge assumptions, DA assumptions, admin-key governance, and upstream release choices.

## Settlement Model

Settlement layer: `sepolia`. Verify finality and bridge conditions against current docs.

## Data Availability Model

DA mode: `ethereum-blobs`. DA failures must be modeled before real deployment.

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
