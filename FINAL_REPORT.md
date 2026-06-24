# Final Report: v0.3.0-beta Live Agent QA Harness

## Summary

Implemented the v0.3.0-beta bootstrap harness on branch `v0.3-beta-live-agent-qa`, then started the strict live evidence pass on branch `v0.3-beta-strict-live-evidence`. The repository now includes live dogfood prompts, expected behavior contracts, transcript and live-run schemas, validators, hook observation checks, skill routing scorecards, known-bad output checks, live-run package templates, platform compatibility docs, release evidence support, and first smoke-run evidence.

This is not a strict v0.3 release yet. One Codex smoke run is captured and validated. Claude plugin discovery is captured, but the live agent turn is blocked by `401 authentication_failed`. Live hook observations and the remaining required prompt matrix remain pending.

## Files Added or Changed

- Added v0.3 dogfood structure under `dogfood/`.
- Added v0.3 root scripts for prompt linting, transcript validation, live-run package validation, live acceptance, skill routing, hook observations, subagent dogfood, fixture comparison, known-bad output detection, live-run package creation, and platform matrix updates.
- Updated `Makefile`, `README.md`, `CHANGELOG.md`, `KNOWN_LIMITATIONS.md`, `docs/release-process.md`, and release evidence generation.
- Added v0.3 docs for live dogfood, hook verification, transcript capture, platform compatibility, release planning, and operator workflow.
- Added Codex smoke evidence under `dogfood/live-runs/codex/01-op-stack-public-testnet/`.
- Added Claude blocked smoke evidence under `dogfood/live-runs/claude/01-op-stack-public-testnet/`.
- Updated validators to allow blocked packages in bootstrap while rejecting them in strict mode.

## Validation Results

Latest command results recorded during the strict evidence pass:

- `claude plugin validate plugins/evm-chain-engineering-pro --strict`: PASS.
- Codex smoke bundle validation: PASS for artifact validation, generated-config validation, known-bad output scan, and strict secret scan.
- Claude smoke run: BLOCKED by `401 authentication_failed` after plugin discovery.
- `python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs --strict`: PASS.
- `python3 scripts/validate_dogfood_transcripts.py --bootstrap`: PASS.
- `python3 scripts/run_live_acceptance_suite.py --bootstrap`: PASS.

Bootstrap evidence:

- `live_codex_transcripts`: 1 smoke transcript.
- `live_claude_transcripts`: 1 blocked smoke transcript.
- `live_hook_observations`: pending.
- `release_ready`: false.
- `v0.3.0-beta` tag: not created.

## Git

- Branch: `v0.3-beta-strict-live-evidence`
- Starting tag: `v0.2.0-alpha`
- v0.3 tag: not created
- Latest baseline/preflight commit before smoke evidence: `7d68dac`
- Push/publish/deploy: not performed

## Known Limitations

No live chain deployment, no real secrets, no MCP servers, no mainnet approval marker, no fabricated transcripts, no fabricated hook observations, and no strict v0.3 release claim.

## Next Recommended Milestone

Capture an authenticated Claude smoke run, then continue the required six-prompt Codex and Claude matrix, live hook observation, subagent evidence, and strict release evidence. Create `v0.3.0-beta` only if `make validate-v03` passes.
