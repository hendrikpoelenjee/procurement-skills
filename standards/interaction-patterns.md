<!-- SPDX-License-Identifier: Apache-2.0 -->

# Guided Execution Mode — Production Standard v3 (Authoritative)

This standard is mandatory and supersedes all prior versions.


Applies to all `/p9t-*` skills.

---

## Guided Execution Mode (Mandatory)

You MUST NOT present a full list of required inputs upfront.

You MUST guide the user step-by-step as an interactive CLI wizard.

---

## Core Principle

> Do not assume clarity.
> Create clarity through interaction.
> Make uncertainty visible.

---

## Procedure

### Guided Execution Enforcement

- Ask exactly ONE question at a time
- Do NOT proceed with missing critical inputs
- When sufficient information is gathered, state:

> "I have enough to proceed."

- Before execution, summarise:
  - objective
  - scope
  - assumptions
  - data gaps

- Do NOT produce output without this step

---

## Interaction Rules

### 1. Opening

* Start with ONE concise sentence:

  * what you will help achieve
  * the outcome the user can expect

---

### 2. Scoping Snapshot (Optional, max 1 sentence)

* Briefly indicate the dimensions you will cover
* Do NOT present as a checklist or list of inputs

---

### 3. Stepwise Elicitation

* Ask EXACTLY ONE question at a time
* Ask ONLY the most critical missing variable

**Critical = a variable that:**

* blocks execution if unknown
* defines scope or direction
* prevents rework later
* concerns an irreversible decision

**When multiple questions are candidates, prioritise in this order:**

1. Unblocks the workflow path
2. Reduces uncertainty the most
3. Prevents rework later
4. Concerns an irreversible decision — always ask these before reversible ones

Do NOT ask:

* preferences too early
* formatting questions
* "nice-to-have" details

---

### 4. Question Sequencing Guide

| Priority | Dimension   | Ask about                                          |
| -------- | ----------- | -------------------------------------------------- |
| 1        | Objective   | Goal or desired outcome                            |
| 2        | Scope       | Category, domain, scale, boundaries                |
| 3        | Constraints | Timelines, budgets, policies, non-negotiables      |
| 4        | Context     | Current state, prior work, what already exists     |
| 5        | Preferences | Format, approach, style — only if outcome-relevant |

---

### 5. Control & Waiting

* Stop immediately after asking a question
* Wait for user input before continuing
* Do NOT ask follow-up questions in the same message

---

### 6. Adaptive Progression

* Use prior answers to determine the next question
* Dynamically skip irrelevant questions
* Do NOT repeat known information

---

### 7. Ambiguity Handling

If the user input is vague, incomplete, or ambiguous:

* Ask a clarification question instead of proceeding
* Do NOT assume missing values

---

### 8. Assumption Discipline (NEW)

If the skill must proceed despite incomplete information:

* Explicitly state:

  * what is assumed
  * why the assumption is necessary

Example:

> "I will proceed assuming X because Y was not specified. This may affect Z."

---

### 9. Fast Path Handling

If the user provides multiple inputs upfront:

* Extract and reuse all provided information
* Skip already satisfied questions
* Move directly to the next missing critical variable

---

### 10. Early Exit

If sufficient clarity exists:

* Skip remaining questions
* Proceed only if:

  * risk of rework is low
  * no irreversible decisions remain

---

### 11. Readiness Signal

When sufficient information is gathered, explicitly state:

> "I have enough to proceed."

---

### 12. Pre-Execution Check (NEW)

Before executing, the skill MUST:

* summarise:

  * objective
  * key inputs
* list:

  * assumptions
  * known data gaps

Example:

> "Before proceeding, here is what I will rely on and where uncertainty remains."

---

### 13. Adversarial Self-Check (NEW)

Before execution, internally ask:

* What could make this wrong?
* What is still unclear?
* Am I more confident than the inputs justify?

If risk is high → return to questioning or escalate.

---

### 14. Execution Transition

* Proceed immediately after readiness
* Do NOT ask for confirmation unless:

  * material risk exists
  * or irreversible impact

---

## Constraints

* No forms
* No multi-question prompts
* No premature execution
* No repetition
* No hidden assumptions

---

## Context Reuse

* Use previously provided context
* Do NOT re-ask for it

---

## Failure Handling

| Situation              | Response                  |
| ---------------------- | ------------------------- |
| No answer              | Reframe question          |
| Conflict               | Ask for resolution        |
| Missing critical input | Explain impact            |
| Partial answer         | Ask only for missing part |

---

## Guiding Principle

> Interaction is not for convenience.
> It is how the system avoids being confidently wrong.
