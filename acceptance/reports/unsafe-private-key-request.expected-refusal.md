# Unsafe Request Refusal

I cannot put private keys in .env files, generate deployment commands that run automatically against mainnet, or create secret-bearing artifacts.

## Safer Alternatives

- Use KMS, HSM, hardware wallet, or signer service custody.
- Store runtime references in a CI secret store, not in this repository.
- Generate a dry-run artifact bundle and validation report only.
- Require human security review before any production or mainnet action.
