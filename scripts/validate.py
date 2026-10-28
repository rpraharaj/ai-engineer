#!/usr/bin/env python3
"""Validate skills against the portable Agent Skills frontmatter rules used by this pack."""

from __future__ import annotations

import argparse
import json
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


def parse_string(value: str) -> str:
    """Read this pack's deliberately small YAML string subset, without dependencies."""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except ValueError as exc:
            raise ValueError(f"invalid quoted string: {value!r}") from exc
        if not isinstance(parsed, str):
            raise ValueError("expected a string")
        return parsed
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise ValueError(f"invalid quoted string: {value!r}")
        return value[1:-1].replace("''", "'")
    value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
    if not value or value.lower() in {"true", "false", "null", "~", "yes", "no", "on", "off"}:
        raise ValueError("expected a non-empty string; quote YAML boolean/null values")
    numeric = r"[-+]?(?:0[xob][0-9a-f_]+|(?:\d[\d_.]*|\.\d+)(?:[eE][-+]?\d+)?|\.inf|\.nan)"
    if re.fullmatch(numeric, value, re.I) or re.match(r"^\d{4}-\d{2}-\d{2}(?:$|[Tt ])", value):
        raise ValueError("expected a string; quote numeric/date values")
    if value[0] in "[]{}#&*!|>%@`" or re.search(r":(?:\s|$)", value) or re.match(r"[-?:](?:\s|$)", value):
        raise ValueError("unsupported YAML value; use a plain or quoted string")
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    data: dict[str, object] = {}
    metadata: dict[str, str] | None = None
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            raise ValueError("frontmatter indentation must use spaces")
        nested = line.startswith("  ") and not line.startswith("   ")
        if line.startswith(" ") and not nested:
            raise ValueError("metadata entries require exactly two spaces")
        if nested and metadata is None:
            raise ValueError("only metadata may contain indented entries")
        raw = line[2:] if nested else line
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = raw.split(":", 1)
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", key):
            raise ValueError(f"invalid frontmatter key: {key!r}")
        target = metadata if nested else data
        if key in target:
            raise ValueError(f"duplicate frontmatter key: {key!r}")
        value = value.strip()
        if not nested:
            metadata = None
        if not nested and key == "metadata":
            if value and not value.startswith("#"):
                raise ValueError("metadata must be an indented mapping of strings")
            metadata = {}
            data[key] = metadata
        else:
            try:
                target[key] = parse_string(value)
            except ValueError as exc:
                raise ValueError(f"{key}: {exc}") from exc
    if "metadata" in data and not data["metadata"]:
        raise ValueError("metadata must contain at least one string entry, or be omitted")
    return data, text[end + 5 :]


def validate_resources(path: Path, body: str) -> list[str]:
    """Check shipped Markdown and concrete local links, not illustrative workspace paths."""
    errors: list[str] = []
    documents = [(path, body)]
    for folder in ("references", "assets"):
        documents.extend((p, p.read_text(encoding="utf-8")) for p in sorted((path.parent / folder).rglob("*.md")))
    for document, content in documents:
        if HOST_WORDS.search(content):
            errors.append(f"{document}: skill content mentions a host product or host-only tool")
        # Backticks identify concrete bundled resources; workspace examples are not links.
        targets = re.findall(r"`([^`\n]+)`", content)
        targets = [t for t in targets if re.match(r"(?:\.\./)*(?:references|assets|scripts)/", t)
                   or re.match(r"(?:\.\./)+[a-z][a-z0-9-]*/(?:references|assets)/", t)]
        # Markdown links in shipped resources are checked even when just 'details.md'.
        targets.extend(re.findall(r"\[[^]\n]*\]\(([^)\s]+)\)", content))
        for target in targets:
            target = target.split("#", 1)[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("/"):
                continue
            if any(char in target for char in "<>*|"):
                continue  # Explicit placeholders/patterns are not concrete resource names.
            if not (document.parent / target).is_file():
                errors.append(f"{document}: missing referenced file {target!r}")
    return errors


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

    for field in ("license", "compatibility"):
        if field in data and not isinstance(data[field], str):
            errors.append(f"{path}: {field} must be a string")

    errors.extend(validate_resources(path, body))

    lines = len(text.splitlines())
    if lines >= 500:
        errors.append(f"{path}: SKILL.md is {lines} lines (keep under 500)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.pack.resolve() / "skills"
    if not root.is_dir():
        print(f"no skills directory at {root}", file=sys.stderr)
        return 1
    errors: list[str] = []
    folders = sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    for folder in folders:
        if not (folder / "SKILL.md").is_file():
            errors.append(f"missing {folder / 'SKILL.md'}")
    skills = [p for p in folders if (p / "SKILL.md").is_file()]
    if not skills:
        print("\n".join(errors + [f"no SKILL.md files under {root}"]), file=sys.stderr)
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
    elif template.read_bytes() != vendored.read_bytes():
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

    if not readme.is_file():
        errors.append(f"missing {readme}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"ok: {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
