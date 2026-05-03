from datetime import datetime, timedelta
from typing import Dict, Any, List
from sports_signal_bot.remediation_lanes.contracts import (
    BoundedExecutionTokenRecord,
    BoundedExecutionTokenFamily
)

def build_bounded_execution_token(
    token_id: str,
    token_family: BoundedExecutionTokenFamily,
    lane_ref: str,
    allowed_step_families: List[str],
    allowed_scope: Dict[str, Any],
    approval_ref: str,
    valid_from: datetime,
    valid_until: datetime
) -> BoundedExecutionTokenRecord:
    return BoundedExecutionTokenRecord(
        token_id=token_id,
        token_family=token_family,
        bound_lane_ref=lane_ref,
        allowed_step_families=allowed_step_families,
        allowed_scope=allowed_scope,
        issued_from_approval_ref=approval_ref,
        valid_from=valid_from,
        valid_until=valid_until
    )

def validate_execution_token_scope(token: BoundedExecutionTokenRecord, requested_scope: Dict[str, Any]) -> bool:
    # basic check
    return all(k in token.allowed_scope and token.allowed_scope[k] == v for k, v in requested_scope.items())

def validate_execution_token_time_window(token: BoundedExecutionTokenRecord, current_time: datetime) -> bool:
    return token.valid_from <= current_time <= token.valid_until
