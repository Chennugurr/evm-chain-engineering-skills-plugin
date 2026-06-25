# Claude Manual Notes

- `claude plugin validate plugins/evm-chain-engineering-pro --strict` passed.
- The first historical stream invocation failed because Claude requires `--verbose` when using `--output-format stream-json`.
- The old `401 authentication_failed` blocker is resolved for discovery in `dogfood/issues/resolved/CLAUDE-AUTH-401.md`.
- This rerun loaded the local plugin, generated `GENERATED_ARTIFACTS/`, and exited successfully.
- The artifact bundle passed strict artifact validation, generated-config validation, known-bad output scanning, and strict secret scanning.
- Claude hook lifecycle events were captured in `CLAUDE_STREAM_REDACTED.jsonl`.
- No beta tag was created.

## 2026-06-25 Rerun Notes

- Triage doc: `docs/claude-auth-blocker-triage.md`
- `--bare` was not used.
- Raw stream was removed after redaction.
- The run stayed planning-only and did not create secrets, deployments, approval markers, or live infrastructure changes.
- `--allowedTools Read` was not used for this artifact run because the prior discovery run showed it did not reliably constrain Bash in this environment.
