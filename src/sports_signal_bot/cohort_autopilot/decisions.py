from datetime import datetime
from typing import List, Dict, Any, Optional
from .contracts import (
    AutopilotDecisionRecord, AutopilotAction, ActivationLevel,
    AutopilotHeuristicRecord
)

def create_decision(
    cohort_id: str,
    current_level: ActivationLevel,
    action: AutopilotAction,
    heuristic_breakdown: Dict[str, Any],
    blockers: List[str] = None,
    next_level: Optional[ActivationLevel] = None
) -> AutopilotDecisionRecord:
    return AutopilotDecisionRecord(
        autopilot_decision_id=f"dec_{cohort_id}_{int(datetime.utcnow().timestamp())}",
        cohort_id=cohort_id,
        current_activation_level=current_level,
        proposed_action=action,
        proposed_next_level=next_level,
        decision_status="generated",
        heuristic_breakdown=heuristic_breakdown,
        blockers=blockers or []
    )

def compute_autopilot_heuristic_components(signals: Dict[str, float]) -> AutopilotHeuristicRecord:
    total = sum(signals.values())
    return AutopilotHeuristicRecord(
        heuristic_id=f"heur_{int(datetime.utcnow().timestamp())}",
        components=signals,
        total_score=total
    )

def combine_autopilot_score(heuristic: AutopilotHeuristicRecord) -> float:
    return heuristic.total_score

def evaluate_hard_growth_blocks(blockers: List[str]) -> bool:
    return len(blockers) > 0

def validate_autopilot_safety(decision: AutopilotDecisionRecord) -> bool:
    if decision.proposed_action == AutopilotAction.PROGRESS_COHORT and decision.blockers:
        return False
    return True
