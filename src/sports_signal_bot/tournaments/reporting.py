from typing import List, Dict, Any
from .contracts import (
    TournamentManifest,
    CandidateScorecardRecord,
    TournamentGateRequirementRecord,
    TournamentCandidateRecord,
    CandidateComparisonRecord,
    TournamentEvidenceRecord,
    SafetyLane
)
from .gate_burden import attach_gate_burden_notes, summarize_gate_requirements
import uuid

def generate_candidate_scorecard(
    candidate: TournamentCandidateRecord,
    comparison: CandidateComparisonRecord,
    gate_burden: TournamentGateRequirementRecord,
    evidence: TournamentEvidenceRecord
) -> CandidateScorecardRecord:

    gains = []
    regressions = []
    for m in comparison.metrics:
        # Simplistic assumption: positive means gain if maximize, or loss if minimize
        from .contracts import ObjectiveDirection
        is_good = (m.value > 0 and m.direction == ObjectiveDirection.MAXIMIZE) or \
                  (m.value < 0 and m.direction == ObjectiveDirection.MINIMIZE)
        if is_good:
            gains.append(f"{m.metric_name}: {m.value}")
        else:
            regressions.append(f"{m.metric_name}: {m.value}")

    caveats = attach_gate_burden_notes(gate_burden)
    if comparison.lane == SafetyLane.EXPLORATORY_LANE:
        caveats.append("Candidate is exploratory and lacks strong support.")

    return CandidateScorecardRecord(
        scorecard_id=str(uuid.uuid4()),
        candidate_id=candidate.candidate_id,
        key_gains=gains,
        key_regressions=regressions,
        risk_summary=f"Risk Level: {candidate.risk_level.value}",
        support_summary=f"Support Strength: {candidate.support_strength:.2f}",
        scope_summary=f"Blast Radius: {candidate.estimated_blast_radius:.2f}",
        gate_burden=gate_burden,
        evidence_refs=[evidence],
        caveats=caveats
    )

def build_tournament_summary(manifest: TournamentManifest) -> Dict[str, Any]:
    summary = {
        "tournament_id": manifest.tournament_id,
        "total_candidates": len(manifest.batch.candidates),
        "pareto_front_count": len(manifest.pareto_fronts),
        "shortlist_tiers": {}
    }

    for s_list in manifest.shortlists:
        summary["shortlist_tiers"][s_list.tier.value] = len(s_list.ranked_candidates)

    blocked = sum(1 for r in manifest.rankings if r.lane == SafetyLane.BLOCKED_LANE)
    invalid = sum(1 for r in manifest.rankings if r.lane == SafetyLane.INVALID_LANE)

    summary["blocked_count"] = blocked
    summary["invalid_count"] = invalid

    return summary
