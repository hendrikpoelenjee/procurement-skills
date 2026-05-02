<!-- SPDX-License-Identifier: Apache-2.0 -->

# Search Patterns

Methodology for supplier and market discovery. Structured to maximise coverage while making evidence quality explicit.

---

## Tier 1 — Public web search

Best for: broad market mapping, news, consolidation activity, named players.

Patterns:
- `[category] suppliers [geography] [year]`
- `top [category] companies [region]`
- `[category] market report [year]`
- `[category] industry association [country]`

**Limitation**: biased toward large, well-indexed suppliers. Small specialists and local players may not appear.

## Tier 2 — Industry and trade bodies

Best for: certified suppliers, regulated markets, regional specialists.

Approach:
- Identify the relevant trade association for the category
- Check their member directory or accredited supplier register
- Note certification bodies and their registrar lists (e.g., ISO, CHAS, SafeContractor, NEN, VCA)

**Limitation**: membership is voluntary; non-members may be equally capable.

## Tier 3 — Procurement databases and frameworks

Best for: pre-qualified suppliers in regulated or public-sector-adjacent categories.

Approach:
- Check public procurement frameworks (EU, UK Crown Commercial Service, national equivalents)
- Check category-specific approved supplier registers
- Note framework lot structure — a supplier on one lot may not cover others

**Limitation**: framework coverage is not market-complete; frameworks lag market entry by 12–36 months.

## Tier 4 — Buyer-side intelligence

Best for: relationship context, performance data, references.

Approach:
- Ask the requesting stakeholder for suppliers they have encountered or worked with
- Check existing approved supplier list or ERP vendor data
- Use peer benchmarking or industry events if accessible

**Limitation**: subjective, potentially biased toward incumbents or personal relationships.

---

## Cross-validation protocol

A candidate included in the longlist should appear in at least two tiers unless:
- It is a niche specialist where a single authoritative source is sufficient
- The geographic market is documented as thin in that tier

Single-tier sources must be labelled as such in the candidate record.

---

## Source credibility assessment

| Source type | Recency | Coverage | Bias risk |
|---|---|---|---|
| Supplier's own website | LOW — self-reported | LOW | HIGH |
| Trade body member list | MEDIUM | MEDIUM | LOW |
| Public procurement framework | HIGH — formally vetted | MEDIUM | LOW |
| Industry analyst report | HIGH if dated ≤2 years | HIGH | MEDIUM |
| Stakeholder nomination | MEDIUM | LOW | HIGH — relationship bias |
| LLM training data (no web access) | LOW — cutoff applies | MEDIUM | MEDIUM |

Use this table to populate `source_quality` fields in the output.

---

## Knowledge cutoff note

When live web access is unavailable, all findings derive from training data. Apply these rules:
- Mark `source_quality.recency` as `LOW`
- Add to `data_gaps`: "No live web search performed — findings based on training data; currency not guaranteed"
- Do not present training-data supplier lists as a current market view
- Flag specific market dynamics (M&A, pricing, new entrants) as potentially outdated
