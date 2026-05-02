from sports_signal_bot.assurance_exchange.compatibility import evaluate_registry_compatibility

def test_evaluate_registry_compatibility():
    res = evaluate_registry_compatibility("strict", "strict", "bundle")
    assert res == "fully_interoperable"

    res = evaluate_registry_compatibility("strict", "loose", "bundle")
    assert res == "review_only_interoperable"
