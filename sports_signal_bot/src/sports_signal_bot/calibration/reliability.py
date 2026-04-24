import numpy as np
from typing import List, Optional
from sports_signal_bot.calibration.contracts import ReliabilityBinRecord

def generate_reliability_bins(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
    positive_class_index: int = 1
) -> List[ReliabilityBinRecord]:
    """
    Generates bin-level reliability summaries.
    For binary classification, analyses the positive class.
    For multiclass, analyses the top predicted class confidence (Confidence Calibration).
    """
    if len(y_prob.shape) == 2:
        if y_prob.shape[1] == 2:
            # Binary
            confidences = y_prob[:, positive_class_index]
            accuracies = (y_true == positive_class_index).astype(int)
        else:
            # Multiclass - Top Class Confidence
            pred_classes = np.argmax(y_prob, axis=1)
            confidences = np.max(y_prob, axis=1)
            accuracies = (y_true == pred_classes).astype(int)
    else:
        confidences = y_prob
        accuracies = (y_true == positive_class_index).astype(int)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    records = []

    for i, (bin_lower, bin_upper) in enumerate(zip(bin_lowers, bin_uppers)):
        if i == len(bin_lowers) - 1:
            # Last bin includes exactly 1.0
            in_bin = (confidences >= bin_lower) & (confidences <= bin_upper)
        elif i == 0:
            # First bin includes exactly 0.0
            in_bin = (confidences >= bin_lower) & (confidences < bin_upper)
        else:
            in_bin = (confidences >= bin_lower) & (confidences < bin_upper)

        count = int(np.sum(in_bin))

        if count > 0:
            mean_pred_prob = float(np.mean(confidences[in_bin]))
            emp_freq = float(np.mean(accuracies[in_bin]))
            cal_gap = float(mean_pred_prob - emp_freq)
        else:
            mean_pred_prob = 0.0
            emp_freq = 0.0
            cal_gap = 0.0

        records.append(ReliabilityBinRecord(
            bin_index=i,
            lower_bound=float(bin_lower),
            upper_bound=float(bin_upper),
            count=count,
            mean_predicted_probability=mean_pred_prob,
            empirical_frequency=emp_freq,
            calibration_gap=cal_gap
        ))

    return records
