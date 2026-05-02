#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import sys
from pathlib import Path

# ----------------------------
# Configuration
# ----------------------------

REQUIRED_SKILL_SECTIONS = [
    "Assumptions & Boundaries",
    "Known Failure Modes",
    "Escalation Triggers",
    "Confidence Definition",
    "Human-in-the-Loop Protocol",
]

REQUIRED_SCHEMA_FIELDS = [
    "confidence_level",
    "assumptions",
    "data_gaps",
    "risk_flags",
]

EVAL_CASE_TYPES = frozenset(
    ["happy_path", "thin_data", "contradictory_inputs", "high_risk"]
)

# ----------------------------
# Utilities
# ----------------------------

def fail(msg):
    print(f"[FAIL] {msg}")
    return False

def ok(msg):
    print(f"[OK] {msg}")
    return True

def warn(msg):
    print(f"[WARN] {msg}")

# ----------------------------
# Checks
# ----------------------------

def check_structure(skill_dir: Path):
    success = True

    skill_md = skill_dir / "SKILL.md"
    assets = skill_dir / "assets"
    schema = assets / "output.schema.json"
    sample = assets / "sample-output.json"

    if not skill_md.exists():
        success &= fail("Missing SKILL.md")
    else:
        ok("SKILL.md found")

    if not schema.exists():
        success &= fail("Missing output.schema.json")
    else:
        ok("output.schema.json found")

    if not sample.exists():
        success &= warn("Missing sample-output.json")
    else:
        ok("sample-output.json found")

    return success


def check_skill_sections(skill_md: Path):
    success = True
    content = skill_md.read_text(encoding="utf-8")

    for section in REQUIRED_SKILL_SECTIONS:
        if section not in content:
            success &= fail(f"Missing section: '{section}'")
        else:
            ok(f"Section present: {section}")

    return success


def check_schema_fields(schema_path: Path):
    success = True

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"Invalid JSON in schema: {e}")

    properties = schema.get("properties", {})

    for field in REQUIRED_SCHEMA_FIELDS:
        if field not in properties:
            success &= fail(f"Schema missing field: '{field}'")
        else:
            ok(f"Schema field present: {field}")

    return success


def check_sample_against_schema(schema_path: Path, sample_path: Path):
    try:
        import jsonschema
    except ImportError:
        warn("jsonschema not installed, skipping sample validation")
        return True

    try:
        schema = json.loads(schema_path.read_text())
        sample = json.loads(sample_path.read_text())
    except Exception as e:
        return fail(f"Error reading schema/sample: {e}")

    try:
        jsonschema.validate(instance=sample, schema=schema)
        ok("Sample output validates against schema")
        return True
    except Exception as e:
        return fail(f"Sample does NOT validate against schema: {e}")


def check_eval_cases(skill_dir: Path) -> bool:
    """
    Ensure evals/p9t-<name>/cases.json exists, parses, matches eval_cases.schema.json,
    declares the canonical four case types, and matches the skill folder name.

    Pack root is the parent of the directory named ``skills`` (mirrors repo and
    post-install layouts: ~/.claude/skills/... + ~/.claude/evals/, same for ~/.agents/).
    """
    sd = skill_dir.resolve()
    if sd.parent.name != "skills":
        return fail(
            "Skill dir must live at .../<pack>/skills/<skill-name>/ so eval and "
            "validator paths resolve; parent folder must be named 'skills' "
            f"(got '{sd.parent.name}' for {sd})"
        )
    pack_root = sd.parent.parent
    eval_cases = pack_root / "evals" / skill_dir.name / "cases.json"
    schema_eval = pack_root / "tools" / "validators" / "eval_cases.schema.json"

    install_hint = (
        " Re-run bash install.sh (Claude Code) or bash install-codex.sh (Codex) from "
        "the repository clone — they deploy tools/validators/ and evals/ next to your "
        "installed skills."
    )

    if not schema_eval.exists():
        return fail(f"Missing eval JSON Schema: {schema_eval}.{install_hint}")

    if not eval_cases.exists():
        return fail(f"Missing eval cases file: {eval_cases}.{install_hint}")

    try:
        data = json.loads(eval_cases.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"Invalid JSON in eval cases: {e}")

    try:
        import jsonschema

        js = json.loads(schema_eval.read_text(encoding="utf-8"))
        jsonschema.validate(instance=data, schema=js)
        ok(f"Eval cases validate against schema: {eval_cases.name}")
    except ImportError:
        warn("jsonschema not installed, skipping eval case schema validation")
    except Exception as e:
        return fail(f"Eval cases do NOT validate against schema: {e}")

    if data.get("skill") != skill_dir.name:
        return fail(
            f"Eval skill field '{data.get('skill')}' != directory name '{skill_dir.name}'"
        )

    found = {c.get("type") for c in data.get("cases", [])}
    missing = EVAL_CASE_TYPES - found
    if missing:
        return fail(f"Eval cases missing mandatory types: {sorted(missing)}")

    ok("Eval cases cover all four mandatory types")
    return True


def check_epistemic_signals(skill_md: Path):
    """
    Lightweight heuristic checks for epistemic awareness.
    """
    content = skill_md.read_text(encoding="utf-8").lower()
    success = True

    if "assumption" not in content:
        success &= warn("No explicit mention of assumptions")

    if "confidence" not in content:
        success &= warn("No confidence definition found")

    if "risk" not in content:
        success &= warn("No explicit risk handling found")

    return success


# ----------------------------
# Main
# ----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", required=True)

    args = parser.parse_args()
    skill_dir = Path(args.skill_dir)

    if not skill_dir.exists():
        print(f"[ERROR] Skill directory not found: {skill_dir}")
        return 1

    print(f"\nValidating skill: {skill_dir.name}")
    print("-" * 50)

    success = True

    success &= check_structure(skill_dir)

    skill_md = skill_dir / "SKILL.md"
    schema = skill_dir / "assets" / "output.schema.json"
    sample = skill_dir / "assets" / "sample-output.json"

    if skill_md.exists():
        success &= check_skill_sections(skill_md)
        success &= check_epistemic_signals(skill_md)

    if schema.exists():
        success &= check_schema_fields(schema)

    if schema.exists() and sample.exists():
        success &= check_sample_against_schema(schema, sample)

    success &= check_eval_cases(skill_dir)

    print("-" * 50)

    if success:
        print("[RESULT] PASS")
        return 0
    else:
        print("[RESULT] FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())