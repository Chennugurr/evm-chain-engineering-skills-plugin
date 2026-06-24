# Skill Inventory

This inventory uses the actual 14 skill directories in the repo. Prompt-only intents such as chain-economics-tokenomics, chain-governance-upgrades, chain-observability-sre, and chain-docs-release-manager are mapped into existing skills rather than creating new skill directories.

## `arbitrum-orbit-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/arbitrum-orbit-engineer`
- Frontmatter name: `arbitrum-orbit-engineer`
- Frontmatter description: Engineer Arbitrum Orbit and Nitro chains, Rollup and AnyTrust modes, L2 or L3 settlement, parent-chain selection, custom gas tokens, validators, batch posting, delayed inbox, sequencer feed, Stylus considerations, and Orbit bridge limits. Use for Arbitrum chain launch, config, or ops. Do not use for OP Stack, Polygon CDK, ZK Stack, or generic L1 builds.
- Intended trigger phrases: engineer Arbitrum Orbit and Nitro chains,  Rollup and AnyTrust modes,  L2 or L3 settlement,  parent-chain selection,  custom gas tokens,  validators.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `anytrust-and-dacs.md`, `custom-gas-token.md`, `delayed-inbox-and-bridge.md`, `l2-vs-l3-settlement.md`, `orbit-and-nitro-architecture.md`, `orbit-server-topology.md`, `orbit-troubleshooting.md`, `parent-chain-selection.md`, `rollup-vs-anytrust.md`, `stylus-considerations.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `blockchain-architect`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/blockchain-architect`
- Frontmatter name: `blockchain-architect`
- Frontmatter description: Design and classify EVM L1s, L2s, L3s, appchains, rollups, validiums, sidechains, settlement, DA, proof, sequencing, gas token, and governance choices. Use when a user asks what chain to build, compares stacks, or needs an architecture decision record. Do not use for generic Solidity app work unless chain architecture is involved.
- Intended trigger phrases: design and classify EVM L1s,  L2s,  L3s,  appchains,  rollups,  validiums.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `architecture-decision-record.md`, `chain-id-and-replay-protection.md`, `l1-vs-l2-vs-l3.md`, `security-models.md`, `stack-selection-matrix.md`, `trust-assumption-matrix.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `bridge-interop-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/bridge-interop-engineer`
- Frontmatter name: `bridge-interop-engineer`
- Frontmatter description: Engineer bridges, canonical bridges, native bridges, L2/L3 bridging, cross-chain messaging, relayers, token mapping, chain metadata, wallet onboarding, bridge monitoring, and bridge security assumptions. Use when moving assets or messages between chains, exposing a bridge UI, or mapping tokens. Do not use without also invoking security review for production, public testnet, or TVL-bearing bridge work.
- Intended trigger phrases: engineer bridges,  canonical bridges,  native bridges,  L2/L3 bridging,  cross-chain messaging,  relayers.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `bridge-and-interoperability.md`, `bridge-monitoring.md`, `bridge-security.md`, `canonical-bridges.md`, `chainlist-and-wallets.md`, `cross-chain-messaging.md`, `l2-l3-bridging.md`, `native-bridges.md`, `relayers.md`, `token-mapping.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `chain-infra-ops`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/chain-infra-ops`
- Frontmatter name: `chain-infra-ops`
- Frontmatter description: Design blockchain infrastructure operations for sequencers, batchers, proposers, validators, provers, RPC nodes, archive nodes, explorers, faucets, bridges, relayers, DA nodes, monitoring, backups, Ubuntu, Docker Compose, systemd, Kubernetes, Terraform, Ansible, Nginx, TLS, firewalls, and incident response. Use for server setup or production topology. Do not use for protocol choice without blockchain-architect.
- Intended trigger phrases: design blockchain infrastructure operations for sequencers,  batchers,  proposers,  validators,  provers,  RPC nodes.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `ansible.md`, `bare-metal-vs-cloud.md`, `disaster-recovery.md`, `docker-compose.md`, `firewalls-and-networking.md`, `kubernetes.md`, `load-balancing.md`, `server-sizing.md`, `snapshots-and-backups.md`, `systemd.md`, `terraform.md`, `tls-and-nginx.md`, ...
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `chain-launch-manager`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/chain-launch-manager`
- Frontmatter name: `chain-launch-manager`
- Frontmatter description: Manage chain launch planning for devnet, public testnet, mainnet candidate, mainnet launch, governance handoff, ecosystem onboarding, launch communications, incident readiness, rollback, pause procedures, and post-launch operations. Use for launch checklists and go/no-go processes. Do not use to bypass security review or generate mainnet deploy commands directly.
- Intended trigger phrases: Manage chain launch planning for devnet,  public testnet,  mainnet candidate,  mainnet launch,  governance handoff,  ecosystem onboarding.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `ecosystem-onboarding.md`, `governance-handoff.md`, `incident-response.md`, `l1-launch-runbook.md`, `launch-communications.md`, `launch-phases.md`, `mainnet-candidate.md`, `mainnet-launch.md`, `mainnet-readiness.md`, `post-launch-ops.md`, `testnet-launch.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `chain-security-reviewer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/chain-security-reviewer`
- Frontmatter name: `chain-security-reviewer`
- Frontmatter description: Review blockchain and rollup security for mainnet, production, public testnet, bridges, admin keys, validators, sequencers, provers, relayers, custom precompiles, upgrade controls, DA trust, fraud or validity proofs, exposed RPC, key custody, and launch readiness. Use whenever the request involves real users, value, public infrastructure, or unsafe shortcuts. Do not use to bless production without findings and go/no-go criteria.
- Intended trigger phrases: Review blockchain and rollup security for mainnet,  production,  public testnet,  bridges,  admin keys,  validators.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `audit-preparation.md`, `bridge-security.md`, `genesis-review.md`, `governance-and-upgrades.md`, `key-management.md`, `mainnet-readiness.md`, `plugin-agent-security.md`, `precompile-review.md`, `rpc-security.md`, `supply-chain-security.md`, `threat-model.md`, `upgrade-admin.md`, ...
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `data-availability-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/data-availability-engineer`
- Frontmatter name: `data-availability-engineer`
- Frontmatter description: Design and review data availability for rollups, validiums, sovereign rollups, appchains, Ethereum calldata and blobs, Celestia, Avail, EigenDA, private DA, DACs, Alt-DA, DA cost models, DA monitoring, and DA failure modes. Use when DA choice, DA trust, or DA operations are material. Do not use for generic node setup without a DA decision.
- Intended trigger phrases: design and review data availability for rollups,  validiums,  sovereign rollups,  appchains,  Ethereum calldata and blobs,  Celestia.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `avail-da.md`, `blobspace-and-calldata.md`, `celestia-da.md`, `da-cost-models.md`, `da-failure-modes.md`, `da-monitoring.md`, `da-selection-guide.md`, `dac-and-da-models.md`, `eigenda.md`, `ethereum-da.md`, `private-da.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `evm-l1-builder`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/evm-l1-builder`
- Frontmatter name: `evm-l1-builder`
- Frontmatter description: Build and review EVM L1 chains including Ethereum-like execution plus consensus clients, BNB-style PoSA, Cosmos EVM, Avalanche L1/Subnet-EVM, and Polkadot Frontier. Use for genesis, chain IDs, validators, fork schedules, precompiles, RPC, gas token, staking, slashing, and L1 launch planning. Do not use for OP Stack, Orbit, CDK, or ZK Stack rollups.
- Intended trigger phrases: Build and review EVM L1 chains including Ethereum-like execution plus consensus clients,  BNB-style PoSA,  Cosmos EVM,  Avalanche L1/Subnet-EVM,  and Polkadot Frontier.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `avalanche-l1-subnet-evm.md`, `bnb-style-posa-l1.md`, `consensus-and-finality.md`, `cosmos-evm-l1.md`, `ethereum-like-l1.md`, `fork-schedule-and-upgrades.md`, `genesis-config.md`, `polkadot-frontier-evm.md`, `precompiles.md`, `validator-economics.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `explorer-indexer-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/explorer-indexer-engineer`
- Frontmatter name: `explorer-indexer-engineer`
- Frontmatter description: Engineer block explorers, indexers, Blockscout, subgraphs, RPC indexing, faucets, wallet and Chainlist metadata, chain registry entries, token lists, bridge frontends, contract verification, developer APIs, and ecosystem onboarding surfaces. Use when a chain needs explorer, faucet, wallet, metadata, or indexer setup. Do not use for core consensus or rollup protocol design.
- Intended trigger phrases: engineer block explorers,  indexers,  Blockscout,  subgraphs,  RPC indexing,  faucets.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `blockscout.md`, `chain-metadata.md`, `chainlist-and-wallets.md`, `contract-verification.md`, `developer-apis.md`, `explorer-faucet-rpc.md`, `explorer-options.md`, `faucets.md`, `rpc-and-indexing.md`, `subgraphs-and-data.md`, `token-lists.md`, `wallet-and-chainlist.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `modular-rollup-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/modular-rollup-engineer`
- Frontmatter name: `modular-rollup-engineer`
- Frontmatter description: Engineer modular rollups, sovereign rollups, Rollkit, Sovereign SDK, Dymension RollApps, Celestia DA, Avail DA, EigenDA, shared sequencing, RaaS assumptions, and compatibility matrices. Use when the user wants all available stacks, modular architecture, or sovereign/appchain options. Do not use as a substitute for stack-specific OP Stack, Orbit, CDK, ZK Stack, or L1 skills when a stack is already chosen.
- Intended trigger phrases: engineer modular rollups,  sovereign rollups,  Rollkit,  Sovereign SDK,  Dymension RollApps,  Celestia DA.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `avail-da.md`, `celestia-da.md`, `dymension-rollapps.md`, `eigenda.md`, `modular-rollup-mainnet-readiness.md`, `modular-rollup-server-topology.md`, `modular-stack-registry.md`, `rollkit.md`, `shared-sequencing.md`, `sovereign-sdk.md`, `sovereign-vs-settled-rollups.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `observability-sre`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/observability-sre`
- Frontmatter name: `observability-sre`
- Frontmatter description: Design observability and SRE systems for EVM chains, rollups, RPC gateways, sequencers, batchers, proposers, provers, validators, bridges, explorers, Prometheus, Grafana, Alertmanager, Loki, OpenTelemetry, health checks, SLOs, SLAs, status pages, and incident signals. Use for monitoring and reliability work. Do not use as a replacement for security review or infrastructure planning.
- Intended trigger phrases: design observability and SRE systems for EVM chains,  rollups,  RPC gateways,  sequencers,  batchers,  proposers.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `grafana-dashboard-design.md`, `grafana-dashboards.md`, `logs-and-loki.md`, `logs-and-tracing.md`, `metrics-catalog.md`, `monitoring.md`, `prometheus-alerts.md`, `rollup-health-checks.md`, `rpc-health-checks.md`, `slo-and-sla-models.md`, `status-pages.md`, `tracing.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `op-stack-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/op-stack-engineer`
- Frontmatter name: `op-stack-engineer`
- Frontmatter description: Engineer OP Stack chains, Optimism-style L2s, Superchain-compatible rollups, OP Stack devnets, op-node, op-geth, op-reth, op-batcher, op-proposer, sequencer, challenger, bridge, Alt-DA, and production server topology. Use for OP Stack deployment or troubleshooting. Do not use for Arbitrum Orbit, Polygon CDK, ZKsync ZK Stack, or EVM L1s.
- Intended trigger phrases: engineer OP Stack chains,  Optimism-style L2s,  Superchain-compatible rollups,  OP Stack devnets,  op-node,  op-geth.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `alt-da.md`, `fault-proofs-and-challenger.md`, `op-deployment-runbook.md`, `op-node-op-geth-op-reth.md`, `op-stack-architecture.md`, `op-stack-server-topology.md`, `op-stack-troubleshooting.md`, `sequencer-batcher-proposer.md`, `superchain-compatibility.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `polygon-cdk-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/polygon-cdk-engineer`
- Frontmatter name: `polygon-cdk-engineer`
- Frontmatter description: Engineer Polygon CDK chains, Agglayer-connected L2s, sovereign mode, validium mode, private validium, zkRollup planning, op-geth, op-reth, DA committees, privacy controls, bridge monitoring, and production operations. Use for CDK stack choices and CDK infra. Do not use for OP Stack-only, Orbit-only, ZK Stack-only, or L1-only requests.
- Intended trigger phrases: engineer Polygon CDK chains,  Agglayer-connected L2s,  sovereign mode,  validium mode,  private validium,  zkRollup planning.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `agglayer.md`, `cdk-architecture.md`, `cdk-mainnet-readiness.md`, `cdk-server-topology.md`, `cdk-troubleshooting.md`, `data-availability-committee.md`, `private-da.md`, `sovereign-validium-zkrollup-modes.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## `zksync-zk-stack-engineer`

