import datetime

from sports_signal_bot.research.contracts import ResearchScenario
from sports_signal_bot.research.planner import WalkForwardPlanner


def test_planner_rolling():
    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 6, 1),
        planning_mode="rolling",
        initial_train_window_days=30,
        calibration_window_days=0,
        forward_test_window_days=10,
    )
    planner = WalkForwardPlanner(scenario)
    plan = planner.generate_plan()

    p1 = plan.periods[0]
    p2 = plan.periods[1]

    assert p2.train_start > p1.train_start  # Rolling
    assert (p2.train_end - p2.train_start).days == 29  # 30 days inclusive
