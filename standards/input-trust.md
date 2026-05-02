<!-- SPDX-License-Identifier: Apache-2.0 -->

# Input Trust Standard

> **Status: stub — to be authored.**
> This file is referenced by `CLAUDE.md §9` and `standards/skill-frontmatter.md`.
> It must be completed before any skill with `external_input: true` is promoted to `production`.

---

## Purpose

Define how skills must handle untrusted external input — supplier submissions, contract PDFs, RFP documents, and any user-uploaded content.

---

## Scope

Applies to any skill that declares `external_input: true` in its frontmatter.

---

## Sections to author

### 1. Threat Model

- Prompt injection via external documents
- Data exfiltration through crafted inputs
- Confidence manipulation through authoritative-looking but false content

### 2. Sanitisation Rules

- How to strip or isolate untrusted content from trusted context
- What to do when a document contains instructions directed at the model

### 3. Sensitivity Classification

- How to classify input sensitivity level
- What categories of data must not be passed to external tools or logged

### 4. Handling Protocol

- Steps required before processing any external document
- How to flag suspicious content to the user without acting on it

### 5. Skill-Level Declarations Required

- Frontmatter fields that must be set when `external_input: true`
- Review and approval gates that become mandatory

---

## Owner

procurement-engineering

## Related

- `CLAUDE.md §9` — Security & Trust Boundaries
- `standards/skill-frontmatter.md` — `external_input` field definition
