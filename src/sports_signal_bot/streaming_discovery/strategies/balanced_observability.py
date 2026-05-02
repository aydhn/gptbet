from .base import BaseStreamingRoutingStrategy
from ..contracts import AdaptiveRoutingProfileRecord

class BalancedObservabilityFabricStrategy(BaseStreamingRoutingStrategy):
    def get_profile(self) -> AdaptiveRoutingProfileRecord:
        return AdaptiveRoutingProfileRecord(
            base_routing_policy_ref="balanced_default",
            adaptation_bounds={"max_trust_weight_change": 0.25},
            trust_sensitivity=0.1,
            freshness_sensitivity=0.1,
            lag_penalty_policy="linear_penalty",
            anomaly_penalty_policy="moderate_suppression",
            fallback_policy="safe_known_only"
        )
