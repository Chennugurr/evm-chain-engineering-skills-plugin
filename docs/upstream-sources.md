# Upstream Sources

Retrieval date: 2026-06-23

Use official docs as primary sources. Exact commands, supported versions, server sizing, and deployment steps remain version-sensitive and should be marked `VERIFY_CURRENT_DOCS` unless freshly verified.

## v0.3 strict live evidence doc refresh

Retrieval date: 2026-06-25

The v0.3 strict live evidence pass refreshed current platform docs before making plugin, hook, skill, or subagent claims.

| platform | topic | url | source_type | use | confidence | unstable_details |
|---|---|---|---|---|---|---|
| codex | plugin overview | https://developers.openai.com/codex/plugins | official docs | Plugin install/use surface and marketplace expectations | High | UI and CLI install flows can change. |
| codex | build plugins | https://developers.openai.com/codex/plugins/build | official docs and fetched Codex manual | Plugin packaging, marketplace shape, bundled hook behavior | High | Local validator behavior remains the final compatibility check. |
| codex | hooks | https://developers.openai.com/codex/hooks | official docs and fetched Codex manual | Hook discovery, trust review, event names, command hook limits | High | Hook trust and supported handler types are active platform behavior and must be live-tested. |
| codex | skills | https://developers.openai.com/codex/skills | official docs and fetched Codex manual | Skill package behavior and activation evidence expectations | High | Automatic activation telemetry can vary by surface. |
| codex | subagents | https://developers.openai.com/codex/subagents | official docs and fetched Codex manual | Subagent availability and evidence expectations | High | UI/CLI visibility and non-interactive behavior can differ. |
| codex | config reference | https://developers.openai.com/codex/config-reference | official docs and fetched Codex manual | Config and local runtime compatibility | High | Config keys evolve with CLI versions. |
| codex | advanced config | https://developers.openai.com/codex/config-advanced | official docs and fetched Codex manual | Hook and runtime configuration details | High | Advanced behavior is version-sensitive. |
| claude | plugins | https://code.claude.com/docs/en/plugins | official docs | Plugin packaging and live session install/use surface | High | CLI plugin loading and marketplace flows can change. |
| claude | plugins reference | https://code.claude.com/docs/en/plugins-reference | official docs | Manifest and plugin component compatibility | High | Strict validator remains the local compatibility check. |
| claude | hooks reference | https://code.claude.com/docs/en/hooks | official docs | Hook event schema and structured outputs | High | Event coverage and permission behavior can change. |
| claude | hooks guide | https://code.claude.com/docs/en/hooks-guide | official docs | Hook setup, `/hooks` visibility, limitations, and troubleshooting | High | Interactive hook browser behavior needs live evidence. |
| claude | skills | https://code.claude.com/docs/en/skills | official docs | Skill behavior in Claude Code | High | Skill invocation UI and telemetry can vary by version. |
| claude | subagents | https://code.claude.com/docs/en/sub-agents | official docs | Subagent behavior and platform limitations | High | Subagent use must be evidenced, not inferred silently. |
| claude | settings | https://code.claude.com/docs/en/settings | official docs | Settings and hook configuration locations | High | User/project/local setting precedence can change. |

## Codex manual - Agent Skills

- URL: https://developers.openai.com/codex/codex-manual.md
- Used for: Codex plugin, marketplace, and skill packaging defaults
- Confidence: High
- Notes: Fetched through the local openai-docs helper on 2026-06-23.

## Codex plugin validator reference

- URL: local-codex-plugin-creator://references/plugin-json-spec.md
- Used for: Codex manifest and marketplace validation shape
- Confidence: High
- Notes: Local system skill reference. Treat as current for this Codex install.

## Agent Skills specification

- URL: https://agentskills.io/specification
- Used for: Portable SKILL.md frontmatter, scripts, references, assets, progressive disclosure
- Confidence: High
- Notes: Skill metadata budgets and optional fields can evolve.

## Claude Code plugins

- URL: https://code.claude.com/docs/en/plugins
- Used for: Claude plugin purpose, namespacing, and local testing model
- Confidence: High
- Notes: Claude CLI behavior changes by version.

## Claude Code plugin reference

- URL: https://code.claude.com/docs/en/plugins-reference
- Used for: Claude plugin manifest fields and component paths
- Confidence: High
- Notes: Experimental components such as monitors can change.

## Claude Code plugin marketplaces

- URL: https://code.claude.com/docs/en/plugin-marketplaces
- Used for: Claude marketplace catalog shape
- Confidence: High
- Notes: Marketplace source types and validation may change.

## Claude Code skills

- URL: https://code.claude.com/docs/en/skills
- Used for: Claude skill frontmatter and invocation controls
- Confidence: High
- Notes: Claude-specific frontmatter is intentionally not used in portable skills.

## OP Stack docs

- URL: https://docs.optimism.io/
- Used for: OP Stack component model, deployment sequence, and role names
- Confidence: High
- Notes: Exact commands and supported client versions are version-sensitive.

## Arbitrum chains overview

