from typing import List
from .contracts import ResilienceActionRecord, DegradationModeRecord

class ResilienceOrchestrator:
    def __init__(self):
        self.action_history: List[ResilienceActionRecord] = []

    def react_to_degradation(self, active_modes: List[DegradationModeRecord]):
        for mode in active_modes:
            if mode.mode_family == "routing_degraded_mode":
                # Action: Quarrantine or suppress
                action = ResilienceActionRecord(
                    action_family="reroute_to_safer_source",
                    target_ref="global_routing_table",
                    reasoning=f"Triggered by active degradation mode: {mode.mode_family}"
                )
                # Ensure idempotency
                if not any(a.action_family == action.action_family for a in self.action_history):
                    self.action_history.append(action)

    def get_actions(self) -> List[ResilienceActionRecord]:
        return self.action_history
