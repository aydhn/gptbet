from sports_signal_bot.assurance_exchange.dashboard_exchanges import (
    build_assurance_dashboard_exchange,
    route_dashboard_exchange,
    summarize_dashboard_exchange
)

def test_build_assurance_dashboard_exchange():
    exchange = build_assurance_dashboard_exchange(
        source_dashboard_refs=["dashboard_1"],
        source_snapshot_refs=["snapshot_1"],
        exchange_scope="test_scope",
        audience_profile_refs=["operator"]
    )

    assert exchange.exchange_status == "prepared"
    assert not exchange.warnings
    assert exchange.exchange_scope == "test_scope"

def test_build_assurance_dashboard_exchange_missing_snapshot():
    exchange = build_assurance_dashboard_exchange(
        source_dashboard_refs=["dashboard_1"],
        source_snapshot_refs=[],
        exchange_scope="test_scope",
        audience_profile_refs=["operator"]
    )

    assert exchange.exchange_status == "prepared_with_warnings"
    assert len(exchange.warnings) == 1
    assert exchange.warnings[0].severity == "high"

def test_route_dashboard_exchange_blocked():
    exchange = build_assurance_dashboard_exchange(
        source_dashboard_refs=["dashboard_1"],
        source_snapshot_refs=[],
        exchange_scope="test_scope",
        audience_profile_refs=["operator"]
    )
    routed = route_dashboard_exchange(exchange)
    assert routed.exchange_status == "exchanged_blocked"
