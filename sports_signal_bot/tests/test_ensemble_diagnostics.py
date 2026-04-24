from sports_signal_bot.ensemble.diagnostics import probability_dispersion, top_class_disagreement, calculate_entropy
import numpy as np

def test_diagnostics():
    probs_list = [
        {"1": 0.5, "X": 0.3, "2": 0.2},
        {"1": 0.3, "X": 0.5, "2": 0.2}
    ]
    classes = ["1", "X", "2"]

    disp = probability_dispersion(probs_list, classes)
    # var(1): mean=0.4, (0.1)^2=0.01. var(X): mean=0.4, 0.01. var(2): mean=0.2, 0
    # mean var = (0.01 + 0.01 + 0) / 3 = 0.00666...
    assert np.isclose(disp, 0.00666666)

    disag = top_class_disagreement(probs_list, classes)
    # 1 vs X
    assert disag == 0.5

    entropy = calculate_entropy({"1": 0.5, "2": 0.5})
    assert np.isclose(entropy, 1.0)
