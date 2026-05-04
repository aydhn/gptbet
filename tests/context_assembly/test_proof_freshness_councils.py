import pytest
from sports_signal_bot.context_assembly.freshness_councils import build_proof_freshness_council
from sports_signal_bot.context_assembly.freshness_cases import (
    open_proof_freshness_case,
    collect_proof_freshness_evidence,
    resolve_proof_freshness_case,
    CASE_REVIEW_ONLY,
    CASE_DECIDED,
    CASE_BLOCKED
)

def test_build_council():
    council = build_proof_freshness_council("proof_currentness_council", "default")
    assert council.council_family == "proof_currentness_council"

def test_resolve_freshness_case_no_quorum():
    case = open_proof_freshness_case("stale_proof_case", ["p1"])
    ev = collect_proof_freshness_evidence(case, {"age_hours": 10})
    decision = resolve_proof_freshness_case(case, [ev], has_quorum=False)
    assert case.case_status == CASE_REVIEW_ONLY

def test_resolve_freshness_case_stale():
    case = open_proof_freshness_case("stale_proof_case", ["p1"])
    ev = collect_proof_freshness_evidence(case, {"age_hours": 100})
    decision = resolve_proof_freshness_case(case, [ev], has_quorum=True)
    assert case.case_status == CASE_BLOCKED

def test_resolve_freshness_case_fresh():
    case = open_proof_freshness_case("borderline_freshness_case", ["p1"])
    ev = collect_proof_freshness_evidence(case, {"age_hours": 5})
    decision = resolve_proof_freshness_case(case, [ev], has_quorum=True)
    assert case.case_status == CASE_DECIDED
