import numpy as np

from sports_signal_bot.ensemble.weights import (derive_source_weight,
                                                normalize_source_weights)


def test_derive_source_weight():
    w1 = derive_source_weight(validation_log_loss=0.5, is_calibrated=False)
    w2 = derive_source_weight(validation_log_loss=0.5, is_calibrated=True)
    w3 = derive_source_weight(validation_log_loss=1.0, is_calibrated=False)

    assert w1 == 2.0
    assert np.isclose(w2, 2.4)
    assert w3 == 1.0


def test_normalize_source_weights():
    weights = {"s1": 2.0, "s2": 6.0}
    norm = normalize_source_weights(weights)
    assert np.isclose(norm["s1"], 0.25)
    assert np.isclose(norm["s2"], 0.75)

    # test zero weights sum
    weights_zero = {"s1": 0.0, "s2": 0.0}
    norm_zero = normalize_source_weights(weights_zero)
    assert np.isclose(norm_zero["s1"], 0.5)
    assert np.isclose(norm_zero["s2"], 0.5)
