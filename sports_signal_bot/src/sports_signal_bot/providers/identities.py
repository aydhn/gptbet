from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EntityAliasRecord(BaseModel):
    internal_id: str
    entity_type: str
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)


class ProviderIdentityMapRecord(BaseModel):
    provider_name: str
    provider_id: str
    internal_id: str
    entity_type: str


class AliasResolutionRecord(BaseModel):
    original_name: str
    resolved_id: Optional[str] = None
    confidence: float = 0.0
    strategy_used: str


class IdentityNormalizationWarningRecord(BaseModel):
    entity_type: str
    provider_id: Optional[str] = None
    original_name: Optional[str] = None
    issue: str


def resolve_team_alias(
    team_name: str, aliases: List[EntityAliasRecord]
) -> AliasResolutionRecord:
    for record in aliases:
        if team_name.lower() == record.canonical_name.lower() or team_name.lower() in [
            a.lower() for a in record.aliases
        ]:
            return AliasResolutionRecord(
                original_name=team_name,
                resolved_id=record.internal_id,
                confidence=1.0,
                strategy_used="exact_match",
            )
    return AliasResolutionRecord(
        original_name=team_name, resolved_id=None, confidence=0.0, strategy_used="none"
    )


def normalize_event_identity(
    event_raw: Dict[str, Any], mapping: List[ProviderIdentityMapRecord]
) -> str:
    # Placeholder
    return event_raw.get("id", "unknown")


def map_provider_ids_to_internal(
    provider_id: str, provider_name: str, mapping: List[ProviderIdentityMapRecord]
) -> Optional[str]:
    for rec in mapping:
        if rec.provider_name == provider_name and rec.provider_id == provider_id:
            return rec.internal_id
    return None


def summarize_identity_resolution(
    resolutions: List[AliasResolutionRecord],
) -> Dict[str, Any]:
    resolved = sum(1 for r in resolutions if r.resolved_id)
    return {
        "total": len(resolutions),
        "resolved": resolved,
        "unresolved": len(resolutions) - resolved,
    }
