# Contributing

Contributions should preserve the plugin's safety model and progressive disclosure design.

## Requirements

- Keep skill frontmatter portable with `name` and `description` only.
- Put detailed stack content in reference files, not giant SKILL.md bodies.
- Mark exact commands, versions, server requirements, and addresses as `VERIFY_CURRENT_DOCS` unless verified from current official docs.
- Add or update tests for manifests, skills, references, scripts, templates, and safety checks.
- Run `python3 -m pytest` before opening changes.

## Prohibited Content

Do not commit real private keys, mnemonics, API tokens, RPC provider secrets, Terraform state, keystore passwords, production endpoints with credentials, or deployment commands that execute mainnet changes.
