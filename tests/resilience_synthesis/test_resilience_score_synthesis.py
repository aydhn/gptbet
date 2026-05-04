import pytest
from sports_signal_bot.resilience_synthesis.score_syntheses import (
    build_governance_resilience_score_synthesis,
    register_synthesis_input
)

def test_build_governance_resilience_score_synthesis():
    syn = build_governance_resilience_score_synthesis("s1", "federated_governance_resilience_synthesis")
    assert syn.synthesis_id == "s1"
    assert syn.current_state == "initialized"

def test_register_synthesis_input():
    syn = build_governance_resilience_score_synthesis("s1", "federated_governance_resilience_synthesis")
    rec = register_synthesis_input(syn, "i1", "source1")
    assert rec.synthesis_input_id == "i1"
    assert len(syn.input_refs) == 1
