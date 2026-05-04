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
