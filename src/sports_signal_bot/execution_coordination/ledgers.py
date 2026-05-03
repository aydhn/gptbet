import datetime
import uuid
from typing import List, Dict, Any
from sports_signal_bot.execution_coordination.contracts import CoordinationLedgerEntryRecord

class CoordinationLedger:
    def __init__(self):
        self.entries: List[CoordinationLedgerEntryRecord] = []

    def append_entry(self, lane_ref: str, event_type: str, details: Dict[str, Any]) -> CoordinationLedgerEntryRecord:
        entry = CoordinationLedgerEntryRecord(
            entry_id=f"led_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            lane_ref=lane_ref,
            event_type=event_type,
            details=details
        )
        self.entries.append(entry)
        return entry

    def get_history(self, lane_ref: str = None) -> List[CoordinationLedgerEntryRecord]:
        if lane_ref:
            return [e for e in self.entries if e.lane_ref == lane_ref]
        return self.entries.copy()
