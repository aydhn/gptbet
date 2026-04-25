from typing import Any, Dict

from sports_signal_bot.probabilistic.basketball.contracts import (
    BasketballDistributionConfig, BasketballScoreEstimate)


class ExpectedPointsBuilder:
    """Builds expected points for home and away teams based on structural features."""

    def build(
        self,
        event_id: str,
        features: Dict[str, Any],
        config: BasketballDistributionConfig,
        model_name: str = "basketball_structural_points_model",
    ) -> BasketballScoreEstimate:
        warnings = []

        # Base Points
        base_total = features.get("base_total_points", config.base_total_points)
        home_adv = features.get("home_advantage_points", config.home_advantage_points)

        # Default split
        base_home = (base_total / 2) + (home_adv / 2)
        base_away = (base_total / 2) - (home_adv / 2)

        # Adjustments
        # These features can be passed directly if the model predicts them or extracted from feature factories
        pace_adjustment = features.get("pace_adjustment", 0.0) * config.pace_weight
        home_off_vs_away_def = (
            features.get("home_off_vs_away_def", 0.0) * config.offense_weight
        )
        away_off_vs_home_def = (
            features.get("away_off_vs_home_def", 0.0) * config.defense_weight
        )
        rating_diff_adj = features.get("rating_diff", 0.0) * config.rating_weight

        # We split pace adjustment evenly, but apply specific offense/defense interaction
        exp_home = (
            base_home
            + (pace_adjustment / 2)
            + home_off_vs_away_def
            + (rating_diff_adj / 2)
        )
        exp_away = (
            base_away
            + (pace_adjustment / 2)
            + away_off_vs_home_def
            - (rating_diff_adj / 2)
        )

        if exp_home < 0:
            warnings.append(f"Expected home points clipped from {exp_home} to 0")
            exp_home = max(0.0, exp_home)
        if exp_away < 0:
            warnings.append(f"Expected away points clipped from {exp_away} to 0")
            exp_away = max(0.0, exp_away)

        return BasketballScoreEstimate(
            event_id=event_id,
            expected_home_points=float(exp_home),
            expected_away_points=float(exp_away),
            expected_total_points=float(exp_home + exp_away),
            expected_margin_home=float(exp_home - exp_away),
            model_name=model_name,
            feature_sources=list(features.keys()),
            warnings=warnings,
        )
