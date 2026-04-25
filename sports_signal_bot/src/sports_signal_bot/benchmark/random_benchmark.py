import random
from typing import Any, Dict

from sports_signal_bot.labels.contracts import BenchmarkPredictionRecord
from sports_signal_bot.markets.definitions import MarketDefinition

from .base import BaseBenchmark


class RandomBenchmark(BaseBenchmark):
    def __init__(self, seed: int = 42):
        super().__init__(name="random")
        self.rng = random.Random(seed)

    def generate_prediction(
        self,
        event_id: str,
        market_def: MarketDefinition,
        context: Dict[str, Any] = None,
    ) -> BenchmarkPredictionRecord:
        classes = market_def.selection_schema
        if not classes:
            return BenchmarkPredictionRecord(
                event_id=event_id,
                market_type=market_def.market_type,
                benchmark_name=self.name,
            )

        predicted_class = self.rng.choice(classes)
        # Generate random normalized probabilities
        raw_probs = [self.rng.random() for _ in classes]
        total = sum(raw_probs)
        probs = {c: p / total for c, p in zip(classes, raw_probs)}

        return BenchmarkPredictionRecord(
            event_id=event_id,
            market_type=market_def.market_type,
            benchmark_name=self.name,
            predicted_class=predicted_class,
            predicted_probabilities=probs,
        )
