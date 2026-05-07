import pytest
from sports_signal_bot.planetary_transport_hardening import ConservativePlanetaryTransportHardeningStrategy, SimulationStatus

def test_audit_calendar_pass():
    strat = ConservativePlanetaryTransportHardeningStrategy()
    res = strat.run_audit_calendar_pass({})
    assert len(res) == 1
    assert res[0].simulation_status == SimulationStatus.SIMULATION_VERIFIED
    assert "global_follow_the_sun_audit_simulation" == res[0].simulation_family
