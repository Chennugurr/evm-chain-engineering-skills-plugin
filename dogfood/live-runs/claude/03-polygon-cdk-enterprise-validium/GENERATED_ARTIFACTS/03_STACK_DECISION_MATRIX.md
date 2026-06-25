# Stack Decision Matrix: Example CDK Enterprise Validium

| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| Polygon CDK | fits `validium` with Polygon CDK validium, zkRollup, sovereign mode, Agglayer, prover, DA committee, enterprise, and bridge planning | ethereum-testnet-or-agglayer | offchain-da-committee | validity-proof | verify CDK support in current docs | high | prover, DA, bridge, keys, RPC | selected |
| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |
| ZK Stack | ZK chain path with prover and proof latency planning | Ethereum/L1 or validium-style options | rollup/validium options | validity | verify current docs | high | prover/bridge/DA | compare for that ecosystem fit |
| EVM L1/appchain | independent chain with validator network and consensus | native consensus | native chain | validator consensus | native token | high | validators/governance/RPC | compare for independent consensus |
