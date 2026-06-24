import re
from conftest import PLUGIN, SKILLS

REQUIRED_SECTIONS = [
    "## Purpose", "## Applies To", "## Does Not Apply To", "## Current-Docs Verification Notes",
    "## Core Concepts", "## Decisions", "## Configuration Considerations", "## Server / Infrastructure Considerations",
    "## Security Considerations", "## Monitoring Considerations", "## Common Mistakes", "## Checklist",
    "## TODO / Verify Against Current Docs", "## Version Sensitivity",
]


def test_skill_references_exist_and_have_sections():
    pattern = re.compile(r"`(references/[^`]+\.md)`")
    for skill in SKILLS.iterdir():
        if not skill.is_dir():
            continue
        refs = pattern.findall((skill / "SKILL.md").read_text())
        assert refs, skill
        for rel in refs:
            path = skill / rel
            assert path.exists(), path
            text = path.read_text()
            for section in REQUIRED_SECTIONS:
                assert section in text, f"{section} missing in {path}"


def test_shared_appendix_references_exist():
    shared = PLUGIN / "references"
    refs = list(shared.glob("*.md"))
    assert len(refs) >= 100
    for path in refs:
        text = path.read_text()
        assert "VERIFY_CURRENT_DOCS" in text
        assert "## Security Considerations" in text
