from typing import Dict, Any, List
import uuid
from .contracts import PublicationSupersessionRecord, PublicationRetractionRecord, TombstonePublicationRecord

def mark_publication_superseded(publication_id: str) -> PublicationSupersessionRecord:
    return PublicationSupersessionRecord(superseded=True)

def build_retraction_notice(publication_id: str, reason: str) -> TombstonePublicationRecord:
    return TombstonePublicationRecord(
        tombstone_id=f"tombstone_{publication_id}",
    )

def route_queries_to_current_publication(publication_id: str, current_id: str) -> str:
    return current_id

def summarize_publication_lifecycle(publication_id: str, states: List[str]) -> Dict[str, Any]:
    return {
        "publication_id": publication_id,
        "lifecycle_states": states,
        "current_state": states[-1] if states else "unknown"
    }
