#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Append feedback record(s) to project feedback JSON (Phase 3).

Validates each record against feedback.schema.json next to this script.
Input may be a single JSON object or a JSON array of objects.
Default target: <project>/workflow/feedback.json (array of records).

Usage:
  python3 tools/feedback/collect_feedback.py \\
    --project-root ~/sourcing-projects \\
    --project-id acme-widgets-001 \\
    --record-file my-record.json

  cat record.json | python3 tools/feedback/collect_feedback.py \\
    --workflow-dir ~/sourcing-projects/acme-widgets-001/workflow
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FEEDBACK_FILENAME = "feedback.json"
SCHEMA_PATH = Path(__file__).resolve().parent / "feedback.schema.json"


def load_schema() -> dict[str, Any]:
    if not SCHEMA_PATH.exists():
        print(f"[ERROR] Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        raise SystemExit(2)
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_record(instance: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        import jsonschema
    except ImportError:
        print(
            "[WARN] jsonschema not installed — skipping schema validation. "
            "Install: pip install jsonschema",
            file=sys.stderr,
        )
        return
    jsonschema.validate(instance=instance, schema=schema)


def resolve_feedback_path(
    *,
    workflow_dir: Path | None,
    project_root: Path | None,
    project_id: str | None,
    stage_folder: str | None,
) -> Path:
    if workflow_dir is not None:
        base = workflow_dir.resolve()
        return base / FEEDBACK_FILENAME
    if project_root is None or not project_id:
        print(
            "[ERROR] Provide --workflow-dir OR both --project-root and --project-id",
            file=sys.stderr,
        )
        raise SystemExit(2)
    root = project_root.expanduser().resolve()
    proj = root / project_id
    if stage_folder:
        sub = proj / stage_folder.strip("/")
        sub.mkdir(parents=True, exist_ok=True)
        return sub / FEEDBACK_FILENAME
    wf = proj / "workflow"
    wf.mkdir(parents=True, exist_ok=True)
    return wf / FEEDBACK_FILENAME


def atomic_write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmppath = tempfile.mkstemp(
        dir=str(path.parent), prefix=".feedback.", suffix=".tmp"
    )
    tmp = Path(tmppath)
    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        tmp.replace(path)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def normalize_record(raw: dict[str, Any], auto_timestamp: bool, auto_run_id: bool) -> dict[str, Any]:
    out = dict(raw)
    if auto_run_id and not out.get("run_id"):
        out["run_id"] = str(uuid.uuid4())
    if auto_timestamp and not out.get("timestamp"):
        out["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow-dir", type=Path, help="Path to .../workflow directory")
    parser.add_argument("--project-root", type=Path, help="Sourcing projects root (see skills-config.yaml)")
    parser.add_argument("--project-id", type=str, help="Project folder name under project root")
    parser.add_argument(
        "--stage-folder",
        type=str,
        help="Optional stage subfolder under project (e.g. S2-market-scan) for stage-local feedback.json",
    )
    parser.add_argument(
        "--record-file",
        type=Path,
        help="JSON object or array of objects. If omitted, read stdin.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not write")
    parser.add_argument(
        "--no-auto-fill",
        action="store_true",
        help="Do not auto-fill run_id or timestamp when missing",
    )
    args = parser.parse_args()

    schema = load_schema()

    if args.record_file:
        payload = json.loads(args.record_file.read_text(encoding="utf-8"))
    elif not sys.stdin.isatty():
        payload = json.loads(sys.stdin.read())
    else:
        print("[ERROR] Provide --record-file or pipe JSON on stdin", file=sys.stderr)
        raise SystemExit(2)

    if isinstance(payload, dict):
        raw_records: list[dict[str, Any]] = [payload]
    elif isinstance(payload, list):
        raw_records = []
        for i, item in enumerate(payload):
            if not isinstance(item, dict):
                print(
                    f"[ERROR] Array item {i} must be a JSON object",
                    file=sys.stderr,
                )
                raise SystemExit(2)
            raw_records.append(item)
    else:
        print("[ERROR] Input must be a JSON object or array of objects", file=sys.stderr)
        raise SystemExit(2)

    records: list[dict[str, Any]] = []
    for idx, raw in enumerate(raw_records):
        rec = normalize_record(
            raw,
            auto_timestamp=not args.no_auto_fill,
            auto_run_id=not args.no_auto_fill,
        )
        try:
            validate_record(rec, schema)
        except Exception as e:
            print(f"[ERROR] Record {idx} failed schema validation: {e}", file=sys.stderr)
            raise SystemExit(1)
        records.append(rec)

    fb_path = resolve_feedback_path(
        workflow_dir=args.workflow_dir,
        project_root=args.project_root,
        project_id=args.project_id,
        stage_folder=args.stage_folder,
    )

    n = len(records)
    print(f"[OK] {n} record(s) valid. Target file: {fb_path}")

    if args.dry_run:
        raise SystemExit(0)

    existing: list[Any] = []
    if fb_path.exists():
        try:
            blob = json.loads(fb_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[ERROR] Existing file is invalid JSON: {e}", file=sys.stderr)
            raise SystemExit(1)
        if isinstance(blob, list):
            existing = blob
        else:
            print(
                "[ERROR] feedback.json root must be a JSON array; fix manually or archive file",
                file=sys.stderr,
            )
            raise SystemExit(1)

    existing.extend(records)
    atomic_write_json(fb_path, existing)
    print(f"[OK] Appended {n} record(s) (total {len(existing)}) to {fb_path}")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
