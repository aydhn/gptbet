from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseFederationEcosystemStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def evaluate_currentness(self, source_state: str, link_status: str) -> str:
        pass

    @abstractmethod
    def evaluate_admission(self, validity: str, caveats: str) -> str:
        pass

    @abstractmethod
    def evaluate_visibility(self, participant_status: str, sovereignty_blocked: bool) -> str:
        pass
