from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() and (candidate / "Makefile").exists():
            return candidate
    return Path(__file__).resolve().parents[2]


def relpath(path: Path, root: Path | None = None) -> str:
    base = root or find_repo_root()
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path)


def skill_names(root: Path | None = None) -> set[str]:
    repo = root or find_repo_root()
    skills = repo / "plugins" / "evm-chain-engineering-pro" / "skills"
    return {item.name for item in skills.iterdir() if item.is_dir()}
