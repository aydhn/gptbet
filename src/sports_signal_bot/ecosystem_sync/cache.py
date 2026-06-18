from datetime import datetime
from typing import Any, Dict, Optional

from .contracts import (
    EcosystemRoutingRecord,
    RoutingCacheRecord,
    RoutingInvalidationRecord,
)


class RoutingCacheBuilder:
    """Manages the routing cache for fast discovery lookups."""

    def __init__(self, invalidation_rules: Dict[str, Any]):
        self.invalidation_rules = invalidation_rules
        self._cache: Dict[str, RoutingCacheRecord] = {}

    def build_routing_cache(
        self, query_family: str, routing_record: EcosystemRoutingRecord
    ) -> RoutingCacheRecord:
        """Builds and stores a cache record from a routing decision."""
        cache_record = RoutingCacheRecord(
            cache_id=f"cache_{datetime.utcnow().timestamp()}",
            query_family=query_family,
            best_current_candidates=routing_record.selected_route_refs,
            safe_subset_protocol_hints=["minimal_readonly_protocol"],
            freshness_state="fresh",
            required_caveats=[],
            invalidated_candidates=[],
            quarantine_only_candidates=[],
            fallback_candidates=[
                c.candidate_ref
                for c in routing_record.candidate_refs
                if c.candidate_ref not in routing_record.selected_route_refs
            ],
        )
        self._cache[query_family] = cache_record
        return cache_record

    def invalidate_stale_routes(
        self, query_family: str, reason: str
    ) -> Optional[RoutingInvalidationRecord]:
        """Invalidates a cache entry due to staleness or other reasons."""
        if query_family in self._cache:
            record = self._cache[query_family]
            record.freshness_state = "stale"
            record.invalidated_candidates.extend(record.best_current_candidates)
            record.best_current_candidates = []

            return RoutingInvalidationRecord(
                invalidation_id=f"inv_{datetime.utcnow().timestamp()}", reason=reason
            )
        return None

    def update_cache_after_overlay_rebuild(
        self, query_family: str, new_routing: EcosystemRoutingRecord
    ) -> None:
        """Refreshes the cache after an overlay is rebuilt."""
        self.build_routing_cache(query_family, new_routing)

    def summarize_cache_state(self) -> Dict[str, Any]:
        """Summarizes the overall state of the routing cache."""
        stale_queries = 0
        fresh_queries = 0
        for c in self._cache.values():
            if c.freshness_state == "stale":
                stale_queries += 1
            elif c.freshness_state == "fresh":
                fresh_queries += 1

        return {
            "total_cached_queries": len(self._cache),
            "stale_queries": stale_queries,
            "fresh_queries": fresh_queries,
        }

    def detect_sync_vs_cache_drift(
        self, query_family: str, latest_sync_timestamp: datetime
    ) -> bool:
        """Detects if the cache is lagging significantly behind the latest sync."""
        # Simplified check
        cache_record = self._cache.get(query_family)
        if not cache_record:
            return True
        return cache_record.freshness_state == "stale"
