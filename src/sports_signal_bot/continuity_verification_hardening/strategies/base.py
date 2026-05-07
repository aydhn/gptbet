from abc import ABC, abstractmethod
from typing import Dict, Any

class ContinuityVerificationStrategy(ABC):

    @abstractmethod
    def evaluate_observatory_federation(self, federation: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def evaluate_scheduler_proof_lane(self, lane: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def evaluate_audit_pulse_council(self, council: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def evaluate_continuity_evidence_exchange(self, exchange: Dict[str, Any]) -> bool:
        pass
