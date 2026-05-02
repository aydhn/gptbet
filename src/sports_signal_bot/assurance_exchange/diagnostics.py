from pydantic import BaseModel
from typing import List

class InteropWarningRecord(BaseModel):
    warning_id: str
    packet_id: str
    severity: str
    message: str

class AssuranceExchangeAuditRecord(BaseModel):
    audit_id: str
    timestamp: str
    events: List[str]
