import pytest
from src.sports_signal_bot.proof_catalogs.narrative_audit_boards import (
    build_narrative_audit_board,
    open_narrative_audit_case,
    resolve_narrative_audit_case
)

def test_build_audit_board():
    board = build_narrative_audit_board("freshness_audit_board")
    assert board.board_family == "freshness_audit_board"

def test_audit_case_lifecycle():
    case = open_narrative_audit_case("stale_narrative_case")
    assert case.case_status == "case_opened"
    resolve_narrative_audit_case(case, "case_decided_with_caveats")
    assert case.case_status == "case_decided_with_caveats"
