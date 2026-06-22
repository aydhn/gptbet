from sports_signal_bot.regional_hardening.archive_migrations import \
    build_archive_migration_validation
from sports_signal_bot.regional_hardening.contracts import (
    ArchiveMigrationHashRecord, ArchiveMigrationLineageRecord,
    ArchiveMigrationSourceRecord, ArchiveMigrationTargetRecord,
    ArchiveMigrationValidationFamily, ArchiveMigrationValidationInputRecord,
    ArchiveMigrationValidationStatus)


def test_archive_migration_validation():
    source = ArchiveMigrationSourceRecord(source_id="s1", is_stale=False)
    target = ArchiveMigrationTargetRecord(target_id="t1")
    hashes = [ArchiveMigrationHashRecord(hash_id="h1", is_continuous=True)]
    lineages = [
        ArchiveMigrationLineageRecord(
            lineage_id="l1", is_preserved=True
        )
    ]

    params = ArchiveMigrationValidationInputRecord(
        family=ArchiveMigrationValidationFamily.archive_relocation_validation,
        source=source,
        target=target,
        segments=[],
        hashes=hashes,
        lineages=lineages,
        replays=[],
        gaps=[],
    )
    validation = build_archive_migration_validation(params)

    assert (
        validation.validation_status
        == ArchiveMigrationValidationStatus.migration_validated
    )
