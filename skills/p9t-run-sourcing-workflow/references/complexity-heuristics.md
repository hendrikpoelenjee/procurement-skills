# Complexity Heuristics

Use this weighted scoring model to classify the sourcing case.

## Scoring dimensions

Score each dimension from 0 to 3.

- `spend_scale`
  - 0 = low or unknown spend with limited downside
  - 1 = moderate spend
  - 2 = material spend for the function or site
  - 3 = enterprise-significant or board-visible spend
- `supply_risk`
  - 0 = many interchangeable suppliers
  - 1 = several credible alternatives
  - 2 = limited qualified market
  - 3 = concentrated market or single-point dependency
- `switching_risk`
  - 0 = easy switch, minimal disruption
  - 1 = manageable transition
  - 2 = meaningful implementation/change burden
  - 3 = high disruption, validation, or shutdown risk
- `specification_complexity`
  - 0 = standard specification
  - 1 = light customization
  - 2 = notable technical requirements
  - 3 = bespoke, regulated, or multi-site complexity
- `stakeholder_complexity`
  - 0 = one decision maker
  - 1 = small aligned group
  - 2 = cross-functional alignment required
  - 3 = many stakeholders with conflicting priorities
- `timeline_pressure`
  - 0 = ample time
  - 1 = normal sourcing timetable
  - 2 = compressed schedule
  - 3 = urgent or business continuity driven
- `incumbent_entrenchment`
  - 0 = no incumbent lock-in
  - 1 = moderate incumbent familiarity
  - 2 = incumbent has integration or relationship advantage
  - 3 = severe dependency, switching penalties, or data lock-in

## Complexity bands

- `0–6` → `simple`
- `7–13` → `moderate`
- `14+` → `strategic`

## Override rules

Classify as `strategic` even if the score is lower when any of the following is true:

- supply market is effectively single-source
- switching failure would disrupt operations materially
- legal, regulatory, cybersecurity, or safety exposure is high
- the category is executive or board visible

Classify as at least `moderate` when:

- the incumbent is entrenched and a negotiation-only path is being considered
- timeline pressure is high and supplier evidence is weak
- cross-functional approval is required before supplier contact

## Output guidance

Always explain:

- score by dimension
- final complexity label
- why any override was applied
- what the minimum viable workflow should be for this case
