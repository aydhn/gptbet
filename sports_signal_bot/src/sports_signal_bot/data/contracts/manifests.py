from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sports_signal_bot.core.constants import SportType

class ValidationIssueRecord(BaseModel):
    level: str  # "error", "warning"
    field: Optional[str] = None
    issue_type: str
    message: str
    record_id: Optional[str] = None

class IngestManifestRecord(BaseModel):
    ingest_id: str
    run_timestamp_utc: datetime
    provider: str
    sport: SportType
    dataset_type: str # "fixtures", "odds", "stats"
    source_path: str
    output_path: str
    record_count: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    duplicate_count: int = 0
    warning_count: int = 0
    issues: List[ValidationIssueRecord] = []
