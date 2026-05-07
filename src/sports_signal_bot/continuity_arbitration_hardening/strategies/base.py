from abc import ABC, abstractmethod

class BaseContinuityArbitrationStrategy(ABC):
    @abstractmethod
    def evaluate_arbitration_health(self) -> str:
        pass

    @abstractmethod
    def handle_stale_proof(self) -> str:
        pass

    @abstractmethod
    def enforce_visibility_ledger(self) -> str:
        pass

class ConservativeContinuityArbitrationStrategy(BaseContinuityArbitrationStrategy):
    def evaluate_arbitration_health(self) -> str:
        return "rail_blocked" # Fails closed easily

    def handle_stale_proof(self) -> str:
        return "reject_stale_proof"

    def enforce_visibility_ledger(self) -> str:
        return "strict_suppression_visibility"

class BalancedArbitrationReadinessStrategy(BaseContinuityArbitrationStrategy):
    def evaluate_arbitration_health(self) -> str:
        return "rail_caveated" # Balanced

    def handle_stale_proof(self) -> str:
        return "reject_stale_proof"

    def enforce_visibility_ledger(self) -> str:
        return "strict_suppression_visibility"

class ProofMeshFirstStrategy(BaseContinuityArbitrationStrategy):
    def evaluate_arbitration_health(self) -> str:
        return "rail_caveated"

    def handle_stale_proof(self) -> str:
        return "reject_stale_proof"

    def enforce_visibility_ledger(self) -> str:
        return "strict_suppression_visibility"

class VisibilityLedgerFirstStrategy(BaseContinuityArbitrationStrategy):
    def evaluate_arbitration_health(self) -> str:
        return "rail_caveated"

    def handle_stale_proof(self) -> str:
        return "reject_stale_proof"

    def enforce_visibility_ledger(self) -> str:
        return "strict_suppression_visibility"
