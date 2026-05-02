---
name: p9t-intake-and-brief
description: Turn an unstructured sourcing request into a clean sourcing brief with
  scope, objectives, assumptions, stakeholders, and constraints.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: intake
  wave: 1
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - intake
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/sourcing-brief.json
  - artifacts/summary.md
  - artifacts/open-questions.json
  review_required: true
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

Turn an unstructured sourcing request into a clean sourcing brief with scope, objectives, assumptions, stakeholders, and constraints.

# Use when

- The initial request is incomplete or unstructured
- A formal sourcing brief is needed before analysis begins

# Do not use when

- The brief already exists and only needs minor editing
- The task is solely to review an existing brief

# Required inputs

- `user_request`
- `known_context`
- `constraints`
- `timeline`
- `stakeholders`

# Expected outputs

- `artifacts/sourcing-brief.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Scope is explicit
- Objectives and constraints are separated
- Assumptions are visible
- Open questions are actionable

# Procedure

1. Extract the business need, scope, and desired outcome. Use `references/question-bank.md` to guide elicitation — load it if the user's request is vague or ambiguous.
2. List known constraints, assumptions, and missing information.
3. Identify stakeholders, timeline, and decision criteria.
4. Draft the sourcing brief using the structure in `references/brief-template.md`.
5. Write a concise human-readable summary and open questions.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm category boundary and what is explicitly excluded
- **Assumptions**: list key inferences about need and constraints
- **Data gaps**: flag missing stakeholder, timeline, or budget information — each gap lowers confidence; gaps that block the next gate require escalation before proceeding

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

- User provides contradictory objectives (e.g., "lowest cost" and "premium quality, no compromise") → ask user to resolve before structuring the brief; do not silently choose one
- Stakeholder is unavailable to confirm scope → flag named accountable party as missing; downstream gates require it
- Timeline is materially shorter than what the requested scope implies → flag as execution risk before proceeding
- Category is extremely broad (e.g., "all IT spend") → ask user to confirm operative sub-scope before building the brief
- User submits a brief that already exists → confirm whether this is an update, replacement, or review; do not overwrite without confirmation

# Epistemic Safety

## Assumptions & Boundaries

- The user's initial request reflects their actual need; unstated requirements are out of scope unless surfaced through elicitation
- Constraints and timeline provided are real, not aspirational
- The brief is a working document; it may be incomplete at first pass and requires user validation before use
- Stakeholder views not represented in the request are not captured

## Known Failure Modes

- Structuring an incomplete request into a confident-looking brief, hiding ambiguity behind clean formatting
- Missing implicit requirements that stakeholders assume are obvious but have not articulated
- Accepting unrealistic timelines without flagging them as execution risks
- Conflating objectives with constraints in the brief structure, producing an ambiguous scope

## Escalation Triggers

- User request contains contradictory objectives → ask user to resolve before structuring the brief; do not silently choose one
- Timeline is materially shorter than what the requested scope implies → flag explicitly before proceeding
- Stakeholders are not identified → flag as a risk; downstream approval gates require named accountable parties

## Confidence Definition

- **HIGH**: Objectives, scope, constraints, and stakeholders are all confirmed by the user; brief is internally consistent
- **MEDIUM**: Core scope is clear but some constraints or stakeholders are inferred; key gaps are labelled
- **LOW**: Request is highly ambiguous; brief is indicative only; must be validated by the user before driving any downstream work

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. The core objective before structuring the full brief
2. Open questions for user resolution before the brief is passed downstream
3. That the brief accurately reflects intent before sign-off

# References

- `references/brief-template.md` — Template for a sourcing brief.
- `references/question-bank.md` — Useful clarification questions for sourcing intake.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/sourcing-brief.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how the brief was structured from stated inputs, inferred constraints, and open questions",
  "escalation_required": "boolean — true when contradictory objectives, missing stakeholders, or unrealistic timelines prevent a reliable brief",
  "data": {
    "brief_id": "string",
    "category": "string",
    "sourcing_objective": "string",
    "in_scope": ["string"],
    "out_of_scope": ["string"],
    "must_have_requirements": ["string"],
    "nice_to_have_requirements": ["string"],
    "constraints": ["string"],
    "stakeholders": [{"name": "string", "role": "string", "approval_required": "boolean"}],
    "timeline": {"target_award": "string", "go_live": "string"},
    "incumbent_context": "string",
    "budget_envelope": "string"
  },
  "handoff_summary": {
    "for_skill": "p9t-supplier-longlist",
    "key_inputs": {
      "category": "string — normalised category label",
      "spec_summary": "string — key product/service requirements",
      "geography": "string",
      "spend_estimate": "string",
      "timeline": "string",
      "constraints": ["string"]
    },
    "flags": ["string — risks or blockers to carry forward"],
    "assumptions_to_carry_forward": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — what was explicitly stated in the user's request
- **inference** — what was structured or interpreted from the request
- **assumptions** — what was taken as given to complete the brief

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/workflow/` — routing context if project already exists

### Writes to
`~/sourcing-projects/[project-id]/S1-intake/`

### Typical outputs
- sourcing-brief.json
- summary.md
- open-questions.json
