from typing import Dict, List, Any
from abc import ABC, abstractmethod
from ..contracts import PublicationProfileRecord, GatewayIndexEntryRecord

class BasePublicationStrategy(ABC):
    @abstractmethod
    def get_default_profile(self) -> str:
        pass

    @abstractmethod
    def allowed_profiles(self) -> List[str]:
        pass

    @abstractmethod
    def evaluate_quarantine_threshold(self, malformed_intake_rate: float) -> bool:
        pass
