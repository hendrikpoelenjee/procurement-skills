---
name: p9t-supplier-longlist
description: Create a credible supplier longlist with rationale, evidence, and fit
  against the sourcing brief.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: Requires local file access. Optional web access. Works via adapter
  overlays for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: 0.1.0
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
  - artifacts/p9t-supplier-longlist.json
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
allowed-tools: Read Bash(git:*) WebSearch WebFetch
---

> **Interaction Standard:** This skill follows [Guided Execution Mode](../../standards/interaction-patterns.md).
> Ask ONE question at a time. Wait. Adapt. Signal readiness before executing.

---


# Purpose

Create a credible supplier longlist with rationale, evidence, and fit against the sourcing brief.

# Use when

- The team needs candidate suppliers to explore or invite
- A longlist is needed before qualification or RFx

# Do not use when

- The task is final supplier selection or legal due diligence

# Required inputs

- `category`
- `geography`
- `must_have_criteria`
- `nice_to_have_criteria`
- `market_context`

# Expected outputs

- `artifacts/p9t-supplier-longlist.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Candidates match the brief
- Rationale is explicit
- Duplicates and weak fits are removed

# Procedure

1. Translate the sourcing brief into supplier search criteria.
2. Identify candidate suppliers and capture the evidence for fit.
3. Remove duplicates and weak or irrelevant candidates.
4. Verify candidates via web search (see below).
5. Return a structured longlist with confidence notes and gaps.

### Supplier verification (web)

For each candidate on the initial longlist, use WebSearch to verify:

1. **Trading status** — search "[supplier name] [country]" to confirm the company is actively trading
2. **Relevant certifications** — search "[supplier name] [certification]" (e.g. KIWA, ISO 14001) where certifications are required by the brief or org-config
3. **Product range confirmation** — search "[supplier name] [product category]" to confirm they supply the specified product type

**Rules:**
- If a search returns no results or contradicts the candidate's claimed capability, downgrade that candidate's confidence to LOW and flag in `risk_flags`
- If a search confirms trading status and product range, mark as `web_verified: true` on that candidate
- If web search is unavailable or fails, declare `web_verification_available: false` in the output and set overall confidence to MEDIUM regardless of other inputs
- Do not fabricate URLs. Only record URLs that were actually returned by search results.
- Limit to 1–2 searches per candidate to stay within context budget

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate as understood
- **Scope**: confirm category, geography, and must-have vs. nice-to-have criteria
- **Assumptions**: list key inferences about market accessibility
- **Data gaps**: flag segments expected to have limited public data coverage — coverage gaps lower confidence and must appear in `source_quality`; if fewer than 3 candidates can be identified, escalate before finalising

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

- Market has fewer than 3 qualified candidates (niche or regulated category) → flag before finalising; do not present as a complete market representation
- All identified candidates are subsidiaries of the same parent group → flag group-level concentration risk immediately
- Only large international players exist but the buyer requires local presence → declare geographic coverage gap; do not include candidates that fail the geography criterion
- User insists on including a specific supplier already known to them → include it but note provenance; apply the same evidence standards as all other candidates
- Must-have criteria would eliminate every identified candidate → escalate to user to review criteria before finalising the list

# Epistemic Safety

## Assumptions & Boundaries

- Search criteria derived from the brief are accurate; an incomplete brief will produce an incomplete longlist
- Public sources and market databases are the primary evidence base; non-public supplier data, capabilities, and pricing are excluded
- The longlist is a starting point for qualification; it is not a recommendation to engage or award
- Supplier fit is assessed against the brief as provided; unstated requirements are not captured

## Known Failure Modes

- Including suppliers that match the category name but not the specific requirement or geographic scope
- Missing non-obvious suppliers that operate under different naming conventions or in adjacent market segments
- Over-reliance on well-known brands, excluding credible but less-visible alternatives
- Treating a short longlist as exhaustive when market coverage through available sources is uncertain

## Escalation Triggers

- Fewer than 3 candidates clearly meet the brief → flag before finalising; do not present as a complete market representation
- A significant segment of the market is inaccessible through available search methods → declare as data gap explicitly
- User's must-have criteria would eliminate the entire available market → ask user to review and revise criteria before proceeding

## Confidence Definition

- **HIGH**: Multiple search methods used, results cross-validated, and candidate fit is clearly evidenced per candidate
- **MEDIUM**: Candidates identified from a single source or method; further validation recommended before qualification
- **LOW**: Sparse results or significant market uncertainty; longlist must not drive RFx design or invitations without further research

> If `web_verification_available: false`, maximum confidence is MEDIUM regardless of other inputs — unverified candidate lists cannot be HIGH confidence.

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Search criteria before building the longlist
2. The resulting longlist before passing it to qualification
3. Any candidate where fit is inferred rather than directly evidenced

# References

- `references/screening-guide.md` — How to interpret must-have and nice-to-have criteria.
- `references/sample-candidate-record.md` — Example longlist record.

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": ["artifacts/p9t-supplier-longlist.json", "artifacts/summary.md", "artifacts/open-questions.json"],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — search methods used, sources consulted, and how candidate fit was assessed against the brief",
  "escalation_required": "boolean — true when fewer than 3 candidates meet the brief, all share a parent group, or must-have criteria eliminate the full available market",
  "source_quality": {
    "recency": "LOW | MEDIUM | HIGH",
    "coverage": "LOW | MEDIUM | HIGH",
    "bias_risk": "LOW | MEDIUM | HIGH"
  },
  "data": {
    "candidates": [
      {
        "candidate_id": "string",
        "name": "string",
        "geography": ["string"],
        "category_fit": "string",
        "certifications": [{}],
        "size_indicator": "string",
        "must_haves_met": {},
        "evidence_sources": ["string"],
        "confidence": "HIGH | MEDIUM | LOW",
        "flags": ["string"],
        "notes": "string",
        "web_verified": "boolean — true if trading status and product range confirmed via web search",
        "verification_notes": "string | null — what was found or why verification was skipped"
      }
    ],
    "total_candidates": "integer",
    "excluded_count": "integer",
    "exclusion_reasons": ["string"],
    "web_verification_available": "boolean — false if WebSearch tool was unavailable during execution"
  }
}
```

Outputs MUST separate:
- **evidence** — candidates with direct documented fit against the brief
- **inference** — candidates included based on adjacent category or partial evidence
- **assumptions** — search criteria taken as complete and accurate

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `~/sourcing-projects/[project-id]/S1-intake/` — sourcing brief
- `~/sourcing-projects/[project-id]/S2-market-scan/` — market scan
- `~/sourcing-projects/[project-id]/workflow/` — routing context

### Writes to
`~/sourcing-projects/[project-id]/S3-supplier-longlist/`

### Typical outputs

**Canonical deliverables** (same basenames as `primary_artifacts` / Expected outputs):

- p9t-supplier-longlist.json
- summary.md
- open-questions.json

**Optional supplementary** (same `Writes to` folder — working or illustrative artifacts, not governed by `output.schema.json`):

- screening-rationale.md
