from sports_signal_bot.witness_mesh.contracts import WitnessStatementRecord, WitnessStatementType, WitnessConsensusType
from sports_signal_bot.witness_mesh.consensus import ConsensusEngine
import datetime

def test_unanimous_consensus():
    statements = [
        WitnessStatementRecord(
            statement_id="stmt1", witness_id="w1", statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="ref1", target_hash="h1", observed_status="ok", observation_window={}, verification_result="confirmed", created_at=datetime.datetime.utcnow()
        ),
        WitnessStatementRecord(
            statement_id="stmt2", witness_id="w2", statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="ref1", target_hash="h1", observed_status="ok", observation_window={}, verification_result="confirmed", created_at=datetime.datetime.utcnow()
        )
    ]
    engine = ConsensusEngine()
    consensus = engine.compute_witness_consensus(statements, "ref1")
    assert consensus.consensus_type == WitnessConsensusType.UNANIMOUS_CONFIRMED
    assert len(consensus.supporting_witness_ids) == 2

def test_split_observation():
    statements = [
        WitnessStatementRecord(
            statement_id="stmt1", witness_id="w1", statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="ref1", target_hash="h1", observed_status="ok", observation_window={}, verification_result="confirmed", created_at=datetime.datetime.utcnow()
        ),
        WitnessStatementRecord(
            statement_id="stmt2", witness_id="w2", statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="ref1", target_hash="h2", observed_status="mismatch", observation_window={}, verification_result="rejected", created_at=datetime.datetime.utcnow()
        )
    ]
    engine = ConsensusEngine()
    consensus = engine.compute_witness_consensus(statements, "ref1")
    assert consensus.consensus_type == WitnessConsensusType.SPLIT_OBSERVATION
