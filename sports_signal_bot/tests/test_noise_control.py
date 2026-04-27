import pytest
from sports_signal_bot.telegram_dispatch.noise_control import NoiseControlEngine
from sports_signal_bot.telegram_dispatch.contracts import TelegramMessageRecord, MessageType, MessageSeverity, DeliveryStatus

def test_duplicate_suppression():
    engine = NoiseControlEngine({"duplicate_suppression_window_minutes": 60})

    msg1 = TelegramMessageRecord(
        message_id_local="1",
        message_type=MessageType.DECISION_ALERT,
        severity=MessageSeverity.INFO,
        sport="football",
        market_type="1x2",
        channel_name="dec",
        title="T1",
        body="B1",
        related_event_ids=["E1"]
    )

    msg2 = TelegramMessageRecord(
        message_id_local="2",
        message_type=MessageType.DECISION_ALERT,
        severity=MessageSeverity.INFO,
        sport="football",
        market_type="1x2", # Same event and market
        channel_name="dec",
        title="T2",
        body="B2",
        related_event_ids=["E1"]
    )

    res = engine.apply_suppression([msg1, msg2])
    assert len(res) == 2
    assert res[0].delivery_status == DeliveryStatus.QUEUED
    assert res[1].delivery_status == DeliveryStatus.SUPPRESSED
