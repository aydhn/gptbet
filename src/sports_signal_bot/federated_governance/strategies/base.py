from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..contracts import FederatedManifest, ControlPlaneRecord

class BaseFederatedGovernanceStrategy(ABC):

    @abstractmethod
    def evaluate_mesh(self, planes: List[ControlPlaneRecord], context: Dict[str, Any]) -> FederatedManifest:
        """Evaluates the mesh state and returns a governance manifest."""
        pass
