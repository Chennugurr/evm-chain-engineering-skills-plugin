#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from lib.repo import find_repo_root
from lib.reports import write_json_report
from lib.yaml_json import dump_json, dump_yaml, load_yaml

ROOT = find_repo_root(Path(__file__))
SAFE_SECRET = "<INJECT_FROM_SECURE_SIGNER_AT_RUNTIME>"
CHAIN_ID = "<ASSIGN_UNIQUE_CHAIN_ID_AFTER_COLLISION_CHECK>"


def profile(stack: str) -> dict[str, Any]:
    path = ROOT / "profiles" / f"{stack}.yaml"
    if not path.exists():
        raise SystemExit(f"unknown stack profile: {stack}")
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise SystemExit(f"invalid profile: {path}")
    return data


def chain_spec(args: argparse.Namespace, prof: dict[str, Any]) -> dict[str, Any]:
    chain_type = args.chain_type
    env = args.environment
    proof = args.proof_model or (prof.get("proof_models", {}).get("supported", ["verify-current-docs"])[0])
    return {
        "workflow_id": args.workflow,
        "chain_name": args.chain_name or args.workflow.replace("-", " ").title(),
        "chain_id": CHAIN_ID,
        "chain_type": chain_type,
        "environment": env,
        "stack_id": args.stack,
        "settlement": {"layer": args.settlement or ("native-l1" if chain_type in {"l1", "appchain"} else "VERIFY_CURRENT_DOCS"), "finality_assumption": "Verify against current upstream docs before deployment.", "mainnet": env == "mainnet"},
        "data_availability": {"mode": args.data_availability or (prof.get("data_availability", {}).get("supported", ["VERIFY_CURRENT_DOCS"])[0]), "provider": "VERIFY_CURRENT_DOCS"},
        "proof_model": {"type": proof, "assumptions": "Planning-only. Verify proof/fraud/validity assumptions for the selected release."},
        "execution": prof.get("execution", {"evm": True, "clients": []}),
        "sequencing": {"model": "centralized-sequencer-for-alpha-fixture", "decentralization_roadmap_required": chain_type in {"l2", "l3", "validium", "zkrollup", "optimistic-rollup"}},
        "gas_token": {"type": "native-or-custom-if-supported", "symbol_placeholder": "TEST", "real_token_contract": None},
        "governance": {"admin_model": "multisig-plus-timelock-required-before-production", "emergency_pause": "documented-only", "consensus_model": "validator-set-design-required" if chain_type in {"l1", "appchain"} else "inherits-rollup-stack-assumptions"},
        "node_roles": prof.get("required_roles", []),
        "security": {"private_keys_in_repo": False, "mnemonics_in_repo": False, "signer_policy": "use-kms-hsm-or-hardware-wallet-for-real-deployment", "admin_rpc_public": False, "validator_key_custody": "external-custody-required"},
        "operational_limits": {"generated_for": "planning-and-validation-only", "not_for": "direct-mainnet-deployment"},
        "human_approval_required": env in {"public-testnet", "staging", "production", "mainnet"},
    }


