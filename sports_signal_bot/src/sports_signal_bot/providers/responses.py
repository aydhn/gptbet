from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.providers.contracts import UnifiedDataRecord
from sports_signal_bot.providers.requests import ProviderRequestRecord


class ProviderQualityRecord(BaseModel):
    freshness_score: float = 0.0
    completeness_score: float = 0.0
    consistency_score: float = 0.0
    schema_validity_score: float = 0.0
    overall_score: float = 0.0
    components: Dict[str, float] = Field(default_factory=dict)
    is_acceptable: bool = False


class ProviderLineageRecord(BaseModel):
    provider_used: str
    provider_candidates: List[str] = Field(default_factory=list)
    fetch_timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_snapshot_time: Optional[datetime] = None
    fallback_chain: List[str] = Field(default_factory=list)
    quality_score: float = 0.0
    normalization_warnings: List[str] = Field(default_factory=list)
    alias_mappings_applied: int = 0
    schema_version_used: str = "v1"


class ProviderResponseRecord(BaseModel):
    records: List[UnifiedDataRecord] = Field(default_factory=list)
    provider_used: str
    provider_candidates: List[str] = Field(default_factory=list)
    failover_path: List[str] = Field(default_factory=list)
    quality_summary: Optional[ProviderQualityRecord] = None
    lineage_summary: Optional[ProviderLineageRecord] = None
    warnings: List[str] = Field(default_factory=list)
    partial_data_flag: bool = False
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    request_ref: Optional[ProviderRequestRecord] = None
    raw_payload: Optional[Any] = (
        None  # Can be dict, list, string depending on raw format
    )


def normalize_provider_response(
    response: ProviderResponseRecord,
) -> ProviderResponseRecord:
    # Placeholder for broader normalization hook
    return response


def attach_provider_lineage(
    response: ProviderResponseRecord, lineage: ProviderLineageRecord
) -> ProviderResponseRecord:
    response.lineage_summary = lineage
    return response


def summarize_provider_fetch(response: ProviderResponseRecord) -> Dict[str, Any]:
    return {
        "provider": response.provider_used,
        "record_count": len(response.records),
        "partial": response.partial_data_flag,
        "quality": (
            response.quality_summary.overall_score if response.quality_summary else None
        ),
        "warnings_count": len(response.warnings),
    }
