#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = SKILL_DIR / 'artifacts'

GATES = {
    'G1_scope_approval': 'Approve scope, objectives, and path before deeper work.',
    'G2_market_and_longlist_approval': 'Approve market view and supplier set before outreach or qualification.',
    'G3_rfx_and_evaluation_approval': 'Approve RFx design and evaluation method before formal competition.',
    'G4_recommendation_approval': 'Approve recommendation before commitment or implementation.'
}

STAGE_ARTIFACTS = {
    'p9t-intake-and-brief': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-complexity-triage': ['artifacts/complexity-assessment.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-category-baseline': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-market-scan': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-supplier-longlist': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-supplier-qualification': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-rfx-pack-builder': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-bid-evaluation-framework': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-negotiation-prep': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-award-recommendation': ['artifacts/result.json', 'artifacts/summary.md', 'artifacts/open_questions.json'],
    'p9t-output-review': ['artifacts/p9t-output-review.json', 'artifacts/summary.md'],
}

STAGE_OBJECTIVES = {
    'p9t-intake-and-brief': 'Normalize the request into a sourcing brief with explicit objectives, scope, and constraints.',
    'p9t-complexity-triage': 'Score the case and determine the minimum viable workflow and governance intensity.',
    'p9t-category-baseline': 'Establish current state, demand profile, cost drivers, and incumbent position.',
    'p9t-market-scan': 'Build a structured external market view with supply, trends, and risk cues.',
    'p9t-supplier-longlist': 'Identify credible candidate suppliers with rationale and evidence.',
    'p9t-supplier-qualification': 'Screen candidate suppliers against must-have criteria and define a shortlist.',
    'p9t-rfx-pack-builder': 'Create the RFx structure, templates, and supplier instructions.',
    'p9t-bid-evaluation-framework': 'Define scoring, weighting, and decision criteria before evaluation.',
    'p9t-negotiation-prep': 'Prepare negotiation objectives, fallback positions, and concession map.',
    'p9t-award-recommendation': 'Synthesize recommendation, rationale, risks, and implementation conditions.',
    'p9t-output-review': 'Check completeness, internal consistency, and support for claims before release.',
}

STAGE_INPUTS = {
    'p9t-intake-and-brief': ['business_need', 'category_or_scope', 'timeline', 'constraints'],
    'p9t-complexity-triage': ['spend_estimate', 'switching_risk', 'supply_risk', 'timeline', 'stakeholder_count'],
    'p9t-category-baseline': ['current_state', 'incumbent_supplier_state', 'stakeholders'],
    'p9t-market-scan': ['category_or_scope', 'geography', 'constraints'],
    'p9t-supplier-longlist': ['category_or_scope', 'geography', 'market_scan'],
    'p9t-supplier-qualification': ['longlist', 'qualification_criteria'],
    'p9t-rfx-pack-builder': ['approved_scope', 'shortlist', 'requirements'],
    'p9t-bid-evaluation-framework': ['rfx_scope', 'evaluation_priorities'],
    'p9t-negotiation-prep': ['incumbent_supplier_state', 'shortlist', 'commercial_objectives'],
    'p9t-award-recommendation': ['evaluated_options', 'negotiation_outcome'],
    'p9t-output-review': ['all_prior_artifacts'],
}

STAGE_EXIT = {
    'p9t-intake-and-brief': 'Brief is complete enough for scoring and path selection.',
    'p9t-complexity-triage': 'Complexity, path type, and gate pattern are justified.',
    'p9t-category-baseline': 'Current state and sourcing levers are explicit.',
    'p9t-market-scan': 'Market structure and supplier landscape are sufficiently evidenced.',
    'p9t-supplier-longlist': 'Credible longlist is produced with rationale and gaps noted.',
    'p9t-supplier-qualification': 'Shortlist is justified against qualification criteria.',
    'p9t-rfx-pack-builder': 'RFx materials are coherent and ready for governance review.',
    'p9t-bid-evaluation-framework': 'Scoring model is approved and ready before bid assessment.',
    'p9t-negotiation-prep': 'Negotiation positions and fallback logic are documented.',
    'p9t-award-recommendation': 'Recommendation package is decision-ready.',
    'p9t-output-review': 'Release packet passes consistency and completeness checks.',
}

