from sports_signal_bot.federation_ecosystem.strategies.base import BaseFederationEcosystemStrategy

class BalancedAttestationHubStrategy(BaseFederationEcosystemStrategy):
    @property
    def name(self) -> str:
        return "BalancedAttestationHubStrategy"

    def evaluate_currentness(self, source_state: str, link_status: str) -> str:
        if link_status in ["linked_degraded", "linked_expired", "linked_suspended"]:
            return "stale"
        if link_status == "linked_caveated":
            return "current_with_caveats"
        return "current"

    def evaluate_admission(self, validity: str, caveats: str) -> str:
        if validity == "expired":
            return "blocked_expired"
        if validity != "valid":
            return "blocked_invalid"
        if caveats == "heavy":
            return "admitted_caveated"
        return "admitted_bounded_exchange"

    def evaluate_visibility(self, participant_status: str, sovereignty_blocked: bool) -> str:
        if sovereignty_blocked:
            return "hidden_due_to_sovereignty"
        if participant_status == "participating_bounded_exchange":
            return "bounded_exchange_visible"
        if participant_status == "participating_review_only":
            return "review_only"
        return "internal_only"
