from .base import PerformanceStrategy

class InferenceOptimizedMode(PerformanceStrategy):
    def __init__(self):
        self.name = "inference_optimized"

    def apply(self):
        pass
