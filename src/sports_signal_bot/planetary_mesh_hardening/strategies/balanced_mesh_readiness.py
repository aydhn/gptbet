from .base import PlanetaryMeshStrategy

class BalancedMeshReadinessStrategy(PlanetaryMeshStrategy):
    def evaluate(self, integration):
        return {"result": "balanced", "blockers": []}
