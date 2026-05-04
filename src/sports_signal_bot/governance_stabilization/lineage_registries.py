from .contracts import *

def build_exception_lineage_registry(reg_id: str, family: ExceptionLineageRegistryFamily) -> ExceptionLineageRegistryRecord:
    return ExceptionLineageRegistryRecord(
        exception_lineage_registry_id=reg_id,
        registry_family=family
    )

def register_exception_lineage_entry(registry: ExceptionLineageRegistryRecord, entry: ExceptionLineageEntryRecord):
    if entry.status in [ExceptionLineageEntryStatus.lineage_expired, ExceptionLineageEntryStatus.lineage_superseded]:
        if not entry.child_exception_refs and not entry.successor_dependency_refs:
            entry.warnings.append("Superseded/expired lineage has no successors defined. Blocks recovery.")
    registry.entries.append(entry)

def detect_lineage_gaps(registry: ExceptionLineageRegistryRecord) -> bool:
    has_gap = False
    for entry in registry.entries:
        if entry.status == ExceptionLineageEntryStatus.lineage_expired and not entry.child_exception_refs:
            has_gap = True
            registry.warnings.append(f"Lineage gap detected at {entry.lineage_entry_id}")
    return has_gap