- Skill directory: `plugins/evm-chain-engineering-pro/skills/zksync-zk-stack-engineer`
- Frontmatter name: `zksync-zk-stack-engineer`
- Frontmatter description: Engineer ZKsync ZK Stack chains, ZK Chains, rollup versus validium modes, custom base tokens, sequencer/server components, prover setup, L1 contracts, bootloader and system contracts, bridge, fee model, and proof operations. Use for ZK Stack deployment, prover sizing, and monitoring. Do not use for optimistic rollups, CDK-only, Orbit-only, or EVM L1-only requests.
- Intended trigger phrases: engineer ZKsync ZK Stack chains,  ZK Chains,  rollup versus validium modes,  custom base tokens,  sequencer/server components,  prover setup.
- Should-trigger examples: requests that use the stack/subsystem terms in the description and ask for architecture, operations, validation, launch, or safety work.
- Should-not-trigger examples: generic Solidity application work, generic cloud work, or another stack explicitly excluded by the description.
- Related references: `custom-base-token.md`, `elastic-chain-and-interoperability.md`, `prover-setup.md`, `sequencer-rpc-prover-aggregator.md`, `system-contracts-and-bootloader.md`, `zk-chain-types.md`, `zk-stack-architecture.md`, `zk-stack-server-topology.md`, `zk-stack-troubleshooting.md`
- Related scripts/templates: root hardening scripts plus plugin-local validators/renderers relevant to the requested stack.
- Safety notes: route production, mainnet, public testnet, bridge, admin key, validator, sequencer, prover, relayer, custom precompile, or public RPC requests through `chain-security-reviewer`.

## Trigger Collision Analysis

- `blockchain-architect` vs `modular-rollup-engineer`: acceptable overlap. Use architect for broad L1/L2/L3 decisions; use modular when the prompt explicitly asks for Rollkit, Dymension, Sovereign SDK, DA layers, or modular compatibility.
- `chain-infra-ops` vs `observability-sre`: acceptable overlap. Infrastructure owns hosts/runtime/backups/firewall; observability owns SLI/SLO, metrics, alerts, dashboards, logs, and status workflows.
- `chain-security-reviewer` vs governance/release intents: governance and release are mapped to `chain-launch-manager` plus `chain-security-reviewer`; security remains the launch blocker authority.
- `op-stack-engineer` vs `polygon-cdk-engineer`: both can mention op-geth/op-reth. CDK should trigger only when Polygon CDK, Agglayer, validium, sovereign, or CDK modes appear; OP Stack should trigger on Optimism, Superchain, op-node, op-batcher, or op-proposer.
- `arbitrum-orbit-engineer` vs generic L3 prompts: generic L3 prompts start with `blockchain-architect`; Orbit triggers when Arbitrum, Orbit, Nitro, AnyTrust, delayed inbox, or Arbitrum parent chain is present.

No skill renames are required for v0.1 internal hardening.
