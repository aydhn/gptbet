import datetime

from sports_signal_bot.research.contracts import ResearchScenario
from sports_signal_bot.research.policies import RefreshPolicyResolver


def test_refresh_policies():
    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 6, 1),
        retrain_frequency=2,
        recalibration_frequency=3,
        reensemble_frequency=1,
    )
    resolver = RefreshPolicyResolver(scenario)

    # Period 1: always refresh everything
    assert resolver.should_retrain_model(1) is True
    assert resolver.should_recalibrate(1) is True
    assert resolver.should_refresh_ensemble(1, True) is True

    # Period 2
    assert resolver.should_retrain_model(2) is False
    assert resolver.should_recalibrate(2) is False
    assert resolver.should_refresh_ensemble(2, False) is True

    # Period 3
    assert resolver.should_retrain_model(3) is True
    assert resolver.should_recalibrate(3) is False
    assert resolver.should_refresh_ensemble(3, False) is True

    # Period 4
    assert resolver.should_retrain_model(4) is False
    assert resolver.should_recalibrate(4) is True
    # Ensemble refreshes because recalibration happened
    assert resolver.should_refresh_ensemble(4, True) is True
