import uuid
from typing import List, Optional

from .contracts import (
    ArchiveMigrationGapRecord,
    ArchiveMigrationHashRecord,
    ArchiveMigrationLineageRecord,
    ArchiveMigrationReplayRecord,
    ArchiveMigrationSegmentRecord,
    ArchiveMigrationSourceRecord,
    ArchiveMigrationTargetRecord,
    ArchiveMigrationValidationFamily,
    ArchiveMigrationValidationRecord,
    ArchiveMigrationValidationStatus,
    ArchiveMigrationWarningRecord,
)


def build_archive_migration_validation(
    family: ArchiveMigrationValidationFamily,
    source: ArchiveMigrationSourceRecord,
    target: ArchiveMigrationTargetRecord,
    segments: List[ArchiveMigrationSegmentRecord],
    hashes: List[ArchiveMigrationHashRecord],
    lineages: List[ArchiveMigrationLineageRecord],
    replays: List[ArchiveMigrationReplayRecord],
    gaps: List[ArchiveMigrationGapRecord],
) -> ArchiveMigrationValidationRecord:
    status = ArchiveMigrationValidationStatus.migration_validated
    warnings = []

    if source.is_stale:
        status = ArchiveMigrationValidationStatus.migration_blocked
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Stale source archive"
            )
        )

    if any(s.is_missing for s in segments):
        status = ArchiveMigrationValidationStatus.migration_gapped
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Missing segments"
            )
        )

    if any(not h.is_continuous for h in hashes):
        status = ArchiveMigrationValidationStatus.migration_corrupted
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Hash continuity broken"
            )
        )

    if any(not l.is_preserved for l in lineages):
        status = ArchiveMigrationValidationStatus.migration_corrupted
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Lineage not preserved"
            )
        )

    return ArchiveMigrationValidationRecord(
        archive_migration_validation_id=str(uuid.uuid4()),
        validation_family=family,
        source_archive_ref=source,
        target_archive_ref=target,
        segment_refs=segments,
        hash_refs=hashes,
        lineage_refs=lineages,
        replay_refs=replays,
        gap_refs=gaps,
        validation_status=status,
        warnings=warnings,
    )


def summarize_archive_migration_validation(
    validation: ArchiveMigrationValidationRecord,
) -> str:
    return f"Archive Migration {validation.archive_migration_validation_id} Status: {validation.validation_status}"
