from typing import List, Tuple
from sports_signal_bot.sizing.contracts import SizingConfig, RiskLimitRecord


def apply_per_decision_caps(
    fraction: float, config: SizingConfig, action_class: str
) -> Tuple[float, List[str]]:
    warnings = []
    capped_fraction = fraction

    # 1. Action Class Specific Cap
    if action_class in config.action_class_fraction_caps:
        ac_cap = config.action_class_fraction_caps[action_class]
        if capped_fraction > ac_cap:
            capped_fraction = ac_cap
            warnings.append(f"Capped by action class ({action_class}) limit: {ac_cap}")

    # 2. Global Max Fraction Cap
    if capped_fraction > config.max_fraction_per_decision:
        capped_fraction = config.max_fraction_per_decision
        warnings.append(
            f"Capped by global max fraction limit: {config.max_fraction_per_decision}"
        )

    return capped_fraction, warnings


def apply_drawdown_throttle(
    current_drawdown_pct: float, config: SizingConfig
) -> Tuple[float, List[str]]:
    warnings = []
    multiplier = 1.0

    if not config.drawdown_throttle_bands:
        return multiplier, warnings

    # Sort thresholds descending to find the highest applicable band
    bands = sorted(
        config.drawdown_throttle_bands.items(), key=lambda x: x[0], reverse=True
    )

    for threshold, throttle in bands:
        if current_drawdown_pct >= threshold:
            multiplier = throttle
            warnings.append(
                f"Drawdown throttle applied ({threshold*100}% DD): {multiplier}x"
            )
            break

    return multiplier, warnings


def apply_streak_throttle(
    current_loss_streak: int, config: SizingConfig
) -> Tuple[float, List[str]]:
    warnings = []
    multiplier = 1.0

    if not config.losing_streak_throttle_bands:
        return multiplier, warnings

    # Sort descending
    bands = sorted(
        config.losing_streak_throttle_bands.items(), key=lambda x: x[0], reverse=True
    )

    for threshold, throttle in bands:
        if current_loss_streak >= threshold:
            multiplier = throttle
            warnings.append(
                f"Losing streak throttle applied ({threshold} losses): {multiplier}x"
            )
            break

    return multiplier, warnings


def apply_bankroll_floor_guard(
    proposed_stake_units: float, current_bankroll: float, config: SizingConfig
) -> Tuple[float, List[str]]:
    warnings = []

    if proposed_stake_units <= 0:
        return 0.0, warnings

    available = current_bankroll - config.bankroll_floor_buffer
    if available <= 0:
        warnings.append(f"Insufficient bankroll buffer. Stake reduced to 0.")
        return 0.0, warnings

    if proposed_stake_units > available:
        warnings.append(
            f"Capped by bankroll floor buffer. Reduced from {proposed_stake_units} to {available}."
        )
        return available, warnings

    return proposed_stake_units, warnings


def apply_unit_caps(
    proposed_stake_units: float, config: SizingConfig
) -> Tuple[float, List[str]]:
    warnings = []
    final_stake = proposed_stake_units

    if final_stake > config.max_stake_units:
        final_stake = config.max_stake_units
        warnings.append(f"Capped by absolute max stake units: {config.max_stake_units}")

    if final_stake < config.min_stake_units and final_stake > 0:
        warnings.append(
            f"Stake below min viable units ({config.min_stake_units}). Zeroed."
        )
        final_stake = 0.0

    return final_stake, warnings


def summarize_risk_limit_impacts(
    original_fraction: float,
    final_fraction: float,
    throttle_mult: float,
    caps_applied: bool,
) -> RiskLimitRecord:
    return RiskLimitRecord(
        per_decision_capped=caps_applied,
        throttle_multiplier=throttle_mult,
        original_fraction=original_fraction,
        capped_fraction=final_fraction,
    )


class RiskLimitEngine:
    def __init__(self, config: SizingConfig):
        self.config = config

    def resolve_size(
        self,
        initial_fraction: float,
        current_bankroll: float,
        current_drawdown: float,
        current_loss_streak: int,
        action_class: str,
    ) -> Tuple[float, float, List[str], List[str]]:
        """
        Applies throttles and caps to resolve the final fraction and stake units.
        Returns: (final_fraction, final_stake_units, throttles_applied, caps_applied)
        """
        throttles = []
        caps = []

        fraction = initial_fraction

        # 1. Throttles (Drawdown & Streak)
        dd_mult, dd_warn = apply_drawdown_throttle(current_drawdown, self.config)
        strk_mult, strk_warn = apply_streak_throttle(current_loss_streak, self.config)

        throttle_mult = dd_mult * strk_mult
        if dd_warn:
            throttles.extend(dd_warn)
        if strk_warn:
            throttles.extend(strk_warn)

        fraction *= throttle_mult

        # 2. Fraction Caps
        fraction, cap_warn = apply_per_decision_caps(
            fraction, self.config, action_class
        )
        if cap_warn:
            caps.extend(cap_warn)

        # 3. Convert to Units
        proposed_units = fraction * current_bankroll

        # 4. Bankroll & Unit Caps
        proposed_units, floor_warn = apply_bankroll_floor_guard(
            proposed_units, current_bankroll, self.config
        )
        if floor_warn:
            caps.extend(floor_warn)

        final_units, unit_warn = apply_unit_caps(proposed_units, self.config)
        if unit_warn:
            caps.extend(unit_warn)

        # Recalculate final fraction based on actual units allocated
        final_fraction = final_units / current_bankroll if current_bankroll > 0 else 0.0

        return final_fraction, final_units, throttles, caps
