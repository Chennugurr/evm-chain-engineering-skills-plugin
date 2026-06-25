# Claude Plugin Discovery Prompt

You are running the v0.3.0-beta Claude plugin discovery smoke test for the local plugin `evm-chain-engineering-pro` loaded from `plugins/evm-chain-engineering-pro`.

Use the plugin skills if they are available. If the platform does not expose hidden routing telemetry, state observed skill use from explicit tool calls and output.

Do not deploy, broadcast transactions, publish, create real secrets, write approval markers, edit plugin manifests, or touch unrelated files. Keep the run dry-run and planning-only.

Tasks:

1. Confirm the plugin is visible.
2. List the visible EVM chain engineering plugin skills.
3. Directly invoke the blockchain architecture skill if available.
4. Classify this natural-language request for automatic routing evidence: "I want to stand up an OP Stack public testnet with batcher and proposer roles; what architecture should I use?"
5. Report hook visibility or a blocker status.
6. Report portability notes, especially whether the plugin depends on a hardcoded local home path.

Required output:

- Plugin visibility.
- Skills visible.
- Direct skill invocation evidence.
- Automatic skill trigger evidence for OP Stack with batcher and proposer context.
- Hook visibility or blocker status.
- Portability notes.
- Safety stance and limitations.
