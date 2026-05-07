from .base import PlanetaryMeshStrategy

class SchedulerAuditFirstStrategy(PlanetaryMeshStrategy):
    def evaluate(self, integration):
        return {"result": "scheduler_first", "blockers": []}
