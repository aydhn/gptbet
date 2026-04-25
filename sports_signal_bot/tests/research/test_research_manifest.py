import datetime

from sports_signal_bot.research.contracts import (PeriodRunRecord,
                                                  ResearchScenario,
                                                  WindowDefinition)
from sports_signal_bot.research.manifests import build_research_manifest


def test_manifest_building():
    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 2, 1),
    )
    w1 = WindowDefinition(
        period_id=1,
        train_start=datetime.date(2023, 1, 1),
        train_end=datetime.date(2023, 1, 31),
        forward_start=datetime.date(2023, 2, 1),
        forward_end=datetime.date(2023, 2, 10),
    )
    r1 = PeriodRunRecord(
        period_id=1,
        scenario_id="test",
        window=w1,
        status="success",
        retrained_model_names=["m1"],
    )

    manifest = build_research_manifest("run123", scenario, [r1], {}, {})

    assert manifest.completed_periods == 1
    assert manifest.total_periods == 1
    assert "m1" in manifest.source_families_involved
