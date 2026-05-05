from typing import Dict, Any

class BaseChaosHardeningStrategy:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def apply_fault(self, target: str, fault_type: str) -> bool:
        raise NotImplementedError()

    def check_honesty(self, status: str) -> bool:
        raise NotImplementedError()
