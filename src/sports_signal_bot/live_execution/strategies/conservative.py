from .base import BaseLiveExecutionStrategy

class ConservativeLiveLaneStrategy(BaseLiveExecutionStrategy):
    def __init__(self):
        self.name = "ConservativeLiveLaneStrategy"

    def evaluate_live_candidate(self, lane_data: dict) -> bool:
        history = lane_data.get("rehearsal_success_count", 0)
        return history >= 5
