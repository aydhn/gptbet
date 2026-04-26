from sports_signal_bot.inference.pipeline import InferencePipelineExecutor
from sports_signal_bot.inference.resolver import ArtifactResolver


def test_prediction_fallback():
    resolver = ArtifactResolver()
    executor = InferencePipelineExecutor()

    # Chain with stacker
    chain_full = resolver.resolve_chain("football", "1x2")

    base_preds = {
        "predictions": {"evt_1": {"home": 0.5, "away": 0.5}},
        "source": "base_model",
    }

    res_full = executor.resolve_prediction_fallback(base_preds, chain_full)
    assert res_full["source"] == "stacker"

    # Chain without stacker (moneyline mock)
    chain_partial = resolver.resolve_chain("basketball", "moneyline")
    res_partial = executor.resolve_prediction_fallback(base_preds, chain_partial)
    assert res_partial["source"] == "ensemble"
