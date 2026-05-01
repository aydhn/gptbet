import pytest
from sports_signal_bot.external_audit_exchange.reputation import compute_witness_reputation, apply_reputation_adjustments
from sports_signal_bot.external_audit_exchange.contracts import ReputationSignalRecord, ReputationAdjustmentRecord, WitnessReputationRecord

def test_compute_witness_reputation():
    signals = [
        ReputationSignalRecord(signal_id="1", witness_id="w1", signal_type="correct", value=20.0, context_ref="ctx1"),
        ReputationSignalRecord(signal_id="2", witness_id="w1", signal_type="correct", value=15.0, context_ref="ctx2")
    ]
    rep = compute_witness_reputation("w1", signals)
    assert rep.reputation_score == 85.0
    assert rep.reputation_band == "excellent"

def test_apply_reputation_adjustments():
    rep = WitnessReputationRecord(witness_id="w1", reputation_score=50.0, reputation_band="adequate", freshness="fresh")
    adjustments = [
        ReputationAdjustmentRecord(adjustment_id="1", witness_id="w1", adjustment_type="penalty", score_delta=-30.0, reason="false positive")
    ]
    updated_rep = apply_reputation_adjustments(rep, adjustments)
    assert updated_rep.reputation_score == 20.0
    assert updated_rep.reputation_band == "low_trust"
