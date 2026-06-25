# Architecture Decision Record: Example EVM L1 PoSA Testnet

## Status

Planning-only fixture. Not approved for production or mainnet.

## Context

The workflow targets `public-testnet` using BNB-style PoSA EVM L1.

## Decision

Use `bnb-style-posa` for a `l1` planning bundle with roles: validator, rpc-node, bootnode, explorer, monitoring, governance-operator.

## Alternatives Considered

| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| BNB-style PoSA EVM L1 | Native EVM chain path with validator network, consensus, validator economics, genesis, native token, chain ID, bootnodes, RPC, explorer, governance, and launch-gate planning | selected for this workflow |
| Arbitrum Orbit | Parent-chain/L3 path | rejected because this fixture requires native consensus planning |
| Polygon CDK / Agglayer | Validity/validium-focused path | rejected because this fixture requires native validator-set planning |
| ZK Stack | ZK chain path with prover operations | rejected because this fixture requires independent validator-network planning |

## Security Model

Generated artifacts are not audits. Security depends on signer custody, bridge assumptions, DA assumptions, admin-key governance, and upstream release choices.

## Settlement Model

Settlement layer: `native-l1`. Verify finality and bridge conditions against current docs.

## Data Availability Model

DA mode: `native-chain`. DA failures must be modeled before real deployment.

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
