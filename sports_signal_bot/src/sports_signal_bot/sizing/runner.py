from typing import Tuple

import uuid
from typing import List
from sports_signal_bot.sizing.contracts import (
    SizingConfig,
    StakeSizingInputRecord,
    SizingDecisionRecord,
    SizingSummaryRecord,
    SizingManifest,
)
from sports_signal_bot.sizing.factory import SizingFactory
from sports_signal_bot.sizing.risk_limits import RiskLimitEngine


class SizingRunner:
    def __init__(self, config: SizingConfig):
        self.config = config
        self.strategy = SizingFactory.create(
            config.default_sizing_strategy.value, config
        )
        self.risk_engine = RiskLimitEngine(config)
        self.run_id = str(uuid.uuid4())

    def process_decision(
        self, input_record: StakeSizingInputRecord
    ) -> SizingDecisionRecord:
        """
        Process a single decision through the sizing policy chain:
        1. Raw sizing proposal
        2. Quality/risk adjustments
        3. Risk limits
        4. Final resolution
        """
        # 1. Proposal
        raw_fraction, raw_kelly, warnings = self.strategy.propose_size(input_record)

        # 2. Adjustments
        adjusted_fraction = self.strategy.apply_adjustments(raw_fraction, input_record)

        # 3. Risk Limits & Final Resolution
        final_fraction, final_units, throttles, caps = self.risk_engine.resolve_size(
            initial_fraction=adjusted_fraction,
            current_bankroll=input_record.current_bankroll,
            current_drawdown=input_record.current_drawdown_pct,
            current_loss_streak=input_record.current_loss_streak,
            action_class=input_record.action_class,
        )

        # 4. Create Decision Record
        return SizingDecisionRecord(
            event_id=input_record.event_id,
            sport=input_record.sport,
            market_type=input_record.market_type,
            action_class=input_record.action_class,
            selected_side=input_record.selected_side,
            sizing_strategy_name=self.strategy.describe(),
            bankroll_before=input_record.current_bankroll,
            raw_size_fraction=raw_fraction,
            adjusted_size_fraction=adjusted_fraction,
            final_stake_units=final_units,
            final_stake_fraction=final_fraction,
            edge_estimate=input_record.edge_estimate,
            calibrated_probability=input_record.final_selection_probability,
            decimal_odds=input_record.market_odds,
            kelly_fraction_raw=raw_kelly,
            kelly_fraction_fractional=raw_fraction if raw_kelly else None,
            risk_throttles_applied=throttles,
            caps_applied=caps,
            warnings=warnings,
            run_id=self.run_id,
        )

    def run_batch(
        self, inputs: List[StakeSizingInputRecord]
    ) -> Tuple[List[SizingDecisionRecord], SizingManifest]:
        decisions = []
        # Sort chronologically just in case
        # Assuming we don't have timestamp in input record, let's assume they are sorted

        for input_rec in inputs:
            decisions.append(self.process_decision(input_rec))

        summary = self._generate_summary(decisions)

        manifest = SizingManifest(
            run_id=self.run_id,
            sport=inputs[0].sport if inputs else "unknown",
            market=inputs[0].market_type if inputs else "unknown",
            strategy=self.strategy.describe(),
            config=self.config.dict(),
            summary=summary,
        )

        return decisions, manifest

    def _generate_summary(
        self, decisions: List[SizingDecisionRecord]
    ) -> SizingSummaryRecord:
        total = len(decisions)
        if total == 0:
            return SizingSummaryRecord()

        capped_count = sum(1 for d in decisions if d.caps_applied)
        throttled_count = sum(1 for d in decisions if d.risk_throttles_applied)

        avg_raw_kelly = sum(d.kelly_fraction_raw or 0.0 for d in decisions) / total
        avg_final_frac = sum(d.final_stake_fraction for d in decisions) / total

        market_summary = {}
        action_summary = {}
        for d in decisions:
            market_summary[d.market_type] = (
                market_summary.get(d.market_type, 0.0) + d.final_stake_fraction
            )
            action_summary[d.action_class] = (
                action_summary.get(d.action_class, 0.0) + d.final_stake_fraction
            )

        # Average it out
        for k in market_summary:
            market_summary[k] /= sum(1 for d in decisions if d.market_type == k)
        for k in action_summary:
            action_summary[k] /= sum(1 for d in decisions if d.action_class == k)

        return SizingSummaryRecord(
            total_sized_decisions=total,
            average_raw_kelly=avg_raw_kelly,
            average_final_stake_fraction=avg_final_frac,
            capped_decision_count=capped_count,
            throttled_decision_count=throttled_count,
            market_sizing_summary=market_summary,
            action_class_sizing_summary=action_summary,
        )
