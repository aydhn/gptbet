from sports_signal_bot.regional_hardening.live_fire_visibility import build_live_fire_visibility_exercise
from sports_signal_bot.regional_hardening.contracts import (
    LiveFireVisibilityExerciseFamily, LiveFireSignalRecord,
    LiveFireLossRecord, LiveFireRecoveryRecord, LiveFireVisibilityExerciseStatus
)

def test_live_fire_visibility():
    signals = [LiveFireSignalRecord(signal_id="s1", is_lost=False)]
    losses = [LiveFireLossRecord(loss_id="l1", is_hidden=False, is_high_severity=False)]
    recoveries = [LiveFireRecoveryRecord(recovery_id="r1", has_explicit_marker=True)]

    exercise = build_live_fire_visibility_exercise(
        LiveFireVisibilityExerciseFamily.no_safe_live_fire_exercise,
        [], signals, [], [], losses, recoveries
    )

    assert exercise.exercise_status == LiveFireVisibilityExerciseStatus.visibility_preserved
