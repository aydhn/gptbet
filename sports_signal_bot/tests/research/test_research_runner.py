import datetime

from sports_signal_bot.research.contracts import ResearchScenario
from sports_signal_bot.research.runner import ResearchRunner


def test_research_runner(tmp_path, monkeypatch):
    from sports_signal_bot.core import paths

    monkeypatch.setattr(paths, "get_processed_dir", lambda: tmp_path)

    scenario = ResearchScenario(
        scenario_id="test",
        sport="test",
        market_type="test",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 2, 1),
        initial_train_window_days=10,
        forward_test_window_days=10,
        calibration_window_days=0,
    )

    runner = ResearchRunner(scenario)
    manifest_path = runner.run()

    assert tmp_path.exists()
    assert manifest_path.endswith("research_manifest.json")
