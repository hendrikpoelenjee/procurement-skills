# Improve skills from feedback (Phase 3)

Use this prompt in **Claude Code**, **Codex**, or any agent after you have accumulated structured feedback for a sourcing project.

## Preconditions

- You have read `@standards/feedback-standard.md`.
- Feedback lives in JSON arrays (`feedback.json`) as defined by `@tools/feedback/feedback.schema.json`.
- You have (or can generate) an aggregate view, e.g. output of:

  ```bash
  python3 tools/feedback/summarize_feedback.py --project /path/to/[project-id]
  ```

## Your task

Improve **this repository’s** `skills/p9t-*` packages (and, only when justified, shared `standards/` or `tools/validators/`) using **evidence from feedback records** — not general opinions.

## Required reading order

1. `standards/feedback-standard.md` — trust, redaction, retention.
2. Aggregate summary (Markdown from `summarize_feedback.py` or equivalent).
3. Raw `feedback.json` entries that the summary flags as high-signal (same `failure_modes_observed`, `data_gaps`, or `validation_result.status` issues recurring).
4. The **target skill’s** `SKILL.md`, `CHANGELOG.md`, and any schema under `assets/` touched by the improvement.

## Analysis steps

1. **Enumerate** feedback records; group by `skill_name`.
2. **Cluster** issues:
   - identical or near-identical `failure_modes_observed`
   - repeated `validation_result.status` ∈ {`fail`, `partial`}
   - repeated `confidence_level` ∈ {`LOW`, `INSUFFICIENT_DATA`} *with* substantive `data_gaps` or `risk_flags`
   - repeated `suggested_improvements` strings
3. **Prioritise** (do **not** refactor for a single anecdote unless it is safety-critical):
   1. Repeated validation failures tied to the same skill or schema mismatch
   2. Repeated user confusion (reviewer notes / failure modes)
   3. Recurring hidden assumptions not surfaced in SKILL output contract
   4. Recurring low confidence tied to the same missing inputs
   5. Repeated missing or weak `data_gaps` / escalation behaviour
4. For each cluster, state **minimum viable change** — prefer a small `SKILL.md` clarification, one new checkpoint, or a schema note over a rewrite.

## Patch rules (non-negotiable)

- **Minimal diffs** — change only what the clustered evidence supports.
- **No speculative rewrites** — if the feedback is thin, document the gap and stop.
- **Preserve skill purpose** — do not merge behaviours from other skills unless the feedback standard explicitly allows it.
- **Validators and standards** — touch `tools/validators/` or `standards/` only when **multiple independent records** show the same structural or cross-skill failure mode; cite the record group in the commit message / CHANGELOG.
- **Versioning** — every skill change gets a `CHANGELOG.md` entry (semver rules per skill).
- **Epistemic discipline** — improvements must not instruct the model to fake `HIGH` confidence or hide `data_gaps`.

## Outputs

1. **Triage table** — skill → cluster → count of records → proposed action (patch / defer / needs human policy).
2. **Concrete patches** — file-scoped edits (`SKILL.md`, `assets/output.schema.json`, `sample-output.json`, eval `cases.json` if needed).
3. **Validation plan** — run `python3 distr/validate.py --skill-dir skills/<name>` (and quick_validate if frontmatter changes).
4. **Residual risk** — what still needs human review before treating the skill as improved.

## Stop conditions

- Evidence for a proposed change is **single-instance** and non-critical → **defer**; optionally add a TODO in `CHANGELOG.md` under “Known follow-ups”.
- Feedback contains **sensitive or identifying** content → **do not paste raw feedback** into commits; summarise in neutral terms per `standards/feedback-standard.md`.

## Guiding principle

Make improvement **visible, reviewable, and reversible**. Prefer feedback-driven patches over stylistic clean-up.
