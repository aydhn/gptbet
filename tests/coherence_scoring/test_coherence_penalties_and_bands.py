import pytest
from sports_signal_bot.coherence_scoring.coherence_scorers import (
    build_governance_coherence_scorer,
    apply_coherence_penalties,
    compute_coherence_band,
    STALE_CONTEXT_PENALTY,
    SOVEREIGNTY_SUPPRESSION_PENALTY,
    CRITICALLY_FRAGILE,
    REVIEW_ONLY_COHERENCE,
    BOUNDED_COHERENCE_WITH_CAVEATS,
    STRONG_BOUNDED_COHERENCE
)
from sports_signal_bot.coherence_scoring.contracts import CoherenceInputRecord

def test_stale_penalty_and_band():
    scorer = build_governance_coherence_scorer("test_family")
    stale_input = CoherenceInputRecord(
        coherence_input_id="inp-stale",
        input_family="test",
        source_ref="src",
        currentness_state="stale",
        caveat_state="clear",
        sovereignty_state="passed",
        no_safe_visibility_state="preserved"
    )
    penalties = apply_coherence_penalties(scorer, [stale_input])
    assert STALE_CONTEXT_PENALTY in penalties
    band_output = compute_coherence_band(scorer, [stale_input])
    assert band_output.band == REVIEW_ONLY_COHERENCE

def test_sovereignty_failure_band():
    scorer = build_governance_coherence_scorer("test_family")
    failed_input = CoherenceInputRecord(
        coherence_input_id="inp-failed",
        input_family="test",
        source_ref="src",
        currentness_state="fresh",
        caveat_state="clear",
        sovereignty_state="failed",
        no_safe_visibility_state="preserved"
    )
    penalties = apply_coherence_penalties(scorer, [failed_input])
    assert SOVEREIGNTY_SUPPRESSION_PENALTY in penalties
    band_output = compute_coherence_band(scorer, [failed_input])
    assert band_output.band == CRITICALLY_FRAGILE
    assert not band_output.no_safe_visibility_preserved

def test_caveated_band():
    scorer = build_governance_coherence_scorer("test_family")
    caveated_input = CoherenceInputRecord(
        coherence_input_id="inp-caveat",
        input_family="test",
        source_ref="src",
        currentness_state="fresh",
        caveat_state="caveated",
        sovereignty_state="passed",
        no_safe_visibility_state="preserved"
    )
    band_output = compute_coherence_band(scorer, [caveated_input])
    assert band_output.band == BOUNDED_COHERENCE_WITH_CAVEATS
    assert len(band_output.preserved_caveats) == 1
    assert band_output.preserved_caveats[0] == "inp-caveat"