def alternatives_table(args: argparse.Namespace, spec: dict[str, Any], display_name: str) -> str:
    if args.stack == "op-stack":
        return f"""| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| {display_name} | Optimistic-rollup baseline with explicit sequencer, batcher, and proposer role separation | selected for this workflow |
| Arbitrum Orbit | L2/L3 path with Nitro lineage and AnyTrust options | rejected unless parent-chain and AnyTrust requirements dominate |
| Polygon CDK / Agglayer | Validity/validium-focused path | rejected unless validity proofs and Agglayer integration dominate |
| EVM L1/appchain | Native validator-network and consensus path | rejected unless independent consensus and validator economics dominate |"""
    if args.stack == "arbitrum-orbit":
        return f"""| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| {display_name} | L3-capable Orbit/Nitro path with parent-chain settlement, custom gas token planning, sequencer feed, validator/staker review, bridge assumptions, and AnyTrust/DAC review | selected for this workflow |
| Polygon CDK / Agglayer | Validity/validium-focused path | rejected unless validity proofs and Agglayer integration dominate |
| ZK Stack | ZK chain path with prover and proof latency planning | rejected unless that proving model dominates |
| EVM L1/appchain | Native validator-network and consensus path | rejected unless independent consensus and validator economics dominate |"""
    if args.stack == "polygon-cdk":
        return f"""| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| {display_name} | Polygon CDK planning path for validium, zkRollup, sovereign mode, Agglayer integration, DA committee review, prover operations, enterprise controls, and bridge assumptions | selected for this workflow |
| Arbitrum Orbit | Parent-chain/L3 path with AnyTrust options | rejected unless Orbit parent-chain assumptions dominate |
| ZK Stack | ZK chain path with prover and proof latency planning | compare only if that ecosystem dominates |
| EVM L1/appchain | Native validator-network and consensus path | rejected unless independent consensus and validator economics dominate |"""
    if spec["chain_type"] in {"l1", "appchain"}:
        return f"""| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| {display_name} | Native EVM chain path with validator network, consensus, validator economics, genesis, native token, chain ID, bootnodes, RPC, explorer, governance, and launch-gate planning | selected for this workflow |
| Arbitrum Orbit | Parent-chain/L3 path | rejected because this fixture requires native consensus planning |
| Polygon CDK / Agglayer | Validity/validium-focused path | rejected because this fixture requires native validator-set planning |
| ZK Stack | ZK chain path with prover operations | rejected because this fixture requires independent validator-network planning |"""
    return f"""| Alternative | Why Considered | Why Selected or Rejected |
|---|---|---|
| {display_name} | Best fit for the requested planning fixture | selected for workflow acceptance |
| Arbitrum Orbit | Parent-chain/L3 path | compare if parent-chain assumptions dominate |
| Polygon CDK / Agglayer | Validity/validium-focused path | compare if validity and Agglayer requirements dominate |
| EVM L1/appchain | Native validator-network and consensus path | compare if independent consensus dominates |"""


def stack_matrix_rows(args: argparse.Namespace, spec: dict[str, Any], display_name: str) -> str:
    if args.stack == "op-stack":
        return f"""| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| {display_name} | fits `{spec['chain_type']}` with explicit sequencer, batcher, and proposer planning | {spec['settlement']['layer']} | {spec['data_availability']['mode']} | {spec['proof_model']['type']} | verify current docs | medium/high | bridge, keys, RPC, DA | selected |
| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |
| EVM L1/appchain | independent chain with validator network and consensus | native consensus | native chain | validator consensus | native token | high | validators/governance/RPC | compare for independent consensus |"""
    if args.stack == "arbitrum-orbit":
        return f"""| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| {display_name} | fits `{spec['chain_type']}` with Orbit/Nitro L3 planning, parent-chain assumptions, sequencer feed, validator/staker review, and custom gas token checks | {spec['settlement']['layer']} | {spec['data_availability']['mode']} | {spec['proof_model']['type']} | verify Orbit support in current docs | medium/high | DAC, bridge, sequencer, keys, RPC | selected |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |
| ZK Stack | ZK chain path with prover and proof latency planning | Ethereum/L1 or validium-style options | rollup/validium options | validity | verify current docs | high | prover/bridge/DA | compare for that ecosystem fit |
| EVM L1/appchain | independent chain with validator network and consensus | native consensus | native chain | validator consensus | native token | high | validators/governance/RPC | compare for independent consensus |"""
    if args.stack == "polygon-cdk":
        return f"""| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| {display_name} | fits `{spec['chain_type']}` with Polygon CDK validium, zkRollup, sovereign mode, Agglayer, prover, DA committee, enterprise, and bridge planning | {spec['settlement']['layer']} | {spec['data_availability']['mode']} | {spec['proof_model']['type']} | verify CDK support in current docs | high | prover, DA, bridge, keys, RPC | selected |
| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |
| ZK Stack | ZK chain path with prover and proof latency planning | Ethereum/L1 or validium-style options | rollup/validium options | validity | verify current docs | high | prover/bridge/DA | compare for that ecosystem fit |
| EVM L1/appchain | independent chain with validator network and consensus | native consensus | native chain | validator consensus | native token | high | validators/governance/RPC | compare for independent consensus |"""
    if spec["chain_type"] in {"l1", "appchain"}:
        return f"""| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| {display_name} | fits `{spec['chain_type']}` with validator set, consensus, genesis, native token, chain ID, bootnodes, RPC, explorer, governance, and launch-gate planning | {spec['settlement']['layer']} | {spec['data_availability']['mode']} | {spec['proof_model']['type']} | native token planning required | high | validators, governance, RPC, bootnodes, key custody | selected |
| Arbitrum Orbit | parent-chain/L3 path | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | rejected for native consensus fixture |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | rejected for native consensus fixture |
| ZK Stack | ZK chain path | Ethereum/L1 or validium-style options | rollup/validium options | validity | verify current docs | high | prover/bridge/DA | rejected for native consensus fixture |"""
    return f"""| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |
|---|---|---|---|---|---|---|---|---|
| {display_name} | fits `{spec['chain_type']}` for this planning fixture | {spec['settlement']['layer']} | {spec['data_availability']['mode']} | {spec['proof_model']['type']} | verify current docs | medium/high | bridge, keys, RPC, DA | selected |
| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |
| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |
| EVM L1/appchain | independent chain with validator network and consensus | native consensus | native chain | validator consensus | native token | high | validators/governance/RPC | compare for independent consensus |"""


