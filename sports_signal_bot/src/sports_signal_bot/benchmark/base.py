from abc import ABC, abstractmethod
from typing import Any, Dict, List

from sports_signal_bot.labels.contracts import BenchmarkPredictionRecord
from sports_signal_bot.markets.definitions import MarketDefinition


class BaseBenchmark(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_prediction(
        self,
        event_id: str,
        market_def: MarketDefinition,
        context: Dict[str, Any] = None,
    ) -> BenchmarkPredictionRecord:
        pass
