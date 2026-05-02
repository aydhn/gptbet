from typing import List, Dict
from .contracts import RoutingAdaptationRecord, DiscoveryEventRecord, AdaptiveRoutingProfileRecord

class AdaptiveTrustRouter:
    def __init__(self, profile: AdaptiveRoutingProfileRecord):
        self.profile = profile
        self.route_weights: Dict[str, float] = {}
        self.history: List[RoutingAdaptationRecord] = []

    def set_baseline(self, route_ref: str, weight: float):
        self.route_weights[route_ref] = weight

    def process_event(self, event: DiscoveryEventRecord):
        # Bounded adaptation logic
        outcome = "no_adjustment"
        adjustment = 0.0
        reasoning = ""

        if event.event_family == "trust_downgraded":
            adjustment = -self.profile.trust_sensitivity
            outcome = "trust_adjusted"
            reasoning = "Trust downgrade event received"
        elif event.event_family == "freshness_degraded":
            adjustment = -self.profile.freshness_sensitivity
            outcome = "freshness_penalty_applied"
            reasoning = "Freshness drift detected"

        if adjustment != 0.0:
            # Bound the adjustment
            max_change = self.profile.adaptation_bounds.get("max_trust_weight_change", 0.2)
            adjustment = max(-max_change, min(max_change, adjustment))

            current_weight = self.route_weights.get(event.source_ref, 1.0)
            new_weight = max(0.0, current_weight + adjustment)
            self.route_weights[event.source_ref] = new_weight

            record = RoutingAdaptationRecord(
                route_ref=f"route_{event.source_ref}",
                source_ref=event.source_ref,
                adaptation_outcome=outcome,
                weight_adjustment=adjustment,
                reasoning=reasoning
            )
            self.history.append(record)

    def get_history(self) -> List[RoutingAdaptationRecord]:
        return self.history
