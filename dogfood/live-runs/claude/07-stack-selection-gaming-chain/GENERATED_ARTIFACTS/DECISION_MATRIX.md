# Gaming Chain Decision Matrix

| Option | Fit | Data availability | Bridge | Ops burden | Security model | Recommendation |
|---|---|---|---|---|---|---|
| L1 appchain | Maximum sovereignty, native token, appchain control | Native DA and validator-set operations | Requires dedicated bridge strategy | High | Independent consensus and validator governance | Consider only if sovereignty outweighs operations cost |
| L2 | Strong settlement alignment and liquidity | Parent-chain DA or supported alternatives | Mature bridge path | Medium | Inherits rollup trust assumptions | Good default when ecosystem alignment matters |
| L3 | Lower cost and app-specific tuning | Parent/committee DA depending stack | Bridge through parent chain | Medium | Adds parent-chain and bridge assumptions | Strong candidate for high-volume games |
| Modular rollup | Flexible DA and execution choices | External DA choices require explicit trust review | Bridge depends on stack | High | DA, settlement, and sequencer assumptions must be separated | Consider with experienced operations team |

## Rejected Options

- Reject any answer that skips tradeoffs or treats a single universal answer as enough.
- Reject paths without custom gas token review, bridge assumptions, and launch-gate security review.

## Dry-Run Next Steps

Draft an ADR, select candidate stack profiles, validate chain ID and data availability assumptions, design bridge controls, and run security review before any deployment phase.
