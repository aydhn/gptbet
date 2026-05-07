from typing import Dict, Any
from .base import ContinuityVerificationStrategy
from ..contracts import (
    ObservatoryFederationStatus,
    SchedulerProofLaneStatus,
    AuditPulseCouncilStatus,
    ContinuityEvidenceExchangeStatus
)

class ProofLaneFirstStrategy(ContinuityVerificationStrategy):
    """
    Proof Lane First Strategy:
    - proof freshness, lineage and rollback readiness dominant
    - hidden proof erosion intolerable
    """
    def evaluate_observatory_federation(self, federation: Dict[str, Any]) -> bool:
        return federation.get("status") in [
            ObservatoryFederationStatus.federation_verified,
            ObservatoryFederationStatus.federation_caveated,
            ObservatoryFederationStatus.federation_review_only
        ]

    def evaluate_scheduler_proof_lane(self, lane: Dict[str, Any]) -> bool:
        return lane.get("status") == SchedulerProofLaneStatus.lane_verified

    def evaluate_audit_pulse_council(self, council: Dict[str, Any]) -> bool:
        return council.get("status") in [
            AuditPulseCouncilStatus.council_verified,
            AuditPulseCouncilStatus.council_caveated
        ]

    def evaluate_continuity_evidence_exchange(self, exchange: Dict[str, Any]) -> bool:
        return exchange.get("status") in [
            ContinuityEvidenceExchangeStatus.exchange_verified,
            ContinuityEvidenceExchangeStatus.exchange_caveated
        ]
