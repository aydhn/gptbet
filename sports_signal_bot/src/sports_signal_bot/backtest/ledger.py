import csv
import json
from pathlib import Path
from typing import List

from sports_signal_bot.backtest.contracts import (
    BacktestLedgerRecord,
    BacktestReplayRecord,
    ExecutionEligibility,
)


class LedgerWriter:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_ledger_records(
        self, run_id: str, replay_records: List[BacktestReplayRecord]
    ) -> List[BacktestLedgerRecord]:
        ledger_records = []
        for r in replay_records:
            d = r.decision
            s = r.settlement
            e = r.eligibility

            executed = e.eligibility == ExecutionEligibility.EXECUTABLE

            lr = BacktestLedgerRecord(
                event_id=d.event_id,
                sport=d.sport,
                market_type=d.market_type,
                event_datetime_utc=d.event_datetime_utc,
                decision_timestamp_utc=d.decision_timestamp_utc,
                signal_status=d.signal_status,
                action_class=d.action_class,
                executed_flag=executed,
                execution_reason=e.reason,
                selection=d.selection,
                final_probability=d.final_probability,
                market_implied_probability=d.market_implied_probability,
                signal_score=d.signal_score,
                threshold_policy_name=d.threshold_policy_name,
                policy_name=d.policy_name,
                result_status=s.status,
                realized_outcome=s.realized_outcome,
                hit_flag=s.hit_flag,
                probabilistic_loss=s.probabilistic_loss,
                edge_snapshot=d.edge_snapshot,
                warnings=d.warnings,
                run_id=run_id,
            )
            ledger_records.append(lr)

        return ledger_records

    def save_to_csv(
        self, records: List[BacktestLedgerRecord], filename: str = "backtest_ledger.csv"
    ) -> Path:
        if not records:
            return self.output_dir / filename

        filepath = self.output_dir / filename
        fieldnames = list(records[0].model_dump().keys())

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                row = r.model_dump()
                row["event_datetime_utc"] = row["event_datetime_utc"].isoformat()
                row["decision_timestamp_utc"] = row[
                    "decision_timestamp_utc"
                ].isoformat()
                writer.writerow(row)

        return filepath

    def save_to_json(
        self,
        records: List[BacktestLedgerRecord],
        filename: str = "backtest_ledger.json",
    ) -> Path:
        filepath = self.output_dir / filename
        data = [r.model_dump(mode="json") for r in records]

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return filepath
