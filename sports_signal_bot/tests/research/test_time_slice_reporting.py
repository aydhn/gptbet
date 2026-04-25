import datetime

from sports_signal_bot.research.contracts import (PeriodRunRecord,
                                                  WindowDefinition)
from sports_signal_bot.research.reporting import TimeSliceReporter


def test_reporting():
    w1 = WindowDefinition(
        period_id=1,
        train_start=datetime.date(2023, 1, 1),
        train_end=datetime.date(2023, 1, 31),
        forward_start=datetime.date(2023, 2, 1),
        forward_end=datetime.date(2023, 2, 10),
    )
    w2 = WindowDefinition(
        period_id=2,
        train_start=datetime.date(2023, 1, 1),
        train_end=datetime.date(2023, 1, 31),
        forward_start=datetime.date(2023, 2, 11),
        forward_end=datetime.date(2023, 2, 20),
    )

    r1 = PeriodRunRecord(
        period_id=1,
        scenario_id="test",
        window=w1,
        status="success",
        evaluation_summary={
            "num_events_evaluated": 10,
            "metrics_by_source": {"m1": {"log_loss": 0.6}},
        },
    )
    r2 = PeriodRunRecord(
        period_id=2,
        scenario_id="test",
        window=w2,
        status="success",
        evaluation_summary={
            "num_events_evaluated": 10,
            "metrics_by_source": {"m1": {"log_loss": 0.5}},
        },
    )

    reporter = TimeSliceReporter()
    summary = reporter.generate_report("test", [r1, r2])

    assert summary.cumulative_leaderboard["m1"]["log_loss"] == 0.55
    assert len(summary.period_performances) == 2
