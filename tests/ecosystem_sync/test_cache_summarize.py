from sports_signal_bot.ecosystem_sync.cache import RoutingCacheBuilder
from sports_signal_bot.ecosystem_sync.contracts import (
    EcosystemRoutingRecord,
    RoutingStatus,
)


def test_summarize_cache_state():
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
        warnings=[],
    )

    builder.build_routing_cache("query_1", routing_record)
    builder.build_routing_cache("query_2", routing_record)

    summary = builder.summarize_cache_state()
    assert summary["total_cached_queries"] == 2
    assert summary["fresh_queries"] == 2
    assert summary["stale_queries"] == 0

    builder.invalidate_stale_routes("query_1", "stale_source")

    summary = builder.summarize_cache_state()
    assert summary["total_cached_queries"] == 2
    assert summary["fresh_queries"] == 1
    assert summary["stale_queries"] == 1
