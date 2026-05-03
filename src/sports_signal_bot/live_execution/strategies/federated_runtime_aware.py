from .base import BaseLiveExecutionStrategy

class FederatedRuntimeAwareStrategy(BaseLiveExecutionStrategy):
    def __init__(self):
        self.name = "FederatedRuntimeAwareStrategy"

    def evaluate_live_candidate(self, lane_data: dict) -> bool:
        fit = lane_data.get("federated_runtime_fit", "unfit_for_lane_runtime")
        return fit == "runtime_fit"
