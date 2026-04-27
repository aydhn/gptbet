import datetime
from typing import List, Dict, Any, Set
from .contracts import TelegramMessageRecord, DeliveryStatus

class NoiseControlEngine:
    def __init__(self, noise_config: Dict[str, Any]):
        self.config = noise_config
        self.suppression_window_minutes = self.config.get("duplicate_suppression_window_minutes", 60)
        self.max_messages = self.config.get("max_messages_per_slot", 100)

        # State tracking (in a real app, this might be Redis or a local DB)
        self.recently_sent: Dict[str, datetime.datetime] = {}

    def _generate_signature(self, msg: TelegramMessageRecord) -> str:
        """Generates a unique signature for suppression purposes."""
        # E.g., duplicate decision alerts for same event+market
        if msg.related_event_ids and msg.market_type:
            event_keys = "-".join(sorted(msg.related_event_ids))
            return f"{msg.message_type.value}_{event_keys}_{msg.market_type}"
        return f"{msg.message_type.value}_{msg.title}"

    def apply_suppression(self, messages: List[TelegramMessageRecord]) -> List[TelegramMessageRecord]:
        """Filters out duplicate or low-priority noisy messages."""
        now = datetime.datetime.utcnow()
        filtered = []

        # Cleanup old cache
        cutoff = now - datetime.timedelta(minutes=self.suppression_window_minutes)
        self.recently_sent = {k: v for k, v in self.recently_sent.items() if v > cutoff}

        for msg in messages:
            sig = self._generate_signature(msg)
            if sig in self.recently_sent:
                # Suppress
                msg.delivery_status = DeliveryStatus.SUPPRESSED
                msg.warnings.append(f"Suppressed duplicate signature: {sig}")
                # We still keep it in the list (or return it) so manifest knows about it,
                # but runner will skip it based on status.
                filtered.append(msg)
            else:
                self.recently_sent[sig] = now
                filtered.append(msg)

        return filtered

    def enforce_slot_limit(self, messages: List[TelegramMessageRecord]) -> List[TelegramMessageRecord]:
         # Basic hard cap
         if len(messages) <= self.max_messages:
             return messages

         # Sort by severity (critical first) if we need to truncate
         # This is a basic implementation
         severity_order = {"critical": 0, "error": 1, "warning": 2, "info": 3, "silent": 4}
         sorted_msgs = sorted(messages, key=lambda m: severity_order.get(m.severity.value, 99))

         for msg in sorted_msgs[self.max_messages:]:
              msg.delivery_status = DeliveryStatus.SUPPRESSED
              msg.warnings.append("Suppressed due to max_messages_per_slot limit.")

         return sorted_msgs
