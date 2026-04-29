import pytest
from sports_signal_bot.quality.synthetic import SyntheticFixtureFactory, ScenarioDataBuilder
from sports_signal_bot.quality.scenarios import LiveLikeInferenceScenario

@pytest.mark.scenario
def test_live_like_inference():
    factory = SyntheticFixtureFactory(seed=42)
    builder = ScenarioDataBuilder(factory)
    scenario = LiveLikeInferenceScenario(builder)

    scenario.setup()
    result = scenario.execute()
    assert scenario.verify(result)
