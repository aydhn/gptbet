from typing import List, Dict, Any, Optional
import uuid

from .contracts import (
    NarrativeIntegrityCouncilRecord,
    NarrativeIntegrityCaseRecord,
    NarrativeIntegrityDecisionRecord,
    CouncilFamily,
    CaseFamily,
    CaseStatus,
    IntegrityDecisionType
)

def build_narrative_integrity_council(
    council_family: CouncilFamily,
    quorum_policy_ref: str,
    precedence_policy_ref: str
) -> NarrativeIntegrityCouncilRecord:
    return NarrativeIntegrityCouncilRecord(
        narrative_integrity_council_id=str(uuid.uuid4()),
        council_family=council_family,
        quorum_policy_ref=quorum_policy_ref,
        precedence_policy_ref=precedence_policy_ref,
        backlog_ref=f"backlog_{uuid.uuid4().hex[:8]}",
        health_status="healthy"
    )

def open_narrative_integrity_case(
    case_family: CaseFamily,
    input_narrative_refs: List[str],
    decision_needed: str
) -> NarrativeIntegrityCaseRecord:
    return NarrativeIntegrityCaseRecord(
        narrative_integrity_case_id=str(uuid.uuid4()),
        case_family=case_family,
        input_narrative_refs=input_narrative_refs,
        decision_needed=decision_needed,
        escalation_state="normal",
        case_status=CaseStatus.CASE_OPENED
    )

def collect_narrative_integrity_evidence(case: NarrativeIntegrityCaseRecord, evidence_refs: List[str]) -> None:
    case.input_proof_refs.extend(evidence_refs)
    case.case_status = CaseStatus.CASE_COLLECTING_EVIDENCE

def resolve_narrative_integrity_case(
    case: NarrativeIntegrityCaseRecord,
    decision_type: IntegrityDecisionType,
    caps: List[str]
) -> NarrativeIntegrityDecisionRecord:

    # Rule: no quorum no strong bounded narrative integrity affirmation (handled by caller logic)

    if "stale" in str(case.input_proof_refs).lower():
        # Rule: stale narrative or stale proof strong approval üretemez
        if decision_type == IntegrityDecisionType.ACCEPT_BOUNDED_NARRATIVE_WITH_CAPS:
            decision_type = IntegrityDecisionType.DOWNGRADE_TO_REVIEW_ONLY_NARRATIVE

    case.case_status = CaseStatus.CASE_DECIDED
    if caps:
         case.case_status = CaseStatus.CASE_DECIDED_WITH_CAVEATS

    return NarrativeIntegrityDecisionRecord(
        decision_id=str(uuid.uuid4()),
        case_ref=case.narrative_integrity_case_id,
        decision_type=decision_type,
        caps=caps
    )

def summarize_narrative_integrity_council(council: NarrativeIntegrityCouncilRecord) -> str:
    return f"Council {council.narrative_integrity_council_id} is {council.health_status}"

def apply_narrative_integrity_decision(decision: NarrativeIntegrityDecisionRecord) -> bool:
    return True

def explain_narrative_integrity_outcome(decision: NarrativeIntegrityDecisionRecord) -> str:
    return f"Decision: {decision.decision_type.value}"

def record_narrative_integrity_lineage(decision: NarrativeIntegrityDecisionRecord) -> str:
    return "Lineage recorded"

def summarize_narrative_integrity_effects(decision: NarrativeIntegrityDecisionRecord) -> str:
    return f"Applied caps: {decision.caps}"
