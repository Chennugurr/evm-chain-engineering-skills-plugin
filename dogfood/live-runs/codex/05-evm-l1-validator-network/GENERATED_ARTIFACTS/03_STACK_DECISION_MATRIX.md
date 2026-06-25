# Stack Decision Matrix: Example EVM L1 PoSA Testnet

| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| BNB-style PoSA EVM L1 | fits `l1` with validator set, consensus, genesis, native token, chain ID, bootnodes, RPC, explorer, governance, and launch-gate planning | native-l1 | native-chain | validator-consensus | native token planning required | high | validators, governance, RPC, bootnodes, key custody | selected |
| Arbitrum Orbit | parent-chain/L3 path | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | rejected for native consensus fixture |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | rejected for native consensus fixture |
| ZK Stack | ZK chain path | Ethereum/L1 or validium-style options | rollup/validium options | validity | verify current docs | high | prover/bridge/DA | rejected for native consensus fixture |
