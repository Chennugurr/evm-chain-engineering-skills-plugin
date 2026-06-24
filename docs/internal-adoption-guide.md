# Internal Adoption Guide

This plugin produces planning-only blockchain engineering artifacts: architecture decisions, chain specs, infrastructure plans, security reviews, launch gates, and validation evidence.

It is not a deployer, audit, bridge certification, key manager, cloud integration, or investment adviser.

Use command prompts from `commands/`, generate bundles with `scripts/render_artifact_bundle.py`, validate bundles with `scripts/validate_artifact_bundle.py`, and run `make validate-v02` before internal release review. Report bad output with the prompt, selected skills, generated bundle path, validation result, and safety concern.

Invoke skills directly by name when needed, especially `chain-security-reviewer` for production/mainnet/bridge/admin/sequencer/prover paths. Update upstream references through `docs/upstream-sources.md` and add new stack support through `docs/contributing-new-stack.md`.
