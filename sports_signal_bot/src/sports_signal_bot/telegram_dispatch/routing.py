from typing import Dict, Any, Optional
from .contracts import (
    MessageType,
    MessageSeverity,
    RoutingDecisionRecord
)
import logging

logger = logging.getLogger(__name__)

class TelegramRoutingPolicy:
    def __init__(self, channels_config: Dict[str, Any], routing_config: Dict[str, Any], env_config: Dict[str, str]):
        self.channels_config = channels_config
        self.routing_config = routing_config
        self.env_config = env_config
        self.channel_aliases = self.channels_config.get("channel_aliases", {})
        self.severity_map = self.routing_config.get("severity_to_channel", {})

    def resolve_target_channel(self, message_type: MessageType, severity: MessageSeverity, inference_mode: str = "production") -> str:
        """Determines the logical channel name based on routing rules."""

        # 1. Preview / Dry Run always goes to debug or summaries
        if inference_mode in ["preview", "dry_run"] or message_type == MessageType.DRY_RUN_PREVIEW:
             return "debug_channel" if "debug_channel" in self.channel_aliases else "summaries_channel"

        # 2. Type-based specific routing
        if message_type == MessageType.DECISION_ALERT:
            return "decisions_channel"
        elif message_type == MessageType.DECISION_REVIEW:
            return "review_channel"
        elif message_type in [MessageType.RUN_SUMMARY, MessageType.DAILY_DIGEST, MessageType.HEALTH_NOTICE]:
            return "summaries_channel"

        # 3. Severity-based routing (for warnings, errors, alarms)
        if severity.value in self.severity_map:
            return self.severity_map[severity.value]

        # 4. Fallback
        logger.warning(f"No specific route found for {message_type.value} with severity {severity.value}. Routing to summaries_channel.")
        return "summaries_channel"

    def get_actual_chat_id(self, logical_channel: str) -> Optional[str]:
        """Resolves the logical channel to an actual Telegram chat ID."""
        env_var_name = self.channel_aliases.get(logical_channel)
        if not env_var_name:
            logger.error(f"Logical channel {logical_channel} has no defined env_var in channels_config.")
            return None
        return self.env_config.get(env_var_name)

class TelegramRouter:
    def __init__(self, policy: TelegramRoutingPolicy):
        self.policy = policy

    def route_message(self, message_id: str, message_type: MessageType, severity: MessageSeverity, inference_mode: str = "production") -> RoutingDecisionRecord:
        logical_channel = self.policy.resolve_target_channel(message_type, severity, inference_mode)
        rationale = f"Routed based on message_type={message_type.value}, severity={severity.value}, mode={inference_mode}"
        return RoutingDecisionRecord(
            message_id_local=message_id,
            message_type=message_type,
            assigned_channel=logical_channel,
            rationale=rationale
        )
