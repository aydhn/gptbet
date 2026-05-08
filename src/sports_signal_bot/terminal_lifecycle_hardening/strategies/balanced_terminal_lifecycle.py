from .base import BaseTerminalLifecycleStrategy

class BalancedTerminalLifecycleStrategy(BaseTerminalLifecycleStrategy):
    @property
    def name(self) -> str:
        return "BalancedTerminalLifecycleStrategy"

    def evaluate(self, integrator) -> dict:
        return {"status": "balanced", "strictness": "medium"}
