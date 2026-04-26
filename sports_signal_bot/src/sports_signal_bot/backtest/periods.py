from datetime import datetime, timedelta
from typing import Dict, List

from sports_signal_bot.backtest.contracts import (
    BacktestLedgerRecord,
    BacktestPeriodSummary,
    SettlementStatus,
)


class PeriodSummarizer:
    def summarize_by_period(
        self, ledger: List[BacktestLedgerRecord], period: str = "daily"
    ) -> List[BacktestPeriodSummary]:
        if not ledger:
            return []

        period_map: Dict[str, List[BacktestLedgerRecord]] = {}

        for r in ledger:
            dt = r.decision_timestamp_utc
            if period == "daily":
                label = dt.strftime("%Y-%m-%d")
            elif period == "weekly":
                year, week, _ = dt.isocalendar()
                label = f"{year}-W{week:02d}"
            elif period == "monthly":
                label = dt.strftime("%Y-%m")
            else:
                label = "all_time"

            period_map.setdefault(label, []).append(r)

        summaries = []
        for label, records in sorted(period_map.items()):
            start_date = min(r.decision_timestamp_utc for r in records)
            end_date = max(r.decision_timestamp_utc for r in records)

            executed_count = sum(1 for r in records if r.executed_flag)
            wins = sum(
                1
                for r in records
                if r.executed_flag and r.result_status == SettlementStatus.SETTLED_WIN
            )
            losses = sum(
                1
                for r in records
                if r.executed_flag and r.result_status == SettlementStatus.SETTLED_LOSS
            )
            voids = sum(
                1
                for r in records
                if r.executed_flag and r.result_status == SettlementStatus.SETTLED_VOID
            )

            resolved_count = wins + losses
            hit_rate = (wins / resolved_count) if resolved_count > 0 else None

            valid_scores = [
                r.signal_score for r in records if r.signal_score is not None
            ]
            avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

            valid_edges = [
                r.edge_snapshot for r in records if r.edge_snapshot is not None
            ]
            avg_edge = sum(valid_edges) / len(valid_edges) if valid_edges else None

            warnings = []
            for r in records:
                if r.warnings:
                    warnings.extend(r.warnings)

            summaries.append(
                BacktestPeriodSummary(
                    period_label=label,
                    start_date=start_date,
                    end_date=end_date,
                    executed_count=executed_count,
                    hit_rate=hit_rate,
                    avg_score=avg_score,
                    avg_edge=avg_edge,
                    void_count=voids,
                    warnings=list(set(warnings))[:5],
                )
            )

        return summaries
