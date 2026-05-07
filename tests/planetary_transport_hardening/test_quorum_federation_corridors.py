import pytest
from sports_signal_bot.planetary_transport_hardening import ConservativePlanetaryTransportHardeningStrategy, CorridorStatus

def test_quorum_corridor_pass():
    strat = ConservativePlanetaryTransportHardeningStrategy()
    res = strat.run_quorum_corridor_pass({})
    assert len(res) == 1
    assert res[0].corridor_status == CorridorStatus.CORRIDOR_VERIFIED
    assert "bounded_quorum_corridor" == res[0].corridor_family
