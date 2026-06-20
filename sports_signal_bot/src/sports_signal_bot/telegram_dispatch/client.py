import logging
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self, bot_token: str, timeout_seconds: int = 10):
        self.bot_token = bot_token
        self.timeout_seconds = timeout_seconds

        # fmt: off
        self.api_url = (
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        )
        # fmt: on

        self.session = requests.Session()

        # fmt: off
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=20, pool_maxsize=20
        )
        # fmt: on

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: str = "MarkdownV2",
    ) -> Dict[str, Any]:
        """Sends a message via Telegram API."""
        if not self.bot_token:
            raise ValueError("Telegram bot token is not configured.")
        if not chat_id:
            raise ValueError("Chat ID is not provided.")

        payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}

        # Protect against exceedingly long messages (Telegram limit is 4096)
        if len(text) > 4000:
            # fmt: off
            logger.warning(
                f"Message length ({len(text)}) exceeds safe "
                "threshold. Truncating."
            )
            # fmt: on
            payload["text"] = text[:4000] + "\n\\.\\.\\.\\[TRUNCATED\\]"

        try:
            # fmt: off
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=self.timeout_seconds
            )
            # fmt: on
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram API error: {e}")
            raise
