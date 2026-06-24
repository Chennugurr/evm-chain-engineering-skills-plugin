# Upstream Freshness Policy

Stack docs are fast-moving. Normal validation must not require internet access, but release review should confirm source freshness.

| Volatility | Warn after |
|---|---:|
| stable | 180 days |
| medium | 90 days |
| volatile | 30 days |

Volatile examples: OP Stack deployment tutorials, Arbitrum Orbit deployment commands, Polygon CDK deployment modes, ZKsync prover setup, client compatibility, bridge deployment instructions, and Docker image versions.

Medium examples: architecture docs, chain operator guides, monitoring practices, and generic role descriptions.

Stable examples: conceptual docs, older specifications that change rarely, and high-level trust model explanations.

Run:

```bash
python3 scripts/check_upstream_freshness.py --sources docs/upstream-sources.md --markdown-report docs/upstream-freshness-report.md --allow-offline
```
