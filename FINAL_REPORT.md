# Final Report: v0.3.0-beta Live Agent QA Harness

## Summary

Implemented the v0.3.0-beta bootstrap harness on branch `v0.3-beta-live-agent-qa`, continued the strict live evidence pass on `v0.3-beta-strict-live-evidence`, and captured the live matrix closure on `v0.3.0-beta-live-matrix-closure`. The repository now includes live dogfood prompts, expected behavior contracts, transcript and live-run schemas, validators, hook observation checks, skill routing scorecards, known-bad output checks, live-run package templates, platform compatibility docs, release evidence support, smoke evidence, hook evidence, and the required Codex/Claude prompt matrix.

This is not tagged yet. Codex and Claude now have captured live evidence for required prompts `01`, `02`, `03`, `05`, `06`, and `07`. Claude plugin discovery is captured successfully with direct skill invocation and hook lifecycle events. Codex live hook observation is captured and validated for smoke scope. Subagent execution is not claimed; the limitation is recorded in `dogfood/reports/subagent-dogfood-limitation.md`.

The latest Claude retry resolved the prior noninteractive `401 authentication_failed` blocker: `claude auth status` reports logged in with account identifiers redacted, `claude plugin validate` passes, a no-plugin `claude --print` smoke reached assistant output, plugin-dir discovery completed, and the OP Stack artifact smoke completed.

The latest Codex hook closure resolved the prior pending hook blocker for smoke scope: Codex discovered the bundled `hooks/hooks.json`, allowed a safe validation command, denied a fake-secret write, denied a mainnet-like broadcast command, and left the sentinel file absent. The run used `--dangerously-bypass-hook-trust` for noninteractive automation; persisted interactive `/hooks` trust is not claimed.

## Files Added or Changed

- Added v0.3 dogfood structure under `dogfood/`.
- Added v0.3 root scripts for prompt linting, transcript validation, live-run package validation, live acceptance, skill routing, hook observations, subagent dogfood, fixture comparison, known-bad output detection, live-run package creation, and platform matrix updates.
- Updated `Makefile`, `README.md`, `CHANGELOG.md`, `KNOWN_LIMITATIONS.md`, `docs/release-process.md`, and release evidence generation.
- Added v0.3 docs for live dogfood, hook verification, transcript capture, platform compatibility, release planning, and operator workflow.
- Added Codex smoke evidence under `dogfood/live-runs/codex/01-op-stack-public-testnet/`.
- Added required Codex matrix evidence under `dogfood/live-runs/codex/{02,03,05,06,07}-*/`.
- Added required Claude matrix evidence under `dogfood/live-runs/claude/{02,03,05,06,07}-*/`.
- Added and then refreshed Claude smoke evidence under `dogfood/live-runs/claude/01-op-stack-public-testnet/`.
- Added Claude discovery evidence under `dogfood/live-runs/claude/00-plugin-discovery/`.
- Added Codex hook evidence under `dogfood/hooks/codex/`.
- Updated validators to allow blocked packages in bootstrap while rejecting them in strict mode.
- Updated hook policy guard packaging so installed Codex plugin cache execution is self-contained.
- Moved canonical blocker issue to `dogfood/issues/resolved/CLAUDE-AUTH-401.md`.
- Added triage doc `docs/claude-auth-blocker-triage.md`.
- Rebuilt `docs/platform-compatibility-matrix.md` with evidence paths and strict status labels.

## Validation Results

Latest command results recorded during the strict evidence pass:

- `python3 -m pytest`: PASS, 58 tests passed.
- `make validate`: PASS.
- `make validate-v03-bootstrap`: PASS.
- `make validate-v03`: pending rerun after committing the live matrix, because committed-only clean install rejects dirty non-release trees.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict`: PASS.
- `claude auth status`: logged in, account identifiers redacted from committed evidence.
- no-plugin `claude --print`: PARTIAL, assistant returned `ok`; command ended nonzero because the budget cap was too low.
- Codex smoke bundle validation: PASS for artifact validation, generated-config validation, known-bad output scan, and strict secret scan.
- Claude discovery run: PASS.
- Claude smoke run: PASS for `01-op-stack-public-testnet`.
- `python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs --strict`: PASS.
- `python3 scripts/validate_dogfood_transcripts.py --strict`: PASS.
- `python3 scripts/run_live_acceptance_suite.py --strict --scope smoke`: PASS.
- `python3 scripts/score_skill_routing.py --strict --scope smoke`: PASS.
- `python3 scripts/validate_live_hook_observations.py --strict --platform claude`: PASS.
- `python3 scripts/validate_live_hook_observations.py --strict --platform codex`: PASS.
- `python3 scripts/validate_live_run_package.py --all --strict`: PASS, 13 packages checked.
- `python3 scripts/run_live_acceptance_suite.py --strict`: PASS, 13 transcripts checked.
- `python3 scripts/score_skill_routing.py --strict`: PASS, overall score 100.
- `python3 scripts/compare_live_to_fixture.py --strict`: PASS.
- `python3 scripts/validate_subagent_dogfood.py --strict`: PASS with documented limitation and no live subagent claim.

Strict `make validate-v03` remaining blocker before commit:

- committed-only clean install requires the live matrix changes to be committed before the full gate can run.

Bootstrap evidence:

- `live_codex_transcripts`: 6 required prompt transcripts.
- `live_claude_transcripts`: 7 transcripts, including discovery plus 6 required prompt transcripts.
- `live_hook_observations`: Claude central observation is pass; Codex central observation is pass for smoke scope.
- `release_ready`: false.
- `v0.3.0-beta` tag: not created.

## Git

- Branch: `v0.3.0-beta-live-matrix-closure`
- Starting tag: `v0.2.0-alpha`
- v0.3 tag: not created
- Strict evidence preflight commit: `7d68dac`
- Smoke evidence commit: `3bbaeec`
- Bootstrap evidence report commit: `a9f88f9`
- Strict evidence report update: `a6ce400`
- Claude auth blocker classification: `67ec145`
- Claude discovery and OP Stack resolution: `873a02f`
- Bootstrap evidence after auth triage: `73c7158`
- Latest generated-evidence refresh after Claude rerun: `1fe4f13`
- Codex hook evidence closure: `727fb3a`
- Latest generated-evidence refresh after Codex hook closure: `0d0c5eb`
- Live matrix closure: pending commit
- Push/publish/deploy: not performed

## Known Limitations

No live chain deployment, no real secrets, no MCP servers, no mainnet approval marker, no fabricated transcripts, no fabricated hook observations, no fabricated subagent execution, and no strict v0.3 release claim until the final full gate passes.

## Next Recommended Milestone

Commit the live matrix closure, rerun the full validation ladder, refresh strict release evidence, and create `v0.3.0-beta` only if `make validate-v03` passes.
