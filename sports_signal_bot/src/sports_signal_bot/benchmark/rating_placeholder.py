from typing import Dict, Any
from .base import BaseBenchmark
from sports_signal_bot.labels.contracts import BenchmarkPredictionRecord
from sports_signal_bot.markets.definitions import MarketDefinition

class SimpleRatingBenchmark(BaseBenchmark):
    def __init__(self):
        super().__init__(name="simple_rating")

    def generate_prediction(self, event_id: str, market_def: MarketDefinition, context: Dict[str, Any] = None) -> BenchmarkPredictionRecord:
        # Placeholder logic: defaults to uniform or naive prediction
        classes = market_def.selection_schema
        if not classes:
             return BenchmarkPredictionRecord(event_id=event_id, market_type=market_def.market_type, benchmark_name=self.name)

        prob = 1.0 / len(classes)
        probs = {c: prob for c in classes}

        return BenchmarkPredictionRecord(
            event_id=event_id,
            market_type=market_def.market_type,
            benchmark_name=self.name,
            predicted_class=classes[0],
            predicted_probabilities=probs
        )
