You are operating inside a procurement skills repository.

Phase 1 (skill upgrades) is complete.

Your task is now to **stress-test, validate, and benchmark the skills**.

---

## Objective

Ensure all `/skills/p9t-*` skills are:

* resistant to failure under real-world conditions
* not producing persuasive but incorrect outputs
* clear in uncertainty and assumptions
* safe for decision support

---

## Inputs

Use:

* tools/prompts/adversarial_skill_review.md
* tools/validators/validate_skill.py
* CLAUDE.md
* standards/interaction-patterns.md
* standards/epistemic-risk-standard.md

---

## Tasks

### 1. Adversarial Review

For each skill:

* run adversarial_skill_review.md
* simulate:

  * incomplete inputs
  * conflicting inputs
  * weak or outdated data
  * ambiguous scope
  * marginal decision scenarios

Identify:

* hidden assumptions
* false confidence
* missing escalation triggers
* weak human-in-the-loop behaviour

---

### 2. Failure Detection Check

Verify:

> If this skill is wrong, can a human detect it?

If not → propose fixes.

---

### 3. Output Risk Assessment

Check outputs for:

* false precision
* overconfident conclusions
* missing data gaps
* missing risk flags

---

### 4. Benchmark Against “Gold Standard”

Compare each skill to the strongest example (e.g. upgraded p9t-market-scan).

Assess:

* clarity of reasoning
* visibility of uncertainty
* strength of output contract
* robustness under ambiguity

---

### 5. Validator Coverage Check

Evaluate:

* what validate_skill.py currently catches
* what it misses (especially epistemic risks)

Propose improvements to validator logic.

---

## Output

Return:

### 1. Skill Risk Report

For each skill:

* verdict: PASS / CONDITIONAL / FAIL
* main risks
* failure scenarios
* confidence level

---

### 2. Systemic Weaknesses

* recurring issues across skills
* structural weaknesses in design

---

### 3. Recommended Fixes

* specific skill improvements
* validator enhancements
* standard updates

---

### 4. Priority Actions

List:

* top 3 risks to fix immediately
* top 3 improvements with highest impact

---

## Rules

* be critical, not polite
* do not rewrite skills unless necessary
* focus on failure modes, not polish
* assume real-world messiness

---

## Guiding Principle

Do not assume the system works.

Prove where it breaks — and why.
