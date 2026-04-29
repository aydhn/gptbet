from .registry import PerformanceRegistry
from .strategies.safe_default import SafeDefaultPerformanceMode
from .strategies.inference_optimized import InferenceOptimizedMode
from .strategies.backfill_optimized import BackfillOptimizedMode

class PerformanceFactory:
    @staticmethod
    def create_strategy(mode: str):
        if mode == "inference_optimized":
            return InferenceOptimizedMode()
        elif mode == "backfill_optimized":
            return BackfillOptimizedMode()
        return SafeDefaultPerformanceMode()