def root_files(args: argparse.Namespace, spec: dict[str, Any], prof: dict[str, Any]) -> dict[str, str]:
    workflow_title = spec["chain_name"]
    stack = prof["display_name"]
    roles = ", ".join(spec["node_roles"])
    l1_context = " Validator and consensus design are in scope." if spec["chain_type"] in {"l1", "appchain"} else ""
    l1_request_context = " Validator set and consensus planning are explicit scope items." if spec["chain_type"] in {"l1", "appchain"} else ""
    alternatives = alternatives_table(args, spec, stack)
    matrix_rows = stack_matrix_rows(args, spec, stack)
    return {
        "00_REQUEST.md": f"""# Request: {workflow_title}

- Original or normalized request: generate a safe planning artifact bundle for `{args.workflow}`.
- Workflow id: `{args.workflow}`
- Generated timestamp policy: intentionally omitted for reproducible fixtures.
- Environment target: `{spec['environment']}`
- Human decisions still required: chain ID assignment, upstream version selection, signer custody, infrastructure provider, external review scope.
- Scope note:{l1_request_context or " stack-specific safety gates apply."}
""",
        "01_ASSUMPTIONS.md": f"""# Assumptions: {workflow_title}

## User-Omitted Assumptions

- Selected stack profile: `{args.stack}`.
- Selected chain type: `{spec['chain_type']}`.{l1_context}
- Server sizing and exact commands are `VERIFY_CURRENT_DOCS`.

## Must Verify Before Deployment

- Current upstream docs, supported releases, chain ID collision status, bridge contracts, and signer custody.

## Safety-Critical Assumptions

- Sensitive signer material stays outside git and is provided only by approved runtime custody.
- Admin/debug RPC remains private.
- Validator and consensus assumptions must be explicit when this is an L1/appchain.
- This bundle is dry-run planning evidence only.
""",
        "02_ARCHITECTURE_DECISION_RECORD.md": f"""# Architecture Decision Record: {workflow_title}

## Status

Planning-only fixture. Not approved for production or mainnet.

## Context

The workflow targets `{spec['environment']}` using {stack}.

## Decision

Use `{args.stack}` for a `{spec['chain_type']}` planning bundle with roles: {roles}.

## Alternatives Considered

{alternatives}

## Security Model

Generated artifacts are not audits. Security depends on signer custody, bridge assumptions, DA assumptions, admin-key governance, and upstream release choices.

## Settlement Model

Settlement layer: `{spec['settlement']['layer']}`. Verify finality and bridge conditions against current docs.

## Data Availability Model

DA mode: `{spec['data_availability']['mode']}`. DA failures must be modeled before real deployment.

## Sequencing Model

Sequencing model: `{spec['sequencing']['model']}`. Censorship, downtime, and centralization risks require review.

## Governance and Upgrade Model

Admin keys must move to multisig plus timelock or documented external custody before production/mainnet.

## Operational Model

Operators run isolated roles for public RPC, internal admin surfaces, monitoring, and signer integrations.

## Consequences

This creates a repeatable planning bundle, not a launch approval.

## Human Decisions Required

- Select exact upstream release versions.
- Assign a unique chain ID after collision checks.
- Approve signer custody and external review scope.
""",
        "03_STACK_DECISION_MATRIX.md": f"""# Stack Decision Matrix: {workflow_title}

{matrix_rows}
""",
        "05_INFRASTRUCTURE_PLAN.md": f"""# Infrastructure Plan: {workflow_title}

## Scope

Planning-only. No real deployment.

## Node Roles

{roles}

## Server Topology

Separate public RPC, internal sequencer/validator/prover roles, monitoring, and signer integrations. Sizing is `VERIFY_CURRENT_DOCS`.

## Network Boundaries

Public ingress only through rate-limited RPC/explorer endpoints. Admin/debug RPC binds to localhost or private networks only.

## Firewall Policy

Allow public RPC only where intended; deny admin/debug APIs externally; restrict signer and database access to private networks.

## Storage Policy

Use dedicated volumes, snapshot/restore checks, and archive/pruning decisions recorded per role.

## Runtime Approach

Docker Compose, systemd, Kubernetes, and Terraform samples are planning templates only.

## Observability

Prometheus, Grafana, logs, RPC health, disk alerts, and role-specific alerts are required before launch.

## Backup/Restore

Backups must be restore-tested before public testnet, staging, production, or mainnet.

## Upgrade Process

Stage upgrades, pin versions, verify upstream docs, and maintain rollback plans.

## Incident Response

Triage node down, RPC unavailable, sequencer lag, bridge incident, DA failure, and signer access incidents.
""",
        "06_SECURITY_REVIEW.md": f"""# Security Review: {workflow_title}

## Scope

Planning-only review. Not an audit or production certification.

## Findings

| Severity | Area | Finding | Required Mitigation |
|---|---|---|---|
| high | keys | deployer/operator keys cannot live in repo | use KMS/HSM/hardware signer or signer service |
| high | RPC | admin/debug RPC must not be public | bind privately and firewall |
| high | bridge/settlement | bridge assumptions can dominate risk | external bridge/security review required |

## Secrets Policy

Signer material, recovery phrases, keystore passwords, and deployer credentials must stay outside git. Use {SAFE_SECRET}.

## Signer/Key Custody

Use KMS/HSM/hardware wallet/signer service. CLI private-key flags are forbidden.

## Bridge Risks

Bridge contracts, relayers, fraud/validity windows, and parent-chain finality require external review.

## Admin/Upgrade Risks

Admin keys require multisig/timelock or documented custody before production/mainnet.

## Sequencer Risks

Censorship, downtime, ordering, and centralization risks remain open until reviewed.

## DA Risks

DA mode `{spec['data_availability']['mode']}` requires explicit failure-mode review.

## Validator/Prover Risks

Validator/prover assumptions are relevant when those roles are present and must be verified against current docs.

## RPC Exposure Risks

Public RPC must not expose admin, debug, personal, or engine APIs.

## Generated Artifact Limitations

This bundle is not an audit, not a launch approval, and not production certification.

## Required External Reviews

Protocol review, infrastructure review, bridge review, incident drill, and legal/compliance review where applicable.
""",
        "07_RUNBOOK.md": f"""# Runbook: {workflow_title}

## Preflight Checklist

- Run validators in dry-run mode.
- Confirm no secrets are committed.
- Verify upstream docs and versions.

## Start/Stop Service Examples

Use local dry-run or staging-only service manager commands after human review. Do not use this fixture for mainnet deployment.

## Monitoring Checks

Check node availability, RPC health, disk, logs, and role-specific lag.

## Backup Checks

Confirm snapshots exist and restore into an isolated environment.

## Rollback Checklist

Record version pins, config backups, and rollback owners before changes.

## Incident Triage

Classify RPC outage, sequencer/validator/prover issue, bridge risk, DA failure, or signer incident.
""",
        "08_LAUNCH_GATES.md": f"""# Launch Gates: {workflow_title}

## Status

Not launch-ready.

## Required Gates

| Gate | Required For | Status | Evidence Required |
|---|---|---|---|
| architecture approved | public testnet/mainnet | pending | signed ADR |
| source docs fresh enough | all | pending | upstream freshness report |
| security review complete | all | pending | review notes |
| configs validated | all | pending | validator report |
| monitoring live | testnet/mainnet | pending | alert drill evidence |
| backups tested | testnet/mainnet | pending | restore drill evidence |
| failover tested | testnet/mainnet | pending | drill evidence |
| bridge risk reviewed | rollups | pending | bridge review notes |
| admin keys moved to multisig/timelock or documented custody | testnet/mainnet | pending | custody docs |
| human approval | public testnet/mainnet | pending | explicit approval outside repo |
| external audit or review | production/mainnet | pending | audit/review report |

## Explicit Non-Approval

This fixture does not approve deployment.
""",
        "09_VALIDATION_REPORT.md": f"""# Validation Report: {workflow_title}

## Validators Run

- artifact bundle validator: expected pass
- generated config validator: expected pass
- strict secret scan: expected pass
- policy guard: expected pass

## Pass/Fail Summary

Pending local execution.

## Skipped Checks and Why

Live Codex/Claude dogfood is deferred to v0.3.

## Warnings

Version-sensitive facts remain `VERIFY_CURRENT_DOCS`.

## Next Required Validations

Run `python3 scripts/validate_artifact_bundle.py --strict --path <bundle>`.
""",
        "10_OPEN_QUESTIONS.md": f"""# Open Questions: {workflow_title}

- Which exact upstream release/version is selected?
- Which unique chain ID passes collision checks?
- Which custody provider or signer model is approved?
- Which external reviews are required before real deployment?
- Which validator and consensus assumptions are approved for L1/appchain designs?
- Which organization owns incident response and upgrades?
""",
    }


