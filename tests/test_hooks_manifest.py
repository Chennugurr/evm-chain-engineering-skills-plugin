import json
import subprocess
import sys
from pathlib import Path
from conftest import PLUGIN, ROOT

REQUIRED_RULES = {"secret-output", "private-key-flag", "mainnet-broadcast", "destructive-filesystem", "admin-rpc-exposure", "unpinned-images", "curl-pipe-shell", "unsafe-env", "production-without-dry-run", "chain-id-collision"}


def test_hook_manifest_shape_and_rules():
    manifest = PLUGIN / "hooks" / "hooks.json"
    data = json.loads(manifest.read_text())
    assert set(data) == {"hooks"}
    metadata = json.loads((PLUGIN / "hooks" / "policy-metadata.json").read_text())
    assert set(metadata["policy_rule_categories"]) == REQUIRED_RULES
    command = data["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    assert "policy_guard.py" in command
    assert str(Path.home()) not in command
    assert data["hooks"]["PreToolUse"][0]["hooks"][0]["timeout"] <= 30


def test_validate_hooks_script_passes():
    result = subprocess.run([sys.executable, "scripts/validate_hooks.py", "--plugin-root", "plugins/evm-chain-engineering-pro", "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