- URL: https://docs.arbitrum.io/launch-arbitrum-chain/overview/introduction
- Used for: Orbit/Nitro feature model, DA modes, custom gas token and validation concepts
- Confidence: High
- Notes: Docs were recently updated; exact Chain SDK commands must be verified.

## Polygon CDK overview

- URL: https://docs.polygon.technology/chain-development/cdk/get-started/overview
- Used for: CDK modes, Agglayer integration, and execution clients
- Confidence: High
- Notes: CDK managed/self-managed details change quickly.

## ZKsync prover setup

- URL: https://docs.zksync.io/zk-stack/running/proving
- Used for: ZK Stack prover assumptions and default dummy executor warning
- Confidence: High
- Notes: Prover requirements and Airbender/Boojum status are version-sensitive.

## Ethereum nodes and clients

- URL: https://ethereum.org/developers/docs/nodes-and-clients/
- Used for: Ethereum-like L1 execution/consensus/validator split
- Confidence: High
- Notes: Client lists and networks change over time.

## BNB Smart Chain intro

- URL: https://docs.bnbchain.org/bnb-smart-chain/introduction/
- Used for: BSC EVM compatibility and PoSA validator model
- Confidence: High
- Notes: Validator counts and staking rules are version-sensitive.

## Cosmos EVM overview

- URL: https://docs.cosmos.network/evm/latest/documentation/overview
- Used for: Cosmos SDK and CometBFT EVM L1 model
- Confidence: High
- Notes: Module APIs and evmd CLI can change.

## Avalanche L1 docs

- URL: https://build.avax.network/docs/avalanche-l1s
- Used for: Avalanche L1/Subnet-EVM architecture and customization areas
- Confidence: High
- Notes: Avalanche naming and tooling changed from Subnets to L1s.

## Frontier docs

- URL: https://polkadot-evm.github.io/frontier/
- Used for: Polkadot/Substrate EVM compatibility path
- Confidence: Medium
- Notes: Frontier integration depends heavily on runtime version.

## Celestia docs

- URL: https://docs.celestia.org/
- Used for: Celestia DA and node operation references
- Confidence: High
- Notes: Network parameters and node commands change.

## Avail DA docs

- URL: https://docs.availproject.org/docs/da/concepts/what-is-avail-da
- Used for: Avail DA concept coverage
- Confidence: Medium
- Notes: Integration APIs and endpoints are version-sensitive.

## EigenDA docs

- URL: https://docs.eigencloud.xyz/eigenda/core-concepts/overview
- Used for: EigenDA concept coverage and network status
- Confidence: Medium
- Notes: Operator and rollup integration docs change quickly.

## Dymension RollApps quickstart

- URL: https://docs.dymension.xyz/launch/quickstart/
- Used for: RollApp and Roller quickstart assumptions
- Confidence: Medium
- Notes: Quickstart is development-focused, not production-ready.

## Sovereign SDK docs

- URL: https://docs.sovereign.xyz/
- Used for: Sovereign SDK rollup concepts
- Confidence: Medium
- Notes: Licensing and production guidance can change.

## Espresso docs

- URL: https://docs.espressosys.com/network/learn/espresso-in-the-modular-stack
- Used for: Shared sequencing and confirmation-layer assumptions
- Confidence: Medium
- Notes: The docs distinguish Espresso from a full shared sequencer; verify integrations.

## Structured Source Records

| stack | topic | url | source_type | dependent_skills | volatility | last_checked | checked_by | notes |
|---|---|---|---|---|---|---|---|---|
| codex | plugin hooks | https://developers.openai.com/codex/hooks | official docs | plugin-creator, chain-security-reviewer | volatile | 2026-06-24 | Codex | Codex plugin-bundled hook discovery and output shape. |
| codex | build plugins | https://developers.openai.com/codex/plugins/build | official docs | plugin-creator | volatile | 2026-06-24 | Codex | Codex manifest and marketplace packaging. |
| claude | plugin hooks | https://code.claude.com/docs/en/hooks | official docs | plugin-creator, chain-security-reviewer | volatile | 2026-06-24 | Codex | Claude hooks/hookSpecificOutput compatibility. |
| claude | plugins reference | https://code.claude.com/docs/en/plugins-reference | official docs | plugin-creator | volatile | 2026-06-24 | Codex | Claude plugin component defaults including hooks/hooks.json. |
| op-stack | deployment tutorials | https://docs.optimism.io/ | official docs | op-stack-engineer | volatile | 2026-06-23 | Codex | Exact commands require current-doc verification. |
| arbitrum-orbit | Orbit chains | https://docs.arbitrum.io/launch-arbitrum-chain/overview/introduction | official docs | arbitrum-orbit-engineer | volatile | 2026-06-23 | Codex | Chain SDK details change. |
| polygon-cdk | CDK overview | https://docs.polygon.technology/chain-development/cdk/get-started/overview | official docs | polygon-cdk-engineer | volatile | 2026-06-23 | Codex | Modes and managed deployment details change. |
| zksync | prover setup | https://docs.zksync.io/zk-stack/running/proving | official docs | zksync-zk-stack-engineer | volatile | 2026-06-23 | Codex | Hardware and prover stack are version-sensitive. |
