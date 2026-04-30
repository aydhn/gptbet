from abc import ABC, abstractmethod
from typing import Dict, Any
from ..contracts import SimulationRunRecord, SimulationRequestRecord, CandidatePatchRecord

class BaseSimulationStrategy(ABC):
    @abstractmethod
    def run_simulation(self, request: SimulationRequestRecord, patch: CandidatePatchRecord) -> SimulationRunRecord:
        pass
