from sports_signal_bot.ensemble.alignment import validate_market_compatibility

def test_validate_market_compatibility():
    # True because source is subset
    assert validate_market_compatibility(["1", "X"], ["1", "X", "2"]) is True
    # False because source has extra
    assert validate_market_compatibility(["1", "X", "2", "3"], ["1", "X", "2"]) is False
    # True exact match
    assert validate_market_compatibility(["A", "B"], ["A", "B"]) is True
