from typing import Dict, Tuple

import numpy as np

from sports_signal_bot.probabilistic.football.score_matrix import \
    PoissonScoreMatrix


class MarketExtractor:
    """
    Extracts betting market probabilities from a score matrix.
    """

    @staticmethod
    def extract_1x2(score_matrix: PoissonScoreMatrix) -> Dict[str, float]:
        """Returns P(Home), P(Draw), P(Away)"""
        mat = score_matrix.matrix

        home_win = np.sum(np.tril(mat, -1))
        draw = np.sum(np.diag(mat))
        away_win = np.sum(np.triu(mat, 1))

        # Guard against minor floating point sum issues
        total = home_win + draw + away_win
        if total > 0:
            return {
                "home_win": float(home_win / total),
                "draw": float(draw / total),
                "away_win": float(away_win / total),
            }
        return {"home_win": 0.0, "draw": 0.0, "away_win": 0.0}

    @staticmethod
    def extract_over_under(
        score_matrix: PoissonScoreMatrix, line: float
    ) -> Dict[str, float]:
        """Returns P(Over), P(Under) for a specific line (e.g., 2.5)"""
        mat = score_matrix.matrix
        max_g = score_matrix.max_goals

        # Create a matrix where each cell value is (home_goals + away_goals)
        i, j = np.indices((max_g + 1, max_g + 1))
        total_goals = i + j

        over_mask = total_goals > line
        under_mask = total_goals < line

        # We assume half lines (e.g. 2.5), so exact hits are not possible.
        # If integer lines are used in future, push/void logic will be needed.
        prob_over = np.sum(mat[over_mask])
        prob_under = np.sum(mat[under_mask])

        # Normalize in case of slight precision drift or integer line ignores
        total = prob_over + prob_under
        if total > 0:
            return {
                "over": float(prob_over / total),
                "under": float(prob_under / total),
            }
        return {"over": 0.0, "under": 0.0}

    @staticmethod
    def extract_btts(score_matrix: PoissonScoreMatrix) -> Dict[str, float]:
        """Returns P(BTTS Yes), P(BTTS No)"""
        mat = score_matrix.matrix

        # BTTS Yes: home >= 1 and away >= 1
        # Everything except the first row (home=0) and first col (away=0)
        prob_yes = np.sum(mat[1:, 1:])
        prob_no = 1.0 - prob_yes

        # Avoid negative probabilities due to float math
        prob_no = max(0.0, min(1.0, prob_no))
        prob_yes = max(0.0, min(1.0, prob_yes))

        return {"yes": float(prob_yes), "no": float(prob_no)}

    @staticmethod
    def extract_expected_metrics(score_matrix: PoissonScoreMatrix) -> Dict[str, float]:
        """Extract expected goals from the matrix (post-truncation/renormalization)."""
        mat = score_matrix.matrix
        max_g = score_matrix.max_goals

        # Calculate expected values based on the matrix probabilities
        # Sum(i * P(home=i))
        home_goals_range = np.arange(max_g + 1)
        away_goals_range = np.arange(max_g + 1)

        # Marginal probabilities
        home_marginals = np.sum(mat, axis=1)  # sum across columns
        away_marginals = np.sum(mat, axis=0)  # sum across rows

        exp_home = np.sum(home_goals_range * home_marginals)
        exp_away = np.sum(away_goals_range * away_marginals)

        return {
            "expected_home_goals": float(exp_home),
            "expected_away_goals": float(exp_away),
            "expected_total_goals": float(exp_home + exp_away),
            "expected_goal_diff": float(exp_home - exp_away),
        }
