import uuid

from .contracts import (
    CutoverRehearsalStatus,
    CutoverWarningRecord,
    MultiWaveCutoverRehearsalParams,
    MultiWaveCutoverRehearsalRecord,
)


def build_multi_wave_cutover_rehearsal(
    params: MultiWaveCutoverRehearsalParams,
) -> MultiWaveCutoverRehearsalRecord:
    status = CutoverRehearsalStatus.cutover_rehearsed_honestly
    warnings = []

    if not all(w.owner for w in params.waves):
        status = CutoverRehearsalStatus.rehearsal_failed
        warnings.append(
            CutoverWarningRecord(
                warning_id=str(uuid.uuid4()), message="Wave missing owner"
            )
        )

    if not all(r.path_explicit for r in params.rollbacks):
        status = CutoverRehearsalStatus.blocked_cutover
        warnings.append(
            CutoverWarningRecord(
                warning_id=str(uuid.uuid4()),
                message="Rollback path not explicit",
            )
        )

    if not all(r.is_visible for r in params.residues):
        status = CutoverRehearsalStatus.overclaimed_cutover
        warnings.append(
            CutoverWarningRecord(
                warning_id=str(uuid.uuid4()), message="Hidden residue detected"
            )
        )

    return MultiWaveCutoverRehearsalRecord(
        cutover_rehearsal_id=str(uuid.uuid4()),
        rehearsal_family=params.family,
        wave_refs=params.waves,
        window_refs=params.windows,
        checkpoint_refs=params.checkpoints,
        rollback_refs=params.rollbacks,
        residue_refs=params.residues,
        rehearsal_status=status,
        warnings=warnings,
    )


def summarize_multi_wave_cutover(
    rehearsal: MultiWaveCutoverRehearsalRecord,
) -> str:
    return (
        f"Cutover Rehearsal {rehearsal.cutover_rehearsal_id} Status: "
        f"{rehearsal.rehearsal_status}"
    )
