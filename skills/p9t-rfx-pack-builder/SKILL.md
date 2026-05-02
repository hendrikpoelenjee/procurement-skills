---
name: p9t-rfx-pack-builder
description: Build a practical RFx pack including instructions, requirements, pricing
  structure, and response logic.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: rfx
  wave: 3
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - rfx
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/rfx-pack.json
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

Build a practical RFx pack including instructions, requirements, pricing structure, and response logic.

# Use when

- The team is preparing to go to market
- Supplier responses need to be structured and comparable

# Do not use when

- The event does not require a formal RFx pack
- The task is legal drafting of final contract terms

# Required inputs

- `sourcing_brief`
- `requirements`
- `timeline`
- `commercial_model`
- `evaluation_logic`

# Expected outputs

- `artifacts/rfx-pack.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- RFx structure is complete
- Response logic supports comparability
- Supplier instructions are clear

# Procedure

1. Define the event type, objectives, and supplier instructions. Use `references/rfx-outline.md` to confirm the required sections before drafting.
2. Organize requirements into clear response sections. Check each requirement for supplier-specific language before proceeding.
3. Draft commercial schedules and pricing template structure. Load `references/pricing-template-guidance.md` and apply the comparability checklist before finalising the template.
4. Align the pack with the intended evaluation approach. Confirm the evaluation criteria exist and are locked before the pack is issued.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm event type, number of lots, and target supplier audience
- **Assumptions**: list key inferences about requirements and commercial model
- **Data gaps**: flag missing specification detail, compliance requirements, or evaluation criteria — missing legal or compliance sections block issue; missing evaluation criteria must be resolved before the pack is sent

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

- Requirements are written in language specific to an incumbent's product or methodology → flag supplier-specific language before proceeding; do not issue
- Commercial model in the target market uses unit rates but buyer requests a fixed-price template → escalate; the template structure must match how the market prices
- Legal review gate is unclear or unavailable → block issue; do not treat absence of legal review as implicit approval
- Multi-lot structure creates inconsistency between lots (different terms, different pricing bases) → surface inconsistencies; require user resolution
- Evaluation criteria are requested after the pack is drafted → flag integrity risk; criteria must precede, not follow, pack design

# Epistemic Safety

## Assumptions & Boundaries

- The sourcing brief and requirements provided are approved and complete; if the brief is incomplete, the RFx will be incomplete
- The RFx is designed to elicit comparable responses; it does not pre-select a winner
- Legal drafting of final contract terms is out of scope; legal review is required before issue
- This skill produces a draft; compliance review of mandatory sections is the user's responsibility

## Known Failure Modes

- Writing requirements in language specific to an incumbent supplier's capability, disadvantaging other bidders
- Pricing templates that cannot accommodate different commercial models, producing incomparable responses
- Missing mandatory compliance or legal sections required for the category or jurisdiction
- Supplier instructions that are ambiguous, producing responses that cannot be consistently evaluated

## Escalation Triggers

- Requirements appear to describe an existing supplier's specific solution → flag supplier-specific language before proceeding
- Pricing template cannot accommodate expected commercial model variation → escalate before finalising the structure
- A legal or regulatory section is missing → block issue; refer to legal review before proceeding

## Confidence Definition

- **HIGH**: Requirements are technology-neutral, pricing template enables fair comparison, instructions are clear and complete; legal sections are present
- **MEDIUM**: Draft is structurally sound but one or more sections need refinement; specific gaps are documented
- **LOW**: Requirements or pricing template have significant gaps; must not be issued to suppliers without revision and legal review

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. That requirements are technology-neutral and do not inadvertently favour an incumbent
2. That the pricing template structure matches the commercial models expected from the market
3. That legal review sign-off is obtained before the RFx is issued to any supplier

# References

- `references/rfx-outline.md` — Suggested sections for RFx packs.
- `references/pricing-template-guidance.md` — How to structure comparable commercial responses.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/rfx-pack.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how the pack structure was derived from the brief, commercial model, and evaluation logic",
  "escalation_required": "boolean — true when requirements appear supplier-specific, legal sections are missing, or the pricing template cannot accommodate the expected commercial model",
  "data": {
    "event_type": "RFI | RFP | RFQ | ITT",
    "lots": "integer",
    "sections": [{"title": "string", "purpose": "string", "status": "complete | draft | missing"}],
    "commercial_model": "string",
    "pricing_template_structure": "string",
    "evaluation_logic_reference": "string",
    "legal_review_required": "boolean"
  }
}
```

Outputs MUST separate:
- **evidence** — requirements drawn directly from the approved brief
- **inference** — structure and format derived from category knowledge and evaluation logic
- **assumptions** — commercial model, legal standard, and evaluation approach taken as given

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S1-intake/` — sourcing brief and requirements
- `~/sourcing-projects/[project-id]/S4-supplier-qualification/` — shortlist
- `~/sourcing-projects/[project-id]/workflow/` — routing context

### Writes to
`~/sourcing-projects/[project-id]/S5-rfq/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- rfx-pack.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- pricing-template.md
- instructions.md
