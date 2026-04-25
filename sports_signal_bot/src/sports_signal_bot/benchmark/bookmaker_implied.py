from typing import Any, Dict, List

from sports_signal_bot.labels.contracts import BenchmarkPredictionRecord
from sports_signal_bot.markets.definitions import MarketDefinition

from .base import BaseBenchmark


def decimal_odds_to_implied_prob(odds: float) -> float:
    if odds <= 1.0:
        return 0.0
    return 1.0 / odds


def normalize_overround(probs: Dict[str, float]) -> Dict[str, float]:
    total_prob = sum(probs.values())
    if total_prob == 0:
        return probs
    return {k: v / total_prob for k, v in probs.items()}


def odds_snapshot_to_market_probs(
    snapshot: List[Any], market_def: MarketDefinition
) -> Dict[str, float]:
    """
    Takes a list of CanonicalOddsRecord matching the market_def,
    returns normalized probabilities per class.
    """
    raw_probs = {}
    for rec in snapshot:
        # Assuming rec.selection maps to market_def.selection_schema
        # This mapping can be complex, using simple match here for now
        sel = str(rec.selection).lower()
        if sel in market_def.selection_schema:
            raw_probs[sel] = decimal_odds_to_implied_prob(rec.decimal_odds)

    # Handle missing selections
    for c in market_def.selection_schema:
        if c not in raw_probs:
            raw_probs[c] = 0.0

    return normalize_overround(raw_probs)


class BookmakerImpliedBenchmark(BaseBenchmark):
    def __init__(self):
        super().__init__(name="bookmaker_implied")

    def generate_prediction(
        self,
        event_id: str,
        market_def: MarketDefinition,
        context: Dict[str, Any] = None,
    ) -> BenchmarkPredictionRecord:
        context = context or {}
        snapshot = context.get("odds_snapshot", [])

        if not snapshot:
            # Graceful degrade
            return BenchmarkPredictionRecord(
                event_id=event_id,
                market_type=market_def.market_type,
                benchmark_name=self.name,
            )

        probs = odds_snapshot_to_market_probs(snapshot, market_def)
        predicted_class = max(probs, key=probs.get) if probs else None

        return BenchmarkPredictionRecord(
            event_id=event_id,
            market_type=market_def.market_type,
            benchmark_name=self.name,
            predicted_class=predicted_class,
            predicted_probabilities=probs,
        )
