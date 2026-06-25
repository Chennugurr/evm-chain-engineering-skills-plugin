# Final Report: v0.3.0-beta Live Agent QA Harness

## Summary

Implemented the v0.3.0-beta bootstrap harness on branch `v0.3-beta-live-agent-qa`, then started the strict live evidence pass on branch `v0.3-beta-strict-live-evidence`. The repository now includes live dogfood prompts, expected behavior contracts, transcript and live-run schemas, validators, hook observation checks, skill routing scorecards, known-bad output checks, live-run package templates, platform compatibility docs, release evidence support, and first smoke-run evidence.

This is not a strict v0.3 release yet. One Codex smoke run is captured and validated. Claude plugin discovery is captured successfully with direct skill invocation and hook lifecycle events. Claude OP Stack smoke is now captured and validated with generated artifacts. Codex hook observations, subagent evidence, and the remaining required prompt matrix remain pending.

The latest Claude retry resolved the prior noninteractive `401 authentication_failed` blocker: `claude auth status` reports logged in with account identifiers redacted, `claude plugin validate` passes, a no-plugin `claude --print` smoke reached assistant output, plugin-dir discovery completed, and the OP Stack artifact smoke completed.

## Files Added or Changed

- Added v0.3 dogfood structure under `dogfood/`.
- Added v0.3 root scripts for prompt linting, transcript validation, live-run package validation, live acceptance, skill routing, hook observations, subagent dogfood, fixture comparison, known-bad output detection, live-run package creation, and platform matrix updates.
- Updated `Makefile`, `README.md`, `CHANGELOG.md`, `KNOWN_LIMITATIONS.md`, `docs/release-process.md`, and release evidence generation.
- Added v0.3 docs for live dogfood, hook verification, transcript capture, platform compatibility, release planning, and operator workflow.
- Added Codex smoke evidence under `dogfood/live-runs/codex/01-op-stack-public-testnet/`.
- Added and then refreshed Claude smoke evidence under `dogfood/live-runs/claude/01-op-stack-public-testnet/`.
- Added Claude discovery evidence under `dogfood/live-runs/claude/00-plugin-discovery/`.
- Updated validators to allow blocked packages in bootstrap while rejecting them in strict mode.
- Moved canonical blocker issue to `dogfood/issues/resolved/CLAUDE-AUTH-401.md`.
- Added triage doc `docs/claude-auth-blocker-triage.md`.
- Rebuilt `docs/platform-compatibility-matrix.md` with evidence paths and strict status labels.

## Validation Results

Latest command results recorded during the strict evidence pass:

- `python3 -m pytest`: PASS, 57 tests passed.
- `make validate`: PASS.
- `make validate-v03-bootstrap`: PASS.
- `make validate-v03 || true`: expected strict failure at `validate_dogfood_transcripts.py --strict`.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict`: PASS.
- `claude auth status`: logged in, account identifiers redacted from committed evidence.
- no-plugin `claude --print`: PARTIAL, assistant returned `ok`; command ended nonzero because the budget cap was too low.
- Codex smoke bundle validation: PASS for artifact validation, generated-config validation, known-bad output scan, and strict secret scan.
- Claude discovery run: PASS.
- Claude smoke run: PASS for `01-op-stack-public-testnet`.
- `python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs --strict`: PASS.
- `python3 scripts/validate_dogfood_transcripts.py --bootstrap`: PASS.
- `python3 scripts/run_live_acceptance_suite.py --bootstrap`: PASS.

Bootstrap evidence:

- `live_codex_transcripts`: 1 smoke transcript.
- `live_claude_transcripts`: 1 discovery transcript plus 1 captured OP Stack smoke transcript.
- `live_hook_observations`: Claude central observation is pass; Codex observation remains pending.
- `release_ready`: false.
- `v0.3.0-beta` tag: not created.

## Git

- Branch: `v0.3-beta-strict-live-evidence`
- Starting tag: `v0.2.0-alpha`
- v0.3 tag: not created
- Strict evidence preflight commit: `7d68dac`
- Smoke evidence commit: `3bbaeec`
- Bootstrap evidence report commit: `a9f88f9`
- Strict evidence report update: `a6ce400`
- Claude auth blocker classification: `67ec145`
- Claude discovery and OP Stack resolution: pending commit
- Bootstrap evidence after auth triage: `73c7158`
- Latest generated-evidence refresh before this report update: `bc7920b`
- Push/publish/deploy: not performed

## Known Limitations

No live chain deployment, no real secrets, no MCP servers, no mainnet approval marker, no fabricated transcripts, no fabricated hook observations, and no strict v0.3 release claim.

## Next Recommended Milestone

Continue the required six-prompt Codex and Claude matrix, capture Codex hook observation, capture subagent evidence, and rerun strict release evidence. Create `v0.3.0-beta` only if `make validate-v03` passes.
