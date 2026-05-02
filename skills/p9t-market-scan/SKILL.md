---
name: p9t-market-scan
description: Produce a structured supply market scan covering market structure, supplier
  landscape, cost drivers, risks, and trends.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.2.0
  status: draft
  category: research
  wave: 1
  maturity: draft
  tags:
  - sourcing
  - agents
  - cli
  - research
  output_schema: assets/output.schema.json
  primary_artifacts:
  - artifacts/p9t-market-scan.json
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

Produce a structured supply market scan covering market structure, supplier landscape, cost drivers, risks, and trends.

# Use when

- A sourcing decision needs external market context
- The user needs a quick but structured market view

# Do not use when

- The task is a deep due diligence or final legal/compliance review

# Required inputs

- `category`
- `geography`
- `constraints`
- `known_suppliers`
- `time_horizon`

# Expected outputs

- `artifacts/p9t-market-scan.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Market structure is described
- Supplier landscape is mapped
- Cost and risk drivers are visible
- Sources are noted

# Procedure

1. Define the market lens: product, service, geography, and time horizon.
2. Map market structure, major segments, and relevant supplier groups. Load `references/market-forces.md` to ensure all structural dimensions are covered — concentration, entry barriers, substitutes, and power balance.
3. Search for suppliers using the methodology in `references/search-patterns.md`. Apply the cross-validation protocol; do not rely on a single source tier.
4. Identify cost drivers, trends, constraints, and risk signals.
5. Summarize findings in a sourcing-oriented market scan. Record `source_quality` ratings based on what was found, not what was hoped for.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm category, geography, and time horizon
- **Assumptions**: list key inferences about market boundaries
- **Data gaps**: flag where web access is limited and training-data cutoff may affect currency — if primary market data is unavailable, set confidence to LOW or INSUFFICIENT_DATA and set `escalation_required: true`; do not proceed with a fabricated landscape

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

- Category is highly fragmented with no dominant suppliers → declare coverage gap explicitly; do not present a partial list as representative
- Market is dominated by a single supplier → flag concentration risk immediately; this finding shapes the entire sourcing strategy
- Knowledge cutoff means recent entrants or M&A are unknown → declare as data gap; label all landscape findings with effective date
- Category scope spans geographies with structurally different supply markets → confirm operative boundary before scanning; do not blend incomparable markets
- No reliable public data found after targeted search → return `INSUFFICIENT_DATA`; do not fabricate plausible-sounding output

# Epistemic Safety

## Assumptions & Boundaries

- Input data reflects market conditions at the time of the scan; this is a point-in-time view
- Category boundaries described by the user are commercially meaningful and will not be redefined without asking
- Published supplier lists are indicative, not exhaustive; fragmented markets will have gaps
- Web access results reflect publicly indexed content only; non-public pricing, contracts, and capacity data are excluded

## Known Failure Modes

- Confusing adjacent or upstream markets with the target category, overstating apparent competition
- Treating a published shortlist as a complete supplier universe when the market is fragmented or niche
- Presenting outdated cost data or pricing benchmarks as current
- Over-confidence in markets with low public data availability — thin evidence produces low-reliability outputs
- Presenting training-data-derived market intelligence as current fact when live web access is unavailable — knowledge cutoff creates a plausible-but-stale picture that may not flag itself as outdated

## Escalation Triggers

- Category scope spans multiple unrelated sub-markets → ask user to confirm the operative boundary before proceeding
- No reliable market data found after targeted search → declare as data gap; do not infer or fabricate
- Regulatory or geopolitical factors dominate but are unverifiable from available sources → surface as risk flag, not finding

## Confidence Definition

- **HIGH**: Multiple independent sources confirm key findings; supplier landscape cross-validated; cost drivers evidenced
- **MEDIUM**: Findings are plausible but based on partial or single-source data; key claims are explicitly labelled
- **LOW**: Limited evidence available; significant inference required; output is indicative only and must not drive decisions without further research
- **INSUFFICIENT_DATA**: Sources or inputs are too thin or contradictory to justify a substantive scan; structured output reflects limits (may pair with blocked/failed status)

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Category scope and geographic boundary before beginning the scan
2. Whether the supplier landscape looks complete before passing results to qualification
3. Any market dynamics that appear counter-intuitive or contradict the user's prior knowledge

# References

- `references/search-patterns.md` — Search patterns for efficient supplier and market discovery.
- `references/market-forces.md` — Prompts for structure, concentration, entry barriers, and power balance.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": [
    "artifacts/p9t-market-scan.json",
    "artifacts/summary.md",
    "artifacts/open-questions.json"
  ],
  "assumptions": ["string"],
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "confidence_level": "LOW | MEDIUM | HIGH | INSUFFICIENT_DATA",
  "reasoning_trace": "string — how conclusions follow from inputs and sources (audit trail)",
  "escalation_required": "boolean — true when confidence is LOW or INSUFFICIENT_DATA, or critical market risks need human adjudication",
  "source_quality": {
    "recency": "LOW | MEDIUM | HIGH",
    "coverage": "LOW | MEDIUM | HIGH",
    "bias_risk": "LOW | MEDIUM | HIGH"
  },
  "data": {},
  "handoff_summary": {
    "for_skill": "p9t-supplier-longlist",
    "key_inputs": {
      "verified_candidates": [
        {"name": "string", "country": "string", "products": ["string"]}
      ],
      "market_flags": ["string — concentration, scarcity, or certification risks"]
    },
    "flags": ["string — low source quality, unverified candidates, or market risks to carry forward"],
    "assumptions_to_carry_forward": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — what is directly sourced or observed
- **inference** — what is reasoned from evidence
- **assumptions** — what is taken as given without verification

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S1-intake/` — sourcing brief and baseline
- `~/sourcing-projects/[project-id]/workflow/` — routing context

### Writes to
`~/sourcing-projects/[project-id]/S2-market-scan/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-market-scan.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- supplier-landscape.md
