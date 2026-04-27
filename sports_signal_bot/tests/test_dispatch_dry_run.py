import pytest
from sports_signal_bot.telegram_dispatch.runner import DispatchRunner
from sports_signal_bot.telegram_dispatch.contracts import DispatchPayloadRecord

def test_dry_run_forces_no_send():
    env_config = {
         "TELEGRAM_BOT_TOKEN": "dummy",
         "TELEGRAM_DECISIONS_CHAT_ID": "123",
         "TELEGRAM_REVIEW_CHAT_ID": "123",
         "TELEGRAM_SUMMARIES_CHAT_ID": "123",
         "TELEGRAM_WARNINGS_CHAT_ID": "123",
         "TELEGRAM_ALARMS_CHAT_ID": "123",
         "TELEGRAM_DEBUG_CHAT_ID": "123"
    }
    channels_config = {
        "channel_aliases": {
            "decisions_channel": "TELEGRAM_DECISIONS_CHAT_ID"
        }
    }

    runner = DispatchRunner(
        env_config=env_config,
        channels_config=channels_config,
        routing_config={"severity_to_channel": {}},
        templates_config={"dispatch_profiles": {"short": True}},
        delivery_config={},
        noise_config={},
        dry_run=True
    )

    payloads = [
         DispatchPayloadRecord(
             event_id="mock_event_1",
             market="1x2",
             sport="football",
             decision_class="approved",
             signal_score=0.88,
             edge=0.06,
             allocated_stake=2.0,
             rationale="High edge."
         )
    ]

    manifest = runner.process_decisions("run-1", "slot-1", "dry_run", payloads)
    assert manifest.total_messages_sent == 0
    assert manifest.total_messages_rendered == 1
    assert manifest.records[0].final_status.value == "dry_run_only"
