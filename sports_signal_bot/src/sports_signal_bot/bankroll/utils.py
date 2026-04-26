from typing import Optional
from sports_signal_bot.bankroll.contracts import MissingOddsPolicy

def resolve_payout_multiple(implied_odds: Optional[float], payout_multiple: Optional[float]) -> Optional[float]:
    """Resolve the payout multiple from available data."""
    if payout_multiple is not None:
        return payout_multiple
    if implied_odds is not None and implied_odds > 0:
        # Convert implied probability to decimal odds, then to payout multiple (odds - 1)
        decimal_odds = 1.0 / implied_odds
        return decimal_odds - 1.0
    return None

def compute_trade_pnl(stake_units: float, result_status: str, hit_flag: Optional[bool], payout_multiple: Optional[float]) -> float:
    """Compute the profit/loss in units for a given trade."""
    # Assuming result_status could be 'settled_win', 'settled_loss', 'settled_void', etc.
    if result_status == 'settled_void' or result_status == 'void' or result_status == 'push':
        return 0.0

    if hit_flag is True:
        if payout_multiple is not None:
            return stake_units * payout_multiple
        # Fallback to even money if win but no payout info
        return stake_units
    elif hit_flag is False:
        return -stake_units

    return 0.0

def handle_missing_odds(policy: MissingOddsPolicy) -> bool:
    """Determine if a bet should be skipped based on missing odds policy. Returns True if we should skip."""
    if policy == MissingOddsPolicy.SKIP:
        return True
    elif policy == MissingOddsPolicy.FAIL:
        raise ValueError("Missing odds encountered with FAIL policy.")
    # For PROXY, we don't skip, but compute_trade_pnl will fallback
    return False
