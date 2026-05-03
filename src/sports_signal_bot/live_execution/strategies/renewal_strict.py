from .base import BaseLiveExecutionStrategy

class RenewalStrictStrategy(BaseLiveExecutionStrategy):
    def __init__(self):
        self.name = "RenewalStrictStrategy"

    def evaluate_live_candidate(self, lane_data: dict) -> bool:
        history = lane_data.get("rehearsal_success_count", 0)
        return history >= 3
