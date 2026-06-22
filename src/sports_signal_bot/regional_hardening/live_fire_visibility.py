import uuid
from .contracts import (
    LiveFireVisibilityExerciseRecord,
    LiveFireVisibilityExerciseStatus,
    LiveFireWarningRecord,
    LiveFireVisibilityExerciseParams,
)


def build_live_fire_visibility_exercise(
    params: LiveFireVisibilityExerciseParams,
) -> LiveFireVisibilityExerciseRecord:
    status = LiveFireVisibilityExerciseStatus.visibility_preserved
    warnings = []

    if any(s.is_lost for s in params.signals):
        status = LiveFireVisibilityExerciseStatus.visibility_lost
        warnings.append(
            LiveFireWarningRecord(
                warning_id=str(uuid.uuid4()),
                message="Signal loss detected",
            )
        )

    if any(loss.is_hidden for loss in params.losses):
        status = LiveFireVisibilityExerciseStatus.visibility_overclaimed
        warnings.append(
            LiveFireWarningRecord(
                warning_id=str(uuid.uuid4()),
                message="Hidden visibility loss",
            )
        )

    if any(not r.has_explicit_marker for r in params.recoveries):
        status = LiveFireVisibilityExerciseStatus.visibility_caveated
        warnings.append(
            LiveFireWarningRecord(
                warning_id=str(uuid.uuid4()),
                message="Recovery missing explicit marker",
            )
        )

    return LiveFireVisibilityExerciseRecord(
        live_fire_exercise_id=str(uuid.uuid4()),
        exercise_family=params.family,
        scenario_refs=params.scenarios,
        signal_refs=params.signals,
        surface_refs=params.surfaces,
        decision_refs=params.decisions,
        loss_refs=params.losses,
        recovery_refs=params.recoveries,
        exercise_status=status,
        warnings=warnings,
    )


def summarize_live_fire_visibility(
    exercise: LiveFireVisibilityExerciseRecord,
) -> str:
    ex_id = exercise.live_fire_exercise_id
    status = exercise.exercise_status
    return f"Live Fire Exercise {ex_id} Status: {status}"
