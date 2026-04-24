# Rating Architecture

The Rating Engine represents Phase 5 of the Sports Signal Bot. It provides a temporal, mathematically sound foundation for estimating team strength using an Elo-based system, designed to be extensible to Glicko or Bayesian methods in the future.

## Purpose
We build rating systems early because raw match outcomes and goals are noisy. A rating system smooths this variance and provides a "latent strength" parameter for every team. This parameter is highly predictive and serves as a core feature for the machine learning models.

## Pre-Event Snapshot Discipline
A core principle of this architecture is temporal consistency.
When generating features for an event that starts at `T`, we strictly use the rating of the team exactly at `T-epsilon`.
The timeline processor deterministically sorts events by time, generates a `RatingSnapshotRecord` for the feature builder, and only then applies the post-match outcome to generate a `RatingUpdateRecord`. This completely prevents data leakage.

## Sport-Aware Elo
The engine shares a common mathematical base but uses configuration files (`football.yaml`, `basketball.yaml`) to adapt:
- **Home Advantage:** Applied dynamically based on the venue. Football generally has a stronger home advantage parameter.
- **Draw Handling:** Football frequently results in draws. The `draw_probability_method` uses a heuristic to allocate probability mass to a draw outcome based on team parity.
- **Margin Weighting:** Basketball games are high-scoring, and point differentials contain signal. We use a dampening function to reward big wins without letting blowouts break the Elo scale. Football uses a more conservative margin weighting.

## Season Transitions
Teams change between seasons. We implement a soft-reset (`apply_season_transition`) that regresses a team's rating towards the base mean depending on a `season_carryover` ratio.

## Benchmark Integration
The Rating Engine seamlessly connects to the Phase 3 Benchmark factory. We can evaluate Elo's raw predictive power against the market or dummy models by converting Elo expected outcomes into probabilities.
