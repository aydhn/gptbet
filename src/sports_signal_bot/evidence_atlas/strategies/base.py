from abc import ABC, abstractmethod
from typing import Dict, Any

class EvidenceAtlasStrategy(ABC):
    @abstractmethod
    def apply_currentness_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def apply_mesh_pressure_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def apply_clearing_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
