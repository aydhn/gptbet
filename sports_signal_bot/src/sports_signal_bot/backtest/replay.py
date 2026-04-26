from typing import List, Tuple

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    BacktestReplayRecord,
    ExecutionEligibility,
    ExecutionEligibilityRecord,
    SettlementRecord,
)
from sports_signal_bot.labels.contracts import LabelRecord


class ReplayPlanner:
    def __init__(self):
        pass

    def build_replay_sequence(
        self, dataset: List[Tuple[BacktestDecisionRecord, LabelRecord]]
    ) -> List[Tuple[BacktestDecisionRecord, LabelRecord]]:

        def sort_key(item: Tuple[BacktestDecisionRecord, LabelRecord]):
            d, _ = item
            return (d.decision_timestamp_utc, d.event_datetime_utc, d.event_id)

        return sorted(dataset, key=sort_key)


class ChronologicalReplayEngine:

    def process_sequence(
        self,
        sequence: List[Tuple[BacktestDecisionRecord, LabelRecord]],
        execution_engine,
        settlement_engine,
    ) -> List[BacktestReplayRecord]:

        replay_records = []
        for decision, label in sequence:
            eligibility_record = execution_engine.resolve_execution_subset(decision)
            settlement_record = settlement_engine.compare_decision_vs_result(
                decision, label
            )

            replay_records.append(
                BacktestReplayRecord(
                    decision=decision,
                    eligibility=eligibility_record,
                    settlement=settlement_record,
                )
            )

        return replay_records
