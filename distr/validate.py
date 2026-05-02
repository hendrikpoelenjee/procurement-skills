#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Entry point for validating any p9t-* skill.

Usage:
    python3 distr/validate.py --skill-dir skills/p9t-market-scan
    python3 distr/validate.py --all

Delegates to: tools/validators/validate_skill.py
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validators" / "validate_skill.py"


def run_skill(skill_dir: Path) -> int:
    return subprocess.call([
        sys.executable,
        str(VALIDATOR),
        "--skill-dir",
        str(skill_dir.resolve()),
    ])


def main():
    parser = argparse.ArgumentParser(
        description="Validate one or all p9t-* skills against the central validator."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--skill-dir",
        help="Path to a single skill directory, e.g. skills/p9t-market-scan",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Validate all skills found under skills/p9t-*/",
    )
    args = parser.parse_args()

    if args.skill_dir:
        raise SystemExit(run_skill(Path(args.skill_dir)))

    # --all: run every skill, report summary
    skills_root = ROOT / "skills"
    skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir() and p.name.startswith("p9t-"))

    if not skill_dirs:
        print("[ERROR] No p9t-* skill directories found.")
        raise SystemExit(1)

    results = {}
    for skill_dir in skill_dirs:
        rc = run_skill(skill_dir)
        results[skill_dir.name] = "PASS" if rc == 0 else "FAIL"

    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    for name, result in results.items():
        print(f"  {'✓' if result == 'PASS' else '✗'} {name}: {result}")

    total = len(results)
    passed = sum(1 for r in results.values() if r == "PASS")
    print(f"\n{passed}/{total} skills passed.")
    print("=" * 50)

    raise SystemExit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
