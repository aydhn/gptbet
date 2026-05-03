import datetime
import uuid
from typing import Dict, Any, List
from sports_signal_bot.execution_coordination.contracts import CoordinationLedgerEntryRecord

class DistributedLedgerManager:
    """Manages the append-only distributed coordination ledger."""

    def __init__(self):
        self.ledger: List[CoordinationLedgerEntryRecord] = []

    def append_distributed_coordination_ledger_entry(
        self,
        lane_ref: str,
        event_type: str,
        details: Dict[str, Any]
    ) -> CoordinationLedgerEntryRecord:
        """Appends a new entry to the coordination ledger."""
        entry = CoordinationLedgerEntryRecord(
            entry_id=f"entry_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            lane_ref=lane_ref,
            event_type=event_type,
            details=details
        )
        self.ledger.append(entry)
        return entry

    def summarize_distributed_ledger(self) -> Dict[str, Any]:
        """Returns a summary of the distributed ledger contents."""
        return {
            "total_entries": len(self.ledger),
            "events_by_type": self._count_events()
        }

    def _count_events(self) -> Dict[str, int]:
        counts = {}
        for entry in self.ledger:
            counts[entry.event_type] = counts.get(entry.event_type, 0) + 1
        return counts
