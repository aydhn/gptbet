import pytest
from sports_signal_bot.ecosystem_sync.cache import RoutingCacheBuilder
from sports_signal_bot.ecosystem_sync.contracts import EcosystemRoutingRecord, RoutingCandidateRecord, RoutingScoreBreakdownRecord, RoutingStatus

def test_cache_build_and_invalidate():
    builder = RoutingCacheBuilder({})

    routing_record = EcosystemRoutingRecord(
        routing_id="route_1",
        query_ref="query_test",
        candidate_refs=[],
        selected_route_refs=["target_a"],
        weighting_profile="test",
        trust_weight_summary=0.0,
        freshness_weight_summary=0.0,
        compatibility_weight_summary=0.0,
        routing_status=RoutingStatus.SELECTED,
        warnings=[]
    )

    cache_record = builder.build_routing_cache("query_test", routing_record)
    assert cache_record.best_current_candidates == ["target_a"]
    assert cache_record.freshness_state == "fresh"

    inv_record = builder.invalidate_stale_routes("query_test", "stale_source")
    assert inv_record is not None
    assert builder._cache["query_test"].freshness_state == "stale"
    assert builder._cache["query_test"].best_current_candidates == []
    assert "target_a" in builder._cache["query_test"].invalidated_candidates
