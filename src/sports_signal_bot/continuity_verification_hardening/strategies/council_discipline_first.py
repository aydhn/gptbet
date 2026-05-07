from typing import Dict, Any
from .base import ContinuityVerificationStrategy
from ..contracts import (
    ObservatoryFederationStatus,
    SchedulerProofLaneStatus,
    AuditPulseCouncilStatus,
    ContinuityEvidenceExchangeStatus
)

class CouncilDisciplineFirstStrategy(ContinuityVerificationStrategy):
    """
    Council Discipline First Strategy:
    - quorum sufficiency, precedence clarity and caveat carry-forward dominant
    - hidden council gaps intolerable
    """
    def evaluate_observatory_federation(self, federation: Dict[str, Any]) -> bool:
        return federation.get("status") in [
            ObservatoryFederationStatus.federation_verified,
            ObservatoryFederationStatus.federation_caveated
        ]

    def evaluate_scheduler_proof_lane(self, lane: Dict[str, Any]) -> bool:
        return lane.get("status") in [
            SchedulerProofLaneStatus.lane_verified,
            SchedulerProofLaneStatus.lane_caveated,
            SchedulerProofLaneStatus.lane_review_only
        ]

    def evaluate_audit_pulse_council(self, council: Dict[str, Any]) -> bool:
        return council.get("status") == AuditPulseCouncilStatus.council_verified

    def evaluate_continuity_evidence_exchange(self, exchange: Dict[str, Any]) -> bool:
        return exchange.get("status") in [
            ContinuityEvidenceExchangeStatus.exchange_verified,
            ContinuityEvidenceExchangeStatus.exchange_caveated
        ]
