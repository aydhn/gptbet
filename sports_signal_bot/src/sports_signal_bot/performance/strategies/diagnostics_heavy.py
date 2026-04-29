from .base import PerformanceStrategy

class DiagnosticsHeavyMode(PerformanceStrategy):
    def __init__(self):
        self.name = "diagnostics_heavy"

    def apply(self):
        pass
