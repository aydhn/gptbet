import uuid

from .contracts import (ArchiveMigrationValidationInputRecord,
                        ArchiveMigrationValidationRecord,
                        ArchiveMigrationValidationStatus,
                        ArchiveMigrationWarningRecord)


def build_archive_migration_validation(
    params: ArchiveMigrationValidationInputRecord,
) -> ArchiveMigrationValidationRecord:
    status = ArchiveMigrationValidationStatus.migration_validated
    warnings = []

    if params.source.is_stale:
        status = ArchiveMigrationValidationStatus.migration_blocked
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Stale source archive"
            )
        )

    if any(s.is_missing for s in params.segments):
        status = ArchiveMigrationValidationStatus.migration_gapped
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Missing segments"
            )
        )

    if any(not h.is_continuous for h in params.hashes):
        status = ArchiveMigrationValidationStatus.migration_corrupted
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Hash continuity broken"
            )
        )

    if any(not lin.is_preserved for lin in params.lineages):
        status = ArchiveMigrationValidationStatus.migration_corrupted
        warnings.append(
            ArchiveMigrationWarningRecord(
                warning_id=str(uuid.uuid4()), message="Lineage not preserved"
            )
        )

    return ArchiveMigrationValidationRecord(
        archive_migration_validation_id=str(uuid.uuid4()),
        validation_family=params.family,
        source_archive_ref=params.source,
        target_archive_ref=params.target,
        segment_refs=params.segments,
        hash_refs=params.hashes,
        lineage_refs=params.lineages,
        replay_refs=params.replays,
        gap_refs=params.gaps,
        validation_status=status,
        warnings=warnings,
    )


def summarize_archive_migration_validation(
    validation: ArchiveMigrationValidationRecord,
) -> str:
    return (
        f"Archive Migration {validation.archive_migration_validation_id} "
        f"Status: {validation.validation_status}"
    )
