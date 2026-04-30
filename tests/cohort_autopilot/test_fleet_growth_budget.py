from sports_signal_bot.cohort_autopilot.fleets import build_cohort_fleet, suppress_growth_under_fleet_pressure

def test_fleet_pressure():
    fleet = build_cohort_fleet("f1", ["c1", "c2", "c3"])
    pressure = suppress_growth_under_fleet_pressure(fleet, threshold=2)
    assert pressure.pressure_level == "high"
