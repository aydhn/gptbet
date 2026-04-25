import datetime

from sports_signal_bot.research.contracts import (ResearchScenario,
                                                  WindowDefinition)
from sports_signal_bot.research.period_runner import PeriodRunner


def test_period_runner():
    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 6, 1),
        enabled_models=["test_model"],
        minimum_rows_guard=10,
    )
    window = WindowDefinition(
        period_id=1,
        train_start=datetime.date(2023, 1, 1),
        train_end=datetime.date(2023, 1, 31),
        forward_start=datetime.date(2023, 2, 1),
        forward_end=datetime.date(2023, 2, 10),
    )

    runner = PeriodRunner(scenario)
    record = runner.run_period(window)

    assert record.status == "success"
    assert "test_model" in record.retrained_model_names
    assert record.evaluation_summary["num_events_evaluated"] > 0
