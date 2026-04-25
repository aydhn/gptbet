from typing import Any, Dict

from sports_signal_bot.labels.contracts import BenchmarkPredictionRecord
from sports_signal_bot.markets.definitions import MarketDefinition

from .base import BaseBenchmark


class MajorityClassBenchmark(BaseBenchmark):
    def __init__(self, historical_frequencies: Dict[str, Dict[str, float]] = None):
        super().__init__(name="majority_class")
        self.freqs = historical_frequencies or {}

    def generate_prediction(
        self,
        event_id: str,
        market_def: MarketDefinition,
        context: Dict[str, Any] = None,
    ) -> BenchmarkPredictionRecord:
        classes = market_def.selection_schema
        m_type = market_def.market_type

        if not classes:
            return BenchmarkPredictionRecord(
                event_id=event_id, market_type=m_type, benchmark_name=self.name
            )

        market_freqs = self.freqs.get(m_type)
        if market_freqs:
            best_class = max(market_freqs, key=market_freqs.get)
            probs = market_freqs
        else:
            # Fallback to uniform if no history
            best_class = classes[0]
            prob = 1.0 / len(classes)
            probs = {c: prob for c in classes}

        return BenchmarkPredictionRecord(
            event_id=event_id,
            market_type=m_type,
            benchmark_name=self.name,
            predicted_class=best_class,
            predicted_probabilities=probs,
        )
