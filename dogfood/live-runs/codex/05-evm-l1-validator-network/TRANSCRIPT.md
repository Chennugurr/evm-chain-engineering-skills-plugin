# Live Transcript (codex)

- Platform: codex
- Prompt ID: 05-evm-l1-validator-network
- Capture date: 2026-06-25
- Raw stream retained outside repo: <TMP>/v03-codex-05.raw.jsonl
- Committed stream: CODEX_STREAM_REDACTED.jsonl

## Assistant Response

## Selected skills

blockchain-architect, evm-l1-builder, chain-infra-ops, chain-security-reviewer

## Planning answer

### ADR

Design a native **L1** PoSA-style EVM appchain testnet with a permissioned initial **validator set**, deterministic **genesis**, public read infrastructure, and explicit **launch gates** before any public use.

Decision: use a small, known validator set for the first testnet, with governance-controlled validator admission and removal. This favors operational safety, fast recovery, and clear accountability over open participation during the test phase.

Non-goals: production readiness, production-network launch approval, live infrastructure deployment, validator key creation, or publication of key material.

### Chain spec

| Area | Testnet plan |
|---|---|
| Chain type | Native EVM L1 / appchain |
| Consensus | PoSA-style authority/staked-validator consensus |
| Native token | Single gas and staking token, testnet-only supply |
| Chain ID | Use a unique, preflight-checked chain ID not colliding with known networks |
| Genesis | Deterministic genesis file with validator addresses, allocations, fork config, gas settings, and governance contracts if needed |
| Validator set | 4-7 initial validators, independent operators preferred |
| Validator economics | Testnet staking weights, reward simulation, slashing policy modeled but not economically binding |
| Governance | Multisig or council-controlled testnet governance for validator changes and emergency parameter updates |
| Bootnodes | 2-3 independently hosted bootnodes, no validator signer keys on bootnode hosts |
| RPC | Public read RPC plus private validator RPC separation |
| Explorer | Block explorer connected to archive/indexing RPC, contract verification enabled if practical |

### Validator design

Initial validator set should include separate organizations or at least separately operated environments. Each validator should have distinct networking, monitoring, and operational ownership.

Validator signer separation is required: consensus-signing material must be isolated from public RPC, explorer, bootnode, CI, and general admin hosts. This plan does not create keys or specify key storage recipes.

Validator economics for testnet should model:

| Topic | Plan |
|---|---|
| Minimum stake | Fixed testnet threshold |
| Rewards | Simulated block rewards for accounting and explorer visibility |
| Penalties | Dry-run slashing events only unless explicitly approved |
| Jailing/removal | Governance-controlled for testnet |
| Delegation | Defer unless required for ecosystem testing |

### Genesis and launch package

The testnet package should include:

- ADR describing L1 architecture, consensus choice, governance assumptions, and non-production scope.
- Chain spec with chain ID, native token symbol, fork schedule, gas rules, validator set, and genesis allocation policy.
- Genesis validation checklist with deterministic hash comparison across operators.
- Bootnode list with peer IDs and network endpoints only, no private material.
- RPC topology describing public, private, archive, and explorer-facing endpoints.
- Explorer/indexer plan.
- Governance procedure for validator add/remove, parameter changes, and emergency halt.
- Launch gates with required approvals before public announcement.

## Security review

This testnet must not be represented as production-safe. Human security review is required before any public or value-bearing use.

Required controls:

- Separate validator signing from RPC, explorer, bootnode, monitoring, and deployment systems.
- Run dry-run validation of genesis, validator startup, peer discovery, block production, restarts, validator removal, and chain recovery.
- Confirm chain ID uniqueness before launch.
- Confirm no private keys, mnemonics, secrets, or signer material appear in repositories, configs, docs, logs, or artifacts.
- Confirm governance authority is documented, limited, and auditable.
- Confirm public RPC has rate limits, method restrictions, and no admin/debug exposure.
- Confirm explorer uses read-only infrastructure.
- Confirm validator operators understand halt, restart, and incident procedures.

Launch must be blocked if any of these are unresolved:

- Chain ID collision risk.
- Non-deterministic genesis hash across operators.
- Validator signer material present on public infrastructure.
- Public RPC exposes privileged methods.
- Governance authority is unclear.
- No tested recovery path for failed validators.
- No human security review sign-off.

## Validation notes

Planning-only validation performed against the requested scope.

No files were edited. No commands were run. No validator keys were created. No infrastructure was deployed.

Recommended launch gate sequence:

1. ADR approved.
2. Chain spec reviewed.
3. Genesis generated and independently hash-verified.
4. Validator dry run completed.
5. Bootnodes and RPC tested without signer co-location.
6. Explorer synced from read-only infrastructure.
7. Governance procedures tested on testnet.
8. Security review completed.
9. Human go/no-go approval recorded.
