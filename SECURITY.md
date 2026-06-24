# Security Policy

## Mainnet and Production Safety

This plugin must never be used to auto-deploy to mainnet, generate real private keys, store mnemonics, sign transactions, or move funds. Production-like requests require a threat model, security review, launch checklist, dry-run plan, rollback or pause plan, and explicit human approval.

## Reporting Issues

Report security problems privately to `user@example.com` until a project-specific security contact is configured. Do not include real private keys, mnemonics, production RPC secrets, wallet files, validator keys, Terraform state, or credentials in reports.

## Safe Defaults

- No real secrets in examples, docs, templates, logs, or tests.
- No public admin/debug RPC exposure.
- No `latest` Docker tags in production templates.
- No destructive scripts.
- All uncertain stack commands are marked `VERIFY_CURRENT_DOCS`.
