import typer
from typing import Optional
from pathlib import Path

# Provide a mock integration with the CLI since main.py is too big to rewrite entirely here
# Instead, we define the commands we want to add and let them be imported

app = typer.Typer()

@app.command()
def run_dispatch(
    sport: str,
    market: str,
    slot: str = "current",
    dry_run: bool = False
):
    from sports_signal_bot.telegram_dispatch.runner import DispatchRunner
    from sports_signal_bot.telegram_dispatch.contracts import DispatchPayloadRecord
    from sports_signal_bot.telegram_dispatch.reporting import DispatchReporter
    from sports_signal_bot.telegram_dispatch.manifests import ManifestWriter
    from pathlib import Path

    # Mock configs for CLI demo
    env_config = {
         "TELEGRAM_BOT_TOKEN": "dummy_token" if dry_run else None, # Let missing token force dry run
         "TELEGRAM_DECISIONS_CHAT_ID": "123",
         "TELEGRAM_REVIEW_CHAT_ID": "123",
         "TELEGRAM_SUMMARIES_CHAT_ID": "123",
         "TELEGRAM_WARNINGS_CHAT_ID": "123",
         "TELEGRAM_ALARMS_CHAT_ID": "123",
         "TELEGRAM_DEBUG_CHAT_ID": "123"
    }
    channels_config = {
        "channel_aliases": {
            "decisions_channel": "TELEGRAM_DECISIONS_CHAT_ID",
            "review_channel": "TELEGRAM_REVIEW_CHAT_ID",
            "summaries_channel": "TELEGRAM_SUMMARIES_CHAT_ID",
            "warnings_channel": "TELEGRAM_WARNINGS_CHAT_ID",
            "alarms_channel": "TELEGRAM_ALARMS_CHAT_ID",
            "debug_channel": "TELEGRAM_DEBUG_CHAT_ID"
        }
    }
    routing_config = {
         "severity_to_channel": {
             "error": "alarms_channel",
             "critical": "alarms_channel"
         }
    }
    templates_config = {"dispatch_profiles": {"standard": True}}
    delivery_config = {"retry_count": 1}
    noise_config = {"duplicate_suppression_window_minutes": 60, "max_messages_per_slot": 100}

    runner = DispatchRunner(
        env_config=env_config,
        channels_config=channels_config,
        routing_config=routing_config,
        templates_config=templates_config,
        delivery_config=delivery_config,
        noise_config=noise_config,
        dry_run=dry_run
    )

    # Mock some data for demonstration
    payloads = [
         DispatchPayloadRecord(
             event_id="mock_event_1",
             market=market,
             sport=sport,
             decision_class="approved",
             signal_score=0.88,
             edge=0.06,
             allocated_stake=2.0,
             rationale="High edge, stable regime."
         ),
         DispatchPayloadRecord(
             event_id="mock_event_2",
             market=market,
             sport=sport,
             decision_class="candidate",
             signal_score=0.91,
             edge=0.08,
             allocated_stake=1.0,
             rationale="High edge but high disagreement.",
             warnings=["high_disagreement"]
         )
    ]

    mode = "dry_run" if dry_run else "production"
    manifest = runner.process_decisions(run_id="run_mock_001", slot=slot, mode=mode, payload_records=payloads)

    reporter = DispatchReporter(manifest)
    print(reporter.get_cli_output())

    writer = ManifestWriter(Path("data/processed/dispatch"))
    writer.write_manifest(manifest)

if __name__ == "__main__":
    app()
