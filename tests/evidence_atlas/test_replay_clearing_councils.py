import pytest
from sports_signal_bot.evidence_atlas.contracts import (
    ReplayClearingCouncilCaseStatus,
    ReplayClearingDecisionOutcome
)
from sports_signal_bot.evidence_atlas.clearing_councils import (
    build_replay_clearing_council,
    open_replay_clearing_case,
    collect_replay_clearing_evidence,
    resolve_replay_clearing_case,
    summarize_replay_clearing_council
)

def test_build_council():
    council = build_replay_clearing_council("c1", "bounded_clearing_council")
    assert council.replay_clearing_council_id == "c1"

def test_open_and_resolve_case():
    council = build_replay_clearing_council("c1", "bounded_clearing_council")
    case = open_replay_clearing_case(council, "case_1", "bounded_match_conflict_case")

    assert case.case_status == ReplayClearingCouncilCaseStatus.case_opened

    case = collect_replay_clearing_evidence(case, [])
    assert case.case_status == ReplayClearingCouncilCaseStatus.case_collecting_evidence

    decision = resolve_replay_clearing_case(case, ReplayClearingDecisionOutcome.accept_bounded_clearing_with_caveats, "Good match")
    assert case.case_status == ReplayClearingCouncilCaseStatus.case_decided
    assert decision.outcome == ReplayClearingDecisionOutcome.accept_bounded_clearing_with_caveats

def test_summarize_council():
    council = build_replay_clearing_council("c1", "bounded_clearing_council")
    cases = []
    for i in range(12): # Open 12 cases
        cases.append(open_replay_clearing_case(council, f"case_{i}", "f"))

    health = summarize_replay_clearing_council(council, cases)
    assert health.is_healthy is False # Because open_cases (12) > 10 threshold
