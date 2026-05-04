from typing import Dict, Any

from .base import BaseTraceRoutingStrategy
from ..contracts import (
    ProofCatalogFederationRecord,
    ObservatorySignalExchangeRecord,
    NarrativeIntegrityCouncilRecord,
    SovereignGovernanceTraceRouterRecord
)

class IntegrityCouncilFirstStrategy(BaseTraceRoutingStrategy):
    """
    narrative integrity, proof sufficiency ve sovereignty visibility baskın
    weak evidence hızla review_only/no_safe olur
    council caps daha görünür olur
    """

    def evaluate_proof_federation(self, federation: ProofCatalogFederationRecord) -> Dict[str, Any]:
        return {"action": "require_strong_evidence", "reason": "integrity_first"}

    def evaluate_signal_exchange(self, exchange: ObservatorySignalExchangeRecord) -> Dict[str, Any]:
        return {"action": "require_strong_evidence", "reason": "integrity_first"}

    def evaluate_integrity_council(self, council: NarrativeIntegrityCouncilRecord) -> Dict[str, Any]:
        return {"action": "prioritize_caps", "reason": "integrity_first"}

    def evaluate_trace_router(self, router: SovereignGovernanceTraceRouterRecord) -> Dict[str, Any]:
        return {"action": "highlight_caps", "reason": "integrity_first"}