ROUTES = {
    ('simple', 'rapid_scan'): {
        'stages': ['p9t-intake-and-brief', 'p9t-complexity-triage', 'p9t-market-scan', 'p9t-supplier-longlist', 'p9t-output-review'],
        'gates': ['G2_market_and_longlist_approval'],
    },
    ('simple', 'negotiation_only'): {
        'stages': ['p9t-intake-and-brief', 'p9t-complexity-triage', 'p9t-category-baseline', 'p9t-negotiation-prep', 'p9t-output-review'],
        'gates': ['G4_recommendation_approval'],
    },
    ('moderate', 'greenfield'): {
        'stages': ['p9t-intake-and-brief', 'p9t-complexity-triage', 'p9t-category-baseline', 'p9t-market-scan', 'p9t-supplier-longlist', 'p9t-supplier-qualification', 'p9t-output-review'],
        'gates': ['G1_scope_approval', 'G2_market_and_longlist_approval'],
    },
    ('moderate', 'renewal'): {
        'stages': ['p9t-intake-and-brief', 'p9t-complexity-triage', 'p9t-category-baseline', 'p9t-market-scan', 'p9t-negotiation-prep', 'p9t-award-recommendation', 'p9t-output-review'],
        'gates': ['G1_scope_approval', 'G4_recommendation_approval'],
    },
    ('strategic', 'competitive_event'): {
        'stages': ['p9t-intake-and-brief', 'p9t-complexity-triage', 'p9t-category-baseline', 'p9t-market-scan', 'p9t-supplier-longlist', 'p9t-supplier-qualification', 'p9t-rfx-pack-builder', 'p9t-bid-evaluation-framework', 'p9t-negotiation-prep', 'p9t-award-recommendation', 'p9t-output-review'],
        'gates': ['G1_scope_approval', 'G2_market_and_longlist_approval', 'G3_rfx_and_evaluation_approval', 'G4_recommendation_approval'],
    },
}

PATH_ALIASES = {
    'competitive event': 'competitive_event',
    'negotiation-only': 'negotiation_only',
    'rapid scan': 'rapid_scan',
}


def normalize_path_type(path_type: str) -> str:
    value = (path_type or '').strip().lower().replace('-', '_')
    return PATH_ALIASES.get(value.replace('_', ' '), value)


def score_case(brief: dict):
    spend = brief.get('spend_estimate') or {}
    timeline = brief.get('timeline') or {}
    current_state = brief.get('current_state') or {}

    def spend_score(v):
        amount = 0
        if isinstance(v, dict):
            amount = float(v.get('amount', 0) or 0)
        elif isinstance(v, (int, float)):
            amount = float(v)
        if amount >= 5_000_000:
            return 3
        if amount >= 1_000_000:
            return 2
        if amount >= 100_000:
            return 1
        return 0

    def pressure_score(t):
        days = None
        if isinstance(t, dict):
            days = t.get('days_to_decision') or t.get('days_remaining')
        try:
            days = int(days) if days is not None else None
        except Exception:
            days = None
        if days is None:
            return 1
        if days <= 14:
            return 3
        if days <= 30:
            return 2
        if days <= 90:
            return 1
        return 0

    def map_scale(value):
        mapping = {
            'low': 0, 'minimal': 0, 'easy': 0, 'standard': 0,
            'medium': 1, 'moderate': 1, 'manageable': 1,
            'high': 2, 'material': 2, 'limited': 2, 'notable': 2,
            'critical': 3, 'single-source': 3, 'single_source': 3, 'board-visible': 3, 'board_visible': 3,
            'concentrated': 3, 'severe': 3, 'urgent': 3,
        }
        if isinstance(value, (int, float)):
            return max(0, min(3, int(value)))
        if not value:
            return 1
        value = str(value).strip().lower()
        return mapping.get(value, 1)

    stakeholders = brief.get('stakeholders') or []
    stakeholder_count = brief.get('stakeholder_count') or (len(stakeholders) if isinstance(stakeholders, list) else 1)
    if stakeholder_count <= 1:
        stakeholder_score = 0
    elif stakeholder_count <= 3:
        stakeholder_score = 1
    elif stakeholder_count <= 6:
        stakeholder_score = 2
    else:
        stakeholder_score = 3

    scores = {
        'spend_scale': spend_score(spend),
        'supply_risk': map_scale(brief.get('supply_risk')),
        'switching_risk': map_scale(brief.get('switching_risk')),
        'specification_complexity': map_scale(brief.get('specification_complexity')),
        'stakeholder_complexity': stakeholder_score,
        'timeline_pressure': pressure_score(timeline),
        'incumbent_entrenchment': map_scale(brief.get('incumbent_supplier_state', {}).get('entrenchment') if isinstance(brief.get('incumbent_supplier_state'), dict) else None),
        'criticality': map_scale(current_state.get('criticality') if isinstance(current_state, dict) else brief.get('criticality')),
    }
    total = sum(scores.values())
    if total >= 16:
        band = 'strategic'
    elif total >= 8:
        band = 'moderate'
    else:
        band = 'simple'

    overrides = []
    if str(brief.get('supply_risk', '')).lower() in {'single-source', 'single_source'}:
        overrides.append('single_source_supply_risk')
    if str(brief.get('switching_risk', '')).lower() in {'critical', 'severe'}:
        overrides.append('critical_switching_risk')
    if str(brief.get('criticality', '')).lower() in {'board-visible', 'board_visible', 'critical'}:
        overrides.append('high_criticality')
    if overrides:
        band = 'strategic'
    elif band == 'simple' and normalize_path_type(brief.get('requested_path_type', '')) == 'negotiation_only' and scores['incumbent_entrenchment'] >= 2:
        band = 'moderate'
        overrides.append('entrenched_incumbent_negotiation')
    return scores, total, band, overrides


