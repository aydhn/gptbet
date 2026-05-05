import pytest
from sports_signal_bot.alignment_compilers.broker_exchanges import (
    build_evidence_broker_exchange,
    route_broker_exchange_packet,
    validate_broker_exchange_packet
)
from sports_signal_bot.alignment_compilers.contracts import BrokerExchangeScopeRecord, BrokerExchangePacketRecord

def test_build_exchange():
    scope = BrokerExchangeScopeRecord(audience_refs=["aud1"], constraints=[])
    exchange = build_evidence_broker_exchange("ex-1", ["src"], ["tgt"], scope, "24h")
    assert exchange.exchange_status == "prepared"

def test_validate_packet():
    packet = BrokerExchangePacketRecord(
        broker_exchange_packet_id="pkt-1",
        source_listing_refs=[],
        source_request_refs=[],
        source_trace_refs=[],
        source_evidence_refs=[],
        evidence_completeness="incomplete",
        currentness_refs=[],
        caveat_refs=[],
        scope_constraints=[],
        warnings=[]
    )
    is_valid = validate_broker_exchange_packet(packet)
    assert not is_valid

def test_route_packet():
    exchange = build_evidence_broker_exchange("ex-1", [], [], BrokerExchangeScopeRecord([], []), "24h")
    packet = BrokerExchangePacketRecord(
        broker_exchange_packet_id="pkt-1",
        source_listing_refs=[],
        source_request_refs=[],
        source_trace_refs=[],
        source_evidence_refs=["ev-1"],
        evidence_completeness="complete",
        currentness_refs=["stale"],
        caveat_refs=[],
        scope_constraints=[],
        warnings=[]
    )
    route = route_broker_exchange_packet(exchange, packet, {})
    assert route.route_status == "revalidation_required_exchange"
