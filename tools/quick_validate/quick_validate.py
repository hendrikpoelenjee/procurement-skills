#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Quick frontmatter validation for p9t-* skills (minimal, Anthropic-inspired).

Inspired by upstream quick_validate patterns:
  https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/quick_validate.py

This script validates SKILL.md YAML frontmatter + pack conventions against
quick_validate.rules.yaml (mirrors standards/skill-frontmatter.md).

Does NOT replace tools/validators/validate_skill.py (schemas, samples, evals).

Usage:
  python3 tools/quick_validate/quick_validate.py
  python3 tools/quick_validate/quick_validate.py skills/p9t-market-scan
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "[ERROR] PyYAML is required: pip install pyyaml\n"
        "(Same dependency pattern as Anthropics skill-creator quick_validate.)",
        file=sys.stderr,
    )
    raise SystemExit(2)


def load_rules(script_dir: Path) -> dict[str, Any]:
    path = script_dir / "quick_validate.rules.yaml"
    if not path.exists():
        print(f"[ERROR] Rules file not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        print("[ERROR] quick_validate.rules.yaml must be a mapping", file=sys.stderr)
        raise SystemExit(2)
    return data


def extract_frontmatter(content: str) -> tuple[bool, str, dict[str, Any] | None]:
    if not content.startswith("---"):
        return False, "No YAML frontmatter found (must start with ---)", None
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format (expected closing --- before body)", None
    text = match.group(1)
    try:
        fm = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}", None
    if not isinstance(fm, dict):
        return False, "Frontmatter must be a YAML mapping (dictionary)", None
    return True, "", fm


def validate_skill(skill_dir: Path, rules: dict[str, Any]) -> tuple[bool, str]:
    skill_dir = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    folder_name = skill_dir.name
    pat = re.compile(rules.get("skill_folder_pattern", "^p9t-[a-z0-9-]+$"))
    if not pat.match(folder_name):
        return False, f"Folder name '{folder_name}' does not match pattern {pat.pattern!r}"

    content = skill_md.read_text(encoding="utf-8")
    ok, err, fm = extract_frontmatter(content)
    if not ok or fm is None:
        return False, err

    required_top = list(rules.get("required_top_level", []))
    allowed_extra = set(rules.get("allowed_top_level_extra", []))
    for key in required_top:
        if key not in fm:
            return False, f"Missing required top-level key: {key!r}"

    unexpected = set(fm.keys()) - set(required_top) - allowed_extra
    if unexpected:
        return False, (
            f"Unexpected top-level key(s): {', '.join(sorted(unexpected))}. "
            f"Add to quick_validate.rules.yaml allowed_top_level_extra if intentional."
        )

    name = fm.get("name", "")
    if not isinstance(name, str) or not name.strip():
        return False, "name must be a non-empty string"
    name = name.strip()
    if len(name) > int(rules.get("name_max_chars", 64)):
        return False, f"name too long ({len(name)} chars; max {rules['name_max_chars']})"
    if not pat.match(name):
        return False, f"name {name!r} must match folder pattern {pat.pattern!r}"
    if rules.get("name_must_match_folder", True) and name != folder_name:
        return False, f"name {name!r} must match folder name {folder_name!r}"

    desc = fm.get("description", "")
    if not isinstance(desc, str) or not desc.strip():
        return False, "description must be a non-empty string"
    desc = desc.strip()
    dmax = int(rules.get("description_max_chars", 1024))
    if len(desc) > dmax:
        return False, f"description too long ({len(desc)} chars; max {dmax})"
    if rules.get("description_forbid_angle_brackets", True) and ("<" in desc or ">" in desc):
        return False, "description cannot contain angle brackets (< or >)"

    lic = fm.get("license")
    allowed_lic = rules.get("allowed_licenses") or []
    if allowed_lic and lic not in allowed_lic:
        return False, f"license must be one of {allowed_lic} (got {lic!r})"

    spdx = fm.get("spdx-license-identifier")
    if allowed_lic and spdx not in allowed_lic:
        return False, f"spdx-license-identifier must match allowed license (got {spdx!r})"

    compat = fm.get("compatibility", "")
    if not isinstance(compat, str):
        return False, "compatibility must be a string"
    cmax = int(rules.get("compatibility_max_chars", 500))
    if len(compat) > cmax:
        return False, f"compatibility too long ({len(compat)} chars; max {cmax})"

    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        return False, "metadata must be a YAML mapping"

    for mk in rules.get("required_metadata", []):
        if mk not in meta:
            return False, f"Missing metadata.{mk}"

    status = meta.get("status")
    status_enum = rules.get("status_enum", [])
    if status_enum and status not in status_enum:
        return False, f"metadata.status must be one of {status_enum} (got {status!r})"

    wave = meta.get("wave")
    if not isinstance(wave, int) or isinstance(wave, bool):
        return False, "metadata.wave must be an integer"

    tags = meta.get("tags")
    if not isinstance(tags, list) or not tags:
        return False, "metadata.tags must be a non-empty array"
    for t in tags:
        if not isinstance(t, str):
            return False, "each metadata.tags entry must be a string"
        if t != t.lower():
            return False, f"metadata.tags entries must be lowercase (got {t!r})"
    for need in rules.get("minimum_tags_must_include", []):
        if need not in tags:
            return False, f"metadata.tags must include {need!r}"

    osch = meta.get("output_schema")
    exp = rules.get("expected_output_schema")
    if exp and osch != exp:
        return False, f"metadata.output_schema must be {exp!r} (got {osch!r})"

    arts = meta.get("primary_artifacts")
    if not isinstance(arts, list) or not arts:
        return False, "metadata.primary_artifacts must be a non-empty array"
    for a in arts:
        if not isinstance(a, str) or not a.strip():
            return False, "each primary_artifacts entry must be a non-empty string"

    for bool_key in ("review_required", "human_approval_required", "external_input"):
        if not isinstance(meta.get(bool_key), bool):
            return False, f"metadata.{bool_key} must be a boolean"

    cm = meta.get("context_budget")
    if not isinstance(cm, dict):
        return False, "metadata.context_budget must be a mapping"
    for ck in rules.get("required_context_budget_keys", []):
        if ck not in cm:
            return False, f"Missing metadata.context_budget.{ck}"

    ver = meta.get("version")
    if not isinstance(ver, str) and not isinstance(ver, float) and not isinstance(ver, int):
        return False, "metadata.version must be numeric or semver string"
    if isinstance(ver, float):
        ver = str(ver)
    elif isinstance(ver, int):
        ver = str(ver)

    return True, "SKILL.md frontmatter OK"


