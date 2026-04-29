from typing import Any, Dict, List, Union
import re

class RedactionEngine:
    def __init__(self, sensitive_fields: List[str] = None):
        self.sensitive_fields = sensitive_fields or [
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_DECISIONS_CHAT_ID",
            "TELEGRAM_REVIEW_CHAT_ID",
            "TELEGRAM_SUMMARIES_CHAT_ID",
            "TELEGRAM_WARNINGS_CHAT_ID",
            "TELEGRAM_ALARMS_CHAT_ID",
            "TELEGRAM_DEBUG_CHAT_ID"
        ]
        self.token_regex = re.compile(r"bot\d+:[a-zA-Z0-9_-]+")

    def redact_text(self, text: str) -> str:
        if not isinstance(text, str):
            return text
        # Regex based scrubbing
        redacted = self.token_regex.sub("bot***:***", text)
        return redacted

    def redact_payload(self, payload: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
        if isinstance(payload, dict):
            return self._redact_dict(payload)
        elif isinstance(payload, list):
            return [self.redact_payload(item) for item in payload]
        elif isinstance(payload, str):
            return self.redact_text(payload)
        return payload

    def _redact_dict(self, data: Dict) -> Dict:
        redacted_data = {}
        for k, v in data.items():
            if any(sensitive in k.upper() for sensitive in self.sensitive_fields):
                redacted_data[k] = "***REDACTED***"
            else:
                redacted_data[k] = self.redact_payload(v)
        return redacted_data
