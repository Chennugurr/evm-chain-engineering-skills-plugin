
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins" / "evm-chain-engineering-pro"
ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
HEX_64_RE = re.compile(r"0x[a-fA-F0-9]{64}")
PLACEHOLDER_ADDR = "0x0000000000000000000000000000000000000000"

ADMIN_PORTS = {8546, 8551, 6060, 6061, 9000, 9090, 9093, 3000, 5432, 6379, 2375}


def emit(payload: dict[str, Any], as_json: bool = False) -> int:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        status = payload.get("status", "ok")
        print(f"status: {status}")
        for item in payload.get("errors", []):
            print(f"error: {item}")
        for item in payload.get("warnings", []):
            print(f"warning: {item}")
        for key, value in payload.items():
            if key in {"status", "errors", "warnings"}:
                continue
            print(f"{key}: {value}")
    return int(payload.get("exit_code", 0))


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_scalar(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "none"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def read_simple_data(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json" or text.lstrip().startswith(("{", "[")):
        return json.loads(text)
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                data[key] = []
                current_key = key
            else:
                data[key] = parse_scalar(value)
                current_key = key
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def path_arg(value: str | None, default: str = ".") -> Path:
    return Path(value or default).expanduser().resolve()


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def detect_host() -> dict[str, Any]:
    mem_total_mb = None
    swap_total_mb = None
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        values: dict[str, int] = {}
        for line in meminfo.read_text(encoding="utf-8", errors="ignore").splitlines():
            parts = line.split()
            if len(parts) >= 2:
                values[parts[0].rstrip(":")] = int(parts[1]) // 1024
        mem_total_mb = values.get("MemTotal")
        swap_total_mb = values.get("SwapTotal")
    disk = shutil.disk_usage(str(ROOT))
    tools = ["docker", "docker-compose", "systemctl", "python3", "go", "cargo", "node", "npm", "forge", "git", "jq", "curl", "openssl"]
    return {
        "os": platform.platform(),
        "kernel": platform.release(),
        "cpu_count": os.cpu_count() or 0,
        "machine": platform.machine(),
        "ram_mb": mem_total_mb,
        "swap_mb": swap_total_mb,
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_free_gb": round(disk.free / (1024 ** 3), 2),
        "gpu_detected": any(command_exists(cmd) for cmd in ["nvidia-smi", "rocm-smi"]),
        "tools": {tool: command_exists(tool) for tool in tools},
    }


def load_requirement_profile(stack: str | None, role: str | None) -> dict[str, Any]:
    candidates = []
    if stack and role:
        candidates.append(PLUGIN_ROOT / "templates" / "requirements" / f"{stack}-{role}.yml")
    if stack:
        candidates.append(PLUGIN_ROOT / "templates" / "requirements" / f"{stack}.yml")
    candidates.append(PLUGIN_ROOT / "templates" / "requirements" / "common.yml")
    for candidate in candidates:
        if candidate.exists():
            payload = read_simple_data(candidate)
            return payload if isinstance(payload, dict) else {}
    return {}


def cmd_check_host_requirements(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Read-only host inspection for chain node requirements.")
    parser.add_argument("--stack")
    parser.add_argument("--role")
    parser.add_argument("--environment", default="devnet")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    detected = detect_host()
    req = load_requirement_profile(args.stack, args.role)
    warnings: list[str] = []
    errors: list[str] = []
    min_cpu = int(req.get("min_cpu", 0) or 0)
    min_ram_mb = int(req.get("min_ram_mb", 0) or 0)
    min_disk_gb = int(req.get("min_disk_gb", 0) or 0)
    if min_cpu and detected["cpu_count"] < min_cpu:
        (errors if args.strict else warnings).append(f"cpu_count {detected['cpu_count']} is below required {min_cpu}")
    if min_ram_mb and (detected.get("ram_mb") or 0) < min_ram_mb:
        (errors if args.strict else warnings).append(f"ram_mb {detected.get('ram_mb')} is below required {min_ram_mb}")
    if min_disk_gb and detected["disk_free_gb"] < min_disk_gb:
        (errors if args.strict else warnings).append(f"disk_free_gb {detected['disk_free_gb']} is below required {min_disk_gb}")
    for tool in as_list(req.get("required_tools")):
        if tool and not detected["tools"].get(str(tool), False):
            (errors if args.strict else warnings).append(f"required tool missing: {tool}")
    payload = {"status": "fail" if errors else "ok", "errors": errors, "warnings": warnings, "detected": detected, "requirements": req, "exit_code": 1 if errors else 0}
    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return emit(payload, args.json)


def parse_int_auto(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value, 16) if value.startswith("0x") else int(value)
        except ValueError:
            return None
    return None


def cmd_validate_genesis(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate EVM L1 genesis and optional chain metadata.")
    parser.add_argument("--genesis", required=True)
    parser.add_argument("--chain-metadata")
    parser.add_argument("--stack")
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors: list[str] = []
    warnings: list[str] = []
    try:
        genesis = read_json(path_arg(args.genesis))
    except Exception as exc:  # noqa: BLE001
        return emit({"status": "fail", "errors": [f"unable to parse genesis: {exc}"], "warnings": [], "exit_code": 1}, args.json)
    config = genesis.get("config", {}) if isinstance(genesis, dict) else {}
    chain_id = config.get("chainId") or genesis.get("chainId") if isinstance(genesis, dict) else None
    if parse_int_auto(chain_id) in (None, 1, 5, 11155111, 17000):
        warnings.append("chainId is missing or collides with a well-known public Ethereum network")
    alloc = genesis.get("alloc", {}) if isinstance(genesis, dict) else {}
    if not isinstance(alloc, dict):
        errors.append("alloc must be an object")
    else:
        for addr, account in alloc.items():
            if not ADDRESS_RE.fullmatch(addr):
                errors.append(f"malformed alloc address: {addr}")
            if addr.lower() == PLACEHOLDER_ADDR.lower():
                warnings.append("alloc includes the zero address placeholder")
            balance = account.get("balance") if isinstance(account, dict) else None
            if balance is None:
                warnings.append(f"alloc {addr} has no balance")
            elif parse_int_auto(balance) is None:
                errors.append(f"alloc {addr} has malformed balance")
    fork_keys = [key for key in config if key.endswith("Block")]
    fork_values = [(key, parse_int_auto(config.get(key))) for key in fork_keys]
    numeric = [item for item in fork_values if item[1] is not None]
    if len(numeric) != len(fork_values):
        errors.append("one or more fork block values are malformed")
    if [value for _, value in numeric] != sorted(value for _, value in numeric):
        warnings.append("fork block ordering is not monotonic")
    gas_limit = parse_int_auto(genesis.get("gasLimit")) if isinstance(genesis, dict) else None
    if gas_limit is None or gas_limit <= 0:
        errors.append("gasLimit must be a positive integer or hex value")
    if args.chain_metadata:
        try:
            metadata = read_simple_data(path_arg(args.chain_metadata))
            meta_chain_id = metadata.get("chainId") if isinstance(metadata, dict) else None
            if meta_chain_id is not None and parse_int_auto(meta_chain_id) != parse_int_auto(chain_id):
                errors.append("chain metadata chainId does not match genesis chainId")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"unable to parse chain metadata: {exc}")
    payload = {"status": "fail" if errors else "ok", "errors": errors, "warnings": warnings, "exit_code": 1 if errors else 0}
    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return emit(payload, args.json)


def collect_addresses(value: Any, prefix: str = "") -> dict[str, str]:
    found: dict[str, str] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(item, str) and ADDRESS_RE.fullmatch(item):
                found[path] = item.lower()
            else:
                found.update(collect_addresses(item, path))
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            found.update(collect_addresses(item, f"{prefix}[{idx}]"))
    return found


def cmd_validate_rollup_config(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate rollup config files using safe generic stack checks.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--stack", required=True, choices=["op-stack", "orbit", "polygon-cdk", "zk-stack", "modular"])
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = read_simple_data(path_arg(args.config))
    except Exception as exc:  # noqa: BLE001
        return emit({"status": "fail", "errors": [f"unable to parse config: {exc}"], "warnings": [], "exit_code": 1}, args.json)
    if not isinstance(data, dict):
        errors.append("config must be an object")
    else:
        addresses = collect_addresses(data)
        for path, addr in addresses.items():
            if addr == PLACEHOLDER_ADDR.lower():
                warnings.append(f"placeholder address at {path}")
        inverse: dict[str, list[str]] = {}
        for path, addr in addresses.items():
            inverse.setdefault(addr, []).append(path)
        for addr, paths in inverse.items():
            roleish = [p for p in paths if any(term in p.lower() for term in ["admin", "batcher", "proposer", "sequencer", "validator", "prover", "relayer"])]
            if len(roleish) > 1:
                warnings.append(f"role address reused across {', '.join(roleish)}")
        if not any("chain" in str(key).lower() for key in data):
            warnings.append("no chain ID or parent chain field detected")
        if not any("da" in str(key).lower() or "data" in str(key).lower() for key in data):
            warnings.append("no data availability mode detected")
        if args.stack == "op-stack" and not any("batcher" in p.lower() for p in addresses):
            warnings.append("OP Stack config should separate batcher role key")
        if args.stack == "zk-stack" and not any("prover" in p.lower() for p in addresses):
            warnings.append("ZK Stack config should document prover or dummy executor mode")
    payload = {"status": "fail" if errors else "ok", "errors": errors, "warnings": warnings, "exit_code": 1 if errors else 0}
    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return emit(payload, args.json)


SECRET_PATTERNS = [
    ("private_key", re.compile(r"(?i)(private[_-]?key|secret[_-]?key)\s*[:=]\s*['\"]?0x[a-f0-9]{64}")),
    ("raw_private_key", re.compile(r"(?i)-----BEGIN (?:EC |RSA |OPENSSH )?PRIVATE KEY-----")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("api_key", re.compile(r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{24,}")),
    ("mnemonic", re.compile(r"(?i)(mnemonic|seed phrase)\s*[:=]\s*['\"]?[a-z]+(?:\s+[a-z]+){11,}")),
]
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", "dist", "build", "node_modules", ".mypy_cache", ".ruff_cache"}
SAFE_MARKERS = ["allow-secret-placeholder", "CHANGE_ME", "REPLACE_ME", "${", "example", "placeholder"]


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def scan_path(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    for path in files:
        if should_skip(path.relative_to(root) if path != root else path):
            continue
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            findings.append({"file": str(path), "line": 1, "kind": "env_file", "severity": "critical", "text": "environment secret file"})
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if any(marker in line for marker in SAFE_MARKERS):
                continue
            for kind, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append({"file": str(path), "line": line_no, "kind": kind, "severity": "critical", "text": line.strip()[:120]})
    return findings


def cmd_scan_secrets(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Scan files for likely secrets without modifying anything.")
    parser.add_argument("--path", default=".")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    findings = scan_path(path_arg(args.path))
    errors = [f"{f['kind']} in {f['file']}:{f['line']}" for f in findings if f["severity"] == "critical"]
    payload = {"status": "fail" if errors else "ok", "errors": errors if args.strict else [], "warnings": [] if args.strict else errors, "findings": findings, "exit_code": 1 if errors and args.strict else 0}
    return emit(payload, args.json)


def parse_values(path: str | None) -> dict[str, Any]:
    values = {
        "chain_name": "example-chain",
        "stack": "op-stack",
        "environment": "devnet",
        "role": "sequencer",
        "image_tag": "v0.1.0",
        "service_user": "chainops",
        "rpc_port": "8545",
        "metrics_port": "9100",
        "domain": "chain.example.com",
        "runbook_url": "https://example.com/runbooks/chain",
    }
    if path:
        loaded = read_simple_data(path_arg(path))
        if isinstance(loaded, dict):
            values.update(loaded)
    return values


def render_text(template: str, values: dict[str, Any]) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        return str(values.get(key, ""))
    return re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", repl, template)


def render_template_file(template_path: Path, values: dict[str, Any]) -> str:
    return render_text(template_path.read_text(encoding="utf-8"), values)


def cmd_render_docker_compose(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render Docker Compose templates with placeholders only.")
    parser.add_argument("--stack", default="op-stack")
    parser.add_argument("--environment", default="devnet")
    parser.add_argument("--roles", default="sequencer,rpc")
    parser.add_argument("--output-dir")
    parser.add_argument("--values")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    values = parse_values(args.values)
    values.update({"stack": args.stack, "environment": args.environment, "roles": args.roles})
    template = PLUGIN_ROOT / "templates" / "docker-compose" / "docker-compose.chain.yml.j2"
    rendered = render_template_file(template, values)
    written: list[str] = []
    if args.output_dir and not args.dry_run:
        out = path_arg(args.output_dir) / f"docker-compose.{args.stack}.{args.environment}.yml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        written.append(str(out))
    else:
        print(rendered)
    return emit({"status": "ok", "errors": [], "warnings": ["VERIFY_CURRENT_DOCS before production use"], "written": written, "exit_code": 0}, args.json)


def cmd_render_systemd_units(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render hardened systemd unit templates for chain roles.")
    parser.add_argument("--stack", default="op-stack")
    parser.add_argument("--environment", default="devnet")
    parser.add_argument("--roles", default="sequencer")
    parser.add_argument("--output-dir")
    parser.add_argument("--values")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    values = parse_values(args.values)
    values.update({"stack": args.stack, "environment": args.environment})
    template = PLUGIN_ROOT / "templates" / "systemd" / "chain-role.service.j2"
    written: list[str] = []
    for role in [r.strip() for r in args.roles.split(",") if r.strip()]:
        values["role"] = role
        rendered = render_template_file(template, values)
        if args.output_dir and not args.dry_run:
            out = path_arg(args.output_dir) / f"{values['chain_name']}-{role}.service"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered, encoding="utf-8")
            written.append(str(out))
        else:
            print(rendered)
    return emit({"status": "ok", "errors": [], "warnings": ["unit files reference environment files; never embed private keys"], "written": written, "exit_code": 0}, args.json)


def cmd_render_prometheus_alerts(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render Prometheus alert rules for chain services.")
    parser.add_argument("--stack", default="op-stack")
    parser.add_argument("--environment", default="devnet")
    parser.add_argument("--roles", default="sequencer,rpc")
    parser.add_argument("--output")
    parser.add_argument("--values")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    values = parse_values(args.values)
    values.update({"stack": args.stack, "environment": args.environment, "roles": args.roles})
    rendered = render_template_file(PLUGIN_ROOT / "templates" / "prometheus" / "alerts.yml.j2", values)
    written = []
    if args.output:
        out = path_arg(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        written.append(str(out))
    else:
        print(rendered)
    return emit({"status": "ok", "errors": [], "warnings": [], "written": written, "exit_code": 0}, args.json)


def cmd_validate_firewall_policy(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate firewall policy for unsafe public service exposure.")
    parser.add_argument("--policy", required=True)
    parser.add_argument("--environment", default="devnet")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = read_simple_data(path_arg(args.policy))
    errors: list[str] = []
    warnings: list[str] = []
    ports = []
    if isinstance(data, dict):
        ports = as_list(data.get("public_ports")) + as_list(data.get("ports"))
    for raw in ports:
        try:
            port = int(raw)
        except (TypeError, ValueError):
            warnings.append(f"non-numeric port entry: {raw}")
            continue
        if port in ADMIN_PORTS and args.environment in {"public-testnet", "staging", "production", "mainnet"}:
            errors.append(f"admin/internal port {port} must not be public in {args.environment}")
    return emit({"status": "fail" if errors else "ok", "errors": errors, "warnings": warnings, "exit_code": 1 if errors else 0}, args.json)


def cmd_validate_chain_metadata(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate wallet and chain registry metadata.")
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--environment", default="devnet")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = read_simple_data(path_arg(args.metadata))
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        errors.append("metadata must be an object")
    else:
        chain_id = parse_int_auto(data.get("chainId"))
        if chain_id is None or chain_id <= 0:
            errors.append("chainId must be a positive integer")
        for field in ["rpc", "explorers"]:
            for url in as_list(data.get(field)):
                raw = url.get("url") if isinstance(url, dict) else url
                if not isinstance(raw, str):
                    continue
                parsed = urlparse(raw)
                if args.environment in {"public-testnet", "production", "mainnet"} and parsed.hostname in {"localhost", "127.0.0.1", "0.0.0.0"}:
                    errors.append(f"public metadata cannot use localhost URL: {raw}")
                if parsed.scheme not in {"http", "https", "ws", "wss"}:
                    warnings.append(f"unexpected URL scheme: {raw}")
        native = data.get("nativeCurrency")
        if not isinstance(native, dict) or not native.get("symbol"):
            warnings.append("nativeCurrency.symbol is missing")
    return emit({"status": "fail" if errors else "ok", "errors": errors, "warnings": warnings, "exit_code": 1 if errors else 0}, args.json)


def cmd_dry_run_deploy_plan(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Print what a deployment plan would change without executing it.")
    parser.add_argument("--plan", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--stack", required=True)
    parser.add_argument("--i-understand-mainnet-risk", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.environment.lower() in {"mainnet", "production"} and not args.i_understand_mainnet_risk:
        return emit({"status": "blocked", "errors": ["mainnet-like dry run requires --i-understand-mainnet-risk"], "warnings": [], "exit_code": 2}, args.json)
    data = read_simple_data(path_arg(args.plan))
    changes = data.get("changes", []) if isinstance(data, dict) else []
    payload = {"status": "ok", "errors": [], "warnings": ["dry run only; no changes executed"], "stack": args.stack, "environment": args.environment, "planned_changes": changes, "exit_code": 0}
    return emit(payload, args.json)


def cmd_compare_stack_versions(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Compare pinned stack versions against maintained source notes.")
    parser.add_argument("--lockfile", default="docs/stack-registry.md")
    parser.add_argument("--sources", default="docs/upstream-sources.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    lock = path_arg(args.lockfile)
    sources = path_arg(args.sources)
    warnings = []
    if not lock.exists():
        warnings.append("lockfile missing")
    if not sources.exists():
        warnings.append("upstream sources missing")
    status = []
    if lock.exists():
        for line in lock.read_text(encoding="utf-8").splitlines():
            if line.startswith("|") and "VERIFY_CURRENT_DOCS" in line:
                parts = [p.strip() for p in line.strip("|").split("|")]
                if parts:
                    status.append({"stack": parts[0], "status": "unknown", "note": "VERIFY_CURRENT_DOCS"})
    return emit({"status": "ok", "errors": [], "warnings": warnings, "stacks": status, "exit_code": 0}, args.json)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value or "adr"


def cmd_generate_adr(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate an architecture decision record from structured answers.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--chain-type", required=True)
    parser.add_argument("--stack", required=True)
    parser.add_argument("--settlement", required=True)
    parser.add_argument("--data-availability", required=True)
    parser.add_argument("--trust-assumptions", required=True)
    parser.add_argument("--open-questions", required=True)
    parser.add_argument("--output-dir", default="docs/adr")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    filename = f"{now}-{slugify(args.title)}.md"
    out = path_arg(args.output_dir) / filename
    content = f"""# Architecture Decision Record: {args.title}\n\n## Decision Summary\n\nVERIFY_CURRENT_DOCS before using this ADR for production deployment.\n\n## Chain Type\n\n{args.chain_type}\n\n## Stack\n\n{args.stack}\n\n## Settlement\n\n{args.settlement}\n\n## Data Availability\n\n{args.data_availability}\n\n## Security Assumptions\n\n{args.trust_assumptions}\n\n## Risks\n\nSecurity review required for production, public testnet, bridges, admin keys, sequencers, validators, provers, and relayers.\n\n## Open Questions\n\n{args.open_questions}\n\n## Next Steps\n\nRun config validators, produce a dry-run plan, and complete chain-security-reviewer outputs.\n"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return emit({"status": "ok", "errors": [], "warnings": ["ADR generated; review before use"], "path": str(out), "exit_code": 0}, args.json)


def cmd_backup_restore_check(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate backup config and produce restore checklist signals.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = read_simple_data(path_arg(args.config))
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        errors.append("backup config must be an object")
    else:
        for key in ["checksum", "retention_days", "restore_destination", "drill_schedule"]:
            if key not in data:
                warnings.append(f"missing backup field: {key}")
        if str(data.get("restore_destination", "")).strip() in {"", "/", "/data"}:
            warnings.append("restore destination should be explicit and isolated")
    return emit({"status": "fail" if errors else "ok", "errors": errors, "warnings": warnings, "restore_checklist": ["verify checksum", "restore to isolated host", "compare height/state", "record drill result"], "exit_code": 1 if errors else 0}, args.json)


DISPATCH = {
    "check_host_requirements.py": cmd_check_host_requirements,
    "validate_genesis.py": cmd_validate_genesis,
    "validate_rollup_config.py": cmd_validate_rollup_config,
    "scan_secrets.py": cmd_scan_secrets,
    "render_docker_compose.py": cmd_render_docker_compose,
    "render_systemd_units.py": cmd_render_systemd_units,
    "render_prometheus_alerts.py": cmd_render_prometheus_alerts,
    "validate_firewall_policy.py": cmd_validate_firewall_policy,
    "validate_chain_metadata.py": cmd_validate_chain_metadata,
    "dry_run_deploy_plan.py": cmd_dry_run_deploy_plan,
    "compare_stack_versions.py": cmd_compare_stack_versions,
    "generate_adr.py": cmd_generate_adr,
    "backup_restore_check.py": cmd_backup_restore_check,
}


def main(script_name: str | None = None, argv: list[str] | None = None) -> int:
    script = Path(script_name or sys.argv[0]).name
    fn = DISPATCH.get(script)
    if fn is None:
        print(f"unknown tool: {script}", file=sys.stderr)
        return 2
    return fn(list(sys.argv[1:] if argv is None else argv))
