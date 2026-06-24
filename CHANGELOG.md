# Changelog

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
