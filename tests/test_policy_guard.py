import json
import subprocess
import sys
from conftest import ROOT

sys.path.insert(0, str(ROOT / "scripts"))

from lib.safety import scan_text  # noqa: E402

SCRIPT = ROOT / "scripts" / "policy_guard.py"


def run_guard(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def payload(result):
    return json.loads(result.stdout)


def test_secret_like_content_is_redacted_and_blocked():
    result = run_guard("--command", "DEPLOYER_SECRET=not-redacted-sentinel", "--json", "--strict")
    assert result.returncode == 2
    data = payload(result)
    assert data["status"] == "block"
    assert data["findings"][0]["matched_preview"].endswith("<REDACTED>")


def test_mainnet_broadcast_is_blocked():
    result = run_guard("--command", "forge script Deploy --broadcast --rpc-url ethereum-mainnet", "--json", "--strict")
    assert result.returncode == 2
    assert any(f["rule_id"] == "mainnet-broadcast" for f in payload(result)["findings"])


def test_local_dev_command_allowed():
    result = run_guard("--command", "anvil --host 127.0.0.1", "--json", "--strict")
    assert result.returncode == 0
    assert payload(result)["status"] == "allow"


def test_unsafe_env_storage_blocked():
    result = run_guard("--command", "write deployer secret to committed .env file", "--json", "--strict")
    assert result.returncode == 2
    assert any(f["rule_id"] == "unsafe-env" for f in payload(result)["findings"])


def test_unpinned_images_warn():
    result = run_guard("--command", "image: ghcr.io/example/node:latest", "--json")
    assert result.returncode == 0
    assert payload(result)["status"] == "warn"


def test_private_material_flag_blocked_even_when_redacted():
    result = run_guard("--command", "forge script Deploy --private-key <REDACTED>", "--json", "--strict")
    assert result.returncode == 2
    assert any(f["rule_id"] == "private-key-flag" for f in payload(result)["findings"])


def test_hook_output_denies_with_zero_exit_for_codex_contract():
    result = run_guard("--command", "forge script Deploy --broadcast --rpc-url ethereum-mainnet", "--strict", "--hook-output")
    assert result.returncode == 0
    data = payload(result)
    assert data["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    assert data["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_engineering_public_testnet_text_is_not_admin_rpc_warning():
    findings = scan_text("Use the EVM Chain Engineering plugin for a public testnet RPC plan.", "test.md")
    assert findings == []