def discover_skill_dirs(repo_root: Path, rules: dict[str, Any]) -> list[Path]:
    rel = rules.get("skills_root_relative", "skills")
    root = (repo_root / rel).resolve()
    if not root.is_dir():
        print(f"[ERROR] Skills root not found: {root}", file=sys.stderr)
        raise SystemExit(2)
    pat = re.compile(rules.get("skill_folder_pattern", "^p9t-[a-z0-9-]+$"))
    dirs = sorted(p for p in root.iterdir() if p.is_dir() and pat.match(p.name))
    return dirs


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    rules = load_rules(script_dir)

    parser = argparse.ArgumentParser(
        description="Quick YAML frontmatter check for p9t procurement skills.",
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        help="Path to one skill folder (default: all under skills/).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root containing skills/ (default: inferred from script location).",
    )
    args = parser.parse_args()
    if args.repo_root is not None:
        global_repo = args.repo_root.resolve()
    else:
        global_repo = repo_root

    if args.skill_dir:
        targets = [Path(args.skill_dir).resolve()]
        for t in targets:
            if not t.is_dir():
                print(f"[ERROR] Not a directory: {t}", file=sys.stderr)
                raise SystemExit(2)
    else:
        targets = discover_skill_dirs(global_repo, rules)

    failures = 0
    for skill_path in targets:
        valid, message = validate_skill(skill_path, rules)
        prefix = "[OK]" if valid else "[FAIL]"
        print(f"{prefix} {skill_path.name}: {message}")
        if not valid:
            failures += 1

    if failures:
        print(f"\n{failures}/{len(targets)} skill(s) failed quick_validate.", file=sys.stderr)
        raise SystemExit(1)
    print(f"\nAll {len(targets)} skill(s) passed quick_validate.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
