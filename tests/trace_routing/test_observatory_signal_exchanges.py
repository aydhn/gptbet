import pytest
from src.sports_signal_bot.trace_routing.contracts import (
    ObservatorySignalExchangeFamily,
    ExchangeStatus,
    ObservatorySignalPacketRecord
)
from src.sports_signal_bot.trace_routing.signal_exchanges import (
    build_observatory_signal_exchange,
    validate_observatory_signal_packet
)

def test_build_observatory_signal_exchange():
    exch = build_observatory_signal_exchange(
        ObservatorySignalExchangeFamily.INTERNAL_OBSERVATORY_SIGNAL_EXCHANGE,
        "scope", ["obs1"]
    )
    assert exch.exchange_status == ExchangeStatus.PREPARED

def test_validate_observatory_signal_packet_expired():
    packet = ObservatorySignalPacketRecord(
        signal_packet_id="p1", source_observatory_ref="obs1", source_snapshot_ref="snap1",
        currentness_refs=[], scope_constraints="narrow"
    )
    status = validate_observatory_signal_packet(packet)
    assert status == ExchangeStatus.EXCHANGED_EXPIRED

def test_validate_observatory_signal_packet_blocked_widening():
    packet = ObservatorySignalPacketRecord(
        signal_packet_id="p1", source_observatory_ref="obs1", source_snapshot_ref="snap1",
        currentness_refs=["ref1"], scope_constraints="wide scope"
    )
    status = validate_observatory_signal_packet(packet)
    assert status == ExchangeStatus.EXCHANGED_BLOCKED
