from sports_signal_bot.ecosystem_resilience.signals import ingest_marketplace_signal
from sports_signal_bot.ecosystem_resilience.signal_catalogs import suppress_marketplace_signal

def test_signal_staleness_and_suppression():
    signal = ingest_marketplace_signal("s1", "treaty_alignment_signal", "b1", "scope1", ["dim1"], is_stale=True)
    assert signal.relevance_band == "suppressed_signal"

    signal = ingest_marketplace_signal("s2", "treaty_alignment_signal", "b1", "scope1", ["dim1"])
    signal = suppress_marketplace_signal(signal, "manual override")
    assert signal.relevance_band == "suppressed_signal"
