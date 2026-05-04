from typing import List, Optional
from .contracts import (
    BaselineSuccessorRegistryRecord,
    SuccessorRegistryEntryRecord,
    SuccessorLinkRecord,
    SuccessorChainRecord,
    SuccessorResolutionRecord,
    SuccessorApplicabilityRecord,
    SuccessorVisibilityRecord,
    SuccessorReplayRecord,
    SuccessorRegistryHealthRecord,
    SuccessorRegistryManifestRecord,
    SuccessorRegistryWarningRecord,
    SuccessorStatus
)

def build_successor_registry(registry_id: str, family: str) -> BaselineSuccessorRegistryRecord:
    health = SuccessorRegistryHealthRecord(is_healthy=True)
    return BaselineSuccessorRegistryRecord(
        successor_registry_id=registry_id,
        registry_family=family,
        health_status=health
    )

def register_successor_entry(registry: BaselineSuccessorRegistryRecord, entry: SuccessorRegistryEntryRecord) -> BaselineSuccessorRegistryRecord:
    if entry.successor_status == SuccessorStatus.SUCCESSOR_UNRESOLVED:
        registry.unresolved_successor_refs.append(entry.successor_entry_id)
    else:
        registry.current_successor_refs.append(entry.successor_entry_id)
    return registry

def resolve_successor_chain(registry: BaselineSuccessorRegistryRecord, chain: SuccessorChainRecord) -> BaselineSuccessorRegistryRecord:
    return registry

def validate_successor_currentness(entry: SuccessorRegistryEntryRecord) -> bool:
    return entry.successor_status in [SuccessorStatus.SUCCESSOR_RESOLVED_CURRENT, SuccessorStatus.SUCCESSOR_RESOLVED_CAVEATED]

def summarize_successor_registry(registry: BaselineSuccessorRegistryRecord) -> SuccessorRegistryHealthRecord:
    return registry.health_status
