#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parents[1]

cmd = [
    sys.executable,
    str(ROOT / "tools" / "validators" / "validate_skill.py"),
    "--skill-dir",
    str(SKILL_DIR),
]

raise SystemExit(subprocess.call(cmd))
