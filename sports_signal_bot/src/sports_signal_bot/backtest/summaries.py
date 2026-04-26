from typing import Dict, List

from sports_signal_bot.backtest.contracts import (
    ActionSubsetSummary,
    BacktestLedgerRecord,
    SettlementStatus,
)
from sports_signal_bot.policy.contracts import ActionClass


class SummaryGenerator:
    def _calculate_subset(
        self, name: str, records: List[BacktestLedgerRecord]
    ) -> ActionSubsetSummary:
        total = len(records)
        executed = sum(1 for r in records if r.executed_flag)
        skipped = total - executed

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

        avg_score = None
        valid_scores = [r.signal_score for r in records if r.signal_score is not None]
        if valid_scores:
            avg_score = sum(valid_scores) / len(valid_scores)

        avg_edge = None
        valid_edges = [r.edge_snapshot for r in records if r.edge_snapshot is not None]
        if valid_edges:
            avg_edge = sum(valid_edges) / len(valid_edges)

        return ActionSubsetSummary(
            subset_name=name,
            total_decisions=total,
            executed_decisions=executed,
            skipped_decisions=skipped,
            win_count=wins,
            loss_count=losses,
            void_count=voids,
            hit_rate=hit_rate,
            average_signal_score=avg_score,
            average_edge_snapshot=avg_edge,
        )

    def summarize_by_action_class(
        self, ledger: List[BacktestLedgerRecord]
    ) -> List[ActionSubsetSummary]:
        class_map: Dict[ActionClass, List[BacktestLedgerRecord]] = {}
        for r in ledger:
            class_map.setdefault(r.action_class, []).append(r)

        summaries = []
        for ac, records in class_map.items():
            summaries.append(self._calculate_subset(ac.value, records))
        return summaries

    def summarize_by_market(
        self, ledger: List[BacktestLedgerRecord]
    ) -> List[ActionSubsetSummary]:
        market_map: Dict[str, List[BacktestLedgerRecord]] = {}
        for r in ledger:
            market_map.setdefault(r.market_type, []).append(r)

        summaries = []
        for mt, records in market_map.items():
            summaries.append(self._calculate_subset(mt, records))
        return summaries
