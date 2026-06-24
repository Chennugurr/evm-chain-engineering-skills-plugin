from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def _simple_yaml_load(text: str) -> Any:
    # Fallback parser for the simple mapping/list YAML committed in this repo.
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    last_key_at_indent: dict[int, str] = {}
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            item = line[2:].strip()
            if not isinstance(parent, list):
                key = last_key_at_indent.get(stack[-1][0])
                if isinstance(stack[-1][1], dict) and key:
                    stack[-1][1][key] = []
                    parent = stack[-1][1][key]
                    stack.append((indent, parent))
                else:
                    raise ValueError("unsupported YAML list placement")
            if ":" in item and not item.startswith(('"', "'")):
                key, value = item.split(":", 1)
                node: dict[str, Any] = {key.strip(): _parse_scalar(value.strip()) if value.strip() else {}}
                parent.append(node)
                if not value.strip():
                    stack.append((indent, node[key.strip()]))
            else:
                parent.append(_parse_scalar(item))
            continue
        if ":" not in line:
            raise ValueError(f"unsupported YAML line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not isinstance(parent, dict):
            raise ValueError("unsupported YAML mapping placement")
        if value == "":
            parent[key] = {}
            last_key_at_indent[indent] = key
            stack.append((indent, parent[key]))
        elif value == "[]":
            parent[key] = []
            last_key_at_indent[indent] = key
        else:
            parent[key] = _parse_scalar(value)
            last_key_at_indent[indent] = key
    return root


def load_yaml(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return _simple_yaml_load(text)


def dump_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml is not None:
        path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=False), encoding="utf-8")
        return
    path.write_text(_to_yaml(value), encoding="utf-8")


def _to_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(_to_yaml(item, indent + 2).rstrip())
            else:
                lines.append(f"{pad}{key}: {_format_scalar(item)}")
        return "\n".join(lines) + "\n"
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(_to_yaml(item, indent + 2).rstrip())
            else:
                lines.append(f"{pad}- {_format_scalar(item)}")
        return "\n".join(lines) + "\n"
    return f"{pad}{_format_scalar(value)}\n"


def _format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    text = str(value)
    if text == "" or text.startswith("<") or ":" in text or "#" in text:
        return json.dumps(text)
    return text


def load_data(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return load_json(path)
    return load_yaml(path)
