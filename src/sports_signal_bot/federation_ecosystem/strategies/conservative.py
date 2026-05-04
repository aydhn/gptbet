from sports_signal_bot.federation_ecosystem.strategies.base import BaseFederationEcosystemStrategy

class ConservativeFederationRegistryStrategy(BaseFederationEcosystemStrategy):
    @property
    def name(self) -> str:
        return "ConservativeFederationRegistryStrategy"

    def evaluate_currentness(self, source_state: str, link_status: str) -> str:
        if source_state != "valid" or link_status != "linked_bounded_exchange":
            return "stale"
        return "current"

    def evaluate_admission(self, validity: str, caveats: str) -> str:
        if validity != "valid":
            return "blocked_invalid"
        if caveats == "heavy":
            return "admitted_review_only"
        return "admitted_bounded_exchange"

    def evaluate_visibility(self, participant_status: str, sovereignty_blocked: bool) -> str:
        if sovereignty_blocked:
            return "hidden_due_to_sovereignty"
        if participant_status == "participating_bounded_exchange":
            return "review_only"
        return "internal_only"
