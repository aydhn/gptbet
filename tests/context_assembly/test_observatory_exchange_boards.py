import pytest
from sports_signal_bot.context_assembly.exchange_boards import build_observatory_exchange_board
from sports_signal_bot.context_assembly.board_cases import (
    open_observatory_exchange_case,
    resolve_observatory_exchange_case,
    CASE_DECIDED_WITH_CAVEATS,
    CASE_REVIEW_ONLY,
    CASE_BLOCKED
)

def test_resolve_exchange_case_no_safe():
    case = open_observatory_exchange_case("stale_signal_exchange_case", ["ex1"])
    decision = resolve_observatory_exchange_case(case, [], has_quorum=True, has_no_safe_alerts=True, is_degraded=False, is_stale=False)
    assert case.case_status == CASE_DECIDED_WITH_CAVEATS

def test_resolve_exchange_case_stale():
    case = open_observatory_exchange_case("stale_signal_exchange_case", ["ex1"])
    decision = resolve_observatory_exchange_case(case, [], has_quorum=True, has_no_safe_alerts=False, is_degraded=False, is_stale=True)
    assert case.case_status == CASE_BLOCKED

def test_resolve_exchange_case_degraded():
    case = open_observatory_exchange_case("degraded_exchange_case", ["ex1"])
    decision = resolve_observatory_exchange_case(case, [], has_quorum=True, has_no_safe_alerts=False, is_degraded=True, is_stale=False)
    assert case.case_status == CASE_REVIEW_ONLY
