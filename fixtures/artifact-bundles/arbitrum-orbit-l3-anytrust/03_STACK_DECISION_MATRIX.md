# Stack Decision Matrix: Example Orbit L3 AnyTrust

| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| Arbitrum Orbit | fits `l3` | arbitrum-style-l2-parent | anytrust-dac | anytrust | verify current docs | medium/high | bridge, keys, RPC, DA | selected |
| OP Stack | L2/L3 optimistic | parent-chain | calldata/blobs/Alt-DA | optimistic | verify current docs | medium | bridge/admin/sequencer | compare if requirements shift |
| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |
