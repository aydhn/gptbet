from typing import List

import numpy as np

from sports_signal_bot.probabilistic.football.contracts import \
    CorrectScoreProbability
from sports_signal_bot.probabilistic.football.score_matrix import \
    PoissonScoreMatrix


class CorrectScoreExtractor:
    """
    Extracts specific correct score probabilities from a score matrix.
    """

    @staticmethod
    def get_top_k(
        score_matrix: PoissonScoreMatrix, k: int = 5
    ) -> List[CorrectScoreProbability]:
        """Returns the top K most probable correct scorelines."""
        mat = score_matrix.matrix

        # Flatten and get indices of top k elements
        # argsort sorts ascending, so we take the last k and reverse
        flat_indices = np.argsort(mat, axis=None)[-k:][::-1]

        # Convert flat indices back to 2D indices (home, away)
        top_k_indices = np.unravel_index(flat_indices, mat.shape)

        results = []
        for i in range(k):
            h_goals = int(top_k_indices[0][i])
            a_goals = int(top_k_indices[1][i])
            prob = float(mat[h_goals, a_goals])
            results.append(
                CorrectScoreProbability(
                    home_goals=h_goals, away_goals=a_goals, probability=prob
                )
            )

        return results
