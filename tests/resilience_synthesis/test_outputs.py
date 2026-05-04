import pytest
from sports_signal_bot.resilience_synthesis.outputs import (
    compute_synthesis_band,
    enforce_sovereignty_across_phase89
)
from sports_signal_bot.resilience_synthesis.contracts import SynthesisCeilingRecord

def test_compute_synthesis_band():
    band = compute_synthesis_band(0.9, [], [], True)
    assert band == "strong_bounded_resilience"

    band_no_sov = compute_synthesis_band(0.9, [], [], False)
    assert band_no_sov == "critically_fragile"

    ceil = SynthesisCeilingRecord(ceiling_id="c1", max_band="review_only_resilience", reason="test")
    band_ceil = compute_synthesis_band(0.9, [], [ceil], True)
    assert band_ceil == "review_only_resilience"

def test_enforce_sovereignty_across_phase89():
    assert enforce_sovereignty_across_phase89("strong_bounded_resilience", True) == "critically_fragile"
    assert enforce_sovereignty_across_phase89("strong_bounded_resilience", False) == "strong_bounded_resilience"
