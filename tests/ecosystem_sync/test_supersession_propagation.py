import pytest
from sports_signal_bot.ecosystem_sync.supersession import SupersessionPropagator
from sports_signal_bot.ecosystem_sync.subscriptions import SubscriptionRegistry
from sports_signal_bot.ecosystem_sync.contracts import DiscoverySubscriptionRecord, SubscriptionFamily, SyncMode, SubscriptionStatus

def test_supersession_propagation():
    registry = SubscriptionRegistry()
    sub = DiscoverySubscriptionRecord(
        subscription_id="sub_1",
        subscription_family=SubscriptionFamily.REGISTRY_CATALOG,
        target_catalog_ref="old_ref",
        target_scope={},
        subscribed_families=[],
        refresh_policy={"refresh_interval_hints": {"interval_seconds": 10}, "freshness_thresholds": {}, "allowed_target_families": [], "trust_downgrade_triggers": [], "stale_source_suppression_rules": {"threshold_seconds": 10, "suppress": True}, "sync_retry_policy": {"max_attempts": 1, "backoff_factor": 1}, "supersession_required_families": [], "quarantine_on_mismatch_rules": {}, "source_visibility_restrictions": [], "overlay_merge_allowances": {"allow_downgrade": True}},
        trust_policy_ref="default",
        sync_mode=SyncMode.SCHEDULED,
        current_status=SubscriptionStatus.ACTIVE_SYNCING
    )
    registry.register(sub)

    propagator = SupersessionPropagator(registry)
    record = propagator.propagate_supersession("old_ref", "new_ref")

    assert record.superseded_ref == "old_ref"
    assert record.new_ref == "new_ref"

    updated_sub = registry.get("sub_1")
    assert updated_sub.current_status == SubscriptionStatus.SUPERSEDED
    assert updated_sub.target_catalog_ref == "new_ref"
