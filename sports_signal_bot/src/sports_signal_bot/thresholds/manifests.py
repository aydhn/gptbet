from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .contracts import ThresholdCandidateRecord, ThresholdPolicyRecord


class ThresholdManifestRecord(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sport: str
    market_type: str

    best_policy: Optional[ThresholdPolicyRecord] = None

    total_evaluated_candidates: int = 0

    accepted_count: int = 0
    rejected_count: int = 0

    rejection_reasons_summary: Dict[str, int] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
