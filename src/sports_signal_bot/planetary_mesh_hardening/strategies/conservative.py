from .base import PlanetaryMeshStrategy

class ConservativePlanetaryMeshHardeningStrategy(PlanetaryMeshStrategy):
    def evaluate(self, integration):
        return {"result": "conservative", "blockers": []}
