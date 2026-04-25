from typing import List, Optional, Tuple

import numpy as np
from scipy.stats import poisson

from sports_signal_bot.probabilistic.football.contracts import (
    GoalEnvironmentConfig, GoalLambdaEstimate, ScoreMatrixRecord)


class PoissonScoreMatrix:
    """
    Generates an independent Poisson score probability matrix.
    Rows = home goals, Columns = away goals.
    """

    def __init__(
        self, lambda_estimate: GoalLambdaEstimate, config: GoalEnvironmentConfig
    ):
        self.estimate = lambda_estimate
        self.config = config
        self.max_goals = config.max_goals_cutoff
        self.matrix: np.ndarray = np.zeros((self.max_goals + 1, self.max_goals + 1))
        self.record: Optional[ScoreMatrixRecord] = None
        self._build()

    def _build(self):
        warnings = []
        # Pre-calculate Poisson probabilities up to max_goals
        # x arrays will be 0 to max_goals
        home_probs = poisson.pmf(
            np.arange(self.max_goals + 1), self.estimate.home_lambda
        )
        away_probs = poisson.pmf(
            np.arange(self.max_goals + 1), self.estimate.away_lambda
        )

        # Independent Poisson assumption: P(X=i, Y=j) = P(X=i) * P(Y=j)
        # Using numpy outer product for efficiency
        self.matrix = np.outer(home_probs, away_probs)

        matrix_sum = np.sum(self.matrix)
        truncated_mass = 1.0 - matrix_sum

        renormalized = False

        if truncated_mass > 0.05:
            warnings.append(
                f"High truncated mass warning: {truncated_mass:.4f} probability lost due to max_goals={self.max_goals}"
            )

        if self.config.renormalize_truncated_mass and matrix_sum > 0:
            self.matrix = self.matrix / matrix_sum
            renormalized = True

        self.record = ScoreMatrixRecord(
            event_id=self.estimate.event_id,
            model_name=self.estimate.model_name,
            max_goals=self.max_goals,
            matrix_sum=float(matrix_sum),
            truncated_mass=float(truncated_mass),
            renormalized=renormalized,
            warnings=warnings,
        )

    def get_probability(self, home_goals: int, away_goals: int) -> float:
        """Safe getter for specific scoreline probability."""
        if home_goals > self.max_goals or away_goals > self.max_goals:
            return 0.0
        return float(self.matrix[home_goals, away_goals])
