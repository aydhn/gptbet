import pandas as pd
from typing import List
from sports_signal_bot.sizing.contracts import SizingDecisionRecord


def export_sizing_decisions_csv(decisions: List[SizingDecisionRecord], filepath: str):
    if not decisions:
        return

    records = []
    for d in decisions:
        records.append(
            {
                "event_id": d.event_id,
                "sport": d.sport,
                "market_type": d.market_type,
                "action_class": d.action_class,
                "sizing_strategy": d.sizing_strategy_name,
                "bankroll_before": d.bankroll_before,
                "raw_kelly_frac": d.kelly_fraction_raw,
                "raw_fraction": d.raw_size_fraction,
                "adjusted_fraction": d.adjusted_size_fraction,
                "final_fraction": d.final_stake_fraction,
                "final_stake_units": d.final_stake_units,
                "edge_estimate": d.edge_estimate,
                "calibrated_prob": d.calibrated_probability,
                "decimal_odds": d.decimal_odds,
                "is_capped": bool(d.caps_applied),
                "is_throttled": bool(d.risk_throttles_applied),
                "run_id": d.run_id,
            }
        )

    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)


def export_kelly_estimates_csv(decisions: List[SizingDecisionRecord], filepath: str):
    if not decisions:
        return

    records = []
    for d in decisions:
        records.append(
            {
                "event_id": d.event_id,
                "market_odds": d.decimal_odds,
                "prob": d.calibrated_probability,
                "edge": d.edge_estimate,
                "raw_kelly": d.kelly_fraction_raw,
                "fractional_kelly": d.kelly_fraction_fractional,
                "warnings": "; ".join(d.warnings) if d.warnings else "",
            }
        )

    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
