import uuid
from typing import List, Dict, Optional
from .contracts import CouncilFederationBoardRecord, FederationBoardCaseRecord, FederationBoardDecisionRecord, WarningRecord

def build_council_federation_board(
    board_family: str,
    member_council_refs: List[str],
    quorum_policy_ref: str
) -> CouncilFederationBoardRecord:
    return CouncilFederationBoardRecord(
        federation_board_id=f"fcb_{uuid.uuid4()}",
        board_family=board_family,
        member_council_refs=member_council_refs,
        participant_refs=[],
        quorum_policy_ref=quorum_policy_ref,
        precedence_policy_ref="default_precedence",
        backlog_ref="default_backlog",
        health_status="healthy",
        warnings=[]
    )

def open_federation_board_case(
    case_family: str,
    input_council_case_refs: List[str],
    input_synthesis_refs: List[str]
) -> FederationBoardCaseRecord:
    return FederationBoardCaseRecord(
        federation_board_case_id=f"fbc_{uuid.uuid4()}",
        case_family=case_family,
        input_council_case_refs=input_council_case_refs,
        input_synthesis_refs=input_synthesis_refs,
        input_dashboard_refs=[],
        input_debt_refs=[],
        input_replay_refs=[],
        decision_needed="bounded_resolution",
        escalation_state="normal",
        case_status="case_opened",
        warnings=[]
    )

def collect_board_positions(case: FederationBoardCaseRecord, positions: List[str]) -> FederationBoardCaseRecord:
    case.case_status = "case_quorum_pending"
    return case

def resolve_federation_board_case(case: FederationBoardCaseRecord) -> FederationBoardDecisionRecord:
    if "sovereignty_failure" in case.input_synthesis_refs:
         case.case_status = "case_blocked"
         return FederationBoardDecisionRecord(decision_id=f"fbd_{uuid.uuid4()}", decision_type="block_due_to_unresolved_board_conflict")

    case.case_status = "case_decided_with_caveats"
    return FederationBoardDecisionRecord(decision_id=f"fbd_{uuid.uuid4()}", decision_type="accept_bounded_assurance_with_caps")

def apply_federation_board_decision(case: FederationBoardCaseRecord, decision: FederationBoardDecisionRecord) -> FederationBoardCaseRecord:
    # Cap/downgrade logic
    return case

def summarize_federation_board(board: CouncilFederationBoardRecord) -> Dict:
    return {
        "id": board.federation_board_id,
        "health": board.health_status,
        "members": len(board.member_council_refs)
    }
