import uuid
import datetime
from typing import List, Optional

from .contracts import (
    GovernanceTierCouncilRecord, CouncilCaseRecordV2, CouncilParticipantRecordV2,
    CouncilQuorumRecord, CouncilDecisionEnvelopeRecord
)

def build_governance_tier_council(family: str, tier_refs: List[str], participant_refs: List[str]) -> GovernanceTierCouncilRecord:
    return GovernanceTierCouncilRecord(
        council_id=f"council_{uuid.uuid4().hex[:8]}",
        council_family=family,
        governed_tier_refs=tier_refs,
        participant_refs=participant_refs,
        quorum_policy_ref="default_quorum_policy",
        precedence_policy_ref="default_precedence_policy",
        backlog_ref="backlog_main",
        health_status="healthy",
        warnings=[]
    )

def open_council_case(council: GovernanceTierCouncilRecord, case_family: str, input_scope_ref: str) -> CouncilCaseRecordV2:
    return CouncilCaseRecordV2(
        case_id=f"case_{uuid.uuid4().hex[:8]}",
        case_family=case_family,
        input_scope_ref=input_scope_ref,
        decision_needed="standard_decision",
        escalation_state="normal",
        case_status="case_opened",
        warnings=[]
    )

def collect_council_positions(case: CouncilCaseRecordV2, positions: List[str]) -> CouncilCaseRecordV2:
    case.case_status = "case_collecting_positions"
    if len(positions) >= 3:
        case.case_status = "case_quorum_pending"
    return case

def evaluate_council_quorum(case: CouncilCaseRecordV2, quorum_type: str, met: bool) -> CouncilQuorumRecord:
    record = CouncilQuorumRecord(
        quorum_id=f"quorum_{uuid.uuid4().hex[:8]}",
        case_ref=case.case_id,
        quorum_type=quorum_type,
        met=met,
        details="Quorum evaluation completed"
    )
    if not met:
        case.case_status = "case_blocked"
        case.warnings.append("Quorum failed, blocking decision")
    else:
        case.case_status = "case_decided"
    return record

def resolve_council_decision(case: CouncilCaseRecordV2, decision_type: str) -> CouncilDecisionEnvelopeRecord:
    caveats = []
    if "caveat" in decision_type.lower() or case.case_status == "case_blocked":
        caveats.append("Decision has caveats or blocked")
        case.case_status = "case_decided_with_caveats" if case.case_status != "case_blocked" else "case_blocked"

    return CouncilDecisionEnvelopeRecord(
        decision_id=f"dec_{uuid.uuid4().hex[:8]}",
        case_ref=case.case_id,
        decision_type=decision_type,
        caveats=caveats,
        lineage_refs=[case.input_scope_ref]
    )

def summarize_council_case(case: CouncilCaseRecordV2) -> str:
    return f"Case {case.case_id} ({case.case_family}): Status={case.case_status}, Escalation={case.escalation_state}"
