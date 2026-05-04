from sports_signal_bot.assurance_exchange.replay_clearing import (
    build_replay_market_clearing_layer,
    build_replay_clearing_book,
    compute_replay_clearing_decision
)

def test_replay_clearing():
    layer = build_replay_market_clearing_layer("test_clearing")
    assert layer.health_status == "healthy"

    book = build_replay_clearing_book("test_family", "test_scope")
    decision = compute_replay_clearing_decision(book)
    assert decision == "no_safe_clearing_path"
    assert book.clearing_status == "clearing_blocked"
