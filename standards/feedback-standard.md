<!-- SPDX-License-Identifier: Apache-2.0 -->

# Feedback capture standard (Phase 3)

Defines how sourcing skill runs capture **structured, traceable feedback** so improvements stay evidence-based, prioritised, and reviewable — not ad hoc chat notes.

Apply together with `@standards/artifact-placement.md` and `@standards/input-trust.md`.

---

## Purpose

1. Make failures, confusion, and thin outputs **visible in the project artefact tree**.
2. Enable **aggregation** (`summarize_feedback.py`) across runs.
3. Enable **minimal, audited skill changes** via `tools/prompts/improve_from_feedback.md`.

Phase 3 does **not** auto-merge skill changes; humans still own PR review and validators.

---

## Where feedback lives

Default (project-wide rollup):

```text
[project_root]/[project-id]/workflow/feedback.json
```

Optional (stage-local detail:

```text
[project_root]/[project-id]/[stage-folder]/feedback.json
```

Examples of `[stage-folder]`: `S1-intake/`, `S5-rfq/`, … per `artifact-placement.md`.

**Rule:** Prefer **one canonical** `workflow/feedback.json` per project for cross-skill summaries; use stage-level files only when feedback is inherently stage-specific.

---

## File format

- **JSON root:** an **array** of feedback **records** (append-only semantics).
- **Encoding:** UTF-8.
- Each record MUST validate against `@tools/feedback/feedback.schema.json`.
- **`run_id`:** unique per invocation (UUID v4 recommended). Never reuse for a distinct run.

---

## Machine schema (canonical fields)

Each record MUST include (see schema for typing and enums):

| Field | Required | Notes |
|-------|----------|--------|
| `skill_name` | yes | Matches skill folder (`p9t-*`). |
| `project_id` | yes | Canonical project slug / id. |
| `run_id` | yes | Correlates artefacts and validator output. |
| `timestamp` | yes | RFC 3339 / ISO 8601 UTC recommended. |
| `artifact_paths` | yes | Array; may be empty if nothing was written yet. Paths relative to project root preferred. |
| `user_rating` | no | 1–5; optional ordinal quality signal. |
| `reviewer_notes` | no | Free text — still subject to sensitivities below. |
| `validation_result` | yes | Structured pass/fail/skip indicator (see schema). |
| `confidence_level` | yes | `HIGH` \| `MEDIUM` \| `LOW` \| `INSUFFICIENT_DATA` (skill vocabulary). |
| `assumptions` | yes | Array (may be empty). |
| `data_gaps` | yes | Array (may be empty). |
| `risk_flags` | yes | Array (may be empty). |
| `failure_modes_observed` | yes | Array of short identifiers or sentences. |
| `suggested_improvements` | yes | Array — concrete, minimal suggestions when possible. |

Optional extension fields MAY be added later if they remain JSON-Schema-compliant and documented here.

---

## Trust, privacy, procurement sensitivity

Assume feedback can be archived and shared internally.

Do **NOT** embed in feedback records unless explicitly aligned with disclosure policy:

- Raw supplier identities, quotes, discounts, totals, contractual terms  
- Credential material, unreleased bids, competitively sensitive payloads  
- Personally identifiable information (PII)

Use **neutral handles** (“Supplier A”, “incumbent”, “candidate 3”), **category labels**, **redacted excerpts**, or **references to internal-only paths** that are themselves access-controlled.

If redaction occurs, mention that in `reviewer_notes` or `risk_flags`.

---

## When to capture feedback

Minimum triggers (non-exhaustive):

- **`blocked` / INSUFFICIENT_DATA` outcomes users found surprising**
- Repeated **missing inputs** surfaced as `data_gaps`
- **validator failures** (`distr/validate.py`, runtime checks)
- **Human review friction** (“could not approve gate G3”)

Do **not** open a Phase 3 improvement ticket from a single weak anecdote unless the issue is critical (legal, safety-of-decision).

---

## Tooling contract

| Script | Role |
|--------|------|
| `tools/feedback/collect_feedback.py` | Validate + append records (atomic write). |
| `tools/feedback/summarize_feedback.py` | Aggregate signals for prioritisation. |

---

## Relation to validators

- Structural / epistemic **skill quality** gates remain **`tools/validators/validate_skill.py`** and human review prompts.
- Feedback records may **cite** validator output but MUST NOT substitute for re-running validators after edits.

---

## Versioning

This standard should gain a changelog entry when materially changed (`CHANGELOG.md` at repo discretion). Skills need not duplicate this standard in `SKILL.md`.
