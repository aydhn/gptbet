from typing import List, Optional
import uuid
from .contracts import (
    MultiWaveCutoverRehearsalRecord, CutoverWaveRecord, CutoverWindowRecord,
    CutoverCheckpointRecord, CutoverRollbackRecord, CutoverResidueRecord,
    CutoverRehearsalStatus, MultiWaveCutoverRehearsalFamily, CutoverWarningRecord
)

def build_multi_wave_cutover_rehearsal(
    family: MultiWaveCutoverRehearsalFamily,
    waves: List[CutoverWaveRecord],
    windows: List[CutoverWindowRecord],
    checkpoints: List[CutoverCheckpointRecord],
    rollbacks: List[CutoverRollbackRecord],
    residues: List[CutoverResidueRecord]
) -> MultiWaveCutoverRehearsalRecord:
    status = CutoverRehearsalStatus.cutover_rehearsed_honestly
    warnings = []

    if not all(w.owner for w in waves):
        status = CutoverRehearsalStatus.rehearsal_failed
        warnings.append(CutoverWarningRecord(warning_id=str(uuid.uuid4()), message="Wave missing owner"))

    if not all(r.path_explicit for r in rollbacks):
        status = CutoverRehearsalStatus.blocked_cutover
        warnings.append(CutoverWarningRecord(warning_id=str(uuid.uuid4()), message="Rollback path not explicit"))

    if not all(r.is_visible for r in residues):
        status = CutoverRehearsalStatus.overclaimed_cutover
        warnings.append(CutoverWarningRecord(warning_id=str(uuid.uuid4()), message="Hidden residue detected"))

    return MultiWaveCutoverRehearsalRecord(
        cutover_rehearsal_id=str(uuid.uuid4()),
        rehearsal_family=family,
        wave_refs=waves,
        window_refs=windows,
        checkpoint_refs=checkpoints,
        rollback_refs=rollbacks,
        residue_refs=residues,
        rehearsal_status=status,
        warnings=warnings
    )

def summarize_multi_wave_cutover(rehearsal: MultiWaveCutoverRehearsalRecord) -> str:
    return f"Cutover Rehearsal {rehearsal.cutover_rehearsal_id} Status: {rehearsal.rehearsal_status}"
