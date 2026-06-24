# Live Dogfood Guide

v0.3 dogfood proves the plugin in real Codex and Claude sessions. Bootstrap checks only validate the harness. Strict checks require transcript-backed evidence.

Current strict-evidence pass status:

- Codex `01-op-stack-public-testnet`: captured and validated.
- Claude `01-op-stack-public-testnet`: blocked by `401 authentication_failed` after plugin discovery.
- Hook observations: pending.
- `v0.3.0-beta` tag: not created.

Use one prompt from `dogfood/prompts/`, run it in the target platform with the local plugin installed, and capture a live-run package with `scripts/create_live_run_package.py`. Redact secrets before committing any transcript.

Required strict prompts for each platform:

- `01-op-stack-public-testnet`
- `02-arbitrum-orbit-l3-anytrust`
- `03-polygon-cdk-enterprise-validium`
- `05-evm-l1-validator-network`
- `06-unsafe-private-key-request`
- `07-stack-selection-gaming-chain`

Prompt 11 should be captured on at least one platform when subagents are available. If subagents are unavailable, record the limitation with evidence.
