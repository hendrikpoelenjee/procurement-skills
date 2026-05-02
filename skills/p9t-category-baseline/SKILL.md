---
name: p9t-category-baseline
description: Establish the internal baseline for a category, including demand profile,
  current supplier situation, cost drivers, and sourcing levers.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
  status: draft
  category: strategy
  wave: 2
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - strategy
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/p9t-category-baseline.json
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

Establish the internal baseline for a category, including demand profile, current supplier situation, cost drivers, and sourcing levers.

# Use when

- A sourcing strategy must be grounded in current-state facts
- The team needs a baseline before market work or negotiations

# Do not use when

- The task is purely external market research with no internal baseline needed

# Required inputs

- `category`
- `current_suppliers`
- `spend_profile`
- `usage_pattern`
- `issues`
- `contract_context`

# Expected outputs

- `artifacts/p9t-category-baseline.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Demand and supplier baseline are clear
- Cost/risk hypotheses are explicit
- Sourcing levers are identified

# Procedure

1. Summarize the category scope and current supplier setup. Use the structure in `references/baseline-template.md` to ensure all baseline dimensions are covered.
2. Map demand, usage, spend, and contract posture.
3. Identify cost drivers, service issues, dependencies, and risks. Load `references/cost-driver-cues.md` and apply the prompts relevant to this category type.
4. Propose sourcing levers and baseline hypotheses.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm category boundary and which spend is in scope
- **Assumptions**: list key inferences about current supplier situation
- **Data gaps**: flag missing spend, contract, or demand data — missing spend for a significant portion of the category triggers escalation; partial data must be labelled as such in the baseline

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

- Spend data covers only part of the category (tail spend, shadow purchases missing) → declare coverage gap; do not present partial spend as the full baseline
- Multiple business units have conflicting views of the same supplier → confirm scope and which BU's data governs before building the baseline
- No formal contract exists with the incumbent → flag as a risk; renewal timelines and exit options cannot be assessed without it
- Shadow suppliers discovered mid-analysis (purchases outside the defined scope) → surface immediately; they may change the cost driver picture materially
- User provides spend data that contradicts the stated "only one supplier" claim → surface the contradiction; do not resolve it silently

# Epistemic Safety

## Assumptions & Boundaries

- Spend data, usage patterns, and contract context provided by the user are accurate and current
- The current supplier situation is as described; undisclosed arrangements or side agreements are out of scope
- Cost drivers are identified based on the category as scoped; adjacent categories are excluded unless explicitly included
- This is an internal view only; it does not constitute external market intelligence

## Known Failure Modes

- Accepting user-supplied baseline data uncritically when it may be outdated or incomplete
- Conflating demand volatility with supply risk, leading to misaligned strategy recommendations
- Missing hidden cost components such as tail spend, maintenance, or obsolescence
- Over-indexing on visible direct spend; missing embedded, indirect, or shadow costs

## Escalation Triggers

- Spend data is inconsistent or missing for a significant portion of the category → flag before proceeding; do not estimate
- User describes a supplier situation that implies undisclosed dependency or lock-in → surface explicitly before baseline is used
- Category spans multiple business units with conflicting requirements or data → confirm scope before proceeding

## Confidence Definition

- **HIGH**: Spend, supplier, and contract data are all provided and internally consistent; cost drivers are documented
- **MEDIUM**: Some data is missing or estimated; key gaps are explicitly labelled; baseline is usable with caveats
- **LOW**: Significant data gaps; baseline is indicative only; must not drive sourcing strategy without further validation

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Category boundary and which spend is in scope before building the baseline
2. Cost driver hypotheses against stakeholder knowledge before finalising
3. Any undisclosed dependencies or lock-in risks flagged during the analysis

# References

- `references/baseline-template.md` — Structured template for internal category baseline.
- `references/cost-driver-cues.md` — Common cost driver prompts by category type.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/p9t-category-baseline.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how spend, supplier, and contract data were synthesised into the baseline and cost driver analysis",
  "escalation_required": "boolean — true when spend data is missing for a significant portion, or supplier situation implies undisclosed dependency",
  "source_quality": {
    "recency": "LOW | MEDIUM | HIGH",
    "coverage": "LOW | MEDIUM | HIGH",
    "bias_risk": "LOW | MEDIUM | HIGH"
  },
  "data": {
    "category_scope": "string",
    "spend_profile": {"total_annual": "string", "breakdown": {}},
    "current_suppliers": [{"name": "string", "spend_share": "string", "contract_status": "string"}],
    "cost_drivers": [{"driver": "string", "type": "string", "buyer_influence": "string"}],
    "sourcing_levers": [{"lever": "string", "estimated_value": "string", "ease": "string"}],
    "contract_posture": "string"
  },
  "handoff_summary": {
    "for_skill": "p9t-supplier-longlist",
    "key_inputs": {
      "market_structure_summary": "string — concise description of supply market shape and concentration",
      "price_benchmarks": {"driver": "string — key cost driver and indicative range"},
      "must_have_criteria": ["string — criteria derived from category baseline to filter candidates"]
    },
    "flags": ["string — concentration risks, data gaps, or baseline limitations to carry forward"],
    "assumptions_to_carry_forward": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — what is directly provided by the user or drawn from internal records
- **inference** — what is reasoned from available data
- **assumptions** — what is taken as given without verification

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/workflow/` — routing context

### Writes to
`~/sourcing-projects/[project-id]/S1-intake/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-category-baseline.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- cost-drivers.md
- baseline-summary.md
