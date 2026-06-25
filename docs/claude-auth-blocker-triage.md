# Claude Auth Blocker Triage

## Status

- Date: 2026-06-25
- Issue: `dogfood/issues/open/CLAUDE-AUTH-401.md`
- Classification: blocker
- Release impact: `v0.3.0-beta` must remain untagged until resolved or the milestone is explicitly redefined.

## Surface

- Claude Code surface used: CLI
- CLI version: `2.1.185 (Claude Code)`
- CLI path: `<HOME>/.local/bin/claude`
- Desktop/IDE/SDK evidence: not captured in this pass

## Commands Checked

Secrets, account identifiers, emails, organization IDs, and private URLs are intentionally omitted.

```bash
claude auth status
env -i HOME="$HOME" PATH="$PATH" SHELL="$SHELL" claude auth status
claude plugin validate plugins/evm-chain-engineering-pro --strict
claude --print --verbose --output-format stream-json --max-budget-usd 0.05 'Reply with the single word ok.'
claude --print --verbose --output-format stream-json --include-hook-events --plugin-dir plugins/evm-chain-engineering-pro ...
```

## Findings

- `claude auth status` reports `loggedIn: true`.
- Auth method is first-party Claude auth; account identifiers are redacted.
- The clean-shell auth status check also reports logged in.
- No `ANTHROPIC_*`, `CLAUDE_*`, API-key, token, or auth credential environment variables were present in the shell environment checked for this pass.
- `claude plugin validate plugins/evm-chain-engineering-pro --strict` passes.
- A no-plugin `claude --print` request fails with `401 authentication_failed`.
- The plugin-dir smoke request also fails with `401 authentication_failed`.
- The plugin-dir smoke init event previously reported the plugin loaded and 14 plugin skills visible before the API request failed.

## Interpretation

The current blocker is auth/session execution for Claude Code noninteractive agent calls. It is not currently plugin-specific because the no-plugin `claude --print` request also fails with the same 401.

## Required Checklist

- Exact date recorded: yes, 2026-06-25.
- Claude Code surface recorded: yes, CLI.
- Command used recorded with secrets redacted: yes.
- Plugin path recorded: yes, `plugins/evm-chain-engineering-pro`.
- Local plugin validation works: yes.
- Interactive Claude Code login works: not rerun; `claude auth status` reports logged in, so no token/login flow was attempted.
- Failure auth-only or plugin-specific: classified as auth-only for noninteractive execution.
- `--bare` accidentally used: no. `--bare` was not used for plugin discovery or smoke evidence.
- Managed settings block plugin hooks: no managed settings file found in common locations; no hook/plugin policy keys found in user settings. Hook behavior remains unverified because auth fails before execution.
- Reproducible from clean shell: auth status is reproducible from a clean shell; no-plugin noninteractive execution still fails with 401 in the normal shell.
- Another authenticated account/environment can reproduce: not tested.

## Safe Auth Rules

- Do not paste tokens into transcripts.
- Do not commit auth files.
- Do not commit screenshots containing account IDs, emails, tokens, workspace IDs, or private URLs.
- Redact all environment variables that might contain credentials.
- Record only whether authentication succeeded or failed.

## Next Action

Resolve the Claude Code noninteractive 401 outside the repo, then rerun:

```bash
claude --print --verbose --output-format stream-json --plugin-dir plugins/evm-chain-engineering-pro ...
```

If the command succeeds, capture `dogfood/live-runs/claude/00-plugin-discovery/` before rerunning the OP Stack smoke package.
