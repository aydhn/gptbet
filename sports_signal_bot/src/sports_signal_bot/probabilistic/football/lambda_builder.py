from typing import Dict, Any, List
from sports_signal_bot.probabilistic.football.contracts import LambdaBuildContext, GoalLambdaEstimate
from sports_signal_bot.probabilistic.football.strength_mapper import StrengthMapper

class GoalLambdaBuilder:
    """
    Builds Poisson lambda parameters (expected goals) for home and away teams.
    Ensures pre-match logic, no negative lambdas, and applies domain constraints.
    """

    def __init__(self, strength_mapper: StrengthMapper = None):
        self.strength_mapper = strength_mapper or StrengthMapper()

    def build(self, context: LambdaBuildContext, features: Dict[str, float]) -> GoalLambdaEstimate:
        warnings: List[str] = []

        # 1. Leakage guard: Ensure we aren't seeing actual goals
        if "final_home_score" in features or "final_away_score" in features:
            warnings.append("LEAKAGE_WARNING: Final score present in features. Ignoring for lambda estimation.")

        # 2. Extract strengths and baseline
        home_str, away_str, base_total = self.strength_mapper.map_strengths(context, features)

        # 3. Apply Home Advantage
        home_advantage = features.get("home_advantage", context.config.home_advantage_goal_bonus)

        # 4. Calculate raw lambdas
        # Simple additive model for home advantage.
        # Base expected goals per team is roughly base_total / 2
        base_team_exp = base_total / 2.0

        raw_home_lambda = (base_team_exp * home_str) + home_advantage
        raw_away_lambda = (base_team_exp * away_str)

        # 5. Domain Constraints & Clipping
        home_lambda = self._clip_lambda(raw_home_lambda, context.config.lambda_min, context.config.lambda_max)
        away_lambda = self._clip_lambda(raw_away_lambda, context.config.lambda_min, context.config.lambda_max)

        if home_lambda != raw_home_lambda:
            warnings.append(f"Home lambda clipped from {raw_home_lambda:.2f} to {home_lambda:.2f}")
        if away_lambda != raw_away_lambda:
            warnings.append(f"Away lambda clipped from {raw_away_lambda:.2f} to {away_lambda:.2f}")

        # 6. Construct output
        expected_total = home_lambda + away_lambda
        expected_diff = home_lambda - away_lambda

        return GoalLambdaEstimate(
            event_id=context.event_id,
            home_lambda=home_lambda,
            away_lambda=away_lambda,
            expected_total_goals=expected_total,
            expected_goal_diff=expected_diff,
            model_name=context.model_name,
            feature_sources=list(features.keys()),
            warnings=warnings
        )

    def _clip_lambda(self, val: float, min_val: float, max_val: float) -> float:
        if val < min_val:
            return min_val
        if val > max_val:
            return max_val
        return val
