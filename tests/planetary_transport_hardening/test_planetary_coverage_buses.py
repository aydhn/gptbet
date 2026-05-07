import pytest
from sports_signal_bot.planetary_transport_hardening import ConservativePlanetaryTransportHardeningStrategy, BusStatus

def test_coverage_bus_pass():
    strat = ConservativePlanetaryTransportHardeningStrategy()
    res = strat.run_coverage_bus_pass({})
    assert len(res) == 1
    assert res[0].bus_status == BusStatus.BUS_VERIFIED
    assert "global_oncall_coverage_bus" == res[0].bus_family
