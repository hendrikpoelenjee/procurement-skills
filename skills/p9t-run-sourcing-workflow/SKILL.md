---
name: p9t-run-sourcing-workflow
description: >
  Orchestrate the sourcing workflow, classify complexity, select downstream
  skills, and sequence the work with named human approval gates for simple,
  moderate, and strategic sourcing cases.
license: Apache-2.0
spdx-license-identifier: Apache-2.0
compatibility: >
  Requires local file access. Optional web access. Works via adapter overlays
  for Claude Code and Codex.
metadata:
  owner: portable-sourcing-lab
  version: "0.3.0"
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
    - artifacts/workflow-plan.json
    - artifacts/workflow-routing.json
    - artifacts/summary.md
    - artifacts/open-questions.json
  review_required: true
  human_approval_required: true
  external_input: false
  claude_md_version: ">=0.2.0"
  context_budget:
    skill_md_lines: "<350"
    loaded_references: "<=3 at any time"
    total_tokens_target: "<6000"
allowed-tools: Read Bash(git:*)
---

> **Interaction Standard:** This skill follows [Guided Execution Mode](../../standards/interaction-patterns.md).
> Ask ONE question at a time. Wait. Adapt. Signal readiness before executing.

---


# Purpose

Act as the conductor for the sourcing skill library. Convert a sourcing request into a proportional workflow with explicit stage selection, sequencing, confidence markers, and human-in-the-loop gates.

# Use when

- A user needs end-to-end sourcing support
- The request spans multiple sourcing stages
- The workflow must decide which specialist skills to run
- The task needs proportional governance based on complexity

# Do not use when

- The task is a single narrow step already covered by one specialist skill
- The user already approved a detailed workflow plan and only wants execution of one stage
- The task requires irreversible action or external communication without human approval

# Required inputs

- `business_need`
- `category_or_scope`
- `spend_estimate`
- `timeline`
- `geography`
- `constraints`
- `current_state` — description of the existing supply arrangement, including whether an incumbent supplier exists and contract status
- `stakeholders` (preferred)
- `incumbent_supplier_state` (preferred)

# Expected outputs

- `artifacts/workflow-plan.json`
- `artifacts/workflow-routing.json`
- `artifacts/summary.md`
- `artifacts/open-questions.json`

# Success criteria

- Complexity is classified as `simple`, `moderate`, or `strategic`
- The selected stages are proportional to the case complexity
- Named approval gates are explicit and justified
- Specialist skills are sequenced with clear entry and exit conditions
- The artifact map is complete enough for downstream execution

# Procedure

### Step 0A — Session initialisation

Before anything else, resolve two questions: is this a new project or a resume, and are there standing org-level constraints?

**Path resolution:**

- Read `~/.claude/skills/skills-config.yaml` to get `project_root` and `org_config_path`
- If the file is not found, fall back to defaults: `project_root = ~/sourcing-projects`, `org_config_path = ~/sourcing-projects/org-config.md`
- If the path is also declared in `~/.claude/CLAUDE.md` (injected by install.sh), use that — it is always in context without a tool call

**Resume detection:**

- If the user provides a `project_id` (or one can be inferred from context):
  - Check whether `[project_root]/[project-id]/workflow/workflow-plan.json` exists
  - If it does: load it, read `approval_state` and `next_required_gate`, confirm the resume point with the user, and proceed from that gate — do not restart the workflow
  - If it does not: this is a new project — continue below
- If no `project_id` is provided and the user describes a category or need:
  - Ask whether this is a new project or a continuation before proceeding

**Org-config loading:**

- Check whether `[org_config_path]` exists
- If it does: load it and apply standing approval thresholds, must-have criteria, preferred commercial models, and concentration risk thresholds to this project
- If it does not: declare `org_config_loaded: false` in the workflow plan; elicit per-project defaults through normal intake
- Always surface which defaults were applied — org-config entries can become stale

See `@standards/org-config-template.md` for the schema.

---

### Step 0 — Precondition routing

Before scoring complexity, check for preconditions that must be resolved first.

If stakeholder conflict on objectives is present:
- Select `stakeholder-engagement` as a mandatory Wave 0 precondition skill
- Do not schedule any sourcing workflow stages until alignment is achieved
- Make `G1_scope_approval` dependent on a conflict-resolution artifact

If category boundaries are ambiguous:
- Request refinement of category scope before proceeding
- Optionally select `specification-challenge` as a precondition skill

These preconditions override normal sequencing.

---

