import pytest
from sports_signal_bot.ecosystem_sync.sync import EcosystemSyncPlanner, SyncExecutor
from sports_signal_bot.ecosystem_sync.subscriptions import SubscriptionRegistry
from sports_signal_bot.ecosystem_sync.contracts import (
    DiscoverySubscriptionRecord, SubscriptionFamily, SyncMode, SubscriptionStatus
)

def test_sync_planner_builds_plan():
    registry = SubscriptionRegistry()
    # Need to add a mock policy, but using minimal setup for unit test
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

    planner = EcosystemSyncPlanner(registry)
    plan = planner.build_sync_plan(SyncMode.SCHEDULED)

    assert plan.sync_mode == SyncMode.SCHEDULED
    assert "sub_1" in plan.subscriptions_to_sync

def test_sync_executor_executes_step():
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
        current_status=SubscriptionStatus.AWAITING_FIRST_SYNC
    )
    registry.register(sub)

    executor = SyncExecutor(registry)
    res = executor.execute_sync_step("sub_1")

    assert res["status"] == "success"
    assert registry.get("sub_1").current_status == SubscriptionStatus.ACTIVE_SYNCING
