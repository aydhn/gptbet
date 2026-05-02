from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..contracts import (
    EcosystemSyncRunRecord,
    DiscoverySubscriptionRecord,
    CatalogOverlayRecord,
    EcosystemRoutingRecord
)

class BaseEcosystemSyncStrategy(ABC):
    """Abstract base class for ecosystem sync and routing strategies."""

    @abstractmethod
    def execute_pass(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a full sync, overlay, and routing pass according to the strategy."""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Returns the name of the strategy."""
        pass
