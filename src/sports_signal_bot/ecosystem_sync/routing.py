from typing import List, Dict, Any, Optional
from datetime import datetime
from .contracts import (
    EcosystemRoutingRecord,
    RoutingCandidateRecord,
    RoutingWeightComponentRecord,
    RoutingScoreBreakdownRecord,
    RoutingPenaltyRecord,
    RoutingStatus,
    RoutingDecisionType,
    RoutingDecisionRecord,
    DriftOutcome
)

class EcosystemRoutingEngine:
    """Trust-weighted ecosystem routing engine."""

    def __init__(self, routing_config: Dict[str, Any]):
        self.config = routing_config
        self.weight_components = routing_config.get("trust_weight_components", {})
        self.penalties = routing_config.get("routing_penalties", {})

    def compute_routing_weights(self, candidate_metadata: Dict[str, Any]) -> RoutingScoreBreakdownRecord:
        """Computes the trust, freshness, and capability weights for a candidate."""
        components = []

        # Mock logic for computing weights based on metadata
        trust_weight = self.weight_components.get("source_trust_weight_max", 40.0) * candidate_metadata.get("trust_ratio", 0.5)
        components.append(RoutingWeightComponentRecord(component_name="trust", weight=trust_weight))

        freshness_weight = self.weight_components.get("freshness_weight_max", 20.0) * candidate_metadata.get("freshness_ratio", 0.8)
        components.append(RoutingWeightComponentRecord(component_name="freshness", weight=freshness_weight))

        cap_weight = self.weight_components.get("capability_fit_weight_max", 15.0) * candidate_metadata.get("capability_ratio", 1.0)
        components.append(RoutingWeightComponentRecord(component_name="capability", weight=cap_weight))

        total = sum(c.weight for c in components)

        return RoutingScoreBreakdownRecord(
            base_score=0.0,
            components=components,
            total_score=total
        )

    def compute_routing_score(self, breakdown: RoutingScoreBreakdownRecord, penalties: List[RoutingPenaltyRecord]) -> float:
        """Computes the final routing score after applying penalties."""
        penalty_total = sum(p.deduction for p in penalties)
        return max(0.0, breakdown.total_score - penalty_total)

    def rank_routing_candidates(self, candidates: List[RoutingCandidateRecord]) -> List[RoutingCandidateRecord]:
        """Ranks candidates by their final score."""
        return sorted(
            candidates,
            key=lambda c: self.compute_routing_score(c.score_breakdown, c.penalties),
            reverse=True
        )

    def explain_routing_recommendation(self, decision: RoutingDecisionRecord) -> str:
        """Provides a human-readable explanation for the routing decision."""
        return f"Decision: {decision.decision_type.value}. Rationale: {decision.rationale}"

    def resolve_trust_freshness_tradeoff(self, trust_score: float, lag_seconds: int) -> str:
        """Resolves tension between a high-trust stale source and low-trust fresh source."""
        if lag_seconds > 86400 and trust_score > 30.0:
             return "prefer_trusted_stale"
        return "prefer_fresh"

    def enforce_capability_floor(self, candidate_caps: List[str], required_caps: List[str]) -> bool:
        """Ensures a candidate meets the minimum required capabilities."""
        return all(cap in candidate_caps for cap in required_caps)

    def prevent_notarization_overweight(self, raw_score: float, max_allowed: float) -> float:
        """Prevents notarization from overwhelming other factors like replay support."""
        return min(raw_score, max_allowed)

    def detect_routing_drift(self, previous_route: EcosystemRoutingRecord, current_candidates: List[RoutingCandidateRecord]) -> DriftOutcome:
        """Detects if the ecosystem has drifted enough to warrant a reroute."""
        if not previous_route.selected_route_refs:
            return DriftOutcome.REROUTE_REQ

        current_top_ref = self.rank_routing_candidates(current_candidates)[0].candidate_ref

        if current_top_ref not in previous_route.selected_route_refs:
            return DriftOutcome.REROUTE_REC

        return DriftOutcome.NO_DRIFT
