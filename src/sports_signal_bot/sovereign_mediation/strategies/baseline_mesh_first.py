from .base import BaseSovereignMediationStrategy

class BaselineMeshFirstStrategy(BaseSovereignMediationStrategy):
    def evaluate_quorum(self, evidence_refs, caveat_refs):
        if not evidence_refs:
            return "attested_review_only"
        return "attested_with_caveats"

    def evaluate_backplane_flow(self, backpressure_state):
        if backpressure_state == "critical":
            return "flowed_suppressed"
        return "flowed_bounded"

    def evaluate_mesh_projection(self, currentness_state, drift_state):
        if currentness_state == "stale" or drift_state != "none":
            return "projected_caveated_hint"
        return "projected_bounded_hint"

    def evaluate_dispute(self, sovereignty_constraints, replay_state):
        if "sovereignty_deny" in sovereignty_constraints:
            return "preserve_local_deny"
        return "accept_bounded_projection_with_caveats"
