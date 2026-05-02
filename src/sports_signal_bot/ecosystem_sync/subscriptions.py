from typing import List, Dict, Any, Optional
from datetime import datetime
from .contracts import (
    DiscoverySubscriptionRecord,
    SubscriptionFamily,
    SubscriptionPolicyRecord,
    SyncMode,
    SubscriptionStatus,
    SubscriptionTargetRecord
)

class SubscriptionRegistry:
    """In-memory registry of subscriptions."""
    def __init__(self):
        self._subscriptions: Dict[str, DiscoverySubscriptionRecord] = {}

    def register(self, subscription: DiscoverySubscriptionRecord) -> None:
        self._subscriptions[subscription.subscription_id] = subscription

    def get(self, subscription_id: str) -> Optional[DiscoverySubscriptionRecord]:
        return self._subscriptions.get(subscription_id)

    def list_active(self) -> List[DiscoverySubscriptionRecord]:
        return [
            s for s in self._subscriptions.values()
            if s.current_status in (
                SubscriptionStatus.ACTIVE_SYNCING,
                SubscriptionStatus.ACTIVE_STALE,
                SubscriptionStatus.DEGRADED,
                SubscriptionStatus.AWAITING_FIRST_SYNC
            )
        ]

    def list_all(self) -> List[DiscoverySubscriptionRecord]:
        return list(self._subscriptions.values())


def derive_subscriptions_from_directory(directory_entries: List[Dict[str, Any]], policy: SubscriptionPolicyRecord) -> List[DiscoverySubscriptionRecord]:
    """Derives new subscriptions based on entries in an ecosystem directory."""
    subscriptions = []
    for entry in directory_entries:
        target_id = entry.get("id", f"target_{datetime.utcnow().timestamp()}")
        # Simplification: assume registry catalog family for directory entries
        family = SubscriptionFamily.REGISTRY_CATALOG

        if family in policy.allowed_target_families:
            sub = DiscoverySubscriptionRecord(
                subscription_id=f"sub_{target_id}",
                subscription_family=family,
                target_catalog_ref=target_id,
                target_scope=entry.get("scope", {}),
                subscribed_families=[family],
                refresh_policy=policy,
                trust_policy_ref="default_trust_policy",
                sync_mode=SyncMode.SCHEDULED,
                current_status=SubscriptionStatus.AWAITING_FIRST_SYNC,
                last_success_at=None,
                warnings=[]
            )
            subscriptions.append(sub)
    return subscriptions

def retire_directory_removed_sources(registry: SubscriptionRegistry, active_directory_ids: List[str]) -> List[str]:
    """Retires subscriptions whose targets are no longer in the directory."""
    retired_ids = []
    for sub in registry.list_all():
        if sub.subscription_family == SubscriptionFamily.DIRECTORY:
            continue # Don't retire the directory subscription itself
        if sub.target_catalog_ref not in active_directory_ids:
            sub.current_status = SubscriptionStatus.RETIRED
            retired_ids.append(sub.subscription_id)
    return retired_ids

def refresh_directory_based_routing(registry: SubscriptionRegistry) -> None:
    """Updates routing hints based on directory changes (placeholder)."""
    pass

def summarize_directory_sync_effect(derived_count: int, retired_count: int) -> Dict[str, Any]:
    """Summarizes the effect of a directory sync."""
    return {
        "derived_subscriptions_count": derived_count,
        "retired_subscriptions_count": retired_count
    }
