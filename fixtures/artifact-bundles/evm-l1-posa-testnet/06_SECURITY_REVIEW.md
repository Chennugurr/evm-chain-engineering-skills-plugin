# Security Review: Example EVM L1 PoSA Testnet

## Scope

Planning-only review. Not an audit or production certification.

## Findings

| Severity | Area | Finding | Required Mitigation |
|---|---|---|---|
| high | keys | deployer/operator keys cannot live in repo | use KMS/HSM/hardware signer or signer service |
| high | RPC | admin/debug RPC must not be public | bind privately and firewall |
| high | bridge/settlement | bridge assumptions can dominate risk | external bridge/security review required |

## Secrets Policy

No private keys, mnemonics, keystore passwords, or deployer secrets may be committed. Use <INJECT_FROM_SECURE_SIGNER_AT_RUNTIME>.

## Signer/Key Custody

Use KMS/HSM/hardware wallet/signer service. CLI private-key flags are forbidden.

## Bridge Risks

Bridge contracts, relayers, fraud/validity windows, and parent-chain finality require external review.

## Admin/Upgrade Risks

Admin keys require multisig/timelock or documented custody before production/mainnet.

## Sequencer Risks

Censorship, downtime, ordering, and centralization risks remain open until reviewed.

## DA Risks

DA mode `native-chain` requires explicit failure-mode review.

## Validator/Prover Risks

Validator/prover assumptions are relevant when those roles are present and must be verified against current docs.

## RPC Exposure Risks

Public RPC must not expose admin, debug, personal, or engine APIs.

## Generated Artifact Limitations

This bundle is not an audit, not a launch approval, and not production certification.

## Required External Reviews

Protocol review, infrastructure review, bridge review, incident drill, and legal/compliance review where applicable.
