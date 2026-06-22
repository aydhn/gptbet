from sports_signal_bot.regional_hardening.contracts import (
    LiveFireLossRecord,
    LiveFireRecoveryRecord,
    LiveFireSignalRecord,
    LiveFireVisibilityExerciseFamily,
    LiveFireVisibilityExerciseParams,
    LiveFireVisibilityExerciseStatus,
)
from sports_signal_bot.regional_hardening.live_fire_visibility import (
    build_live_fire_visibility_exercise,
)


def test_live_fire_visibility():
    signals = [LiveFireSignalRecord(signal_id="s1", is_lost=False)]
    losses = [LiveFireLossRecord(loss_id="l1", is_hidden=False, is_high_severity=False)]
    recoveries = [LiveFireRecoveryRecord(recovery_id="r1", has_explicit_marker=True)]

    params = LiveFireVisibilityExerciseParams(
        family=LiveFireVisibilityExerciseFamily.no_safe_live_fire_exercise,
        scenarios=[],
        signals=signals,
        surfaces=[],
        decisions=[],
        losses=losses,
        recoveries=recoveries,
    )
    exercise = build_live_fire_visibility_exercise(params)

    assert exercise.exercise_status == (
        LiveFireVisibilityExerciseStatus.visibility_preserved
    )
