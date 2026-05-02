---
name: p9t-supplier-qualification
description: Screen longlisted suppliers against qualification criteria and produce
  a defendable shortlist.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: selection
  wave: 2
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - selection
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/p9t-supplier-qualification.json
  - artifacts/summary.md
  - artifacts/open-questions.json
  review_required: true
  human_approval_required: false
  external_input: true
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

Screen longlisted suppliers against qualification criteria and produce a defendable shortlist.

# Use when

- A longlist must be narrowed before RFx or engagement
- Minimum viability or risk gating is needed

# Do not use when

- The task is detailed due diligence or final award sign-off

# Required inputs

- `supplier_longlist`
- `qualification_criteria`
- `disqualifiers`
- `evidence`

# Expected outputs

- `artifacts/p9t-supplier-qualification.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Criteria are applied consistently
- Pass/fail reasons are visible
- Shortlist is defendable

# Procedure

1. Load the candidate list and confirm the qualification criteria with the user before screening begins. Use `references/qualification-matrix.md` to structure the two-layer approach (mandatory disqualifiers first, weighted criteria second).
2. Apply pass/fail and weighted screening logic consistently. Do not apply disqualifiers and weighted scoring simultaneously — run the mandatory layer first; only score candidates that pass it.
3. Record evidence, uncertainty, and disqualification reasons for every candidate, including borderline cases.
4. Produce a shortlist with rationale. Flag concentration risk if fewer than 3 pass, or if all passing candidates share a parent group.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm which candidate list is in scope and which criteria are mandatory disqualifiers
- **Assumptions**: list key inferences about evidence availability
- **Data gaps**: flag candidates where evidence is absent or unverifiable — absent evidence is not a disqualifier by itself; record as "unverified" and surface to the user before the verdict is applied

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

- All candidates fail qualification → criteria may be miscalibrated or set to incumbent profile; escalate before concluding no viable market exists
- Only one candidate passes → flag concentration risk immediately; this shapes the entire RFx strategy
- Evidence for a mandatory criterion is self-declared only → record as unverified, not as met; flag for independent confirmation
- An incumbent's certification has lapsed since the longlist was built → apply the same rules as any other candidate; do not grandfather
- A disqualifier is contested by the user after it has been applied → re-open the affected verdict; document the dispute; do not silently overturn without documented rationale

# Epistemic Safety

## Assumptions & Boundaries

- The supplied longlist is a reasonable starting set, not adversarially curated to favour a predetermined shortlist
- Qualification criteria reflect actual stakeholder priorities, not legacy defaults or incumbent-calibrated standards
- Evidence provided by or about suppliers is accurate and current; this skill cannot independently verify it
- Legal status, insurance, and compliance certifications cannot be verified independently without external tools

## Known Failure Modes

- Disqualifying on absence of evidence rather than evidence of a disqualifying condition
- Applying criteria inconsistently when criteria descriptions are ambiguous
- Reinforcing incumbent bias when qualification criteria are implicitly calibrated to an existing supplier's profile
- Missing unstated disqualifiers that stakeholders assume are obvious but have not articulated

## Escalation Triggers

- All candidates fail qualification → criteria may be miscalibrated; pause and review before proceeding
- Only one candidate passes → concentration risk; flag explicitly before moving to RFx
- Evidence for a candidate is contradictory or unverifiable → surface as data gap; do not apply a ruling
- A disqualifier is contested by the user → resolve before applying it to any candidate

## Confidence Definition

- **HIGH**: Criteria are explicit, evidence is documented for each decision, shortlist is fully auditable
- **MEDIUM**: Most criteria applied with partial evidence; reasoning is visible and traceable for each candidate
- **LOW**: Criteria are vague or evidence is missing for a significant portion of the longlist; shortlist must not be used without further review

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Qualification criteria and any mandatory disqualifiers before screening begins
2. Borderline pass/fail decisions before finalising the shortlist
3. Whether the resulting shortlist preserves sufficient competition and is commercially credible

# References

- `references/qualification-matrix.md` — Pass/fail and weighted qualification patterns.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/p9t-supplier-qualification.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how criteria were applied, evidence was weighed, and borderline cases were handled",
  "escalation_required": "boolean — true when all candidates fail, only one passes, evidence is contradictory, or a disqualifier is contested",
  "data": {
    "shortlisted": [{"candidate_id": "string", "name": "string", "weighted_score": 0, "verdict_rationale": "string"}],
    "disqualified": [{"candidate_id": "string", "name": "string", "disqualification_reason": "string", "disqualifying_criterion": "string"}],
    "borderline": [{"candidate_id": "string", "name": "string", "borderline_reason": "string"}],
    "concentration_risk_flag": "boolean",
    "criteria_applied": [{"criterion": "string", "type": "mandatory | weighted", "weight": 0}]
  }
}
```

Outputs MUST separate:
- **evidence** — what is directly documented per candidate
- **inference** — what is reasoned from partial evidence
- **assumptions** — what is taken as given without independent verification

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S3-supplier-longlist/` — longlist
- `~/sourcing-projects/[project-id]/workflow/` — qualification criteria and gate state

### Writes to
`~/sourcing-projects/[project-id]/S4-supplier-qualification/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-supplier-qualification.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- qualification-matrix.json
- shortlist.json
