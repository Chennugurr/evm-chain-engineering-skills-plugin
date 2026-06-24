#!/usr/bin/env python3
"""Deterministic safety guard for chain engineering commands and generated files."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SECRET_VALUE_RE = re.compile(r"(?i)\b(secret|token|credential|password|mnemonic|seed|private[-_ ]?key|rpc[_-]?url|deployer[_-]?secret)\b\s*[:=]\s*(?!<REDACTED>|REDACTED|\$\{|external-secret-ref|runtime-secret-ref|secret-ref)([^\s'\"]{8,})")
MNEMONIC_CONTEXT_RE = re.compile(r"(?i)(mnemonic|seed phrase)\s*[:=]")
PRIVATE_FLAG_RE = re.compile(r"(?i)--(private-key|mnemonic|seed|deployer-secret|password|rpc-password)(?:=|\s+)\S+")
MAINNET_BROADCAST_RE = re.compile(r"(?i)\b(cast|forge|hardhat|npx hardhat|yarn hardhat|bun hardhat)\b.*\b(--broadcast|send|deploy|create)\b.*\b(mainnet|ethereum|bnb|polygon|arbitrum one|op mainnet|base|avalanche|c-chain|chain-id\s+1|chainid\s+1)\b|\b(--broadcast)\b.*\b(mainnet|chain-id\s+1|chainid\s+1)\b")
DESTRUCTIVE_RE = re.compile(r"(?i)\b(rm\s+-rf\s+/(?:\s|$)|rm\s+-rf\s+\.|docker\s+volume\s+rm|docker\s+system\s+prune|kubectl\s+delete|terraform\s+destroy|ansible-playbook\b.*\bdelete|drop\s+database|wipe|prune\s+archive|erase\s+keys)\b")
ADMIN_RPC_RE = re.compile(r"(?i)(0\.0\.0\.0|\*)[:=].*(8546|8551|6060|9090|9093|5432|6379)|(--http\.addr|--ws\.addr|--authrpc\.addr)\s+0\.0\.0\.0.*\b(debug|admin|personal|engine)\b|\b(debug|admin|personal|engine)\b.*0\.0\.0\.0")
UNPINNED_IMAGE_RE = re.compile(r"(?i)\b(image\s*:\s*[^\s#]+:latest|[\w./-]+:latest\b|uses:\s*[^\s@]+@(main|master|latest))")
CURL_PIPE_RE = re.compile(r"(?i)\b(curl|wget)\b[^\n|;]*(\||\s+-O\s+-)\s*(sudo\s+)?(bash|sh|zsh|python)")
UNSAFE_ENV_RE = re.compile(r"(?i)(\.env|env file|environment file).{0,120}(deployer secret|private key|mnemonic|seed phrase|signer secret|admin key)|(deployer secret|private key|mnemonic|seed phrase|signer secret|admin key).{0,120}(\.env|env file|environment file)|(?:deployer_secret|private_key|mnemonic|seed_phrase)\s*=")
PRODUCTION_RE = re.compile(r"(?i)\b(production|mainnet|public testnet|staging|go-live|launch)\b")
DRY_RUN_RE = re.compile(r"(?i)\b(dry[- ]run|validation|backup|rollback|human review|approval)\b")
CHAIN_ID_RE = re.compile(r"(?i)\b(genesis|chain config|chain metadata)\b")
CHAIN_ID_CHECK_RE = re.compile(r"(?i)\b(chain id|chainid|replay protection|collision)\b")
SAFE_WORDS = ("must not", "do not", "avoid", "<redacted>", "redacted placeholder", "placeholder only", "example.invalid", "external-secret-ref", "runtime-secret-ref")
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules"}


@dataclass
class Finding:
    rule_id: str
    severity: str
    path: str | None
    line: int | None
    message: str
    remediation: str
    matched_preview: str = "redacted"


def redact(value: str) -> str:
    value = SECRET_VALUE_RE.sub(lambda m: m.group(0).split(m.group(2))[0] + "<REDACTED>", value)
    value = PRIVATE_FLAG_RE.sub(lambda m: m.group(0).split()[0] + " <REDACTED>", value)
    value = re.sub(r"https?://[^\s/@:]+:[^\s/@]+@", "https://<REDACTED>@", value)
    return value[:160]


def is_safe_explanation(line: str) -> bool:
    lowered = line.lower()
    return any(word in lowered for word in SAFE_WORDS)


def add(findings: list[Finding], rule_id: str, severity: str, path: str | None, line: int | None, message: str, remediation: str, preview: str) -> None:
    findings.append(Finding(rule_id, severity, path, line, message, remediation, redact(preview)))


def scan_text(text: str, *, path: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines() or [text], 1):
        if SECRET_VALUE_RE.search(line) and not is_safe_explanation(line):
            add(findings, "secret-output", "block", path, line_no, "Possible unredacted secret value in command or file content.", "Use hardware wallet, KMS/HSM, signer service, platform secret manager, or runtime secret injection. Keep examples redacted.", line)
        if MNEMONIC_CONTEXT_RE.search(line) and not is_safe_explanation(line):
            add(findings, "secret-output", "block", path, line_no, "Mnemonic or seed phrase storage pattern detected.", "Never create or store mnemonics. Use external custody and redacted documentation only.", line)
        if PRIVATE_FLAG_RE.search(line):
            add(findings, "private-key-flag", "block", path, line_no, "Private material appears to be passed through command-line flags.", "Use a signer, hardware wallet, KMS/HSM, or runtime secret injection; CLI args can leak through process listings and shell history.", line)
        if MAINNET_BROADCAST_RE.search(line):
            add(findings, "mainnet-broadcast", "block", path, line_no, "Mainnet-like broadcast command detected.", "Produce a dry-run plan, verify addresses, use fork/testnet rehearsal, multisig/timelock, and explicit human approval first.", line)
        if DESTRUCTIVE_RE.search(line) and not re.search(r"(?i)dry[- ]run|review|snapshot|backup|approval", line):
            add(findings, "destructive-filesystem", "block", path, line_no, "Destructive command lacks dry-run, backup, or approval language.", "Run a dry-run, snapshot backups, define rollback, and require explicit human approval.", line)
        if ADMIN_RPC_RE.search(line):
            add(findings, "admin-rpc-exposure", "warn", path, line_no, "Admin/debug/internal service may be exposed publicly.", "Bind to localhost or a private network, firewall it, remove unsafe APIs, and use authenticated internal access only.", line)
        if UNPINNED_IMAGE_RE.search(line):
            add(findings, "unpinned-images", "warn", path, line_no, "Mutable image, action, or binary reference detected.", "Pin by digest, version, or commit and record the upstream source.", line)
        if CURL_PIPE_RE.search(line):
            add(findings, "curl-pipe-shell", "warn", path, line_no, "curl/wget piped directly to a shell.", "Download, verify checksum/signature, inspect, then execute with least privilege.", line)
        if UNSAFE_ENV_RE.search(line) and not is_safe_explanation(line):
            add(findings, "unsafe-env", "block", path, line_no, "Example appears to teach storing deployer or signer secrets in env files.", "Use redacted placeholders in docs and platform secret injection for runtime.", line)
        if PRODUCTION_RE.search(line) and re.search(r"(?i)deploy|launch|apply|broadcast|release", line) and not DRY_RUN_RE.search(line):
            add(findings, "production-without-dry-run", "block", path, line_no, "Production-like action lacks dry-run, validation, backup, rollback, or approval language.", "Add dry-run, validation, backup, rollback, and explicit human review gates.", line)
        if CHAIN_ID_RE.search(line) and not CHAIN_ID_CHECK_RE.search(line):
            add(findings, "chain-id-collision", "warn", path, line_no, "Genesis or chain config mention lacks chain ID uniqueness/replay check language.", "Add chain ID collision and replay protection validation.", line)
    return findings


def extract_text_from_event(raw: str) -> str:
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    parts: list[str] = []
    if isinstance(event, dict):
        tool_input = event.get("tool_input")
        if isinstance(tool_input, dict):
            for key in ("command", "cmd", "text", "content", "patch"):
                value = tool_input.get(key)
                if isinstance(value, str):
                    parts.append(value)
            if not parts:
                parts.append(json.dumps(tool_input, sort_keys=True))
        for key in ("command", "text", "content", "prompt"):
            value = event.get(key)
            if isinstance(value, str):
                parts.append(value)
    return "\n".join(parts) if parts else raw


def iter_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for file_path in path.rglob("*"):
        if file_path.is_file() and not any(part in EXCLUDED_DIRS for part in file_path.parts):
            yield file_path


def scan_path(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        return [Finding("tool-error", "block", str(path), None, "Path does not exist.", "Provide an existing file or directory.", "redacted")]
    for file_path in iter_files(path):
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(text, path=str(file_path)))
    return findings


def approval_valid(path: Path | None) -> bool:
    if path is None or not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if data.get("approved_by") != "human" or not data.get("scope") or not data.get("reason"):
        return False
    try:
        expires = datetime.fromisoformat(str(data.get("expires_at", "")).replace("Z", "+00:00"))
    except ValueError:
        return False
    return expires > datetime.now(timezone.utc)


def apply_approval(findings: list[Finding], approval_file: Path | None) -> list[Finding]:
    if not approval_valid(approval_file):
        return findings
    approved_rules = {"mainnet-broadcast", "production-without-dry-run"}
    adjusted: list[Finding] = []
    for finding in findings:
        if finding.rule_id in approved_rules and finding.severity == "block":
            adjusted.append(Finding(finding.rule_id, "warn", finding.path, finding.line, finding.message + " Human approval marker found; still requires manual review.", finding.remediation, finding.matched_preview))
        else:
            adjusted.append(finding)
    return adjusted


def status_for(findings: list[Finding], strict: bool) -> tuple[str, int]:
    has_block = any(f.severity == "block" for f in findings)
    has_warn = any(f.severity == "warn" for f in findings)
    if has_block:
        return "block", 2
    if has_warn:
        return "warn", 1 if strict else 0
    return "allow", 0


def hook_output(status: str, findings: list[Finding]) -> dict[str, Any]:
    message = "; ".join(f"{f.rule_id}: {f.message}" for f in findings[:3]) or "Policy guard passed."
    if status == "block":
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": message}}
    if status == "warn":
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "Policy guard warning: " + message}}
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow", "permissionDecisionReason": "Policy guard passed."}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan command text, hook events, files, or directories for unsafe blockchain engineering patterns.")
    parser.add_argument("--stdin", action="store_true", help="Read command text or JSON hook event from stdin")
    parser.add_argument("--command", help="Command or content to scan")
    parser.add_argument("--path", help="File or directory to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--strict", action="store_true", help="Return nonzero for warnings")
    parser.add_argument("--allow-offline", action="store_true", help="Accepted for hook compatibility; no network is used")
    parser.add_argument("--approval-file", help="Optional human approval marker for mainnet-like actions")
    parser.add_argument("--hook-output", action="store_true", help="Emit Codex/Claude hook decision JSON")
    args = parser.parse_args(argv)

    findings: list[Finding] = []
    if args.stdin:
        raw = sys.stdin.read()
        findings.extend(scan_text(extract_text_from_event(raw), path="stdin"))
    if args.command:
        findings.extend(scan_text(args.command, path="command"))
    if args.path:
        findings.extend(scan_path(Path(args.path)))
    if not any([args.stdin, args.command, args.path]):
        findings.extend(scan_text(sys.stdin.read(), path="stdin"))

    findings = apply_approval(findings, Path(args.approval_file) if args.approval_file else None)
    status, exit_code = status_for(findings, args.strict)
    payload = {"status": status, "findings": [asdict(f) for f in findings]}
    if args.hook_output:
        print(json.dumps(hook_output(status, findings), indent=2))
    elif args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status: {status}")
        for finding in findings:
            print(f"{finding.severity}: {finding.rule_id}: {finding.message}")
            print(f"  remediation: {finding.remediation}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
