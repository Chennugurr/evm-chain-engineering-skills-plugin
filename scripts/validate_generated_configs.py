#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lib.repo import find_repo_root, relpath
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report
from lib.safety import SAFE_PLACEHOLDERS, scan_text
from lib.yaml_json import load_yaml

ROOT = find_repo_root(Path(__file__))


def targets(args: argparse.Namespace) -> list[Path]:
    if args.path:
        return [Path(args.path)]
    base = Path(args.all or "fixtures/artifact-bundles")
    return sorted([item for item in base.iterdir() if item.is_dir()]) if base.exists() else []


def iter_files(bundle: Path) -> list[Path]:
    return [p for p in (bundle / "configs").rglob("*") if p.is_file()] if (bundle / "configs").exists() else []


def validate_compose(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = relpath(path, ROOT)
    try:
        data = load_yaml(path)
    except Exception as exc:
        return [Finding("error", rel, f"compose YAML parse failed: {exc}")]
    if not isinstance(data, dict) or not isinstance(data.get("services"), dict):
        findings.append(Finding("error", rel, "compose file must contain services mapping"))
        return findings
    for name, service in data["services"].items():
        if not isinstance(service, dict):
            continue
        image = str(service.get("image", ""))
        if image.endswith(":latest") or (image and ":" not in image and "@sha256:" not in image):
            findings.append(Finding("error", rel, f"service {name} image is not pinned"))
        if service.get("privileged") is True:
            findings.append(Finding("error", rel, f"service {name} uses privileged mode"))
        if service.get("network_mode") == "host":
            findings.append(Finding("error", rel, f"service {name} uses host networking"))
        env = service.get("environment", {})
        items = env.items() if isinstance(env, dict) else []
        for key, value in items:
            if re.search(r"(?i)(PRIVATE_KEY|MNEMONIC|SEED|SECRET)", str(key)) and str(value) not in SAFE_PLACEHOLDERS and "external" not in str(value).lower():
                findings.append(Finding("error", rel, f"service {name} has inline secret-like environment value"))
        for port in service.get("ports", []) or []:
            if isinstance(port, str) and port.startswith("0.0.0.0") and any(admin in port for admin in ["8546", "8551"]):
                findings.append(Finding("error", rel, f"service {name} exposes admin/debug port publicly"))
    return findings


def validate_systemd(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    rel = relpath(path, ROOT)
    findings: list[Finding] = []
    for section in ["[Unit]", "[Service]", "[Install]"]:
        if section not in text:
            findings.append(Finding("error", rel, f"missing {section}"))
    if "User=" not in text:
        findings.append(Finding("error", rel, "service must set User="))
    if "User=root" in text:
        findings.append(Finding("error", rel, "service must not run as root by default"))
    if "Restart=" not in text:
        findings.append(Finding("error", rel, "service should set Restart="))
    if "WorkingDirectory=" not in text and "WorkingDirectory intentionally omitted" not in text:
        findings.append(Finding("error", rel, "service should set WorkingDirectory= or explain omission"))
    return findings


def validate_prometheus(path: Path, bundle_text: str) -> list[Finding]:
    rel = relpath(path, ROOT)
    try:
        data = load_yaml(path)
    except Exception as exc:
        return [Finding("error", rel, f"prometheus YAML parse failed: {exc}")]
    text = path.read_text(encoding="utf-8").lower()
    findings: list[Finding] = []
    if not isinstance(data, dict) or not data.get("groups"):
        findings.append(Finding("error", rel, "prometheus rules must contain groups"))
    if "down" not in text and "unavailable" not in text:
        findings.append(Finding("error", rel, "rules must cover node down or RPC unavailable"))
    if "disk" not in text:
        findings.append(Finding("error", rel, "rules must cover disk usage"))
    if any(role in bundle_text.lower() for role in ["sequencer", "batcher", "proposer", "prover", "validator"]) and "role" not in text:
        findings.append(Finding("error", rel, "rules must include role-specific health coverage"))
    return findings


def validate_nginx(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    rel = relpath(path, ROOT)
    findings: list[Finding] = []
    if re.search(r"(?i)(admin|debug).{0,80}proxy_pass", text):
        findings.append(Finding("error", rel, "nginx must not proxy admin/debug RPC by default"))
    if "rate" not in text.lower():
        findings.append(Finding("warning", rel, "nginx sample should mention rate limiting"))
    if "ssl_certificate" not in text and "TLS termination is external" not in text:
        findings.append(Finding("warning", rel, "nginx sample should include TLS placeholder or external TLS note"))
    return findings


def validate_k8s(path: Path) -> list[Finding]:
    rel = relpath(path, ROOT)
    try:
        load_yaml(path)
    except Exception as exc:
        return [Finding("error", rel, f"k8s YAML parse failed: {exc}")]
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    if "resources:" not in text:
        findings.append(Finding("error", rel, "k8s containers should include resources"))
    if "privileged: true" in text:
        findings.append(Finding("error", rel, "privileged k8s containers are forbidden in fixtures"))
    if re.search(r"(?i)kind:\s*Secret", text):
        findings.append(Finding("error", rel, "inline Kubernetes Secret is forbidden in fixtures"))
    if "LoadBalancer" in text and re.search(r"(?i)(admin|debug)", text):
        findings.append(Finding("error", rel, "admin/debug RPC must not be exposed by LoadBalancer"))
    return findings


def validate_terraform(path: Path) -> list[Finding]:
    rel = relpath(path, ROOT)
    findings: list[Finding] = []
    if path.suffix == ".tfvars" and not path.name.endswith(".example"):
        findings.append(Finding("error", rel, ".tfvars samples must use .example suffix"))
    text = path.read_text(encoding="utf-8")
    if re.search(r"(?i)(access_key|secret_key|password)\s*=", text):
        findings.append(Finding("error", rel, "terraform sample contains hardcoded credential field"))
    return findings


def validate_bundle(bundle: Path) -> list[Finding]:
    findings: list[Finding] = []
    bundle_text = ""
    for file_path in bundle.rglob("*"):
        if file_path.is_file():
            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            bundle_text += "\n" + text
            findings.extend(scan_text(text, relpath(file_path, ROOT)))
    for file_path in iter_files(bundle):
        name = file_path.name.lower()
        if name.startswith("docker-compose") or name.startswith("compose"):
            findings.extend(validate_compose(file_path))
        elif name.endswith(".service"):
            findings.extend(validate_systemd(file_path))
        elif file_path.suffix in {".tf", ".tfvars"} or ".tfvars" in name:
            findings.extend(validate_terraform(file_path))
        elif file_path.suffix in {".yaml", ".yml"} and "k8s" in file_path.parts:
            findings.extend(validate_k8s(file_path))
        elif "prometheus" in file_path.parts and file_path.suffix in {".yaml", ".yml"}:
            findings.extend(validate_prometheus(file_path, bundle_text))
        elif "nginx" in file_path.parts and (name.endswith(".conf") or name.endswith(".example")):
            findings.extend(validate_nginx(file_path))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Statically validate generated planning config samples.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path")
    group.add_argument("--all")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    args = parser.parse_args(argv)
    bundles = targets(args)
    findings: list[Finding] = []
    for bundle in bundles:
        findings.extend(validate_bundle(bundle))
    errors = [f for f in findings if f.level == "error" or (args.strict and f.level == "warning")]
    report = Report(ok=not errors, script="scripts/validate_generated_configs.py", target=args.path or args.all, summary={"bundles_checked": len(bundles), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_out:
        write_markdown_report(args.markdown_out, "Generated Config Validation Report", report, ["validate_generated_configs"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
