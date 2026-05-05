from typing import List, Optional, Dict
import uuid

from src.sports_signal_bot.assurance_synthesizers.contracts import (
    TribunalRouteCouncilRecord,
    TribunalRouteCaseRecord,
    CaseStatus,
    RouteDecisionType,
    TribunalRouteDecisionRecord
)

def build_tribunal_route_council(
    council_family: str,
    quorum_policy_ref: str,
    precedence_policy_ref: str
) -> TribunalRouteCouncilRecord:
    return TribunalRouteCouncilRecord(
        tribunal_route_council_id=f"council_{uuid.uuid4().hex[:8]}",
        council_family=council_family,
        quorum_policy_ref=quorum_policy_ref,
        precedence_policy_ref=precedence_policy_ref,
        backlog_ref="default_backlog",
        health_status="active"
    )

def open_tribunal_route_case(
    case_family: str,
    input_trace_refs: List[str]
) -> TribunalRouteCaseRecord:
    return TribunalRouteCaseRecord(
        tribunal_route_case_id=f"case_{uuid.uuid4().hex[:8]}",
        case_family=case_family,
        input_trace_refs=input_trace_refs,
        escalation_state="normal",
        case_status=CaseStatus.case_opened
    )

def resolve_tribunal_route_case(
    case: TribunalRouteCaseRecord,
    has_sufficient_evidence: bool,
    has_sovereignty_conflict: bool
) -> TribunalRouteDecisionRecord:
    decision_type = RouteDecisionType.accept_bounded_route_with_caps

    if has_sovereignty_conflict:
        decision_type = RouteDecisionType.block_due_to_unresolved_route_conflict
        case.warnings.append("blocked by local sovereignty")
        case.case_status = CaseStatus.case_blocked
    elif not has_sufficient_evidence:
        decision_type = RouteDecisionType.downgrade_to_review_only_route
        case.warnings.append("downgraded due to insufficient evidence")
        case.case_status = CaseStatus.case_review_only
    else:
        case.case_status = CaseStatus.case_decided_with_caveats

    return TribunalRouteDecisionRecord(
        decision_id=f"dec_{uuid.uuid4().hex[:8]}",
        decision_type=decision_type
    )

def summarize_tribunal_route_council(council: TribunalRouteCouncilRecord) -> Dict[str, str]:
    return {
        "id": council.tribunal_route_council_id,
        "family": council.council_family,
        "health": council.health_status
    }
