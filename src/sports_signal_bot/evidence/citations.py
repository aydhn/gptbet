from datetime import datetime
from typing import Optional, List
from sports_signal_bot.evidence.contracts import CitationTrailRecord

def build_citation_trail(
    citation_id: str,
    citation_type: str,
    source_family: str,
    source_ref: str,
    artifact_ref: str,
    manifest_ref: str,
    notes: str,
    field_path: Optional[str] = None,
    record_key: Optional[str] = None,
    snapshot_time: Optional[datetime] = None
) -> CitationTrailRecord:
    return CitationTrailRecord(
        citation_id=citation_id,
        citation_type=citation_type,
        source_family=source_family,
        source_ref=source_ref,
        artifact_ref=artifact_ref,
        manifest_ref=manifest_ref,
        field_path=field_path,
        record_key=record_key,
        snapshot_time=snapshot_time,
        notes=notes
    )

def deduplicate_citations(citations: List[CitationTrailRecord]) -> List[CitationTrailRecord]:
    seen = set()
    deduped = []
    for cit in citations:
        if cit.citation_id not in seen:
            seen.add(cit.citation_id)
            deduped.append(cit)
    return deduped
