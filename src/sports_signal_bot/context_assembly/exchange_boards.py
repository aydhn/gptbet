import uuid
from .contracts import ObservatoryExchangeBoardRecord

def build_observatory_exchange_board(family: str, policy_ref: str) -> ObservatoryExchangeBoardRecord:
    board_id = f"oeb_{uuid.uuid4().hex[:8]}"
    return ObservatoryExchangeBoardRecord(
        observatory_exchange_board_id=board_id,
        board_family=family,
        governed_exchange_refs=[],
        participant_refs=[],
        quorum_policy_ref=policy_ref,
        precedence_policy_ref="default_precedence",
        backlog_ref="backlog_main",
        health_status="healthy"
    )

def summarize_observatory_exchange_board(board: ObservatoryExchangeBoardRecord) -> str:
    return f"Board {board.observatory_exchange_board_id} [{board.board_family}] Health: {board.health_status}"
