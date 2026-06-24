# Claude Manual Notes

- `claude plugin validate plugins/evm-chain-engineering-pro --strict` passed.
- The first stream invocation failed because Claude requires `--verbose` when using `--output-format stream-json`.
- The corrected invocation loaded the local plugin and reported 14 plugin skills available.
- The live agent request then failed with `401 authentication_failed`.
- No generated artifacts were produced by Claude.
- No beta tag was created.
