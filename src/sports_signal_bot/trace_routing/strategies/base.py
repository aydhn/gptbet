from abc import ABC, abstractmethod
from typing import Dict, Any

from ..contracts import (
    ProofCatalogFederationRecord,
    ObservatorySignalExchangeRecord,
    NarrativeIntegrityCouncilRecord,
    SovereignGovernanceTraceRouterRecord
)

class BaseTraceRoutingStrategy(ABC):

    @abstractmethod
    def evaluate_proof_federation(self, federation: ProofCatalogFederationRecord) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_signal_exchange(self, exchange: ObservatorySignalExchangeRecord) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_integrity_council(self, council: NarrativeIntegrityCouncilRecord) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_trace_router(self, router: SovereignGovernanceTraceRouterRecord) -> Dict[str, Any]:
        pass
