# Live Hook Verification

v0.3 keeps the existing plugin hook layout at `plugins/evm-chain-engineering-pro/hooks/hooks.json` and continues omitting a Codex manifest `hooks` field.

Strict validation requires each platform to provide either:

- a passing hook observation with evidence paths, or
- a documented `not-supported` platform limitation with evidence.

Bootstrap mode keeps `dogfood/hooks/*/observed-hooks.json` at `pending` and records release readiness as false.
