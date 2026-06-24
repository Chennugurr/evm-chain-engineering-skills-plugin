import re
from conftest import SKILLS


def description(path):
    text = path.read_text()
    block = re.match(r"^---\n(.*?)\n---", text, re.S).group(1)
    for line in block.splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    raise AssertionError("missing description")


def test_descriptions_have_activation_and_boundaries():
    descriptions = [description(path / "SKILL.md") for path in SKILLS.iterdir() if path.is_dir()]
    assert len(set(descriptions)) == len(descriptions)
    for desc in descriptions:
        assert "Use" in desc or "use" in desc
        assert "Do not use" in desc or "Do not" in desc
        assert any(term in desc.lower() for term in ["evm", "rollup", "chain", "bridge", "rpc", "sequencer", "validator", "prover"])
