# TPO Procurement Skills

### Sourcing workflows for Claude Code and OpenAI Codex

Twelve interconnected skills covering intake, complexity triage, category baseline, market scan, supplier longlist and qualification, RFx pack build, bid evaluation framing, negotiation prep, award recommendation, orchestration, and structured output review. Shared [execution standard](CLAUDE.md), procurement-specific [standards](standards/), central [structural validator](tools/validators/validate_skill.py), optional [eval cases](evals/), and a [Phase 3 feedback loop](#phase-3--feedback-loop-continuous-improvement) for evidence-based iteration.

Installation is local: clone the repo, run the install script for your runtime, restart the client. No hosted API keys are required to use the prompts.

**12 skills** | **shared standards** | **central validation** | **Claude Code + Codex**

README structure is partly inspired by [Computational Design Skills](https://github.com/Amanbh997/Claude-skills-for-Computational-Designers) — adapted for sourcing and governance in this repository.

---

## Table of contents

- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Skills reference](#skills-reference)
- [Example prompts](#example-prompts)
- [Repository layout](#repository-layout)
- [Standards & knowledge base](#standards--knowledge-base)
- [Validation & evals](#validation--evals)
- [AGENTS.md and Codex](#agentsmd-and-codex-does-it-work)
- [Phase 3 — feedback loop](#phase-3--feedback-loop-continuous-improvement)
- [Install / uninstall](#install--claude-code)
- [Requirements](#requirements)
- [License & disclaimer](#license)

---

## Quick start

### Claude Code

Requires `~/.claude` (Claude Code installed and signed in).

```bash
git clone https://github.com/theprocurementoffice/procurement-skills
cd procurement-skills
bash install.sh
```

Restart Claude Code. Skills appear under `~/.claude/skills/p9t-*/`; shared standards under `~/.claude/standards/`.

Invoke with a **slash prefix**, e.g. `/p9t-intake-and-brief`, `/p9t-run-sourcing-workflow`.

### OpenAI Codex

Uses Codex’s user skill layout: `~/.agents/skills`.

```bash
git clone https://github.com/theprocurementoffice/procurement-skills
cd procurement-skills
bash install-codex.sh
```

Restart Codex. Skills appear under `~/.agents/skills/p9t-*/`; standards under `~/.agents/standards/`.

Invoke by **explicit skill selection or name** without a leading slash (see each skill’s `providers/codex.yaml`).

### Copy into a repo (Codex-friendly)

Codex discovers skills under `.agents/skills` from the repo root upward. Copy or symlink this repo’s `skills/` and `standards/` into your project `.agents/` tree so teams share versions.

---

## How it works

The pack uses a **lean invocation surface** and **progressive disclosure** so the assistant does not preload every workflow at once:

```
User asks for sourcing help / picks a skill
        |
        v
Runtime loads skill name + description (discovery metadata)
        |
        v
On invocation: full SKILL.md behaviour + bundled assets/schemas
        |
        v
Heavy reference docs under skills/*/references/
  load only when the skill directs (or user asks deeper detail)
        |
        v
Optional: workflows write artifacts under ~/sourcing-projects/...
       (paths from skills-config / project conventions)
```

**Context layers**

| Layer | What loads | When |
| ----- | ----------- | ------ |
| **0** | Skill names and descriptions only | Listed in Claude/Codex skill discovery |
| **1** | `SKILL.md` + front matter + bundled assets/schemas | Skill is invoked |
| **2** | Skill `references/*.md`, project files | Needed for depth or gated steps |

Operational rules that apply across all `p9t-*` skills — epistemic fields, Guided Execution Mode, lifecycle — live in **[CLAUDE.md](CLAUDE.md)** and **[standards/](standards/)** (referenced from skills; not duplicated in full in every `SKILL.md`).

---

## Skills reference

| Group | Skill | Role |
| ----- | ------ | ----- |
| **Orchestration** | [`p9t-run-sourcing-workflow`](skills/p9t-run-sourcing-workflow/) | End-to-end routing, gates, sequencing |
| | [`p9t-complexity-triage`](skills/p9t-complexity-triage/) | Complexity and minimum viable pathway |
| **Intake & baseline** | [`p9t-intake-and-brief`](skills/p9t-intake-and-brief/) | Unstructured ask → sourcing brief |
| | [`p9t-category-baseline`](skills/p9t-category-baseline/) | Internal baseline: demand, suppliers, cost drivers |
| **Market & suppliers** | [`p9t-market-scan`](skills/p9t-market-scan/) | Market structure, landscape, risks |
| | [`p9t-supplier-longlist`](skills/p9t-supplier-longlist/) | Longlist with rationale |
| | [`p9t-supplier-qualification`](skills/p9t-supplier-qualification/) | Shortlist screening |
| **RFx & commercial** | [`p9t-rfx-pack-builder`](skills/p9t-rfx-pack-builder/) | RFx instructions, pricing, evaluation logic |
| | [`p9t-bid-evaluation-framework`](skills/p9t-bid-evaluation-framework/) | Weighted criteria and scoring design |
| | [`p9t-negotiation-prep`](skills/p9t-negotiation-prep/) | Targets, BATNA-style prep, concessions |
| **Decision & QA** | [`p9t-award-recommendation`](skills/p9t-award-recommendation/) | Decision-ready recommendation |
| | [`p9t-output-review`](skills/p9t-output-review/) | Completeness, schema fit, contradiction check |

Exact front matter (`name`, `description`, lifecycle, external input flags, etc.) is validated against [standards/skill-frontmatter.md](standards/skill-frontmatter.md).

---

## Example prompts

Natural language (many clients route to skills by description and context):

```
"We got an email asking for a new AV vendor across three countries — turn it into a sourcing brief."
  → Usually maps to intake / triage early; may suggest p9t-intake-and-brief

"This category is messy, political, single-source risk — what's the minimum workflow?"
  → p9t-complexity-triage plus downstream suggestions

"We need suppliers for industrial gases in Benelux, credible longlist."
  → p9t-supplier-longlist after brief/baseline clarity

"Build an RFQ pack with weighted technical vs commercial scoring."
  → p9t-rfx-pack-builder + evaluation framework interplay

"Dry-run my award memo against contradictions and missing risks."
  → p9t-output-review
```

Explicit invocation (**Claude Code** style):

```
/p9t-intake-and-brief
/p9t-run-sourcing-workflow
/p9t-market-scan
```

Codex typically uses picker + **skill names without** `/` — see [`providers/codex.yaml`](skills/p9t-intake-and-brief/providers/codex.yaml) in each skill.

---

## Repository layout

Conceptual tree (omit deep leaves):

```text
procurement-skills/
├── README.md                     # You are here
├── CLAUDE.md                     # Execution standard for all skills
├── AGENTS.snippet.md             # Optional merge snippet for AGENTS.md
├── standards/                    # Interaction, epistemic, eval, artifact rules
├── skills/
│   ├── p9t-intake-and-brief/
│   │   ├── SKILL.md
│   │   ├── CHANGELOG.md
│   │   ├── assets/
│   │   ├── references/
│   │   ├── providers/            # claude.yaml / codex.yaml variants
│   │   └── scripts/validate.py   # Thin wrapper → central validator
│   └── … (eleven other p9t-* skills)
├── tools/
│   ├── validators/
│   │   └── validate_skill.py   # Structural + schema checks (single source)
│   ├── feedback/                 # Phase 3: collect + summarise feedback JSON
│   └── quick_validate/           # Fast SKILL.md YAML/frontmatter linter
├── evals/
│   └── p9t-*/
│       └── cases.json            # Required for production lifecycle
├── distr/
│   └── validate.py               # CLI entry: --skill-dir or --all
├── install.sh / install-codex.sh
├── uninstall.sh / uninstall-codex.sh
└── manifest/                     # Pack manifest for scripted install
```

Installed copies mirror this shape under `~/.claude/` or `~/.agents/` so validator paths resolve predictably.

---

## Standards & knowledge base

| Resource | Purpose |
| -------- | ------- |
| [CLAUDE.md](CLAUDE.md) | Model pinning, Guided Execution, epistemic output contract, lifecycle, validator references |
| [standards/interaction-patterns.md](standards/interaction-patterns.md) | One-question-at-a-time interaction |
| [standards/epistemic-risk-standard.md](standards/epistemic-risk-standard.md) | Assumptions, failure modes, confidence vocabulary |
| [standards/eval-protocol.md](standards/eval-protocol.md) | Eval case taxonomy |
| [standards/feedback-standard.md](standards/feedback-standard.md) | Phase 3 feedback file locations & hygiene |
| [standards/input-trust.md](standards/input-trust.md) | External documents, prompt injection, sensitivity |

---

## Validation & evals

Structural checks (skill sections, `assets/output.schema.json` where present, `sample-output.json`, `evals/p9t-*/cases.json`) run with:

```bash
python3 distr/validate.py --all
python3 distr/validate.py --skill-dir skills/p9t-market-scan
```

Fast **SKILL.md frontmatter-only** check (YAML rules in-repo):

```bash
python3 tools/quick_validate/quick_validate.py
python3 tools/quick_validate/quick_validate.py skills/p9t-market-scan
# pip install pyyaml   # quick_validate dependency
```

After install, wrappers under each skill call the deployed validator next to evals:

```bash
python3 ~/.claude/skills/p9t-market-scan/scripts/validate.py
python3 ~/.agents/skills/p9t-market-scan/scripts/validate.py
```

Install **`jsonschema`** for full schema validation: `pip install jsonschema`.

**Remaining governance (human + runtime):**

| Topic | Notes |
| ----- | ----- |
| **Lifecycle proof** | Exercise eval cases via your runtime; record outcomes in [`tools/validators/validation_log.md`](tools/validators/validation_log.md) before claiming `production` |
| **Reference depth** | Some `skills/p9t-*/references/*.md` are intentionally thin scaffolding |
| **Schema drift** | Not every skill exposes the same richness in `output.schema.json` yet |

---

## AGENTS.md and Codex — does it work?

Yes — complementary roles:

| Mechanism | Role |
| --------- | ----- |
| **Skills** (`SKILL.md` + assets) | Executable workflows: intake → award |
| **`AGENTS.md`** (project root) | Repo-wide conventions: tone, gates, escalation |

Skills are discovered from disk paths; **`AGENTS.md` does not load skills.** Merge snippets from **[AGENTS.snippet.md](AGENTS.snippet.md)** into root `AGENTS.md` where your toolchain expects it (`AGENT.md` in some setups). Skill stubs respect project `AGENTS.md` when present.

---

## Phase 3 — feedback loop (continuous improvement)

Capture structured usage feedback per sourcing project so improvements stay **traceable**. Spec: **[tools/prompts/phase_three_cont_improvement_loop.md](tools/prompts/phase_three_cont_improvement_loop.md)**.

| Piece | Role |
| ----- | ---- |
| [standards/feedback-standard.md](standards/feedback-standard.md) | Paths, retention, redaction expectations |
| [tools/feedback/feedback.schema.json](tools/feedback/feedback.schema.json) | JSON Schema for one record |
| [tools/feedback/sample-feedback.json](tools/feedback/sample-feedback.json) | Example payload |

Append validated records to `workflow/feedback.json` (see standard for stage-local files):

```bash
python3 tools/feedback/collect_feedback.py \
  --workflow-dir ~/sourcing-projects/example-category-001/workflow \
  --record-file tools/feedback/sample-feedback.json

python3 tools/feedback/collect_feedback.py --dry-run \
  --project-root ~/sourcing-projects \
  --project-id example-category-001 \
  --record-file my-record.json
```

Summarise for triage:

```bash
python3 tools/feedback/summarize_feedback.py --project ~/sourcing-projects/example-category-001
python3 tools/feedback/summarize_feedback.py \
  --project ~/sourcing-projects/example-category-001 \
  --include-stage-feedback \
  --out ~/sourcing-projects/example-category-001/workflow/feedback-summary.md
```

Agent-facing improvement instructions: **[tools/prompts/improve_from_feedback.md](tools/prompts/improve_from_feedback.md)**. `pip install jsonschema` enables schema enforcement in `collect_feedback.py`.

---

## Install — Claude Code

Requires [Claude Code](https://claude.ai/code) so `~/.claude` exists.

```bash
cd procurement-skills   # your clone
bash install.sh
```

Restart Claude Code if skills do not appear.

---

## Install — OpenAI Codex

See [Agent Skills — Codex](https://developers.openai.com/codex/skills).

```bash
cd procurement-skills
bash install-codex.sh
```

If `~/.codex` exists, installs a pointer block into `~/.codex/AGENTS.md` when appropriate.

Restart Codex if skills do not show up.

---

## Uninstall

Run from **this repository clone** so `manifest/p9t-pack-skills.txt` resolves. Scripts remove only pack-listed `p9t-*` folders and evaluator trees **marked** `.installed_by_tpo_procurement_pack`.

**Claude**

```bash
bash uninstall.sh
```

**Codex**

```bash
bash uninstall-codex.sh
```

`~/.agents/standards/` may be left intentionally if shared with other packs.

---

## Requirements

- `bash`, `rsync` (macOS and most Linux)
- **Python 3** for `distr/validate.py`, quick_validate, and feedback tooling
- **Claude Code** or **Codex** runtime as above

---

## At a glance

| Metric | Notes |
| ------ | ----- |
| Pack skills | 12 (`p9t-*`) |
| Shared standards docs | Multiple `.md` under `standards/` |
| Structural validator | Single implementation in `tools/validators/` |
| Eval bundles | One `cases.json` per skill under `evals/p9t-*/` |
| Feedback tooling | Collect + summarise + improvement prompt |

---

## License

Licensed under **[Apache License 2.0](LICENSE)** (`SPDX: Apache-2.0`; see skills’ front matter and [NOTICE](NOTICE)).

---

## Disclaimer

Provided **“as is”** without warranties. Not a substitute for professional, legal, or regulatory advice.

---

## Responsible use

Do **not** rely solely on outputs for binding legal/regulatory commits, uninsured commercial bets, or safety-critical choices. Maintain human approvals for sourcing and award decisions.

---

## Support / security / contributing / AI-assisted development

- **Issues:** GitHub Issues / discussions when available — no SLA promised.
- **Security:** Report sensitive issues responsibly; see **[SECURITY.md](SECURITY.md)**.
- **Contributions:** **[CONTRIBUTING.md](CONTRIBUTING.md)** — contributions licensed Apache-2.0.
- **AI-assisted authoring:** Portions may be AI-assisted; maintainers review.

---

## About

Built by **[The Procurement Office](https://theprocurementoffice.com)** — encoding the TPO sourcing methodology from intake through award as structured, reviewable workflows.
