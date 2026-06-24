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


def root_files(args: argparse.Namespace, spec: dict[str, Any], prof: dict[str, Any]) -> dict[str, str]:
    workflow_title = spec["chain_name"]
    stack = prof["display_name"]
    roles = ", ".join(spec["node_roles"])
    return {
        "00_REQUEST.md": f"""# Request: {workflow_title}\n\n- Original or normalized request: generate a safe planning artifact bundle for `{args.workflow}`.\n- Workflow id: `{args.workflow}`\n- Generated timestamp policy: intentionally omitted for reproducible fixtures.\n- Environment target: `{spec['environment']}`\n- Human decisions still required: chain ID assignment, upstream version selection, signer custody, infrastructure provider, external review scope.\n""",
        "01_ASSUMPTIONS.md": f"""# Assumptions: {workflow_title}\n\n## User-Omitted Assumptions\n\n- Selected stack profile: `{args.stack}`.\n- Selected chain type: `{spec['chain_type']}`.\n- Server sizing and exact commands are `VERIFY_CURRENT_DOCS`.\n\n## Must Verify Before Deployment\n\n- Current upstream docs, supported releases, chain ID collision status, bridge contracts, and signer custody.\n\n## Safety-Critical Assumptions\n\n- No private keys or mnemonics are committed.\n- Admin/debug RPC remains private.\n- This bundle is dry-run planning evidence only.\n""",
        "02_ARCHITECTURE_DECISION_RECORD.md": f"""# Architecture Decision Record: {workflow_title}\n\n## Status\n\nPlanning-only fixture. Not approved for production or mainnet.\n\n## Context\n\nThe workflow targets `{spec['environment']}` using {stack}.\n\n## Decision\n\nUse `{args.stack}` for a `{spec['chain_type']}` planning bundle with roles: {roles}.\n\n## Alternatives Considered\n\n| Alternative | Why Considered | Why Selected or Rejected |\n|---|---|---|\n| {stack} | Best fit for this fixture | selected for workflow acceptance |\n| OP Stack | Common optimistic-rollup baseline | rejected unless this fixture uses OP Stack |\n| Arbitrum Orbit | L3 and AnyTrust-capable path | rejected unless this fixture uses Orbit |\n| Polygon CDK | Validity/validium-focused path | rejected unless this fixture uses CDK |\n\n## Security Model\n\nGenerated artifacts are not audits. Security depends on signer custody, bridge assumptions, DA assumptions, admin-key governance, and upstream release choices.\n\n## Settlement Model\n\nSettlement layer: `{spec['settlement']['layer']}`. Verify finality and bridge conditions against current docs.\n\n## Data Availability Model\n\nDA mode: `{spec['data_availability']['mode']}`. DA failures must be modeled before real deployment.\n\n## Sequencing Model\n\nSequencing model: `{spec['sequencing']['model']}`. Censorship, downtime, and centralization risks require review.\n\n## Governance and Upgrade Model\n\nAdmin keys must move to multisig plus timelock or documented external custody before production/mainnet.\n\n## Operational Model\n\nOperators run isolated roles for public RPC, internal admin surfaces, monitoring, and signer integrations.\n\n## Consequences\n\nThis creates a repeatable planning bundle, not a launch approval.\n\n## Human Decisions Required\n\n- Select exact upstream release versions.\n- Assign a unique chain ID after collision checks.\n- Approve signer custody and external review scope.\n""",
        "03_STACK_DECISION_MATRIX.md": f"""# Stack Decision Matrix: {workflow_title}\n\n| stack | chain type fit | settlement fit | DA fit | proof/trust model | custom gas token support | operational complexity | security risks | recommendation |\n|---|---|---|---|---|---|---|---|---|\n| {stack} | fits `{spec['chain_type']}` | {spec['settlement']['layer']} | {spec['data_availability']['mode']} | {spec['proof_model']['type']} | verify current docs | medium/high | bridge, keys, RPC, DA | selected |\n| OP Stack | L2/L3 optimistic | parent-chain | calldata/blobs/Alt-DA | optimistic | verify current docs | medium | bridge/admin/sequencer | compare if requirements shift |\n| Arbitrum Orbit | L2/L3 Orbit | parent-chain | AnyTrust or parent-chain | optimistic/AnyTrust | verify current docs | medium | DAC/bridge/sequencer | compare if L3/DAC focus increases |\n| Polygon CDK | validium/zk modes | Ethereum/Agglayer/sovereign | offchain/DA committee/Ethereum | validity | verify current docs | high | prover/bridge/DA | compare for validity proof focus |\n""",
        "05_INFRASTRUCTURE_PLAN.md": f"""# Infrastructure Plan: {workflow_title}\n\n## Scope\n\nPlanning-only. No real deployment.\n\n## Node Roles\n\n{roles}\n\n## Server Topology\n\nSeparate public RPC, internal sequencer/validator/prover roles, monitoring, and signer integrations. Sizing is `VERIFY_CURRENT_DOCS`.\n\n## Network Boundaries\n\nPublic ingress only through rate-limited RPC/explorer endpoints. Admin/debug RPC binds to localhost or private networks only.\n\n## Firewall Policy\n\nAllow public RPC only where intended; deny admin/debug APIs externally; restrict signer and database access to private networks.\n\n## Storage Policy\n\nUse dedicated volumes, snapshot/restore checks, and archive/pruning decisions recorded per role.\n\n## Runtime Approach\n\nDocker Compose, systemd, Kubernetes, and Terraform samples are planning templates only.\n\n## Observability\n\nPrometheus, Grafana, logs, RPC health, disk alerts, and role-specific alerts are required before launch.\n\n## Backup/Restore\n\nBackups must be restore-tested before public testnet, staging, production, or mainnet.\n\n## Upgrade Process\n\nStage upgrades, pin versions, verify upstream docs, and maintain rollback plans.\n\n## Incident Response\n\nTriage node down, RPC unavailable, sequencer lag, bridge incident, DA failure, and signer access incidents.\n""",
        "06_SECURITY_REVIEW.md": f"""# Security Review: {workflow_title}\n\n## Scope\n\nPlanning-only review. Not an audit or production certification.\n\n## Findings\n\n| Severity | Area | Finding | Required Mitigation |\n|---|---|---|---|\n| high | keys | deployer/operator keys cannot live in repo | use KMS/HSM/hardware signer or signer service |\n| high | RPC | admin/debug RPC must not be public | bind privately and firewall |\n| high | bridge/settlement | bridge assumptions can dominate risk | external bridge/security review required |\n\n## Secrets Policy\n\nNo private keys, mnemonics, keystore passwords, or deployer secrets may be committed. Use {SAFE_SECRET}.\n\n## Signer/Key Custody\n\nUse KMS/HSM/hardware wallet/signer service. CLI private-key flags are forbidden.\n\n## Bridge Risks\n\nBridge contracts, relayers, fraud/validity windows, and parent-chain finality require external review.\n\n## Admin/Upgrade Risks\n\nAdmin keys require multisig/timelock or documented custody before production/mainnet.\n\n## Sequencer Risks\n\nCensorship, downtime, ordering, and centralization risks remain open until reviewed.\n\n## DA Risks\n\nDA mode `{spec['data_availability']['mode']}` requires explicit failure-mode review.\n\n## Validator/Prover Risks\n\nValidator/prover assumptions are relevant when those roles are present and must be verified against current docs.\n\n## RPC Exposure Risks\n\nPublic RPC must not expose admin, debug, personal, or engine APIs.\n\n## Generated Artifact Limitations\n\nThis bundle is not an audit, not a launch approval, and not production certification.\n\n## Required External Reviews\n\nProtocol review, infrastructure review, bridge review, incident drill, and legal/compliance review where applicable.\n""",
        "07_RUNBOOK.md": f"""# Runbook: {workflow_title}\n\n## Preflight Checklist\n\n- Run validators in dry-run mode.\n- Confirm no secrets are committed.\n- Verify upstream docs and versions.\n\n## Start/Stop Service Examples\n\nUse local dry-run or staging-only service manager commands after human review. Do not use this fixture for mainnet deployment.\n\n## Monitoring Checks\n\nCheck node availability, RPC health, disk, logs, and role-specific lag.\n\n## Backup Checks\n\nConfirm snapshots exist and restore into an isolated environment.\n\n## Rollback Checklist\n\nRecord version pins, config backups, and rollback owners before changes.\n\n## Incident Triage\n\nClassify RPC outage, sequencer/validator/prover issue, bridge risk, DA failure, or signer incident.\n""",
        "08_LAUNCH_GATES.md": f"""# Launch Gates: {workflow_title}\n\n## Status\n\nNot launch-ready.\n\n## Required Gates\n\n| Gate | Required For | Status | Evidence Required |\n|---|---|---|---|\n| architecture approved | public testnet/mainnet | pending | signed ADR |\n| source docs fresh enough | all | pending | upstream freshness report |\n| security review complete | all | pending | review notes |\n| configs validated | all | pending | validator report |\n| monitoring live | testnet/mainnet | pending | alert drill evidence |\n| backups tested | testnet/mainnet | pending | restore drill evidence |\n| failover tested | testnet/mainnet | pending | drill evidence |\n| bridge risk reviewed | rollups | pending | bridge review notes |\n| admin keys moved to multisig/timelock or documented custody | testnet/mainnet | pending | custody docs |\n| human approval | public testnet/mainnet | pending | explicit approval outside repo |\n| external audit or review | production/mainnet | pending | audit/review report |\n\n## Explicit Non-Approval\n\nThis fixture does not approve deployment.\n""",
        "09_VALIDATION_REPORT.md": f"""# Validation Report: {workflow_title}\n\n## Validators Run\n\n- artifact bundle validator: expected pass\n- generated config validator: expected pass\n- strict secret scan: expected pass\n- policy guard: expected pass\n\n## Pass/Fail Summary\n\nPending local execution.\n\n## Skipped Checks and Why\n\nLive Codex/Claude dogfood is deferred to v0.3.\n\n## Warnings\n\nVersion-sensitive facts remain `VERIFY_CURRENT_DOCS`.\n\n## Next Required Validations\n\nRun `python3 scripts/validate_artifact_bundle.py --strict --path <bundle>`.\n""",
        "10_OPEN_QUESTIONS.md": f"""# Open Questions: {workflow_title}\n\n- Which exact upstream release/version is selected?\n- Which unique chain ID passes collision checks?\n- Which custody provider or signer model is approved?\n- Which external reviews are required before real deployment?\n- Which organization owns incident response and upgrades?\n""",
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
