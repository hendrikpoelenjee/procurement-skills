# Changelog

## 0.2.0 — 2026-04-29

- Output contract: `source_quality` is now a structured object (`recency`, `coverage`, `bias_risk`), each `LOW` | `MEDIUM` | `HIGH`.
- `confidence_level` adds `INSUFFICIENT_DATA`; epistemic section updated accordingly.
- Required fields aligned with governance: `reasoning_trace`, `escalation_required`.

## 0.1.0

- Initial packaged skill (`p9t-market-scan`).
