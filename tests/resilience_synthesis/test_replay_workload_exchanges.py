import pytest
from sports_signal_bot.resilience_synthesis.replay_exchanges import (
    build_replay_workload_exchange,
    validate_replay_exchange_packet
)
from sports_signal_bot.resilience_synthesis.contracts import ReplayExchangePacketRecord, ReplayExchangeScopeRecord

def test_build_replay_workload_exchange():
    exc = build_replay_workload_exchange("exc-1")
    assert exc.replay_exchange_id == "exc-1"
    assert exc.exchange_status == "prepared"

def test_validate_replay_exchange_packet():
    packet = ReplayExchangePacketRecord(
        replay_exchange_packet_id="p1",
        workload_ref="w1",
        replay_family="fam",
        required_fidelity="high",
        required_evidence_refs=["ev1"],
        scope_constraints=ReplayExchangeScopeRecord(scope_id="s1")
    )
    assert validate_replay_exchange_packet(packet)

    packet2 = ReplayExchangePacketRecord(
        replay_exchange_packet_id="p2",
        workload_ref="w2",
        replay_family="fam",
        required_fidelity="high",
        required_evidence_refs=[],
        scope_constraints=ReplayExchangeScopeRecord(scope_id="s2")
    )
    assert not validate_replay_exchange_packet(packet2)
