import datetime

from sports_signal_bot.research.contracts import ResearchScenario
from sports_signal_bot.research.planner import WalkForwardPlanner


def test_planner_expanding():
    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 6, 1),
        planning_mode="expanding",
        initial_train_window_days=30,
        calibration_window_days=10,
        forward_test_window_days=10,
    )
    planner = WalkForwardPlanner(scenario)
    plan = planner.generate_plan()

    assert plan.total_periods > 0

    p1 = plan.periods[0]
    assert p1.train_start == datetime.date(2023, 1, 1)

    p2 = plan.periods[1]
    assert p2.train_start == datetime.date(2023, 1, 1)  # Expanding means same start
    assert p2.forward_start == p1.forward_end + datetime.timedelta(days=1)
