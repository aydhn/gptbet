import pytest
from sports_signal_bot.telegram_dispatch.contracts import (
    TelegramMessageRecord, MessageType, MessageSeverity
)

def test_telegram_message_record_creation():
    msg = TelegramMessageRecord(
        message_id_local="msg123",
        message_type=MessageType.DECISION_ALERT,
        severity=MessageSeverity.INFO,
        sport="football",
        channel_name="decisions_channel",
        title="Test Message",
        body="This is a test body."
    )
    assert msg.message_id_local == "msg123"
    assert msg.sport == "football"
    assert msg.channel_name == "decisions_channel"
