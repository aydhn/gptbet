# gptbet

## Release Management
The Release Management layer governs artifact promotion from candidate -> canary -> stable. It ensures that changes are validated, anomalies can trigger rollbacks, and inference uses the correct channel state.
You can interact with the release engine via CLI:
```bash
python -m sports_signal_bot.main release preview-release-channels --sport football --market 1x2
python -m sports_signal_bot.main release run-release --sport football --market 1x2 --strategy conservative_promotion
```
For architecture details, refer to `docs/release_promotion_architecture.md`.

## Scheduled Orchestration
The system features a scheduled orchestration backbone to automate `ingest`, `inference`, `dispatch`, and `monitoring` jobs across defined time slots (morning, midday, evening).
You can run the scheduler manually via CLI:
```bash
python -m sports_signal_bot.main scheduler run-scheduler --slot evening --strategy conservative_ops
```
For architecture details, refer to `docs/scheduled_orchestration_architecture.md`.
