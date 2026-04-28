import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from sports_signal_bot.approvals.contracts import (
    ApprovalRequestRecord, ApprovalDecisionRecord, ReviewItemRecord,
    OverrideRecord, AlarmAckRecord, ApprovalLedgerRecord
)
from pydantic import BaseModel

class ApprovalRegistry:
    """Simple file-based registry for storing approval artifacts."""
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _save_json(self, filename: str, data: BaseModel) -> None:
        path = self.storage_dir / filename
        with open(path, "w") as f:
            f.write(data.model_dump_json(indent=2))

    def _append_csv(self, filename: str, data: dict, fieldnames: List[str]) -> None:
        path = self.storage_dir / filename
        file_exists = path.exists()
        with open(path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def save_request(self, request: ApprovalRequestRecord) -> None:
        self._save_json(f"request_{request.request_id}.json", request)

    def save_decision(self, decision: ApprovalDecisionRecord) -> None:
        self._save_json(f"decision_{decision.decision_id}.json", decision)

    def log_audit(self, ledger_record: ApprovalLedgerRecord) -> None:
        data = ledger_record.model_dump(mode="json")
        self._append_csv("audit_ledger.csv", data, list(data.keys()))

    def save_override(self, override: OverrideRecord) -> None:
        self._save_json(f"override_{override.override_id}.json", override)
