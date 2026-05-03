from .base import BaseLiveExecutionStrategy

class ClosureDominantStrategy(BaseLiveExecutionStrategy):
    def __init__(self):
        self.name = "ClosureDominantStrategy"

    def evaluate_live_candidate(self, lane_data: dict) -> bool:
        history = lane_data.get("rehearsal_success_count", 0)
        return history >= 4
