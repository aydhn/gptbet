import uuid
from typing import List, Dict, Any
from .contracts import (
    ObservatoryExchangeCaseRecord,
    ObservatoryExchangeEvidenceRecord,
    ObservatoryExchangeDecisionRecord
)

CASE_OPENED = "case_opened"
CASE_COLLECTING_EVIDENCE = "case_collecting_evidence"
CASE_QUORUM_PENDING = "case_quorum_pending"
CASE_DECIDED = "case_decided"
CASE_DECIDED_WITH_CAVEATS = "case_decided_with_caveats"
CASE_REVIEW_ONLY = "case_review_only"
CASE_BLOCKED = "case_blocked"
CASE_SUPERSEDED = "case_superseded"
CASE_ARCHIVED = "case_archived"

DECISION_PRESERVE_EXISTING_EXCHANGE_CAPS = "preserve_existing_exchange_caps"
DECISION_DOWNGRADE_TO_REVIEW_ONLY = "downgrade_to_review_only_exchange"
DECISION_REQUIRE_SNAPSHOT_REFRESH = "require_snapshot_refresh"
DECISION_REQUIRE_SIGNAL_REVALIDATION = "require_signal_revalidation"
DECISION_AMPLIFY_EXCHANGE_CAVEATS = "amplify_exchange_caveats"
DECISION_PRESERVE_NO_SAFE_VISIBILITY = "preserve_no_safe_visibility"
DECISION_ACCEPT_BOUNDED_EXCHANGE = "accept_bounded_exchange_with_caps"
DECISION_BLOCK_UNRESOLVED = "block_due_to_unresolved_exchange_conflict"

def open_observatory_exchange_case(family: str, exchange_refs: List[str]) -> ObservatoryExchangeCaseRecord:
    return ObservatoryExchangeCaseRecord(
        observatory_exchange_case_id=f"oec_{uuid.uuid4().hex[:8]}",
        case_family=family,
        input_exchange_refs=exchange_refs,
        input_snapshot_refs=[],
        input_signal_refs=[],
        input_alert_refs=[],
        input_mesh_refs=[],
        decision_needed="exchange_review",
        escalation_state="none",
        case_status=CASE_OPENED
    )

def collect_observatory_exchange_evidence(case: ObservatoryExchangeCaseRecord, data: Dict[str, Any]) -> ObservatoryExchangeEvidenceRecord:
    case.case_status = CASE_COLLECTING_EVIDENCE
    return ObservatoryExchangeEvidenceRecord(
        evidence_id=f"ev_{uuid.uuid4().hex[:8]}",
        data=data
    )

def resolve_observatory_exchange_case(
    case: ObservatoryExchangeCaseRecord,
    evidence: List[ObservatoryExchangeEvidenceRecord],
    has_quorum: bool,
    has_no_safe_alerts: bool,
    is_degraded: bool,
    is_stale: bool
) -> ObservatoryExchangeDecisionRecord:

    # Rule: no quorum no strong bounded exchange affirmation
    if not has_quorum:
        case.case_status = CASE_REVIEW_ONLY
        return ObservatoryExchangeDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_DOWNGRADE_TO_REVIEW_ONLY
        )

    # Rule: stale signals or stale snapshots cannot produce strong exchange pass
    if is_stale:
        case.case_status = CASE_BLOCKED
        return ObservatoryExchangeDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_REQUIRE_SNAPSHOT_REFRESH
        )

    # Rule: no-safe and sovereignty alerts explicitly preserved
    if has_no_safe_alerts:
        case.case_status = CASE_DECIDED_WITH_CAVEATS
        return ObservatoryExchangeDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_PRESERVE_NO_SAFE_VISIBILITY
        )

    # Rule: degraded exchange hidden kalamaz
    if is_degraded:
        case.case_status = CASE_REVIEW_ONLY
        return ObservatoryExchangeDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_DOWNGRADE_TO_REVIEW_ONLY
        )

    case.case_status = CASE_DECIDED
    return ObservatoryExchangeDecisionRecord(
        decision_id=f"dec_{uuid.uuid4().hex[:8]}",
        decision_type=DECISION_ACCEPT_BOUNDED_EXCHANGE
    )

def apply_observatory_exchange_decision(case: ObservatoryExchangeCaseRecord, decision: ObservatoryExchangeDecisionRecord):
    pass

def explain_observatory_exchange_outcome(case: ObservatoryExchangeCaseRecord, decision: ObservatoryExchangeDecisionRecord) -> str:
    return f"Exchange Case {case.observatory_exchange_case_id} resolved with {decision.decision_type}. Status: {case.case_status}"

def record_observatory_exchange_lineage(case: ObservatoryExchangeCaseRecord):
    pass

def summarize_observatory_exchange_effects(case: ObservatoryExchangeCaseRecord) -> str:
    return f"Exchange Case affected {len(case.input_exchange_refs)} exchanges."
