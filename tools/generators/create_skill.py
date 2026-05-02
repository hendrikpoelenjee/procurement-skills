#!/usr/bin/env python3
import os
import sys
from pathlib import Path

TEMPLATE = """# SKILL.md — {skill_name}

## ✦ Purpose
[Describe what this skill does]

---

## ✦ Assumptions & Boundaries
- ...
- ...

---

## ✦ Execution Logic
1. ...
2. ...
3. ...

---

## ✦ Known Failure Modes
- ...
- ...

---

## ✦ Escalation Triggers
- ...
- ...

---

## ✦ Human-in-the-Loop Protocol
- Ask:
  - ...
  - ...

---

## ✦ Output Requirements
- ...

---

## ✦ Confidence Definition
- HIGH:
- MEDIUM:
- LOW:

---

## ✦ Validation
- Must include assumptions
- Must include risk flags
- Must include confidence_level
"""

def create_skill(skill_name):
    root = Path("skills") / skill_name

    folders = [
        root,
        root / "assets",
        root / "providers",
        root / "references",
        root / "scripts"
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    (root / "SKILL.md").write_text(TEMPLATE.format(skill_name=skill_name))

    (root / "assets" / "output.schema.json").write_text("""{
  "confidence_level": "",
  "assumptions": [],
  "data_gaps": [],
  "risk_flags": []
}""")

    (root / "assets" / "sample-output.json").write_text("""{}""")

    (root / "scripts" / "validate.py").write_text("""#!/usr/bin/env python3
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
""")

    print(f"Skill '{skill_name}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: create_skill.py <skill-name>")
        sys.exit(1)

    create_skill(sys.argv[1])