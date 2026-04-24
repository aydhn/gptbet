import numpy as np
from sklearn.metrics import log_loss, brier_score_loss
from typing import Dict, Any, Optional

from sports_signal_bot.calibration.utils import clip_probabilities

def calculate_log_loss(y_true: np.ndarray, y_prob: np.ndarray, labels: Optional[np.ndarray] = None) -> float:
    """Calculates log loss, handling 1D (binary) and 2D (multiclass) probabilities."""
    y_prob = clip_probabilities(y_prob)
    if labels is None and len(y_prob.shape) == 2:
        labels = np.arange(y_prob.shape[1])
    try:
        return float(log_loss(y_true, y_prob, labels=labels))
    except ValueError:
        return float('nan') # E.g., if only one class is present in y_true

def calculate_brier_score(y_true: np.ndarray, y_prob: np.ndarray, positive_class_index: int = 1) -> float:
    """Calculates Brier score. Currently standard Brier score is binary."""
    # Scikit-learn's brier_score_loss is for binary classification.
    # For multiclass, one typically uses the Brier score definition which sums over all classes.
    if len(y_prob.shape) == 1 or (len(y_prob.shape) == 2 and y_prob.shape[1] == 2):
        # Binary case
        if len(y_prob.shape) == 2:
            y_prob_pos = y_prob[:, positive_class_index]
        else:
            y_prob_pos = y_prob

        # Ensure y_true is 0 or 1 based on positive_class_index
        y_true_binary = (y_true == positive_class_index).astype(int)
        try:
             return float(brier_score_loss(y_true_binary, y_prob_pos))
        except ValueError:
             return float('nan')
    else:
        # Multiclass case (Brier score is sum of squared differences over all classes)
        # B = 1/N * sum( sum( (y_ij - p_ij)^2 ) )
        N = y_true.shape[0]
        C = y_prob.shape[1]

        # One-hot encode y_true
        y_true_onehot = np.zeros((N, C))
        valid_idx = (y_true >= 0) & (y_true < C) # Ignore NaNs or out of bounds
        y_true_onehot[np.arange(N)[valid_idx], y_true[valid_idx].astype(int)] = 1

        brier_score = np.mean(np.sum((y_prob - y_true_onehot)**2, axis=1))
        return float(brier_score)

def calculate_ece_mce(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10, positive_class_index: int = 1) -> tuple[float, float]:
    """
    Calculates Expected Calibration Error (ECE) and Maximum Calibration Error (MCE)
    for a single class (usually the positive class or the predicted class).
    """
    if len(y_prob.shape) == 2:
        if y_prob.shape[1] == 2:
            # Binary, use positive class
            confidences = y_prob[:, positive_class_index]
            accuracies = (y_true == positive_class_index).astype(int)
        else:
             # Multiclass, typical ECE is top-class ECE
             pred_classes = np.argmax(y_prob, axis=1)
             confidences = np.max(y_prob, axis=1)
             accuracies = (y_true == pred_classes).astype(int)
    else:
        confidences = y_prob
        accuracies = (y_true == positive_class_index).astype(int)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    mce = 0.0

    for i, (bin_lower, bin_upper) in enumerate(zip(bin_lowers, bin_uppers)):
        if i == len(bin_lowers) - 1:
            in_bin = (confidences >= bin_lower) & (confidences <= bin_upper)
        else:
            in_bin = (confidences >= bin_lower) & (confidences < bin_upper)

        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])

            error_in_bin = np.abs(avg_confidence_in_bin - accuracy_in_bin)
            ece += prop_in_bin * error_in_bin
            mce = max(mce, error_in_bin)

    return float(ece), float(mce)
