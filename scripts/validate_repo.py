#!/usr/bin/env python3
"""Validate this repository without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "write-video-scripts"
SKILL_MD = SKILL / "SKILL.md"


class ValidationError(Exception):
    """Collect a user-facing validation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    require(bool(lines) and lines[0] == "---", "SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError("SKILL.md frontmatter is not closed") from exc

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        require(bool(line.strip()), "SKILL.md frontmatter must not contain blank lines")
        match = re.fullmatch(r"([a-z][a-z0-9-]*):\s+(.+)", line)
        require(match is not None, f"Unsupported frontmatter line: {line!r}")
        key, value = match.groups()
        require(key not in fields, f"Duplicate frontmatter field: {key}")
        fields[key] = value.strip().strip('"\'')
    return fields


def validate_skill() -> None:
    text = SKILL_MD.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    require(set(fields) == {"name", "description"}, "Use only name and description in frontmatter")

    name = fields["name"]
    description = fields["description"]
    require(1 <= len(name) <= 64, "Skill name must be 1–64 characters")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None, "Invalid skill name")
    require(name == SKILL.name, "Skill name must match its parent directory")
    require(1 <= len(description) <= 1024, "Description must be 1–1024 characters")
    require("Use when" in description, "Description must explain when the skill triggers")
    require(len(text.splitlines()) < 500, "SKILL.md must stay under 500 lines")

    for relative in (
        "references/format-playbook.md",
        "references/output-contracts.md",
        "references/quality-rubric.md",
        "references/factual-safety.md",
        "agents/openai.yaml",
    ):
        require((SKILL / relative).is_file(), f"Missing skill resource: {relative}")

    agent_yaml = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    require('$write-video-scripts' in agent_yaml, "Default prompt must explicitly invoke the skill")
    short_match = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', agent_yaml, re.MULTILINE)
    require(short_match is not None, "agents/openai.yaml needs a quoted short_description")
    require(25 <= len(short_match.group(1)) <= 64, "short_description must be 25–64 characters")


def validate_relative_links() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            resolved = (path.parent / target).resolve()
            require(resolved.exists(), f"Broken relative link in {path.relative_to(ROOT)}: {raw_target}")


def validate_evals() -> None:
    cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
    require(isinstance(cases, list) and len(cases) >= 5, "Provide at least five evaluation cases")
    identifiers: set[str] = set()
    for case in cases:
        require(isinstance(case, dict), "Each evaluation case must be an object")
        require(set(case) == {"id", "language", "prompt", "expectations"}, "Unexpected eval fields")
        identifier = case["id"]
        require(isinstance(identifier, str) and identifier, "Each eval needs an id")
        require(identifier not in identifiers, f"Duplicate eval id: {identifier}")
        identifiers.add(identifier)
        require(isinstance(case["language"], str) and case["language"], f"{identifier}: missing language")
        require(isinstance(case["prompt"], str) and len(case["prompt"]) >= 10, f"{identifier}: prompt too short")
        expectations = case["expectations"]
        require(isinstance(expectations, list) and len(expectations) >= 3, f"{identifier}: add expectations")
        require(all(isinstance(item, str) and item for item in expectations), f"{identifier}: invalid expectation")


def validate_repository() -> None:
    required = (
        "README.md",
        "README.zh-CN.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        ".github/workflows/validate.yml",
    )
    for relative in required:
        require((ROOT / relative).is_file(), f"Missing repository file: {relative}")

    for path in SKILL.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json"}:
            content = path.read_text(encoding="utf-8")
            require("TODO" not in content and "TBD" not in content, f"Unresolved marker in {path.relative_to(ROOT)}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    require("Apache License" in license_text and "Version 2.0, January 2004" in license_text, "LICENSE is not Apache-2.0")


def main() -> int:
    checks = (
        ("repository baseline", validate_repository),
        ("Agent Skill structure", validate_skill),
        ("relative Markdown links", validate_relative_links),
        ("evaluation corpus", validate_evals),
    )
    failures: list[str] = []
    for label, check in checks:
        try:
            check()
            print(f"PASS  {label}")
        except (ValidationError, OSError, json.JSONDecodeError) as exc:
            failures.append(f"FAIL  {label}: {exc}")
            print(failures[-1])

    if failures:
        print(f"\n{len(failures)} validation group(s) failed.")
        return 1
    print("\nRepository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
