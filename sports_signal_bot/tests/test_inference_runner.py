from datetime import datetime

from sports_signal_bot.inference.runner import InferenceRunner


def test_inference_runner_smoke():
    runner = InferenceRunner()
    result = runner.run(
        "football", "1x2", slot_name="midday", mode="research_live_like_mode"
    )
    assert result is not None

    manifest, decisions, reviews = result
    assert manifest.universe_size > 0
    assert manifest.run_context.slot_id == "midday"

    assert len(decisions) == manifest.universe_size
    assert len(reviews) == manifest.universe_size

    d_packet = decisions[0]
    assert d_packet.sport == "football"
    assert d_packet.market_type == "1x2"
    assert (
        "home" in d_packet.final_probabilities or "over" in d_packet.final_probabilities
    )
