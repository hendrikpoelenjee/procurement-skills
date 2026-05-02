<!-- SPDX-License-Identifier: Apache-2.0 -->

# Organisation Sourcing Config — Template

Standing constraints applied across all sourcing projects in this organisation.

The **instance** of this file lives at `~/sourcing-projects/org-config.md` (outside the skills repo, user-maintained).
This template defines the schema and rules for populating it.

The orchestrator (`p9t-run-sourcing-workflow`) reads the instance at session start, if present.
If absent, the orchestrator proceeds without org-level defaults and relies on per-project elicitation.

---

## 1. Approval authority

Define the spend thresholds that determine who must approve before a gate passes.
Used by the orchestrator to set `human_approval_required` and gate assignment at the correct level.

| Spend threshold | Approver role | Gate this applies to |
|---|---|---|
| Below [amount] | [Role] | G1_scope_approval |
| [amount]–[amount] | [Role] | G1 + G4_recommendation_approval |
| Above [amount] | [Role] + [Role] | All gates |

**Rule**: If no approval authority is defined here, the orchestrator defaults to requiring sign-off at every gate regardless of spend.

---

## 2. Standing must-have criteria by category

Criteria that always apply for named categories, regardless of what the individual sourcing brief specifies.
Skills that perform screening (`p9t-supplier-qualification`) load these as baseline mandatory disqualifiers.

| Category | Mandatory criterion | Evidence required | Issuing body |
|---|---|---|---|
| [Category name] | [Criterion] | [e.g., Certificate in scope and in date] | [e.g., Accredited certification body] |

**Rule**: Standing criteria supplement, not replace, brief-specific criteria. If a brief adds criteria, both apply.

---

## 3. Preferred commercial models by category type

Helps `p9t-rfx-pack-builder` select the right pricing template structure without re-eliciting it each time.

| Category type | Preferred model | Notes |
|---|---|---|
| Labour-intensive services | Unit rate | Fixed price only if scope is fully defined and volume is predictable |
| Material-intensive supply | Fixed price or indexed | Include indexation clause for contracts >12 months |
| Technology / SaaS | Subscription or consumption | Require cost breakdown including implementation and support |
| Professional services | Day-rate open book | Require rate card and utilisation reporting |
| Infrastructure / capital | Hybrid (fixed base + variable) | Require milestone payment schedule |

---

## 4. Concentration risk thresholds

Defines when the skills must escalate rather than proceeding with a thin shortlist.

| Condition | Threshold | Required action |
|---|---|---|
| Sole-source shortlist | 1 passing candidate | Always escalate; require documented justification |
| Thin shortlist | [N] passing candidates | Flag; proceed only with documented stakeholder rationale |
| Parent-group concentration | All passing candidates share a parent | Escalate; document group-level risk |
| Geographic concentration | All passing candidates in same production region | Flag as supply chain risk |

---

## 5. Blacklisted / debarred suppliers

Suppliers that must never appear on a shortlist, regardless of category or qualification outcome.
`p9t-supplier-qualification` checks this list before finalising any shortlist.

| Supplier name | Reason | Date added | Review date |
|---|---|---|---|
| [Name] | [Reason — debarment, legal, policy] | [YYYY-MM-DD] | [YYYY-MM-DD] |

**Rule**: Entries here are disqualifiers. They are not weighted criteria. They apply before any scoring.

---

## 6. Preferred suppliers (standing relationships)

Suppliers that have already passed qualification for a category and can be included on a longlist without re-screening, subject to certificate expiry checks.

| Supplier name | Category | Valid until | Notes |
|---|---|---|---|
| [Name] | [Category] | [YYYY-MM-DD] | [e.g., ISO certificate expires YYYY-MM] |

**Rule**: Preferred status does not guarantee shortlisting. Mandatory disqualifiers still apply. Certificate expiry must be checked before each use.

---

## 7. Standing data gaps and known unknowns

Organisational constraints that are known to be missing or unavailable and should be declared as data gaps in every project where they are relevant.

| Gap | Affected skills | Impact |
|---|---|---|
| [e.g., No central spend data system] | category-baseline | Spend profile will always be LOW confidence until resolved |
| [e.g., No formal contract register] | award-recommendation | Contract posture must be confirmed manually each project |

---

## Usage rules for the orchestrator

1. Read this file at the start of every session, before Step 0 precondition routing
2. Apply standing criteria silently — do not re-elicit what is already defined here
3. Flag any conflict between org-config defaults and brief-specific requirements before proceeding
4. If the file does not exist, declare `org_config_loaded: false` in the workflow plan and proceed without defaults
5. Never treat org-config as overriding a brief — it supplements; it does not replace
