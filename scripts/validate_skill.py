#!/usr/bin/env python3
"""
Validate a skill without requiring PyYAML.

This parser intentionally supports only the simple frontmatter subset used by
this repository: top-level `key: value` string entries inside the opening YAML
frontmatter block.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}


def _parse_simple_frontmatter(frontmatter_text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    lines = frontmatter_text.splitlines()
    index = 0

    while index < len(lines):
      raw_line = lines[index]
      index += 1

      if not raw_line.strip() or raw_line.lstrip().startswith("#"):
          continue

      if raw_line.startswith((" ", "\t")):
          raise ValueError("Indented YAML structures are not supported by the local validator")

      if ":" not in raw_line:
          raise ValueError(f"Invalid frontmatter line: {raw_line}")

      key, value = raw_line.split(":", 1)
      key = key.strip()
      value = value.strip()

      if not key:
          raise ValueError(f"Invalid frontmatter key in line: {raw_line}")

      if value == "":
          nested: dict[str, str] = {}
          while index < len(lines):
              child_line = lines[index]
              if not child_line.strip():
                  index += 1
                  continue
              if not child_line.startswith((" ", "\t")):
                  break
              if child_line.startswith("\t"):
                  raise ValueError("Tab-indented YAML structures are not supported by the local validator")
              stripped = child_line.strip()
              if ":" not in stripped:
                  raise ValueError(f"Invalid nested frontmatter line: {child_line}")
              child_key, child_value = stripped.split(":", 1)
              nested[child_key.strip()] = _strip_wrapping_quotes(child_value.strip())
              index += 1
          data[key] = nested
          continue

      data[key] = _strip_wrapping_quotes(value)

    return data


def _strip_wrapping_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def validate_skill(skill_path: str) -> tuple[bool, str]:
    skill_dir = Path(skill_path)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = _parse_simple_frontmatter(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except ValueError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_PROPERTIES))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_skill.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
