from typing import List, Dict, Any, Optional
from datetime import datetime
from .contracts import (
    SyncPlanRecord,
    EcosystemSyncRunRecord,
    DiscoverySubscriptionRecord,
    SyncMode,
    SyncLagRecord,
    SubscriptionStatus,
    SyncWarningRecord
)
from .subscriptions import SubscriptionRegistry
from .lag import compute_sync_lag
from .checkpoints import create_sync_checkpoint

class EcosystemSyncPlanner:
    """Plans continuous sync executions based on policies and lag."""

    def __init__(self, subscription_registry: SubscriptionRegistry):
        self.registry = subscription_registry

    def build_sync_plan(self, sync_mode: SyncMode) -> SyncPlanRecord:
        """Builds a plan detailing which subscriptions need syncing."""
        subs_to_sync = []
        for sub in self.registry.list_active():
            # In a real system, we'd check `last_success_at` against the `refresh_interval`
            subs_to_sync.append(sub.subscription_id)

        return SyncPlanRecord(
            plan_id=f"plan_{datetime.utcnow().timestamp()}",
            subscriptions_to_sync=subs_to_sync,
            sync_mode=sync_mode,
            timestamp=datetime.utcnow()
        )

class SyncExecutor:
    """Executes a sync plan."""

    def __init__(self, registry: SubscriptionRegistry):
        self.registry = registry

    def execute_sync_step(self, subscription_id: str) -> Dict[str, Any]:
        """Executes a single step of the sync plan for a subscription."""
        sub = self.registry.get(subscription_id)
        if not sub:
            return {"status": "error", "message": "Subscription not found"}

        # Mock fetching data
        sub.last_success_at = datetime.utcnow()

        if sub.current_status == SubscriptionStatus.AWAITING_FIRST_SYNC:
             sub.current_status = SubscriptionStatus.ACTIVE_SYNCING

        # Create a mock checkpoint
        chk = create_sync_checkpoint(sub.target_catalog_ref, sub.target_catalog_ref, "digest_src", "digest_loc")
        lag_record = compute_sync_lag(chk, datetime.utcnow())

        return {
            "status": "success",
            "subscription_id": subscription_id,
            "lag_record": lag_record
        }

    def validate_sync_results(self, results: List[Dict[str, Any]]) -> bool:
        """Validates that sync results meet minimum integrity standards."""
        return all(r.get("status") == "success" for r in results)

    def summarize_sync_run(self, run_record: EcosystemSyncRunRecord) -> Dict[str, Any]:
        """Summarizes a complete sync run."""
        return {
            "run_id": run_record.run_id,
            "status": run_record.status,
            "duration_seconds": (run_record.end_time - run_record.start_time).total_seconds() if run_record.end_time else 0,
            "lag_records_count": len(run_record.lag_records)
        }
