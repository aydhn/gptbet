from typing import Tuple, List, Dict
from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy
from sports_signal_bot.sizing.factory import SizingFactory
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord, SizingConfig
from sports_signal_bot.sizing.risk_limits import RiskLimitEngine
from sports_signal_bot.sizing.runner import SizingRunner # We will create this

class AdvancedSizingOverlay(BaseOverlayStrategy):
    """
    Adapter that bridges the simple BankrollRunner interface to the
    new, complex Advanced Sizing Engine.
    """
    def __init__(self, config: BankrollConfig):
        super().__init__(config)
        # Parse sizing config from dict if available, otherwise use defaults
        sizing_config_dict = getattr(config, 'advanced_sizing_config', {})
        self.sizing_config = SizingConfig(**sizing_config_dict)

        # We need a SizingRunner to handle the complex flow
        self.sizing_runner = SizingRunner(self.sizing_config)

    def compute_stake(self, decision: BankrollDecisionRecord, current_bankroll: float) -> Tuple[float, List[str]]:
        # This requires input fields that might not be on the standard BankrollDecisionRecord yet.
        # We will map what we can.

        # The Sizing Runner needs a StakeSizingInputRecord
        input_record = StakeSizingInputRecord(
            event_id=decision.event_id,
            sport=decision.sport,
            market_type=decision.market_type,
            action_class=decision.action_class,
            selected_side="unknown", # We need to pass this somehow, or ignore if single-side

            # Map probabilities. If missing, sizing runner will skip/warn.
            final_selection_probability=getattr(decision, 'calibrated_probability', 0.0),
            market_odds=1.0 / decision.implied_odds if decision.implied_odds and decision.implied_odds > 0 else 0.0,
            implied_probability=decision.implied_odds or 0.0,

            signal_score=decision.signal_score,
            edge_estimate=getattr(decision, 'edge_estimate', 0.0),
            confidence_score=getattr(decision, 'confidence_score', 1.0),

            uncertainty_penalty=getattr(decision, 'uncertainty_penalty', 0.0),
            disagreement_penalty=getattr(decision, 'disagreement_penalty', 0.0),
            data_quality_penalty=getattr(decision, 'data_quality_penalty', 0.0),
            source_health_penalty=getattr(decision, 'source_health_penalty', 0.0),
            regime_adjustment=getattr(decision, 'regime_adjustment', 1.0),

            current_bankroll=current_bankroll,
            current_drawdown_pct=getattr(decision, 'current_drawdown_pct', 0.0), # Need to inject this
            current_loss_streak=getattr(decision, 'current_loss_streak', 0),    # Need to inject this
            same_day_exposure=0.0
        )

        # Run the sizing engine
        sizing_decision = self.sizing_runner.process_decision(input_record)

        return sizing_decision.final_stake_units, sizing_decision.warnings

    def describe(self) -> str:
        strategy = self.sizing_config.default_sizing_strategy.value
        return f"AdvancedSizing({strategy})"
