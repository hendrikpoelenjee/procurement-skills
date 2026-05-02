<!-- SPDX-License-Identifier: Apache-2.0 -->

# Skill Registry Gap Analysis

Scope: `skills/p9t-run-sourcing-workflow/references/skill-registry.md`

Purpose: document mapping errors between the registry, the actual skill contracts, and the conductor routing references.

---

## Executive Summary

The current registry has three material integrity issues:

1. `p9t-complexity-triage` is mispositioned (wrong wave and weak trigger wording).
2. `p9t-output-review` is misclassified (wrong role and wrong trigger).
3. `p9t-run-sourcing-workflow` row is incomplete (missing trigger condition and no explicit "entrypoint" semantics).

These do not only create documentation drift; they can cause incorrect routing assumptions and maintenance mistakes when new contributors treat the registry as the source of truth.

---

## Detailed Mismatches

## 1) `p9t-complexity-triage` mapping drift

Current registry row:

`| p9t-complexity-triage |  | 3 | Strategic, transformation, or high-risk supplier cases |`

Why this is inconsistent:

- The skill metadata sets `wave: 1` and category `orchestration`.
- The skill purpose says it is used early to classify complexity and recommend workflow intensity.
- The handoff matrix places `p9t-complexity-triage` immediately after intake in every path variant.

Broken links:

- Registry wave (`3`) conflicts with skill metadata wave (`1`).
- Trigger text implies selective usage ("strategic/transformation/high-risk"), but routing uses it as a default early-stage classifier across simple/moderate/strategic paths.
- Empty `primary_role` removes intent for maintainers and for any future validation script.

Operational risk:

- New maintainers may schedule triage too late.
- Future "wave-aware" automation could incorrectly skip or delay complexity assessment.

---

## 2) `p9t-output-review` role/trigger mismatch

Current registry row:

`| p9t-output-review | stakeholder alignment | 0 | Stakeholder conflict or alignment dependency |`

Why this is inconsistent:

- The skill purpose is QA/governance review: completeness, schema fit, contradictions, unsupported claims, handoff readiness.
- Skill metadata category is `governance`, not stakeholder alignment.
- Handoff rules route this skill as a downstream quality gate/review stage, typically final in path sequences, not a Wave 0 precondition.
- Stakeholder conflict precondition in conductor step 0 explicitly references `stakeholder-engagement`, not `p9t-output-review`.

Broken links:

- `primary_role` points to the wrong capability domain.
- `trigger_condition` references conflict alignment handling that belongs to a different skill family.
- `typical_wave` of `0` conflicts with observed routing position (end-of-flow review step).

Operational risk:

- Contributors may invoke `p9t-output-review` as a precondition for alignment issues.
- Quality review may be underused or incorrectly replaced by alignment tasks.

---

## 3) `p9t-run-sourcing-workflow` incomplete registry row

Current registry row:

`| p9t-run-sourcing-workflow | orchestrator | 0 |   |`

Why this is incomplete:

- Empty trigger condition means the row is not actionable as a lookup contract.
- The registry purpose says the orchestrator may only reference skills in this table; if the table is policy, each row should have a deterministic trigger.
- The row does not explicitly state that this skill is the routing authority and project-root authority for artifact governance.

Broken links:

- Missing trigger weakens registry completeness and validation potential.
- Missing governance semantics hides a critical dependency on artifact placement discipline.

Operational risk:

- Ambiguous startup criteria for when to invoke the conductor vs direct specialist skills.
- Harder to automate checks that enforce table completeness.

---

## Secondary Integrity Note (adjacent)

The conductor references precondition skills (`stakeholder-engagement`, optional `specification-challenge`) in step 0. These are not part of this TPO bundle and are not listed in this registry.

This is not necessarily wrong, but it should be explicitly marked as "external dependency" behavior in registry governance to prevent confusion.

---

## Recommended Corrected Rows

Use these rows to replace the problematic entries:

| skill_id | primary_role | typical_wave | trigger_condition |
|---|---|---:|---|
| `p9t-complexity-triage` | complexity classification and governance calibration | 1 | Run after intake to classify simple/moderate/strategic complexity and set review/gate intensity |
| `p9t-output-review` | output quality assurance and handoff readiness review | 4 | Run when stage outputs must be checked for completeness, schema fit, contradictions, and handoff readiness |
| `p9t-run-sourcing-workflow` | workflow orchestrator and gate controller | 0 | Use for end-to-end sourcing requests requiring stage selection, sequencing, and approval-gate control |

Notes:

- Keep `typical_wave` as guidance, not a hard enforcement rule.
- If you keep wave numbers strict, map `p9t-output-review` to the final wave used by your common paths (often `4`).

---

## Suggested Governance Rule Additions

To prevent recurrence, add these checks to registry maintenance:

1. No blank `primary_role` or `trigger_condition` fields.
2. `typical_wave` must not contradict a skill's `metadata.wave` unless explicitly marked `multi-wave`.
3. `primary_role` wording must align with skill `Purpose`.
4. Trigger wording must align with conductor references (`handoff-rules.md` + precondition logic in conductor `SKILL.md`).
5. External dependency skills (not in bundle) must be tagged as `external`.

---

## Optional Follow-up

After updating `skill-registry.md`, run a short consistency sweep against:

- `skills/p9t-run-sourcing-workflow/references/handoff-rules.md`
- `skills/*/SKILL.md` (Purpose, metadata.wave, category)
- any future validation script using the registry as policy input

