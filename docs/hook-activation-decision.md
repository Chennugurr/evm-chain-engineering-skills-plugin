# Hook Activation Decision

The plugin keeps hooks in `plugins/evm-chain-engineering-pro/hooks/hooks.json`. The Codex manifest intentionally omits a `hooks` field because the local validator rejects unsupported manifest fields. Claude validation accepts the plugin manifest, and the hook fixture tests validate deterministic policy guard behavior.

The fixture tests prove our guard script decisions for Codex-style and Claude-style hook events. Platform hook activation must still be checked in live Codex/Claude installations before broader rollout.

The policy guard fails closed on secret persistence, private-key CLI flags, mainnet broadcast patterns, destructive commands, public admin/debug RPC, unsafe env examples, unpinned images, and production-like actions without review gates.
