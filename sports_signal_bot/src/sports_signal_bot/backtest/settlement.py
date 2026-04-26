from typing import Any, Dict, Optional, Tuple

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    SettlementRecord,
    SettlementStatus,
)
from sports_signal_bot.labels.contracts import LabelRecord
from sports_signal_bot.markets.enums import LabelValidityStatus


class SettlementEngine:

    def __init__(self, supported_markets: list[str] = None):
        self.supported_markets = supported_markets or [
            "football_1x2",
            "football_over_under",
            "football_btts",
            "basketball_match_winner",
            "basketball_total_points",
        ]

    def resolve_realized_selection(self, label: LabelRecord) -> Optional[str]:
        if label.validity_status in [
            LabelValidityStatus.VOID,
            LabelValidityStatus.INVALID,
            LabelValidityStatus.UNSUPPORTED,
        ]:
            return None
        return label.target_text

    def compare_decision_vs_result(
        self, decision: BacktestDecisionRecord, label: LabelRecord
    ) -> SettlementRecord:
        if decision.market_type not in self.supported_markets:
            return SettlementRecord(
                status=SettlementStatus.UNSUPPORTED_SETTLEMENT,
                notes=f"Market {decision.market_type} not supported for settlement",
            )

        realized_outcome = self.resolve_realized_selection(label)

        is_void = self.handle_void_or_cancelled(label)
        if is_void:
            return SettlementRecord(
                status=SettlementStatus.SETTLED_VOID,
                notes="Event or label was void/cancelled",
            )

        if label.validity_status == LabelValidityStatus.PENDING:
            return SettlementRecord(
                status=SettlementStatus.UNSETTLED_PENDING,
                notes="Label result is pending",
            )

        if decision.market_type in [
            "football_1x2",
            "football_btts",
            "basketball_match_winner",
        ]:
            return self.settle_multiclass_decision(decision, realized_outcome)
        elif decision.market_type in ["football_over_under", "basketball_total_points"]:
            return self.settle_line_based_market(decision, label)

        return SettlementRecord(
            status=SettlementStatus.UNSUPPORTED_SETTLEMENT,
            notes=f"Fallback unsupported market logic hit for {decision.market_type}",
        )

    def settle_binary_decision(
        self, decision: BacktestDecisionRecord, realized_outcome: Optional[str]
    ) -> SettlementRecord:
        if not realized_outcome:
            return SettlementRecord(
                status=SettlementStatus.INVALID_RESULT,
                notes="Realized outcome is missing",
            )

        hit = decision.selection.lower() == realized_outcome.lower()
        status = SettlementStatus.SETTLED_WIN if hit else SettlementStatus.SETTLED_LOSS
        return SettlementRecord(
            status=status, realized_outcome=realized_outcome, hit_flag=hit
        )

    def settle_multiclass_decision(
        self, decision: BacktestDecisionRecord, realized_outcome: Optional[str]
    ) -> SettlementRecord:
        if not realized_outcome:
            return SettlementRecord(
                status=SettlementStatus.INVALID_RESULT,
                notes="Realized outcome is missing",
            )

        hit = decision.selection.lower() == realized_outcome.lower()
        status = SettlementStatus.SETTLED_WIN if hit else SettlementStatus.SETTLED_LOSS
        return SettlementRecord(
            status=status, realized_outcome=realized_outcome, hit_flag=hit
        )

    def settle_line_based_market(
        self, decision: BacktestDecisionRecord, label: LabelRecord
    ) -> SettlementRecord:
        realized_outcome = label.target_text
        if not realized_outcome:
            return SettlementRecord(
                status=SettlementStatus.INVALID_RESULT,
                notes="Realized outcome is missing",
            )

        if label.line_value is not None and label.target_value is not None:
            if label.line_value == label.target_value:
                return SettlementRecord(
                    status=SettlementStatus.SETTLED_PUSH,
                    realized_outcome=realized_outcome,
                    hit_flag=None,
                    notes="Push due to matching line exactly",
                )

        hit = decision.selection.lower() == realized_outcome.lower()
        status = SettlementStatus.SETTLED_WIN if hit else SettlementStatus.SETTLED_LOSS
        return SettlementRecord(
            status=status, realized_outcome=realized_outcome, hit_flag=hit
        )

    def handle_void_or_cancelled(self, label: LabelRecord) -> bool:
        if label.validity_status in [
            LabelValidityStatus.VOID,
            LabelValidityStatus.INVALID,
        ]:
            return True
        return False
