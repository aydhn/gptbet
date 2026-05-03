from datetime import datetime
import uuid
from typing import List, Dict, Any
from .contracts import RehearsalLedgerRecord, RehearsalEntryRecord

class RehearsalManager:
    def __init__(self):
        self.ledgers = {}

    def create_ledger(self, ledger_family: str, target_incident_family: str) -> RehearsalLedgerRecord:
        ledger_id = f"ldgr_{uuid.uuid4().hex[:8]}"
        ledger = RehearsalLedgerRecord(
            ledger_id=ledger_id,
            ledger_family=ledger_family,
            target_incident_family=target_incident_family,
            entries=[],
            last_updated_at=datetime.utcnow(),
            warnings=[]
        )
        self.ledgers[ledger_id] = ledger
        return ledger

    def append_rehearsal_ledger_entry(self, ledger_id: str, entry_family: str, details: str):
        ledger = self.ledgers.get(ledger_id)
        if ledger:
            entry = RehearsalEntryRecord(
                entry_id=f"ent_{uuid.uuid4().hex[:8]}",
                entry_family=entry_family,
                timestamp=datetime.utcnow(),
                details=details
            )
            # Serialize for ledger entries which expects Dict
            ledger.entries.append(entry.model_dump())
            ledger.last_updated_at = datetime.utcnow()
        return ledger
