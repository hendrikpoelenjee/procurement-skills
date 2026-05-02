---
name: p9t-bid-evaluation-framework
description: Define a weighted bid evaluation framework with commercial, technical,
  service, and risk criteria.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: selection
  wave: 3
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - selection
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/p9t-bid-evaluation-framework.json
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

Define a weighted bid evaluation framework with commercial, technical, service, and risk criteria.

# Use when

- Supplier bids must be assessed consistently
- A scorecard is needed before the RFx launches or before responses are reviewed

# Do not use when

- The task is to produce final approval documentation only

# Required inputs

- `requirements`
- `decision_criteria`
- `risk_factors`
- `commercial_priorities`

# Expected outputs

- `artifacts/p9t-bid-evaluation-framework.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Weights are clear
- Criteria are non-overlapping
- Scoring logic is auditable

# Procedure

1. Convert decision priorities into weighted evaluation dimensions. Load `references/scorecard-patterns.md` to select an appropriate dimension taxonomy and weight range for the category type.
2. Define clear scoring anchors and evidence expectations for every score point — not just the top and bottom.
3. Check for overlap (double-counting), implicit bias toward an incumbent, and missing criteria.
4. Confirm total weight sums to 100%. Write the scorecard structure and guidance.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm evaluation dimensions and weight allocation approach
- **Assumptions**: list key inferences about priorities
- **Data gaps**: flag missing criteria or stakeholder alignment gaps — if criteria are missing or stakeholders disagree on weights, set confidence to INSUFFICIENT_DATA and block; do not issue a framework that has not been agreed

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

- Stakeholders cannot agree on weight allocation → document divergence and escalate to decision authority; do not average conflicting inputs silently
- Framework is requested after bids have been received → flag as integrity risk; document criteria provenance to confirm they are not reverse-engineered from a preferred bid
- A regulatory or policy-mandated criterion is missing from the initial design → add it; flag if it materially changes the framework weights
- Only one scoring anchor (e.g., the top score) is clearly defined while others are vague → require anchor definitions for all scores before use; vague anchors produce divergent evaluator scores
- Total weights do not sum to 100% → block; return framework for correction before use

# Epistemic Safety

## Assumptions & Boundaries

- Decision criteria provided reflect actual business priorities, not post-hoc rationalisation
- The framework is designed before bids are received; it must not be reverse-engineered from a preferred outcome
- Commercial and technical dimensions are separable enough to be scored independently
- Politically sensitive weighting choices may not surface through standard elicitation; surfacing them is the user's responsibility

## Known Failure Modes

- Overlapping criteria that inflate the apparent importance of one evaluation dimension
- Weights calibrated — intentionally or not — to produce a predetermined winner
- Scoring anchors too vague to apply consistently across evaluators, producing divergent scores
- Omitting criteria that are hard to quantify but are genuinely decision-relevant

## Escalation Triggers

- Stakeholders disagree on weight allocation → do not proceed; document divergence and escalate to decision authority
- A legally or policy-mandated criterion is absent → add it before use; flag if it changes the framework materially
- The framework would produce only one defensible winner regardless of bid content → flag as structural risk; do not issue
- Framework is being designed after bids have been received → flag as integrity risk; document criteria provenance to confirm they are not reverse-engineered from a preferred bid

## Confidence Definition

- **HIGH**: Criteria are non-overlapping, weights are stakeholder-validated, scoring anchors are specific and consistently applicable
- **MEDIUM**: Framework is structurally sound but one or more criteria need refinement before live evaluation use
- **LOW**: Weights are provisional; criteria require stakeholder review; must not be applied to live bids without revision
- **INSUFFICIENT_DATA**: Decision criteria or requirements are too thin, absent, or contradictory to construct a defensible framework; do not produce a framework under these conditions

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Weight allocation before the framework is finalised
2. That no mandatory compliance or regulatory criteria are missing
3. That scoring anchors are unambiguous enough for all evaluators to apply consistently

# References

- `references/scorecard-patterns.md` — Common weighted scorecard patterns for sourcing events.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/p9t-bid-evaluation-framework.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "confidence_level": "LOW | MEDIUM | HIGH | INSUFFICIENT_DATA",
  "reasoning_trace": "string — how decision priorities were translated into dimensions, weights were allocated, and overlap was checked",
  "escalation_required": "boolean — true when stakeholders disagree on weights, a mandatory criterion is absent, the framework produces only one defensible winner, or it was designed after bids were received",
  "data": {
    "dimensions": [{"name": "string", "weight": 0, "scoring_scale": "string", "score_anchors": {}, "evidence_expectation": "string"}],
    "total_weight": 100,
    "commercial_weight": 0,
    "overlap_check": "PASS | FAIL",
    "mandatory_criteria": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — criteria and weights validated by stakeholders
- **inference** — scoring anchors derived from category knowledge
- **assumptions** — priorities taken as given without stakeholder sign-off

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S1-intake/` — objectives and constraints
- `~/sourcing-projects/[project-id]/S5-rfq/` — RFQ scope and criteria
- `~/sourcing-projects/[project-id]/workflow/` — routing context

### Writes to
`~/sourcing-projects/[project-id]/S6-evaluation-framework/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-bid-evaluation-framework.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- scoring-matrix.md
