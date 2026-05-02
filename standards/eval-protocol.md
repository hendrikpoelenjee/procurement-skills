<!-- SPDX-License-Identifier: Apache-2.0 -->

# Eval Protocol Standard

Define the minimum test-case requirements, format, and pass criteria for skill evaluation files at `/evals/p9t-*/cases.json`.

Referenced by `CLAUDE.md` (eval standard).

---

## Purpose

- Give each skill **repeatable**, **reviewable** scenarios before lifecycle promotion.
- Separate **fixture data** (`evals/` tree) from **skill behaviour** (`skills/p9t-*/`).
- Produce evidence suitable for append-only logging in `tools/validators/validation_log.md`.

---

## Scope

- Applies to all skills targeting `production`.
- Skills in `draft` or `review`: eval files should still exist; execution may be staged.

---

## File layout

```text
evals/
├── p9t-<skill-name>/
│   └── cases.json
└── README.md                       # Optional: how replay is run on your stack
```

There is exactly one `cases.json` per skill folder; its `skill` property must equal the directory name (`p9t-…`).

---

## `cases.json` format

Validated by `tools/validators/eval_cases.schema.json`.

| Field       | Requirement |
|------------|---------------|
| `skill`    | Must match `/^p9t-[a-z0-9-]+$/` and the parent folder name |
| `version`  | String you bump when fixtures or expectations materially change |
| `cases[]` | At least **four** rows, covering **all** types below |

### Case types (`cases[].type`)

| Type | Intent |
|------|--------|
| `happy_path` | Well-formed inputs; expect schema-complete output aligned with skill purpose |
| `thin_data` | Missing critical fields; expect `confidence_level` downgrade, `blocked`/`INSUFFICIENT_DATA`, or explicit data gaps |
| `contradictory_inputs` | Conflicting canonical fields; expect explicit conflict surfaced, **not** silent resolution |
| `high_risk` | Inputs that should force `risk_flags`, escalation, or human gate semantics |

Each case includes:

| Field           | Requirement |
|----------------|-------------|
| `id`           | Stable slug for logs |
| `type`         | One of the four enums above |
| `title`        | Human-readable summary |
| `inputs`       | JSON object — minimal stub or inlined brief (expand later with fixtures) |
| `fixture_path` | Optional — repo-relative path when large payloads move to separate files |
| `pass_signals` | Optional — acceptance hints for reviewer or tooling |

---

## How to execute evals today

Mechanical structural checks run in `tools/validators/validate_skill.py`:

- File exists at `evals/<skill-dir-name>/cases.json`
- Parses as JSON and validates against `eval_cases.schema.json`
- Covers all four mandatory case types at least once

**Execution** against a runtime (Claude, Codex, etc.) remains **human-invoked**:

1. Open `cases.json` for the skill.
2. Replay `inputs` (or fixture) through the hosted skill invocation.
3. Compare output to skill `assets/output.schema.json` and skill epistemic rules.
4. Record outcome in `tools/validators/validation_log.md` before promoting lifecycle state.

Automated replay hooks may be introduced later — they **do not** replace the schema checks above.

---

## Pass criteria (reviewer)

### happy_path

- Output validates against the skill schema.
- `reasoning_trace` (where required) is coherent with cited inputs.
- `confidence_level` is not inconsistent with populated `data_gaps`.

### thin_data

- No **HIGH** confidence with unexplained residual gaps (`CLAUDE.md` §3).
- Prefer explicit `blocked`/`INSUFFICIENT_DATA`/`LOW` plus visible gaps over a polished hallucination.

### contradictory_inputs

- Contradictions appear in assumptions, `open_questions`, or explicit escalation — **not** resolved away.

### high_risk

- `risk_flags` and/or `escalation_required` aligns with stakes; reviewer does not approve blind promotion.

Borderline judgement → document in validation log **before** flipping status.

---

## Closed vs open gaps

Structural eval coverage is **closed** when validator reports `[OK]` for eval cases.

**Still open until done deliberately:**

| Item | Responsibility |
|------|----------------|
| Fixture depth | Expand `inputs` / `fixture_path` with anonymised procurement-like payloads |
| Agent harness | Scripted replay (optional tooling) |
| Reference stub quality | Separate from evals (`references/*.md` substance) |

---

## Lifecycle gate

- Eval skeleton must exist before claiming “eval gap closed”.
- Full promotion to `production` requires passing **live** reviewer criteria above and logged validation run.

---

## Owner

procurement-engineering

## Related

- `CLAUDE.md` — Eval standard
- `tools/validators/eval_cases.schema.json` — Schema for `cases.json`
- `tools/validators/validation_log.md` — Append-only audit log
