import pytest
from sports_signal_bot.alignment_compilers.dispute_tribunals import (
    build_context_dispute_tribunal,
    open_context_dispute_case,
    collect_context_dispute_evidence,
    resolve_context_dispute_case,
    build_tribunal_claim
)
from sports_signal_bot.alignment_compilers.contracts import TribunalEvidenceRecord

def test_build_tribunal():
    tribunal = build_context_dispute_tribunal("tribunal-1", "context_integrity_tribunal", "quorum-pol", "prec-pol")
    assert tribunal.context_dispute_tribunal_id == "tribunal-1"

def test_open_case():
    tribunal = build_context_dispute_tribunal("tribunal-1", "context_integrity_tribunal", "quorum-pol", "prec-pol")
    case = open_context_dispute_case(tribunal, "case-1", "conflicting_context_bundle_case", ["ctx-1"])
    assert case.case_status == "case_opened"

def test_collect_evidence():
    tribunal = build_context_dispute_tribunal("tribunal-1", "context_integrity_tribunal", "quorum-pol", "prec-pol")
    case = open_context_dispute_case(tribunal, "case-1", "family", [])
    collect_context_dispute_evidence(case, [TribunalEvidenceRecord("ev-1", "src", "incomplete")])
    assert case.case_status == "case_collecting_evidence"
    assert len(case.warnings) == 1

def test_resolve_case():
    tribunal = build_context_dispute_tribunal("tribunal-1", "context_integrity_tribunal", "quorum-pol", "prec-pol")
    case = open_context_dispute_case(tribunal, "case-1", "family", [])
    decision = resolve_context_dispute_case(case, "downgrade_to_review_only_context", ["cap1"], [])
    assert case.case_status == "case_review_only"
