# Calibration Architecture

## Why Calibration is a Separate Layer
In our system, model training and probability calibration are treated as strictly distinct phases. While training aims to optimize predictive power (accuracy, ranking), calibration focuses purely on probability quality and reliability. Treating calibration as a separate layer ensures:
1. **Clean Validation Discipline:** Calibrators are fit on out-of-fold validation predictions, preventing the overfitting that occurs when calibrating on the training set.
2. **Artifact Separation:** We store the raw model artifact and the calibrator artifact separately.
3. **Downstream Ready:** Signal optimization and thresholding logics require trustworthy probabilities. By separating calibration, we guarantee the downstream systems receive standardized, reliable `CalibratedPredictionRecord`s.

## Binary vs Multiclass Calibration
The architecture supports both paradigms via specific wrappers and implementations:
- **Binary:** Direct methods like `BinarySigmoidCalibrator` (Platt Scaling) and `BinaryIsotonicCalibrator` operate on the positive class probability, adjusting it and ensuring $P(0) + P(1) = 1$.
- **Multiclass:** A `MulticlassWrapperCalibrator` applies One-Vs-Rest calibration to each class independently using a base binary method, followed by strict normalization so all probabilities sum to 1. A placeholder for Temperature Scaling is also provided for future expansion when logits become available.

## Reliability Bins and Metrics
To assess probability quality, the system generates:
- **Log Loss & Brier Score:** Standard strictly proper scoring rules.
- **Expected Calibration Error (ECE) & Maximum Calibration Error (MCE):** We group predictions into configurable reliability bins (e.g., 10 equal-width bins). For each bin, we measure the gap between the mean predicted probability and the empirical frequency. ECE is the weighted average of these gaps.

## Artifact and Manifest Structure
Every calibration run produces a `CalibrationRunManifest` that captures:
- Source model metadata
- Method and configuration used
- Raw vs. Calibrated metric comparisons (Delta Log Loss, Delta ECE, etc.)
- Paths to the saved calibrator artifact (`calibrator.joblib`), reliability bins summary (`reliability_bins.json`), and the actual calibrated predictions (`calibrated_predictions.jsonl`).

## Raw vs Calibrated Comparison
A core design principle is side-by-side comparability. The `CalibrationComparisonRecord` automatically highlights whether the calibration improved the ECE and Log Loss, and flags potential overfitting if the validation ECE drops suspiciously low compared to the raw score.

## Future Extension Paths
- **True Temperature Scaling:** Requires modifying the training pipeline to export raw logits alongside probabilities.
- **Dirichlet Calibration:** For advanced, interdependent multiclass calibration.
- **Conformal Prediction:** To provide rigorous prediction intervals around the calibrated probabilities.
