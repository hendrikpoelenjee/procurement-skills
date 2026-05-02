<!-- SPDX-License-Identifier: Apache-2.0 -->

# Artifact naming contract (per skill)

This standard prevents **machine-unreliable drift** between different parts of the same skill: YAML front matter, prose sections, JSON examples, sample assets, and the Artifact Contract footer.

---

## Why drift happens

Skills are edited over time by different people or passes. Common failure modes:

1. **Renaming in one place only** — e.g. `review-result.json` is chosen for `primary_artifacts`, but an older draft still lists `findings.json` under “Typical outputs”.
2. **Copy-paste from another skill** — filenames survive from a template that does not match this skill’s contract.
3. **“Typical outputs” treated as informal** — treated as rough prose while `Expected outputs` is treated as canonical; both are consumed by agents and should match.
4. **Optional or future files** — e.g. `routing.json` imagined for a later version but never added to `primary_artifacts` or `Expected outputs`.
5. **Path style mixing** — `artifacts/foo.json` in one section vs `foo.json` in another without stating the same project root + stage folder (see [artifact-placement.md](artifact-placement.md)).

Any mismatch breaks: orchestration handoffs, automated validation, grep-based audits, and agent behaviour (“write the wrong file”).

---

## Single source of truth (priority order)

For each skill, **one logical set of on-disk filenames** must appear everywhere. Resolve conflicts using this order:

| Priority | Location | Role |
|----------|----------|------|
| 1 | `metadata.primary_artifacts` in `SKILL.md` front matter | Declared deliverables for tooling |
| 2 | `# Expected outputs` in `SKILL.md` | Human-readable mirror of (1); must list the **same** paths |
| 3 | `# Output contract` JSON example — `artifacts` array | Runtime return shape; must list the **same** paths |
| 4 | `assets/sample-output.json` (if present) | Illustrative; must use the **same** logical artifact names |
| 5 | `## Artifact Contract` → **Typical outputs** | Basenames under the skill’s **Writes to** folder; must match (1)–(3) as basenames |

If you change a filename, update **all** of the above in the same change.

---

## Rules

1. **No orphan filenames** — If a filename appears under “Typical outputs”, it must also appear in `primary_artifacts` and `Expected outputs` (unless you explicitly mark it as deprecated and remove it everywhere).
2. **No duplicate semantics** — Do not use both `findings.json` and `review-result.json` for the same role; pick one canonical name.
3. **Basename vs path** — `Expected outputs` may use `artifacts/<name>`; “Typical outputs” lists basenames under the canonical folder from Artifact Contract (`Writes to`). They must refer to the **same files**.
4. **Optional outputs** — If an output is truly optional, state it once under a subsection “Optional outputs” and add it to `primary_artifacts` only if you want agents to always emit it; otherwise omit it entirely.
5. **Cross-skill references** — Handoff rules and orchestrator registries must use the same `skill_id` and the same artifact names as the producing skill.

---

## Editor checklist (before merge)

- [ ] `primary_artifacts` = `Expected outputs` = `Output contract` `artifacts` array (same set).
- [ ] “Typical outputs” basenames match those files for the declared `Writes to` folder.
- [ ] `assets/sample-output.json` (if any) does not reference removed or renamed files.
- [ ] Grep the skill folder for old filenames after renames.

---

## Related

- [artifact-placement.md](artifact-placement.md) — project root and stage folders.
- Orchestrator references — `skills/p9t-run-sourcing-workflow/references/handoff-rules.md` and `skill-registry.md` must stay aligned with producing skills.
