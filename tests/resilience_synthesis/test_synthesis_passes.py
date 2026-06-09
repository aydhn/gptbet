import pytest
from sports_signal_bot.resilience_synthesis.synthesis_passes import (
    execute_score_synthesis_passes,
    compute_synthesis_dimensions
)
from sports_signal_bot.resilience_synthesis.contracts import (
    GovernanceResilienceScoreSynthesisRecord,
    SynthesisPassRecord
)

def test_execute_score_synthesis_passes():
    synthesis = GovernanceResilienceScoreSynthesisRecord(
        synthesis_id="syn1",
        synthesis_family="federated_governance_resilience_synthesis",
        current_state="test"
    )

    passes = [
        SynthesisPassRecord(pass_id="p1", pass_type="federated_currentness_pass", is_successful=True, notes="test 1"),
        SynthesisPassRecord(pass_id="p2", pass_type="replay_stability_pass", is_successful=False, notes="test 2"),
    ]

    assert synthesis.pass_refs == []

    execute_score_synthesis_passes(synthesis, passes)

    assert synthesis.pass_refs == ["p1", "p2"]

def test_compute_synthesis_dimensions():
    dims = compute_synthesis_dimensions()
    assert dims == {"federated_health_quality": 1.0, "replay_support_quality": 1.0}
