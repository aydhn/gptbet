from typing import List, Dict, Any, Tuple
import uuid
from .contracts import (
    ExpansionControlStateRecord, ExpansionStatus, ThrottleDirectiveRecord, PressureBand
)

def apply_global_throttle(state: ExpansionControlStateRecord, reason: str, level: str = "moderate") -> ThrottleDirectiveRecord:
    """Applies a global throttle to expansion, slowing but not pausing growth."""
    if state.global_status == ExpansionStatus.EXPANSION_NORMAL:
        state.global_status = ExpansionStatus.EXPANSION_THROTTLED

    directive = ThrottleDirectiveRecord(
        directive_id=f"thr_{uuid.uuid4().hex[:8]}",
        target_scope={"scope": "global"},
        throttle_rules={
            "max_active_growing_cohorts_reduction_pct": 50 if level == "severe" else 25,
            "block_level_2_to_3_growth": level in ["high", "severe"],
            "tighten_budget_reservations": True
        }
    )

    state.warnings.append(f"Global throttle applied ({level}): {reason}")
    return directive

def apply_family_throttle(state: ExpansionControlStateRecord, family_name: str, reason: str, level: str = "moderate") -> ThrottleDirectiveRecord:
    """Applies a throttle specific to one family."""
    directive = ThrottleDirectiveRecord(
        directive_id=f"thr_{uuid.uuid4().hex[:8]}",
        target_scope={"scope": "family", "family_name": family_name},
        throttle_rules={
            "per_family_concurrency_reduction_pct": 50 if level == "severe" else 25,
            "require_stricter_clean_windows": True
        }
    )

    state.warnings.append(f"Family throttle applied to '{family_name}' ({level}): {reason}")
    return directive

def compute_throttle_level(pressure_band: PressureBand, recent_rollbacks: int) -> str:
    """Determines the appropriate throttle level based on pressure and recent instability."""
    if pressure_band in [PressureBand.CRITICAL, PressureBand.SEVERE] or recent_rollbacks > 1:
        return "severe"
    elif pressure_band == PressureBand.HIGH or recent_rollbacks == 1:
        return "high"
    elif pressure_band == PressureBand.MODERATE:
        return "moderate"
    else:
        return "none"

def explain_throttle_decision(directive: ThrottleDirectiveRecord) -> str:
    """Provides a human-readable explanation of a throttle directive."""
    target = directive.target_scope.get("scope", "unknown")
    if target == "family":
        target = f"family '{directive.target_scope.get('family_name')}'"

    rules = [f"{k}={v}" for k, v in directive.throttle_rules.items()]
    return f"Throttle on {target}. Rules applied: {', '.join(rules)}."
