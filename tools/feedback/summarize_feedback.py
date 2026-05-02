#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Aggregate feedback records for prioritisation (Phase 3).

Reads JSON arrays from:
  - <project>/workflow/feedback.json
Optional:
  --include-stage-feedback  adds <project>/<stage-folder>/feedback.json matches

Outputs a concise Markdown summary to stdout (or --out).

Usage:
  python3 tools/feedback/summarize_feedback.py \\
    --project ~/sourcing-projects/example-category-001

  python3 tools/feedback/summarize_feedback.py \\
    --project ~/sourcing-projects/example-category-001 \\
    --include-stage-feedback \\
    --out ~/sourcing-projects/example-category-001/workflow/feedback-summary.md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

FEEDBACK_FILE = "feedback.json"


def load_array(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[WARN] Skip invalid JSON {path}: {e}", file=sys.stderr)
        return []
    if not isinstance(data, list):
        print(f"[WARN] Skip non-array JSON {path}", file=sys.stderr)
        return []
    out = []
    for item in data:
        if isinstance(item, dict):
            out.append(item)
    return out


def discover_feedback_files(project_dir: Path, include_stage: bool) -> list[Path]:
    project_dir = project_dir.expanduser().resolve()
    wf = project_dir / "workflow" / FEEDBACK_FILE
    files: list[Path] = [wf]
    wf_resolved = wf.resolve()
    seen: set[Any] = {wf_resolved}
    if include_stage:
        for p in sorted(project_dir.rglob(FEEDBACK_FILE)):
            try:
                pr = p.resolve()
            except OSError:
                continue
            if pr in seen:
                continue
            try:
                rel = p.relative_to(project_dir)
            except ValueError:
                continue
            # phase_three: `<project>/<stage-folder>/feedback.json` => two path parts
            if len(rel.parts) != 2:
                continue
            seen.add(pr)
            files.append(p)
    return files


def format_summary(project_id: str, records: list[dict[str, Any]], sources: list[Path]) -> str:
    lines: list[str] = []
    lines.append(f"# Feedback summary — `{project_id}`")
    lines.append("")
    lines.append(f"- **records:** {len(records)}")
    lines.append(f"- **sources scanned:** {len(sources)}")
    lines.append("")

    if not records:
        lines.append("No feedback records found.")
        lines.append("")
        return "\n".join(lines)

    by_skill: Counter[str] = Counter()
    val_status: Counter[str] = Counter()
    conf: Counter[str] = Counter()
    failures: Counter[str] = Counter()
    risks: Counter[str] = Counter()
    gaps: Counter[str] = Counter()
    suggestions: Counter[str] = Counter()

    for r in records:
        skill = str(r.get("skill_name") or "?")
        by_skill[skill] += 1
        vr = r.get("validation_result") or {}
        if isinstance(vr, dict):
            val_status[str(vr.get("status") or "?")] += 1
        conf[str(r.get("confidence_level") or "?")] += 1
        for fm in r.get("failure_modes_observed") or []:
            if isinstance(fm, str):
                failures[fm] += 1
        for x in r.get("risk_flags") or []:
            if isinstance(x, str):
                risks[x] += 1
        for x in r.get("data_gaps") or []:
            if isinstance(x, str):
                gaps[x] += 1
        for x in r.get("suggested_improvements") or []:
            if isinstance(x, str):
                suggestions[x] += 1

    lines.append("## Signals by skill")
    for sk, ct in by_skill.most_common():
        lines.append(f"- **{sk}:** {ct}")
    lines.append("")

    lines.append("## Validation outcomes")
    for st, ct in val_status.most_common():
        lines.append(f"- **{st}:** {ct}")
    lines.append("")

    lines.append("## Confidence levels")
    for st, ct in conf.most_common():
        lines.append(f"- **{st}:** {ct}")
    lines.append("")

    def top_heading(title: str, ctr: Counter, n: int = 15) -> None:
        lines.append(f"## {title} (top {n})")
        if not ctr:
            lines.append("(none)")
            lines.append("")
            return
        for txt, ct in ctr.most_common(n):
            lines.append(f"- ({ct}×) {txt}")
        lines.append("")

    top_heading("Recurring failure modes", failures)
    top_heading("Recurring risk_flags", risks)
    top_heading("Recurring data_gaps", gaps)
    top_heading("Suggested improvements", suggestions)

    lines.append("## Prioritisation hint (automated heuristic)")
    lines.append("")
    lines.append("| Priority cue | Threshold | Meaning |")
    lines.append("|-------------|------------|---------|")
    lines.append("| skill volume | ≥3 records / skill | Repeated exposure |")
    lines.append("| string recurrence | ≥2 identical strings | Pattern worth triaging |")
    lines.append("| validation_result | fail / partial | Fix or clarify skill |")
    lines.append("")
    lines.append("*Human reviewer applies final ordering per `standards/feedback-standard.md` and Phase 3 rules.*")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        type=Path,
        required=True,
        help="Path to [project_root]/[project-id] directory",
    )
    parser.add_argument(
        "--include-stage-feedback",
        action="store_true",
        help="Also aggregate stage-level .../<Stage>/feedback.json files",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Write Markdown summary to this path instead of stdout",
    )
    args = parser.parse_args()

    proj = args.project.expanduser().resolve()
    if not proj.is_dir():
        print(f"[ERROR] Not a directory: {proj}", file=sys.stderr)
        raise SystemExit(2)

    sources = discover_feedback_files(proj, args.include_stage_feedback)
    rows: list[dict[str, Any]] = []
    paths_used: list[Path] = []

    for path in sorted(set(sources), key=lambda q: str(q)):
        blob = load_array(path)
        paths_used.append(path)
        rows.extend(blob)

    md = format_summary(proj.name, rows, paths_used)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"[OK] Wrote {args.out}")
    else:
        print(md)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
