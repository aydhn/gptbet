from typing import Dict, List, Any
from datetime import datetime, timedelta
from .contracts import (
    DisclosureBundleRecord,
    GatewayIndexEntryRecord
)

def validate_disclosure_consistency(
    packet_proof_refs: List[str],
    index_entry: GatewayIndexEntryRecord
) -> tuple[bool, List[str]]:
    inconsistencies = []

    # Check if index lists different proofs
    if index_entry.signed_checkpoint_refs is not None:
        if set(packet_proof_refs) != set(index_entry.signed_checkpoint_refs):
            inconsistencies.append("Packet proofs do not match index proofs")

    return len(inconsistencies) == 0, inconsistencies

def detect_publication_staleness(
    entry: GatewayIndexEntryRecord,
    threshold_hours: int = 48
) -> bool:
    # A dummy check - in reality, we'd look at the created_at of the bundle
    # Just a placeholder for the logic
    return entry.freshness != "Current"

def summarize_consistency_findings(findings: List[str]) -> Dict[str, Any]:
    return {
        "consistent": len(findings) == 0,
        "inconsistencies": findings
    }
