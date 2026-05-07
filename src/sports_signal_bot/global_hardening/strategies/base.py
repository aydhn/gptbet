from abc import ABC, abstractmethod
from typing import Dict, Any

class GlobalHardeningStrategy(ABC):
    @abstractmethod
    def evaluate_quorum_mesh(self, mesh_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_planetary_coverage(self, coverage_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_continuity_drill(self, drill_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_recovery_governance(self, gov_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
