from typing import List, Optional
import uuid
from .contracts import (
    LiveFireVisibilityExerciseRecord, LiveFireScenarioRecord,
    LiveFireSignalRecord, LiveFireSurfaceRecord, LiveFireDecisionRecord,
    LiveFireLossRecord, LiveFireRecoveryRecord, LiveFireVisibilityExerciseStatus,
    LiveFireVisibilityExerciseFamily, LiveFireWarningRecord
)

def build_live_fire_visibility_exercise(
    family: LiveFireVisibilityExerciseFamily,
    scenarios: List[LiveFireScenarioRecord],
    signals: List[LiveFireSignalRecord],
    surfaces: List[LiveFireSurfaceRecord],
    decisions: List[LiveFireDecisionRecord],
    losses: List[LiveFireLossRecord],
    recoveries: List[LiveFireRecoveryRecord]
) -> LiveFireVisibilityExerciseRecord:
    status = LiveFireVisibilityExerciseStatus.visibility_preserved
    warnings = []

    if any(s.is_lost for s in signals):
        status = LiveFireVisibilityExerciseStatus.visibility_lost
        warnings.append(LiveFireWarningRecord(warning_id=str(uuid.uuid4()), message="Signal loss detected"))

    if any(l.is_hidden for l in losses):
        status = LiveFireVisibilityExerciseStatus.visibility_overclaimed
        warnings.append(LiveFireWarningRecord(warning_id=str(uuid.uuid4()), message="Hidden visibility loss"))

    if any(not r.has_explicit_marker for r in recoveries):
        status = LiveFireVisibilityExerciseStatus.visibility_caveated
        warnings.append(LiveFireWarningRecord(warning_id=str(uuid.uuid4()), message="Recovery missing explicit marker"))

    return LiveFireVisibilityExerciseRecord(
        live_fire_exercise_id=str(uuid.uuid4()),
        exercise_family=family,
        scenario_refs=scenarios,
        signal_refs=signals,
        surface_refs=surfaces,
        decision_refs=decisions,
        loss_refs=losses,
        recovery_refs=recoveries,
        exercise_status=status,
        warnings=warnings
    )

def summarize_live_fire_visibility(exercise: LiveFireVisibilityExerciseRecord) -> str:
    return f"Live Fire Exercise {exercise.live_fire_exercise_id} Status: {exercise.exercise_status}"
