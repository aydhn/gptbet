class BaseLiveExecutionStrategy:
    def __init__(self):
        self.name = "base"

    def evaluate_live_candidate(self, lane_data: dict) -> bool:
        return False
