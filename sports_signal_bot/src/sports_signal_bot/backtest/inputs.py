from typing import Dict, List, Tuple

from sports_signal_bot.backtest.contracts import BacktestDecisionRecord
from sports_signal_bot.labels.contracts import LabelRecord


class BacktestInputBuilder:
    def __init__(self):
        pass

    def load_backtest_inputs(
        self, decisions: List[BacktestDecisionRecord], labels: List[LabelRecord]
    ) -> Tuple[List[BacktestDecisionRecord], List[LabelRecord]]:
        return decisions, labels

    def align_decisions_with_results(
        self, decisions: List[BacktestDecisionRecord], labels: List[LabelRecord]
    ) -> List[Tuple[BacktestDecisionRecord, LabelRecord]]:
        aligned = []
        label_map = {f"{l.event_id}_{l.market_type}": l for l in labels}

        for d in decisions:
            key = f"{d.event_id}_{d.market_type}"
            if key in label_map:
                aligned.append((d, label_map[key]))

        return aligned

    def validate_replay_dataset(
        self, dataset: List[Tuple[BacktestDecisionRecord, LabelRecord]]
    ) -> List[str]:
        warnings = []
        event_decision_combos = set()
        for d, l in dataset:
            key = f"{d.event_id}_{d.market_type}_{d.selection}"
            if key in event_decision_combos:
                warnings.append(f"Duplicate decision found for {key}")
            event_decision_combos.add(key)

            if d.event_id != l.event_id:
                warnings.append(
                    f"Mismatch event ids in aligned dataset: {d.event_id} vs {l.event_id}"
                )

        return warnings

    def enrich_with_signal_context(
        self, decision: BacktestDecisionRecord, signal_score: float, edge: float
    ) -> BacktestDecisionRecord:
        decision.signal_score = signal_score
        decision.edge_snapshot = edge
        return decision
