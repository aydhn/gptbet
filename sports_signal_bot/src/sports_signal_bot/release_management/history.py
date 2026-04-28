import csv
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import (
    PromotionDecisionRecord,
    PromotionPlanRecord,
    PromotionRequestRecord,
    ReleaseLedgerRecord,
    RollbackPlanRecord,
)

logger = get_logger("ReleaseLedger")


class ReleaseLedger:
    def __init__(self, data_dir: str = "data/release"):
        self.ledger_file = os.path.join(data_dir, "release_ledger.csv")
        os.makedirs(data_dir, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.ledger_file):
            with open(self.ledger_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "release_event_id",
                        "action",
                        "target_channel",
                        "chain_group_id",
                        "operator",
                        "timestamp",
                        "rationale",
                    ]
                )

    def append_ledger(
        self,
        request: PromotionRequestRecord,
        decision: PromotionDecisionRecord,
        plan: Optional[PromotionPlanRecord],
    ):
        event_id = str(uuid.uuid4())

        target_channel = ""
        if plan and plan.steps:
            target_channel = plan.steps[0].target_channel.value

        record = ReleaseLedgerRecord(
            release_event_id=event_id,
            action=f"promotion_{decision.decision}",
            target_channel=target_channel,
            chain_group_id=request.target_chain_group_id or request.target_artifact_id,
            operator=request.requested_by,
            timestamp=datetime.now(timezone.utc),
            rationale=decision.rationale,
            related_requests=[request.request_id],
        )
        self._write_record(record)

    def append_rollback(self, request: PromotionRequestRecord, plan: RollbackPlanRecord):
        event_id = str(uuid.uuid4())
        record = ReleaseLedgerRecord(
            release_event_id=event_id,
            action="rollback_executed" if plan.execution and plan.execution.status == "success" else "rollback_failed",
            target_channel="stable", # reverting to stable
            chain_group_id=plan.target.chain_group_id,
            operator=request.requested_by,
            timestamp=datetime.now(timezone.utc),
            rationale=plan.target.reason,
            related_requests=[request.request_id],
        )
        self._write_record(record)

    def _write_record(self, record: ReleaseLedgerRecord):
        with open(self.ledger_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    record.release_event_id,
                    record.action,
                    record.target_channel,
                    record.chain_group_id,
                    record.operator,
                    record.timestamp.isoformat(),
                    record.rationale,
                ]
            )
