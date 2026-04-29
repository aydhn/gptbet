from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LineageRecord(BaseModel):
    parent_run_ids: List[str] = Field(default_factory=list)
    parent_artifact_ids: List[str] = Field(default_factory=list)
    source_manifest_refs: List[str] = Field(default_factory=list)
    generation_step: str = "unknown"
    slot_context: Optional[str] = None
    release_channel: Optional[str] = None
    promotion_state: Optional[str] = None

def extract_lineage(manifest_payload: Dict[str, Any]) -> LineageRecord:
    lineage_dict = manifest_payload.get("lineage", {})
    return LineageRecord(**lineage_dict)
