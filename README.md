# gptbet

## Scheduled Orchestration
The system features a scheduled orchestration backbone to automate `ingest`, `inference`, `dispatch`, and `monitoring` jobs across defined time slots (morning, midday, evening).
You can run the scheduler manually via CLI:
```bash
python -m sports_signal_bot.main scheduler run-scheduler --slot evening --strategy conservative_ops
```
For architecture details, refer to `docs/scheduled_orchestration_architecture.md`.
