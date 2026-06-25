# Stack Decision Matrix: smoke-op-stack-public-testnet

| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| OP Stack | fits `l2` with separated batcher and proposer roles | sepolia | ethereum-blobs | optimistic | verify current docs | medium/high | bridge, keys, RPC, DA | selected |
| OP Stack | L2/L3 optimistic with explicit batcher and proposer separation | parent-chain | calldata/blobs/Alt-DA | optimistic | verify current docs | medium | bridge/admin/sequencer | compare if requirements shift |
| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |

OP Stack comparisons require batcher and proposer planning evidence before any real deployment.
