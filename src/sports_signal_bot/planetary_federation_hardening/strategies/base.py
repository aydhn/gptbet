from abc import ABC, abstractmethod

class BasePlanetaryFederationHardeningStrategy(ABC):

    @abstractmethod
    def evaluate_mesh_federation(self, state: dict) -> dict:
        pass

    @abstractmethod
    def evaluate_superchain(self, state: dict) -> dict:
        pass

    @abstractmethod
    def evaluate_scheduler_bus(self, state: dict) -> dict:
        pass

    @abstractmethod
    def evaluate_audit_cadence(self, state: dict) -> dict:
        pass
