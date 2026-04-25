from typing import Tuple

from sports_signal_bot.ratings.base import BaseRatingEngine
from sports_signal_bot.ratings.contracts import RatingConfig
from sports_signal_bot.ratings.margin import get_margin_multiplier


class EloRatingEngine(BaseRatingEngine):
    def __init__(self, config: RatingConfig):
        super().__init__(config)
        self.scale = 400.0

    def calculate_expected_outcome(
        self, home_rating: float, away_rating: float, is_neutral: bool = False
    ) -> Tuple[float, float]:
        home_adv = (
            0.0
            if is_neutral
            and self.config.neutral_venue_policy == "ignore_home_advantage"
            else self.config.home_advantage
        )
        adjusted_home_rating = home_rating + home_adv
        rating_diff = adjusted_home_rating - away_rating
        expected_home = 1.0 / (1.0 + 10.0 ** (-rating_diff / self.scale))
        expected_away = 1.0 - expected_home
        return expected_home, expected_away

    def _get_actual_outcome_value(
        self, home_score: float, away_score: float
    ) -> Tuple[float, float]:
        if home_score > away_score:
            return 1.0, 0.0
        elif away_score > home_score:
            return 0.0, 1.0
        else:
            return 0.5, 0.5

    def calculate_rating_updates(
        self,
        home_rating: float,
        away_rating: float,
        actual_home_score: float,
        actual_away_score: float,
        is_neutral: bool = False,
    ) -> Tuple[float, float]:
        expected_home, expected_away = self.calculate_expected_outcome(
            home_rating, away_rating, is_neutral
        )
        outcome_home, outcome_away = self._get_actual_outcome_value(
            actual_home_score, actual_away_score
        )
        rating_diff = home_rating - away_rating
        margin_mult = get_margin_multiplier(
            self.config.margin_method,
            actual_home_score,
            actual_away_score,
            rating_diff,
            self.config.margin_cap,
        )
        home_delta = self.config.k_factor * margin_mult * (outcome_home - expected_home)
        away_delta = self.config.k_factor * margin_mult * (outcome_away - expected_away)
        return home_delta, away_delta
