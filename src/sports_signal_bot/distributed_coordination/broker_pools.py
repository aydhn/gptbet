import uuid
from typing import List, Dict, Any
from sports_signal_bot.distributed_coordination.contracts import BrokerPoolRecord

class BrokerPoolManager:
    """Manages token broker pools."""

    def build_broker_pool(self, pool_family: str, allocation_strategy: str, failover_policy: str) -> BrokerPoolRecord:
        """Builds a new Broker Pool Record."""
        return BrokerPoolRecord(
            broker_pool_id=f"pool_{uuid.uuid4().hex[:8]}",
            pool_family=pool_family,
            member_broker_refs=[],
            allocation_strategy=allocation_strategy,
            ownership_partitions={},
            renewal_backlog_refs=[],
            failover_policy=failover_policy,
            health_status="healthy",
            warnings=[]
        )

    def summarize_pool_pressure(self, pool: BrokerPoolRecord, total_allocations: int, total_backlog: int) -> Dict[str, Any]:
        """Returns a summary of pool pressure."""
        return {
            "pool_ref": pool.broker_pool_id,
            "health_status": pool.health_status,
            "total_allocations": total_allocations,
            "total_backlog": total_backlog,
            "pressure_index": float(total_backlog) / max(1, float(total_allocations))
        }

    def block_double_allocation(self, pool: BrokerPoolRecord, token_ref: str, active_allocations: List[str]) -> bool:
        """Returns True if double allocation is blocked (i.e. already allocated)."""
        return token_ref in active_allocations