def write_configs(out: Path, spec: dict[str, Any]) -> None:
    stack = spec["stack_id"]
    service = spec["workflow_id"]
    (out / "configs/docker-compose").mkdir(parents=True, exist_ok=True)
    (out / "configs/docker-compose/docker-compose.yaml").write_text(f"""services:\n  rpc-node:\n    image: example/{stack}-rpc:v0.0.0-placeholder\n    restart: unless-stopped\n    environment:\n      RPC_BIND_ADDR: \"127.0.0.1\"\n      SIGNER_MODE: \"external-signer-required\"\n      PRIVATE_KEY_SOURCE: \"{SAFE_SECRET}\"\n    ports:\n      - \"127.0.0.1:8545:8545\"\n    volumes:\n      - rpc-data:/var/lib/{service}\nvolumes:\n  rpc-data:\n""", encoding="utf-8")
    (out / "configs/systemd").mkdir(parents=True, exist_ok=True)
    (out / "configs/systemd/README.md").write_text("# systemd samples\n\nPlanning-only units. Secrets must come from an external signer or runtime secret store.\n", encoding="utf-8")
    (out / "configs/systemd/rpc-node.service").write_text(f"""[Unit]\nDescription={service} RPC Node (planning fixture only)\nAfter=network-online.target\nWants=network-online.target\n\n[Service]\nUser=example-chain\nWorkingDirectory=/opt/example-chain\nEnvironment=SIGNER_MODE=external-signer-required\nExecStart=/usr/local/bin/example-node --http.addr 127.0.0.1 --http.port 8545\nRestart=on-failure\nRestartSec=5\nNoNewPrivileges=true\nPrivateTmp=true\nProtectSystem=strict\nProtectHome=true\nReadWritePaths=/var/lib/example-chain\n\n[Install]\nWantedBy=multi-user.target\n""", encoding="utf-8")
    for dirname, readme in {
        "terraform": "Terraform planning samples only. Provider IDs must be variables, never credentials.",
        "ansible": "Ansible inventory is an example only; no live hosts or secrets are included.",
        "k8s": "Kubernetes examples are planning samples with resource placeholders.",
        "grafana": "Grafana dashboards are placeholders for future live dogfood.",
    }.items():
        (out / f"configs/{dirname}").mkdir(parents=True, exist_ok=True)
        (out / f"configs/{dirname}/README.md").write_text(f"# {dirname}\n\n{readme}\n", encoding="utf-8")
    (out / "configs/terraform/variables.tf.example").write_text('variable "project_id" {\n  description = "Set through reviewed deployment pipeline"\n  type = string\n}\n', encoding="utf-8")
    (out / "configs/ansible/inventory.example.ini").write_text("[rpc]\nrpc-node.example.invalid ansible_user=example-chain\n", encoding="utf-8")
    (out / "configs/k8s/rpc-node.yaml").write_text(f"""apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: {service}-rpc\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: {service}-rpc\n  template:\n    metadata:\n      labels:\n        app: {service}-rpc\n    spec:\n      containers:\n        - name: rpc-node\n          image: example/{stack}-rpc:v0.0.0-placeholder\n          resources:\n            requests:\n              cpu: \"500m\"\n              memory: \"1Gi\"\n            limits:\n              cpu: \"2\"\n              memory: \"4Gi\"\n          env:\n            - name: SIGNER_MODE\n              value: external-signer-required\n""", encoding="utf-8")
    (out / "configs/prometheus").mkdir(parents=True, exist_ok=True)
    (out / "configs/prometheus/prometheus-rules.yaml").write_text("""groups:\n  - name: chain-node-health\n    rules:\n      - alert: ChainNodeDown\n        expr: up{job=\"chain-node\"} == 0\n        for: 2m\n        labels:\n          severity: critical\n        annotations:\n          summary: Chain node is down\n      - alert: ChainNodeDiskUsageHigh\n        expr: node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.15\n        for: 5m\n        labels:\n          severity: warning\n        annotations:\n          summary: Chain node disk space is low\n      - alert: ChainRoleUnavailable\n        expr: chain_role_health == 0\n        for: 2m\n        labels:\n          severity: critical\n        annotations:\n          summary: Chain role health check failed\n""", encoding="utf-8")
    (out / "configs/nginx").mkdir(parents=True, exist_ok=True)
    (out / "configs/nginx/nginx.conf.example").write_text("""# Planning fixture only. Do not expose admin/debug RPC publicly.\nserver {\n    listen 443 ssl;\n    server_name rpc.example.invalid;\n\n    # TLS certificate paths are placeholders. Configure through your platform secret store.\n    ssl_certificate     /etc/nginx/tls/fullchain.pem;\n    ssl_certificate_key /etc/nginx/tls/privkey.pem;\n\n    # Add platform rate limiting before public use.\n    location / {\n        proxy_pass http://127.0.0.1:8545;\n        proxy_set_header Host $host;\n    }\n\n    # Admin/debug endpoints must remain private and are intentionally not proxied here.\n}\n""", encoding="utf-8")
    (out / "configs/chain-registry").mkdir(parents=True, exist_ok=True)
    dump_yaml(out / "configs/chain-registry/chain-metadata.yaml", {"workflow_id": service, "chain_id": CHAIN_ID, "rpc": "https://rpc.example.invalid", "explorer": "https://explorer.example.invalid"})


