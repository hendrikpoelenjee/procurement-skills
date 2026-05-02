---
name: p9t-award-recommendation
description: Synthesize the sourcing outputs into a decision-ready award recommendation
  with rationale, risks, and implementation conditions.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: decision
  wave: 3
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - decision
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/p9t-award-recommendation.json
  - artifacts/summary.md
  - artifacts/open-questions.json
  review_required: true
  human_approval_required: true
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

Synthesize the sourcing outputs into a decision-ready award recommendation with rationale, risks, and implementation conditions.

# Use when

- A sourcing decision memo is needed
- The team must recommend an award or preferred option

# Do not use when

- Evidence is too thin or essential analysis stages are missing

# Required inputs

- `evaluation_results`
- `commercial_view`
- `risk_view`
- `implementation_needs`
- `approvals`

# Expected outputs

- `artifacts/p9t-award-recommendation.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Recommendation is clear
- Trade-offs are transparent
- Risks and conditions are explicit

# Procedure

1. Confirm all upstream stages are complete and approved before beginning. If any are missing, return blocked — do not synthesise from an incomplete evidence base.
2. Review the relevant baseline, market, and evaluation outputs. Use `references/decision-memo-template.md` as the structure for the recommendation document.
3. Compare the main options and their trade-offs. Include the no-award option if scores are close or evidence is thin.
4. Draft a recommendation with rationale, risks, and implementation conditions. List assumptions, dependencies, and approval requirements explicitly.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm boundaries and which upstream stages are complete
- **Assumptions**: list key inferences
- **Data gaps**: flag what is missing or unverified — missing upstream stage outputs set confidence to INSUFFICIENT_DATA and return blocked; do not synthesise a recommendation from an incomplete evidence base

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

- Evaluation scores are within margin of error between top candidates → present as a tie; do not break without explicit stakeholder input; this is an `INSUFFICIENT_DATA` scenario for a clean recommendation
- A disqualifying risk emerges after evaluation is complete → pause the recommendation; return to the evaluation stage before proceeding
- Required approvers are unavailable or in dispute → do not issue the recommendation; document the blocker and await resolution
- No-award or re-run option has not been considered when evidence is thin or scores are close → surface it explicitly; do not default to recommending the highest-scoring bid
- Stakeholder preference is stated before analysis is complete → flag as bias risk; document the preference and continue the analysis independently

# Epistemic Safety

## Assumptions & Boundaries

- All referenced evaluation outputs are complete, approved, and accurately reflect the sourcing process
- The commercial view reflects the final negotiated position, not an opening offer or indicative price
- The approval hierarchy and sign-off requirements are known before recommendation is issued
- This output does not constitute a legal or contractual commitment; it supports a human decision

## Known Failure Modes

- Recommending based on incomplete upstream evaluation stages, masking evidence gaps
- Framing a stakeholder preference as a data-driven outcome
- Missing implementation risks not captured in the evaluation data
- Overlooking split-award, no-award, or re-run options when evidence is thin or scores are close
- Producing a persuasive narrative that frames a marginal or contested preference as a clear, data-driven outcome — masking the degree of judgment applied

## Escalation Triggers

- Evaluation scores are within margin of error between top candidates → present as tie; do not break without explicit stakeholder input
- A disqualifying risk emerges after evaluation is complete → pause recommendation; return to evaluation stage
- Required approvals cannot be confirmed → do not issue recommendation until resolved
- Stakeholder alignment is absent or contested → document disagreement explicitly; do not issue recommendation

## Confidence Definition

- **HIGH**: Complete evidence trail from baseline through negotiation; all required upstream stages completed and approved; recommendation is fully auditable
- **MEDIUM**: Some evaluation gaps exist but recommendation is defensible; all gaps are explicitly disclosed
- **LOW**: Key inputs are missing or contested; recommendation is indicative only and must not be used for final award without further upstream work
- **INSUFFICIENT_DATA**: Essential upstream stages (evaluation, qualification, or negotiation) are incomplete; a recommendation cannot be responsibly made; return blocked

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. That all upstream evaluation stages are complete and approved before beginning synthesis
2. The trade-off options before a final recommendation is stated
3. That required approvals are in place before the recommendation is communicated externally

# References

- `references/decision-memo-template.md` — Suggested structure for sourcing decision memoranda.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/p9t-award-recommendation.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "confidence_level": "LOW | MEDIUM | HIGH | INSUFFICIENT_DATA",
  "reasoning_trace": "string — how upstream evaluation outputs were synthesised into the recommendation and what trade-offs were considered",
  "escalation_required": "boolean — true when scores are within margin of error, a disqualifying risk emerges post-evaluation, required approvals are missing, or stakeholder alignment is absent",
  "data": {
    "recommended_supplier": "string",
    "recommendation_rationale": "string",
    "evaluated_options": [{"supplier": "string", "score": 0, "rank": 0, "notes": "string"}],
    "alternative_considered": "string",
    "implementation_conditions": ["string"],
    "key_risks": ["string"],
    "approval_requirements": [{"approver": "string", "gate": "string", "status": "string"}]
  }
}
```

Outputs MUST separate:
- **evidence** — what is drawn from approved upstream evaluation outputs
- **inference** — what is reasoned or synthesised across stages
- **assumptions** — what is taken as given, including approval status and commercial finality

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S6-evaluation-framework/` — scoring and evaluation
- `~/sourcing-projects/[project-id]/S7-award/` — negotiation outputs
- `~/sourcing-projects/[project-id]/workflow/` — gate state and approval requirements

### Writes to
`~/sourcing-projects/[project-id]/S7-award/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-award-recommendation.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- award-recommendation.md
- decision-memo.json
