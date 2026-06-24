from conftest import ROOT

DEMOS = [
    "op-stack-public-testnet",
    "arbitrum-orbit-l3-anytrust",
    "polygon-cdk-enterprise-validium",
    "zksync-zk-stack-zk-chain",
    "evm-l1-validator-network",
    "modular-rollup-stack-selection",
]
REQUIRED = ["prompt.md", "expected-skills.md", "expected-output.md", "generated-files-tree.txt", "validation.md", "security-review.md", "README.md"]


def test_golden_demo_directories_complete():
    base = ROOT / "examples" / "golden-demos"
    for demo in DEMOS:
        demo_dir = base / demo
        assert demo_dir.is_dir(), demo
        for filename in REQUIRED:
            assert (demo_dir / filename).exists(), f"{demo}/{filename}"
        output = (demo_dir / "expected-output.md").read_text()
        assert "## Architecture Decision Record" in output
        assert "## Security and Trust Assumptions" in output
        validation = (demo_dir / "validation.md").read_text().lower()
        assert "pass/fail" in validation
