from sports_signal_bot.distributed_coordination.strategies.base import BaseDistributedFabricStrategy

class BalancedClusterCoordinationStrategy(BaseDistributedFabricStrategy):
    """
    Balanced strategy: balances pool sharing with isolation,
    preserving safe bounded parallelism where possible.
    """

    def evaluate_cluster_health(self) -> str:
        return "fabric_normal"

    def resolve_contention(self, contention_family: str) -> str:
        if contention_family == "rollback_binding_contention":
            return "reserve_for_rollback_clusterwide"
        return "approve_safe_parallel_subset"

    def evaluate_failover_readiness(self) -> float:
        return 0.7 # Tolerates some lack of readiness if load demands it
