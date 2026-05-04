from sports_signal_bot.federation_ecosystem.strategies.base import BaseFederationEcosystemStrategy

class BaselineCatalogFirstStrategy(BaseFederationEcosystemStrategy):
    @property
    def name(self) -> str:
        return "BaselineCatalogFirstStrategy"

    def evaluate_currentness(self, source_state: str, link_status: str) -> str:
        if link_status in ["linked_degraded", "linked_expired", "linked_suspended"]:
            return "stale"
        return "current"

    def evaluate_admission(self, validity: str, caveats: str) -> str:
        if validity != "valid":
            return "blocked_invalid"
        if caveats == "missing_baseline":
            return "blocked_scope_mismatch"
        return "admitted_bounded_exchange"

    def evaluate_visibility(self, participant_status: str, sovereignty_blocked: bool) -> str:
        if sovereignty_blocked:
            return "hidden_due_to_sovereignty"
        return "baseline_visible_only"
