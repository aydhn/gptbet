from sports_signal_bot.signal_scoring.contracts import SignalCandidateRecord
from sports_signal_bot.signal_scoring.runner import SignalScoringRunner

def test_runner_initialization_and_flow(tmp_path):
    config = {
        "default_signal_strategy": "edge_focused",
        "weights": {},
        "thresholds": {}
    }

    runner = SignalScoringRunner(config, str(tmp_path))

    cand1 = SignalCandidateRecord(
        event_id="e1", sport="football", market_type="1x2", selection="home",
        final_probability=0.6, market_implied_probability=0.5
    )

    manifest = runner.run([cand1], "football", "1x2")

    assert manifest.total_processed == 1
    assert manifest.scored_count == 1
    assert len(manifest.top_signals) == 1
    assert manifest.top_signals[0].event_id == "e1"
