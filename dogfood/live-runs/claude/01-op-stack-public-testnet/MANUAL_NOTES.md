# Claude Manual Notes

- `claude plugin validate plugins/evm-chain-engineering-pro --strict` passed.
- The first stream invocation failed because Claude requires `--verbose` when using `--output-format stream-json`.
- The corrected invocation loaded the local plugin and reported 14 plugin skills available.
- The live agent request then failed with `401 authentication_failed`.
- No generated artifacts were produced by Claude.
- No beta tag was created.

## 2026-06-25 Auth Triage Update

- Canonical blocker issue: `dogfood/issues/open/CLAUDE-AUTH-401.md`
- Triage doc: `docs/claude-auth-blocker-triage.md`
- `claude auth status` reports logged in, with account identifiers redacted from committed evidence.
- A no-plugin `claude --print` request also fails with `401 authentication_failed`, so the blocker is classified as noninteractive Claude auth/session execution rather than plugin-specific behavior.
- `--bare` was not used for plugin discovery or smoke evidence.
- No managed settings file was found in common locations; hook behavior remains unverified because auth fails before execution.
