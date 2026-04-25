from typing import Tuple

from sports_signal_bot.ratings.base import BaseRatingEngine
from sports_signal_bot.ratings.contracts import RatingConfig


class GlickoPlaceholderEngine(BaseRatingEngine):
    def __init__(self, config: RatingConfig):
        super().__init__(config)

    def calculate_expected_outcome(
        self, home_rating: float, away_rating: float, is_neutral: bool = False
    ) -> Tuple[float, float]:
        return 0.5, 0.5

    def calculate_rating_updates(
        self,
        home_rating: float,
        away_rating: float,
        actual_home_score: float,
        actual_away_score: float,
        is_neutral: bool = False,
    ) -> Tuple[float, float]:
        return 0.0, 0.0
