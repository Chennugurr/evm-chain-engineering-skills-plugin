# Stack Decision Matrix: Example Orbit L3 AnyTrust

| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| Arbitrum Orbit | fits `l3` with Orbit/Nitro L3 planning, parent-chain assumptions, sequencer feed, validator/staker review, and custom gas token checks | arbitrum-style-l2-parent | anytrust-dac | anytrust | verify Orbit support in current docs | medium/high | DAC, bridge, sequencer, keys, RPC | selected |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |
| ZK Stack | ZK chain path with prover and proof latency planning | Ethereum/L1 or validium-style options | rollup/validium options | validity | verify current docs | high | prover/bridge/DA | compare for that ecosystem fit |
| EVM L1/appchain | independent chain with validator network and consensus | native consensus | native chain | validator consensus | native token | high | validators/governance/RPC | compare for independent consensus |
