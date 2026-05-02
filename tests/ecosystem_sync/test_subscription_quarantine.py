import pytest
from sports_signal_bot.ecosystem_sync.quarantine import QuarantineManager
from sports_signal_bot.ecosystem_sync.subscriptions import SubscriptionRegistry
from sports_signal_bot.ecosystem_sync.contracts import DiscoverySubscriptionRecord, SubscriptionFamily, SyncMode, SubscriptionStatus

def test_quarantine_flow():
    registry = SubscriptionRegistry()
    sub = DiscoverySubscriptionRecord(
        subscription_id="sub_1",
        subscription_family=SubscriptionFamily.REGISTRY_CATALOG,
        target_catalog_ref="target_1",
        target_scope={},
        subscribed_families=[],
        refresh_policy={"refresh_interval_hints": {"interval_seconds": 10}, "freshness_thresholds": {}, "allowed_target_families": [], "trust_downgrade_triggers": [], "stale_source_suppression_rules": {"threshold_seconds": 10, "suppress": True}, "sync_retry_policy": {"max_attempts": 1, "backoff_factor": 1}, "supersession_required_families": [], "quarantine_on_mismatch_rules": {}, "source_visibility_restrictions": [], "overlay_merge_allowances": {"allow_downgrade": True}},
        trust_policy_ref="default",
        sync_mode=SyncMode.SCHEDULED,
        current_status=SubscriptionStatus.ACTIVE_SYNCING
    )
    registry.register(sub)

    manager = QuarantineManager(registry)

    # Escalate to quarantine
    cluster = manager.escalate_repeated_sync_failures("sub_1", 3)
    assert cluster.failures == 3
    assert registry.get("sub_1").current_status == SubscriptionStatus.QUARANTINED

    # Recover
    manager.recover_subscription_source_if_safe("quar_id", "sub_1")
    assert registry.get("sub_1").current_status == SubscriptionStatus.ACTIVE_SYNCING
