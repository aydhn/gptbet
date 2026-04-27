import pytest
from sports_signal_bot.telegram_dispatch.sender import TelegramSender
from sports_signal_bot.telegram_dispatch.contracts import TelegramMessageRecord, MessageType, MessageSeverity
from sports_signal_bot.telegram_dispatch.routing import TelegramRoutingPolicy

class MockClientFail:
    def __init__(self, fails_before_success=2):
        self.fails = 0
        self.fails_before_success = fails_before_success
    def send_message(self, chat_id, text, parse_mode="MarkdownV2"):
        if self.fails < self.fails_before_success:
            self.fails += 1
            raise Exception("Network error")
        return {"ok": True}

def test_sender_retry_success():
    channels_config = {"channel_aliases": {"dec_chan": "DEC_ID"}}
    policy = TelegramRoutingPolicy(channels_config, {}, {"DEC_ID": "123"})
    client = MockClientFail(fails_before_success=2)

    # Needs to be fast for tests, replace time.sleep locally if possible, but for simplicity here we just use it
    import time
    original_sleep = time.sleep
    time.sleep = lambda x: None

    try:
        sender = TelegramSender(client, policy, {"retry_count": 3})
        msg = TelegramMessageRecord(
            message_id_local="1",
            message_type=MessageType.DECISION_ALERT,
            severity=MessageSeverity.INFO,
            sport="football",
            channel_name="dec_chan",
            title="T",
            body="B"
        )

        attempts = sender.send(msg)
        assert len(attempts) == 3
        assert attempts[0].status.value == "failed_retryable"
        assert attempts[1].status.value == "failed_retryable"
        assert attempts[2].status.value == "sent"
    finally:
        time.sleep = original_sleep
