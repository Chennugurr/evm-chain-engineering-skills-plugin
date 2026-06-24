# Upstream Sources

Retrieval date: 2026-06-23

Use official docs as primary sources. Exact commands, supported versions, server sizing, and deployment steps remain version-sensitive and should be marked `VERIFY_CURRENT_DOCS` unless freshly verified.

## Codex manual - Agent Skills

- URL: https://developers.openai.com/codex/codex-manual.md
- Used for: Codex plugin, marketplace, and skill packaging defaults
- Confidence: High
- Notes: Fetched through the local openai-docs helper on 2026-06-23.

## Codex plugin validator reference

- URL: file:///home/iljanemesis/.codex/skills/.system/plugin-creator/references/plugin-json-spec.md
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
