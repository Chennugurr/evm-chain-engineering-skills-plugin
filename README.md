# EVM Chain Engineering Pro

## What this plugin is

A dual Codex and Claude Code plugin bundle for planning, validating, securing, and operating EVM L1s, L2s, L3s, appchains, rollups, bridges, explorers, faucets, and infrastructure.

## What it is not

- It is not an automatic mainnet deployer.
- It does not store or manage private keys.
- It does not replace audits.
- It does not make stale stack docs safe.
- It does not make OP Stack, Arbitrum Orbit, Polygon CDK, ZKsync ZK Stack, Cosmos EVM, Avalanche L1s, and modular rollups interchangeable.

## Supported workflows

Architecture decision records, stack selection, server topology, bridge risk review, DA selection, launch gates, observability planning, dry-run validation, docs review, behavior evals, and release readiness.

## Repository layout

- `plugins/evm-chain-engineering-pro/skills`: 14 portable skills.
- `plugins/evm-chain-engineering-pro/references`: shared stack references.
- `plugins/evm-chain-engineering-pro/scripts`: plugin-packaged safe helper scripts and hook policy guard wrapper.
- `scripts`: root-level hardening orchestration scripts.
- `evals`: deterministic behavior eval matrix.
- `examples/golden-demos`: safe model answers for dogfooding.

## Install/view in Codex

Use `.agents/plugins/marketplace.json`, restart Codex, then view or install `evm-chain-engineering-pro` from the EVM Chain Engineering marketplace.

## Install/view in Claude Code

Use `.claude-plugin/marketplace.json` or validate the local plugin directly with:

```bash
claude plugin validate plugins/evm-chain-engineering-pro --strict
```

## Skill list

`blockchain-architect`, `evm-l1-builder`, `op-stack-engineer`, `arbitrum-orbit-engineer`, `polygon-cdk-engineer`, `zksync-zk-stack-engineer`, `modular-rollup-engineer`, `data-availability-engineer`, `bridge-interop-engineer`, `chain-infra-ops`, `observability-sre`, `chain-security-reviewer`, `chain-launch-manager`, and `explorer-indexer-engineer`.

## Safety model

Dry-run first, no secrets in repo, policy guard hooks, mainnet-like actions approval-gated, chain-specific trust assumptions documented, and production launch requires human review.

## Dogfood workflow

Use `docs/dogfood-plan.md`, run the prompts from `evals/skill-trigger-matrix.yaml`, and record results in `docs/usage-review.md`.

## Behavior evals

```bash
python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict
```

## Golden demos

Six demos live in `examples/golden-demos/` and provide safe, dry-run expected outputs.

## Upstream source freshness

```bash
python3 scripts/check_upstream_freshness.py --sources docs/upstream-sources.md --markdown-report docs/upstream-freshness-report.md --allow-offline
```

## Release validation

```bash
make validate-all
```

## Known limitations

Exact deployment commands, server requirements, client versions, bridge instructions, and stack modes remain version-sensitive and require `VERIFY_CURRENT_DOCS` before production-like use.

## v0.2.0-alpha Workflow Acceptance

v0.2 adds a machine-checkable artifact bundle contract, stack profiles, safe artifact generators, validated fixture bundles, generated config validation, workflow acceptance cases, hook fixture tests, clean install validation, and release evidence.

Quick commands:

```bash
make validate-v02
python3 scripts/render_artifact_bundle.py --workflow op-stack-public-testnet --stack op-stack --chain-type l2 --environment public-testnet --settlement sepolia --output generated/op-stack-public-testnet --overwrite
python3 scripts/validate_artifact_bundle.py --strict --path generated/op-stack-public-testnet
```

The layer remains planning-only: no deployment, no real secrets, no cloud/provider calls, no MCP servers, and no production certification. See `KNOWN_LIMITATIONS.md`.

## v0.3.0-beta Live Agent QA Harness

v0.3 adds the evidence harness for live Codex and Claude dogfood: prompts, expected contracts, transcript schemas, live-run package validation, hook observation checks, skill routing scorecards, known-bad output checks, and release evidence.

Current strict-evidence status:

- Codex smoke run `01-op-stack-public-testnet`: captured and validated under `dogfood/live-runs/codex/01-op-stack-public-testnet/`.
- Claude smoke run `01-op-stack-public-testnet`: blocked by `401 authentication_failed` after plugin discovery under `dogfood/live-runs/claude/01-op-stack-public-testnet/`.
- Live hook observation: still pending.
- `v0.3.0-beta` tag: not created.

Bootstrap mode validates the harness plus any captured smoke evidence:

```bash
make validate-v03-bootstrap
```

Strict mode is intentionally blocked until real live evidence is captured:

```bash
make validate-v03
```

Do not tag `v0.3.0-beta` until strict validation passes with the required Codex and Claude transcripts, hook observations, validated generated artifact bundles, and release evidence.
