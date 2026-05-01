import pytest
from sports_signal_bot.external_audit_exchange.reputation import apply_reputation_adjustments
from sports_signal_bot.external_audit_exchange.contracts import WitnessReputationRecord, ReputationAdjustmentRecord

def test_reputation_bounds():
    rep = WitnessReputationRecord(witness_id="w1", reputation_score=90.0, reputation_band="excellent", freshness="fresh")
    adjustments = [
        ReputationAdjustmentRecord(adjustment_id="1", witness_id="w1", adjustment_type="credit", score_delta=50.0, reason="test")
    ]
    updated_rep = apply_reputation_adjustments(rep, adjustments)
    assert updated_rep.reputation_score == 100.0

    adjustments = [
        ReputationAdjustmentRecord(adjustment_id="2", witness_id="w1", adjustment_type="penalty", score_delta=-200.0, reason="test")
    ]
    updated_rep = apply_reputation_adjustments(updated_rep, adjustments)
    assert updated_rep.reputation_score == 0.0
