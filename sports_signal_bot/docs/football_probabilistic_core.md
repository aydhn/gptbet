# Football Probabilistic Core

The Football Probabilistic Core is an independent module designed to explicitly model goal scoring distributions for football matches, rather than relying on black-box machine learning models to directly predict market outcomes (like 1X2).

By generating an intermediate expected goals ($\lambda$) parameter for both teams, we can build a full probability distribution (a score matrix) and extract any arbitrary market line consistently.

## Architecture

1. **Strength Mapper**: Maps incoming raw feature data (ratings, form, baselines) to base attacking and defensive strengths.
2. **Lambda Builder**: Computes the expected goals (`home_lambda` and `away_lambda`). Enforces pre-match data purity, applies home advantage, and handles domain clipping.
3. **Score Matrix**: Constructs a 2D numpy array representing $P(Home=i, Away=j)$ using an Independent Poisson assumption up to a `max_goals` cutoff. Handles truncation warnings and renormalization.
4. **Market Extractor**: Deterministically extracts betting probabilities (1X2, Over/Under 2.5, BTTS) and expected metrics from the score matrix.
5. **Correct Score Extractor**: Provides the top-K most likely scorelines for previews.

## Rationale for Independent Poisson
While actual football scores exhibit a slight correlation (e.g., 0-0 or 1-1 draws are more common than perfectly independent models suggest), an Independent Poisson model serves as a robust, mathematically sound baseline.

## Future Extensions
* **Dixon-Coles Adjustment**: A placeholder exists to apply a bivariate adjustment factor ($\rho$) to low-scoring draws to account for correlation.
* **Zero Inflation**: Can be added as a mix-in to handle teams that frequently fail to score.
* **Market Blending**: Can blend these structural probabilities with bookmaker implied probabilities or ML adjustments.
* **Calibration**: The output of this core provides standard probabilities that can be calibrated in downstream pipelines.

## CLI Previews
You can preview the pipeline logic without running a full training loop using the CLI:
```bash
python -m sports_signal_bot.main preview-football-poisson
python -m sports_signal_bot.main preview-football-markets --market 1x2
python -m sports_signal_bot.main preview-correct-scores
```
