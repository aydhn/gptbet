from sports_signal_bot.ecosystem_resilience.projections import project_marketplace_signals_into_scorecards
from sports_signal_bot.ecosystem_resilience.signals import ingest_marketplace_signal

def test_projection_downgrades():
    signal = ingest_marketplace_signal("s1", "treaty_alignment_signal", "b1", "scope1", ["dim1"], is_stale=True)
    new_score = project_marketplace_signals_into_scorecards([signal], 0.8)
    assert new_score == 0.8 # Suppressed signal does not increase score
