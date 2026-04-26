from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.inference.contracts import SlotDefinitionRecord

logger = get_logger("SlotResolver")


class SlotResolver:
    def __init__(self, slot_configs: Optional[Dict[str, dict]] = None):
        self.configs = slot_configs or {
            "morning": {
                "name": "Morning Preview",
                "lookahead_window_hours": 24,
                "event_inclusion_horizon_hours": 1,
                "freshness_requirement_minutes": 120,
                "allowed_markets": ["1x2", "ou_2_5", "moneyline", "spread", "totals"],
                "artifact_resolution_policy": "latest_compatible",
                "output_profile": "analyst_review",
            },
            "midday": {
                "name": "Midday Refinement",
                "lookahead_window_hours": 12,
                "event_inclusion_horizon_hours": 1,
                "freshness_requirement_minutes": 60,
                "allowed_markets": ["1x2", "ou_2_5", "moneyline", "spread"],
                "artifact_resolution_policy": "latest_stable",
                "output_profile": "concise_ops",
            },
            "evening": {
                "name": "Evening Action",
                "lookahead_window_hours": 6,
                "event_inclusion_horizon_hours": 0,  # Strict
                "freshness_requirement_minutes": 15,
                "allowed_markets": ["1x2", "ou_2_5", "moneyline", "spread"],
                "artifact_resolution_policy": "latest_stable",  # Conservative
                "output_profile": "concise_ops",
            },
        }

    def resolve_slot_definition(self, slot_id: str) -> SlotDefinitionRecord:
        if slot_id not in self.configs:
            logger.warning(f"Slot '{slot_id}' not found. Using generic fallback.")
            return SlotDefinitionRecord(slot_id=slot_id, name="Custom Slot")

        cfg = self.configs[slot_id]
        return SlotDefinitionRecord(
            slot_id=slot_id,
            name=cfg["name"],
            lookahead_window_hours=cfg.get("lookahead_window_hours", 12),
            event_inclusion_horizon_hours=cfg.get("event_inclusion_horizon_hours", 1),
            freshness_requirement_minutes=cfg.get("freshness_requirement_minutes", 60),
            allowed_markets=cfg.get("allowed_markets", []),
            artifact_resolution_policy=cfg.get(
                "artifact_resolution_policy", "latest_compatible"
            ),
            output_profile=cfg.get("output_profile", "concise_ops"),
        )

    def compute_slot_event_window(
        self, slot_def: SlotDefinitionRecord, run_timestamp: datetime
    ) -> tuple[datetime, datetime]:
        start_time = run_timestamp + timedelta(
            hours=slot_def.event_inclusion_horizon_hours
        )
        end_time = run_timestamp + timedelta(hours=slot_def.lookahead_window_hours)
        return start_time, end_time
