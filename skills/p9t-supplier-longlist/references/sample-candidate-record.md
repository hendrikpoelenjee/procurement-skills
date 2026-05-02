<!-- SPDX-License-Identifier: Apache-2.0 -->

# Sample Candidate Record

Example longlist record showing the required fields and how to populate them.

---

## Field definitions

| Field | Required | Description |
|---|---|---|
| `candidate_id` | Yes | Stable slug for the record (e.g., `cand-001`) |
| `name` | Yes | Supplier name |
| `geography` | Yes | Countries or regions where the supplier operates in this category |
| `category_fit` | Yes | Specific service or product lines relevant to the brief |
| `certifications` | Yes | Relevant certifications with issuing body and expiry date |
| `size_indicator` | Yes | Revenue band or headcount in the relevant service line |
| `must_haves_met` | Yes | Pass / Fail / Pending per must-have criterion |
| `evidence_sources` | Yes | Where the information was found (URL, register, database) |
| `confidence` | Yes | HIGH / MEDIUM / LOW — see `screening-guide.md` |
| `flags` | No | Any concerns, risks, or items requiring follow-up |
| `notes` | No | Context that does not fit another field |

---

## Example record

```json
{
  "candidate_id": "cand-003",
  "name": "[Supplier Name — anonymised]",
  "geography": ["Netherlands", "Belgium", "Germany"],
  "category_fit": "Integrated FM — cleaning (all sites), security (tier 1 sites only), catering (partial)",
  "certifications": [
    {
      "type": "ISO 14001",
      "issuing_body": "Bureau Veritas",
      "expiry": "2027-03"
    },
    {
      "type": "ISO 45001",
      "issuing_body": "DNV",
      "expiry": "2026-09"
    }
  ],
  "size_indicator": "~3,200 FM FTE in Benelux / DACH region; estimated regional revenue €180M",
  "must_haves_met": {
    "ISO 14001": "PASS — certificate verified",
    "minimum 200 FM FTE": "PASS — verified from trade body directory",
    "Dutch language capability": "PASS — confirmed via company website"
  },
  "evidence_sources": [
    "Trade body member directory — FM Nederland",
    "Supplier website — services page",
    "Bureau Veritas certificate register"
  ],
  "confidence": "MEDIUM",
  "flags": [
    "Catering capability covers fewer than 50% of in-scope sites — may require sub-contracting",
    "Security services limited to tier 1 sites — confirm if tier 2 and 3 requirements are in scope"
  ],
  "notes": "Identified via Tier 2 search (FM Nederland directory). Not on existing approved supplier list. No prior relationship with this organisation."
}
```

---

## Rules

- Every must-have criterion must appear in `must_haves_met` with a verdict and evidence note
- `confidence` must reflect the actual evidence quality — not an optimistic summary
- `flags` are not disqualifiers unless they reference a must-have criterion that is not met — they are items for the qualification stage to investigate
- Do not include the candidate's own marketing materials as the sole evidence source for a must-have criterion
