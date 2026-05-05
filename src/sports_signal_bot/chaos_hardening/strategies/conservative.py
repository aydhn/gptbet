from .base import BaseChaosHardeningStrategy

class ConservativeChaosHardeningStrategy(BaseChaosHardeningStrategy):
    def apply_fault(self, target: str, fault_type: str) -> bool:
        return True

    def check_honesty(self, status: str) -> bool:
        if status == "degraded_honestly":
            return True
        return False
