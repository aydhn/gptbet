import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List

from .contracts import (
    TelegramMessageRecord,
    DeliveryStatus,
    DeliveryAttemptRecord,
)
from .client import TelegramClient
from .routing import TelegramRoutingPolicy

logger = logging.getLogger(__name__)


class TelegramSender:
    def __init__(
        self,
        client: TelegramClient,
        routing_policy: TelegramRoutingPolicy,
        delivery_config: Dict[str, Any],
    ):
        self.client = client
        self.routing_policy = routing_policy
        self.max_retries = delivery_config.get("retry_count", 3)
        self.max_workers = delivery_config.get("max_workers", 5)

    def send(
        self, message: TelegramMessageRecord, parse_mode: str = "MarkdownV2"
    ) -> List[DeliveryAttemptRecord]:
        attempts = []
        actual_chat_id = self.routing_policy.get_actual_chat_id(
            message.channel_name
        )

        if not actual_chat_id:
            logger.error(
                f"Cannot send message {message.message_id_local}: "
                f"No chat ID resolved for {message.channel_name}"
            )
            error_msg = f"Unresolved logical channel: {message.channel_name}"
            attempts.append(
                DeliveryAttemptRecord(
                    message_id_local=message.message_id_local,
                    status=DeliveryStatus.FAILED_FINAL,
                    error_message=error_msg,
                )
            )
            return attempts

        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    time.sleep(2**attempt)

                self.client.send_message(
                    chat_id=actual_chat_id,
                    text=message.body,
                    parse_mode=parse_mode,
                )

                attempts.append(
                    DeliveryAttemptRecord(
                        message_id_local=message.message_id_local,
                        status=DeliveryStatus.SENT,
                    )
                )
                return attempts

            except Exception as e:
                is_final = attempt == self.max_retries
                if is_final:
                    status = DeliveryStatus.FAILED_FINAL
                else:
                    status = DeliveryStatus.FAILED_RETRYABLE
                logger.warning(
                    f"Delivery attempt {attempt + 1} failed for "
                    f"{message.message_id_local}. Status: {status}. "
                    f"Error: {str(e)}"
                )
                attempts.append(
                    DeliveryAttemptRecord(
                        message_id_local=message.message_id_local,
                        status=status,
                        error_message=str(e),
                    )
                )

        return attempts

    def send_batch(
        self,
        messages: List[TelegramMessageRecord],
        parse_mode: str = "MarkdownV2",
    ) -> Dict[str, List[DeliveryAttemptRecord]]:
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_msg_id = {
                executor.submit(
                    self.send, msg, parse_mode
                ): msg.message_id_local
                for msg in messages
            }
            for future in as_completed(future_to_msg_id):
                msg_id = future_to_msg_id[future]
                try:
                    attempts = future.result()
                    results[msg_id] = attempts
                except Exception as e:
                    logger.error(
                        f"Unexpected error sending message {msg_id}: {str(e)}"
                    )
                    results[msg_id] = [
                        DeliveryAttemptRecord(
                            message_id_local=msg_id,
                            status=DeliveryStatus.FAILED_FINAL,
                            error_message=str(e),
                        )
                    ]
        return results
