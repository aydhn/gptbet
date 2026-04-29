from .base import PerformanceStrategy

class SafeDefaultPerformanceMode(PerformanceStrategy):
    def __init__(self):
        self.name = "safe_default"

    def apply(self):
        pass