1. Normalize the request into a sourcing brief with objective, scope, constraints, and known unknowns.

### Step 1A — Missing input handling

When required inputs are missing, apply the following rule:

- If the request is low-risk, low-spend, and commodity-like:
  - Proceed with documented assumptions
  - Record all assumptions explicitly
- Otherwise:
  - Return `blocked`
  - List missing required inputs in `open_questions`

Always distinguish:
- facts (provided)
- assumptions (inferred)
- unknowns (must be resolved before next gate)

---

2. Score the case using `references/complexity-heuristics.md` and confirm whether it is `simple`, `moderate`, or `strategic`.

---

3. Determine the sourcing path type: `greenfield`, `renewal`, `competitive event`, `rapid scan`, or `negotiation-only`.

### Step 3A — Path-type tiebreakers

If `current_state` and `incumbent_supplier_state` are missing:

- Default to `rapid_scan` for low-spend commodity cases
- Default to `greenfield` when no incumbent signal exists
- Default to `competitive_event` when replacement language is present
- Default to `negotiation_only` only when sole-source is explicit

Always flag missing state data in `open_questions`.

---

4. Use the routing matrix in `references/handoff-rules.md` to select only the necessary specialist skills.

---

5. Build the workflow in waves. Do not schedule later-wave skills unless their prerequisites are met or explicitly waived.

---

6. Insert the correct human approval gates based on complexity and path:

Gate selection rules:

- `simple` → `G1_scope_approval`
- `moderate` → `G1_scope_approval`, `G4_recommendation_approval`
- `strategic` → `G1_scope_approval`, `G2_market_and_longlist_approval`, `G3_rfx_and_evaluation_approval`, `G4_recommendation_approval`
- `negotiation_only` → `G1_scope_approval`, `G4_recommendation_approval`

Do not include unnecessary gates.

---

7. For each selected stage, define:
   - objective
   - trigger to start
   - required inputs
   - expected artifacts
   - exit criteria
   - owner (`agent` or `human`)

---

8. Write a concise workflow summary for the user and a structured routing plan for the runtime.

---

9. Stop at the next required approval gate.

For new engagements:
- Always halt at `G1_scope_approval` unless scope is already explicitly approved.

## Readiness Check

When objective, scope, and key constraints are confirmed, state:

> "I have enough to proceed."

Then confirm before executing:
- **Objective**: restate the sourcing need as understood
- **Scope**: confirm category, spend estimate, and stakeholder alignment status
- **Assumptions**: list key inferences used in complexity scoring
- **Data gaps**: flag inputs that were estimated or inferred; these affect routing reliability

# Operating rules

## Context discipline

- Prefer targeted context over full transcripts.
- Load referenced files only when needed.
- Keep the conductor focused on routing, sequencing, and governance rather than doing specialist analysis itself.

## Tool discipline

- Use only the minimum tools required for planning and routing.
- Treat tool failures as explicit failures.
- Never claim a shell or file action succeeded without evidence.

## Quality discipline

- Distinguish facts, assumptions, and recommendations.
- State why each stage was selected or skipped.
- Prefer the minimum viable sourcing workflow that still manages risk.
- Escalate to human review when commercial, legal, or implementation risk rises materially.

# Failure policy

Stop and return `blocked` when:
- required input is missing and no safe assumption is possible
- the complexity cannot be scored with reasonable confidence
- a required tool is unavailable
- validation fails after the allowed retries
- the task would require a prohibited or irreversible action without approval

When blocked, return:
- what was completed
- what failed
- what input or approval is needed next
- the minimum restart point

# Edge cases

| Edge case | Disposition | Required action |
|----------|------------|----------------|
| Stakeholder conflict on objectives | Block + precondition | Run stakeholder-engagement first; G1 depends on alignment |
| One-bidder / incumbent-only | Escalate | Document sole-source justification; require human review |
| Ambiguous category boundaries | Block | Request category clarification |
| Unrealistic timelines | Escalate | Flag risk; require timeline validation |
| Missing supplier evidence | Block | Request market validation or supplier data |
| High spend, low switching risk | Continue with caution | Validate commercial leverage assumptions |
| Low spend, high criticality | Escalate | Treat as moderate/strategic for governance |

# Epistemic Safety

## Assumptions & Boundaries

- The business need described reflects the actual sourcing situation; undisclosed constraints or political context are out of scope
- Complexity scoring is a routing recommendation, not a binding governance decision; human confirmation is required before execution
- This skill orchestrates only; it does not perform the specialist analysis done by downstream skills
- Downstream skill outputs are only as reliable as their inputs; this skill cannot validate their substantive quality

