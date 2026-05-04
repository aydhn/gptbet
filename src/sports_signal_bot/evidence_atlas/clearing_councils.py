from typing import List
from .contracts import (
    ReplayClearingCouncilRecord,
    ReplayClearingCouncilCaseRecord,
    ReplayClearingCouncilEvidenceRecord,
    ReplayClearingCouncilDecisionRecord,
    ReplayClearingCouncilHealthRecord,
    ReplayClearingCouncilCaseStatus,
    ReplayClearingDecisionOutcome
)

def build_replay_clearing_council(council_id: str, family: str) -> ReplayClearingCouncilRecord:
    return ReplayClearingCouncilRecord(
        replay_clearing_council_id=council_id,
        council_family=family,
        quorum_policy_ref="default_quorum_policy",
        precedence_policy_ref="default_precedence_policy",
        backlog_ref="default_backlog",
        health_status="initializing"
    )

def open_replay_clearing_case(council: ReplayClearingCouncilRecord, case_id: str, family: str) -> ReplayClearingCouncilCaseRecord:
    return ReplayClearingCouncilCaseRecord(
        replay_clearing_case_id=case_id,
        case_family=family,
        decision_needed="requires_clearing",
        escalation_state="normal",
        case_status=ReplayClearingCouncilCaseStatus.case_opened
    )

def collect_replay_clearing_evidence(case: ReplayClearingCouncilCaseRecord, evidence: List[ReplayClearingCouncilEvidenceRecord]) -> ReplayClearingCouncilCaseRecord:
    case.case_status = ReplayClearingCouncilCaseStatus.case_collecting_evidence
    # In a real implementation, we would attach evidence to the case
    return case

def resolve_replay_clearing_case(case: ReplayClearingCouncilCaseRecord, outcome: ReplayClearingDecisionOutcome, justification: str) -> ReplayClearingCouncilDecisionRecord:
    case.case_status = ReplayClearingCouncilCaseStatus.case_decided
    return ReplayClearingCouncilDecisionRecord(
        decision_id=f"decision_{case.replay_clearing_case_id}",
        outcome=outcome,
        justification=justification
    )

def summarize_replay_clearing_council(council: ReplayClearingCouncilRecord, cases: List[ReplayClearingCouncilCaseRecord]) -> ReplayClearingCouncilHealthRecord:
    open_cases = len([c for c in cases if c.case_status not in [
        ReplayClearingCouncilCaseStatus.case_decided,
        ReplayClearingCouncilCaseStatus.case_decided_with_caveats,
        ReplayClearingCouncilCaseStatus.case_review_only,
        ReplayClearingCouncilCaseStatus.case_blocked,
        ReplayClearingCouncilCaseStatus.case_superseded,
        ReplayClearingCouncilCaseStatus.case_archived
    ]])

    is_healthy = open_cases < 10 # Example threshold
    return ReplayClearingCouncilHealthRecord(
        is_healthy=is_healthy,
        score=1.0 if is_healthy else 0.5
    )

def apply_replay_clearing_council_decision(decision: ReplayClearingCouncilDecisionRecord) -> str:
    return f"Applied decision {decision.decision_id}: {decision.outcome.value}"

def explain_replay_clearing_council_outcome(decision: ReplayClearingCouncilDecisionRecord) -> str:
    return f"Outcome: {decision.outcome.value}. Justification: {decision.justification}"
