import json
from pathlib import Path
from typing import List

from sports_signal_bot.backtest.contracts import (
    BacktestLedgerRecord,
    BacktestRunManifest,
    BacktestSummaryRecord,
    SettlementStatus,
)


class BacktestReporter:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_summary(
        self, run_id: str, sport: str, market: str, ledger: List[BacktestLedgerRecord]
    ) -> BacktestSummaryRecord:
        total = len(ledger)
        executed = sum(1 for r in ledger if r.executed_flag)
        skipped = total - executed

        wins = sum(
            1
            for r in ledger
            if r.executed_flag and r.result_status == SettlementStatus.SETTLED_WIN
        )
        losses = sum(
            1
            for r in ledger
            if r.executed_flag and r.result_status == SettlementStatus.SETTLED_LOSS
        )
        voids = sum(
            1
            for r in ledger
            if r.executed_flag and r.result_status == SettlementStatus.SETTLED_VOID
        )

        resolved_count = wins + losses
        hit_rate = (wins / resolved_count) if resolved_count > 0 else None

        valid_scores = [r.signal_score for r in ledger if r.signal_score is not None]
        avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

        valid_edges = [r.edge_snapshot for r in ledger if r.edge_snapshot is not None]
        avg_edge = sum(valid_edges) / len(valid_edges) if valid_edges else None

        ac_dist = {}
        for r in ledger:
            ac_dist[r.action_class.value] = ac_dist.get(r.action_class.value, 0) + 1

        return BacktestSummaryRecord(
            run_id=run_id,
            sport=sport,
            market=market,
            total_decisions=total,
            executed_decisions=executed,
            skipped_decisions=skipped,
            win_count=wins,
            loss_count=losses,
            void_count=voids,
            hit_rate=hit_rate,
            average_signal_score=avg_score,
            average_edge_snapshot=avg_edge,
            action_class_distribution=ac_dist,
        )

    def save_manifest(
        self, manifest: BacktestRunManifest, filename: str = "replay_manifest.json"
    ) -> Path:
        filepath = self.output_dir / filename
        with open(filepath, "w") as f:
            json.dump(manifest.model_dump(mode="json"), f, indent=2)
        return filepath

    def save_summary(
        self, summary: BacktestSummaryRecord, filename: str = "backtest_summary.json"
    ) -> Path:
        filepath = self.output_dir / filename
        with open(filepath, "w") as f:
            json.dump(summary.model_dump(mode="json"), f, indent=2)
        return filepath
