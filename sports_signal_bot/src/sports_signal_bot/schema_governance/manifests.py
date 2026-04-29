from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class StandardManifest(BaseModel):
    manifest_family: str
    schema_version: str
    producer_component: str
    producer_version: Optional[str] = None
    artifact_family: str
    artifact_id: str
    run_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    lineage: Dict[str, Any] = Field(default_factory=dict)
    payload: Dict[str, Any]
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    channel: Optional[str] = None
    state: Optional[str] = None
    compatibility: Dict[str, Any] = Field(default_factory=dict)
    signature: Optional[str] = None
    hash: Optional[str] = None

def compute_manifest_hash_placeholder(payload: Dict[str, Any]) -> str:
    import json
    import hashlib
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()
