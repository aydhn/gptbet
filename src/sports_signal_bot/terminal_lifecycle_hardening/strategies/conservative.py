from .base import BaseTerminalLifecycleStrategy

class ConservativeTerminalLifecycleStrategy(BaseTerminalLifecycleStrategy):
    @property
    def name(self) -> str:
        return "ConservativeTerminalLifecycleStrategy"

    def evaluate(self, integrator) -> dict:
        return {"status": "conservative", "strictness": "high"}