def infer_path_type(brief: dict, complexity: str) -> str:
    requested = normalize_path_type(brief.get('requested_path_type', ''))
    if requested in {'greenfield', 'renewal', 'competitive_event', 'rapid_scan', 'negotiation_only'}:
        return requested
    incumbent = brief.get('incumbent_supplier_state') or {}
    current_state = brief.get('current_state') or {}
    if incumbent.get('exists') and brief.get('objective') in {'renewal', 'renegotiation'}:
        return 'renewal'
    if incumbent.get('exists') and not brief.get('competition_desired', True):
        return 'negotiation_only'
    if complexity == 'strategic':
        return 'competitive_event'
    if current_state.get('baseline_strength') == 'low' or brief.get('new_requirement'):
        return 'greenfield'
    return 'rapid_scan' if complexity == 'simple' else 'greenfield'


def build_plan(brief: dict):
    scores, total, complexity, overrides = score_case(brief)
    path_type = infer_path_type(brief, complexity)
    route = ROUTES.get((complexity, path_type))
    if route is None:
        # graceful fallback to closest sensible route
        if complexity == 'strategic':
            route = ROUTES[('strategic', 'competitive_event')]
            path_type = 'competitive_event'
        elif path_type in {'renewal', 'negotiation_only'}:
            route = ROUTES[('moderate', 'renewal')]
            path_type = 'renewal'
            complexity = 'moderate' if complexity == 'simple' else complexity
        else:
            route = ROUTES[('moderate', 'greenfield')]
            path_type = 'greenfield'
            complexity = 'moderate' if complexity == 'simple' else complexity

    stages = []
    completed_gates = set((brief.get('approval_state') or {}).get('approved_gates', []))
    next_required_gate = None
    stopped_after_sequence = None
    for idx, skill_id in enumerate(route['stages'], start=1):
        gate_after = None
        if skill_id == 'p9t-intake-and-brief' and 'G1_scope_approval' in route['gates']:
            gate_after = 'G1_scope_approval'
        elif skill_id in {'p9t-supplier-longlist', 'p9t-supplier-qualification'} and 'G2_market_and_longlist_approval' in route['gates']:
            gate_after = 'G2_market_and_longlist_approval'
        elif skill_id == 'p9t-bid-evaluation-framework' and 'G3_rfx_and_evaluation_approval' in route['gates']:
            gate_after = 'G3_rfx_and_evaluation_approval'
        elif skill_id in {'p9t-award-recommendation', 'p9t-negotiation-prep'} and 'G4_recommendation_approval' in route['gates']:
            gate_after = 'G4_recommendation_approval'

        stage = {
            'sequence_number': idx,
            'skill_id': skill_id,
            'objective': STAGE_OBJECTIVES[skill_id],
            'why_selected': f'Selected for {complexity} {path_type} workflow.',
            'required_inputs': STAGE_INPUTS[skill_id],
            'expected_artifacts': STAGE_ARTIFACTS[skill_id],
            'exit_criteria': STAGE_EXIT[skill_id],
            'depends_on': [route['stages'][idx - 2]] if idx > 1 else [],
            'owner': 'agent',
            'approval_gate_after': gate_after,
        }
        stages.append(stage)
        if gate_after and gate_after not in completed_gates and next_required_gate is None:
            next_required_gate = gate_after
            stopped_after_sequence = idx
            break

    selected_skills = [s['skill_id'] for s in stages]
    gates_in_plan = [s['approval_gate_after'] for s in stages if s['approval_gate_after']]
    summary = f"{complexity.capitalize()} {path_type} workflow with {len(selected_skills)} planned stages."
    if next_required_gate:
        summary += f" Stop after stage {stopped_after_sequence} for {next_required_gate}."

    assumptions = []
    if not brief.get('requested_path_type'):
        assumptions.append(f"Inferred path_type as '{path_type}' from the brief.")
    if not brief.get('stakeholders') and not brief.get('stakeholder_count'):
        assumptions.append('Assumed a default stakeholder complexity because stakeholder count was not provided.')
    if not brief.get('spend_estimate'):
        assumptions.append('Used conservative default spend scoring because spend estimate was not provided.')

    open_questions = []
    if not brief.get('qualification_criteria') and 'p9t-supplier-qualification' in selected_skills:
        open_questions.append('Qualification criteria need to be confirmed before p9t-supplier-qualification.')
    if 'p9t-rfx-pack-builder' in selected_skills and not brief.get('requirements'):
        open_questions.append('Detailed requirements are still needed before RFx pack creation.')
    if next_required_gate:
        open_questions.append(f'Human approval required at {next_required_gate} before continuing.')

    plan = {
        'status': 'completed',
        'summary': summary,
        'brief_id': brief.get('brief_id', 'brief-001'),
        'complexity_assessment': {
            'complexity': complexity,
            'score_total': total,
            'dimension_scores': scores,
            'overrides': overrides,
        },
        'path_type': path_type,
        'selected_skills': selected_skills,
        'required_gates': route['gates'],
        'gates_in_current_plan': gates_in_plan,
        'next_required_gate': next_required_gate,
        'approval_state': brief.get('approval_state', {'approved_gates': []}),
        'stopped_after_sequence': stopped_after_sequence,
        'stages': stages,
        'assumptions': assumptions,
        'open_questions': open_questions,
        'next_action': f'Obtain {next_required_gate}.' if next_required_gate else 'Execute the full planned workflow.',
        'artifact_map': {
            'workflow_plan': 'artifacts/workflow-plan.json',
            'workflow_routing': 'artifacts/workflow-routing.json',
            'summary': 'artifacts/summary.md',
            'open_questions': 'artifacts/open-questions.json',
        },
        'gate_definitions': GATES,
    }
    return plan


