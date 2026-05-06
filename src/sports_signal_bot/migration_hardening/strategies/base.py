from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseMigrationHardeningStrategy(ABC):
    @abstractmethod
    def evaluate_migration_readiness(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_coordination(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_recovery_chain(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_visibility_wargame(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass
