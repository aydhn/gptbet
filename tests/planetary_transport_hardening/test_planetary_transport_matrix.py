import pytest
from sports_signal_bot.planetary_transport_hardening import ConservativePlanetaryTransportHardeningStrategy

def test_transport_matrix():
    strat = ConservativePlanetaryTransportHardeningStrategy()
    res = strat.generate_transport_matrix({})
    assert len(res.rows) == 1
    assert res.rows[0].seam_explicit is True
    assert res.rows[0].owner_visible is True
