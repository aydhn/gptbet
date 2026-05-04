from .base import BaseSovereignMediationStrategy

class ConservativeQuorumMediationStrategy(BaseSovereignMediationStrategy):
    def evaluate_quorum(self, evidence_refs, caveat_refs):
        if not evidence_refs or len(evidence_refs) < 2:
            return "attested_review_only"
        if caveat_refs:
            return "attested_review_only"
        return "attested_verified"

    def evaluate_backplane_flow(self, backpressure_state):
        if backpressure_state in ["moderate", "high", "critical"]:
            return "flowed_review_only"
        return "flowed_bounded"

    def evaluate_mesh_projection(self, currentness_state, drift_state):
        if currentness_state != "current" or drift_state != "none":
            return "projected_review_only_hint"
        return "projected_bounded_hint"

    def evaluate_dispute(self, sovereignty_constraints, replay_state):
        if "sovereignty_deny" in sovereignty_constraints:
            return "preserve_local_deny"
        return "downgrade_to_review_only"
