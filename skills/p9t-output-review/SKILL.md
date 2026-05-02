---
name: p9t-output-review
description: Review sourcing outputs for completeness, schema fit, contradictions,
  unsupported claims, and readiness for handoff.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: governance
  wave: 1
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - governance
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/review-result.json
  - artifacts/summary.md
  - artifacts/open-questions.json
  review_required: false
  human_approval_required: false
  external_input: false
  claude_md_version: ">=0.2.0"
  context_budget:
    skill_md_lines: "<200"
    loaded_references: "<=2 at any time"
    total_tokens_target: "<4000"
allowed-tools: Read Bash(git:*)
---

> **Interaction Standard:** This skill follows [Guided Execution Mode](../../standards/interaction-patterns.md).
> Ask ONE question at a time. Wait. Adapt. Signal readiness before executing.

---


# Purpose

Review sourcing outputs for completeness, schema fit, contradictions, unsupported claims, and readiness for handoff.

# Use when

- Any skill output needs an independent check before handoff
- A workflow stage should be gated by review

# Do not use when

- The reviewer is expected to redo the substantive work instead of checking it

# Required inputs

- `target_artifacts`
- `expected_schema`
- `acceptance_criteria`

# Expected outputs

- `artifacts/review-result.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Issues are specific
- Verdict is explicit
- Next action is actionable

# Procedure

1. Load the target artifacts and expected output contract.
2. Check completeness, consistency, and schema fit.
3. Flag unsupported claims, hidden assumptions, and missing evidence.
4. Return a verdict and recommended next action.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate which skill output is under review and against which gate
- **Scope**: confirm which artifacts are in scope for this review pass
- **Assumptions**: list any inferences about expected quality standard
- **Data gaps**: flag any missing artifacts or context that would limit review completeness — missing artifacts block the review; do not issue a verdict on something you have not been able to inspect

# Operating rules

## Context discipline

- Prefer targeted context over full transcripts.
- Load referenced files only when needed.
- Keep the top-level skill focused and push detailed guidance into `references/`.

## Tool discipline

- Use only the minimum tools required for the task.
- Treat tool failures as explicit failures.
- Never claim a shell or file action succeeded without evidence.

## Quality discipline

- Distinguish facts, assumptions, and recommendations.
- Be explicit about uncertainty and evidence gaps.
- Prefer structured outputs over prose where possible.

# Failure policy

Stop and return `blocked` when:
- required input is missing and no safe assumption is possible
- a required tool is unavailable
- validation fails after the allowed retries
- the task would require a prohibited or irreversible action without approval

When blocked, return:
- what was completed
- what failed
- what input or approval is needed next

# Edge cases

- Artifact is schema-compliant but evidentially thin (clean structure, no real substance) → flag as substantive failure, not a schema pass; the two are independent checks
- Conflicting conclusions between artifacts from different stages → do not issue a PASS; surface the conflict and escalate for human resolution
- Reviewer is asked to accept a PASS on an artifact they were not given access to → block; a review without access to the artifact is not a review
- A finding at review stage has upstream blocking implications for the workflow (e.g., a qualification error that invalidates the shortlist) → escalate before issuing a verdict; do not contain findings within the review artifact alone
- Reviewer is asked to correct issues in the artifact rather than return them → decline; the role is to check, not redo; substantive issues must be returned to the originating skill

# Epistemic Safety

## Assumptions & Boundaries

- The reviewer role is to check, not redo; substantive issues found must be returned to the originating skill, not corrected in-place
- The target artifacts are the most current approved versions
- Review criteria are those specified by the user or the applicable workflow gate definition
- This skill cannot independently verify the accuracy of external data referenced in artifacts

## Known Failure Modes

- Passing artifacts that are technically schema-compliant but substantively weak or evidentially thin
- Missing unsupported claims that are plausible-sounding but not evidenced in the artifact
- Over-reviewing to the point of substituting reviewer judgment for the originating skill's analysis
- Failing to escalate when a review finding has downstream blocking implications for the workflow

## Escalation Triggers

- A critical required field is absent or empty → block handoff immediately; return to the originating skill
- A finding would materially change the recommended next action → escalate before issuing a verdict
- Conflicting content between artifacts is unresolvable at review stage → escalate to human decision; do not issue a PASS

## Confidence Definition

- **HIGH**: All required sections are present, internally consistent, evidenced, and schema-compliant; verdict is clear
- **MEDIUM**: Minor gaps or weak evidence in non-critical sections; issues are documented; verdict is conditional
- **LOW**: Significant gaps, unsupported claims, or schema violations detected; artifact must not progress until resolved

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. If review verdict is FAIL, return to the originating skill rather than attempting repair
2. Present the finding summary before issuing the final PASS or FAIL verdict
3. Any borderline cases where the verdict requires human judgment rather than rule application

# References

- `references/review-checklist.md` — Standard review checklist for sourcing skill outputs.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/review-result.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — what was reviewed, which protocol was applied, and how the verdict was reached",
  "escalation_required": "boolean — true when a critical field is absent, a finding materially changes the recommended next action, or artifacts contain unresolvable conflicts",
  "data": {
    "verdict": "PASS | CONDITIONAL_PASS | FAIL",
    "target_skill": "string",
    "gate": "string",
    "findings": [{"field": "string", "issue": "string", "severity": "blocking | advisory"}],
    "blocking_issues_count": "integer",
    "advisory_issues_count": "integer",
    "conditions": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — findings directly observable in the reviewed artifact
- **inference** — gaps inferred from what is absent or inconsistent
- **assumptions** — what is taken as the intended standard the artifact is being held to

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/[stage-folder]/` — any stage folder under review
- `~/sourcing-projects/[project-id]/workflow/` — workflow state

### Writes to
`~/sourcing-projects/[project-id]/workflow/`

### Typical outputs

Basenames under `workflow/` (must match Expected outputs and `primary_artifacts`):

- `review-result.json`
- `summary.md`
- `open-questions.json`
