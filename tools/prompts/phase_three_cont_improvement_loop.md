You are operating inside a procurement skills repository.

Phase 1 upgraded the skills.
Phase 2 stress-tested the skills.

Your task is now to design and implement **Phase 3: Continuous Improvement Loop**.

---

## Objective

Create a feedback-driven improvement system so the skills improve based on real usage, validation failures, review findings, and recurring risks.

The system should make skill improvement:

* traceable
* evidence-based
* prioritised
* versionable
* safe

---

## Required Additions

Create or update the following:

```text
standards/
  feedback-standard.md

tools/
  feedback/
    collect_feedback.py
    summarize_feedback.py

tools/prompts/
  improve_from_feedback.md

assets or examples/
  feedback.schema.json
  sample-feedback.json
```

---

## Feedback Standard

Define how every skill run should capture feedback.

Each feedback record should include:

* skill_name
* project_id
* run_id
* timestamp
* artifact_paths
* user_rating
* reviewer_notes
* validation_result
* confidence_level
* assumptions
* data_gaps
* risk_flags
* failure_modes_observed
* suggested_improvements

---

## Feedback File Location

Feedback should be written to the relevant project folder:

```text
~/sourcing-projects/[project-id]/workflow/feedback.json
```

or, for skill-specific feedback:

```text
~/sourcing-projects/[project-id]/[stage-folder]/feedback.json
```

---

## Improvement Prompt

Create:

```text
tools/prompts/improve_from_feedback.md
```

This prompt should instruct Claude/Codex to:

1. Read feedback records
2. Identify recurring issues
3. Group issues by skill
4. Prioritise improvements
5. Suggest minimal patches
6. Avoid speculative rewrites
7. Preserve skill purpose
8. Update validators or standards only when repeated failures justify it

---

## Improvement Rules

Do NOT improve a skill based on one weak signal unless the issue is critical.

Prioritise:

1. repeated validation failures
2. repeated user confusion
3. recurring hidden assumptions
4. recurring low confidence
5. repeated missing data gaps
6. recurring escalation failures

---

## Output Required

Produce:

### 1. Files Created

List all files created.

### 2. Feedback Schema

Show the feedback structure.

### 3. Improvement Workflow

Explain how feedback flows from run → review → backlog → skill improvement.

### 4. CLI Commands

Provide example commands, such as:

```bash
python tools/feedback/summarize_feedback.py --project ~/sourcing-projects/example-project
```

### 5. Remaining Risks

Identify what still requires human governance.

---

## Guiding Principle

Do not let the skills drift quietly.

Make improvement visible, reviewable, and evidence-based.
