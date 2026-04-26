import datetime
import uuid
from typing import List

from sports_signal_bot.bankroll.contracts import (BankrollConfig,
                                                  BankrollDecisionRecord,
                                                  BankrollLedgerRecord,
                                                  BankrollRunManifest,
                                                  BankrollSummaryRecord)
from sports_signal_bot.bankroll.capital_curve import CapitalCurveBuilder
from sports_signal_bot.bankroll.drawdown import DrawdownAnalyzer
from sports_signal_bot.bankroll.streaks import StreakAnalyzer
from sports_signal_bot.bankroll.exposure import ExposureTracker
from sports_signal_bot.bankroll.factory import OverlayFactory
from sports_signal_bot.bankroll.utils import compute_trade_pnl, resolve_payout_multiple, handle_missing_odds
from sports_signal_bot.bankroll.diagnostics import apply_stake_caps, enforce_bankroll_floor

class BankrollRunner:
    def __init__(self, config: BankrollConfig):
        self.config = config
        self.run_id = str(uuid.uuid4())
        self.curve_builder = CapitalCurveBuilder(config.initial_bankroll)
        self.drawdown_analyzer = DrawdownAnalyzer()
        self.streak_analyzer = StreakAnalyzer()
        self.exposure_tracker = ExposureTracker()

        strategy_name = self.config.default_overlay_strategy.value
        self.strategy = OverlayFactory.create(strategy_name, config)

    def run(self, decisions: List[BankrollDecisionRecord], sport: str, market: str) -> BankrollRunManifest:
        ledger: List[BankrollLedgerRecord] = []

        current_bankroll = self.config.initial_bankroll
        cumulative_pnl = 0.0

        executed_count = 0
        win_count = 0
        action_class_pnl = {}
        market_pnl = {}

        # Sort just in case they aren't
        decisions.sort(key=lambda d: d.event_datetime_utc)

        for decision in decisions:
            warnings = []

            # 1. Check if executed
            if not decision.executed_flag:
                continue

            # 2. Handle missing odds
            payout = resolve_payout_multiple(decision.implied_odds, decision.payout_multiple)
            if payout is None and decision.result_status not in ["settled_void", "void", "push"]:
                 if handle_missing_odds(self.config.missing_odds_policy):
                     warnings.append("Skipped due to missing odds")
                     continue
                 else:
                     warnings.append("Proxying missing odds (Fallback logic applied)")

            # 3. Compute Stake
            if self.config.enable_no_financial_shadow:
                 stake_units = 0.0
                 stake_warnings = ["No financial shadow active"]
                 warnings.extend(stake_warnings)
            else:
                # Inject dynamic state for advanced sizing
                if hasattr(self.strategy, 'sizing_runner'):
                    decision.current_drawdown_pct = self.drawdown_analyzer.max_drawdown_pct # simplistic, ideally current
                    decision.current_loss_streak = self.streak_analyzer.longest_loss_streak # simplistic, ideally current

                raw_stake, stake_warnings = self.strategy.compute_stake(decision, current_bankroll)
                warnings.extend(stake_warnings)

                capped_stake, cap_warnings = apply_stake_caps(raw_stake, current_bankroll, self.config)
                warnings.extend(cap_warnings)
                stake_units = capped_stake

            if stake_units <= 0 and not self.config.enable_no_financial_shadow:
                # E.g., no_action or watchlist in tiered
                continue

            # 4. Compute PnL
            pnl_units = compute_trade_pnl(stake_units, decision.result_status, decision.hit_flag, payout)

            # Update stats
            executed_count += 1
            if pnl_units > 0:
                win_count += 1

            action_class_pnl[decision.action_class] = action_class_pnl.get(decision.action_class, 0.0) + pnl_units
            market_pnl[decision.market_type] = market_pnl.get(decision.market_type, 0.0) + pnl_units

            bankroll_before = current_bankroll
            current_bankroll += pnl_units
            cumulative_pnl += pnl_units

            current_bankroll, floor_warnings = enforce_bankroll_floor(current_bankroll, self.config)
            warnings.extend(floor_warnings)

            # 5. Update Analytics
            streak_state = self.streak_analyzer.update(decision.event_id, decision.event_datetime_utc, decision.hit_flag)
            exposure_state = self.exposure_tracker.get_current_exposure(decision.event_datetime_utc)

            curve_point = self.curve_builder.add_point(
                timestamp=decision.event_datetime_utc,
                bankroll=current_bankroll,
                pnl=pnl_units,
                streak_state=streak_state,
                exposure=exposure_state
            )
            self.drawdown_analyzer.update(decision.event_id, decision.event_datetime_utc, curve_point)

            # 6. Record Ledger
            ledger_rec = BankrollLedgerRecord(
                event_id=decision.event_id,
                market_type=decision.market_type,
                sport=decision.sport,
                event_datetime_utc=decision.event_datetime_utc,
                action_class=decision.action_class,
                executed_flag=True,
                stake_units=stake_units,
                stake_fraction=stake_units / bankroll_before if bankroll_before > 0 else 0.0,
                bankroll_before=bankroll_before,
                bankroll_after=current_bankroll,
                pnl_units=pnl_units,
                pnl_pct_bankroll=pnl_units / bankroll_before if bankroll_before > 0 else 0.0,
                cumulative_pnl_units=cumulative_pnl,
                cumulative_return_pct=cumulative_pnl / self.config.initial_bankroll,
                result_status=decision.result_status,
                hit_flag=decision.hit_flag,
                implied_odds=decision.implied_odds,
                payout_multiple=payout,
                overlay_strategy_name=self.strategy.describe(),
                warnings=warnings,
                run_id=self.run_id
            )
            ledger.append(ledger_rec)

        # 7. Final Summary
        summary = BankrollSummaryRecord(
            initial_bankroll=self.config.initial_bankroll,
            ending_bankroll=current_bankroll,
            net_pnl_units=cumulative_pnl,
            return_pct=cumulative_pnl / self.config.initial_bankroll,
            avg_stake_units=sum([r.stake_units for r in ledger]) / executed_count if executed_count > 0 else 0.0,
            executed_count=executed_count,
            win_rate=win_count / executed_count if executed_count > 0 else 0.0,
            max_drawdown_pct=self.drawdown_analyzer.max_drawdown_pct,
            longest_loss_streak=self.streak_analyzer.longest_loss_streak,
            longest_win_streak=self.streak_analyzer.longest_win_streak,
            average_pnl_per_decision=cumulative_pnl / executed_count if executed_count > 0 else 0.0,
            action_class_pnl_summary=action_class_pnl,
            by_market_pnl_summary=market_pnl
        )

        manifest = BankrollRunManifest(
            run_id=self.run_id,
            timestamp=datetime.datetime.utcnow(),
            sport=sport,
            market=market,
            overlay_strategy=self.strategy.describe(),
            config=self.config,
            summary=summary
        )

        return manifest, ledger, self.curve_builder.get_points(), self.drawdown_analyzer.get_events()
