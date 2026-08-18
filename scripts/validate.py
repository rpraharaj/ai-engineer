#!/usr/bin/env python3
"""Validate skills against the portable Agent Skills frontmatter rules used by this pack."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED_KEYS = {"name", "description", "license", "metadata", "compatibility"}
HOST_ONLY_KEYS = {
    "when-to-use",
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "model",
    "allowed-tools",
    "disallowed-tools",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HOST_WORDS = re.compile(
    r"\b(grok|claude code|cursor|codex|copilot|gemini cli|spawn_subagent|todo_write)\b",
    re.I,
)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, object] = {}
    current_map: dict[str, str] | None = None
    map_key: str | None = None
    for line in raw.splitlines():
        if current_map is not None and (line.startswith("  ") or line.startswith("\t")):
            if ":" not in line:
                raise ValueError(f"invalid metadata line: {line!r}")
            k, v = line.strip().split(":", 1)
            current_map[k.strip()] = v.strip().strip('"')
            continue
        current_map = None
        map_key = None
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            current_map = {}
            data[key] = current_map
            map_key = key
            continue
        data[key] = value.strip('"')
        _ = map_key
    return data, body


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        data, body = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{path}: {exc}"]

    folder = path.parent.name
    name = data.get("name")
    desc = data.get("description")

    for key in data:
        if key in HOST_ONLY_KEYS:
            errors.append(f"{path}: host-only frontmatter key {key!r}")
        elif key not in ALLOWED_KEYS:
            errors.append(f"{path}: unknown frontmatter key {key!r}")

    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"{path}: invalid name {name!r}")
    elif name != folder:
        errors.append(f"{path}: name {name!r} does not match folder {folder!r}")

    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{path}: description is required")
    elif len(desc) > 1024:
        errors.append(f"{path}: description is {len(desc)} chars (max 1024)")

    if "license" in data and not isinstance(data["license"], str):
        errors.append(f"{path}: license must be a string")

    if HOST_WORDS.search(body):
        errors.append(f"{path}: skill body mentions a host product or host-only tool")

    lines = text.count("\n") + 1
    if lines > 500:
        errors.append(f"{path}: SKILL.md is {lines} lines (keep under 500)")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent / "skills"
    if not root.is_dir():
        print(f"no skills directory at {root}", file=sys.stderr)
        return 1
    errors: list[str] = []
    skills = sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    if not skills:
        print(f"no SKILL.md files under {root}", file=sys.stderr)
        return 1
    for skill in skills:
        errors.extend(validate_skill(skill / "SKILL.md"))

    pack_root = root.parent
    template = pack_root / "templates" / "AGENTS.md"
    vendored = root / "explore-codebase" / "references" / "agents-template.md"
    if not template.is_file():
        errors.append(f"missing {template}")
    elif not vendored.is_file():
        errors.append(f"missing {vendored} (must match templates/AGENTS.md)")
    elif template.read_text(encoding="utf-8") != vendored.read_text(encoding="utf-8"):
        errors.append(
            "templates/AGENTS.md and skills/explore-codebase/references/agents-template.md must be identical"
        )

    readme = pack_root / "README.md"
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        for skill in skills:
            token = f"`{skill.name}`"
            if token not in readme_text:
                errors.append(f"README.md does not mention {token}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"ok: {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
