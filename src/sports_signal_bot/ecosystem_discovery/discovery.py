from typing import List, Dict, Any
import uuid
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQueryRecord,
    DiscoveryResultRecord,
    CatalogEntryRecord,
    DiscoveryPolicyRecord
)

def resolve_discovery_policy(config: dict) -> DiscoveryPolicyRecord:
    policy = DiscoveryPolicyRecord()
    if config:
        policy.allowed_source_catalogs = config.get("allowed_source_catalogs", [])
        policy.trusted_discovery_families = config.get("trusted_discovery_families", [])
    return policy

def filter_discovery_results(results: DiscoveryResultRecord, policy: DiscoveryPolicyRecord) -> DiscoveryResultRecord:
    valid_entries = []
    for entry in results.matched_entries:
        if entry.entry_family in policy.hidden_artifact_families:
            continue
        valid_entries.append(entry)
    results.matched_entries = valid_entries
    return results

def suppress_unsafe_entries(results: DiscoveryResultRecord) -> DiscoveryResultRecord:
    safe = []
    for entry in results.matched_entries:
        if "unsafe" not in entry.warnings:
            safe.append(entry)
    results.matched_entries = safe
    return results

def explain_discovery_filtering(results: DiscoveryResultRecord) -> str:
    return f"Filtered down to {len(results.matched_entries)} safe entries."

def run_ecosystem_discovery(query: DiscoveryQueryRecord, available_entries: List[CatalogEntryRecord]) -> DiscoveryResultRecord:
    import uuid
    result = DiscoveryResultRecord(
        result_id=f"res_{uuid.uuid4().hex[:8]}",
        query_id=query.query_id,
        status="discovered_unverified"
    )
    for entry in available_entries:
        # Simple mock matching
        if query.query_family == entry.entry_family or not query.query_family:
            result.matched_entries.append(entry)

    if result.matched_entries:
        result.status = "discovered_requires_negotiation"

    return result

def validate_discovery_to_negotiation_transition(result: DiscoveryResultRecord) -> bool:
    return result.status == "discovered_requires_negotiation"

def summarize_discovery_pipeline(result: DiscoveryResultRecord) -> dict:
    return {
        "status": result.status,
        "matches": len(result.matched_entries)
    }
