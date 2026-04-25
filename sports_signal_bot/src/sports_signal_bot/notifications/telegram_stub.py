import logging

from .interfaces import BaseNotifier

logger = logging.getLogger(__name__)


class TelegramNotifierStub(BaseNotifier):
    def send_message(self, message: str) -> bool:
        logger.info(f"TELEGRAM STUB: Sending message -> {message}")
        return True
