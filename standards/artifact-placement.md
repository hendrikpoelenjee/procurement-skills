<!-- SPDX-License-Identifier: Apache-2.0 -->

# Artifact Placement Standard

Applies to all skills that create, update, or rely on project artifacts.

---

## Purpose

All project artifacts MUST be written into a single project folder so that:
- outputs are predictable
- stage deliverables remain grouped together
- downstream skills can find prior artifacts reliably
- the user always knows where project files are stored

Random, temporary, implicit, or skill-local output paths are NOT allowed unless explicitly required for system internals.

---

## Project Root Rule

All user-facing project artifacts MUST be stored under:

`~/sourcing-projects/[project-id]/`

Where:
- `[project-id]` is the canonical project identifier
- the conductor skill is responsible for establishing this identifier if not already defined

If a project root already exists, reuse it.
Do NOT create a second parallel project folder for the same project.

---

## Canonical Stage Folder Convention

Within the project root, artifacts MUST be placed in the appropriate stage folder:

| Path | Contents |
|------|----------|
| `README.md` | Project index, decisions log, next actions |
| `workflow/` | Routing plan, workflow state, approval gates |
| `S1-intake/` | Sourcing brief and intake artifacts |
| `S2-market-scan/` | Market scan and landscape analysis |
| `S3-supplier-longlist/` | Longlist and screening outputs |
| `S4-supplier-qualification/` | Qualification and shortlist outputs |
| `S5-rfq/` | RFQ package and pricing templates |
| `S6-evaluation-framework/` | Evaluation model, criteria, scoring matrix |
| `S7-award/` | Proposal evaluation, recommendation, award pack |

If a skill writes an artifact, it MUST place it in the matching stage folder.

---

## Mandatory Placement Behaviour

Before writing any artifact, the skill MUST:

1. Determine the active `project-id`
2. Determine the correct stage folder
3. Write the artifact into the canonical project folder
4. Reuse existing project structure where present
5. Avoid writing duplicate copies elsewhere

Do NOT:
- scatter artifacts across unrelated directories
- create ad hoc output folders
- store stage outputs beside the skill definition
- invent new folder names when a canonical one already exists

---

## Project ID Rule

If `project-id` is already known from the current workflow, prior conversation context, an existing project path, or a workflow artifact — reuse it.

If no `project-id` exists yet, the conductor skill MUST establish one before downstream artifact creation begins.

---

## Conductor Responsibility

The conductor skill is the authority for:
- setting or confirming the canonical `project-id`
- establishing the project root folder
- ensuring all downstream skills use the same root
- routing outputs into the correct stage folders

Downstream skills MUST inherit the established project root and MUST NOT redefine it independently unless explicitly instructed.

---

## Read/Write Resolution Rule

When reading prior artifacts, skills MUST look first in:

`~/sourcing-projects/[project-id]/`

and then the relevant stage subfolder.

When writing new artifacts, skills MUST write back into that same project root.

This ensures read/write continuity across the workflow.

---

## README Discipline

The root `README.md` SHOULD function as the project index and operating log. When appropriate, update it with:
- artifact inventory
- current stage
- key decisions
- next actions
- blockers or approval gates

---

## Workflow Folder Discipline

The `workflow/` folder SHOULD contain orchestration artifacts such as:
- workflow-plan.json
- routing decisions
- gate status
- handoff notes
- stage progression records

---

## Exception Rule

If the user explicitly instructs another root path, follow the user instruction. In that case:
- treat the user-defined path as the new project root
- keep the same stage folder convention unless the user specifies otherwise

---

## Context Reuse

If the project root has already been established earlier in the conversation, reuse it.
Do NOT ask again.
Do NOT relocate the project unless the user requests it.

---

## Compliance Requirement

Any skill that generates artifacts MUST comply with this standard.

If a skill cannot determine the correct project root or stage folder, it MUST resolve that before writing files. It MUST NOT fall back to an arbitrary directory.

---

## Related standards

- [artifact-naming-contract.md](artifact-naming-contract.md) — **same filenames** across YAML, Expected outputs, Output contract, and “Typical outputs” within each skill.
