from .base import PlanetaryMeshStrategy

class ChainIntegrityFirstStrategy(PlanetaryMeshStrategy):
    def evaluate(self, integration):
        return {"result": "chain_first", "blockers": []}
