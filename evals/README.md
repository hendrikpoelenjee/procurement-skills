# Skill eval suites (`cases.json`)

Each `p9t-*` skill has **`evals/p9t-<name>/cases.json`**: four mandated case types (`happy_path`, `thin_data`, `contradictory_inputs`, `high_risk`) validated by:

```bash
python3 distr/validate.py --all
```

**Structure and execution protocol:** see **`standards/eval-protocol.md`** and **`tools/validators/eval_cases.schema.json`**.

Live replay (through Claude Code / Codex) stays **human-invoked** until an automated harness exists; populate `inputs` / `fixture_path` with anonymised procurement-like payloads before treating results as lifecycle evidence.
