import pytest
from src.sports_signal_bot.trace_routing.contracts import (
    CouncilFamily,
    CaseFamily,
    CaseStatus,
    IntegrityDecisionType
)
from src.sports_signal_bot.trace_routing.integrity_councils import (
    build_narrative_integrity_council,
    open_narrative_integrity_case,
    resolve_narrative_integrity_case
)

def test_build_narrative_integrity_council():
    council = build_narrative_integrity_council(
        CouncilFamily.FRESHNESS_INTEGRITY_COUNCIL,
        "quorum_pol", "prec_pol"
    )
    assert council.health_status == "healthy"

def test_open_narrative_integrity_case():
    case = open_narrative_integrity_case(
        CaseFamily.STALE_NARRATIVE_INTEGRITY_CASE,
        ["nar1"], "decision needed"
    )
    assert case.case_status == CaseStatus.CASE_OPENED

def test_resolve_narrative_integrity_case_stale_downgrade():
    case = open_narrative_integrity_case(
        CaseFamily.STALE_NARRATIVE_INTEGRITY_CASE,
        ["nar1"], "decision needed"
    )
    case.input_proof_refs = ["proof_stale_1"]

    decision = resolve_narrative_integrity_case(
        case, IntegrityDecisionType.ACCEPT_BOUNDED_NARRATIVE_WITH_CAPS, []
    )

    assert decision.decision_type == IntegrityDecisionType.DOWNGRADE_TO_REVIEW_ONLY_NARRATIVE
    assert case.case_status == CaseStatus.CASE_DECIDED
