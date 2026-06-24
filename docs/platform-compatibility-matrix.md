# Platform Compatibility Matrix

Generated from v0.3 local evidence. `pending` means bootstrap-compatible but not strict-release-ready.

Official platform docs were refreshed on 2026-06-25. Compatibility statuses still require evidence paths from live Codex and Claude sessions before they can move from `pending` to `yes`, `partial`, `blocked`, or `no`.

| Platform | Live Transcripts | Hook Activation | Skill Observation | Artifact Generation |
|---|---|---|---|---|
| codex | partial: smoke prompt captured | pending | partial: smoke skills observed | partial: smoke bundle validated |
| claude | blocked: 401 authentication_failed | pending | partial: plugin discovery only | blocked: auth before generation |

## Evidence Paths

- Codex smoke package: `dogfood/live-runs/codex/01-op-stack-public-testnet/`
- Claude blocked smoke package: `dogfood/live-runs/claude/01-op-stack-public-testnet/`

## Release Impact

Strict v0.3 remains not release-ready until authenticated Claude execution, required prompt coverage on both platforms, and live hook observation are captured.
