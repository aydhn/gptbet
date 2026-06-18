import uuid
import logging
from typing import List, Dict, Any

from .contracts import (
    TelegramMessageRecord,
    DeliveryStatus,
    TelegramDispatchManifest,
    MessageType,
    MessageSeverity,
    DispatchPayloadRecord,
    SummaryMessageRecord,
    AlarmMessageRecord,
)
from .client import TelegramClient
from .sender import TelegramSender
from .routing import TelegramRoutingPolicy, TelegramRouter
from .templates import MessageTemplateEngine
from .noise_control import NoiseControlEngine
from .review_queue import ReviewQueueBuilder

logger = logging.getLogger(__name__)


class DispatchRunner:
    def __init__(
        self,
        env_config: Dict[str, str],
        channels_config: Dict[str, Any],
        routing_config: Dict[str, Any],
        templates_config: Dict[str, Any],
        delivery_config: Dict[str, Any],
        noise_config: Dict[str, Any],
        dry_run: bool = False,
    ):
        self.dry_run = dry_run

        self.routing_policy = TelegramRoutingPolicy(
            channels_config, routing_config, env_config
        )
        self.router = TelegramRouter(self.routing_policy)
        self.template_engine = MessageTemplateEngine(templates_config)
        self.noise_control = NoiseControlEngine(noise_config)
        self.review_builder = ReviewQueueBuilder()
        self.parse_mode = templates_config.get("parse_mode", "MarkdownV2")

        token = env_config.get("TELEGRAM_BOT_TOKEN")
        if not token and not self.dry_run:
            logger.warning("TELEGRAM_BOT_TOKEN missing. Forcing dry_run.")
            self.dry_run = True

        self.client = TelegramClient(bot_token=token if token else "dummy")
        self.sender = TelegramSender(
            self.client, self.routing_policy, delivery_config
        )

    def process_decisions(
        self,
        run_id: str,
        slot: str,
        mode: str,
        payload_records: List[DispatchPayloadRecord],
    ) -> TelegramDispatchManifest:
        manifest = TelegramDispatchManifest(run_id=run_id)
        messages: List[TelegramMessageRecord] = []

        for payload in payload_records:
            msg_id = f"msg_{uuid.uuid4().hex[:8]}"

            if payload.decision_class == "approved":
                msg_type = MessageType.DECISION_ALERT
                severity = MessageSeverity.INFO
                body = self.template_engine.render_decision(payload, run_id)
            elif payload.decision_class == "candidate":
                msg_type = MessageType.DECISION_REVIEW
                severity = MessageSeverity.INFO
                review_record = self.review_builder.build_from_candidate(
                    payload
                )
                body = self.template_engine.render_review(review_record)
            else:
                continue

            routing_decision = self.router.route_message(
                msg_id, msg_type, severity, inference_mode=mode
            )

            record = TelegramMessageRecord(
                message_id_local=msg_id,
                message_type=msg_type,
                severity=severity,
                sport=payload.sport,
                market_type=payload.market,
                channel_name=routing_decision.assigned_channel,
                title=f"Decision: {payload.event_id}",
                body=body,
                related_run_id=run_id,
                related_event_ids=[payload.event_id],
            )
            messages.append(record)

        messages = self.noise_control.apply_suppression(messages)
        messages = self.noise_control.enforce_slot_limit(messages)

        self._execute_delivery(messages, manifest)

        return manifest

    def process_summary(
        self,
        run_id: str,
        slot: str,
        mode: str,
        summary_record: SummaryMessageRecord,
    ) -> TelegramDispatchManifest:
        manifest = TelegramDispatchManifest(run_id=run_id)
        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        msg_type = MessageType.RUN_SUMMARY
        severity = MessageSeverity.INFO

        body = self.template_engine.render_summary(summary_record)
        routing_decision = self.router.route_message(
            msg_id, msg_type, severity, inference_mode=mode
        )

        record = TelegramMessageRecord(
            message_id_local=msg_id,
            message_type=msg_type,
            severity=severity,
            sport="all",
            channel_name=routing_decision.assigned_channel,
            title=f"Summary: {run_id}",
            body=body,
            related_run_id=run_id,
        )

        self._execute_delivery([record], manifest)
        return manifest

    def process_alarm(
        self,
        run_id: str,
        slot: str,
        mode: str,
        alarm_record: AlarmMessageRecord,
    ) -> TelegramDispatchManifest:
        manifest = TelegramDispatchManifest(run_id=run_id)
        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        if alarm_record.severity == MessageSeverity.CRITICAL:
            msg_type = MessageType.CRITICAL_ALARM
        else:
            msg_type = MessageType.PIPELINE_WARNING

        body = self.template_engine.render_alarm(alarm_record)
        routing_decision = self.router.route_message(
            msg_id, msg_type, alarm_record.severity, inference_mode=mode
        )

        record = TelegramMessageRecord(
            message_id_local=msg_id,
            message_type=msg_type,
            severity=alarm_record.severity,
            sport="system",
            channel_name=routing_decision.assigned_channel,
            title=f"Alarm: {alarm_record.incident_title}",
            body=body,
            related_run_id=run_id,
        )

        self._execute_delivery([record], manifest)
        return manifest

    def _execute_delivery(
        self,
        messages: List[TelegramMessageRecord],
        manifest: TelegramDispatchManifest,
    ):
        from .contracts import TelegramDispatchRecord

        active_messages = []

        for msg in messages:
            manifest.total_messages_rendered += 1

            if self.dry_run:
                msg.delivery_status = DeliveryStatus.DRY_RUN_ONLY
                record = TelegramDispatchRecord(
                    message=msg, final_status=DeliveryStatus.DRY_RUN_ONLY
                )
                manifest.records.append(record)
                logger.info(
                    f"[DRY RUN] Would send to {msg.channel_name}:\n{msg.body}"
                )
                continue

            if msg.delivery_status == DeliveryStatus.SUPPRESSED:
                manifest.suppressed_count += 1
                record = TelegramDispatchRecord(
                    message=msg, final_status=DeliveryStatus.SUPPRESSED
                )
                manifest.records.append(record)
                continue

            active_messages.append(msg)

        if not active_messages:
            return

        batch_results = self.sender.send_batch(
            active_messages, parse_mode=self.parse_mode
        )

        for msg in active_messages:
            attempts = batch_results.get(msg.message_id_local, [])
            if attempts:
                final_status = attempts[-1].status
            else:
                final_status = DeliveryStatus.FAILED_FINAL
            msg.delivery_status = final_status

            record = TelegramDispatchRecord(
                message=msg, attempts=attempts, final_status=final_status
            )
            manifest.records.append(record)

            if final_status == DeliveryStatus.SENT:
                manifest.total_messages_sent += 1
            elif final_status in [
                DeliveryStatus.FAILED_FINAL,
                DeliveryStatus.FAILED_RETRYABLE,
            ]:
                manifest.final_failures_count += 1

            manifest.retry_count += max(0, len(attempts) - 1)

            ch_bd = manifest.channel_breakdown.get(msg.channel_name, 0)
            manifest.channel_breakdown[msg.channel_name] = ch_bd + 1

            sev_v = msg.severity.value
            sev_bd = manifest.severity_breakdown.get(sev_v, 0)
            manifest.severity_breakdown[sev_v] = sev_bd + 1
