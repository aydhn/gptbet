from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.markets.enums import TargetType, LabelValidityStatus

class LabelDefinition(BaseModel):
    label_name: str
    market_type: str
    target_type: TargetType
    class_labels: List[str]
    positive_class: Optional[str] = None
    threshold_line: Optional[float] = None
    sport: SportType
    enabled: bool = True

class LabelRecord(BaseModel):
    event_id: str
    market_type: str
    label_name: str
    target_value: Optional[float] = None
    target_text: Optional[str] = None
    class_index: Optional[int] = None
    line_value: Optional[float] = None
    source: str = "system"
    generated_at_utc: datetime = Field(default_factory=datetime.utcnow)
    validity_status: LabelValidityStatus = LabelValidityStatus.PENDING
    invalid_reason: Optional[str] = None

class BenchmarkPredictionRecord(BaseModel):
    event_id: str
    market_type: str
    benchmark_name: str
    predicted_class: Optional[str] = None
    predicted_probabilities: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class LeakageAuditRecord(BaseModel):
    event_id: str
    label_name: str
    audit_status: str # "pass", "warn", "fail"
    issue_type: str
    message: str
