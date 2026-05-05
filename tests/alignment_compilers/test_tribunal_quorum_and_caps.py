import pytest
from sports_signal_bot.alignment_compilers.dispute_tribunals import (
    build_context_dispute_tribunal,
    open_context_dispute_case,
    resolve_context_dispute_case
)

def test_tribunal_quorum_and_caps():
    tribunal = build_context_dispute_tribunal("trib-q-1", "family", "quorum-pol-1", "prec-pol-1")
    case = open_context_dispute_case(tribunal, "case-q-1", "case-family", ["ctx-1"])

    # Simulate a decision based on quorum applying caps
    decision = resolve_context_dispute_case(case, "accept_bounded_context_with_caps", ["cap_due_to_quorum"], [])

    assert decision.decision_type == "accept_bounded_context_with_caps"
    assert "cap_due_to_quorum" in decision.caps
    assert case.case_status == "case_decided_with_caveats"
