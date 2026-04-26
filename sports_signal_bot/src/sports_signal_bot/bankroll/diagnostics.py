from typing import List, Tuple
from sports_signal_bot.bankroll.contracts import BankrollConfig

def validate_bankroll_inputs(bankroll: float, config: BankrollConfig) -> List[str]:
    warnings = []
    if bankroll <= 0:
        warnings.append("Initial bankroll is zero or negative.")
    if config.max_fraction_per_decision <= 0:
        warnings.append("Max fraction per decision is zero or negative.")
    return warnings

def apply_stake_caps(stake_units: float, current_bankroll: float, config: BankrollConfig) -> Tuple[float, List[str]]:
    warnings = []
    original_stake = stake_units

    if stake_units < config.min_stake_units:
        warnings.append(f"Stake {stake_units} below minimum. Adjusted to {config.min_stake_units}.")
        stake_units = config.min_stake_units

    if stake_units > config.max_stake_units:
        warnings.append(f"Stake {stake_units} above absolute maximum. Capped at {config.max_stake_units}.")
        stake_units = config.max_stake_units

    max_allowed_by_fraction = current_bankroll * config.max_fraction_per_decision
    if stake_units > max_allowed_by_fraction:
        warnings.append(f"Stake {stake_units} above max fraction. Capped at {max_allowed_by_fraction}.")
        stake_units = max_allowed_by_fraction

    if config.round_stakes_to is not None and config.round_stakes_to > 0:
        stake_units = round(stake_units / config.round_stakes_to) * config.round_stakes_to

    return stake_units, warnings

def enforce_bankroll_floor(bankroll_after_bet: float, config: BankrollConfig) -> Tuple[float, List[str]]:
    warnings = []
    if bankroll_after_bet < config.bankroll_floor:
        warnings.append(f"Bankroll fell below floor. Adjusted from {bankroll_after_bet} to {config.bankroll_floor}.")
        return config.bankroll_floor, warnings
    return bankroll_after_bet, warnings

def summarize_risk_warnings(warnings: List[str]) -> str:
    if not warnings:
        return "No warnings."
    return " | ".join(warnings)
