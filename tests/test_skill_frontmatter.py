import re
from conftest import SKILLS

FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.S)


def parse_frontmatter(path):
    match = FRONTMATTER.match(path.read_text())
    assert match, f"missing frontmatter: {path}"
    data = {}
    for line in match.group(1).splitlines():
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def test_frontmatter_valid_and_names_match():
    for skill in SKILLS.iterdir():
        if not skill.is_dir():
            continue
        data = parse_frontmatter(skill / "SKILL.md")
        assert set(data) == {"name", "description"}
        assert data["name"] == skill.name
        assert re.fullmatch(r"[a-z0-9-]{1,64}", data["name"])
        assert len(data["description"]) >= 140
        assert len(data["description"]) <= 1024
        assert "<" not in data["description"] and ">" not in data["description"]
