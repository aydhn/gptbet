from .base import BaseSovereignMediationStrategy

class BalancedBackplaneFederationStrategy(BaseSovereignMediationStrategy):
    def evaluate_quorum(self, evidence_refs, caveat_refs):
        if not evidence_refs:
            return "attested_review_only"
        if caveat_refs:
            return "attested_with_caveats"
        return "attested_verified"

    def evaluate_backplane_flow(self, backpressure_state):
        if backpressure_state in ["high", "critical"]:
            return "flowed_degraded"
        return "flowed_bounded"

    def evaluate_mesh_projection(self, currentness_state, drift_state):
        if currentness_state == "stale":
            return "projected_caveated_hint"
        if drift_state != "none":
            return "projected_review_only_hint"
        return "projected_bounded_hint"

    def evaluate_dispute(self, sovereignty_constraints, replay_state):
        if "sovereignty_deny" in sovereignty_constraints:
            return "preserve_local_deny"
        if replay_state == "mismatch":
            return "require_replay_rebuild"
        return "accept_bounded_projection_with_caveats"
