import pytest
from sports_signal_bot.telegram_dispatch.routing import TelegramRoutingPolicy, TelegramRouter
from sports_signal_bot.telegram_dispatch.contracts import MessageType, MessageSeverity

@pytest.fixture
def policy():
    channels_config = {
        "channel_aliases": {
            "decisions_channel": "TELEGRAM_DECISIONS_CHAT_ID",
            "alarms_channel": "TELEGRAM_ALARMS_CHAT_ID",
            "summaries_channel": "TELEGRAM_SUMMARIES_CHAT_ID",
            "debug_channel": "TELEGRAM_DEBUG_CHAT_ID"
        }
    }
    routing_config = {
        "severity_to_channel": {
            "error": "alarms_channel",
            "critical": "alarms_channel"
        }
    }
    env_config = {
        "TELEGRAM_DECISIONS_CHAT_ID": "123",
        "TELEGRAM_ALARMS_CHAT_ID": "456",
        "TELEGRAM_SUMMARIES_CHAT_ID": "789",
        "TELEGRAM_DEBUG_CHAT_ID": "000"
    }
    return TelegramRoutingPolicy(channels_config, routing_config, env_config)

def test_resolve_target_channel_decision(policy):
    router = TelegramRouter(policy)
    res = router.route_message("msg1", MessageType.DECISION_ALERT, MessageSeverity.INFO, "production")
    assert res.assigned_channel == "decisions_channel"

def test_resolve_target_channel_alarm(policy):
    router = TelegramRouter(policy)
    res = router.route_message("msg2", MessageType.CRITICAL_ALARM, MessageSeverity.CRITICAL, "production")
    assert res.assigned_channel == "alarms_channel"

def test_resolve_target_channel_dry_run(policy):
    router = TelegramRouter(policy)
    res = router.route_message("msg3", MessageType.DECISION_ALERT, MessageSeverity.INFO, "dry_run")
    assert res.assigned_channel == "debug_channel"