## Known Failure Modes

- Underestimating complexity, leading to under-governed workflows with insufficient human approval gates
- Overestimating complexity, imposing unnecessarily heavy processes on simple or commodity cases
- Routing decisions that do not account for time pressure or resource constraints in the actual team
- Treating the workflow plan as final when scope approval (G1) has not yet been obtained
- Starting a new project when the user intended to resume an existing one — this restarts gates that have already been approved and discards prior decisions
- Applying org-config defaults silently without confirming they are still current — org-config entries can become stale; always surface what was applied so the user can correct it

## Escalation Triggers

- Stakeholder conflict on objectives is present → run precondition resolution before any sourcing stages; do not proceed
- Sole-source or single-bidder situation → require explicit written justification and human approval before proceeding
- Required inputs for complexity scoring are missing and the case is not clearly low-risk commodity → return blocked
- An approval gate is overdue without explanation → flag and pause the workflow

## Confidence Definition

- **HIGH**: All required inputs provided, complexity is unambiguous, routing is deterministic from the heuristics model
- **MEDIUM**: Some inputs inferred; routing is sound but assumptions are visible and must be confirmed at G1
- **LOW**: Critical inputs missing; routing is provisional; workflow must not proceed past G1 without explicit user confirmation

## Human-in-the-Loop Protocol

Pause and ask the user to confirm:
1. Complexity rating and workflow plan before any specialist skill is executed
2. Halt at every defined approval gate; do not auto-proceed past any gate under any circumstance
3. Any edge case not covered by routing rules → escalate to the user; do not apply a default silently

# References

- `references/complexity-heuristics.md`
- `references/handoff-rules.md`
- `@standards/org-config-template.md` — schema for the org-level config file read at session start

# Output contract

Return a structured result with this shape:

```json
{
  "status": "completed | blocked | failed",
  "summary": "string",
  "artifacts": [
    "artifacts/workflow-plan.json",
    "artifacts/workflow-routing.json",
    "artifacts/summary.md",
    "artifacts/open-questions.json"
  ],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "next_action": "string",
  "data_gaps": ["string"],
  "risk_flags": ["string"],
  "confidence_level": "LOW | MEDIUM | HIGH",
  "reasoning_trace": "string — how the brief was interpreted, complexity scored, path type selected, and stages sequenced",
  "escalation_required": "boolean — true when stakeholder conflict is present, complexity cannot be scored reliably, or an approval gate is overdue",
  "session_context": {
    "resume_detected": "boolean — true when an existing workflow-plan.json was found and loaded",
    "resumed_from_gate": "string | null — gate name if resuming; null if new project",
    "org_config_loaded": "boolean — true when ~/sourcing-projects/org-config.md was found and applied",
    "org_config_overrides": ["string — list of defaults applied from org-config"]
  },
  "data": {
    "complexity": "simple | moderate | strategic",
    "path_type": "greenfield | renewal | competitive_event | rapid_scan | negotiation_only",
    "selected_skills": ["string"],
    "gates": ["string"]
  }
}
```

Outputs MUST separate:
- **evidence** — inputs explicitly provided and used in complexity scoring
- **inference** — path type and routing decisions derived from the scoring model
- **assumptions** — inputs estimated or inferred when not provided
```

---

## Conductor-Specific Project Folder Governance

@standards/artifact-placement.md

This skill is responsible for establishing, reusing, and maintaining the canonical project root for the workflow.

Unless the user explicitly specifies another root path, all user-facing project artifacts MUST be written under:

`[project_root]/[project-id]/`

where `project_root` is read from `~/.claude/skills/skills-config.yaml` (default: `~/sourcing-projects`).

If the project root has already been established in the current workflow or prior context, reuse it and do not redefine it.

This skill MUST:
- establish or reuse the canonical `project-id`
- establish or reuse the canonical project root
- ensure all downstream skills write into the same root
- route artifacts into the correct canonical stage folder
- prevent duplicate, scattered, or conflicting artifact placement
- preserve read/write continuity across workflow stages

---

## Artifact Contract

@standards/artifact-placement.md

### Reads from
- `[project_root]/[project-id]/S1-intake/` — brief and baseline
- `[project_root]/[project-id]/workflow/` — prior routing and gate state

### Writes to
`[project_root]/[project-id]/workflow/`

### Typical outputs
- workflow-plan.json
- workflow-routing.json
- summary.md
- open-questions.json
