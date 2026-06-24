# Claude Authentication Blocker

## Status

Open

## Evidence

- Live-run package: `dogfood/live-runs/claude/01-op-stack-public-testnet/`
- Redacted stream: `dogfood/live-runs/claude/01-op-stack-public-testnet/CLAUDE_STREAM_REDACTED.jsonl`
- Error: `401 authentication_failed`

## Impact

Claude strict live evidence is blocked. The plugin was discovered and 14 plugin skills were reported by the init event, but the agent turn did not execute.

## Required Resolution

Configure a valid Claude Code authentication path, rerun the smoke prompt, generate the artifact bundle, capture hook events if available, and rerun strict v0.3 validation.
