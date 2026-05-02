<!-- SPDX-License-Identifier: Apache-2.0 -->

# Procurement Skills — Upgrade & Standardisation Directive (v1)

You are operating inside a structured procurement skills repository.

Your task is to **upgrade the existing skills to production-grade quality**, aligned with system-wide standards for:

* interaction discipline
* epistemic safety
* output reliability
* validation compliance

You MUST operate directly on the repository files.

---

# ✦ Context

This repository implements a **modular procurement execution system**, where each skill:

* represents a discrete capability
* produces structured outputs
* participates in a larger workflow

The system is governed by:

* `CLAUDE.md` → core operating principles
* `standards/interaction-patterns.md` → Guided Execution Mode (v3)
* `standards/epistemic-risk-standard.md` → uncertainty & safety rules
* `tools/validators/validate_skill.py` → structural validation

---

# ✦ Objective

Upgrade all `/skills/p9t-*` skills so they are:

* structurally consistent
* epistemically safe
* compliant with Guided Execution Mode v3
* validator-compliant
* resistant to “persuasive error”

---

# ✦ Non-Negotiable Rules

You MUST:

* preserve each skill’s **core purpose**
* apply **minimal, surgical improvements**
* keep skills **readable and concise**
* avoid duplication of standards
* enforce **uncertainty visibility**

You MUST NOT:

* rewrite skills unnecessarily
* introduce speculative or generic content
* change artifact structure unless required
* modify unrelated files

---

# ✦ Required Upgrades (Apply to EACH skill)

## 1. Epistemic Safety Sections

Ensure each SKILL.md contains:

### Assumptions & Boundaries

* what the skill assumes
* when outputs may be misleading

### Known Failure Modes

* how the skill can be wrong

### Escalation Triggers

* when to pause and ask for user input

### Confidence Definition

* define LOW / MEDIUM / HIGH

### Human-in-the-Loop Protocol

* explicit user validation questions

---

## 2. Interaction Compliance

Ensure alignment with Guided Execution Mode v3:

* one-question-at-a-time
* no upfront forms
* progressive structuring
* readiness signal:

> "I have enough to proceed."

* pre-execution summary:

  * objective
  * scope
  * assumptions
  * data gaps

---

## 3. Output Contract Upgrade

Update output contracts to include:

* assumptions
* data_gaps
* risk_flags
* confidence_level (NOT numeric confidence)
* source_quality (where relevant)

Ensure outputs separate:

* evidence
* inference
* assumptions

---

## 4. Schema Alignment

Update `assets/output.schema.json`:

MUST include:

* confidence_level
* assumptions
* data_gaps
* risk_flags

Ensure:

* schema enforces thinking, not just formatting
* sample-output.json validates against schema

---

## 5. Failure Visibility Rule

Each skill must satisfy:

> If the skill is wrong, a human must be able to detect it.

If not → improve the skill.

---

# ✦ Priority Skills (Upgrade First)

1. p9t-market-scan
2. p9t-supplier-qualification
3. p9t-bid-evaluation-framework
4. p9t-award-recommendation

These have highest decision impact.

---

# ✦ Validation Step (Mandatory)

After modifying each skill:

Run:

```bash
python skills/<skill-name>/scripts/validate.py
```

Ensure:

* PASS result
* no missing required sections
* schema compliance

If FAIL → fix immediately

---

# ✦ Adversarial Review Step

After validation, apply adversarial thinking:

Ask:

* What could make this output wrong?
* Where are assumptions hidden?
* Could this produce a persuasive but incorrect result?

If yes → improve the skill.

---

# ✦ Execution Strategy

For each skill:

1. Read SKILL.md
2. Identify missing epistemic sections
3. Add minimal required sections
4. Align interaction behaviour
5. Upgrade output contract
6. Update schema
7. Validate
8. Apply adversarial check

Repeat until compliant.

---

# ✦ Output Requirement

At the end of your run, produce:

## Summary

* skills upgraded
* key improvements applied

## Files Modified

* list of changed files

## Validation Results

* PASS/FAIL per skill

## Remaining Risks

* what is still imperfect

---

# ✦ Guiding Principle

Do not make the skills more impressive.

Make them:

* harder to misuse
* clearer in uncertainty
* safer in decision support

---

# ✦ System Philosophy

This system does not aim to eliminate error.

It aims to ensure that:

> errors become visible, traceable, and correctable.
