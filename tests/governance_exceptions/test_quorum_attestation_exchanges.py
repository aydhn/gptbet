import pytest
from sports_signal_bot.governance_exceptions.contracts import QuorumExchangePacketRecord, QuorumExchangeConstraintRecord
from sports_signal_bot.governance_exceptions.quorum_exchanges import validate_quorum_exchange_packet

def test_validate_quorum_exchange_packet_success():
    packet = QuorumExchangePacketRecord(
        quorum_exchange_packet_id="test_id",
        source_attestation_ref="att_ref",
        source_decision_lineage_refs=[],
        attested_decision_type="governance_hint",
        preserved_vote_refs=[],
        preserved_evidence_refs=[],
        caveat_refs=["caveat_1"],
        currentness_refs=[],
        scope_constraints=QuorumExchangeConstraintRecord(
            max_caveat_count=5,
            require_fresh_evidence=True
        ),
        warnings=[]
    )
    assert validate_quorum_exchange_packet(packet) is True

def test_validate_quorum_exchange_packet_missing_caveats():
    packet = QuorumExchangePacketRecord(
        quorum_exchange_packet_id="test_id",
        source_attestation_ref="att_ref",
        source_decision_lineage_refs=[],
        attested_decision_type="governance_hint",
        preserved_vote_refs=[],
        preserved_evidence_refs=[],
        caveat_refs=[],
        currentness_refs=[],
        scope_constraints=QuorumExchangeConstraintRecord(
            max_caveat_count=5,
            require_fresh_evidence=True
        ),
        warnings=[]
    )
    assert validate_quorum_exchange_packet(packet) is False
    assert len(packet.warnings) == 1
    assert packet.warnings[0].warning_code == "MISSING_CAVEATS"

from sports_signal_bot.governance_exceptions.contracts import BuildQuorumAttestationExchangeParams
from sports_signal_bot.governance_exceptions.quorum_exchanges import build_quorum_attestation_exchange

def test_build_quorum_attestation_exchange():
    params = BuildQuorumAttestationExchangeParams(
        source_attestation_refs=["att1"],
        source_council_refs=["council1"],
        target_scope_refs=["target1"],
        allowed_domains=["domain1"],
        time_window_seconds=3600,
        preserved_caveat_refs=["caveat1"],
        currentness_refs=["currentness1"],
        validity_window=86400,
        replay_support_refs=["replay1"]
    )

    exchange = build_quorum_attestation_exchange(params)

    assert exchange.source_attestation_refs == ["att1"]
    assert exchange.source_council_refs == ["council1"]
    assert exchange.target_scope_refs == ["target1"]
    assert exchange.exchange_scope.allowed_domains == ["domain1"]
    assert exchange.exchange_scope.time_window_seconds == 3600
    assert exchange.preserved_caveat_refs == ["caveat1"]
    assert exchange.currentness_refs == ["currentness1"]
    assert exchange.validity_window == 86400
    assert exchange.replay_support_refs == ["replay1"]
    assert exchange.exchange_status == "prepared"
    assert exchange.warnings == []
    assert exchange.quorum_exchange_id is not None
