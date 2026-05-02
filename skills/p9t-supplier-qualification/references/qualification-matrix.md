<!-- SPDX-License-Identifier: Apache-2.0 -->

# Qualification Matrix

Pass/fail and weighted qualification patterns. Use this reference to structure the screening logic applied to a supplier longlist.

---

## Qualification structure

Qualification operates in two layers:

1. **Mandatory disqualifiers** (pass/fail): applied first. Failure on any one disqualifies the candidate regardless of weighted scores.
2. **Weighted criteria** (scored): applied only to candidates that pass the mandatory layer.

---

## Layer 1 — Mandatory disqualifiers

| Category | Example criteria |
|---|---|
| Legal / financial | Insolvency, administration, or winding-up in the last 3 years |
| Regulatory | Lacking a mandatory certification or licence for the category |
| Sanctions / debarment | Listed on a national or EU debarment register |
| Financial threshold | Annual revenue below the stated minimum for the category |
| Geographic | No operational presence in the required geography |
| Conflict of interest | Undisclosed relationship with the buyer organisation |

**Rule**: Mandatory disqualifiers must be confirmed with the user before screening begins. Do not apply assumptions about what constitutes a disqualifier.

**Rule**: Disqualify on evidence of a disqualifying condition — not on absence of evidence of compliance. If evidence is missing, escalate as "unverified" rather than applying a disqualification ruling.

---

## Layer 2 — Weighted criteria

### Typical dimensions and weights

| Dimension | Simple category | Complex / strategic category |
|---|---|---|
| Financial stability | 20% | 20% |
| Relevant sector experience | 30% | 20% |
| Capability and capacity | 25% | 25% |
| References | 15% | 15% |
| ESG / sustainability | 10% | 10% |
| Innovation / value-add | — | 10% |

Weights must sum to 100% for the weighted layer. Weights must be confirmed with stakeholders before screening begins.

### Scoring scale (weighted layer)

| Score | Meaning |
|---|---|
| 3 | Criterion fully met — strong, evidenced |
| 2 | Criterion partially met — some evidence; gaps present |
| 1 | Criterion weakly met — limited evidence; concerns noted |

---

## Borderline handling protocol

A borderline candidate is one that:
- Passes the mandatory layer but scores within 5% of the pass threshold in weighted scoring
- Has a "Pending" verdict on one or more evidence items that are critical to the weighted score
- Triggers a stakeholder concern that has not been formally documented

**Protocol**:
1. Do not remove borderline candidates silently
2. Present them separately as "borderline — requires human review"
3. Do not apply judgment calls in place of stakeholder decision
4. Document the specific reason for borderline status in the candidate record

---

## Concentration risk detection

Flag and escalate when:
- Only one candidate passes qualification → sole-source risk before any RFx
- Passing candidates are all subsidiaries of the same parent group → group-level concentration risk
- All passing candidates share a geographic dependency (e.g., same production region) → supply chain concentration

These flags must appear in `risk_flags` and trigger `escalation_required: true`.

---

## Evidence rules

| Evidence type | Accept as | Notes |
|---|---|---|
| Audited financial accounts | Strong evidence | Must be dated within 18 months |
| Companies House / KvK / national register | Strong evidence | Current filing status |
| ISO certificate from accredited body | Strong evidence | Must be in-date and in scope |
| Client reference | Medium evidence | Sector-relevant; independently contactable |
| Supplier self-declaration | Weak evidence alone | Acceptable only as supporting corroboration |

Do not treat a supplier's own marketing materials or website claims as evidence for a mandatory disqualifier criterion.
