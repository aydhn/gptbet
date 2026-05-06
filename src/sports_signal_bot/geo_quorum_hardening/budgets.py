from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class GeoQuorumBudgetHealthRecord(BaseModel):
    budget_health_id: str
    status: str
    warnings: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def summarize_geo_quorum_budgets(inputs: Dict[str, Any]) -> GeoQuorumBudgetHealthRecord:
    warnings = []
    status = "healthy"

    if inputs.get("quorum_erosion_breach"):
        warnings.append("Quorum erosion budget breached.")
        status = "degraded"

    return GeoQuorumBudgetHealthRecord(
        budget_health_id=f"gqbh-{uuid.uuid4().hex[:8]}",
        status=status,
        warnings=warnings
    )
