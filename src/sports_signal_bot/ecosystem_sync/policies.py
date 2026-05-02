from typing import Dict, Any, List
from .contracts import (
    SubscriptionPolicyRecord,
    RefreshWindowRecord,
    RetryPolicyRecord,
    SourceSuppressionRuleRecord,
    SubscriptionFamily,
    OverlayAllowanceRuleRecord
)

def build_subscription_policy(config: Dict[str, Any]) -> SubscriptionPolicyRecord:
    """Builds a SubscriptionPolicyRecord from a configuration dict."""
    refresh_hints = config.get("refresh_policies", {})
    default_interval = refresh_hints.get("default_interval_seconds", 3600)

    thresholds = config.get("stale_source_thresholds", {})
    quarantine_threshold = thresholds.get("quarantine_threshold_seconds", 259200)

    retry_limits = config.get("sync_retry_limits", {})

    return SubscriptionPolicyRecord(
        refresh_interval_hints=RefreshWindowRecord(interval_seconds=default_interval),
        freshness_thresholds={"quarantine_seconds": quarantine_threshold},
        allowed_target_families=[SubscriptionFamily(f) for f in config.get("allowed_subscription_families", [])],
        trust_downgrade_triggers=["missing_notarization", "invalid_digest"],
        stale_source_suppression_rules=SourceSuppressionRuleRecord(
            threshold_seconds=thresholds.get("warning_threshold_seconds", 86400),
            suppress=True
        ),
        sync_retry_policy=RetryPolicyRecord(
            max_attempts=retry_limits.get("max_attempts", 3),
            backoff_factor=retry_limits.get("backoff_factor", 2.0)
        ),
        supersession_required_families=[SubscriptionFamily.PROTOCOL_PROFILE, SubscriptionFamily.REGISTRY_CATALOG],
        quarantine_on_mismatch_rules={"digest_mismatch": True, "signature_invalid": True},
        source_visibility_restrictions=["quarantined_hidden"],
        overlay_merge_allowances=OverlayAllowanceRuleRecord(allow_downgrade=True)
    )

def validate_subscription_scope(policy: SubscriptionPolicyRecord, family: SubscriptionFamily) -> bool:
    """Validates if a subscription family is allowed by the policy."""
    return family in policy.allowed_target_families

def resolve_refresh_schedule(policy: SubscriptionPolicyRecord, family: SubscriptionFamily, custom_hints: Dict[str, int]) -> int:
    """Resolves the correct refresh interval in seconds."""
    if family.value in custom_hints:
        return custom_hints[family.value]
    return policy.refresh_interval_hints.interval_seconds

def summarize_subscription_policy(policy: SubscriptionPolicyRecord) -> Dict[str, Any]:
    """Provides a summary of the subscription policy."""
    return {
        "refresh_interval_seconds": policy.refresh_interval_hints.interval_seconds,
        "allowed_families": [f.value for f in policy.allowed_target_families],
        "max_retries": policy.sync_retry_policy.max_attempts,
        "suppression_threshold_seconds": policy.stale_source_suppression_rules.threshold_seconds
    }