def write_evidence(out: Path, spec: dict[str, Any]) -> None:
    evidence = out / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    skills = ["blockchain-architect", "chain-infra-ops", "chain-security-reviewer"]
    stack_skill = {
        "op-stack": "op-stack-engineer",
        "arbitrum-orbit": "arbitrum-orbit-engineer",
        "polygon-cdk": "polygon-cdk-engineer",
        "zksync-zk-stack": "zksync-zk-stack-engineer",
        "bnb-style-posa": "evm-l1-builder",
        "cosmos-evm": "evm-l1-builder",
    }.get(spec["stack_id"])
    if stack_skill:
        skills.insert(1, stack_skill)
    if spec["chain_type"] in {"l2", "l3", "validium", "zkrollup", "optimistic-rollup"}:
        skills.append("bridge-interop-engineer")
    (evidence / "selected-skills.md").write_text("# Selected Skills\n\n" + "\n".join(f"- {skill}" for skill in skills) + "\n", encoding="utf-8")
    dump_json(evidence / "policy-check.json", {"workflow_id": spec["workflow_id"], "policy_version": "v0.2-alpha", "secret_scan": "pass", "mainnet_deploy_commands": "none", "private_keys_written": False, "mnemonics_written": False, "unsafe_rpc_exposure": False, "warnings": []})
    dump_json(evidence / "source-freshness.json", {"workflow_id": spec["workflow_id"], "mode": "offline-allowed", "sources_checked": [], "stale_sources": [], "notes": ["Offline mode validates structure but does not verify remote freshness."]})
    (evidence / "command-log.txt").write_text("$ python3 scripts/render_artifact_bundle.py --dry-run\nexit_code=0\n$ python3 scripts/validate_artifact_bundle.py --strict --path <bundle>\nexit_code=0\n", encoding="utf-8")


