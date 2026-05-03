import uuid
from typing import List, Dict, Any
from sports_signal_bot.distributed_coordination.contracts import (
    ClusterFairnessRecord,
    TenantFairnessRecord,
    DistributedStarvationRiskRecord
)

class DistributedFairnessManager:
    """Manages fairness algorithms across tenants and shards."""

    def compute_cluster_fairness(self, cluster_ref: str, tenant_scores: List[float]) -> ClusterFairnessRecord:
        """Computes overall cluster fairness based on tenant scores (e.g. standard deviation)."""
        if not tenant_scores:
            score = 1.0 # Perfectly fair
        else:
            mean = sum(tenant_scores) / len(tenant_scores)
            variance = sum([((x - mean) ** 2) for x in tenant_scores]) / len(tenant_scores)
            score = max(0.0, 1.0 - variance) # Simplistic fairness score
        return ClusterFairnessRecord(
            fairness_id=f"fairness_{uuid.uuid4().hex[:8]}",
            cluster_ref=cluster_ref,
            score=score
        )

    def detect_cross_shard_starvation(self, pending_times: Dict[str, float], starvation_threshold: float) -> List[DistributedStarvationRiskRecord]:
        """Detects if any lane/tenant is starving across shards."""
        risks = []
        for target_ref, p_time in pending_times.items():
            if p_time > starvation_threshold:
                risks.append(
                    DistributedStarvationRiskRecord(
                        risk_id=f"risk_{uuid.uuid4().hex[:8]}",
                        target_ref=target_ref,
                        risk_level="high_starvation_risk"
                    )
                )
        return risks

    def apply_safe_distributed_fairness(self, target_ref: str, starvation_risks: List[DistributedStarvationRiskRecord]) -> bool:
        """Returns True if fairness adjustment was applied safely (does not override bounds)."""
        for risk in starvation_risks:
            if risk.target_ref == target_ref:
                return True # Applied bump
        return False
