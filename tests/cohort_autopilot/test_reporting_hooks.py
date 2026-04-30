from sports_signal_bot.cohort_autopilot.reporting import get_fleet_pressure_index

def test_reporting_hooks():
    idx = get_fleet_pressure_index()
    assert isinstance(idx, float)
