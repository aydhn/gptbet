# Policy Engine Architecture

## Why Policy After Scoring and Thresholds?
The policy engine acts as a critical quantitative decision layer before signals reach the bankroll / bet placement phase. While scoring outputs pure signal probabilities and thresholds define basic acceptability cutoffs, they lack context. A signal might have a high score, but what if there's significant disagreement among sources? What if the data quality is too low? The policy engine evaluates all these factors to assign an operational `ActionClass`.

## Signal Status and Action Lifecycle
A signal enters the policy engine with a `status=SCORED`. It is passed through multiple rule sets:
- **Hard Blocks**: Invalid configurations, lack of market reference, etc.
- **No-Bet Zone**: High uncertainty, score in gray zone, missing edge.
- **Watchlist**: Stronger than no-bet, but not strong enough for a candidate.
- **Candidate**: Passed basic requirements.
- **Approval**: Candidate met all robust criteria (e.g., very high score and low uncertainty).

If a signal hits a negative rule, its status is degraded (e.g., `BLOCKED` or `NO_BET_ZONE`). If it passes all the way, it may become `APPROVED`.

The statuses map directly to `ActionClass`:
- `BLOCKED` / `REJECTED` -> `blocked_candidate` / `no_action`
- `NO_BET_ZONE` / `WEAK_SIGNAL` -> `no_action` / `watchlist`
- `CANDIDATE` -> `candidate`
- `APPROVED` -> `approved_candidate`

## No-Bet Zone Philosophy
The *No-Bet Zone* is a first-class concept. It's built for situations where a signal is decent but fails secondary quality checks, such as high uncertainty or borderline edge. Identifying this zone explicitly prevents false positives from entering the action pipeline, saving bankroll and allowing systematic monitoring of borderline situations.

## Rationale Codes
Decisions generate *Rationale Codes* (e.g., `high_uncertainty`, `passed_score_threshold`, `missing_market_reference`). These codes provide complete traceability and transparency for why a signal was blocked, approved, or put into the no-bet zone.

## Future Extension Path
- **Bankroll-Aware Gating**: Linking the generated `ActionClass` into live bankroll management logic.
- **Live Dispatch Rules**: Only sending `APPROVED` signals to Telegram.
- **Manual Review Workflows**: Utilizing `OverrideReasonRecord` to bypass policy via CLI/UI.
