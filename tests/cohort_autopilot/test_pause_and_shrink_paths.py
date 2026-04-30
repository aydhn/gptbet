from sports_signal_bot.cohort_autopilot.pauses import pause_cohort_progression
from sports_signal_bot.cohort_autopilot.shrinks import apply_cohort_shrink

def test_pause_cohort():
    pause = pause_cohort_progression("c1", "Stale verification")
    assert pause.cohort_id == "c1"
    assert pause.reason == "Stale verification"

def test_shrink_cohort():
    shrink = apply_cohort_shrink("c1", {"sport": "all"}, {"sport": "football"}, "Regression in basketball")
    assert shrink.new_scope == {"sport": "football"}
