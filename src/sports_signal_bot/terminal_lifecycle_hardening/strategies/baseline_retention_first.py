from .base import BaseTerminalLifecycleStrategy

class BaselineRetentionFirstStrategy(BaseTerminalLifecycleStrategy):
    @property
    def name(self) -> str:
        return "BaselineRetentionFirstStrategy"

    def evaluate(self, integrator) -> dict:
        return {"status": "baseline_retention_focused", "strictness": "medium-high"}
