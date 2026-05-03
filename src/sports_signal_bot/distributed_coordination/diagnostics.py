from typing import Dict, Any
from sports_signal_bot.execution_coordination.contracts import FabricStatus

class DistributedDiagnosticsManager:
    """Manages diagnostics and health checks for the distributed fabric."""

    def compute_distributed_fabric_health(self, active_shards: int, divergence_rate: float, failover_readiness: float) -> FabricStatus:
        """Computes the overall health status of the distributed fabric."""
        if divergence_rate > 0.1:
            return FabricStatus.FABRIC_DEGRADED
        if failover_readiness < 0.5:
            return FabricStatus.FABRIC_CAUTIOUS
        if active_shards > 100: # Simulating high load
            return FabricStatus.FABRIC_CONTENTION_HEAVY

        return FabricStatus.FABRIC_NORMAL

    def explain_health_hotspots(self, health_status: FabricStatus) -> str:
        """Explains why the fabric is in a certain state."""
        explanations = {
            FabricStatus.FABRIC_DEGRADED: "Broker pools are diverging. Lineage risks present.",
            FabricStatus.FABRIC_CAUTIOUS: "Failover candidates are lacking readiness. Snapshot coverage low.",
            FabricStatus.FABRIC_CONTENTION_HEAVY: "High number of active shards causing scheduling saturation.",
            FabricStatus.FABRIC_NORMAL: "Cluster is operating normally."
        }
        return explanations.get(health_status, "Unknown state.")
