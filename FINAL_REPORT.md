# Final Report: v0.3.0-beta Live Agent QA Harness

## Summary

Implemented the v0.3.0-beta bootstrap harness on branch `v0.3-beta-live-agent-qa`. The release adds live dogfood prompts, expected behavior contracts, transcript and live-run schemas, validators, hook observation checks, skill routing scorecards, known-bad output checks, live-run package templates, platform compatibility docs, and release evidence support.

This is not a strict v0.3 release yet. Real Codex and Claude transcripts, live hook observations, and strict acceptance evidence remain pending.

## Files Added or Changed

- Added v0.3 dogfood structure under `dogfood/`.
- Added v0.3 root scripts for prompt linting, transcript validation, live-run package validation, live acceptance, skill routing, hook observations, subagent dogfood, fixture comparison, known-bad output detection, live-run package creation, and platform matrix updates.
- Updated `Makefile`, `README.md`, `CHANGELOG.md`, `KNOWN_LIMITATIONS.md`, `docs/release-process.md`, and release evidence generation.
- Added v0.3 docs for live dogfood, hook verification, transcript capture, platform compatibility, release planning, and operator workflow.

## Validation Results

Pending final run:

- `python3 -m pytest`
- `make validate`
- `make validate-v02`
- `make validate-v03-bootstrap`
- `make validate-v03 || true`

Expected before live evidence:

- Bootstrap validation: PASS.
- Strict validation: FAIL for missing live Codex/Claude evidence and pending hook observations only.

## Git

- Branch: `v0.3-beta-live-agent-qa`
- Starting tag: `v0.2.0-alpha`
- v0.3 tag: not created
- Push/publish/deploy: not performed

## Known Limitations

No live chain deployment, no real secrets, no MCP servers, no mainnet approval marker, no fabricated transcripts, no fabricated hook observations, and no strict v0.3 release claim.

## Next Recommended Milestone

Capture real Codex and Claude live-run packages, validate strict mode, then create `v0.3.0-beta` only if strict validation passes.
