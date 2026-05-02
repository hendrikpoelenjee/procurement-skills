# Handoff Rules

This routing matrix tells the conductor which skills to invoke and where human approval is required.

## Path types

- `rapid_scan` — fast market view and longlist only
- `greenfield` — new sourcing event from limited baseline
- `renewal` — incumbent renewal or renegotiation
- `competitive_event` — formal RFx or structured competition
- `negotiation_only` — supplier known, leverage and negotiation plan needed

## Routing matrix

### Simple

#### rapid_scan
1. `p9t-intake-and-brief`
2. `p9t-complexity-triage`
3. `p9t-market-scan`
4. `p9t-supplier-longlist`
5. `p9t-output-review`

Approval gates:
- `G1_scope_approval` optional
- `G2_market_and_longlist_approval` required before supplier outreach

#### negotiation_only
1. `p9t-intake-and-brief`
2. `p9t-complexity-triage`
3. `p9t-category-baseline`
4. `p9t-negotiation-prep`
5. `p9t-output-review`

Approval gates:
- `G1_scope_approval` optional
- `G4_recommendation_approval` required before final commercial commitment

### Moderate

#### greenfield
1. `p9t-intake-and-brief`
2. `p9t-complexity-triage`
3. `p9t-category-baseline`
4. `p9t-market-scan`
5. `p9t-supplier-longlist`
6. `p9t-supplier-qualification`
7. `p9t-output-review`

Approval gates:
- `G1_scope_approval` required
- `G2_market_and_longlist_approval` required

#### renewal
1. `p9t-intake-and-brief`
2. `p9t-complexity-triage`
3. `p9t-category-baseline`
4. `p9t-market-scan`
5. `p9t-negotiation-prep`
6. `p9t-award-recommendation`
7. `p9t-output-review`

Approval gates:
- `G1_scope_approval` required
- `G4_recommendation_approval` required

### Strategic

#### competitive_event
1. `p9t-intake-and-brief`
2. `p9t-complexity-triage`
3. `p9t-category-baseline`
4. `p9t-market-scan`
5. `p9t-supplier-longlist`
6. `p9t-supplier-qualification`
7. `p9t-rfx-pack-builder`
8. `p9t-bid-evaluation-framework`
9. `p9t-negotiation-prep`
10. `p9t-award-recommendation`
11. `p9t-output-review`

Approval gates:
- `G1_scope_approval` required
- `G2_market_and_longlist_approval` required
- `G3_rfx_and_evaluation_approval` required
- `G4_recommendation_approval` required

## Stage prerequisites

- `p9t-supplier-longlist` requires a defined scope and at least a light market scan.
- `p9t-supplier-qualification` requires qualification criteria and an initial longlist.
- `p9t-rfx-pack-builder` requires an agreed scope and target supplier set.
- `p9t-bid-evaluation-framework` should be drafted before bids are invited and approved before scoring.
- `p9t-negotiation-prep` requires either shortlisted suppliers or a defined incumbent negotiation case.
- `p9t-award-recommendation` requires comparative evidence or a justified waiver.

## Stop / continue rule

The conductor must stop at the next required gate. It may not automatically continue past a required gate unless the calling runtime explicitly provides approval state.

## Output expectations

For each selected skill, emit:

- `sequence_number`
- `skill_id`
- `why_selected`
- `required_inputs`
- `expected_artifacts`
- `exit_criteria`
- `depends_on`
- `approval_gate_after`
