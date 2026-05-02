from typing import List, Dict, Any, Set
from datetime import datetime
from .contracts import (
    SupersessionPropagationRecord,
    DiscoverySubscriptionRecord,
    SubscriptionStatus,
    RoutingCacheRecord
)
from .subscriptions import SubscriptionRegistry

class SupersessionPropagator:
    """Handles the propagation of supersession events across the ecosystem."""

    def __init__(self, subscription_registry: SubscriptionRegistry):
        self.subscription_registry = subscription_registry
        self.superseded_refs: Set[str] = set()

    def propagate_supersession(self, old_ref: str, new_ref: str) -> SupersessionPropagationRecord:
        """Propagates a supersession event, marking the old ref as superseded."""
        self.superseded_refs.add(old_ref)

        record = SupersessionPropagationRecord(
            propagation_id=f"prop_{datetime.utcnow().timestamp()}",
            superseded_ref=old_ref,
            new_ref=new_ref,
            timestamp=datetime.utcnow()
        )

        # Update current markers in subscriptions
        self.update_current_markers(old_ref, new_ref)

        return record

    def update_current_markers(self, old_ref: str, new_ref: str) -> None:
        """Updates internal status markers for subscriptions targeting the old ref."""
        for sub in self.subscription_registry.list_all():
            if sub.target_catalog_ref == old_ref:
                sub.current_status = SubscriptionStatus.SUPERSEDED
                sub.target_catalog_ref = new_ref # Attempt auto-forwarding

    def emit_supersession_tombstones(self, superseded_ref: str) -> Dict[str, Any]:
        """Emits a tombstone record for a superseded entry."""
        return {
            "tombstone_ref": superseded_ref,
            "status": "superseded",
            "timestamp": datetime.utcnow().isoformat()
        }

    def summarize_supersession_impact(self, propagation: SupersessionPropagationRecord) -> Dict[str, Any]:
        """Summarizes the impact of a supersession propagation."""
        impacted_subs = [
            sub.subscription_id for sub in self.subscription_registry.list_all()
            if sub.target_catalog_ref == propagation.new_ref and sub.current_status == SubscriptionStatus.SUPERSEDED
        ]

        return {
            "superseded_ref": propagation.superseded_ref,
            "new_ref": propagation.new_ref,
            "impacted_subscriptions": impacted_subs,
            "timestamp": propagation.timestamp.isoformat()
        }
