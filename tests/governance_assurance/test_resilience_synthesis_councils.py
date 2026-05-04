import pytest
from sports_signal_bot.governance_assurance.contracts import (
    CouncilFamily, CaseFamily, CaseStatus, CouncilDecisionType
)
from sports_signal_bot.governance_assurance.synthesis_councils import (
    build_resilience_synthesis_council, summarize_synthesis_council
)
from sports_signal_bot.governance_assurance.council_cases import (
    open_synthesis_council_case, collect_synthesis_council_evidence, resolve_synthesis_council_case
)

def test_build_resilience_synthesis_council():
    council = build_resilience_synthesis_council("c1", CouncilFamily.SYNTHESIS_BAND_REVIEW, ["s1", "s2"])
    assert council.synthesis_council_id == "c1"
    assert len(council.governed_synthesis_refs) == 2

    summary = summarize_synthesis_council(council)
    assert summary["family"] == CouncilFamily.SYNTHESIS_BAND_REVIEW.value

def test_council_case_workflow():
    case = open_synthesis_council_case("case1", CaseFamily.SYNTHESIZED_BAND_CONFLICT, ["s1"])
    assert case.case_status == CaseStatus.OPENED

    case = collect_synthesis_council_evidence(case, ["ev1"])
    assert case.case_status == CaseStatus.COLLECTING_EVIDENCE
    assert len(case.warnings) == 0

    case = resolve_synthesis_council_case(case, CouncilDecisionType.PRESERVE_EXISTING_CAP, has_sovereignty_conflict=False)
    assert case.case_status == CaseStatus.DECIDED_WITH_CAVEATS
    assert case.decision.decision_type == CouncilDecisionType.PRESERVE_EXISTING_CAP

def test_council_case_sovereignty_conflict():
    case = open_synthesis_council_case("case2", CaseFamily.SOVEREIGNTY_CAP, ["s2"])
    case = resolve_synthesis_council_case(case, CouncilDecisionType.PRESERVE_EXISTING_CAP, has_sovereignty_conflict=True)
    assert case.case_status == CaseStatus.BLOCKED
    assert case.decision.decision_type == CouncilDecisionType.BLOCK_DUE_TO_UNRESOLVED_CONFLICT
    assert len(case.warnings) > 0
    assert case.warnings[0].severity == "critical"