def write_outputs(plan: dict, output_path: Path, pretty: bool):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, indent=2 if pretty else None), encoding='utf-8')
    routing_path = output_path.parent / 'workflow-routing.json'
    routing_path.write_text(json.dumps({
        'brief_id': plan['brief_id'],
        'complexity': plan['complexity_assessment']['complexity'],
        'path_type': plan['path_type'],
        'selected_skills': plan['selected_skills'],
        'next_required_gate': plan['next_required_gate'],
    }, indent=2), encoding='utf-8')
    summary_path = output_path.parent / 'summary.md'
    summary_lines = [
        '# Workflow Summary',
        '',
        plan['summary'],
        '',
        f"- Complexity: `{plan['complexity_assessment']['complexity']}`",
        f"- Path type: `{plan['path_type']}`",
        f"- Planned stages: {', '.join(plan['selected_skills'])}",
        f"- Next required gate: `{plan['next_required_gate']}`" if plan['next_required_gate'] else '- Next required gate: none',
    ]
    summary_path.write_text('\n'.join(summary_lines) + '\n', encoding='utf-8')
    openq_path = output_path.parent / 'open-questions.json'
    openq_path.write_text(json.dumps({'open_questions': plan['open_questions']}, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Generate workflow-plan.json from a sourcing brief JSON.')
    parser.add_argument('--brief', required=True, help='Path to sourcing brief JSON file')
    parser.add_argument('--output', required=False, help='Optional output path for workflow-plan.json')
    parser.add_argument('--pretty', action='store_true', help='Pretty-print workflow-plan.json')
    args = parser.parse_args()

    brief_path = Path(args.brief)
    brief = json.loads(brief_path.read_text(encoding='utf-8'))
    plan = build_plan(brief)
    output_path = Path(args.output) if args.output else ARTIFACTS_DIR / 'workflow-plan.json'
    write_outputs(plan, output_path, args.pretty)
    print(str(output_path))


if __name__ == '__main__':
    main()
