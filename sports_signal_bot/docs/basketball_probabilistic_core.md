# Basketball Probabilistic Core

## Design Philosophy
Unlike football, which operates in a low-scoring, Poisson-friendly environment, basketball scoring is high-volume and continuous in nature. Modeling basketball using a Poisson matrix is computationally expensive and conceptually flawed (e.g., discrete point increments don't map perfectly due to 2-point and 3-point shots).

To address this, we use a **Structural Points Model** paired with a **Normal Approximation Core**.

### Expected Points
We model `expected_home_points` and `expected_away_points` by starting from a base total and an expected split, and applying structural adjustments:
- **Pace:** A blend of home and away tempo proxies.
- **Offense vs. Defense:** Comparing home offensive efficiency proxy against away defensive resistance proxy.
- **Form / Fatigue:** Incorporating recent shifts in tempo or back-to-back penalties.
- **Ratings:** ELO or other strength metrics mapping into point spread differentials.

### Normal Approximation
Given `expected_total` and `expected_margin`, we approximate the distributions of total points and point margins using Gaussian (Normal) distributions:
- `Margin ~ N(expected_margin, margin_std)`
- `Total ~ N(expected_total, total_std)`

Using standard cumulative distribution functions (CDF) and survival functions (SF), we can extract continuous probabilities:
- **Moneyline:** `P(Home Win) = P(Margin > 0)`
- **Spread:** `P(Home Cover) = P(Margin > -spread_line)`
- **Totals:** `P(Over) = P(Total > line)`

## Sign Convention
For Spreads, we use standard US conventions:
- A negative spread (e.g., `-5.5`) means the team is the **favorite** and must win by more than 5.5 points to cover.
- A positive spread (e.g., `+3.5`) means the team is the **underdog** and covers if they win, tie, or lose by less than 3.5 points.

## Limitations & Future Extensions
- **Constant Variance:** Currently, `total_std` and `margin_std` are primarily fixed parameters defined in `configs/probabilistic/basketball.yaml`. While feature-driven hooks exist (`total_std_modifier`), dynamic variance modeling is a future goal.
- **Team Totals:** We do not currently decompose the overall variance matrix into correlated home and away variances (e.g., using copulas). This is required to accurately price "Team Totals" markets.
- **Possession Simulation:** A full micro-simulation of possessions is deliberately avoided in this phase for simplicity, though the architecture supports swapping the `ExpectedPointsBuilder` with a simulation engine.
