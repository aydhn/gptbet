# Bankroll Overlay Architecture

## Purpose
The bankroll overlay layer is designed to sit on top of the established `backtest ledger`. It bridges the gap between raw decision evaluation ("Was this the right choice?") and simulated capital management ("What would our bankroll look like under these decisions?").

## Overlay Strategies
This layer supports multiple placeholder strategies, allowing researchers to explore capital curves without attempting fully optimized Kelly sizing too early.
Supported overlays:
- **Flat Stake**: Consistently uses `flat_stake_units` for every approved decision.
- **Fixed Fraction**: Places a static percentage of the current bankroll per bet.
- **Tiered Flat**: Places larger flat stakes for high-confidence decisions (approved candidate) vs smaller stakes for candidate decisions.
- **Conservative Capped Fraction**: Fixed fraction with hard unit floors and ceilings.
- **No Financial Shadow**: Useful as a baseline, bypasses actual financial processing.

## Capital Accounting
- **Chronological Requirement**: Capital curves and drawdowns must be processed sequentially.
- **Ledger Records**: For each execution, it outputs bankroll before/after, PnL units/percent, and warnings.
- **Drawdown and Streaks**: Tracks peak-to-trough (drawdown) absolute and percentage figures dynamically as well as win/loss streaks to monitor performance stability.

## Safety Guardrails
- Implements `missing_odds_policy` allowing options to skip, proxy, or fail when odds are missing.
- Prevents negative bankrolls via `enforce_bankroll_floor`.
- Respects max constraints on the amount a given stake can occupy.

## Future Extensibility
This baseline allows simple plug-and-play for:
- Fully dynamic Kelly fractional betting.
- Multi-bet concurrent exposure models.
- Deep integration with regime-aware portfolio rules.
