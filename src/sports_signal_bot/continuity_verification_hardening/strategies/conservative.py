from typing import Dict, Any
from .base import ContinuityVerificationStrategy
from ..contracts import (
    ObservatoryFederationStatus,
    SchedulerProofLaneStatus,
    AuditPulseCouncilStatus,
    ContinuityEvidenceExchangeStatus
)

class ConservativeContinuityVerificationStrategy(ContinuityVerificationStrategy):
    """
    Default Strategy:
    - slightest proof staleness, council gap or exchange ambiguity visible
    - stale support rejection strict
    - strong release blocking
    """
    def evaluate_observatory_federation(self, federation: Dict[str, Any]) -> bool:
        return federation.get("status") == ObservatoryFederationStatus.federation_verified

    def evaluate_scheduler_proof_lane(self, lane: Dict[str, Any]) -> bool:
        return lane.get("status") == SchedulerProofLaneStatus.lane_verified

    def evaluate_audit_pulse_council(self, council: Dict[str, Any]) -> bool:
        return council.get("status") == AuditPulseCouncilStatus.council_verified

    def evaluate_continuity_evidence_exchange(self, exchange: Dict[str, Any]) -> bool:
        return exchange.get("status") == ContinuityEvidenceExchangeStatus.exchange_verified
