# Changelog

Pack-level summary for **TPO Procurement Skills** (repository root). Individual skills keep their own `skills/p9t-*/CHANGELOG.md` where required by [CLAUDE.md](CLAUDE.md).

All notable changes below are consolidated from work merged into this tree around **2026-05-01** (prior root changelog did not exist).

The format loosely follows [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

(No entries yet.)

---

## [2026-05-01]

### Added

- **Phase 3 — continuous improvement loop** ([spec](tools/prompts/phase_three_cont_improvement_loop.md))
  - [standards/feedback-standard.md](standards/feedback-standard.md) — where and how feedback is stored, trust/redaction expectations.
  - [tools/feedback/feedback.schema.json](tools/feedback/feedback.schema.json) — JSON Schema for a single feedback record.
  - [tools/feedback/sample-feedback.json](tools/feedback/sample-feedback.json) — example payload.
  - [tools/feedback/collect_feedback.py](tools/feedback/collect_feedback.py) — validate append record(s) to project `workflow/feedback.json` (or stage-local path); supports `--dry-run`, object or array input.
  - [tools/prompts/improve_from_feedback.md](tools/prompts/improve_from_feedback.md) — agent prompt for evidence-based minimal patches from aggregated feedback.
- [tools/feedback/summarize_feedback.py](tools/feedback/summarize_feedback.py) — Markdown summary across `workflow/feedback.json` and optional stage-level `*/feedback.json` files.
- [PROGRESS.md](PROGRESS.md) — execution checklist for Phase 3 implementation status (update when extending the loop).
- [CHANGELOG.md](CHANGELOG.md) — this root changelog (first commit to this tree).
- **[CLAUDE.md](CLAUDE.md) §14** — repository, Git, and GitHub boundary rules for agents (no unprompted `git push`, destructive resets, or `gh` merge/publish actions).

### Changed

- **[README.md](README.md)** — rebuilt as a fuller pack guide (quick start Claude/Codex, how-it-works / progressive disclosure, skills matrix, examples, repo layout, standards pointers, validation, Phase 3, uninstall, licence). README structure partly inspired by [Claude-skills-for-Computational-Designers](https://github.com/Amanbh997/Claude-skills-for-Computational-Designers); content is specific to procurement.

### Already in tree (referenced by recent work)

These items substantively landed in-session or immediately before Phase 3 documentation; retained here for auditors reading only the changelog:

- **Installers** — `install.sh` / `install-codex.sh` deploy `tools/validators/` and `evals/` next to installed skills (`~/.claude/…` / `~/.agents/…`); uninstall removes pack-marked evaluator trees where applicable (see uninstall scripts).
- **Fast frontmatter QA** — [tools/quick_validate/](tools/quick_validate/) (`quick_validate.py`, `quick_validate.rules.yaml`) for SKILL.md YAML checks outside the heavy validator.

### Notes

- **Structural validation (`distr/validate.py`, `tools/validators/validate_skill.py`)** and **skill `sample-output.json` / eval alignment** fixes may appear in Git history where available; root summary here focuses on observable pack additions listed above.
- **Phase 3 CLI assets** (`tools/feedback/*`) ship with the **clone/repo** — they are **not** part of `install.sh` / `install-codex.sh` skill rsync targets unless/until added explicitly to installers.
