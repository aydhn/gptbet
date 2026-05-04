from sports_signal_bot.ecosystem_resilience.signals import ingest_marketplace_signal

def test_marketplace_signal_ingestion():
    signal = ingest_marketplace_signal("s1", "treaty_alignment_signal", "b1", "scope1", ["dim1", "dim2", "dim3", "dim4"])
    assert signal.relevance_band == "useful_signal"
    assert signal.freshness_state == "fresh"
