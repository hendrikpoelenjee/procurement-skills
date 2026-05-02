<!-- SPDX-License-Identifier: Apache-2.0 -->

# Skill Frontmatter Standard

Every `SKILL.md` file must open with a YAML frontmatter block enclosed in `---` delimiters.
This block is the machine-readable identity and governance contract for the skill.

---

## Canonical Structure

```yaml
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
```

---

## Field Reference

### Top-level fields

| Field | Required | Description |
|---|---|---|
| `name` | yes | Skill identifier. Must match the folder name exactly. |
| `description` | yes | One or two sentences. What the skill produces. No marketing language. |
| `license` | yes | Always `Apache-2.0` unless explicitly overridden. |
| `spdx-license-identifier` | yes | Always `Apache-2.0`. Required for SPDX compliance tooling. |
| `compatibility` | yes | State file access requirements and any provider adapter notes. |
| `allowed-tools` | yes | Whitelist of tools the skill may invoke. Be minimal. |

### `metadata` fields

| Field | Required | Description |
|---|---|---|
| `owner` | yes | Team or individual responsible for this skill. |
| `version` | yes | Semantic version (`MAJOR.MINOR.PATCH`). Must increment on each meaningful change. |
| `status` | yes | Lifecycle state. See lifecycle rules below. |
| `category` | yes | Functional grouping: `research`, `selection`, `decision`, `execution`, `review`. |
| `wave` | yes | Sourcing workflow stage (integer). Defines sequencing in `p9t-run-sourcing-workflow`. |
| `maturity` | yes | `draft`, `review`, or `production`. Must match `status` intent. |
| `tags` | yes | Array of lowercase strings. Include at minimum: `sourcing`, and the runtime environment(s). |
| `output_schema` | yes | Relative path to the JSON Schema file. Always `assets/output.schema.json`. |
| `primary_artifacts` | yes | List of output file paths the skill is expected to produce. |
| `review_required` | yes | Boolean. Whether human review is required before output is used. |
| `human_approval_required` | yes | Boolean. Whether formal approval sign-off is required before proceeding. |
| `external_input` | yes | Boolean. Set `true` if the skill ingests content from external documents or suppliers. Triggers input-trust rules. |
| `claude_md_version` | yes | Minimum CLAUDE.md version this skill is compatible with. Format: `">=X.Y.Z"`. |
| `context_budget` | yes | Declared context footprint. Enforced by `tools/validators/context_budget_checker.py`. |

### `context_budget` sub-fields

| Field | Description |
|---|---|
| `skill_md_lines` | Maximum line count for this `SKILL.md`. Target `<200`; hard limit `400`. |
| `loaded_references` | Maximum number of reference files loaded into context simultaneously. |
| `total_tokens_target` | Target total token footprint for skill context. |

---

## Lifecycle States

`status` must be one of:

| Value | Meaning | Constraints |
|---|---|---|
| `draft` | Under development | Not for use in real decisions |
| `review` | Passed structural validation | Pending epistemic and logic review |
| `production` | Fully validated | Requires passing validation run in `validation_log.md` |
| `deprecated` | Superseded | Add `replaces` field pointing to the successor skill |

---

## Rules

1. **`name` must match the folder name.** Mismatches cause validator failures.
2. **`version` must increment** on every meaningful change to the skill's behaviour or output contract.
3. **`status: production`** requires a logged passing validation run in `@tools/validators/validation_log.md`.
4. **`human_approval_required: true`** must be set for any skill whose output directly triggers an award, contract, or financial commitment.
5. **`external_input: true`** must be set if the skill reads supplier submissions, contract PDFs, or any user-uploaded documents. This activates input sanitisation per `@standards/input-trust.md`.
6. **`allowed-tools`** must be the minimum necessary. Do not whitelist tools speculatively.
7. **`context_budget`** is a declaration, not a suggestion. Skills that cannot operate within budget must be redesigned, not given a larger budget.

---

## What NOT to put in frontmatter

- Business logic or decision rules — these belong in the skill body
- Full output schema definitions — reference `assets/output.schema.json`
- Interaction patterns — reference `@standards/interaction-patterns.md`
- Epistemic rules — reference `@standards/epistemic-risk-standard.md`
