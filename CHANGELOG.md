# Changelog

## v0.3.0-beta evidence closure

Changed:
- Resolved the Claude noninteractive `401 authentication_failed` blocker for discovery and moved the issue to `dogfood/issues/resolved/CLAUDE-AUTH-401.md`.
- Added Claude `00-plugin-discovery` evidence with plugin visibility, direct skill invocation, routing evidence, hook lifecycle events, and portability notes.
- Reran Claude `01-op-stack-public-testnet` successfully with generated artifacts, validation reports, hook events, and policy evidence.
- Updated Claude hook observation status to pass.
- Captured Codex live hook evidence with plugin-bundled `PreToolUse:Bash` decisions, safe-command allow, fake-secret deny, and mainnet-like broadcast deny.
- Made the policy guard hook output use Codex `permissionDecision` JSON with exit `0`, while preserving strict nonzero exits for normal CLI scans.
- Moved hook metadata into `hooks/policy-metadata.json` so `hooks/hooks.json` stays compatible with Codex hook parsing.
- Made the plugin-local policy guard self-contained for installed plugin cache execution.

Validation:
- `claude auth status` reports logged in with account identifiers redacted.
- A no-plugin `claude --print` request returned assistant text `ok`; the command ended nonzero only because the budget cap was too low.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict` passes.
- Claude plugin discovery passes.
- Claude OP Stack smoke validation passes for artifact bundle, generated configs, known-bad output scan, and strict secret scan.
- Codex hook observation validation passes for smoke scope.

Release:
- Strict v0.3 remains blocked by the remaining live prompt matrix and subagent evidence.
- `v0.3.0-beta` tag remains uncreated.

## v0.3.0-beta auth blocker classification

Changed:
- Added canonical blocker issue `dogfood/issues/open/CLAUDE-AUTH-401.md`, later moved to `dogfood/issues/resolved/CLAUDE-AUTH-401.md`.
- Added `docs/claude-auth-blocker-triage.md` with redacted Claude Code auth diagnostics and later resolution notes.
- Rebuilt `docs/platform-compatibility-matrix.md` with status rows and evidence paths.
- Updated Claude OP Stack smoke manual notes with the original auth-only classification, later superseded by the successful rerun.

Validation:
- `claude auth status` reports logged in with account identifiers redacted.
- A no-plugin `claude --print` request failed with `401 authentication_failed` during the original classification pass, then reached assistant output during the later retry.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict` still passes.

Release:
- Strict v0.3 remains blocked by incomplete live matrix evidence, not by this resolved auth issue.
- `v0.3.0-beta` tag remains uncreated.

## v0.3.0-beta strict evidence pass

Added:
- Codex live smoke package for `01-op-stack-public-testnet` with redacted transcript stream, generated artifact bundle, validation reports, policy events, and manual notes.
- Initial Claude live smoke package for `01-op-stack-public-testnet` documenting plugin discovery and `401 authentication_failed`; later superseded by the successful Claude rerun.

Changed:
- v0.3 validators include live-run `TRANSCRIPT.json` files in transcript discovery.
- Bootstrap mode accepts documented blocked live packages; strict mode rejects them.
- Skill routing and live acceptance skip blocked packages in bootstrap and reject them in strict mode.

Validation:
- Codex smoke bundle passed artifact validation, generated-config validation, known-bad output scan, and strict secret scan.
- Claude plugin manifest validation passed; live agent execution did not authenticate in the original pass and later succeeded in the closure rerun.

Release:
- `v0.3.0-beta` tag remains uncreated.
- Strict v0.3 remains blocked pending remaining required prompts on both platforms, Codex hook observation, and subagent evidence.

## v0.3.0-beta bootstrap harness

Added:
- live dogfood prompts and expected behavior contracts
- transcript, live-run, hook observation, acceptance, and skill routing schemas
- bootstrap and strict validators for live evidence
- skill routing scorecard generation
- known-bad output detection
- live-run package templates
- v0.3 release evidence support
- live dogfood, hook verification, transcript capture, compatibility, and operator docs

Changed:
- Makefile includes `validate-v03-bootstrap` and `validate-v03`
- release evidence distinguishes harness validation from strict release readiness

Security:
- strict mode rejects missing live transcripts, pending hook observations, unsafe outputs, and unvalidated live artifacts
- bootstrap mode records live evidence as pending and release readiness as false

Limitations:
- no live evidence is fabricated
- no `v0.3.0-beta` tag is created until strict live validation passes
- no push, publish, deploy, real secrets, MCP servers, or mainnet approval marker

## v0.2.0-alpha

Added:
- machine-checkable artifact bundle contract
- stack profiles and validators
- safe artifact generators
- validated fixture artifact bundles
- generated config validator
- acceptance suite
- hook fixture tests
- clean install test
- release evidence builder
- internal adoption docs
- known limitations
- contributor workflow for new stacks

Changed:
- Makefile includes `validate-v02` targets
- README documents artifact workflows

Security:
- stronger validation against committed secrets and unsafe deployment commands
- stricter fixture validation

Limitations:
- no live deployment, no MCP servers, no mainnet approval workflow, and live Codex/Claude dogfood remains manual


## v0.1.0-internal

Internal hardening release for `evm-chain-engineering-pro`.

Adds or verifies:
- behavior eval matrix
- dogfood plan
- safety hooks
- deterministic policy guard
- hook validation
- golden demos
- upstream freshness checker
- subagent workflows
- release checklist
- release readiness checks
- expanded tests

No live deployment functionality was executed as part of this release.

## 0.1.0 - 2026-06-23

- Initial full repository scaffold for the EVM Chain Engineering Plugin.
- Added dual Codex and Claude manifests, 14 skills, shared references, safe scripts, templates, tests, evals, and documentation.
