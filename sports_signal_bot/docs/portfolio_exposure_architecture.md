# Portfolio & Exposure Architecture (Phase 23)

## Why Portfolio After Event-Level Sizing?
The sizing engine determines the optimal stake for a *single isolated event* (e.g., using Kelly Criterion with confidence and uncertainty overlays). However, in the real world, multiple events often occur simultaneously or within the same day. Deploying the optimally sized stake for each individual event blindly can lead to extreme risk concentration or overextending the daily risk budget.

The Portfolio layer steps in *after* the sizing engine to:
- Group concurrent events.
- Enforce daily, sport, market, and action-class risk budgets.
- Mitigate concentration risk.
- Ensure risk is deployed safely across the entire portfolio.

## Time Buckets and Concurrent Risk
Events that happen within the same configurable timeframe (e.g., a 60-minute bucket) are evaluated together. This ensures that the portfolio can rank concurrent opportunities and allocate the limited time-bucket budget (e.g., max 5% of bankroll per hour) to the most promising candidates first.

## Budget Cascade
Every candidate goes through a strict budget cascade limit evaluation:
1. **Global Daily Limit** (e.g., 15% of bankroll)
2. **Time Bucket Limit** (e.g., 5% of bankroll per bucket)
3. **Sport Limit** (e.g., 10% for football)
4. **Market Limit** (e.g., 5% for 1x2)
5. **Action Class Limit** (e.g., 15% for approved candidates)

The *minimum* available budget across all these dimensions dictates the absolute maximum stake a candidate can be allocated.

## Concentration and Correlation Placeholders
To avoid putting too many eggs in one basket:
- **Concentration Penalties**: Small percentage penalties applied to proposed stakes when the portfolio already holds significant exposure in the same sport or market.
- **Correlation Guard**: A strict check that prevents allocating capital to highly correlated markets within the same event (e.g., backing a team on the Moneyline while simultaneously betting the Over in the same game, risking double exposure to a single match script).

## Allocation Strategies
- **Sequential Cap**: Ranks candidates by priority and allocates fully until the budget runs dry. Simple and robust.
- **Proportional Priority**: Distributes the time bucket budget across all candidates in the bucket proportional to their priority scores.
- **Tiered Action Class**: Ensures top-tier signals get funded first.
- **Conservative Exposure**: High penalties for concentration and strict budget limits.
- **Budget Reserve**: Keeps a portion of the daily budget reserved for late-day opportunities.
- **Shadow No Allocation**: Useful for backtesting the sizing engine without actual deployment constraints.

## Future Extension Path
- **Covariance-Aware Allocation**: Transition from placeholder correlation guards to actual covariance matrices for mean-variance optimization.
- **Live Exposure Tracking**: Real-time integration with open orders across multiple books.
- **Portfolio Freeze Rules**: Instantly halt new allocations if a rapid sequence of losses breaches a daily pain threshold.
- **Market Clustering**: Grouping similar markets (e.g., Asian Handicap and Spread) dynamically based on historical correlation rather than manual placeholders.
