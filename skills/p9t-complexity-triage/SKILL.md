---
name: p9t-complexity-triage
description: >
  Assess sourcing complexity and recommend the minimum viable workflow, review
  intensity, and human approval gates.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: >
  Requires local file access. Optional web access. Works via adapter overlays
  for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: "0.2.0"
  status: draft
  category: orchestration
  wave: 1
  maturity: beta
  tags:
    - sourcing
    - agents
    - cli
    - orchestration
  output_schema: assets/output.schema.json
  primary_artifacts:
    - artifacts/complexity-assessment.json
    - artifacts/summary.md
    - artifacts/open-questions.json
  review_required: true
  human_approval_required: false
  external_input: false
  claude_md_version: ">=0.2.0"
  context_budget:
    skill_md_lines: "<215"
    loaded_references: "<=2 at any time"
    total_tokens_target: "<4000"
allowed-tools: Read Bash(git:*)
---

> **Interaction Standard:** This skill follows [Guided Execution Mode](../../standards/interaction-patterns.md).
> Ask ONE question at a time. Wait. Adapt. Signal readiness before executing.

---


# Purpose

Assess sourcing complexity and recommend the minimum viable workflow, review intensity, and approval gates.

# Use when

- The user wants the right level of sourcing effort
- The request may be simple, moderate, or highly strategic
- The conductor needs a defensible routing decision

# Do not use when

- The complexity has already been classified and approved
- The task is not related to sourcing decision support

# Required inputs

- `category`
- `spend_estimate`
- `switching_risk`
- `supply_risk`
- `timeline`
- `stakeholder_count`
- `incumbent_supplier_state` (preferred)
- `regulatory_or_operational_criticality` (preferred)

# Expected outputs

- `artifacts/complexity-assessment.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Complexity rating is justified by scored dimensions
- Recommended workflow is proportional
- Review intensity is explicit
- Human approval requirements are explicit

# Procedure

1. Score the request using the model in `references/complexity-model.md`.
2. Explain the rating in terms of value, risk, and change impact.
3. Recommend the minimum viable set of sourcing stages.
4. Flag where human approval is required and what decision each gate controls.
5. Return a restart point if more input is needed.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm category, spend estimate, and key risk dimensions
- **Assumptions**: list key inferences used in scoring
- **Data gaps**: flag inputs estimated or inferred rather than provided — inferred inputs lower confidence to MEDIUM at best; missing critical inputs (spend, criticality) require escalation before a routing decision is issued

# Operating rules

## Context discipline

- Prefer targeted context over full transcripts.
- Load referenced files only when needed.
- Keep the output compact enough for the conductor to consume directly.

## Tool discipline

- Use only the minimum tools required for assessment.
- Treat tool failures as explicit failures.
- Never claim a shell or file action succeeded without evidence.

## Quality discipline

- Distinguish facts, assumptions, and recommendations.
- Show the scoring logic.
- Use override rules explicitly when applied.

# Failure policy

Stop and return `blocked` when:
- required input is missing and no safe assumption is possible
- a required tool is unavailable
- validation fails after the allowed retries
- the complexity cannot be assessed with meaningful confidence

When blocked, return:
- what was completed
- what failed
- what input or approval is needed next

# Edge cases

- Spend is low but criticality is high (safety-critical or single-source item) → override to at least `moderate`; do not score on spend alone
- Category overlaps multiple business units with conflicting risk profiles → confirm operative scope before scoring
- User deliberately understates complexity to obtain a simpler process → this skill scores what it is given; flag assumptions explicitly and note what would change the rating
- Timeline is shorter than any viable workflow path for the scored complexity → flag as timeline risk; do not silently compress the workflow
- No incumbent signal present but user expects renewal-style governance → surface the ambiguity; default path-type reasoning applies

# Epistemic Safety

## Assumptions & Boundaries

- Inputs reflect the actual sourcing situation, not a sanitised or optimistic view
- The complexity model is calibrated for standard procurement contexts; highly regulated or politically sensitive categories may require manual overrides
- Triage output is a routing recommendation, not a binding governance decision; a human must confirm before execution begins
- This skill scores on visible dimensions only; undisclosed constraints are out of scope

## Known Failure Modes

- Underestimating complexity when spend is low but switching risk or criticality is high
- Overestimating complexity on commodity categories, adding unnecessary process overhead
- Treating the routing recommendation as binding before stakeholders have confirmed scope
- Missing operational criticality signals that are not reflected in spend or risk data alone
- Producing a misleadingly simple routing recommendation when scope or spend is deliberately understated — this skill scores what it is given; garbage in, governance out

## Escalation Triggers

- Spend and risk signals are contradictory (e.g., low spend, high criticality) → escalate for human calibration; do not apply default scoring
- Category is in a regulated sector or involves safety-critical supply → override to at least `moderate` regardless of spend
- Stakeholder count is high and alignment is uncertain → flag G1 gate as blocking before any workflow stages begin

## Confidence Definition

- **HIGH**: All required scoring inputs provided; complexity dimensions are unambiguous; routing is deterministic
- **MEDIUM**: Some dimensions estimated or inferred; scoring rationale is visible; user confirmation recommended
- **LOW**: Critical inputs missing; routing recommendation is provisional and must be confirmed before any workflow stage begins

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Complexity rating before the workflow plan is issued
2. Any override rules applied and the rationale for them
3. That G1_scope_approval is required before any specialist skill is executed

# References

- `references/complexity-model.md` — Weighted criteria and override rules for simple, moderate, and strategic sourcing cases.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/complexity-assessment.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how dimension scores led to the complexity classification and routing recommendation",
  "escalation_required": "boolean — true when spend/risk signals are contradictory, category is safety-critical, or stakeholder alignment is uncertain",
  "data": {
    "complexity": "simple | moderate | strategic",
    "score_total": 0,
    "dimension_scores": {},
    "recommended_path_types": ["string"],
    "required_gates": ["string"]
  },
  "handoff_summary": {
    "for_skill": "p9t-run-sourcing-workflow",
    "key_inputs": {
      "complexity": "simple | moderate | strategic",
      "recommended_path": "string — path type recommended by triage",
      "confidence_level": "LOW | MEDIUM | HIGH"
    },
    "flags": ["string — override rules applied or escalation triggers"],
    "assumptions_to_carry_forward": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — scored dimensions from provided inputs
- **inference** — override rules applied and rationale
- **assumptions** — dimensions estimated from partial data
```

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S1-intake/` — sourcing brief

### Writes to
`~/sourcing-projects/[project-id]/workflow/`

### Typical outputs

Basenames under `workflow/` (must match Expected outputs and `primary_artifacts`):

- `complexity-assessment.json`
- `summary.md`
- `open-questions.json`
