from typing import List, Optional
from sports_signal_bot.governance_assurance.contracts import (
    SynthesisCouncilCaseRecord,
    CaseFamily,
    CaseStatus,
    CouncilDecisionType,
    SynthesisCouncilDecisionRecord,
    SynthesisCouncilWarningRecord
)

def open_synthesis_council_case(
    case_id: str,
    case_family: CaseFamily,
    input_synthesis_refs: List[str]
) -> SynthesisCouncilCaseRecord:
    return SynthesisCouncilCaseRecord(
        synthesis_case_id=case_id,
        case_family=case_family,
        input_synthesis_refs=input_synthesis_refs,
        input_compiler_refs=[],
        input_debt_refs=[],
        input_replay_refs=[],
        input_portfolio_refs=[],
        decision_needed="requires_bounded_review",
        escalation_state="normal",
        case_status=CaseStatus.OPENED,
        warnings=[]
    )

def collect_synthesis_council_evidence(case: SynthesisCouncilCaseRecord, evidence_refs: List[str]) -> SynthesisCouncilCaseRecord:
    case.case_status = CaseStatus.COLLECTING_EVIDENCE
    # Mock evidence collection
    if len(evidence_refs) == 0:
        case.warnings.append(SynthesisCouncilWarningRecord(warning_id="no_evidence", message="No evidence provided", severity="high"))
    return case

def resolve_synthesis_council_case(
    case: SynthesisCouncilCaseRecord,
    decision_type: CouncilDecisionType,
    has_sovereignty_conflict: bool = False
) -> SynthesisCouncilCaseRecord:

    if has_sovereignty_conflict:
        # Enforce sovereignty rule: block if conflict exists
        decision_type = CouncilDecisionType.BLOCK_DUE_TO_UNRESOLVED_CONFLICT
        case.warnings.append(SynthesisCouncilWarningRecord(
            warning_id="sovereignty_conflict",
            message="Local sovereignty deny block encountered",
            severity="critical"
        ))

    case.decision = SynthesisCouncilDecisionRecord(
        decision_id=f"dec_{case.synthesis_case_id}",
        decision_type=decision_type,
        cap_refs=["default_cap" if decision_type != CouncilDecisionType.BLOCK_DUE_TO_UNRESOLVED_CONFLICT else "blocked_cap"],
        caveat_refs=["sovereignty_preserved"],
        explanation="Decision formulated based on bounded review"
    )

    if decision_type == CouncilDecisionType.BLOCK_DUE_TO_UNRESOLVED_CONFLICT:
        case.case_status = CaseStatus.BLOCKED
    else:
        case.case_status = CaseStatus.DECIDED_WITH_CAVEATS

    return case

def apply_synthesis_council_decision(case: SynthesisCouncilCaseRecord) -> str:
    """Applies the decision, returning the resulting capped score status or block."""
    if case.case_status == CaseStatus.BLOCKED:
        return "blocked_by_sovereignty"
    return "applied_with_caps"
