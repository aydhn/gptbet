import uuid
from typing import List, Optional
from datetime import datetime, timezone
from sports_signal_bot.approvals.contracts import (
    OverrideRecord, OverrideType, OverrideScopeRecord, OverrideStatus
)

class OverrideManager:
    def __init__(self):
        self._overrides: List[OverrideRecord] = []

    def add_override(self, override: OverrideRecord) -> None:
        self._overrides.append(override)

    def get_active_overrides(self) -> List[OverrideRecord]:
        now = datetime.now(timezone.utc)
        active = []
        for ov in self._overrides:
            if ov.status == OverrideStatus.active:
                if ov.expires_at and ov.expires_at < now:
                    ov.status = OverrideStatus.expired
                else:
                    active.append(ov)
        return active

    def revoke_override(self, override_id: str) -> bool:
        for ov in self._overrides:
            if ov.override_id == override_id:
                ov.status = OverrideStatus.revoked
                return True
        return False

    def get_override(self, override_id: str) -> Optional[OverrideRecord]:
        for ov in self._overrides:
            if ov.override_id == override_id:
                return ov
        return None

def apply_override_precedence(overrides: List[OverrideRecord]) -> List[OverrideRecord]:
    """Sort overrides by precedence. Higher precedence rules apply first."""
    # Safety > Block > Manual Approvals > Default
    # We assign default precedences based on type if not explicitly set
    type_precedence = {
        OverrideType.force_freeze: 100,
        OverrideType.force_degrade: 90,
        OverrideType.block_market_temporarily: 80,
        OverrideType.force_stable_only_mode: 70,
        OverrideType.force_review_only_dispatch: 60,
        OverrideType.force_debug_dispatch: 50,
        OverrideType.allow_slot_run_once: 40,
        OverrideType.suppress_noncritical_alerts: 30
    }

    def get_score(ov: OverrideRecord) -> int:
        if ov.precedence_level > 0:
            return ov.precedence_level
        return type_precedence.get(ov.override_type, 0)

    return sorted(overrides, key=get_score, reverse=True)
