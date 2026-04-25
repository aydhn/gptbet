from typing import Any, Dict

from sports_signal_bot.benchmark.base import (BaseBenchmark,
                                              BenchmarkPredictionRecord)
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.markets.definitions import MarketDefinition
from sports_signal_bot.ratings.config import load_rating_config
from sports_signal_bot.ratings.draw_probability import \
    calculate_1x2_probabilities
from sports_signal_bot.ratings.elo import EloRatingEngine

logger = get_logger(__name__)


class RatingBenchmarkEngine(BaseBenchmark):
    def __init__(self):
        super().__init__("elo_rating")
        self._engines: Dict[str, EloRatingEngine] = {}

    def _get_engine(self, sport: str) -> EloRatingEngine:
        if sport not in self._engines:
            config = load_rating_config(sport)
            self._engines[sport] = EloRatingEngine(config)
        return self._engines[sport]

    def _get_snapshot(self, event_id: str, context: Dict[str, Any]) -> Any:
        for s in context.get("rating_snapshots", []):
            if s.event_id == event_id:
                return s
        return None

    def generate_prediction(
        self, event_id: str, market_def: MarketDefinition, context: Dict[str, Any]
    ) -> BenchmarkPredictionRecord:
        snapshot = self._get_snapshot(event_id, context)
        if not snapshot:
            return self._fallback_prediction(event_id, market_def)

        sport_str = (
            snapshot.sport.value
            if isinstance(snapshot.sport, SportType)
            else str(snapshot.sport)
        )
        engine = self._get_engine(sport_str)

        exp_h, exp_a = engine.calculate_expected_outcome(
            snapshot.pre_home_rating, snapshot.pre_away_rating, snapshot.is_neutral
        )

        probs: Dict[str, float] = {}

        m_type = str(market_def.market_type).upper()
        if "1X2" in m_type:
            p_h, p_d, p_a = calculate_1x2_probabilities(
                exp_h, exp_a, engine.config.draw_probability_method
            )
            probs = {"1": p_h, "X": p_d, "2": p_a}
        elif "MONEYLINE" in m_type:
            probs = {"1": exp_h, "2": exp_a}

        else:
            return self._fallback_prediction(event_id, market_def)

        total = sum(probs.values())
        if total > 0:
            probs = {k: v / total for k, v in probs.items()}
        else:
            return self._fallback_prediction(event_id, market_def)

        return BenchmarkPredictionRecord(
            event_id=event_id,
            market_type=str(market_def.market_type),
            benchmark_name=self.name,
            predicted_class=max(probs, key=probs.get),
            predicted_probabilities=probs,
            metadata={"source": "rating_snapshot"},
        )

    def _fallback_prediction(
        self, event_id: str, market_def: MarketDefinition
    ) -> BenchmarkPredictionRecord:
        n = len(market_def.possible_outcomes)
        if n == 0:
            return BenchmarkPredictionRecord(
                event_id=event_id,
                market_type=str(market_def.market_type),
                benchmark_name=self.name,
                predicted_class="unknown",
                predicted_probabilities={},
                metadata={},
            )
        probs = {out: 1.0 / n for out in market_def.possible_outcomes}
        return BenchmarkPredictionRecord(
            event_id=event_id,
            market_type=str(market_def.market_type),
            benchmark_name=self.name,
            predicted_class=market_def.possible_outcomes[0],
            predicted_probabilities=probs,
            metadata={"fallback": True},
        )
