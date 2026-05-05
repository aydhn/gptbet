import pytest
from sports_signal_bot.coherence_scoring.coherence_scorers import (
    build_governance_coherence_scorer,
    summarize_coherence_scorer
)
from sports_signal_bot.coherence_scoring.context_federations import (
    build_context_assembler_federation,
    summarize_context_federation_health
)

def test_coherence_scorer_summary():
    scorer = build_governance_coherence_scorer("composite_governance_coherence_scorer")
    summary = summarize_coherence_scorer(scorer)
    assert summary["family"] == "composite_governance_coherence_scorer"
    assert summary["inputs"] == 0
    assert summary["state"] == "initialized"

def test_context_federation_summary():
    fed = build_context_assembler_federation("operator_context_federation", {})
    summary = summarize_context_federation_health(fed)
    assert summary["members"] == 0
    assert summary["links"] == 0
    assert summary["status"] == "initializing"
