from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .repo import find_repo_root, relpath, skill_names
from .reports import Finding
from .yaml_json import load_json, load_yaml

PLATFORMS = ("codex", "claude")
STRICT_REQUIRED_PROMPTS = (
    "01-op-stack-public-testnet",
    "02-arbitrum-orbit-l3-anytrust",
    "03-polygon-cdk-enterprise-validium",
    "05-evm-l1-validator-network",
    "06-unsafe-private-key-request",
    "07-stack-selection-gaming-chain",
)
ARTIFACT_PROMPTS = {
    "01-op-stack-public-testnet",
    "02-arbitrum-orbit-l3-anytrust",
    "03-polygon-cdk-enterprise-validium",
    "04-zksync-zk-stack-chain",
    "05-evm-l1-validator-network",
}
REFUSAL_PROMPTS = {"06-unsafe-private-key-request"}


def dogfood_root(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "dogfood"


def prompt_id_from_path(path: Path) -> str:
    return path.stem


def prompt_paths(root: Path | None = None) -> list[Path]:
    return sorted((dogfood_root(root) / "prompts").glob("*.md"))


def expected_paths(root: Path | None = None) -> list[Path]:
    return sorted((dogfood_root(root) / "expected").glob("*.yaml"))


def load_expected(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError("expected YAML must be a mapping")
    return data


def expected_by_id(root: Path | None = None) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in expected_paths(root):
        data = load_expected(path)
        result[str(data.get("id") or path.stem)] = data
    return result


def prompt_ids(root: Path | None = None) -> set[str]:
    return {prompt_id_from_path(path) for path in prompt_paths(root)}


def known_skills(root: Path | None = None) -> set[str]:
    return skill_names(root or find_repo_root())


def known_subagents(root: Path | None = None) -> set[str]:
    repo = root or find_repo_root()
    names: set[str] = set()
    for base in [repo / "agents", repo / "plugins" / "evm-chain-engineering-pro" / "agents", repo / ".claude" / "agents"]:
        if not base.exists():
            continue
        for path in base.glob("*.md"):
            names.add(path.stem)
    return names


def transcript_paths(root: Path | None = None, platform: str | None = None) -> list[Path]:
    base = dogfood_root(root) / "transcripts"
    platforms = [platform] if platform else list(PLATFORMS)
    paths: list[Path] = []
    for item in platforms:
        paths.extend(sorted((base / item).glob("*.json")))
    return paths


def live_run_paths(root: Path | None = None, platform: str | None = None) -> list[Path]:
    base = dogfood_root(root) / "live-runs"
    platforms = [platform] if platform else list(PLATFORMS)
    paths: list[Path] = []
    for item in platforms:
        if (base / item).exists():
            paths.extend(sorted(path.parent for path in (base / item).glob("**/METADATA.json")))
    return paths


def hook_observation_paths(root: Path | None = None, platform: str | None = None) -> list[Path]:
    base = dogfood_root(root) / "hooks"
    platforms = [platform] if platform else list(PLATFORMS)
    return [base / item / "observed-hooks.json" for item in platforms]


def load_json_file(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValueError("JSON file must contain an object")
    return data


def load_live_run_metadata(path: Path) -> dict[str, Any]:
    meta = path / "METADATA.json" if path.is_dir() else path
    return load_json_file(meta)


def rel(path: Path, root: Path | None = None) -> str:
    return relpath(path, root or find_repo_root())


def lower_corpus(paths: list[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        files = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()]
        for file_path in files:
            try:
                chunks.append(file_path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue
    return "\n".join(chunks).lower()


def missing_required_fields(data: dict[str, Any], required: list[str]) -> list[str]:
    return [field for field in required if field not in data]


def validate_known_skills(values: list[str], path: Path, findings: list[Finding], root: Path | None = None) -> None:
    known = known_skills(root)
    for skill in values:
        if skill not in known:
            findings.append(Finding("error", rel(path, root), f"unknown skill: {skill}"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
