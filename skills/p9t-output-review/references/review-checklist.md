<!-- SPDX-License-Identifier: Apache-2.0 -->

# Review Checklist

Standard review checklist for sourcing skill outputs. Structured in four layers: schema compliance, epistemic safety, internal consistency, and handoff readiness.

Apply in order. A failure in any layer is a FAIL — do not continue to the next layer and issue a PASS.

---

## Layer 1 — Schema compliance

| Check | Pass condition |
|---|---|
| `status` present | One of: `completed`, `blocked`, `failed` |
| `summary` present | Non-empty string |
| `artifacts` present | Non-empty array; paths are plausible |
| `assumptions` present | Array present (may be empty for simple outputs) |
| `data_gaps` present | Array present (may be empty) |
| `risk_flags` present | Array present (may be empty) |
| `confidence_level` present | One of: `LOW`, `MEDIUM`, `HIGH`, `INSUFFICIENT_DATA` |
| `reasoning_trace` present (where required) | Non-empty string |

**FAIL immediately if any required field is absent.**

---

## Layer 2 — Epistemic safety

| Check | Pass condition |
|---|---|
| Confidence vs. data_gaps | `HIGH` confidence with non-empty `data_gaps` requires explicit justification in `reasoning_trace`. No justification = FAIL. |
| Confidence vs. status | `INSUFFICIENT_DATA` confidence must be paired with `status: blocked` or `status: failed`. |
| Assumptions are visible | Inferences presented as facts = FAIL. Assumptions must be labelled. |
| Evidence / inference / assumption separation | Output separates what is sourced, what is reasoned, and what is taken as given. |
| Risk flags populated when risk exists | A HIGH-risk output with empty `risk_flags` = FAIL. |

---

## Layer 3 — Internal consistency

| Check | Pass condition |
|---|---|
| Summary vs. risk_flags | Summary cannot state "no risks identified" if `risk_flags` is non-empty. |
| Summary vs. confidence_level | Summary tone must match confidence level — a confident narrative with `LOW` confidence = flag for review. |
| Assumptions vs. open_questions | Items listed as assumptions must not also be listed as open questions requiring resolution. |
| Artifacts vs. expected outputs | Artifacts listed in output must match the skill's declared `primary_artifacts`. |
| Recommendation vs. gate status | No recommendation should state "proceed to next stage" if an approval gate has not been confirmed. |

---

## Layer 4 — Handoff readiness

| Check | Pass condition |
|---|---|
| Gate cleared | The required gate for this workflow stage is confirmed — not assumed. |
| Open questions resolved | No blocking open questions remain unresolved. |
| Next action is specific | `next_action` names a concrete step and an owner, not just "proceed". |
| Escalation_required | Set to `true` if any risk or gap would affect the downstream skill's ability to operate safely. |

---

## Verdict protocol

- **PASS**: all four layers pass; handoff may proceed.
- **FAIL**: one or more checks fail; artifact must be returned to originating skill with the specific finding noted.
- **CONDITIONAL PASS**: reviewable gaps exist but are documented and acknowledged. Use only for minor non-blocking issues where the downstream stage can still operate safely. Must be logged with the specific condition.

**The reviewer does not correct the artifact.** The reviewer returns it with findings. Correction is the originating skill's responsibility.
