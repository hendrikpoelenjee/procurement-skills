<!-- SPDX-License-Identifier: Apache-2.0 -->

<!--
  Merge this block into your repository root AGENTS.md (or AGENT.md if that is
  your project convention). It complements Codex skills: skills supply workflows;
  AGENTS.md supplies project-specific rules. Codex provider stubs in this repo
  note: respect project-level AGENTS.md when present.
-->

## TPO procurement skills (optional)

If this repo uses the [TPO procurement skills](https://github.com/theprocurementoffice/procurement-skills) (installed under `~/.agents/skills/` or checked in under `.agents/skills/`):

- Prefer **Guided Execution Mode**: `~/.agents/standards/interaction-patterns.md` (or `../standards/` relative to the skill folder when using a local clone).
- Write project artifacts under `~/sourcing-projects/[project-id]/` per `artifact-placement.md`, unless the user sets another root.
- Do not contradict each skill’s stated output contract in `SKILL.md`.
