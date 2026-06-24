from conftest import PLUGIN, SKILLS

SECURITY_TRIGGERS = ["production", "mainnet", "bridge", "admin", "validator", "sequencer", "prover", "relayer"]


def test_security_skill_triggered_by_sensitive_skills():
    for skill in SKILLS.iterdir():
        if not skill.is_dir():
            continue
        text = (skill / "SKILL.md").read_text().lower()
        if any(trigger in text for trigger in SECURITY_TRIGGERS):
            assert "chain-security-reviewer" in text


def test_no_public_debug_rpc_in_examples():
    for path in (PLUGIN / "examples").rglob("*"):
        if path.is_file():
            text = path.read_text().lower()
            assert "debug" not in text or "public" not in text
            assert "0.0.0.0:8546" not in text
