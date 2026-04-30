from sports_signal_bot.cohort_autopilot.growth import progress_cohort
from sports_signal_bot.cohort_autopilot.contracts import ActivationLevel

def test_ladder_progression():
    progression = progress_cohort("c1", ActivationLevel.LEVEL_1_NARROW_ACTIVATION, ActivationLevel.LEVEL_2_SMALL_COHORT)
    assert progression.from_level == ActivationLevel.LEVEL_1_NARROW_ACTIVATION
    assert progression.to_level == ActivationLevel.LEVEL_2_SMALL_COHORT
