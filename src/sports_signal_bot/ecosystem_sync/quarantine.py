from datetime import datetime
from typing import Dict, Any, List
from .contracts import (
    SubscriptionQuarantineRecord,
    DiscoverySubscriptionRecord,
    SubscriptionStatus,
    QuarantineRecoveryRecord,
    SyncFailureClusterRecord,
    SourceTrustDowngradeRecord
)
from .subscriptions import SubscriptionRegistry

class QuarantineManager:
    """Manages the quarantine lifecycle for subscriptions and sources."""
    def __init__(self, registry: SubscriptionRegistry):
        self.registry = registry

    def quarantine_subscription_source(self, subscription_id: str, reason: str) -> SubscriptionQuarantineRecord:
        """Places a subscription's source into quarantine."""
        sub = self.registry.get(subscription_id)
        if sub:
            sub.current_status = SubscriptionStatus.QUARANTINED

        return SubscriptionQuarantineRecord(
            quarantine_id=f"quar_{datetime.utcnow().timestamp()}",
            subscription_id=subscription_id,
            reason=reason,
            timestamp=datetime.utcnow()
        )

    def recover_subscription_source_if_safe(self, quarantine_id: str, subscription_id: str) -> QuarantineRecoveryRecord:
        """Attempts to recover a subscription from quarantine if conditions are met."""
        sub = self.registry.get(subscription_id)
        if sub and sub.current_status == SubscriptionStatus.QUARANTINED:
            # Mock check: assuming it's safe to recover
            sub.current_status = SubscriptionStatus.ACTIVE_SYNCING

        return QuarantineRecoveryRecord(
            recovery_id=f"recov_{datetime.utcnow().timestamp()}",
            quarantine_id=quarantine_id,
            timestamp=datetime.utcnow()
        )

    def escalate_repeated_sync_failures(self, subscription_id: str, failures: int) -> SyncFailureClusterRecord:
        """Escalates repeated sync failures, potentially triggering quarantine."""
        cluster = SyncFailureClusterRecord(
            cluster_id=f"clust_{datetime.utcnow().timestamp()}",
            failures=failures
        )
        if failures >= 3:
             self.quarantine_subscription_source(subscription_id, "Repeated sync failures")
        return cluster

    def summarize_subscription_quarantine(self, records: List[SubscriptionQuarantineRecord]) -> Dict[str, Any]:
        """Summarizes current quarantine activity."""
        return {
            "total_quarantined": len(records),
            "reasons": list(set(r.reason for r in records))
        }
