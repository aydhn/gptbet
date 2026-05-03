from sports_signal_bot.distributed_coordination.strategies.base import BaseDistributedFabricStrategy

class TenancyFirstCoordinationStrategy(BaseDistributedFabricStrategy):
    """
    Tenancy First strategy: Heavily prioritizes tenant and domain boundary isolation,
    easily sacrificing cross-tenant parallel opportunities to ensure safety.
    """

    def evaluate_cluster_health(self) -> str:
        return "fabric_isolation_stressed"

    def resolve_contention(self, contention_family: str) -> str:
        return "defer_tenant_lane"

    def evaluate_failover_readiness(self) -> float:
        return 0.95 # Extreme safety check before handoff
