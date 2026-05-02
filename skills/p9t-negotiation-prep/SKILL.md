---
name: p9t-negotiation-prep
description: Prepare the negotiation strategy, target positions, fallback positions,
  concessions, and supplier pressure points.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: negotiation
  wave: 2
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - negotiation
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/p9t-negotiation-prep.json
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

Prepare the negotiation strategy, target positions, fallback positions, concessions, and supplier pressure points.

# Use when

- Negotiation is approaching
- The team needs a clear plan before engaging suppliers

# Do not use when

- The task is to conduct the live negotiation itself
- The current state lacks enough baseline and market context

# Required inputs

- `supplier_context`
- `market_scan`
- `baseline`
- `commercial_objectives`
- `risks`

# Expected outputs

- `artifacts/p9t-negotiation-prep.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Targets and fallbacks are explicit
- Concessions are controlled
- Risks and leverage points are visible

# Procedure

1. Summarize negotiation objectives and the current supplier posture. Load `references/negotiation-map.md` to structure positions, leverage, and concessions.
2. Translate market and baseline insights into leverage points. Rate each leverage point (HIGH / MEDIUM / LOW) and note whether it is real or theoretical.
3. Define target positions, walk-away points, and fallback options. Apply the ZOPA and BATNA concepts from the negotiation map; confirm walk-away with decision authority before use.
4. Draft a concession sequence and meeting plan. Apply the concession sequencing rules — low-cost items first; never concede without a counter.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm supplier, category, and which negotiation stage this covers
- **Assumptions**: list key inferences about leverage and supplier posture
- **Data gaps**: flag missing market scan, baseline, or supplier intelligence — missing BATNA or absence of real alternatives must be declared explicitly; they change the nature of the plan materially

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

- No real BATNA exists (incumbent is sole source or switching cost is prohibitive) → do not overstate competitive leverage; declare constraint explicitly before positions are set
- Supplier has demonstrated knowledge of the buyer's internal constraints → flag leverage inversion risk; adjust position assumptions accordingly
- Negotiation is already underway with active supplier offers on the table → do not generate fresh baseline positions that could contradict what has been communicated; update the existing plan
- Walk-away point would cause supply disruption → escalate to risk decision authority before the point is finalised
- This is a strategic or relationship-sensitive supplier → require senior stakeholder review of the plan before any negotiation interaction

# Epistemic Safety

## Assumptions & Boundaries

- Market scan and baseline data used as inputs are accurate and have been approved upstream
- Supplier context is based on available information; undisclosed supplier constraints or intentions are out of scope
- This output is a preparation document; it does not predict how the supplier will actually behave
- Walk-away points and fallback positions are commercially sensitive; access must be controlled and not shared with external parties

## Known Failure Modes

- Overstating leverage when market alternatives are theoretical rather than real and accessible
- Presenting walk-away positions as fixed when they are actually negotiable or stakeholder-dependent
- Missing relationship or political dimensions that affect what leverage is realistically usable
- Underestimating an incumbent supplier's information advantage about the buyer's constraints

## Escalation Triggers

- Market scan shows limited or no real alternatives → do not overstate competitive leverage; flag explicitly
- Walk-away position would trigger supply disruption → escalate to risk decision authority before use
- Supplier has demonstrated knowledge of the buyer's internal constraints → flag leverage inversion risk
- This is a strategic supplier relationship → require senior stakeholder review of the negotiation plan before use
- Negotiation is already underway with active supplier offers in play → do not generate fresh baseline positions; update the existing plan rather than creating positions that could contradict what has already been communicated

## Confidence Definition

- **HIGH**: Market, baseline, and supplier data are complete and validated; leverage assessment is well-grounded and cross-checked
- **MEDIUM**: Some leverage assumptions are inferred from partial data; key assumptions are visible and labelled
- **LOW**: Limited market or supplier intelligence; negotiation plan is indicative only; must not be used without further research and stakeholder review

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Walk-away point and fallback positions with decision authority before negotiation begins
2. Leverage assumptions against stakeholder's knowledge of the relationship
3. That the negotiation plan has explicit sign-off before being shared with any participant

# References

- `references/negotiation-map.md` — Framework for positions, concessions, and leverage.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/p9t-negotiation-prep.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how market and baseline data were translated into leverage assessment and position setting",
  "escalation_required": "boolean — true when no real alternatives exist, walk-away triggers supply disruption, leverage inversion is detected, or senior sign-off is required",
  "data": {
    "supplier": "string",
    "objectives": ["string"],
    "positions": {"opening": "string", "target": "string", "walk_away": "string"},
    "leverage_points": [{"point": "string", "strength": "HIGH | MEDIUM | LOW"}],
    "concession_sequence": [{"item": "string", "value_to_buyer": "string", "cost_to_supplier": "string"}],
    "batna": "string",
    "relationship_sensitivity": "string"
  }
}
```

Outputs MUST separate:
- **evidence** — leverage points grounded in validated market and baseline data
- **inference** — positions derived from partial supplier intelligence
- **assumptions** — conditions taken as given, including supplier behaviour and market access

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S4-supplier-qualification/` — shortlist and supplier profiles
- `~/sourcing-projects/[project-id]/S6-evaluation-framework/` — evaluation results
- `~/sourcing-projects/[project-id]/workflow/` — gate state

### Writes to
`~/sourcing-projects/[project-id]/S7-award/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-negotiation-prep.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- negotiation-strategy.md
- positions.json
- negotiation-summary.md
