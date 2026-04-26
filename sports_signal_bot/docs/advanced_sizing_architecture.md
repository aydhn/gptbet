# Advanced Sizing Architecture

This phase introduces an advanced, research-grade stake sizing engine. It replaces basic flat staking overlays with a robust, policy-driven architecture that translates signal edge and quality into dynamic bet sizes, primarily using heavily modified and bounded variations of the Kelly criterion.

## Why Advanced Sizing?
In early phases, the bankroll engine used a simple overlay system (e.g., bet $100 on everything). Advanced Sizing sits between the policy engine and the bankroll execution layer to answer *how much* to bet, rather than just *if* we should bet.

## Architecture

1. **Input Preparation**: The `StakeSizingInputRecord` gathers calibrated probabilities, market odds, edges, confidence scores, and current risk states (drawdown, streaks).
2. **Strategy Proposal**: A `BaseSizingStrategy` (e.g., `FractionalKellyOverlay`) proposes a raw stake fraction.
3. **Adjustments**: The proposed fraction is modified by dampeners (confidence, uncertainty, data quality, regime risk).
4. **Risk Limit Engine**: The adjusted fraction is subjected to absolute caps (per decision, action class), and throttles based on current bankroll drawdown and losing streaks.
5. **Resolution**: A final `SizingDecisionRecord` is produced, detailing exactly how the final stake was derived.

## Key Strategies
- `FractionalKellyOverlay`: Standard fractional Kelly (e.g., 0.25).
- `CappedFractionalKellyOverlay`: Fractional Kelly with strict absolute limits.
- `ConfidenceAdjustedKellyOverlay`: Scales the fraction based on signal confidence and uncertainty entropy.
- `EdgeBandSizingOverlay`: Simple band-based sizing ignoring exact Kelly math.
- `ConservativeResearchSizingOverlay`: Extremely low baseline size for testing risky concepts.

## Kelly Estimation vs. Final Resolution
The system intentionally separates Kelly calculation from the final stake. Kelly provides the theoretically optimal growth fraction assuming perfect probabilities. Since our probabilities are never perfect, we treat Kelly as a *raw input proposal* that must survive layers of skepticism (adjustments) and bankroll defense (risk limits) before execution.

## Future Extension Paths
- **Portfolio Allocation**: Transitioning from single-event sizing to slate-level covariance-aware optimization.
- **Regime-Aware Schedules**: Shifting base fractions dynamically based on broader market regimes.
- **Live Risk Controls**: Integrating with live bankroll freezes during severe intraday drawdowns.
