# Backtest Core Architecture

## Why Backtest After Policy?
The system is built as a highly robust event-driven inference pipeline. Evaluating prediction quality before policy ignores the context, boundaries, constraints, and business logic layered onto a model's raw probability output. A policy acts as the ultimate filter, effectively generating an actionable universe. This phase establishes a chronological replay engine capable of reading that final actionable universe and evaluating it as it would have sequentially occurred in real-time.

## Chronological Replay Lifecycle
1. **Input Generation**: Decision records from the policy engine and ground-truth label records are joined on `event_id` and `market_type`.
2. **Replay Planning**: To prevent temporal leakage or future look-ahead bias, events are sorted strictly chronologically based on `decision_timestamp_utc`, and optionally falling back to `event_datetime_utc` or lexical ordering.
3. **Execution Policy Resolution**: Before seeing the result, an execution policy assesses whether the event sits in a valid universe (e.g. `ApprovedOnlyExecution` or `CandidateAndApprovedExecution`). If valid, it is marked as `EXECUTABLE`.
4. **Settlement**: The engine resolves the realization of the event context (e.g. was the label `home`, `away`, `over`, `under`, `push`, `void`), against the selection.
5. **Ledger Generation**: A `BacktestLedgerRecord` is generated containing the executed trace, edge snapshot, policy context, and realization logic for detailed historical analysis.

## Execution Policies
In a replay phase, an execution is not placing a real bet but evaluating eligibility for simulation. This allows us to assess the performance of the system if different boundaries were applied.

Policies supported include:
- `ApprovedOnlyExecution`: Replays only decisions that achieved the absolute highest status.
- `CandidateAndApprovedExecution`: Adds secondary candidate plays.
- `WatchlistShadowExecution`: Shadow-runs plays that were kept on a watchlist but ordinarily un-executed.
- `CustomActionClassExecutionPolicy`: A highly flexible runtime override.

## Settlement and Ledger Design
The settlement engine translates ground truth outputs into `SettlementStatus`. It implements safe guards to handle voided occurrences (`SETTLED_VOID`), standard payouts (`SETTLED_WIN`, `SETTLED_LOSS`), and exact numeric pushes (`SETTLED_PUSH`).

The Ledger (`BacktestLedgerRecord`) merges all this into a unified structure tracking the `edge_snapshot`, `final_probability`, and execution trace.

## Period Summaries
`PeriodSummarizer` groups Ledger Records dynamically (e.g., daily, weekly) enabling a researcher to identify regime transitions where edge deteriorated temporarily or where volatility clustered within a specific timeframe.

## No-Bankroll-Yet Yaklaşımı
This system implements unitless, decision-quality-oriented metrics (Hit Rate, Brier, LogLoss, Edge correlation). Financial PnL structures (`stake_units`, `payout_multiplier`, `pnl_units`) exist strictly as placeholders in the data contracts. True dynamic staking requires a robust bankroll core overlaying this engine in a future phase.

## Future Extension Path
- **Bankroll Overlays**: Implementing Kelly Criterion, Flat Staking, or Fractional unit execution models parsing the ledger trace over a live state object.
- **Stake Sizing Analytics**: Producing drawdown metrics and maximum consecutive loss evaluations.
- **Capital Curves**: Transforming the sequential ledger trace into a chronological equity curve to evaluate Sharpe Ratio and Sortino characteristics on strategy profiles.
