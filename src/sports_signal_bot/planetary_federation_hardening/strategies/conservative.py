from .base import BasePlanetaryFederationHardeningStrategy

class ConservativePlanetaryFederationHardeningStrategy(BasePlanetaryFederationHardeningStrategy):

    def evaluate_mesh_federation(self, state: dict) -> dict:
        stale_members = state.get("stale_members", 0)
        return {"status": "blocked" if stale_members > 0 else "verified"}

    def evaluate_superchain(self, state: dict) -> dict:
        stale_segments = state.get("stale_segments", 0)
        return {"status": "blocked" if stale_segments > 0 else "verified"}

    def evaluate_scheduler_bus(self, state: dict) -> dict:
        drift_ms = state.get("drift_ms", 0)
        return {"status": "blocked" if drift_ms > 0 else "verified"}

    def evaluate_audit_cadence(self, state: dict) -> dict:
        missing_acks = state.get("missing_acks", 0)
        return {"status": "blocked" if missing_acks > 0 else "verified"}
