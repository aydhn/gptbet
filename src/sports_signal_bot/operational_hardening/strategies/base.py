from abc import ABC, abstractmethod

class BaseOperationalHardeningStrategy(ABC):
    @abstractmethod
    def run_hardening_pass(self) -> dict:
        pass
