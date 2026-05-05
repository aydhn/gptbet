from abc import ABC, abstractmethod
from typing import List
from src.sports_signal_bot.assurance_synthesizers.contracts import (
    AssuranceSynthesisInputRecord, AssuranceBand
)

class AssuranceSynthesizerStrategy(ABC):
    @abstractmethod
    def evaluate(self, inputs: List[AssuranceSynthesisInputRecord]) -> AssuranceBand:
        pass
