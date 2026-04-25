import datetime

from sports_signal_bot.research.contracts import (ResearchScenario,
                                                  WindowDefinition)
from sports_signal_bot.research.period_runner import PeriodRunner


def test_reuse_vs_retrain():
    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 6, 1),
        enabled_models=["m1", "m2"],
        minimum_rows_guard=10,
    )
    window = WindowDefinition(
        period_id=2,  # Will be handled by runner according to flags
        train_start=datetime.date(2023, 1, 1),
        train_end=datetime.date(2023, 1, 31),
        forward_start=datetime.date(2023, 2, 1),
        forward_end=datetime.date(2023, 2, 10),
        should_retrain=False,
    )

    runner = PeriodRunner(scenario)
    record = runner.run_period(window)

    assert len(record.retrained_model_names) == 0
    assert len(record.reused_model_names) == 2
