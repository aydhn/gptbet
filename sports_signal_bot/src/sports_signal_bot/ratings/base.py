from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple

from sports_signal_bot.ratings.contracts import RatingConfig, TeamRatingState


class BaseRatingEngine(ABC):
    def __init__(self, config: RatingConfig):
        self.config = config

    @abstractmethod
    def calculate_expected_outcome(
        self, home_rating: float, away_rating: float, is_neutral: bool = False
    ) -> Tuple[float, float]:
        pass

    @abstractmethod
    def calculate_rating_updates(
        self,
        home_rating: float,
        away_rating: float,
        actual_home_score: float,
        actual_away_score: float,
        is_neutral: bool = False,
    ) -> Tuple[float, float]:
        pass

    def apply_updates(
        self,
        home_state: TeamRatingState,
        away_state: TeamRatingState,
        actual_home_score: float,
        actual_away_score: float,
        is_neutral: bool = False,
    ) -> Tuple[TeamRatingState, TeamRatingState, float, float]:
        home_delta, away_delta = self.calculate_rating_updates(
            home_state.current_rating,
            away_state.current_rating,
            actual_home_score,
            actual_away_score,
            is_neutral,
        )
        home_state.current_rating += home_delta
        home_state.matches_played += 1
        away_state.current_rating += away_delta
        away_state.matches_played += 1
        return home_state, away_state, home_delta, away_delta
