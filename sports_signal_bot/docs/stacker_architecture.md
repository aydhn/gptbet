# Stacker Architecture

## Purpose
The Stacker layer elevates the ensemble architecture by moving from fixed-weight heuristic ensembles to a learning-based combination approach. It uses meta-learning to understand the biases and behaviors of different prediction sources, creating a more robust final prediction.

## Out-of-Fold (OOF) Integrity
OOF integrity is non-negotiable. Meta-features must be built using OOF predictions to prevent data leakage. If a source's prediction on an event was in-sample during its base training, it must NOT be used to train the stacker.

## Meta-Feature Design
Meta-features are grouped into distinct families to capture different aspects of the underlying signals:
- **Source Probabilities**: Raw class probabilities from each base model.
- **Source Confidence/Sharpness**: Measures like maximum probability and entropy.
- **Source Agreement/Dispersion**: Standard deviation of probabilities across sources for each class.
- **Source Metadata**: Indicator of whether a source is calibrated.
- **Context Features**: Meta-information like missing source count.

## Missing Source Management
Not all sources are available for all events. The stacker handles this by using a configured imputation strategy (e.g., `mean_impute`) and including a context feature (`missing_source_count`) to inform the model when information is degraded.

## Fallback Policy
If the meta-model fails or if available sources drop below a minimum threshold, the system is designed to seamlessly fall back to a rule-based or identity ensemble strategy defined in the config.

## Future Extensions
The stacker architecture lays the groundwork for:
- Dynamic/Regime-conditioned Stacking
- Online Meta-learning
- Integration of new source families (e.g., structural models)
