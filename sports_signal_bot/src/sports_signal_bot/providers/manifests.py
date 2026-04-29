from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.providers.requests import ProviderRequestRecord


class ProviderManifest(BaseModel):
    manifest_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    request: ProviderRequestRecord
    providers_attempted: List[str]
    final_provider: str
    record_count: int
    quality_score: float


def build_provider_manifest(
    request: ProviderRequestRecord,
    final_provider: str,
    attempted: List[str],
    count: int,
    score: float,
) -> ProviderManifest:
    import uuid

    return ProviderManifest(
        manifest_id=str(uuid.uuid4()),
        request=request,
        providers_attempted=attempted,
        final_provider=final_provider,
        record_count=count,
        quality_score=score,
    )
