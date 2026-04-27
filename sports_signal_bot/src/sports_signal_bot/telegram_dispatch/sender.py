import logging
import time
from typing import Dict, Any, List
from .contracts import TelegramMessageRecord, DeliveryStatus, DeliveryAttemptRecord
from .client import TelegramClient
from .routing import TelegramRoutingPolicy

logger = logging.getLogger(__name__)

class TelegramSender:
    def __init__(self, client: TelegramClient, routing_policy: TelegramRoutingPolicy, delivery_config: Dict[str, Any]):
        self.client = client
        self.routing_policy = routing_policy
        self.max_retries = delivery_config.get("retry_count", 3)

    def send(self, message: TelegramMessageRecord, parse_mode: str = "MarkdownV2") -> List[DeliveryAttemptRecord]:
        attempts = []
        actual_chat_id = self.routing_policy.get_actual_chat_id(message.channel_name)

        if not actual_chat_id:
            logger.error(f"Cannot send message {message.message_id_local}: No chat ID resolved for {message.channel_name}")
            attempts.append(DeliveryAttemptRecord(
                message_id_local=message.message_id_local,
                status=DeliveryStatus.FAILED_FINAL,
                error_message=f"Unresolved logical channel: {message.channel_name}"
            ))
            return attempts

        for attempt in range(self.max_retries + 1):
            try:
                # Add delay between retries
                if attempt > 0:
                     time.sleep(2 ** attempt) # exponential backoff 1, 2, 4 seconds

                self.client.send_message(
                    chat_id=actual_chat_id,
                    text=message.body,
                    parse_mode=parse_mode
                )

                attempts.append(DeliveryAttemptRecord(
                    message_id_local=message.message_id_local,
                    status=DeliveryStatus.SENT
                ))
                return attempts # Success

            except Exception as e:
                is_final = (attempt == self.max_retries)
                status = DeliveryStatus.FAILED_FINAL if is_final else DeliveryStatus.FAILED_RETRYABLE
                logger.warning(f"Delivery attempt {attempt + 1} failed for {message.message_id_local}. Status: {status}. Error: {str(e)}")
                attempts.append(DeliveryAttemptRecord(
                    message_id_local=message.message_id_local,
                    status=status,
                    error_message=str(e)
                ))

        return attempts
