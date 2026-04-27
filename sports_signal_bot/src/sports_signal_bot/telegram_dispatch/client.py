import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self, bot_token: str, timeout_seconds: int = 10):
        self.bot_token = bot_token
        self.timeout_seconds = timeout_seconds
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, chat_id: str, text: str, parse_mode: str = "MarkdownV2") -> Dict[str, Any]:
        """Sends a message via Telegram API."""
        if not self.bot_token:
             raise ValueError("Telegram bot token is not configured.")
        if not chat_id:
             raise ValueError("Chat ID is not provided.")

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }

        # Protect against exceedingly long messages (Telegram limit is 4096)
        if len(text) > 4000:
            logger.warning(f"Message length ({len(text)}) exceeds safe threshold. Truncating.")
            payload["text"] = text[:4000] + "\n\\.\\.\\.\\[TRUNCATED\\]"

        try:
            response = requests.post(self.api_url, json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram API error: {e}")
            raise
