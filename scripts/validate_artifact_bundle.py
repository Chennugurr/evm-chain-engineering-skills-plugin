#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from lib.repo import find_repo_root, relpath, skill_names
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report
from lib.safety import scan_path
from lib.yaml_json import load_json, load_yaml

ROOT = find_repo_root(Path(__file__))
REQUIRED_ROOT_FILES = [
    "00_REQUEST.md", "01_ASSUMPTIONS.md", "02_ARCHITECTURE_DECISION_RECORD.md", "03_STACK_DECISION_MATRIX.md",
    "04_CHAIN_SPEC.yaml", "05_INFRASTRUCTURE_PLAN.md", "06_SECURITY_REVIEW.md", "07_RUNBOOK.md",
    "08_LAUNCH_GATES.md", "09_VALIDATION_REPORT.md", "10_OPEN_QUESTIONS.md",
]
REQUIRED_EVIDENCE = ["selected-skills.md", "policy-check.json", "source-freshness.json", "command-log.txt"]
ROLLUP_TYPES = {"l2", "l3", "validium", "zkrollup", "optimistic-rollup", "sovereign-rollup"}
L1_TYPES = {"l1", "appchain"}
PROD_ENVS = {"production", "mainnet"}


def bundle_paths(args: argparse.Namespace) -> list[Path]:
    if args.path:
        return [Path(args.path)]
    base = Path(args.all or "fixtures/artifact-bundles")
    return sorted([item for item in base.iterdir() if item.is_dir()]) if base.exists() else []


def text_contains(path: Path, terms: list[str]) -> bool:
    text = ""
    for file_path in path.rglob("*"):
        if file_path.is_file():
            try:
                text += "\n" + file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass
    return all(term.lower() in text.lower() for term in terms)


def selected_skills(path: Path) -> list[str]:
    skills_file = path / "evidence" / "selected-skills.md"
    if not skills_file.exists():
        return []
    skills: list[str] = []
    for line in skills_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().lstrip("-").strip().strip("`")
        if stripped and not stripped.startswith("#"):
            skills.append(stripped)
    return skills


def validate_chain_spec(bundle: Path, findings: list[Finding]) -> dict[str, Any]:
    rel = relpath(bundle / "04_CHAIN_SPEC.yaml", ROOT)
    try:
        spec = load_yaml(bundle / "04_CHAIN_SPEC.yaml")
    except Exception as exc:
        findings.append(Finding("error", rel, f"cannot parse chain spec: {exc}"))
        return {}
    if not isinstance(spec, dict):
        findings.append(Finding("error", rel, "chain spec must be a mapping"))
        return {}
    required = ["workflow_id","chain_name","chain_type","stack_id","environment","settlement","data_availability","proof_model","execution","sequencing","gas_token","governance","node_roles","security","operational_limits","human_approval_required"]
    for key in required:
        if key not in spec:
            findings.append(Finding("error", rel, f"missing chain spec field: {key}"))
    chain_type = str(spec.get("chain_type", ""))
    env = str(spec.get("environment", ""))
    settlement = spec.get("settlement") if isinstance(spec.get("settlement"), dict) else {}
    sequencing = spec.get("sequencing") if isinstance(spec.get("sequencing"), dict) else {}
    proof_model = spec.get("proof_model") if isinstance(spec.get("proof_model"), dict) else {}
    security = spec.get("security") if isinstance(spec.get("security"), dict) else {}
    governance = spec.get("governance") if isinstance(spec.get("governance"), dict) else {}
    if chain_type in ROLLUP_TYPES and not settlement.get("layer"):
        findings.append(Finding("error", rel, "L2/L3/rollup specs must include settlement.layer"))
    if chain_type in ROLLUP_TYPES and not sequencing.get("model"):
        findings.append(Finding("error", rel, "rollup specs must include sequencing.model"))
    if chain_type in {"validium", "zkrollup"} and not (proof_model.get("type") or proof_model.get("assumptions")):
        findings.append(Finding("error", rel, "ZK/validium specs must include proof assumptions"))
    if chain_type in L1_TYPES and not (governance.get("consensus_model") or security.get("validator_key_custody") or "validator" in " ".join(map(str, spec.get("node_roles", []))).lower()):
        findings.append(Finding("error", rel, "L1/appchain specs must document validator or consensus model"))
    if env in PROD_ENVS and spec.get("human_approval_required") is not True:
        findings.append(Finding("error", rel, "production/mainnet specs must require human approval"))
    if spec.get("chain_id") is None:
        findings.append(Finding("warning", rel, "chain_id placeholder or value should be present"))
    return spec


