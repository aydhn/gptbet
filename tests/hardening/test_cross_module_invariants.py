import pytest
from sports_signal_bot.hardening.invariant_matrix import build_cross_module_invariant_matrix

def test_build_matrix():
    matrix = build_cross_module_invariant_matrix(["modA", "modB"])
    assert matrix.overall_health == "healthy"
    assert "modA_modB" in matrix.pair_validations
