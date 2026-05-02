# skill-registry.md

## Purpose

Provide a local registry of specialist skills known to the sourcing library.

The orchestrator may only reference skills present here or explicitly defined in `handoff-rules.md`.

## Registry format

| skill_id | primary_role | typical_wave | trigger_condition |
|---|---|---:|---|
| `p9t-intake-and-brief` | intake normalization | 1 | Any sourcing workflow requiring formal brief creation |
| `p9t-category-baseline` | baseline / strategy input | 1 | Case needs spend/category baseline before market action |
| `p9t-market-scan` | market scan | 1 | Early market visibility needed |
| `p9t-supplier-longlist` | supplier discovery / longlist | 2 | Competitive event requires supplier options |
| `p9t-supplier-qualification` | supplier qualification | 2 | Strategic or qualification-heavy events |
| `p9t-rfx-pack-builder` | RFx design | 3 | Competitive event requires formal RFx package |
| `p9t-bid-evaluation-framework` | evaluation design | 3 | Competitive event needs structured scoring |
| `p9t-negotiation-prep` | negotiation preparation | 4 | Renewal, negotiation-only, or post-evaluation negotiation |
| `p9t-award-recommendation` | award / recommendation output | 4 | Final recommendation required |
| `p9t-complexity-triage` | complexity classification and governance calibration | 1 | Run after intake to classify simple/moderate/strategic complexity and set review/gate intensity |
| `p9t-output-review` | output quality assurance and handoff readiness review | 4 | Run when stage outputs must be checked for completeness, schema fit, contradictions, and handoff readiness |
| `p9t-run-sourcing-workflow` | workflow orchestrator and gate controller | 0 | Use for end-to-end sourcing requests requiring stage selection, sequencing, and approval-gate control |

## Registry rules

- If a skill is not listed here and not explicitly defined in `handoff-rules.md`, the orchestrator must not invent or select it.
- If a listed skill is missing from the filesystem, return `blocked` with `unknown_skill`.
- Keep this registry synchronized with the installed skill directories (e.g. `~/.claude/skills/` for Claude Code, `~/.agents/skills/` for OpenAI Codex user skills).

## Maintenance note

When adding a new specialist skill, update:
1. `skill-registry.md`
2. `handoff-rules.md` if the skill is routable from the orchestrator
3. any collection-level validation assets if used
