import math
from typing import List, Tuple
from sports_signal_bot.sizing.contracts import KellyEstimateRecord


def validate_kelly_inputs(
    decimal_odds: float, calibrated_probability: float
) -> Tuple[bool, List[str]]:
    warnings = []
    is_valid = True

    if decimal_odds <= 1.0 or math.isnan(decimal_odds) or math.isinf(decimal_odds):
        warnings.append("Invalid decimal odds for Kelly calculation.")
        is_valid = False

    if (
        calibrated_probability < 0.0
        or calibrated_probability > 1.0
        or math.isnan(calibrated_probability)
    ):
        warnings.append("Invalid calibrated probability for Kelly calculation.")
        is_valid = False

    return is_valid, warnings


def compute_full_kelly_fraction(
    decimal_odds: float, calibrated_probability: float
) -> float:
    """
    Computes the full Kelly fraction.
    Kelly fraction = (b * p - q) / b
    where b = decimal_odds - 1 (the payout multiple)
    p = probability of winning
    q = probability of losing (1 - p)
    """
    is_valid, _ = validate_kelly_inputs(decimal_odds, calibrated_probability)
    if not is_valid:
        return 0.0

    b = decimal_odds - 1.0
    if b <= 0:
        return 0.0

    p = calibrated_probability
    q = 1.0 - p

    kelly_fraction = (b * p - q) / b

    # NaN/inf guardrail
    if math.isnan(kelly_fraction) or math.isinf(kelly_fraction):
        return 0.0

    return kelly_fraction


def compute_fractional_kelly(full_kelly: float, fraction: float) -> float:
    if full_kelly <= 0.0:
        return 0.0
    return full_kelly * fraction


def clip_kelly_fraction(kelly_fraction: float, max_fraction: float) -> float:
    if kelly_fraction <= 0.0:
        return 0.0
    return min(kelly_fraction, max_fraction)


def explain_kelly_estimate(
    decimal_odds: float, calibrated_probability: float, fraction: float = 1.0
) -> KellyEstimateRecord:
    is_valid, warnings = validate_kelly_inputs(decimal_odds, calibrated_probability)

    b = decimal_odds - 1.0 if is_valid and decimal_odds > 1.0 else 0.0
    p = calibrated_probability if is_valid else 0.0
    q = 1.0 - p if is_valid else 1.0

    full_kelly = compute_full_kelly_fraction(decimal_odds, calibrated_probability)
    fractional_kelly = compute_fractional_kelly(full_kelly, fraction)

    if full_kelly <= 0.0 and is_valid:
        warnings.append("Kelly estimate is zero or negative (no edge).")

    return KellyEstimateRecord(
        b=b,
        p=p,
        q=q,
        full_kelly_fraction=full_kelly,
        fractional_kelly_fraction=fractional_kelly,
        warnings=warnings,
    )
