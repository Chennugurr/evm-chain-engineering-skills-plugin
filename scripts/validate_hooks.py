#!/usr/bin/env python3
"""Validate bundled plugin hook manifests and referenced policy scripts."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

RULES = {"secret-output", "private-key-flag", "mainnet-broadcast", "destructive-filesystem", "admin-rpc-exposure", "unpinned-images", "curl-pipe-shell", "unsafe-env", "production-without-dry-run", "chain-id-collision"}


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("hook manifest must be an object")
    return data


def validate_command(command: str, plugin_root: Path, errors: list[str], warnings: list[str]) -> None:
    if str(Path.home()) in command or command.startswith("/"):
        errors.append(f"hook command uses local absolute path: {command}")
    if "policy_guard.py" not in command:
        errors.append("hook command must call policy_guard.py")
    script = plugin_root / "scripts" / "policy_guard.py"
    if not script.exists():
        errors.append(f"missing referenced policy guard script: {script}")
        return
    result = subprocess.run([sys.executable, str(script), "--help"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        errors.append("policy_guard.py does not support --help")


def validate_manifest(path: Path, plugin_root: Path) -> tuple[list[str], list[str], set[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data = load(path)
    rules = set(data.get("policy_rule_categories", []))
    missing_rules = RULES - rules
    if missing_rules:
        errors.append(f"missing policy rule categories: {', '.join(sorted(missing_rules))}")
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        errors.append("hooks field must be an object")
        return errors, warnings, rules
    for event, groups in hooks.items():
        if event not in {"PreToolUse", "PostToolUse", "UserPromptSubmit", "Stop", "SessionStart", "PermissionRequest"}:
            warnings.append(f"unrecognized hook event: {event}")
        if not isinstance(groups, list):
            errors.append(f"{event} must be a list")
            continue
        for group in groups:
            if not isinstance(group, dict):
                errors.append(f"{event} group must be an object")
                continue
            for hook in group.get("hooks", []):
                if hook.get("type") != "command":
                    errors.append("only command hooks are expected for this plugin")
                timeout = hook.get("timeout", 0)
                if not isinstance(timeout, int) or timeout <= 0 or timeout > 30:
                    errors.append("hook timeout must be between 1 and 30 seconds")
                command = str(hook.get("command", ""))
                validate_command(command, plugin_root, errors, warnings)
                if "--strict" not in command:
                    warnings.append("hook command should use --strict to fail closed for block rules")
    return errors, warnings, rules


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate plugin hook manifests and referenced scripts.")
    parser.add_argument("--plugin-root", default="plugins/evm-chain-engineering-pro")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    plugin_root = Path(args.plugin_root)
    manifest = plugin_root / "hooks" / "hooks.json"
    errors: list[str] = []
    warnings: list[str] = []
    if not manifest.exists():
        errors.append(f"missing hook manifest: {manifest}")
        rules: set[str] = set()
    else:
        try:
            hook_errors, hook_warnings, rules = validate_manifest(manifest, plugin_root)
            errors.extend(hook_errors)
            warnings.extend(hook_warnings)
        except Exception as exc:
            errors.append(str(exc))
            rules = set()
    status = "fail" if errors else ("warn" if warnings else "pass")
    payload = {"status": status, "errors": errors, "warnings": warnings, "rule_categories": sorted(rules)}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status: {status}")
        for error in errors:
            print(f"error: {error}")
        for warning in warnings:
            print(f"warning: {warning}")
    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
