# Training Architecture

This document describes the training architecture for the Sports Signal Bot. The focus of this phase is to establish a rigorous, time-aware, and reproducible training pipeline rather than simply throwing data at a model.

## Why Not Random CV?
In sports forecasting, data is inherently chronological. A team's strength and strategy evolve over time. Randomly splitting data (like standard K-Fold CV) leaks future information into the past. For example, if a model learns that a team won heavily in December, it might unfairly boost predictions for that team in a November test set. All splits and feature generation must strictly respect temporal causality.

## Dataset Assembly Discipline
The `TrainingDatasetBuilder` strictly aligns feature matrices with generated labels based on `event_id`.
- Only valid, resolved outcomes are included.
- Missing values in features are handled by an explicit imputation pipeline (via Scikit-Learn `ColumnTransformer`).
- All data is temporally sorted by `event_datetime_utc` before any splitting occurs.

## Leakage Guards
To ensure integrity, we employ several leakage checks before training:
1.  **Suspicious Column Detection**: We flag columns with names implying post-match information (e.g., `final_score`, `outcome`, `target`).
2.  **Target Exclusion**: We strictly verify that the target column itself does not accidentally sneak into the feature list.
3.  **Strict Temporal Ordering**: The dataset is verified or forced to be sorted by time to allow safe walk-forward validation.

## Split Strategies
We provide multiple time-aware split strategies:
- **HoldoutTimeSplit**: A simple train/valid split based on a percentage of chronologically ordered data.
- **ExpandingWindowSplit / WalkForwardSplit**: Starts with an initial training window, tests on the subsequent window, then expands the training set to include the tested window, repeating the process. This mimics real-world model deployment.
- **RollingWindowSplit**: Similar to Expanding, but the training window size remains fixed, sliding forward through time.

## Preprocessing and Trainer Registry
We use `scikit-learn` pipelines for robust preprocessing (e.g., median imputation, scaling).
Models are managed via a `TrainerRegistry` and `TrainerFactory`, allowing seamless switching between algorithms (e.g., Logistic Regression, Gradient Boosting, Random Forest) via configuration files without altering the orchestration code.

## Validation Predictions and Artifacts
Every training run produces:
-   **Model Artifacts**: The trained models and preprocessors saved via `joblib`.
-   **Training Manifests**: Detailed JSON files summarizing the run, fold metrics, feature counts, and configurations used.
-   **Validation Predictions**: Out-of-fold predictions on the validation sets are saved in a strictly schema'd `ValidationPredictionRecord` format (JSONL).

**Why are Validation Predictions saved?**
Saving out-of-fold predictions is critical for Phase 9 and beyond. These predictions form the basis for:
1.  **Calibration**: Adjusting raw model probabilities to reflect true real-world frequencies.
2.  **Ensembling/Stacking**: Combining multiple models. The meta-model must be trained on the out-of-fold predictions to prevent severe overfitting.
3.  **Benchmark Compatibility**: Our generated prediction schema matches the `BenchmarkPredictionRecord` schema, allowing apples-to-apples evaluation of trained models against random, majority, and bookmaker baselines.
