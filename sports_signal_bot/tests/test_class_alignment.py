from sports_signal_bot.ensemble.alignment import align_probability_vector, validate_market_compatibility

def test_validate_market_compatibility():
    assert validate_market_compatibility(["1", "X", "2"], ["1", "X", "2"]) is True
    assert validate_market_compatibility(["1", "X"], ["1", "X", "2"]) is True
    assert validate_market_compatibility(["1", "X", "2", "3"], ["1", "X", "2"]) is False

def test_align_probability_vector():
    source_probs = {"1": 0.5, "X": 0.3, "2": 0.2}
    source_classes = ["1", "X", "2"]
    target_classes = ["1", "X", "2"]

    aligned = align_probability_vector(source_probs, source_classes, target_classes)
    assert aligned == {"1": 0.5, "X": 0.3, "2": 0.2}

    # Missing class gets 0
    source_probs2 = {"1": 0.6, "X": 0.4}
    source_classes2 = ["1", "X"]
    target_classes2 = ["1", "X", "2"]
    aligned2 = align_probability_vector(source_probs2, source_classes2, target_classes2)
    assert aligned2 == {"1": 0.6, "X": 0.4, "2": 0.0}

    # Incompatible classes
    source_probs3 = {"1": 0.5, "Y": 0.5}
    source_classes3 = ["1", "Y"]
    target_classes3 = ["1", "X", "2"]
    aligned3 = align_probability_vector(source_probs3, source_classes3, target_classes3)
    assert aligned3 is None
