from sports_signal_bot.assurance_exchange.federation_boards import (
    build_council_federation_board,
    open_federation_board_case,
    resolve_federation_board_case
)

def test_federation_board_lifecycle():
    board = build_council_federation_board("test_board", ["council_1"], "quorum_1")
    assert board.health_status == "healthy"

    case = open_federation_board_case("test_case", ["council_case_1"], ["synthesis_1"])
    assert case.case_status == "case_opened"

    decision = resolve_federation_board_case(case)
    assert decision.decision_type == "accept_bounded_assurance_with_caps"
    assert case.case_status == "case_decided_with_caveats"

def test_federation_board_sovereignty_failure():
    case = open_federation_board_case("test_case", ["council_case_1"], ["sovereignty_failure"])
    decision = resolve_federation_board_case(case)
    assert decision.decision_type == "block_due_to_unresolved_board_conflict"
    assert case.case_status == "case_blocked"
