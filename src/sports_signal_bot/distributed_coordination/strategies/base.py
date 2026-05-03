from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseDistributedFabricStrategy(ABC):
    """Abstract base strategy for coordinating a distributed execution fabric."""

    @abstractmethod
    def evaluate_cluster_health(self) -> str:
        """Evaluates cluster health."""
        pass

    @abstractmethod
    def resolve_contention(self, contention_family: str) -> str:
        """Resolves cross-node contention."""
        pass

    @abstractmethod
    def evaluate_failover_readiness(self) -> float:
        """Evaluates the readiness to perform a broker or node failover."""
        pass
