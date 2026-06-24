# Safety Model

The plugin treats blockchain infrastructure as high risk by default.

## Hard Gates

- No real private keys, mnemonics, API tokens, keystore passwords, or Terraform state.
- No automatic deployment commands.
- No mainnet or production action without explicit human approval.
- No public admin/debug RPC.
- No `latest` Docker tags in production templates.
- No claim of production readiness without security review and launch checklist.

## Required Reviews

Invoke `chain-security-reviewer` for mainnet, production, public testnet, bridges, admin keys, validators, sequencers, provers, relayers, custom precompiles, public RPC, or value-bearing workflows.
