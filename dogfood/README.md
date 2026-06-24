# v0.3 Live Dogfood

This directory contains the v0.3.0-beta live agent QA harness. It is designed to prove behavior with real Codex and Claude sessions without making deployment claims from tests alone.

Bootstrap validation accepts pending live evidence. Strict validation requires transcript-backed live runs, hook observations, skill routing evidence, validated generated artifact bundles, and a release evidence summary.

Rules:

- Do not fabricate transcripts, hook observations, generated artifacts, or subagent use.
- Do not store real secrets, private keys, mnemonics, cloud credentials, or RPC credentials.
- Do not create `.agent-approvals/mainnet-action-approved.json`.
- Do not run live deploy, publish, push, or transaction-sending commands.
- Use dry-run, local validation, read-only inspection, or pseudocode when showing commands.

Directory guide:

- `prompts/`: operator prompts for live Codex and Claude dogfood.
- `expected/`: machine-checkable expected behavior contracts.
- `transcripts/`: transcript metadata JSON and Markdown captures.
- `live-runs/`: validated live-run packages created from templates.
- `hooks/`: platform hook observation records.
- `reports/`: generated bootstrap and strict reports.
- `templates/live-run-package/`: reusable capture package skeleton.
