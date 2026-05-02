import pytest
from sports_signal_bot.ecosystem_sync.policies import build_subscription_policy, validate_subscription_scope
from sports_signal_bot.ecosystem_sync.contracts import SubscriptionFamily

def test_build_subscription_policy():
    config = {
        "refresh_policies": {"default_interval_seconds": 3600},
        "allowed_subscription_families": ["registry_catalog_subscription"]
    }
    policy = build_subscription_policy(config)
    assert policy.refresh_interval_hints.interval_seconds == 3600
    assert SubscriptionFamily.REGISTRY_CATALOG in policy.allowed_target_families

def test_validate_subscription_scope():
    config = {
        "allowed_subscription_families": ["registry_catalog_subscription"]
    }
    policy = build_subscription_policy(config)
    assert validate_subscription_scope(policy, SubscriptionFamily.REGISTRY_CATALOG) is True
    assert validate_subscription_scope(policy, SubscriptionFamily.VERIFIER_CATALOG) is False
