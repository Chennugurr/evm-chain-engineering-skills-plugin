# Claude Auth Blocker Triage

## Status

- Date: 2026-06-25
- Issue: `dogfood/issues/resolved/CLAUDE-AUTH-401.md`
- Classification: resolved for discovery
- Release impact: `v0.3.0-beta` must remain untagged until the remaining strict evidence matrix, Codex hook evidence, and subagent evidence are captured.

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
- A no-plugin `claude --print` request returned assistant text `ok`; the command exited nonzero only because the budget cap was too low.
- The plugin discovery request succeeded with `--plugin-dir plugins/evm-chain-engineering-pro` and without `--bare`.
- The plugin discovery init event reported the plugin loaded and 14 plugin skills visible.
- The discovery run directly invoked `evm-chain-engineering-pro:blockchain-architect`.
- The discovery JSONL stream recorded `PreToolUse:Bash` hook lifecycle events and policy guard allow decisions.

## Interpretation

The original blocker was auth/session execution for Claude Code noninteractive agent calls. It is now resolved for discovery because both no-plugin agent text generation and plugin-dir discovery completed without a 401.

The remaining release blockers are no longer Claude auth or the OP Stack smoke. They are the broader strict matrix, Codex hook evidence, and subagent evidence.

## Required Checklist

- Exact date recorded: yes, 2026-06-25.
- Claude Code surface recorded: yes, CLI.
- Command used recorded with secrets redacted: yes.
- Plugin path recorded: yes, `plugins/evm-chain-engineering-pro`.
- Local plugin validation works: yes.
- Interactive Claude Code login works: not rerun; `claude auth status` reports logged in, so no token/login flow was attempted.
- Failure auth-only or plugin-specific: previously auth-only for noninteractive execution; now resolved for discovery.
- `--bare` accidentally used: no. `--bare` was not used for plugin discovery or smoke evidence.
- Managed settings block plugin hooks: no managed settings file found in common locations; no hook/plugin policy keys found in user settings. Discovery captured hook lifecycle events.
- Reproducible from clean shell: auth status is reproducible from a clean shell; the latest no-plugin run reached assistant output.
- Another authenticated account/environment can reproduce: not tested.

## Safe Auth Rules

- Do not paste tokens into transcripts.
- Do not commit auth files.
- Do not commit screenshots containing account IDs, emails, tokens, workspace IDs, or private URLs.
- Redact all environment variables that might contain credentials.
- Record only whether authentication succeeded or failed.

## Next Action

The Claude Code noninteractive 401 is resolved for discovery and the OP Stack artifact smoke. Continue the remaining live prompt matrix with the same noninteractive pattern:

```bash
claude --print --verbose --output-format stream-json --include-hook-events --plugin-dir plugins/evm-chain-engineering-pro ...
```

Capture each refreshed package under `dogfood/live-runs/claude/<prompt-id>/` and keep only redacted evidence.
