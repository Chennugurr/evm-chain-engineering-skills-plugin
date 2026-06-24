import json
from conftest import PLUGIN, ROOT, SKILLS

EXPECTED_SKILLS = {
    "blockchain-architect", "evm-l1-builder", "op-stack-engineer", "arbitrum-orbit-engineer",
    "polygon-cdk-engineer", "zksync-zk-stack-engineer", "modular-rollup-engineer",
    "data-availability-engineer", "bridge-interop-engineer", "chain-infra-ops", "observability-sre",
    "chain-security-reviewer", "chain-launch-manager", "explorer-indexer-engineer",
}


def test_codex_and_claude_manifests_exist():
    codex = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
    claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    assert codex["name"] == "evm-chain-engineering-pro"
    assert claude["name"] == "evm-chain-engineering-pro"
    assert codex["version"] and claude["version"]
    assert codex["skills"] == "./skills/"
    assert claude["skills"] == "./skills/"


def test_marketplaces_reference_plugin():
    codex_market = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text())
    claude_market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert codex_market["plugins"][0]["name"] == "evm-chain-engineering-pro"
    assert codex_market["plugins"][0]["source"]["path"] == "./plugins/evm-chain-engineering-pro"
    assert claude_market["plugins"][0]["source"] == "./plugins/evm-chain-engineering-pro"


def test_all_skills_present():
    assert {p.name for p in SKILLS.iterdir() if p.is_dir()} == EXPECTED_SKILLS
    for name in EXPECTED_SKILLS:
        assert (SKILLS / name / "SKILL.md").exists()
