import pytest
from sports_signal_bot.ecosystem_sync.subscriptions import SubscriptionRegistry, derive_subscriptions_from_directory, retire_directory_removed_sources
from sports_signal_bot.ecosystem_sync.contracts import SubscriptionFamily, SubscriptionStatus
from sports_signal_bot.ecosystem_sync.policies import build_subscription_policy

def test_derive_and_retire():
    policy = build_subscription_policy({"allowed_subscription_families": ["registry_catalog_subscription"]})
    directory = [{"id": "dir_target_1"}]

    subs = derive_subscriptions_from_directory(directory, policy)
    assert len(subs) == 1
    assert subs[0].target_catalog_ref == "dir_target_1"

    registry = SubscriptionRegistry()
    registry.register(subs[0])

    # Retire it by passing an empty list of active targets
    retired = retire_directory_removed_sources(registry, [])
    assert "sub_dir_target_1" in retired
    assert registry.get("sub_dir_target_1").current_status == SubscriptionStatus.RETIRED
