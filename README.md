# EVM Chain Engineering Plugin

A dual-compatible Codex and Claude plugin bundle for agent-assisted blockchain engineering. It helps agents design, build, validate, secure, and operate EVM L1s, L2s, L3s, rollups, appchains, bridges, explorers, faucets, and production server infrastructure.

## What This Is

This repository packages focused agent skills, shared references, safe Python utilities, reusable infrastructure templates, tests, and behavior evals. It is intended to make an AI agent better at chain architecture and operations while preserving human approval around deployment and mainnet risk.

## What This Is Not

This is not a turnkey mainnet deployment tool. It does not generate private keys, sign transactions, move funds, auto-deploy contracts, or claim production safety without a threat model, launch checklist, and explicit human approval.

## Covered Chain Types

- EVM L1s, Ethereum-like L1s, BNB-style PoSA chains, Cosmos EVM chains, Avalanche L1s, and Polkadot Frontier chains.
- OP Stack, Arbitrum Orbit/Nitro, Polygon CDK, ZKsync ZK Stack, modular rollups, sovereign rollups, validiums, zkRollups, optimistic rollups, L2s, and L3s.
- Bridges, relayers, RPC, explorers, indexers, faucets, observability, backups, launch readiness, and incident response.

## Skills Included

The plugin includes 14 focused skills under `plugins/evm-chain-engineering-pro/skills/`. Each skill has a concise trigger description, a short workflow, and references that load only when relevant.

## Installation

For Codex, use the repo-local marketplace at `.agents/plugins/marketplace.json`. Restart Codex after adding or changing local plugins. For Claude Code, use the marketplace at `.claude-plugin/marketplace.json` or load the plugin directory directly with Claude's local plugin workflow.

## Development

```bash
python3 -m pytest
make validate
```

All helper scripts are read-only by default unless their name and help text explicitly describe safe file generation. Deployment scripts are intentionally absent in v1.

## Safety Model

The repository enforces dry-run-first workflows, no real secrets, no mainnet auto-deploy, no public admin/debug RPC, pinned production image tags, role/key separation, current-doc verification notes, and security review triggers for production-like work.