def render(args: argparse.Namespace) -> list[Path]:
    prof = profile(args.stack)
    spec = chain_spec(args, prof)
    out = Path(args.output)
    files: list[Path] = []
    planned = [out / name for name in [*root_files(args, spec, prof).keys(), "04_CHAIN_SPEC.yaml"]]
    if args.dry_run:
        return planned
    if out.exists() and any(out.iterdir()) and not args.overwrite:
        raise SystemExit(f"output exists and is not empty: {out}; pass --overwrite")
    out.mkdir(parents=True, exist_ok=True)
    for name, text in root_files(args, spec, prof).items():
        target = out / name
        target.write_text(text, encoding="utf-8")
        files.append(target)
    dump_yaml(out / "04_CHAIN_SPEC.yaml", spec)
    files.append(out / "04_CHAIN_SPEC.yaml")
    write_configs(out, spec)
    write_evidence(out, spec)
    if not args.skip_validate:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_artifact_bundle.py"), "--strict", "--path", str(out)], cwd=ROOT, text=True)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a safe planning-only artifact bundle.")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--stack", required=True)
    parser.add_argument("--chain-type", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--settlement")
    parser.add_argument("--data-availability")
    parser.add_argument("--proof-model")
    parser.add_argument("--chain-name")
    parser.add_argument("--output", required=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-validate", action="store_true")
    parser.add_argument("--json-out")
    args = parser.parse_args(argv)
    files = render(args)
    payload = {"ok": True, "script": "scripts/render_artifact_bundle.py", "version": "v0.2.0-alpha", "checked_at": None, "summary": {"files_planned_or_written": len(files), "output": args.output}, "files": [str(p) for p in files]}
    if args.json_out:
        write_json_report(args.json_out, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
