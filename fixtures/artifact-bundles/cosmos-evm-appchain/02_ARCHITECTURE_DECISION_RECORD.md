# Architecture Decision Record: Example Cosmos EVM Appchain

## Status

Planning-only fixture. Not approved for production or mainnet.

## Context

The workflow targets `public-testnet` using Cosmos EVM Appchain.

## Decision

Use `cosmos-evm` for a `appchain` planning bundle with roles: validator, full-node, rpc-node, rest-api, explorer, monitoring, governance-operator.

## Alternatives Considered

| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| Cosmos EVM Appchain | Best fit for this fixture | selected for workflow acceptance |
| OP Stack | Common optimistic-rollup baseline | rejected unless this fixture uses OP Stack |
| Arbitrum Orbit | L3 and AnyTrust-capable path | rejected unless this fixture uses Orbit |
| Polygon CDK | Validity/validium-focused path | rejected unless this fixture uses CDK |

## Security Model

Generated artifacts are not audits. Security depends on signer custody, bridge assumptions, DA assumptions, admin-key governance, and upstream release choices.

## Settlement Model

Settlement layer: `native-cometbft`. Verify finality and bridge conditions against current docs.

## Data Availability Model

DA mode: `native-cometbft-chain`. DA failures must be modeled before real deployment.

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