def validate_evidence(bundle: Path, spec: dict[str, Any], findings: list[Finding]) -> None:
    evidence = bundle / "evidence"
    for name in REQUIRED_EVIDENCE:
        if not (evidence / name).exists():
            findings.append(Finding("error", relpath(evidence / name, ROOT), "missing evidence file"))
    skills = selected_skills(bundle)
    known = skill_names(ROOT)
    for skill in skills:
        if skill not in known:
            findings.append(Finding("error", relpath(evidence / "selected-skills.md", ROOT), f"unknown selected skill: {skill}"))
    policy_path = evidence / "policy-check.json"
    if policy_path.exists():
        try:
            policy = load_json(policy_path)
        except Exception as exc:
            findings.append(Finding("error", relpath(policy_path, ROOT), f"cannot parse policy-check.json: {exc}"))
            policy = {}
        for key, expected in {"private_keys_written": False, "mnemonics_written": False, "unsafe_rpc_exposure": False}.items():
            if policy.get(key) is not expected:
                findings.append(Finding("error", relpath(policy_path, ROOT), f"policy {key} must be {expected}"))
        if policy.get("mainnet_deploy_commands") != "none":
            findings.append(Finding("error", relpath(policy_path, ROOT), "mainnet_deploy_commands must be none"))
    launch = bundle / "08_LAUNCH_GATES.md"
    if spec.get("environment") in PROD_ENVS and launch.exists() and "human approval" not in launch.read_text(encoding="utf-8").lower():
        findings.append(Finding("error", relpath(launch, ROOT), "production/mainnet launch gates must mention human approval"))


def validate_bundle(bundle: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not bundle.exists():
        return [Finding("error", str(bundle), "bundle path does not exist")]
    for filename in REQUIRED_ROOT_FILES:
        if not (bundle / filename).exists():
            findings.append(Finding("error", relpath(bundle / filename, ROOT), "missing required artifact file"))
    for dirname in ["configs/docker-compose", "configs/systemd", "configs/terraform", "configs/ansible", "configs/k8s", "configs/prometheus", "configs/grafana", "configs/nginx", "configs/chain-registry", "evidence"]:
        if not (bundle / dirname).exists():
            findings.append(Finding("error", relpath(bundle / dirname, ROOT), "missing required artifact directory"))
    spec = validate_chain_spec(bundle, findings) if (bundle / "04_CHAIN_SPEC.yaml").exists() else {}
    validate_evidence(bundle, spec, findings)
    findings.extend(scan_path(bundle, ROOT))
    return findings


def run_secret_scan(target: Path, findings: list[Finding]) -> None:
    script = ROOT / "plugins" / "evm-chain-engineering-pro" / "scripts" / "scan_secrets.py"
    result = subprocess.run([sys.executable, str(script), "--path", str(target), "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        findings.append(Finding("error", relpath(target, ROOT), "strict secret scan failed"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate blockchain engineering artifact bundles.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path")
    group.add_argument("--all")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    args = parser.parse_args(argv)
    bundles = bundle_paths(args)
    findings: list[Finding] = []
    for bundle in bundles:
        findings.extend(validate_bundle(bundle))
        run_secret_scan(bundle, findings)
    errors = [f for f in findings if f.level == "error" or (args.strict and f.level == "warning")]
    report = Report(ok=not errors, script="scripts/validate_artifact_bundle.py", target=args.path or args.all, summary={"bundles_checked": len(bundles), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_out:
        write_markdown_report(args.markdown_out, "Artifact Bundle Validation Report", report, ["validate_artifact_bundle"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
