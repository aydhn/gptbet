from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class ManifestEnvelopeRecord(BaseModel):
    manifest_family: str
    schema_name: str
    schema_version: str
    manifest_version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    producer_component: str
    artifact_family: str
    artifact_id: Optional[str] = None
    run_id: Optional[str] = None
    payload: Dict[str, Any]
    compatibility_notes: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
